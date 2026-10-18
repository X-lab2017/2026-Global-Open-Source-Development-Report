/* Stable overviews, fixed-size exploration and presentation. No remote dependencies. */
(()=>{'use strict';
const logic=document.querySelector('.logic-explorer'),osdi=document.querySelector('.osdi-explorer');
if(logic&&!logic.classList.contains('architecture-flow')){const zh=logic.dataset.lang==='zh',t=(z,e)=>zh?z:e,chapters=[...logic.querySelectorAll('[data-logic-chapter]')],frames=[...logic.querySelectorAll('[data-logic-framework]')],details=[...logic.querySelectorAll('.logic-detail')],fd=logic.querySelector('#logic-framework-detail');
function selectChapter(b){chapters.forEach(x=>x.setAttribute('aria-expanded',String(x===b)));frames.forEach(x=>x.setAttribute('aria-expanded','false'));details.forEach(x=>x.hidden=x.id!==b.getAttribute('aria-controls'));fd.hidden=true}
chapters.forEach(b=>b.addEventListener('click',()=>selectChapter(b)));
const content={sdg:[t('UN SDGs · 价值参照','UN SDGs · shared values'),t('联合国17项可持续发展目标为报告提供价值参照与研究启发；本报告的目标框架与指标并非联合国认证。','The 17 UN Sustainable Development Goals provide a value reference and research inspiration; this report’s goals and indicators are not UN certification.'),'ch01-s01',t('阅读1.1：开源与公共价值','Read 1.1: open source and public value')],osdg:[t('OSDGs · 从价值到开源发展目标','OSDGs · goals for open source'),t('四大支柱、十个维度组织开源发展的共同方向。它们交叉服务于GOSO、GOSR、GOSL、GOSM，并非与四章一一对应。','Four pillars and ten dimensions frame shared directions. They cut across all four research chapters rather than mapping one-to-one.'),'ch01-s02',t('阅读1.2：目标框架','Read 1.2: goals framework')],osdi:[t('OSDI · 从目标到可查证的观察','OSDI · verifiable observations'),t('二十九项指标定义观察对象、计算口径与证据要求，为四个研究板块提供共同的方法基础；不自动合成为单一总分。','Twenty-nine indicators define observations, calculations and evidence. They provide a shared methodology without automatically forming a composite score.'),'fig-osdi-map',t('进入OSDI指标探索','Explore OSDI indicators')]};
frames.forEach(b=>b.addEventListener('click',()=>{chapters.forEach(x=>x.setAttribute('aria-expanded','false'));frames.forEach(x=>x.setAttribute('aria-expanded',String(x===b)));details.forEach(x=>x.hidden=true);fd.replaceChildren();const [title,body,id,label]=content[b.dataset.logicFramework],h=document.createElement('h4'),p=document.createElement('p'),a=document.createElement('a');h.textContent=title;p.textContent=body;a.href='#'+id;a.textContent=label+' →';fd.append(h,p,a);fd.hidden=false}));

}
if(osdi){const zh=osdi.dataset.lang==='zh',t=(z,e)=>zh?z:e,pillars=[...osdi.querySelectorAll('[data-osdi-pillar]')],dims=[...osdi.querySelectorAll('[data-osdi-dimension]')],measures=[...osdi.querySelectorAll('.osdi-measure')],panel=osdi.querySelector('.osdi-detail'),reset=osdi.querySelector('.osdi-reset');
const evidenceRegister=JSON.parse(document.getElementById('osdi-review-evidence')?.textContent||'{}');
const records=measures.map(m=>({code:m.dataset.osdiCode,dimension:m.dataset.dimension,pillar:m.dataset.pillar,name:m.querySelector('summary b').textContent,role:m.querySelector('summary em').textContent,definition:m.querySelector('.osdi-measure-body>p').textContent,calc:m.querySelector('dl').cloneNode(true),evidence:[...m.querySelector('.osdi-evidence').querySelectorAll('p')].map(p=>p.textContent),link:null}));
// Keep canonical definitions in the document for printing; exploration replaces one fixed panel.
const source=document.createElement('div');source.className='osdi-canonical-source';source.hidden=true;measures.forEach(m=>source.append(m));osdi.append(source);panel.replaceChildren();
let currentDimension='',currentCode='',currentTab='definition';
const el=(tag,text,cls)=>{const e=document.createElement(tag);if(text)e.textContent=text;if(cls)e.className=cls;return e};
function show(code,tab='definition'){currentCode=code;currentTab=tab;const r=records.find(x=>x.code===code);if(!r)return;panel.querySelectorAll('[data-screen-indicator]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.screenIndicator===code)));let detail=panel.querySelector('.osdi-screen-reading');if(!detail){detail=el('section','','osdi-screen-reading');panel.append(detail)}detail.replaceChildren();detail.append(el('small',r.code+' · '+r.role,'osdi-screen-code'),el('h4',r.name));const tabs=el('div','','osdi-screen-tabs');for(const [key,label]of [['definition',t('定义与口径','Definition')],['evidence',t('证据状态','Evidence')]]){const b=el('button',label);b.type='button';b.setAttribute('aria-pressed',String(tab===key));b.onclick=()=>show(code,key);tabs.append(b)}detail.append(tabs);const body=el('div','','osdi-screen-body');if(tab==='definition'){body.append(el('p',r.definition),r.calc.cloneNode(true))}else{const ev=evidenceRegister[r.code];if(ev){const states=el('div','','osdi-evidence-states');for(const[key,z,e]of[['method','方法','Method'],['data','数据','Data'],['application','应用','Application'],['reproduction','复现','Reproduction']]){const card=el('div');card.append(el('small',t(z,e)),el('strong',ev[key]));states.append(card)}body.append(states,el('p',ev.note,'osdi-evidence-note'));const scope=el('p',r.code==='ModelRank'?t('月度资料：2024-07—2026-08，共 26 个月。','Monthly records: 2024-07–2026-08, 26 months.'):t('统计期与缺失规则见完整定义；观测、派生、模拟与预测逐图标识。','See the definition for periods and missing values. Observed, derived, simulated and forecast data are labelled separately.'),'osdi-evidence-scope');body.append(scope)}else r.evidence.forEach(text=>body.append(el('p',text)))}detail.append(body);}
function choose(id){currentDimension=id;panel.replaceChildren();const b=dims.find(d=>d.dataset.osdiDimension===id),rs=records.filter(r=>r.dimension===id);pillars.forEach(p=>p.setAttribute('aria-pressed',String(p.dataset.osdiPillar===rs[0].pillar)));dims.forEach(d=>d.setAttribute('aria-pressed',String(d===b)));panel.append(el('div',id+' '+b.querySelector('strong').textContent+' · '+rs.length+t('项指标',' indicators'),'osdi-breadcrumb'));const buttons=el('div','','osdi-screen-choices');rs.forEach(r=>{const b=el('button',r.name);b.type='button';b.dataset.screenIndicator=r.code;b.setAttribute('aria-pressed','false');b.onclick=()=>show(r.code);buttons.append(b)});panel.append(buttons);show(rs[0].code)}
pillars.forEach(b=>b.onclick=()=>choose(records.find(r=>r.pillar===b.dataset.osdiPillar).dimension));dims.forEach(b=>b.onclick=()=>choose(b.dataset.osdiDimension));reset.hidden=false;reset.textContent=t('初始视图','Reset');reset.onclick=()=>choose(records[0].dimension);const all=osdi.querySelector('.osdi-all');all.hidden=true;choose(records[0].dimension);
}
// Source tables remain complete in HTML. Paging replaces rows inside one frame.
for(const figure of document.querySelectorAll('.chapter-table-figure')){
 const rows=[...figure.querySelectorAll('tbody tr')],nav=figure.querySelector('.table-pagination');
 figure.style.setProperty('--slide-height',figure.dataset.slideHeight+'px');
 if(!nav)continue;
 const zh=figure.dataset.lang==='zh',size=8,pages=Math.ceil(rows.length/size);
 figure.classList.add('has-pages');nav.hidden=false;
 const status=document.createElement('span');status.setAttribute('aria-live','polite');nav.append(status);
 const controls=[];
 function choose(page){rows.forEach((r,i)=>r.hidden=i<page*size||i>=(page+1)*size);controls.forEach((b,i)=>{if(i===page)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current')});status.textContent=zh?`第 ${page*size+1}–${Math.min(rows.length,(page+1)*size)} 项 / 共 ${rows.length} 项`:`${page*size+1}–${Math.min(rows.length,(page+1)*size)} of ${rows.length} records`;}
 for(let i=0;i<pages;i++){const b=document.createElement('button');b.type='button';b.textContent=String(i+1);b.setAttribute('aria-label',zh?`第 ${i+1} 页`:`Page ${i+1}`);b.onclick=()=>choose(i);controls.push(b);nav.append(b)}
 choose(0);
}
// Expand reference tables for printing and restore each disclosure afterwards.
let printReferences=[];
window.addEventListener('beforeprint',()=>{printReferences=[...document.querySelectorAll('.chapter-table-reference')].map(d=>[d,d.open]);printReferences.forEach(([d])=>d.open=true)});
window.addEventListener('afterprint',()=>{printReferences.forEach(([d,open])=>d.open=open);printReferences=[]});
// A single presentation lifecycle for every Chapter 1 figure and table.
// The canvas dimensions stay fixed in both manuscript and body-level dialog.
for(const figure of document.querySelectorAll('.chapter-explorer,.chapter-one-visual,.chapter-table-figure,.goso-unified-canvas')){
 const zh=figure.dataset.lang==='zh',t=(z,e)=>zh?z:e,designWidth=1280,designHeight=Number(figure.dataset.slideHeight)||800;
 const frame=document.createElement('div');frame.className='explorer-slide-frame';figure.before(frame);frame.append(figure);figure.classList.add('screen-slide');
 const tools=document.createElement('div');tools.className='slide-launcher';
 const launch=document.createElement('button');launch.type='button';launch.textContent=t('⛶ 全屏演示','⛶ Present full screen');
 const hint=document.createElement('span');hint.textContent=figure.classList.contains('chapter-table-figure')?t('单屏对照 · 全屏可放大查阅','Single-screen comparison · enlarge to read'):t('一屏展示 · 点击切换 · 无需滚动','One screen · click to explore');tools.append(hint,launch);frame.before(tools);
 const dialog=document.createElement('dialog');dialog.className='explorer-presentation';const chartOwner=figure.closest('.imap-review,.tmap-review,.amap-review,.dmap-review,.gmap-review');if(chartOwner)dialog.classList.add(['imap-review','tmap-review','amap-review','dmap-review','gmap-review'].find(c=>chartOwner.classList.contains(c)));dialog.setAttribute('aria-label',figure.querySelector('h3,h4')?.textContent||t('报告交互图全屏演示','Interactive report presentation'));
 const bar=document.createElement('div');bar.className='slide-presentation-bar';const title=document.createElement('span');title.textContent=t('GOSD · 全球开源发展报告','GOSD · Global Open Source Development Report');const close=document.createElement('button');close.type='button';close.textContent=t('退出演示 Esc','Exit · Esc');bar.append(title,close);dialog.append(bar);document.body.append(dialog);
 let marker=null,oldOverflow='';
 function fit(){const full=dialog.open,w=frame.clientWidth;if(w<=0)return;const h=full?frame.clientHeight:Math.max(160,Math.min(window.innerHeight-140,620)),scale=Math.min(w/designWidth,Math.max(1,h)/designHeight);figure.style.transform=`scale(${scale})`;figure.style.left=Math.max(0,(w-designWidth*scale)/2)+'px';figure.style.top=full?Math.max(0,(h-designHeight*scale)/2)+'px':'0px';if(!full)frame.style.height=designHeight*scale+'px';}
 launch.onclick=()=>{if(dialog.open)return;marker=document.createComment('slide-position');frame.before(marker);dialog.append(frame);oldOverflow=document.documentElement.style.overflow;document.documentElement.style.overflow='hidden';dialog.showModal();fit();requestAnimationFrame(fit);close.focus()};
 function restore(){if(!marker)return;marker.replaceWith(frame);marker=null;document.documentElement.style.overflow=oldOverflow;fit();requestAnimationFrame(fit);launch.focus({preventScroll:true})}
 function leave(){if(dialog.open)dialog.close();restore()}
 window.addEventListener('beforeprint',()=>{if(dialog.open)leave()});
 close.onclick=leave;dialog.addEventListener('cancel',e=>{e.preventDefault();leave()});dialog.addEventListener('close',restore);
 // Same-page chapter links must leave the modal before navigating back to text.
 dialog.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a)return;const url=new URL(a.href,location.href);if(url.origin===location.origin&&url.pathname===location.pathname&&url.hash){leave();requestAnimationFrame(()=>document.getElementById(decodeURIComponent(url.hash.slice(1)))?.scrollIntoView())}});
 if('ResizeObserver'in window)new ResizeObserver(fit).observe(frame);window.addEventListener('resize',fit);fit();document.fonts?.ready.then(fit);
 const requested=new URLSearchParams(location.search).get('present'),key=figure===logic?'structure':figure===osdi?'osdi':figure.dataset.slideKey;if(requested===key)launch.click();
}
})();
