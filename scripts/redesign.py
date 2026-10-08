from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1];p=root/'dist/content.js';d=json.loads(p.read_text()[12:].rstrip(';\n'))
flows={
'1':[('Individual choice','Micro studies a consumer, firm or market.'),('Economy-wide totals','Macro studies output, employment and prices.'),('Interdependence','Individual decisions combine; aggregate conditions feed back.')],
'2':[('Households','Supply factors of production.'),('Firms','Pay factor incomes and produce goods.'),('Spending','Households buy goods and services.'),('Circular flow','Money and real resources move in opposite directions.')],
'3':[('Domestic → national','Add NFIA.'),('Gross → net','Subtract depreciation.'),('Market price → factor cost','Subtract net indirect taxes.')],
'4':[('Production','Add value at each stage.'),('Income','Add the factor incomes generated.'),('Expenditure','Add spending on final domestic output.')],
'5':[('Barter problem','Exchange needs a double coincidence of wants.'),('Money','A commonly accepted medium connects transactions.'),('Other functions','It measures value, stores purchasing power and enables deferred payment.')],
'6':[('Initial deposit','A bank receives funds.'),('Required reserve','A fraction is retained.'),('Loan and redeposit','The remainder enters another deposit.'),('Repeated rounds','Deposits expand subject to reserve and lending conditions.')],
'7':[('Income earned','Disposable income is available.'),('Consumption','Part is spent: C = C̄ + MPC × Y.'),('Saving','The remainder: S = Y − C.')],
'8':[('Planned spending','Compare AD with output.'),('Inventories change','Unplanned stocks signal the mismatch.'),('Output adjusts','Producers change production and employment.'),('Equilibrium','Planned AD = output; planned S = I.')],
'9':[('Compare demand','Is AD consistent with full-employment output?'),('Identify the gap','Excess demand or deficient demand.'),('Choose the policy','Reduce or raise spending accordingly.'),('Explain transmission','Connect the policy to AD and the gap.')],
'10':[('Receipts','Revenue and capital receipts.'),('Expenditure','Revenue and capital spending.'),('Deficits','Measure the financing gap.'),('Policy objectives','Allocation, redistribution and stability.')],
'11':[('Foreign-currency demand','Imports and other payments abroad.'),('Foreign-currency supply','Exports and other receipts from abroad.'),('Exchange rate','Interaction of demand and supply determines the market rate.')],
'12':[('Record transactions','Residents’ dealings with the rest of the world.'),('Classify accounts','Current or capital account.'),('Identify the motive','Autonomous or accommodating.'),('Assess imbalance','Examine autonomous receipts against payments.')],
'i1':[('Colonial objective','Raw materials for Britain; a market for its goods.'),('Policy channels','Land revenue, trade rules and infrastructure.'),('Economic effects','Low productivity, deindustrialisation and income drain.'),('Independence challenge','Rebuild productive capacity and living standards.')],
'i2':[('Choose a system','A mixed economy with planned development.'),('Set the goals','Growth, modernisation, self-reliance and equity.'),('Build capacity','Land reforms, Green Revolution and industry.'),('Assess outcomes','Compare achievements with continuing weaknesses.')],
'i3':[('1991 crisis','External payments and fiscal pressures.'),('Stabilise','Address immediate imbalances.'),('Restructure','Liberalisation, privatisation and globalisation.'),('Appraise','Efficiency and choice alongside jobs and distribution.')],
'i4':[('Invest in people','Education, health, training and access.'),('Build capabilities','Knowledge, skills, health and adaptability.'),('Use them productively','Higher efficiency, participation and innovation.'),('Reinvest gains','Higher income can fund further human development.')],
'i5':[('Finance production','Timely, accessible rural credit.'),('Improve returns','Fair marketing and useful infrastructure.'),('Diversify','Allied activities and non-farm livelihoods.'),('Sustain resources','Protect soil, water and future productive capacity.')],
'i6':[('Count work correctly','Distinguish workforce, labour force and participation.'),('Examine its quality','Status, sector, pay and security.'),('Identify the gap','Unemployment, underemployment and jobless growth.'),('Connect policy','Jobs, skills, credit and protection.')]
}
for c in d['chapters']:c['flow']=flows[c['id']]
# Explicitly structured layouts retain every sentence while exposing the learning task.
for c in d['chapters']:
 if c['subject']!='macro':continue
 for l in c['lessons']:
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',l['body'])
  if len(sentences)>3:
   l['body']='\n\n'.join(' '.join(sentences[i:i+2]) for i in range(0,len(sentences),2))
