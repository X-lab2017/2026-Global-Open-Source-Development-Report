(()=>{'use strict';
 document.querySelectorAll('.cocreation').forEach(root=>{
  const labels=JSON.parse(root.dataset.labels),en=root.dataset.lang==='en',buttons=[...root.querySelectorAll('[data-key]')],canvas=root.querySelector('.star-cosmos'),core=root.querySelector('.star-core'),book=root.querySelector('.star-book'),popover=root.querySelector('.star-popover'),link=popover.querySelector('a');
  const base=document.querySelector('meta[name="gosd-base"]')?.content||'',open={eco:false,report:false};let pinned=null,current=null,anchor=null,timer=0,down=null,moved=false,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,visible=true;let orbitFrame=0,orbitLast=0;const orbitPhase={eco:0,report:0},orbitMetrics={};
  function visual(key){const d=key?labels[key]:null;buttons.forEach(b=>{b.classList.toggle('is-active',b.dataset.key===key);b.setAttribute('aria-pressed',String(b.dataset.key===pinned))});
   if(d?.group==='eco')root.dataset.ecoSelected=String(d.index);else delete root.dataset.ecoSelected;
   root.style.setProperty('--star-accent',d?.group==='eco'?`var(--eco-${d.index})`:d?.group==='pillar'?`var(--star-${d.index})`:'var(--cyan)');
   root.querySelectorAll('.star-cluster').forEach(c=>c.classList.toggle('is-muted',d?.group==='eco'&&+c.dataset.cluster!==d.index));
  }
  function position(){if(!anchor||popover.hidden)return;const r=root.getBoundingClientRect(),a=anchor.getBoundingClientRect(),w=popover.offsetWidth||240,h=popover.offsetHeight||180;let x=a.right-r.left+10;
   if(x+w>r.width-8)x=a.left-r.left-w-10;
   let y=a.top-r.top+(a.height-h)/2;
   if(x<8){x=a.left-r.left+a.width/2-w/2;y=a.bottom-r.top+10}
   x=Math.max(8,Math.min(x,r.width-w-8));y=Math.max(8,Math.min(y,r.height-h-8));popover.style.left=x+'px';popover.style.top=y+'px';
  }
  function hide(){clearTimeout(timer);if(anchor)anchor.removeAttribute('aria-describedby');popover.hidden=true;current=null;anchor=null;visual(null);syncOrbit()}
  function show(key,el){clearTimeout(timer);if(anchor&&anchor!==el)anchor.removeAttribute('aria-describedby');const d=labels[key];current=key;anchor=el;popover.querySelector('strong').textContent=d.title;popover.querySelector('p').textContent=d.description;popover.querySelector('small').textContent=d.detail;link.hidden=!d.href;if(d.href)link.href=base+d.href;popover.hidden=false;el.setAttribute('aria-describedby','star-popover');visual(key);position();syncOrbit()}
  function restore(){if(pinned){const b=buttons.find(b=>b.dataset.key===pinned);show(pinned,b)}else hide()}
  function later(){clearTimeout(timer);timer=setTimeout(restore,180)}
  function setOpen(side,value){open[side]=value;root.classList.toggle(`is-${side}-open`,value);const panel=root.querySelector(side==='eco'?'.star-eco-labels':'.star-report-labels');panel.setAttribute('aria-hidden',String(!value));panel.querySelectorAll('button').forEach(b=>b.tabIndex=value?0:-1);
   const controls=side==='eco'?[canvas,core]:[book];controls.forEach(c=>c.setAttribute('aria-expanded',String(value)));const toggle=root.querySelector(`[data-expand="${side}"]`);toggle.setAttribute('aria-expanded',String(value));toggle.innerHTML=(value?(en?'Close exploration':'收起探索'):side==='eco'?(en?'Explore the ecosystem':'探索生态对象'):(en?'Explore the report':'探索报告结构'))+` <span aria-hidden="true">${value?'−':'＋'}</span>`;
   if(!value){if(panel.contains(document.activeElement))toggle.focus();if(pinned&&((labels[pinned].group==='eco')===(side==='eco')))pinned=null;if(current&&((labels[current].group==='eco')===(side==='eco')))hide()}
   measureOrbits();syncOrbit();
  }

  // Rotate positions on an ellipse; each label remains upright and readable.
  function measureOrbits(){for(const side of ['eco','report']){const panel=root.querySelector(side==='eco'?'.star-eco-labels':'.star-report-labels'),items=[...panel.querySelectorAll('button')],w=panel.offsetWidth||300,h=panel.offsetHeight||300,maxW=Math.max(...items.map(b=>b.offsetWidth||80)),maxH=Math.max(...items.map(b=>b.offsetHeight||34));orbitMetrics[side]={items,w,h,rx:Math.max(50,(w-maxW)/2-7),ry:Math.max(60,(h-maxH)/2-9)}}paintOrbits()}
  function paintOrbits(){for(const side of ['eco','report']){if(!open[side]||!orbitMetrics[side])continue;const m=orbitMetrics[side],angles=side==='eco'?[-90,-30,30,90,150,210]:[-135,180,135,90,-90,-45,0,45];m.items.forEach((b,i)=>{const a=angles[i]*Math.PI/180+orbitPhase[side];b.style.left=(m.w/2+Math.cos(a)*m.rx)+'px';b.style.top=(m.h/2+Math.sin(a)*m.ry)+'px'})}}
  function orbitReading(side){return current&&((labels[current].group==='eco')===(side==='eco'))}
  function orbitActive(){return !root.classList.contains('is-paused')&&['eco','report'].some(s=>open[s]&&!orbitReading(s))}
  function orbitTick(now){orbitFrame=0;const dt=orbitLast?Math.min(.05,(now-orbitLast)/1000):0;orbitLast=now;for(const side of ['eco','report'])if(open[side]&&!orbitReading(side))orbitPhase[side]+=dt*(side==='eco'?.105:-.078);paintOrbits();if(orbitActive())orbitFrame=requestAnimationFrame(orbitTick)}
  function syncOrbit(){if(orbitActive()){if(!orbitFrame){orbitLast=0;orbitFrame=requestAnimationFrame(orbitTick)}}else{cancelAnimationFrame(orbitFrame);orbitFrame=0}}
  // Web Animations changes speed without resetting the flow's phase.
  root.querySelectorAll('.star-bridge,.star-bridge-mobile').forEach(bridge=>{let leaveTimer=0;function speed(value){if(paused)value=1;bridge.dataset.flowSpeed=String(value);bridge.querySelectorAll('.star-bridge-pulse').forEach(path=>{for(const animation of path.getAnimations?.()||[]){if(animation.updatePlaybackRate)animation.updatePlaybackRate(value);else animation.playbackRate=value}})}bridge.addEventListener('pointerenter',e=>{if(e.pointerType!=='mouse')return;clearTimeout(leaveTimer);speed(3)});bridge.addEventListener('pointerleave',()=>{leaveTimer=setTimeout(()=>speed(1),120)})});

  root.querySelectorAll('[data-expand]').forEach(b=>b.addEventListener('click',()=>setOpen(b.dataset.expand,!open[b.dataset.expand])));
  core.addEventListener('click',()=>setOpen('eco',!open.eco));book.addEventListener('click',()=>setOpen('report',!open.report));
  canvas.addEventListener('pointerdown',e=>{down={x:e.clientX,y:e.clientY};moved=false});canvas.addEventListener('pointermove',e=>{if(down&&Math.hypot(e.clientX-down.x,e.clientY-down.y)>6)moved=true});canvas.addEventListener('pointerup',()=>down=null);canvas.addEventListener('pointercancel',()=>{down=null;moved=true});canvas.addEventListener('click',()=>{if(!moved)setOpen('eco',!open.eco)});canvas.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();setOpen('eco',!open.eco)}});
  buttons.forEach(b=>{const key=b.dataset.key;b.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse')show(key,b)});b.addEventListener('pointerleave',later);b.addEventListener('focus',()=>show(key,b));b.addEventListener('blur',e=>{if(!popover.contains(e.relatedTarget))later()});b.addEventListener('click',()=>{if(pinned===key){pinned=null;hide()}else{pinned=key;show(key,b)}})});
  popover.addEventListener('pointerenter',()=>clearTimeout(timer));popover.addEventListener('pointerleave',later);popover.addEventListener('focusin',()=>clearTimeout(timer));popover.addEventListener('focusout',e=>{if(!popover.contains(e.relatedTarget))later()});popover.querySelector('.star-popover-close').addEventListener('click',()=>{const returnTo=anchor;pinned=null;hide();returnTo?.focus();hide()});
  document.addEventListener('pointerdown',e=>{if(current&&!popover.contains(e.target)&&!e.target.closest('[data-key]')){pinned=null;hide()}});
  root.addEventListener('keydown',e=>{if(e.key==='Escape'){pinned=null;hide();setOpen('eco',false);setOpen('report',false);untilt()}});
  book.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||paused)return;const r=book.getBoundingClientRect(),x=Math.max(-.5,Math.min(.5,(e.clientX-r.left)/r.width-.5)),y=Math.max(-.5,Math.min(.5,(e.clientY-r.top)/r.height-.5));book.style.setProperty('--book-x',`${6-y*8}deg`);book.style.setProperty('--book-y',`${-18+x*12}deg`)});
  function untilt(){book.style.removeProperty('--book-x');book.style.removeProperty('--book-y')}book.addEventListener('pointerleave',untilt);
  function sync(){root.classList.toggle('is-paused',paused||!visible||document.hidden);if(paused)untilt();syncOrbit()}
  document.addEventListener('visibilitychange',sync);matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',e=>{paused=e.matches;sync()});
  if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync()}).observe(root);if('ResizeObserver'in window)new ResizeObserver(()=>{measureOrbits();position()}).observe(root);window.addEventListener('resize',()=>{measureOrbits();position()});
  setOpen('eco',false);setOpen('report',false);sync();
 });
})();
