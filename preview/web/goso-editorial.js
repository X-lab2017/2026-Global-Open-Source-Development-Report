/* Progressive editorial navigation: every figure remains readable without JS. */
(()=>{'use strict';
const stages=[...document.querySelectorAll('[data-stage]')];
function activate(stage,key,save=false){
 const tabs=[...stage.querySelectorAll('[data-stage-tab]')];
 if(!tabs.some(t=>t.dataset.stageTab===key))key='primary';
 tabs.forEach(t=>{const on=t.dataset.stageTab===key;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;});
 stage.querySelectorAll('[data-stage-panel]').forEach(p=>{p.hidden=p.dataset.stagePanel!==key;});
 if(save){const u=new URL(location.href);u.searchParams.set('reading-'+stage.dataset.stage,key);history.replaceState(null,'',u);}
}
function restore(){const u=new URL(location.href);stages.forEach(s=>activate(s,u.searchParams.get('reading-'+s.dataset.stage)||'primary'));revealHash();}
function revealHash(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const target=document.getElementById(id);const panel=target?.closest('[data-stage-panel]');if(panel){activate(panel.closest('[data-stage]'),panel.dataset.stagePanel);target.scrollIntoView?.({block:'start'});}}
stages.forEach(s=>{s.querySelector('.stage-tabs').hidden=false;const tabs=[...s.querySelectorAll('[data-stage-tab]')];tabs.forEach((t,i)=>{t.addEventListener('click',()=>activate(s,t.dataset.stageTab,true));t.addEventListener('keydown',e=>{let n;if(e.key==='ArrowRight')n=(i+1)%tabs.length;else if(e.key==='ArrowLeft')n=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')n=0;else if(e.key==='End')n=tabs.length-1;else return;e.preventDefault();tabs[n].click();tabs[n].focus();});});});
restore();addEventListener('popstate',restore);addEventListener('hashchange',revealHash);
document.querySelectorAll('[data-flow-figure]').forEach(f=>{const ribbons=[...f.querySelectorAll('[data-ribbon]')];const readout=f.querySelector('[data-flow-readout]');const show=r=>{ribbons.forEach(x=>x.classList.toggle('is-muted',x!==r));readout.textContent=r.dataset.description;};let filter='all';const reset=()=>ribbons.forEach(r=>r.classList.toggle('is-muted',filter!=='all'&&r.dataset.flowTarget!==filter));f.querySelectorAll('[data-flow-filter]').forEach(b=>b.addEventListener('click',()=>{filter=b.dataset.flowFilter;f.querySelectorAll('[data-flow-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));reset();readout.textContent=filter==='all'?'全部连接 · 悬停或点选查看原表读数。':(filter==='CN'?'中国':'美国')+'项目 · 高亮对应贡献来源。';}));ribbons.forEach(r=>{['pointerenter','focus','click'].forEach(e=>r.addEventListener(e,()=>show(r)));r.addEventListener('pointerleave',reset);r.addEventListener('blur',reset);r.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show(r);}});});});
document.querySelectorAll('[data-stack-segment]').forEach(s=>{const show=()=>{const r=s.closest('figure').querySelector('[data-stack-readout]');if(r)r.textContent=s.dataset.description;};['pointerenter','focus','click'].forEach(e=>s.addEventListener(e,show));s.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show();}});});
})();
