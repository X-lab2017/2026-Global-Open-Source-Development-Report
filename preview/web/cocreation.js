(()=>{'use strict';
 document.querySelectorAll('.cocreation').forEach(root=>{
  const data=JSON.parse(root.dataset.pillars),en=root.dataset.lang==='en',buttons=[...root.querySelectorAll('[data-pillar]')],clusters=[...root.querySelectorAll('[data-cluster]')];
  const detail=root.querySelector('.star-detail'),title=detail.querySelector('h2'),desc=detail.querySelector('p'),dims=detail.querySelector('.star-dimensions'),reset=root.querySelector('.star-reset'),motion=root.querySelector('.star-motion');
  const initial=[title.textContent,desc.textContent,dims.textContent];let selected=null,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,visible=true;
  function show(index){
   if(index===null)delete root.dataset.selected;else root.dataset.selected=String(index);
   clusters.forEach((c,i)=>c.classList.toggle('is-active',i===index));
   buttons.forEach((b,i)=>{b.setAttribute('aria-pressed',String(i===selected));b.classList.toggle('is-preview',i===index)});
   const d=index===null?initial:[data[index].title,data[index].description,data[index].dimensions];
   [title,desc,dims].forEach((el,i)=>{if(el.textContent!==d[i])el.textContent=d[i]});reset.hidden=selected===null;
  }
  buttons.forEach((b,i)=>{
   b.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse')show(i)});
   b.addEventListener('pointerleave',()=>show(selected));
   b.addEventListener('focus',()=>show(i));b.addEventListener('blur',()=>show(selected));
   b.addEventListener('click',()=>{selected=selected===i?null:i;show(selected)});
  });
  function clear(){selected=null;show(null)}reset.addEventListener('click',clear);
  root.querySelector('.star-stage').addEventListener('click',e=>{if(!e.target.closest('button,canvas'))clear()});
  root.addEventListener('keydown',e=>{if(e.key==='Escape')clear()});
  function sync(){root.classList.toggle('is-paused',paused||!visible||document.hidden);motion.setAttribute('aria-pressed',String(paused));motion.textContent=paused?(en?'Resume motion':'播放动态'):(en?'Pause motion':'暂停动态')}
  motion.addEventListener('click',()=>{paused=!paused;sync()});document.addEventListener('visibilitychange',sync);
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');reduced.addEventListener('change',e=>{paused=e.matches;sync()});
  if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync()}).observe(root);
  sync();
 });
})();
