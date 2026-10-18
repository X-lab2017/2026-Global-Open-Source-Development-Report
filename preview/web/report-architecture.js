/* One chapter map, with a clearly separate reading panel. */
(()=>{'use strict';
const fig=document.querySelector('.architecture-flow');if(!fig)return;
const zh=fig.dataset.lang==='zh',t=(z,e)=>zh?z:e;
const chapters=[...fig.querySelectorAll('[data-logic-chapter]')],details=[...fig.querySelectorAll('.logic-detail')],edges=[...fig.querySelectorAll('.architecture-edge')],start=fig.querySelector('#logic-start'),reset=fig.querySelector('[data-architecture-reset]');
function select(id){const core=['2','3','4','5'].includes(id);fig.classList.toggle('has-path',core);chapters.forEach(b=>b.setAttribute('aria-expanded',String(b.dataset.logicChapter===id)));details.forEach(d=>d.hidden=d.id!=='logic-detail-'+id);start.hidden=!!id;reset.hidden=!id;fig.dataset.selectedChapter=id||'';edges.forEach(e=>e.classList.toggle('is-active',!!id&&(!core||e.dataset.arcFrom===id||e.dataset.arcTo===id)));}
chapters.forEach(b=>b.addEventListener('click',()=>select(b.dataset.logicChapter)));reset.addEventListener('click',()=>{select('');chapters[0].focus({preventScroll:true});});
const toggle=fig.querySelector('[data-architecture-motion]'),reduced=window.matchMedia?.('(prefers-reduced-motion: reduce)');
function motion(on){const play=!!on&&!reduced?.matches;fig.classList.toggle('is-flowing',play);toggle.setAttribute('aria-pressed',String(play));toggle.textContent=play?t('暂停连线','Pause motion'):t('流动连线','Animate links');}
toggle.addEventListener('click',()=>motion(toggle.getAttribute('aria-pressed')!=='true'));reduced?.addEventListener?.('change',()=>motion(false));select('');motion(true);
})();
