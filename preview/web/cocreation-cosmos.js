/* Illustrative 3D ecosystem. Rear and foreground canvases enclose the supplied logo;
   point counts, colours and flows are not measurements or statistical comparisons. */
(()=>{'use strict';
 document.querySelectorAll('.cocreation').forEach(root=>{
 const canvas=root.querySelector('.star-cosmos'),front=root.querySelector('.star-cosmos-front');let ctx,fore;try{ctx=canvas?.getContext('2d');fore=front?.getContext('2d')}catch{}if(!ctx)return;
 root.classList.add('has-cosmos');let seed=26;const rand=()=>((seed=(seed*1664525+1013904223)>>>0)/4294967296);
 const points=[],edges=[],orbits=[],filaments=[];let yaw=.25,pitch=-.22,time=0,last=0,w=600,h=510,ratio=1,frame=0,drag=null,hover=false,targetYaw=.25,targetPitch=-.22;const focus=[1,1,1,1,1,1];
 const colors={dark:[[104,200,204],[129,175,228],[191,154,214],[176,210,126],[242,209,92],[164,206,219]],light:[[0,107,118],[36,84,140],[104,65,127],[46,104,62],[121,88,0],[52,94,115]]};
 const mobile=matchMedia('(max-width: 540px)').matches,count=mobile?1000:1800;
 // Spiral arms and a spherical envelope; local clusters add depth and texture.
 for(let i=0;i<count;i++){
  const group=i%6,t=rand(),angle=group*Math.PI/3+t*5.6+(rand()-.5)*.6,r=.12+Math.sqrt(t)*.87;
  let x=Math.cos(angle)*r,y=(rand()-.5)*(.18+t*.32),z=Math.sin(angle)*r;
  if(i%3===0){const a=rand()*Math.PI*2,v=rand()*2-1,rr=.65+rand()*.35;x=rr*Math.sqrt(1-v*v)*Math.cos(a);y=rr*v;z=rr*Math.sqrt(1-v*v)*Math.sin(a)}
  points.push({x,y,z,g:group,size:i%43===0?2.1:.35+rand()*.75});
 }
 for(let g=0;g<6;g++){const a=g*Math.PI/3+.3,c={x:Math.cos(a)*.72,y:Math.sin(a*2)*.34,z:Math.sin(a)*.72};for(let j=0;j<(mobile?35:75);j++){const u=rand()*6.28,v=rand()*2-1,r=Math.pow(rand(),.8)*.14;points.push({x:c.x+Math.cos(u)*Math.sqrt(1-v*v)*r,y:c.y+v*r,z:c.z+Math.sin(u)*Math.sqrt(1-v*v)*r,g,size:.35+rand()*.65})}}
 for(let i=0;i<(mobile?130:260);i++){
  const a=i*6;let best=-1,dist=10;for(let j=a+6;j<Math.min(a+180,count);j+=6){const p=points[a],q=points[j],d=(p.x-q.x)**2+(p.y-q.y)**2+(p.z-q.z)**2;if(d<dist&&d>.004){dist=d;best=j}}
  if(best>=0&&dist<.3)edges.push([a,best]);
 }
 for(let i=0;i<16;i++)orbits.push({tilt:rand()*Math.PI,phase:rand()*6.28,r:i<4?.34+i*.065:1+rand()*.13,g:i%6});
 for(let i=0;i<18;i++){const angle=i/18*Math.PI*2;filaments.push({angle,g:i%6,lift:rand()*.5-.25,phase:rand()})}
 function project(p){const x=p.x*Math.cos(yaw)+p.z*Math.sin(yaw),z=-p.x*Math.sin(yaw)+p.z*Math.cos(yaw),y=p.y*Math.cos(pitch)-z*Math.sin(pitch),zz=p.y*Math.sin(pitch)+z*Math.cos(pitch),s=3.5/(3.5-zz),scale=Math.min(w,h)*.365;return{x:w/2+x*s*scale,y:h/2+y*s*scale,z:zz,s};}
 function rgba(rgb,a){return `rgba(${rgb.join(',')},${a})`}
 function layer(z){return z>0&&fore?fore:ctx}
 function dot(p,r,rgb,alpha){const c=layer(p.z);c.beginPath();c.arc(p.x,p.y,r,0,Math.PI*2);c.fillStyle=rgba(rgb,alpha);c.fill()}
 function segment(a,b,rgb,alpha,width=.65){const c=layer((a.z+b.z)/2);c.beginPath();c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);c.strokeStyle=rgba(rgb,alpha);c.lineWidth=width;c.stroke()}
 function draw(){
  ctx.clearRect(0,0,w,h);if(fore)fore.clearRect(0,0,w,h);const dark=document.documentElement.dataset.theme==='dark',pal=colors[dark?'dark':'light'];
  const projected=points.map(p=>({...project(p),g:p.g,size:p.size}));
  const glow=ctx.createRadialGradient(w*.5,h*.5,2,w*.5,h*.5,w*.43);glow.addColorStop(0,dark?'#2e77982b':'#399eb00e');glow.addColorStop(1,'#279fa900');ctx.fillStyle=glow;ctx.fillRect(0,0,w,h);
  for(const o of orbits){let previous=null;for(let j=0;j<=90;j++){const a=j/90*Math.PI*2,p=project({x:Math.cos(a)*o.r,y:Math.sin(a)*Math.sin(o.tilt)*o.r,z:Math.sin(a)*Math.cos(o.tilt)*o.r});if(previous)segment(previous,p,pal[o.g],(o.r<.7?(dark?.24:.42):(dark?.13:.3))*focus[o.g],dark?.65:.9);previous=p}
   const a=time*(o.r<.7?.5:.25)+o.phase,p=project({x:Math.cos(a)*o.r,y:Math.sin(a)*Math.sin(o.tilt)*o.r,z:Math.sin(a)*Math.cos(o.tilt)*o.r});dot(p,1.5*p.s,pal[o.g],.85*focus[o.g]);}
  for(let k=0;k<edges.length;k++){const [ai,bi]=edges[k],a=projected[ai],b=projected[bi];segment(a,b,pal[a.g],(dark?(.07+(a.z+1)*.045):(.2+(a.z+1)*.07))*focus[a.g],dark?.65:.85);if(k%7===0){const t=(time*.23+k*.13)%1,p={x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t,z:a.z+(b.z-a.z)*t};dot(p,1.25,pal[a.g],.85*focus[a.g])}}
  // Curved filaments carry pulses through the core's surrounding volume.
  for(const f of filaments){const at=t=>{const r=.19+t*.73,a=f.angle+t*1.4;return project({x:Math.cos(a)*r,y:Math.sin(t*Math.PI)*f.lift,z:Math.sin(a)*r})};let prev=at(0);for(let j=1;j<=24;j++){const p=at(j/24);segment(prev,p,pal[f.g],(dark?.18:.32)*focus[f.g],dark?.7:.95);prev=p}const p=at(1-(time*.12+f.phase)%1);dot(p,1.7*p.s,pal[f.g],.9*focus[f.g]);}
  projected.sort((a,b)=>a.z-b.z).forEach(p=>{const nearCore=Math.hypot(p.x-w/2,p.y-h/2)<55,alpha=(dark?Math.min(.9,.2+(p.z+1)*.3):Math.min(.98,.42+(p.z+1)*.29))*focus[p.g]*(nearCore&&p.z>0?.55:1);dot(p,p.size*p.s*(dark?1:1.08),pal[p.g],alpha);if(dark&&p.size>2&&p.z>0)dot(p,p.size*p.s*2.5,pal[p.g],alpha*.07)});
 }
 function tick(now){frame=0;const dt=last?Math.min(.05,(now-last)/1000):.016;last=now;if(!drag&&!hover)targetYaw+=dt*.085;
  const ease=1-Math.exp(-dt*12);yaw+=(targetYaw-yaw)*ease;pitch+=(targetPitch-pitch)*ease;const selected=root.dataset.ecoSelected;focus.forEach((v,i)=>focus[i]+=((selected===undefined||+selected===i?1:.16)-v)*ease);
  time+=dt;draw();if(!root.classList.contains('is-paused'))frame=requestAnimationFrame(tick)}
 function schedule(){if(!root.classList.contains('is-paused')){if(!frame){last=0;frame=requestAnimationFrame(tick)}}else{cancelAnimationFrame(frame);frame=0;yaw=targetYaw;pitch=targetPitch;focus.forEach((v,i)=>focus[i]=root.dataset.ecoSelected===undefined||+root.dataset.ecoSelected===i?1:.16);draw()}}
 function resize(){const rect=canvas.getBoundingClientRect();w=rect.width||600;h=rect.height||510;ratio=Math.min(devicePixelRatio||1,2);for(const [el,c] of [[canvas,ctx],[front,fore]]){if(!el||!c)continue;el.width=Math.round(w*ratio);el.height=Math.round(h*ratio);c.setTransform(ratio,0,0,ratio,0,0)}draw()}
 new ResizeObserver(resize).observe(canvas);new MutationObserver(schedule).observe(root,{attributes:true,attributeFilter:['class','data-eco-selected']});new MutationObserver(draw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
 canvas.addEventListener('pointerenter',()=>{hover=true});canvas.addEventListener('pointerleave',()=>{hover=false});
 canvas.addEventListener('pointerdown',e=>{if(e.button&&e.button!==0)return;drag={x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId)});
 canvas.addEventListener('pointermove',e=>{if(!drag)return;targetYaw+=(e.clientX-drag.x)*.006;targetPitch=Math.max(-1.2,Math.min(1.2,targetPitch+(e.clientY-drag.y)*.005));drag={x:e.clientX,y:e.clientY};if(root.classList.contains('is-paused')){yaw=targetYaw;pitch=targetPitch;draw()}});
 const release=()=>{drag=null};canvas.addEventListener('pointerup',release);canvas.addEventListener('pointercancel',release);canvas.addEventListener('lostpointercapture',release);
 canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key))return;e.preventDefault();targetYaw+=e.key==='ArrowLeft'?-.12:e.key==='ArrowRight'?.12:0;targetPitch=Math.max(-1.2,Math.min(1.2,targetPitch+(e.key==='ArrowUp'?-.1:e.key==='ArrowDown'?.1:0)));if(root.classList.contains('is-paused')){yaw=targetYaw;pitch=targetPitch;draw()}});
 resize();schedule();
 });
})();
