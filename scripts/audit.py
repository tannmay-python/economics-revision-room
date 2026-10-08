"""Check publishable content, question keys and local references without dependencies."""
from pathlib import Path
import json,re,collections
root=Path(__file__).resolve().parents[1];dist=root/'dist'
d=json.loads((dist/'content.js').read_text()[12:].rstrip(';\n'))
assert len(d['chapters'])==18
chapters={c['id'] for c in d['chapters']};pages={p['id'] for c in d['chapters'] for p in c['pages']}
assert len(pages)==196
ids=[q['id'] for q in d['questions']];assert len(ids)==len(set(ids))
for c in d['chapters']:
 assert c['lessons'] and c['pages']
 for l in c['lessons']:
  assert l['source'] in pages,(c['id'],l['title'])
  assert l['body'] and l['textbookHeading']
 for p in c['pages']:
  assert (dist/p['image']).is_file(),p['image']
 for b in c['boxes']:
  assert b['page'] in pages and (dist/b['image']).is_file()
for q in d['questions']:
 assert q['chapter'] in chapters
 assert q['q'] and q['marks'] in (1,3,4,6)
 if q['type']=='mcq':
  assert len(q['options'])==4 and len(set(q['options']))==4
  assert isinstance(q['answer'],int) and 0<=q['answer']<4 and q['explanation']
 else:assert q['solution']
for source in re.findall(r"source:'([^']+)'",(dist/'exam-diagrams.js').read_text()):assert source in pages,source
for asset in re.findall(r'(?:src|href)="([^"]+)"',(dist/'index.html').read_text()):
 if not asset.startswith(('http','data:','#')):assert (dist/asset).is_file(),asset
print('PASS:',len(chapters),'chapters;',len(pages),'source spreads;',sum(len(c['lessons']) for c in d['chapters']),'lessons;',len(ids),'questions;',dict(collections.Counter(q['type'] for q in d['questions'])))