c=next(c for c in d['chapters'] if c['id']=='4')
l=next(l for l in c['lessons'] if 'Expenditure method' in l['title'])
l['blocks']=[
 {'tone':'definition','title':'What it measures','text':'Final expenditure on domestically produced output during the accounting year.'},
 {'tone':'point','title':'1 · Private consumption (PFCE)','text':'Households’ private final consumption expenditure.'},
 {'tone':'point','title':'2 · Government consumption (GFCE)','text':'Government final consumption expenditure on goods and services.'},
 {'tone':'point','title':'3 · Capital formation (GDCF)','text':'Gross domestic capital formation includes fixed capital formation and change in stocks.'},
 {'tone':'point','title':'4 · Net exports (X − M)','text':'Add exports and subtract imports: imported content may already be included in consumption or investment.'},
 {'tone':'caution','title':'Exclude these','text':'Financial-asset purchases, transfers and second-hand purchases are not expenditure on current output. Include the current brokerage service.'},
 {'tone':'caution','title':'Avoid counting stocks twice','text':'Do not add change in stock again if gross domestic capital formation already includes it.'}]
p.write_text('window.ECON='+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n')
a=root/'dist/app.js';s=a.read_text()
s=s.replace(",sources:'Sources & coverage'",'')
s=re.sub(r'function sources\(\).*?\n(?=function render)', '',s,flags=re.S)
s=s.replace('{notes,visual,bank,recall,sources}','{notes,visual,bank,recall}')
s=s.replace("let t=esc(s);terms.forEach", "let t=esc(s).replace(/\\*\\*([^*]+)\\*\\*/g,'<strong>$1</strong>');terms.forEach")
start=s.index('function lessonBody(');end=s.index('\nfunction head',start)
s=s[:start]+'''function studyBlock(title,text,tone='point'){return `<section class="study-block ${tone}">${title?`<h4>${rich(title)}</h4>`:''}<p>${rich(text)}</p></section>`}
function lessonBody(l){
 if(l.blocks)return `<div class="study-grid">${l.blocks.map(b=>studyBlock(b.title,b.text,b.tone)).join('')}</div>`;
 if(l.points)return `<div class="study-grid">${l.points.map(p=>{let at=p.indexOf(':');return studyBlock(at>0?p.slice(0,at):'',at>0?p.slice(at+1).trim():p)}).join('')}</div>${studyBlock('Remember',l.takeaway,'insight')}`;
 let out=[],tiles=[];const flush=()=>{if(tiles.length){out.push(`<div class="study-grid">${tiles.join('')}</div>`);tiles=[]}};
 l.body.split(/\\n\\n/).forEach((p,i)=>{
  const pieces=p.split(/(?=\\*\\*[^*]{2,100}:\\*\\*)/).filter(Boolean);
  pieces.forEach(part=>{let m=part.match(/^\\*\\*([^*]+):\\*\\*\\s*([\\s\\S]*)$/);
   if(m){let tone=/concern|weakness|cost|limitation|challenge|neglect|unemployment|slowdown|problem|low |inadequate|deficient|bias|drain/i.test(m[1])?'caution':'point';tiles.push(studyBlock(m[1],m[2],tone))}
   else{flush();let tone=/example|case illustrates|for example/i.test(part)?'example':/do not confuse|do not treat|keep.*distinct|distinguish.*from|not automatically/i.test(part)?'insight':'prose';out.push(studyBlock('',part,tone))}
  });
 });flush();return `<div class="lesson-body">${out.join('')}</div>`
}
function chapterFlow(){return c.flow?`<section class="chapter-map"><div class="section-top"><h2>At a glance</h2><span>The chapter’s big picture</span></div><div class="chapter-flow">${c.flow.map((x,i)=>`<div class="flow-step"><div class="flow-top"><span>${String(i+1).padStart(2,'0')}</span><i></i></div><h3>${esc(x[0])}</h3><p>${esc(x[1])}</p></div>`).join('')}</div></section>`:''}
''' + s[end:]
s=s.replace('`<div class="toolbar"><button data-go="bank">Practise this chapter</button></div><details', '`<div class="toolbar"><button data-go="bank">Practise this chapter</button></div>${chapterFlow()}<details')
s=s.replace('`<p>${esc(h)}</p>`','`<a href="#lesson-${c.lessons.findIndex(l=>(l.textbookHeading||l.title)===h)}">${esc(h)}</a>`')
s=s.replace('<article class="card" id="lesson-${i}">','<article class="card lesson-card ${/box|zone|case/i.test(l.kind)?\'extension-card\':\'\'}" id="lesson-${i}">')
s=s.replace("id=c.id+'-'+card", "id=c.id+'-'+(l.key||card)")
s=s.replace("let id=c.id+'-'+card;", "let id=c.id+'-'+(c.lessons[card].key||card);")
a.write_text(s)
i=root/'dist/index.html';s=i.read_text().replace('study-only-2','complete-study-3');s=re.sub(r'<footer class="site-footer">.*?</footer>','',s);i.write_text(s)
