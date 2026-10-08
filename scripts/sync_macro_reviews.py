from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parents[1];p=root/'dist/content.js';d=json.loads(p.read_text()[12:].rstrip(';\n'));old=json.loads(subprocess.check_output(['git','show','HEAD:dist/content.js'],cwd=root).decode()[12:].rstrip(';\n'));cs={c['id']:c for c in d['chapters']}
for oc in old['chapters'][:12]:
 c=cs[oc['id']]
 for i,ol in enumerate(oc['lessons']):
  l=c['lessons'][i]
  for q in d['questions']:
   if q['chapter']==c['id'] and q['type']=='theory' and ol['title'].lower() in q['q'].lower():
    selected=[l]
    if c['id']=='1' and i==3:selected+=[x for x in c['lessons'] if x['title'].startswith('Significance of macroeconomics')]
    if c['id']=='11' and i==6:selected+=[x for x in c['lessons'] if x['title'].startswith(('Fixed exchange rate: all five demerits','Flexible exchange rate: all five'))]
    if c['id']=='12' and i==6:selected+=[x for x in c['lessons'] if x['title'].startswith('Balance of payments: all five')]
    q['solution']=selected[0]['title']+'\n'+'\n'.join(x['body'].replace('\n\n','\n') for x in selected);q['tag']='Full-topic review'
# Complete the comparative table as well as the seven explained cards.
l=cs['1']['lessons'][1]
l['comparison']['rows']=[['Concept','Individual, household, firm or industry','Economy as a whole'],['Central issue','Resource allocation; satisfaction and profit','Overall output and employment; growth with stability'],['Variables','Individual demand and supply','AD, AS, national income and total employment'],['Aggregation','Limited, such as one industry','Economy-wide'],['Agents','Individual consumers and producers','Government, RBI and other institutions'],['Method','Partial equilibrium','General equilibrium'],['Simplified assumption','Overall output and employment given','Distribution given while output and employment vary']]
p.write_text('window.ECON='+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n')
i=root/'dist/index.html';i.write_text(i.read_text().replace('complete-study-3','complete-macro-4'))
r=root/'README.md';s=r.read_text().replace('194 concept lessons (85 Macro + 109 IED)','226 concept lessons (117 Macro + 109 IED)').replace('401 original','446 original').replace('209 theory','254 theory');r.write_text(s)
