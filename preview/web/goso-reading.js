/* Shared chapter affordances, layered over the reviewed per-map interactions. */
(()=>{'use strict';
const chapter=document.querySelector('.goso-chapter');if(!chapter)return;
const screens=[...chapter.querySelectorAll('.goso-screen')],all=[];
const sourceSelector='[data-dialog="world-source"],[data-dialog="comparison-source"],[data-dialog="china-source"],[data-tm-info],[data-am-source],[data-dm-source],[data-gm-source]';
const safeText=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const sourceNotes={1:'本节的全球与中国地图使用 2025 自然年 GitHub 同源快照。Gitee＋AtomGit 补充为条件情景；历史五年表与当前地图分别标注，不混合推算。',2:'本节分别保留自然年 GitHub 地图、报告五域序列与项目流向样本。地球中的机制示意、实测分布、样本流向和估算层分别标注，不混合计算。'};
function fallbackSource(stage,section,fig){
 const button=document.createElement('button');button.type='button';button.className='goso-source-trigger';button.textContent='口径与来源';button.setAttribute('aria-haspopup','dialog');stage.querySelector('.viz-heading')?.append(button);
 const dialog=document.createElement('dialog');dialog.className='goso-source-dialog goso-presentation';dialog.setAttribute('aria-label','图表口径与来源');dialog.innerHTML='<button type="button" aria-label="关闭口径与来源">关闭 ×</button><h3>口径与来源</h3><div></div>';document.body.append(dialog);
 const close=dialog.querySelector('button');let trigger=button;
 button.addEventListener('click',()=>{
  const caption=fig.querySelector('figcaption'),note=sourceNotes[section.dataset.mapIndex]||'',links=[...fig.querySelectorAll('a[href]')].filter(a=>!a.getAttribute('href').startsWith('#'));
  const uniq=[...new Map(links.map(a=>[a.href,a])).values()];
  dialog.querySelector('h3').textContent=stage.dataset.figureNumber+' · 口径与来源';dialog.querySelector('div').innerHTML='<p>'+safeText(note)+'</p>'+(caption?'<p>'+safeText(caption.textContent.trim())+'</p>':'')+'<div class="goso-source-links">'+uniq.map(a=>a.outerHTML).join('')+'</div><p>完整的指标反馈与待补证据保留在本节末尾。</p>';
  trigger=document.activeElement;dialog.showModal();close.focus();
 });
 close.addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>trigger?.focus({preventScroll:true}));return button;
}
for(const stage of screens){
 const section=stage.closest('.goso-reading-section'),fig=stage.closest('figure'),frame=stage.parentElement,launcher=frame.previousElementSibling;
 if(!launcher?.classList.contains('slide-launcher'))continue;
 const launch=launcher.querySelector('button'),title=stage.querySelector('.board-head h3,.tm-board-head h4,.am-board-head h4,.dm-board-head h4,.gm-board-head h4,.viz-heading h4')?.textContent||stage.getAttribute('aria-label');
 const hint=launcher.querySelector('span');hint.textContent=stage.dataset.figureNumber+' · 点击探索，演示放大';
 const tools=document.createElement('div');tools.className='goso-chart-tools';const source=document.createElement('button');source.type='button';source.textContent='口径与来源';source.setAttribute('aria-haspopup','dialog');
 const nativeSource=stage.querySelector(sourceSelector)||fallbackSource(stage,section,fig);source.addEventListener('click',()=>nativeSource.click());tools.append(source,launch);launcher.append(tools);launch.classList.add('goso-present-button');
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
