"""Check publishable content, question keys and local references without dependencies."""
from pathlib import Path
import json,re,collections
root=Path(__file__).resolve().parents[1];dist=root/'dist'
d=json.loads((dist/'content.js').read_text()[12:].rstrip(';\n'))
assert len(d['chapters'])==18
chapters={c['id'] for c in d['chapters']}
assert not any(p.suffix.lower() in ('.jpg','.jpeg','.png','.heic','.pdf','.webp') for p in dist.rglob('*')), 'Textbook/media files must not be published'
assert 'ied-pages/' not in (dist/'content.js').read_text()
assert 'data-source' not in (dist/'app.js').read_text()
ids=[q['id'] for q in d['questions']];assert len(ids)==len(set(ids))
for c in d['chapters']:
 assert c['lessons'] and 'pages' not in c and 'boxes' not in c
 for l in c['lessons']:
  assert l['body'] and l['textbookHeading']
for q in d['questions']:
 assert q['chapter'] in chapters
 assert q['q'] and q['marks'] in (1,3,4,6)
 if q['type']=='mcq':
  assert len(q['options'])==4 and len(set(q['options']))==4
  assert isinstance(q['answer'],int) and 0<=q['answer']<4 and q['explanation']
 else:assert q['solution']
for asset in re.findall(r'(?:src|href)="([^"]+)"',(dist/'index.html').read_text()):
 if not asset.startswith(('http','data:','#')):assert (dist/asset.split('?')[0]).is_file(),asset
print('PASS:',len(chapters),'chapters;',sum(len(c['lessons']) for c in d['chapters']),'lessons;',len(ids),'questions;',dict(collections.Counter(q['type'] for q in d['questions'])))
