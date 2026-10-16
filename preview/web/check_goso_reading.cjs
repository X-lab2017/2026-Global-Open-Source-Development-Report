/* DOM regression checks for the shared chapter shell. Requires jsdom 26.
   This verifies behavior and scale arithmetic, not browser pixel layout. */
const fs=require('fs'),path=require('path'),assert=require('assert');
const {JSDOM}=require('jsdom');
const out=path.resolve(process.argv[2]||'dist/report'),base=process.argv[3]||'/report';
const html=fs.readFileSync(path.join(out,'2026/zh/chapters/02/index.html'),'utf8');
const dom=new JSDOM(html,{url:'https://www.x-lab.info'+base+'/2026/zh/chapters/02/',runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window,d=w.document,errors=[];let width=960,height=700,checks=0;
w.addEventListener('error',e=>errors.push(e.message));w.ResizeObserver=class{observe(){}};
w.HTMLElement.prototype.scrollIntoView=function(){};
Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{configurable:true,get(){return width}});
Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{configurable:true,get(){return height}});
w.HTMLDialogElement.prototype.showModal=function(){this.open=true};
w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'))};
for(const name of ['assets/imap/data.js','assets/tmap/data.js','imap.js','tmap.js','assets/amap/d3.min.js','assets/amap/data.js','amap.js','assets/dmap/data.js','dmap.js','assets/gmap/data.js','gmap.js','chapter1-explorers.js','vmap.js','cmap.js','goso-reading.js'])w.eval(fs.readFileSync(path.join(out,name),'utf8'));
const $=s=>d.querySelector(s),$$=s=>[...d.querySelectorAll(s)];
function check(){assert.deepEqual(errors,[]);checks++;}
function click(el){if(typeof el==='string')el=$(el);assert(el,'Missing click target');el.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));check();}
function change(sel,value){const el=$(sel);assert(el,sel);if(el.type==='checkbox')el.checked=value;else el.value=value;el.dispatchEvent(new w.Event('change',{bubbles:true}));check();}
const sections=$$('.goso-reading-section'),stages=$$('.goso-screen');
assert.equal(sections.length,7);assert.equal(stages.length,26);assert.equal($$('.goso-action').length,21);
assert.equal($$('.goso-chart-tools').length,26);assert.equal($$('.goso-slide-switch').length,26);
for(const [i,s]of sections.entries()){assert(s.id==='ch02-s0'+(i+1));assert.equal(s.querySelectorAll('.goso-action').length,3);assert.equal(s.querySelectorAll('.goso-section-nav a').length,4);}
for(const n of [1,2,3,4,5,6,7])for(let i=1;i<=[3,4,3,5,3,3,5][n-1];i++)assert($('#fig-2-'+n+'-'+i));
function source(stage){const button=stage.parentElement.previousElementSibling.querySelector('.goso-chart-tools button');click(button);closeSource(stage);}
function closeSource(stage){
 const overlay=stage.querySelector('.am-source-overlay:not([hidden]),.dm-source-overlay:not([hidden]),.gm-source-overlay:not([hidden])');
 if(overlay){click(overlay.querySelector('button'));assert(overlay.hidden);return;}
 const modal=$$('dialog[open]').find(x=>!x.classList.contains('explorer-presentation'));assert(modal,'Source modal should open');click(modal.querySelector('button'));assert(!modal.open);
}
// Every outside source control works, including dynamic source links at project base.
for(const stage of stages)source(stage);
// Shared lifecycle moves the same canvas; its visual state must survive both directions.
for(const viewport of [1280,960,736,360]){
 width=viewport;w.dispatchEvent(new w.Event('resize'));
 for(const stage of stages){
  const fig=stage.closest('figure'),before=stage.innerHTML;
  click(stage.parentElement.previousElementSibling.querySelector('.goso-present-button'));const dialog=stage.closest('dialog');assert(dialog?.open);
  assert(stage.style.transform.startsWith('scale('));const scale=Number(stage.style.transform.match(/[\d.]+/)[0]);
  assert(1280*scale<=width+0.01);assert((Number(stage.dataset.slideHeight)||800)*scale<=height+0.01);
  assert.equal(stage.innerHTML,before);
  click(stage.querySelector('[data-dialog="world-source"],[data-dialog="comparison-source"],[data-dialog="china-source"],[data-tm-info],[data-am-source],[data-dm-source],[data-gm-source],.goso-source-trigger'));closeSource(stage);
  click(dialog.querySelector('.slide-presentation-bar>button'));assert(!dialog.open);assert(fig.contains(stage));assert.equal(stage.innerHTML,before);
 }
}
// Traverse all 26 figures and section boundaries without scrolling the report.
click(stages[0].parentElement.previousElementSibling.querySelector('.goso-present-button'));
for(let i=0;i<stages.length;i++){const dialog=stages[i].closest('dialog');assert(dialog?.open);assert.equal(dialog.querySelector('.goso-slide-switch button').disabled,i===0);const next=dialog.querySelector('.goso-slide-switch button:last-child');assert.equal(next.disabled,i===25);if(i<25)click(next);}
for(let i=25;i>0;i--){click(stages[i].closest('dialog').querySelector('.goso-slide-switch button'));assert(stages[i-1].closest('dialog')?.open);}
const first=stages[0].closest('dialog');first.dispatchEvent(new w.Event('cancel',{cancelable:true}));assert(!first.open);assert.equal($$('.goso-reading-section .goso-screen').length,26);
// Main tabs across newer modules render without invalid numbers; paired filters stay linked.
for(const attr of ['data-world-view','data-comparison-view','data-china-view','data-tm-tab','data-am-tab','data-dm-tab','data-gm-tab']){
 const values=[...new Set($$('['+attr+']').map(el=>el.getAttribute(attr)))];
 for(const value of values){click('['+attr+'="'+value+'"]');}
}
click('[data-dm-tab="network:paired"]');
const edges=sel=>$$(sel+' [data-dm-edge]').map(el=>[el.dataset.dmEdge,el.getAttribute('aria-label')]).sort();
for(const dataset of ['flow','top']){change('[data-dm-dataset]',dataset);for(const country of ['CN','US','compare']){click('[data-dm-focus="'+country+'"]');for(const direction of ['in','out','both']){click('[data-dm-direction="'+direction+'"]');for(const domestic of [false,true]){change('[data-dm-domestic]',domestic);assert.deepEqual(edges('.dm-sankey'),edges('.dm-chord'));}}}}
for(const el of $$('.goso-screen svg'))assert(!/NaN|Infinity|undefined/.test(el.outerHTML));
for(const a of $$('.goso-reading-section a[href],dialog a[href]')){const u=new URL(a.href);if(u.origin!==w.location.origin)continue;assert(u.pathname.startsWith(base+'/'),u.href);const rel=u.pathname.slice(base.length+1);assert(fs.existsSync(path.join(out,decodeURIComponent(rel))),u.href);}
const ids=$$('[id]').map(x=>x.id);assert.equal(ids.length,new Set(ids).size);check();
console.log(`PASS: 7 sections, 26 sources/presentations, 21 actions, 4 scale widths, full next/previous traversal, paired flow filters, project-base links; ${checks} behavior assertions. DOM checks only.`);
w.close();
