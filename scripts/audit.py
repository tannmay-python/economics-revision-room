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
# Regression checks for restored substantive sections and box concepts.
coverage=json.loads((root/'scripts/ied-coverage.json').read_text())
for chapter,terms in coverage.items():
 c=next(c for c in d['chapters'] if c['id']==chapter)
 text=' '.join(l['body']+' '+l['title']+' '+l['textbookHeading'] for l in c['lessons']).lower()
 for term in terms:assert term.lower() in text,(chapter,'missing coverage',term)
 assert len(text.split())>1000,(chapter,'unexpectedly abridged')
 for l in c['lessons']:
  assert l.get('key')
  assert any(q['id']=='ied-review-'+chapter[1:]+'-'+l['key'] for q in d['questions'])
assert 'Sources & coverage' not in (dist/'app.js').read_text()
assert all(c.get('flow') for c in d['chapters'])
print('PASS: IED topic/box coverage, complete-topic practice and study navigation')
# The introductory point lists must never collapse back into a summary paragraph.
macro={c['id']:c for c in d['chapters'] if c['subject']=='macro'}
scope=next(l for l in macro['1']['lessons'] if l['title'].startswith('Scope of macroeconomics:'))
significance=next(l for l in macro['1']['lessons'] if l['title'].startswith('Significance of macroeconomics:'))
assert len(scope['blocks'])==7 and len(significance['blocks'])==7
assert all(len(b['text'].split())>=20 for b in scope['blocks'][1:]+significance['blocks'][1:])
required={
 '1':['Description of the Economy','Roadmap for Business Decisions','Policy Formulation','Global Economic Issues','Environmental Pollution and Sustainable Development','Structural Changes and Growth Path'],
 '2':['Significance: Estimation','Intersectoral Interdependence','Depreciation Reserve Fund','Desired inventory'],
 '3':['Distribution of Income','Composition of GDP','Non-monetary Exchanges','Externalities'],
 '4':['Self-consumption','Imputed Rent','Windfall','Financial-asset'],
 '5':['Dynamic Functions','High-powered Money','Minimum Reserve','CBDC'],
 '6':['Issuer of Currency','Lender of Last Resort','Moral Suasion','Repo 4','OMO 2'],
 '7':['Psychological Law','Saving to Consumption','Undefined Ratios'],
 '8':['Stocks','Ex-post Identity'],
 '9':['Reduction in Private Consumption','Increase in Private Investment','Undesired Stocks','Static GDP','Wage–Price Spiral'],
 '10':['Escheat','Special Assessment','Crowding-out','Non-plan'],
 '11':['Fixed exchange rate: all five merits','Fixed exchange rate: all five demerits','Flexible exchange rate: all five merits','Flexible exchange rate: all five demerits'],
 '12':['Market Potential','Net Factor Income from Abroad','Cross-border Prejudices']}
for ch,terms in required.items():
 text=' '.join(l['body']+' '+l['title'] for l in macro[ch]['lessons']).lower()
 for term in terms:assert term.lower() in text,(ch,term)
q=next(q for q in d['questions'] if q['id']=='q124')
assert 'Roadmap for Business Decisions' in q['solution'] and 'Theory of Employment' in q['solution']
print('PASS: Macro point lists, explanations and restored scope/significance answer')
