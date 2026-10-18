/* Deterministic illustrative 3D coordinates; perspective projection, depth sorting,
   orbital pulses and camera interaction. No data quantities are implied. */
(()=>{'use strict';
 document.querySelectorAll('.cocreation').forEach(root=>{
 const canvas=root.querySelector('.star-cosmos');let ctx;try{ctx=canvas?.getContext('2d')}catch{}if(!ctx)return;
 root.classList.add('has-cosmos');let seed=26;const rand=()=>((seed=(seed*1664525+1013904223)>>>0)/4294967296);
 const points=[],edges=[],orbits=[];let yaw=.25,pitch=-.22,time=0,last=0,w=600,h=510,ratio=1,frame=0,drag=null;
 const colors={dark:[[104,200,204],[129,175,228],[191,154,214],[176,210,126]],light:[[8,121,132],[45,97,162],[119,83,143],[62,123,80]]};
 // Four interwoven spiral populations, with a diffuse shell and satellite clusters.
 for(let i=0;i<1200;i++){
  const group=i%4,t=rand(),angle=group*Math.PI/2+t*4.9+(rand()-.5)*.65,r=.15+Math.sqrt(t)*.83;
  let x=Math.cos(angle)*r,y=(rand()-.5)*.42,z=Math.sin(angle)*r;
  if(i%3===0){const a=rand()*Math.PI*2,v=rand()*2-1,rr=.75+rand()*.26;x=rr*Math.sqrt(1-v*v)*Math.cos(a);y=rr*v;z=rr*Math.sqrt(1-v*v)*Math.sin(a)}
  points.push({x,y,z,g:group,size:i%29===0?2.5:.45+rand()*.7});
 }
 for(let i=0;i<180;i++){
  const a=i*5;let best=-1,dist=10;for(let j=a+4;j<Math.min(a+160,points.length);j+=4){const p=points[a],q=points[j],d=(p.x-q.x)**2+(p.y-q.y)**2+(p.z-q.z)**2;if(d<dist&&d>.005){dist=d;best=j}}
  if(best>=0&&dist<.32)edges.push([a,best]);
 }
 for(let i=0;i<12;i++)orbits.push({tilt:rand()*Math.PI,phase:rand()*6.28,r:1.01+rand()*.14,g:i%4});
 function project(p){const x=p.x*Math.cos(yaw)+p.z*Math.sin(yaw),z=-p.x*Math.sin(yaw)+p.z*Math.cos(yaw),y=p.y*Math.cos(pitch)-z*Math.sin(pitch),zz=p.y*Math.sin(pitch)+z*Math.cos(pitch),s=3.5/(3.5-zz),scale=Math.min(w,h)*.365;return{x:w/2+x*s*scale,y:h/2+y*s*scale,z:zz,s};}
 function rgba(rgb,a){return `rgba(${rgb.join(',')},${a})`}
 function draw(){
  ctx.clearRect(0,0,w,h);const dark=document.documentElement.dataset.theme==='dark',pal=colors[dark?'dark':'light'],chosen=root.dataset.selected;
  const projected=points.map(p=>({...project(p),g:p.g,size:p.size}));
  const glow=ctx.createRadialGradient(w*.5,h*.5,2,w*.5,h*.5,w*.43);glow.addColorStop(0,dark?'#2e77982b':'#399eb00e');glow.addColorStop(1,'#279fa900');ctx.fillStyle=glow;ctx.fillRect(0,0,w,h);
  function strength(g){return chosen===undefined||+chosen===g?1:.12}
  for(const o of orbits){ctx.beginPath();for(let j=0;j<=100;j++){const a=j/100*Math.PI*2,p=project({x:Math.cos(a)*o.r,y:Math.sin(a)*Math.sin(o.tilt)*o.r,z:Math.sin(a)*Math.cos(o.tilt)*o.r});j?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y)}ctx.strokeStyle=rgba(pal[o.g],(dark?.17:.16)*strength(o.g));ctx.lineWidth=.65;ctx.stroke();
   const a=time*.3+o.phase,p=project({x:Math.cos(a)*o.r,y:Math.sin(a)*Math.sin(o.tilt)*o.r,z:Math.sin(a)*Math.cos(o.tilt)*o.r});ctx.beginPath();ctx.arc(p.x,p.y,1.8*p.s,0,Math.PI*2);ctx.fillStyle=rgba(dark?[242,209,92]:[136,100,0],.8*strength(o.g));ctx.fill();}
  for(let k=0;k<edges.length;k++){const [ai,bi]=edges[k],a=projected[ai],b=projected[bi],alpha=(.08+(a.z+1)*.055)*strength(a.g);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.strokeStyle=rgba(pal[a.g],alpha);ctx.lineWidth=.7;ctx.stroke();if(k%6===0){const t=(time*.25+k*.13)%1;ctx.beginPath();ctx.arc(a.x+(b.x-a.x)*t,a.y+(b.y-a.y)*t,1.5,0,Math.PI*2);ctx.fillStyle=rgba(pal[a.g],.9*strength(a.g));ctx.fill()}}
  projected.sort((a,b)=>a.z-b.z).forEach(p=>{const alpha=Math.min(.95,.25+(p.z+1)*.32)*strength(p.g);ctx.beginPath();ctx.arc(p.x,p.y,p.size*p.s,0,Math.PI*2);ctx.fillStyle=rgba(pal[p.g],alpha);ctx.fill();if(dark&&p.size>2&&p.z>0){ctx.beginPath();ctx.arc(p.x,p.y,p.size*p.s*2.8,0,Math.PI*2);ctx.fillStyle=rgba(pal[p.g],alpha*.08);ctx.fill()}});
 }
 function tick(now){frame=0;const dt=last?Math.min(.05,(now-last)/1000):0;last=now;if(!drag)yaw+=dt*.085;time+=dt;draw();if(!root.classList.contains('is-paused'))frame=requestAnimationFrame(tick)}
 function schedule(){if(!root.classList.contains('is-paused')){if(!frame){last=0;frame=requestAnimationFrame(tick)}}else{cancelAnimationFrame(frame);frame=0;draw()}}
 function resize(){const rect=canvas.getBoundingClientRect();w=rect.width||600;h=rect.height||510;ratio=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(w*ratio);canvas.height=Math.round(h*ratio);ctx.setTransform(ratio,0,0,ratio,0,0);draw()}
 new ResizeObserver(resize).observe(canvas);new MutationObserver(schedule).observe(root,{attributes:true,attributeFilter:['class','data-selected']});new MutationObserver(draw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
 canvas.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId)});
 canvas.addEventListener('pointermove',e=>{if(!drag)return;yaw+=(e.clientX-drag.x)*.006;pitch=Math.max(-1.2,Math.min(1.2,pitch+(e.clientY-drag.y)*.005));drag={x:e.clientX,y:e.clientY};draw()});
 const release=()=>{drag=null};canvas.addEventListener('pointerup',release);canvas.addEventListener('pointercancel',release);
 canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key))return;e.preventDefault();yaw+=e.key==='ArrowLeft'?-.12:e.key==='ArrowRight'?.12:0;pitch=Math.max(-1.2,Math.min(1.2,pitch+(e.key==='ArrowUp'?-.1:e.key==='ArrowDown'?.1:0)));draw()});
 root.querySelector('.star-book').addEventListener('click',e=>{const b=e.currentTarget;b.setAttribute('aria-pressed',String(b.getAttribute('aria-pressed')!=='true'))});
 root.addEventListener('keydown',e=>{if(e.key==='Escape')root.querySelector('.star-book').setAttribute('aria-pressed','false')});
 resize();schedule();
 });
})();
