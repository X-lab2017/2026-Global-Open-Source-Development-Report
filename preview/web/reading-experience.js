/* Focused reading, disclosures and consistent chart affordances. */
(()=>{'use strict';
// Run each overview cue only while its own card or section is visible.
const motionRoots=[...document.querySelectorAll('[data-home-motion]')];
if(motionRoots.length){
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 const visibility=new Map(motionRoots.map(el=>[el,!('IntersectionObserver' in window)]));
 const sync=()=>motionRoots.forEach(el=>el.classList.toggle('is-motion-active',visibility.get(el)&&!document.hidden&&!motion.matches));
 if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{entries.forEach(e=>visibility.set(e.target,e.isIntersecting));sync()},{threshold:0});motionRoots.forEach(el=>observer.observe(el))}
 motion.addEventListener('change',sync);document.addEventListener('visibilitychange',sync);sync();
}
// Native anchors keep browser history and keyboard navigation intact.
const overviewNav=document.querySelector('.overview-page-nav');
if(overviewNav){
 const stops=[...overviewNav.querySelectorAll('a[href^="#"]')].map(a=>({a,section:document.getElementById(a.getAttribute('href').slice(1))})).filter(s=>s.section);
 let frame=0;
 function updatePosition(){frame=0;const edge=overviewNav.getBoundingClientRect().bottom+20;let active=stops[0];for(const stop of stops)if(stop.section.getBoundingClientRect().top<=edge)active=stop;for(const stop of stops){if(stop===active)stop.a.setAttribute('aria-current','location');else stop.a.removeAttribute('aria-current')}}
 function queuePosition(){if(!frame)frame=requestAnimationFrame(updatePosition)}
 window.addEventListener('scroll',queuePosition,{passive:true});window.addEventListener('resize',queuePosition);window.addEventListener('hashchange',queuePosition);window.addEventListener('load',queuePosition);queuePosition();
}
const root=document.querySelector('.foundation-reading');if(!root)return;
const zh=document.documentElement.lang.startsWith('zh'),t=(z,e)=>zh?z:e;
const figures=[...root.querySelectorAll('.foundation-figure,.chapter-table-figure')],presentations=[];
for(const figure of figures){
 const frame=figure.parentElement,launcher=frame.previousElementSibling;if(!launcher?.classList.contains('slide-launcher'))continue;
 const launch=launcher.querySelector('button'),title=figure.dataset.readingTitle||figure.querySelector('h3,h4')?.textContent||t('对照表','Reference table');
 launcher.querySelector('span').textContent=figure.dataset.readingNumber||t('对照表 · 点击探索','Reference · explore');
 const controls=document.createElement('div');controls.className='reading-chart-tools';launch.classList.add('reading-present');launch.textContent=t('⛶ 全屏演示','⛶ Present');launch.setAttribute('aria-label',(figure.dataset.readingNumber||title)+' '+t('全屏演示','Present'));controls.append(launch);launcher.append(controls);
 const dialog=[...document.querySelectorAll('dialog.explorer-presentation')].find(d=>d.getAttribute('aria-label')===(figure.querySelector('h3,h4')?.textContent||t('报告交互图全屏演示','Interactive report presentation'))&&!presentations.some(x=>x.dialog===d));if(!dialog)continue;
 dialog.classList.add('foundation-presentation');const bar=dialog.querySelector('.slide-presentation-bar'),close=bar.querySelector('button');const label=document.createElement('span');label.className='reading-present-title';label.textContent=(figure.dataset.readingNumber||'')+' · '+title;bar.insertBefore(label,close);
 presentations.push({figure,launch,dialog,close});
}
const core=presentations.filter(p=>p.figure.classList.contains('foundation-figure'));
for(const [i,p]of core.entries()){
 const nav=document.createElement('div');nav.className='reading-slide-nav';const prev=document.createElement('button'),next=document.createElement('button');prev.type=next.type='button';prev.textContent=t('← 上一图','← Previous');next.textContent=t('下一图 →','Next →');prev.disabled=i===0;next.disabled=i===core.length-1;nav.append(prev,next);p.close.before(nav);
 const move=n=>{const target=core[i+n];if(target){p.close.click();target.launch.click()}};prev.onclick=()=>move(-1);next.onclick=()=>move(1);
 p.dialog.addEventListener('keydown',e=>{if(e.target.matches('input,textarea,select'))return;if(e.key==='PageDown'||e.key==='PageUp'){e.preventDefault();move(e.key==='PageDown'?1:-1)}});
}
// Hidden references get a fresh fit when opened, including direct incoming anchors.
for(const disclosure of root.querySelectorAll('details.reading-reference'))disclosure.addEventListener('toggle',()=>{if(disclosure.open)window.dispatchEvent(new Event('resize'))});
function revealHash(){let id;try{id=decodeURIComponent(location.hash.slice(1))}catch{return}const target=document.getElementById(id);if(!target||!root.contains(target))return;let p=target.parentElement;while(p&&p!==root){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}window.dispatchEvent(new Event('resize'));requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}
window.addEventListener('hashchange',revealHash);if(location.hash)revealHash();
// The chapter sidebar shows the active section's modules, without a second book list.
const sections=[...root.querySelectorAll('.foundation-section')],groups=[...document.querySelectorAll('.focus-group')];
function activate(id){for(const g of groups){const active=g.dataset.readingSection===id;g.querySelector('.focus-subsections').hidden=!active;const a=g.querySelector('.local-section');if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')}}
if('IntersectionObserver'in window){const visible=new Map();const observer=new IntersectionObserver(entries=>{entries.forEach(e=>visible.set(e.target.id,e.isIntersecting));const current=sections.find(s=>visible.get(s.id));if(current)activate(current.id)},{rootMargin:'-100px 0px -60% 0px',threshold:0});sections.forEach(s=>observer.observe(s));}
document.querySelectorAll('.focus-group>.local-section,.foundation-route a').forEach(a=>a.addEventListener('click',()=>activate(a.getAttribute('href').slice(1))));
let hashTarget=null;try{hashTarget=document.getElementById(decodeURIComponent(location.hash.slice(1)))}catch{}activate(hashTarget?.closest('.foundation-section')?.id||'ch01-s01');
// References are available to print; restore the reader's disclosures afterwards.
let printState=[];window.addEventListener('beforeprint',()=>{printState=[...root.querySelectorAll('details.reading-reference:not(.chapter-table-reference)')].map(d=>[d,d.open]);printState.forEach(([d])=>d.open=true)});window.addEventListener('afterprint',()=>printState.forEach(([d,open])=>d.open=open));
})();
