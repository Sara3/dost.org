"""Prepare public media from year folders. Originals are never changed."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif', '.tif', '.tiff'}
VIDEOS = {'.mp4', '.mov', '.m4v', '.webm', '.mkv'}
VERSION = 'dost-media-1'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip()[-1600:] or 'Conversion failed')
    return result.stdout


def save_photo(source, destination, maximum):
    from PIL import Image, ImageOps
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
    except ImportError:
        pass
    with tempfile.TemporaryDirectory() as temporary:
        try:
            picture = Image.open(source)
        except (OSError, ValueError):
            if source.suffix.lower() not in {'.heic', '.heif'} or not shutil.which('sips'):
                raise RuntimeError(f'Cannot read {source.name}. HEIC needs macOS or pillow-heif.')
            converted = Path(temporary) / 'converted.png'
            run(['sips', '-s', 'format', 'png', str(source), '--out', str(converted)])
            picture = Image.open(converted)
        with picture:
            oriented = ImageOps.exif_transpose(picture)
            oriented.thumbnail((maximum, maximum), Image.Resampling.LANCZOS)
            # A fresh image strips EXIF/location data from the public copy.
            mode = 'RGBA' if 'A' in oriented.getbands() else 'RGB'
            output = Image.new(mode, oriented.size)
            output.paste(oriented.convert(mode))
            output.save(destination, 'WEBP', quality=84, method=6)
            return output.size


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                          '-show_entries', 'stream=width,height:format=duration',
                          '-of', 'json', str(path)]))


def prepare(root=ROOT):
    inbox = root / 'media'
    manifest_path = root / 'content/media-generated.json'
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    old = previous.get('cache', {})
    cache, items, reports, failures = {}, [], {}, []
    skipped = []
    for folder in sorted(inbox.iterdir()) if inbox.exists() else []:
        if not folder.is_dir() or folder.is_symlink() or not re.fullmatch(r'20\d{2}', folder.name):
            continue
        year = int(folder.name)
        metadata_path = folder / 'captions.json'
        try:
            metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
            if not isinstance(metadata, dict):
                raise ValueError('captions.json must be an object keyed by filename')
        except (ValueError, OSError) as error:
            failures.append(f'{year}/captions.json: {error}')
            continue
        for source in sorted(folder.rglob('*')):
            relative = source.relative_to(folder).as_posix()
            if not source.is_file() or source.is_symlink() or any(p.startswith('.') for p in source.relative_to(inbox).parts):
                continue
            # Do not follow symlinked directories outside the public-media inbox.
            if not source.resolve().is_relative_to(folder.resolve()):
                continue
            extension = source.suffix.lower()
            is_report = relative.lower() == 'report.pdf'
            if extension not in PHOTOS | VIDEOS and not is_report:
                if source.name != 'captions.json' and extension not in {'.md', '.txt', '.json'}:
                    skipped.append(f'{year}/{relative}')
                continue
            details = metadata.get(relative, {})
            if not isinstance(details, dict):
                failures.append(f'{year}/{relative}: caption entry must be an object')
                continue
            if details.get('include') is False:
                continue
            key = f'{year}/{relative}'
            try:
                digest = hashlib.sha256()
                with source.open('rb') as original:
                    for chunk in iter(lambda: original.read(1024 * 1024), b''):
                        digest.update(chunk)
                raw_hash = digest.hexdigest()
                signature = hashlib.sha256((VERSION + key + raw_hash).encode()).hexdigest()
                slug = re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', source.stem).encode('ascii', 'ignore').decode().lower()).strip('-')[:48] or 'media'
                stem = f'{slug}-{signature[:12]}'
                output_folder = root / 'assets/media' / str(year)
                output_folder.mkdir(parents=True, exist_ok=True)
                cached = old.get(key, {})
                if cached.get('signature') == signature and all((root / p).is_file() for p in cached.get('outputs', [])) and cached.get('outputs'):
                    entry = cached
                else:
                    print(f'Preparing {key}', flush=True)
                    with tempfile.TemporaryDirectory(dir=output_folder) as temp:
                        staging = Path(temp)
                        if is_report:
                            if not source.read_bytes().startswith(b'%PDF-'):
                                raise ValueError('report.pdf does not contain a PDF file')
                            target = staging / f'{stem}.pdf'
                            shutil.copyfile(source, target)
                            data = {'pdf': (output_folder / target.name).relative_to(root).as_posix()}
                        elif extension in PHOTOS:
                            target = staging / f'{stem}.webp'
                            width, height = save_photo(source, target, 1600)
                            thumbnail = staging / f'{stem}-thumb.webp'
                            thumb_width, _ = save_photo(target, thumbnail, 480)
                            data = {'type': 'photo', 'src': (output_folder / target.name).relative_to(root).as_posix(),
                                    'thumbnail': (output_folder / thumbnail.name).relative_to(root).as_posix(), 'thumbnailWidth': thumb_width, 'width': width, 'height': height}
                        else:
                            if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
                                raise RuntimeError('Video preparation needs FFmpeg (ffmpeg and ffprobe). See media/README.md.')
                            target = staging / f'{stem}.mp4'
                            run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(source), '-map', '0:v:0', '-map', '0:a:0?',
                                 '-vf', "scale=w='min(iw,1280)':h='min(ih,1280)':force_original_aspect_ratio=decrease:force_divisible_by=2,setsar=1",
                                 '-c:v', 'libx264', '-preset', 'medium', '-crf', '24', '-pix_fmt', 'yuv420p',
                                 '-c:a', 'aac', '-b:a', '128k', '-map_metadata', '-1', '-movflags', '+faststart', str(target)])
                            info = probe(target)
                            width, height = info['streams'][0]['width'], info['streams'][0]['height']
                            poster = staging / f'{stem}-poster.jpg'
                            run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(target), '-frames:v', '1', '-q:v', '3', str(poster)])
                            thumbnail = staging / f'{stem}-thumb.webp'
                            save_photo(poster, thumbnail, 480)
                            data = {'type': 'video', 'src': (output_folder / target.name).relative_to(root).as_posix(),
                                    'poster': (output_folder / poster.name).relative_to(root).as_posix(),
                                    'thumbnail': (output_folder / thumbnail.name).relative_to(root).as_posix(),
                                    'width': width, 'height': height, 'duration': round(float(info['format']['duration']))}
                        outputs = []
                        for output in staging.iterdir():
                            destination = output_folder / output.name
                            output.replace(destination)
                            outputs.append(destination.relative_to(root).as_posix())
                        entry = {'signature': signature, 'outputs': outputs, 'data': data}
                cache[key] = entry
                data = dict(entry['data'])
                if is_report:
                    reports[str(year)] = data['pdf']
                    continue
                title = re.sub(r'^\d+[ _.-]+', '', source.stem).replace('_', ' ').replace('-', ' ').strip()
                if re.fullmatch(r'(img|dsc|pxl|mov|vid|image|video)[ _\d.]*', title, re.I):
                    title = f'{"Photograph" if data["type"] == "photo" else "Video"} from {year}'
                title = title[:1].upper() + title[1:]
                data.update({'year': year, 'title': str(details.get('title', title or f'Dost archive · {year}')),
                             'caption': str(details.get('caption', f'From Dost’s {year} archive.')),
                             'short': str(details.get('title', title or str(year))),
                             'alt': str(details.get('alt', details.get('title', title))),
                             'order': float(details.get('order', 100)), 'sourceKey': key})
                items.append(data)
            except (OSError, ValueError, KeyError, RuntimeError, ImportError) as error:
                failures.append(f'{key}: {error}')
    if skipped:
        print('Unsupported files left unchanged: ' + ', '.join(skipped), flush=True)
    if failures:
        # Keep the previous published manifest intact if any conversion fails.
        raise RuntimeError('\n'.join(failures))
    items.sort(key=lambda item: (-item['year'], item['order'], item['sourceKey'].lower()))
    value = {'items': items, 'reports': reports, 'cache': cache}
    if value != previous:
        write_json(manifest_path, value)
    # Remove only prior generated copies owned by this manifest, never originals.
    current_outputs = {p for entry in cache.values() for p in entry['outputs']}
    for entry in old.values():
        for path in entry.get('outputs', []):
            target = root / path
            if path not in current_outputs and target.resolve().is_relative_to((root / 'assets/media').resolve()):
                target.unlink(missing_ok=True)
    print(f'Media ready: {len(items)} photos/videos and {len(reports)} PDFs. Originals unchanged.', flush=True)
    return value


def rebuild(root=ROOT):
    prepare(root)
    subprocess.run([sys.executable, str(root / 'scripts/build.py')], check=True)
    subprocess.run([sys.executable, str(root / 'scripts/package.py')], check=True)
    print('Website updated. Refresh the preview to see your changes.', flush=True)


def snapshot(root):
    return tuple((p.relative_to(root).as_posix(), p.stat().st_size, p.stat().st_mtime_ns)
                 for p in sorted((root / 'media').rglob('*'))
                 if p.is_file() and not p.is_symlink() and not any(part.startswith('.') for part in p.relative_to(root).parts))


def watch(root=ROOT):
    print('Watching media/YYYY folders. Keep this window open; press Control+C to stop.', flush=True)
    last = None
    candidate = snapshot(root)
    changed_at = time.monotonic()
    while True:
        time.sleep(2)
        current = snapshot(root)
        if current != candidate:
            candidate, changed_at = current, time.monotonic()
        elif current != last and time.monotonic() - changed_at >= 3:
            try:
                rebuild(root)
            except (RuntimeError, subprocess.CalledProcessError) as error:
                print(f'Not updated: {error}\nCorrect the file and save it again to retry.', file=sys.stderr, flush=True)
            last = current


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--watch', action='store_true', help='Rebuild after year-folder changes settle')
    parser.add_argument('--prepare-only', action='store_true', help='Prepare assets without rebuilding the website')
    arguments = parser.parse_args()
    try:
        watch() if arguments.watch else prepare() if arguments.prepare_only else rebuild()
    except KeyboardInterrupt:
        print('\nMedia watcher stopped. Your files are saved.')
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f'Not updated: {error}', file=sys.stderr)
        sys.exit(1)
