/* Same-origin presentation bridge; no independent chart or dataset implementation. */
(()=>{'use strict';if(!document.body.classList.contains('deck-embed-mode'))return;
const origin=location.origin,params=new URLSearchParams(location.search),send=data=>{if(parent!==window)parent.postMessage({channel:'gosd-chart',...data},origin)};
let current=null,currentFigure=null,replaying=false,actions=[],lastTrigger=null;
const allowed=[...document.querySelectorAll('.foundation-figure,.goso-reading-figure')].map(x=>x.id);
const stages=new Map(allowed.map(id=>{const fig=document.getElementById(id);return [id,fig.matches('.chapter-explorer,.chapter-one-visual')?fig:fig.querySelector('.goso-screen')];}));
function stageFor(id){return stages.get(id);}
function source(){const s=stageFor(currentFigure);s?.querySelector('.reading-inline-source,[data-dialog="world-source"],[data-dialog="comparison-source"],[data-dialog="china-source"],[data-tm-info],[data-am-source],[data-dm-source],[data-gm-source],.goso-source-trigger')?.click();}
function theme(value){document.documentElement.dataset.theme=value==='dark'?'dark':'light';document.dispatchEvent(new Event('gosdthemechange'));}
function safeTarget(selector){if(typeof selector!=='string'||selector.length>700)return null;try{const el=current?.querySelector(selector);if(!el||el.closest('.slide-presentation-bar')||el.matches('a'))return null;return el.matches('button,input,select,[role="button"],[data-country],[data-dm-edge],svg [data-region]')||[...el.attributes].some(a=>a.name.startsWith('data-'))?el:null;}catch{return null;}}
function replay(list){replaying=true;for(const a of Array.isArray(list)?list.slice(-60):[]){if(!Array.isArray(a)||a.length>3)continue;const el=safeTarget(a[0]);if(!el)continue;if(a[1]==='change'&&el.matches('input,select')){if(el.type==='checkbox')el.checked=!!a[2];else el.value=String(a[2]??'');el.dispatchEvent(new Event('change',{bubbles:true}));}else if(a[1]==='click')el.dispatchEvent(new MouseEvent('click',{bubbles:true}));}replaying=false;}
function show(id,list){if(!allowed.includes(id))return;const stage=stageFor(id);if(!stage)return;
 if(current&&currentFigure!==id){for(const d of document.querySelectorAll('dialog[open]'))if(d!==current)d.close();for(const o of current.querySelectorAll('.am-source-overlay:not([hidden]),.dm-source-overlay:not([hidden]),.gm-source-overlay:not([hidden])'))o.querySelector('button')?.click();current.querySelector('.slide-presentation-bar>button')?.click();}
 currentFigure=id;
 if(!stage.closest('dialog[open]')){const bar=stage.parentElement.previousElementSibling;bar?.querySelector('.reading-present,.goso-present-button')?.click();}
 current=stage.closest('dialog.explorer-presentation');if(!current)return;
 if(Array.isArray(list)){actions=list.slice(-60);replay(actions);}else actions=[];
 window.dispatchEvent(new Event('resize'));
 send({type:'ready',figure:id});
}
function selectorFor(el){if(el.id)return '#'+CSS.escape(el.id);const attrs=[...el.attributes].filter(a=>a.name.startsWith('data-')&&!['data-lang','data-figure-id','data-figure-number','data-map-code','data-slide-height'].includes(a.name));
 for(const a of attrs){const s=el.tagName.toLowerCase()+'['+a.name+'='+JSON.stringify(a.value)+']';try{if(current.querySelectorAll(s).length===1)return s;}catch{}}
 const label=el.getAttribute('aria-label');if(label){const s=el.tagName.toLowerCase()+'[aria-label='+JSON.stringify(label)+']';if(current.querySelectorAll(s).length===1)return s;}
 // Deterministic DOM path is only a fallback for unlabeled generated controls.
 const chain=[];for(let n=el;n&&n!==current;n=n.parentElement){if(!n.parentElement)return null;const siblings=[...n.parentElement.children].filter(x=>x.tagName===n.tagName);chain.unshift(n.tagName.toLowerCase()+':nth-of-type('+(siblings.indexOf(n)+1)+')');}return chain.join('>');}
function record(e){if(replaying||!current||!current.contains(e.target))return;let el=e.target;if(e.type==='click'){for(;el&&el!==current;el=el.parentElement)if(el.matches('button,[role="button"]')||[...el.attributes].some(a=>a.name.startsWith('data-')))break;}
 if(!el||el===current||el.closest('.slide-presentation-bar')||el.matches('a')||el.closest('.am-source-overlay,.dm-source-overlay,.gm-source-overlay'))return;
 if(el.matches('.reading-inline-source,.goso-source-trigger,[data-dialog],[data-tm-info],[data-am-source],[data-dm-source],[data-gm-source]'))return;
 if(e.type==='click'&&el.matches('input,select'))return;
 const selector=selectorFor(el);if(!selector||selector.length>700)return;const row=[selector,e.type];if(e.type==='change')row.push(el.type==='checkbox'?el.checked:el.value);
 if(JSON.stringify(actions.at(-1))!==JSON.stringify(row))actions.push(row);actions=actions.slice(-60);send({type:'state',figure:currentFigure,actions});}
document.addEventListener('click',record,true);document.addEventListener('change',record,true);
document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a)return;const u=new URL(a.href,location.href);if(!['http:','https:'].includes(u.protocol))return;if(u.origin===origin&&u.pathname===location.pathname){u.pathname=(document.querySelector('meta[name="gosd-base"]')?.content||'')+'/2026/zh/chapters/'+(currentFigure?.startsWith('fig-2-')||currentFigure?.startsWith('fig-vmap')||currentFigure?.startsWith('fig-cmap')?'02':'01')+'/';}if(a.hasAttribute('download'))return;e.preventDefault();e.stopPropagation();send({type:'link',url:u.href});},true);
document.addEventListener('keydown',e=>{if(e.target.matches?.('input,select,textarea'))return;const extra=[...document.querySelectorAll('dialog[open]')].some(x=>x!==current)||current?.querySelector('.am-source-overlay:not([hidden]),.dm-source-overlay:not([hidden]),.gm-source-overlay:not([hidden])');if(extra)return;
 const offset=e.key==='PageDown'?1:e.key==='PageUp'?-1:((!e.target.closest?.('button,[role="button"],svg,canvas')||e.target.closest?.('.slide-presentation-bar'))&&(e.key==='ArrowRight'||e.key==='ArrowLeft')?(e.key==='ArrowRight'?1:-1):0);if(offset){e.preventDefault();e.stopImmediatePropagation();send({type:'navigate',offset});}
 if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();send({type:'unfocus'});}
},true);
window.addEventListener('message',e=>{if(e.origin!==origin||e.source!==parent||e.data?.channel!=='gosd-deck')return;const m=e.data;if(m.type==='show')show(m.figure,m.actions);if(m.type==='source')source();if(m.type==='theme')theme(m.value);if(m.type==='pause'){for(const b of document.querySelectorAll('[data-globe-motion][aria-pressed="true"],[data-globe-rotate][aria-pressed="true"]'))b.click();}if(m.type==='reset'){actions=[];location.reload();}});
// All deferred report initializers precede this bridge; module/WebGL can finish lazily.
theme(params.get('theme'));show(params.get('figure'));send({type:'loaded'});
})();
