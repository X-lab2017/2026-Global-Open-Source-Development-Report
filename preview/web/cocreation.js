(()=>{'use strict';
 document.querySelectorAll('.cocreation').forEach(root=>{
  const data=JSON.parse(root.dataset.pillars),en=root.dataset.lang==='en',buttons=[...root.querySelectorAll('[data-pillar]')],clusters=[...root.querySelectorAll('[data-cluster]')];
  const detail=root.querySelector('.star-detail'),title=detail.querySelector('h2'),desc=detail.querySelector('p'),dims=detail.querySelector('.star-dimensions'),reset=root.querySelector('.star-reset'),motion=root.querySelector('.star-motion'),explore=root.querySelector('.star-explore'),pillars=root.querySelector('.star-pillars'),canvas=root.querySelector('.star-cosmos'),book=root.querySelector('.star-book'),caption=root.querySelector('.star-report-caption');
  const initial=[title.textContent,desc.textContent,dims.textContent],short=['TALENT','SUPPLY','CONNECTION','PUBLIC VALUE'];let selected=null,expanded=false,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,visible=true,down=null,moved=false;
  function show(index){
   if(index===null)delete root.dataset.selected;else root.dataset.selected=String(index);
   clusters.forEach((c,i)=>c.classList.toggle('is-active',i===index));
   buttons.forEach((b,i)=>{b.setAttribute('aria-pressed',String(i===selected));b.classList.toggle('is-preview',i===index)});
   const d=index===null?initial:[data[index].title,data[index].description,data[index].dimensions];
   [title,desc,dims].forEach((el,i)=>{if(el.textContent!==d[i])el.textContent=d[i]});reset.hidden=selected===null;
   caption.textContent=index===null?'GOSD / 2026':`X${index+1} / ${short[index]}`;
  }
  function setExpanded(value){
   expanded=value;root.classList.toggle('is-exploring',expanded);pillars.setAttribute('aria-hidden',String(!expanded));explore.setAttribute('aria-expanded',String(expanded));canvas.setAttribute('aria-expanded',String(expanded));
   explore.innerHTML=(expanded?(en?'Close exploration':'收起四个支柱'):(en?'Explore four pillars':'探索四个支柱'))+` <span aria-hidden="true">${expanded?'−':'＋'}</span>`;
   buttons.forEach(b=>b.tabIndex=expanded?0:-1);
   if(!expanded){if(buttons.includes(document.activeElement))explore.focus();selected=null;show(null)}
  }
  explore.addEventListener('click',()=>setExpanded(!expanded));
  canvas.addEventListener('pointerdown',e=>{down={x:e.clientX,y:e.clientY};moved=false});
  canvas.addEventListener('pointermove',e=>{if(down&&Math.hypot(e.clientX-down.x,e.clientY-down.y)>6)moved=true});
  canvas.addEventListener('pointerup',()=>{down=null});canvas.addEventListener('pointercancel',()=>{down=null;moved=true});
  canvas.addEventListener('click',()=>{if(!moved)setExpanded(!expanded)});
  canvas.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();setExpanded(!expanded)}});
  buttons.forEach((b,i)=>{
   b.addEventListener('pointerenter',e=>{if(expanded&&e.pointerType==='mouse')show(i)});
   b.addEventListener('pointerleave',()=>show(selected));
   b.addEventListener('focus',()=>{if(expanded)show(i)});b.addEventListener('blur',()=>show(selected));
   b.addEventListener('click',()=>{if(!expanded)return;selected=selected===i?null:i;show(selected)});
  });
  reset.addEventListener('click',()=>{selected=null;show(null)});
  book.addEventListener('click',()=>book.setAttribute('aria-pressed',String(book.getAttribute('aria-pressed')!=='true')));
  book.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||paused)return;const r=book.getBoundingClientRect(),x=Math.max(-.5,Math.min(.5,(e.clientX-r.left)/r.width-.5)),y=Math.max(-.5,Math.min(.5,(e.clientY-r.top)/r.height-.5));book.style.setProperty('--book-x',`${6-y*10}deg`);book.style.setProperty('--book-y',`${-18+x*15}deg`)});
  function untilt(){book.style.removeProperty('--book-x');book.style.removeProperty('--book-y')}
  book.addEventListener('pointerleave',untilt);
  root.addEventListener('keydown',e=>{if(e.key==='Escape'){setExpanded(false);book.setAttribute('aria-pressed','false');untilt()}});
  function sync(){root.classList.toggle('is-paused',paused||!visible||document.hidden);motion.setAttribute('aria-pressed',String(paused));motion.textContent=paused?(en?'Resume motion':'播放动态'):(en?'Pause motion':'暂停动态');if(paused)untilt()}
  motion.addEventListener('click',()=>{paused=!paused;sync()});document.addEventListener('visibilitychange',sync);
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');reduced.addEventListener('change',e=>{paused=e.matches;sync()});
  if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync()}).observe(root);
  setExpanded(false);sync();
 });
})();
