"""Integration checks for the year-folder importer; fixtures never enter the site."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from PIL import Image
from prepare_media import prepare


class MediaImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dost-media-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.year = self.root / 'media/2025'
        self.year.mkdir(parents=True)
        self.photo = self.year / '01-class portrait.jpg'
        image = Image.new('RGB', (2400, 1200), '#d6bd93')
        exif = image.getexif()
        exif[274] = 6
        image.save(self.photo, exif=exif)
        self.original_hash = hashlib.sha256(self.photo.read_bytes()).hexdigest()

    def test_orientation_dimensions_metadata_cache_and_caption_edit(self):
        result = prepare(self.root)
        item = result['items'][0]
        self.assertEqual((item['width'], item['height']), (800, 1600))
        self.assertEqual(item['year'], 2025)
        self.assertEqual(item['title'], 'Class portrait')
        output = self.root / item['src']
        with Image.open(output) as image:
            self.assertFalse(image.getexif())
        self.assertEqual(hashlib.sha256(self.photo.read_bytes()).hexdigest(), self.original_hash)
        timestamp = output.stat().st_mtime_ns
        (self.year / 'captions.json').write_text(json.dumps({self.photo.name: {'title': 'A verified title', 'alt': 'Accurate description'}}))
        updated = prepare(self.root)
        self.assertEqual(updated['items'][0]['title'], 'A verified title')
        self.assertEqual(output.stat().st_mtime_ns, timestamp)
        self.assertEqual(updated['items'][0]['alt'], 'Accurate description')

    def test_small_photos_exclusion_and_failed_import_keep_previous_manifest(self):
        small = self.year / 'small.png'
        Image.new('RGB', (80, 60)).save(small)
        initial = prepare(self.root)
        self.assertEqual(next(i for i in initial['items'] if i['title']=='Small')['width'], 80)
        manifest = self.root / 'content/media-generated.json'
        before = manifest.read_bytes()
        (self.year / 'broken.jpg').write_bytes(b'not an image')
        with self.assertRaises(RuntimeError):
            prepare(self.root)
        self.assertEqual(manifest.read_bytes(), before)
        (self.year / 'broken.jpg').unlink()
        (self.year / 'captions.json').write_text(json.dumps({self.photo.name: {'include': False}}))
        updated = prepare(self.root)
        self.assertEqual(len(updated['items']), 1)
        excluded = next(i for i in initial['items'] if i['title']=='Class portrait')
        self.assertFalse((self.root / excluded['src']).exists())
        self.assertTrue(self.photo.exists())

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
    def test_video_and_report_import(self):
        movie = self.year / '02-distribution.mov'
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i','color=c=green:s=1920x1080:r=12',
                        '-t','0.5','-c:v','libx264','-pix_fmt','yuv420p',str(movie)],check=True)
        Image.new('RGB', (100, 100)).save(self.year/'report.pdf', 'PDF')
        result = prepare(self.root)
        video = next(i for i in result['items'] if i['type']=='video')
        self.assertEqual((video['width'],video['height']), (1280,720))
        for field in ('src','poster','thumbnail'):
            self.assertTrue((self.root/video[field]).is_file())
        self.assertTrue((self.root/result['reports']['2025']).read_bytes().startswith(b'%PDF-'))
        timestamp = (self.root/video['src']).stat().st_mtime_ns
        prepare(self.root)
        self.assertEqual((self.root/video['src']).stat().st_mtime_ns, timestamp)


if __name__ == '__main__':
    unittest.main()
