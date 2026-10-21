/* Shared chapter affordances, layered over the reviewed per-map interactions. */
(()=>{'use strict';
const chapter=document.querySelector('.goso-chapter');if(!chapter)return;
const screens=[...chapter.querySelectorAll('.goso-screen')],all=[];
const sourceSelector='[data-dialog="world-source"],[data-dialog="comparison-source"],[data-dialog="china-source"],[data-tm-info],[data-am-source],[data-dm-source],[data-gm-source]';
const safeText=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function chapterSource(stage){
 const button=document.createElement('button');button.type='button';button.className='goso-source-trigger';button.textContent='口径与来源';button.setAttribute('aria-haspopup','dialog');stage.querySelector('.viz-heading').append(button);
 const dialog=document.createElement('dialog');dialog.className='goso-source-dialog goso-presentation';dialog.setAttribute('aria-label','第二章口径与来源');
 dialog.innerHTML='<button type="button" aria-label="关闭口径与来源">关闭 ×</button><h3>第二章 · 口径与来源</h3><p>本章来源与统计范围集中列于此处。各图时间窗不同，不将自然年、报告年度、快照和累计样本混作同一统计期。</p>';
 for(const section of chapter.querySelectorAll('.goso-reading-section')){
  const heading=document.createElement('h4');heading.textContent=section.querySelector('h2').textContent;dialog.append(heading);
  const seen=new Set();
  for(const node of section.querySelector('template[data-goso-source-notes]').content.querySelectorAll('p,li')){
   const text=node.textContent.trim();if(!text||seen.has(text))continue;seen.add(text);
   const p=document.createElement('p');p.textContent=text;dialog.append(p);
  }
 }
 document.body.append(dialog);button.addEventListener('click',()=>dialog.showModal());dialog.querySelector('button').addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>button.focus({preventScroll:true}));
}
for(const stage of screens){
 const section=stage.closest('.goso-reading-section'),fig=stage.closest('figure'),frame=stage.parentElement,launcher=frame.previousElementSibling;
 if(!launcher?.classList.contains('slide-launcher'))continue;
 const launch=launcher.querySelector('button'),title=stage.querySelector('.board-head h3,.tm-board-head h4,.am-board-head h4,.dm-board-head h4,.gm-board-head h4,.viz-heading h4')?.textContent||stage.getAttribute('aria-label');
 const hint=launcher.querySelector('span');hint.textContent='';hint.hidden=true;
 const tools=document.createElement('div');tools.className='goso-chart-tools';
 if(stage.dataset.figureId==='fig-2-1-1')chapterSource(stage);
 tools.append(launch);launcher.append(tools);launch.classList.add('goso-present-button');
 launch.textContent='⛶ 全屏演示';launch.setAttribute('aria-label',stage.dataset.figureNumber+' 全屏演示：'+title);
 // Find the dialog assigned by the shared Chapter 1 lifecycle without changing it.
 const dialog=[...document.querySelectorAll('dialog.explorer-presentation')].find(d=>d.getAttribute('aria-label')===(stage.querySelector('h3,h4')?.textContent||'报告交互图全屏演示')&&!all.some(x=>x.dialog===d));
 if(!dialog)continue;
 dialog.classList.add('goso-presentation');const bar=dialog.querySelector('.slide-presentation-bar'),close=bar.querySelector('button');
 const caption=document.createElement('span');caption.className='goso-slide-caption';caption.textContent=stage.dataset.figureNumber+' · '+title;bar.insertBefore(caption,close);
 const nav=document.createElement('div');nav.className='goso-slide-switch';const prev=document.createElement('button'),next=document.createElement('button');prev.type=next.type='button';prev.textContent='← 上一图';next.textContent='下一图 →';nav.append(prev,next);bar.insertBefore(nav,close);close.textContent='退出演示 Esc';
 all.push({stage,launch,dialog,prev,next,close});
}
all.forEach((item,i)=>{
 item.prev.disabled=i===0;item.next.disabled=i===all.length-1;
 function move(offset){const target=all[i+offset];if(!target)return;item.close.click();target.launch.click();}
 item.prev.addEventListener('click',()=>move(-1));item.next.addEventListener('click',()=>move(1));
 item.dialog.addEventListener('keydown',e=>{if(e.target.matches('input,select,textarea')||document.querySelector('.am-source-overlay:not([hidden]),.dm-source-overlay:not([hidden]),.gm-source-overlay:not([hidden])'))return;if(e.key==='PageDown'||e.key==='PageUp'){e.preventDefault();move(e.key==='PageDown'?1:-1)}});
});
// Preserve old incoming anchors while making the seven-topic overview track reading.
if('IntersectionObserver'in window){const sections=[...chapter.querySelectorAll('.goso-reading-section')],seen=new Map();const io=new IntersectionObserver(entries=>{for(const e of entries)seen.set(e.target.id,e.isIntersecting);const active=sections.find(s=>seen.get(s.id));if(!active)return;chapter.querySelectorAll('.atlas-chapter-route a').forEach(a=>{if(a.hash==='#'+active.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')})},{rootMargin:'-90px 0px -65% 0px',threshold:0});sections.forEach(s=>io.observe(s))}
})();
