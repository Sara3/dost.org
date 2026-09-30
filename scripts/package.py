"""Package the current website and editable source for laptop use."""
from pathlib import Path
import zipfile
import json
root=Path(__file__).resolve().parent.parent
files=list(root.glob('*.html'))+[root/'README.md']+list(root.glob('*.command'))
for folder in ('assets','content','reports','team','scripts','api','docs'):
 files.extend(p for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('desktop.ini','.DS_Store') and not p.is_relative_to(root/'assets/media'))
manifest=root/'content/media-generated.json'
if manifest.exists():
 files.extend(root/p for entry in json.loads(manifest.read_text()).get('cache',{}).values() for p in entry['outputs'])
files.append(root/'media/README.md')
files.append(root/'downloads/dost-report-archive.zip')
with zipfile.ZipFile(root/'downloads/dost-website.zip','w',zipfile.ZIP_DEFLATED) as archive:
 for year in range(2018,2027):
  archive.writestr(f'dost-website/media/{year}/', '')
 for path in files:
  archive.write(path,Path('dost-website')/path.relative_to(root))
print(f'Packaged {len(files)} website files.')
