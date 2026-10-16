/* Reading regression. Requires jsdom 26; not a browser layout audit. */
const fs=require('fs'),path=require('path'),assert=require('assert'),{JSDOM}=require('jsdom');
const out=path.resolve(process.argv[2]||'dist/report'),base=process.argv[3]||'/report';
const load=rel=>fs.readFileSync(path.join(out,rel),'utf8');
const dom=new JSDOM(load('2026/zh/chapters/01/index.html'),{url:'https://www.x-lab.info'+base+'/2026/zh/chapters/01/',runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window,d=w.document,errors=[];let width=960,height=700,count=0;
const $=s=>d.querySelector(s),$$=s=>[...d.querySelectorAll(s)];
let readScroll=null;w.HTMLElement.prototype.scrollIntoView=function(){readScroll=this.id};w.ResizeObserver=class{observe(){}};
Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return this.closest('details:not([open])')?0:width}});Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return height}});
w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'))};w.addEventListener('error',e=>errors.push(e.message));
for(const name of ['chapter-visuals.js','chapter1-explorers.js','reading-experience.js'])w.eval(load(name));
function check(){assert.deepEqual(errors,[]);count++}function click(el){if(typeof el==='string')el=$(el);assert(el,'missing target');el.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));check();}
const refs=$$('.chapter-table-reference'),figs=$$('.foundation-figure'),all=$$('.foundation-figure,.chapter-table-figure');
assert.equal(refs.length,10);assert(refs.every(x=>!x.open));assert.equal(figs.length,6);assert.equal(all.length,16);assert.equal($$('.reading-module').length,12);assert.equal($$('.foundation-section').length,3);
assert.equal($$('.reading-chart-tools').length,16);assert.equal($$('.reading-slide-nav').length,6);assert.equal($$('.local-section').length,3);
function source(figure){click(figure.querySelector('.reading-inline-source')||figure.parentElement.previousElementSibling.querySelector('.reading-chart-tools button'));assert($('.reading-source-dialog').open);assert($('.reading-source-dialog div').textContent.trim().length>0);click('.reading-source-dialog>button');assert(!$('.reading-source-dialog').open);}
for(const figure of figs)source(figure);
// Core content and state survive moving between reading and presentation.
for(const vw of [1280,960,736,360]){width=vw;w.dispatchEvent(new w.Event('resize'));for(const fig of figs){const frame=fig.parentElement,launch=frame.previousElementSibling.querySelector('.reading-present'),before=fig.innerHTML;click(launch);const dialog=fig.closest('dialog');assert(dialog?.open);const scale=Number(fig.style.transform.match(/[\d.]+/)[0]);assert(scale>0&&scale*1280<=width+.01);source(fig);click(dialog.querySelector('.slide-presentation-bar>button'));assert.equal(fig.innerHTML,before);assert.equal(fig.parentElement,frame);}}
click(figs[0].parentElement.previousElementSibling.querySelector('.reading-present'));
for(let i=0;i<6;i++){assert(figs[i].closest('dialog')?.open);if(i<5)click(figs[i].closest('dialog').querySelector('.reading-slide-nav button:last-child'));}
for(let i=5;i>0;i--)click(figs[i].closest('dialog').querySelector('.reading-slide-nav button'));
figs[0].closest('dialog').dispatchEvent(new w.Event('cancel',{cancelable:true}));assert.equal($$('.foundation-reading .foundation-figure').length,6);
// Full framework, method and story exploration remains available.
for(const b of $$('[data-logic-chapter]')){click(b);assert.equal($('#'+b.getAttribute('aria-controls')).hidden,false);}
for(const b of $$('[data-logic-framework]')){click(b);assert(!$('#logic-framework-detail').hidden);}
const codes=new Set();for(const dimension of $$('[data-osdi-dimension]')){click(dimension);for(const choice of $$('[data-screen-indicator]')){click(choice);codes.add(choice.dataset.screenIndicator);const tabs=$$('.osdi-screen-tabs button');click(tabs[1]);assert($('.osdi-screen-body').textContent.trim());click(tabs[0]);assert($('.osdi-screen-body dl'));}}assert.equal(codes.size,29);
for(const attr of ['data-linux-kind','data-month','data-sdg','data-dpg','data-goal'])for(const el of $$('['+attr+']')){click(el);assert.equal(el.getAttribute('aria-pressed'),'true');}
// Closed references fit on opening, paginate, print all rows, then restore state.
for(const ref of refs){ref.open=true;ref.dispatchEvent(new w.Event('toggle'));const fig=ref.querySelector('figure');assert(Number(fig.style.transform.match(/[\d.]+/)[0])>0);source(fig);for(const b of ref.querySelectorAll('.table-pagination button'))click(b);ref.open=false;}
const oldOpen=$$('.reading-reference').map(x=>x.open);w.dispatchEvent(new w.Event('beforeprint'));assert($$('.reading-reference').every(x=>x.open));w.dispatchEvent(new w.Event('afterprint'));assert.deepEqual($$('.reading-reference').map(x=>x.open),oldOpen);
// Deep links reveal source/table disclosures rather than landing on invisible text.
for(const target of ['ch01-s03-table-59','ch01-s02-资料与口径']){w.history.replaceState(null,'','#'+encodeURIComponent(target));w.dispatchEvent(new w.Event('hashchange'));let el=d.getElementById(target);assert(el);for(let p=el.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')assert(p.open);}
for(const a of $$('.foundation-route a,.focus-group>.local-section')){click(a);assert.equal(d.querySelector('[data-reading-section="'+a.hash.slice(1)+'"] .focus-subsections').hidden,false);}
for(const a of $$('a[href]')){const u=new URL(a.href);if(u.origin!==w.location.origin)continue;assert(u.pathname.startsWith(base+'/'),u.href);const p=path.join(out,decodeURIComponent(u.pathname.slice(base.length+1)));assert(fs.existsSync(p),u.href);}
assert(!/NaN|Infinity|undefined/.test($('.foundation-reading').textContent));check();
console.log(`PASS: 6 core figures, 10 on-demand tables, 12 modules, 29 indicators, sources, 4 widths, presentation traversal, deep links and print restoration; ${count} interaction checks. DOM only.`);w.close();
