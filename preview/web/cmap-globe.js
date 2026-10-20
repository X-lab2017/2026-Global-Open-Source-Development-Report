import * as THREE from './assets/cmap/vendor/three.module.js';
import {OrbitControls} from './assets/cmap/vendor/OrbitControls.js';
import {latLon,arcPoint,localLoop} from './cmap-globe-math.mjs';
import {selectedFlows,visualWidth} from './cmap-globe-analysis.mjs';
const root=document.querySelector('[data-cm-globe]'),dataNode=document.getElementById('cmap-data');
if(root&&dataNode){
 const D=JSON.parse(dataNode.textContent),F=D.flows,by=Object.fromEntries(D.countries.map(r=>[r.id,r])),q=s=>root.querySelector(s),stage=q('[data-globe-stage]'),hint=q('[data-globe-hint]'),tooltip=q('[data-globe-tooltip]');
 const exact=v=>v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),press=(name,value)=>root.querySelectorAll(`[data-${name}]`).forEach(b=>b.setAttribute('aria-pressed',String(b.getAttribute('data-'+name)===String(value))));
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches,maximum=Math.max(...F.edges.map(e=>e.value));
 let target='all',filter='all',multiplier=3,selected=null,page=0,motion=!reduced,renderer,scene,camera,controls,earth,land,flowGroup,raf=0,clock=0,lastTime=0,visible=true,started=false,failed=false,cameraGoal=null;
 let curves=[],particles=[],pickers=[];const nodes=[];const pageSize=5;
 const rows=()=>selectedFlows(F,{target,filter});
 function stat(title,value,note){return `<span class="cm-globe-stat"><small>${title}</small><strong>${value}</strong><em>${note}</em></span>`;}
 function updateText(){
  const rr=rows(),pages=Math.max(1,Math.ceil(rr.length/pageSize));page=Math.min(page,pages-1);press('globe-target',target);press('globe-filter',filter);press('globe-enhance',multiplier);
  q('[data-globe-badge]').textContent=`实际来源样本 · ${rr.length} 条关系 · ${multiplier===1?'原始线宽':'视觉增强 ×3'}`;
  q('[data-globe-list]').innerHTML=rr.slice(page*pageSize,(page+1)*pageSize).map(e=>`<button type="button" data-globe-edge="${e.id}" aria-pressed="${selected===e.id}"><span>${esc(by[e.source].name)} → ${esc(by[e.target].name)}</span><b>${exact(e.value)}</b></button>`).join('');
  q('[data-globe-page-status]').textContent=`${page+1} / ${pages} · ${rr.length} 条`;
  q('[data-globe-page="prev"]').disabled=page===0;q('[data-globe-page="next"]').disabled=page===pages-1;
  const edge=F.edges.find(e=>e.id===selected);
  q('[data-globe-detail]').innerHTML=edge?`<strong>${esc(by[edge.source].name)} → ${esc(by[edge.target].name)}项目</strong><p>${exact(edge.value)} OpenRank · 原表份额 ${edge.share_pct.toFixed(2)}%</p>`:'<strong>20 条来源记录，14 个国家</strong><p>列表、连线与读数联动。单位：OpenRank。</p>';
  const a=F.targets.CN,b=F.targets.US;
  q('[data-globe-bottom]').innerHTML=stat('中国项目 · 本土贡献',a.local_share_pct.toFixed(2)+'%','来源前十已列 '+a.observed_share_pct.toFixed(2)+'%')+stat('美国项目 · 本土贡献',b.local_share_pct.toFixed(2)+'%','来源前十已列 '+b.observed_share_pct.toFixed(2)+'%')+stat('中国→美国项目 / 反向','12.3 倍','仅限本表中两条定向关系');
  q('[data-globe-motion]').setAttribute('aria-pressed',String(motion));q('[data-globe-motion]').textContent=motion?'暂停流动':'播放流动';
 }
 function schedule(){if(!raf&&renderer&&visible&&!document.hidden)raf=requestAnimationFrame(draw);}
 function draw(time=0){raf=0;if(!renderer||!visible||document.hidden)return;const dt=lastTime?Math.min(50,Math.max(0,time-lastTime)):0;lastTime=time;if(motion)clock+=dt/1000;
  for(const p of particles)if(p.group.visible)p.mesh.position.copy(p.curve.getPoint((clock*.10+p.offset)%1));
  if(cameraGoal){camera.position.lerp(cameraGoal,.12);if(camera.position.distanceTo(cameraGoal)<.008)cameraGoal=null;}
  controls.update();renderer.render(scene,camera);if(motion||controls.autoRotate||cameraGoal)schedule();
 }
 function updateScene(){updateText();tooltip.hidden=true;if(!scene)return;const ids=new Set(rows().map(e=>e.id));
  for(const e of curves){e.group.visible=ids.has(e.row.id);e.material.opacity=selected?(selected===e.row.id?.95:.16):.68;}
  const countries=new Set(rows().flatMap(e=>[e.source,e.target]));for(const n of nodes)n.visible=countries.has(n.userData.id);schedule();
 }
 function choose(id){selected=id;const rr=rows();page=Math.floor(Math.max(0,rr.findIndex(e=>e.id===id))/pageSize);updateScene();
  const e=F.edges.find(e=>e.id===id);if(camera&&e){const a=latLon(...by[e.source].coordinates),b=latLon(...by[e.target].coordinates);cameraGoal=new THREE.Vector3(...arcPoint(a,b,.5,0)).normalize().multiplyScalar(camera.position.length());schedule();}
 }
 root.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
  if(b.dataset.globeTarget){target=b.dataset.globeTarget;selected=null;page=0;updateScene();}
  else if(b.dataset.globeFilter){filter=b.dataset.globeFilter;selected=null;page=0;updateScene();}
  else if(b.dataset.globeEnhance){multiplier=Number(b.dataset.globeEnhance);if(renderer)buildFlows();updateScene();}
  else if(b.dataset.globeEdge)choose(b.dataset.globeEdge);
  else if(b.dataset.globePage){page+=b.dataset.globePage==='next'?1:-1;updateText();}
  else if(b.hasAttribute('data-globe-motion')){motion=!motion;updateText();schedule();}
  else if(b.hasAttribute('data-globe-rotate')&&controls){controls.autoRotate=!controls.autoRotate;b.setAttribute('aria-pressed',String(controls.autoRotate));b.textContent=controls.autoRotate?'暂停旋转':'自动旋转';schedule();}
  else if(b.hasAttribute('data-globe-reset')){selected=null;target='all';filter='all';page=0;if(controls){controls.autoRotate=false;cameraGoal=new THREE.Vector3(...latLon(5,62,3.25));const auto=q('[data-globe-rotate]');auto.setAttribute('aria-pressed','false');auto.textContent='自动旋转';}updateScene();}
 });
 stage.addEventListener('keydown',e=>{if(!camera||e.target!==stage||!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-'].includes(e.key))return;e.preventDefault();cameraGoal=null;const s=new THREE.Spherical().setFromVector3(camera.position);if(e.key==='ArrowLeft')s.theta-=.12;if(e.key==='ArrowRight')s.theta+=.12;if(e.key==='ArrowUp')s.phi-=.1;if(e.key==='ArrowDown')s.phi+=.1;if(e.key==='+'||e.key==='=')s.radius-=.15;if(e.key==='-')s.radius+=.15;s.phi=Math.max(.15,Math.min(Math.PI-.15,s.phi));s.radius=Math.max(2.1,Math.min(4.3,s.radius));camera.position.setFromSpherical(s);controls.update();schedule();});
 function resize(){if(!renderer)return;const w=stage.clientWidth,h=stage.clientHeight;if(!w||!h)return;renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();schedule();}
 function showFallback(error){failed=true;if(raf)cancelAnimationFrame(raf);raf=0;if(controls)controls.autoRotate=false;hint.textContent='静态网络与来源记录可继续查阅';stage.dataset.renderStatus='fallback';['rotate','motion'].forEach(k=>q(`[data-globe-${k}]`).disabled=true);if(renderer){renderer.dispose();renderer.domElement.remove();renderer=null;}q('.cm-globe-fallback').hidden=false;console.warn('C-Map globe fallback:',error?.message||'WebGL unavailable');}
 function buildFlows(){
  for(const g of [...flowGroup.children]){g.traverse(o=>{o.geometry?.dispose();if(o.material)o.material.dispose();});flowGroup.remove(g);}curves=[];particles=[];pickers=[];
  for(const row of F.edges){const a=by[row.source].coordinates,b=by[row.target].coordinates;if(!a||!b)continue;
   const same=row.source===row.target,curve=new THREE.CatmullRomCurve3(Array.from({length:49},(_,i)=>new THREE.Vector3(...(same?localLoop(...a,i/48):arcPoint(latLon(...a),latLon(...b),i/48,.12+.16*Math.sqrt(row.value/maximum))))));
   const group=new THREE.Group();flowGroup.add(group);const radius=visualWidth(row.value,maximum,multiplier),color=row.target==='CN'?0x88baff:0x64d4d2,material=new THREE.MeshBasicMaterial({color,transparent:true,opacity:.68}),tube=new THREE.Mesh(new THREE.TubeGeometry(curve,48,radius,6,false),material);tube.userData={row};group.add(tube);pickers.push(tube);
   const arrow=new THREE.Mesh(new THREE.ConeGeometry(Math.max(radius*2.2,.007),.028,8),new THREE.MeshBasicMaterial({color}));arrow.position.copy(curve.getPoint(.78));arrow.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),curve.getTangent(.78).normalize());group.add(arrow);
   for(let i=0;i<3*multiplier;i++){const mesh=new THREE.Mesh(new THREE.SphereGeometry(Math.max(.003,radius*1.3),7,5),new THREE.MeshBasicMaterial({color}));group.add(mesh);particles.push({mesh,group,curve,offset:i/(3*multiplier)});}
   curves.push({row,group,material});
  }
 }
 async function init(){if(started)return;started=true;try{
 const response=await fetch(new URL('./assets/cmap/globe-surface.json',import.meta.url));if(!response.ok)throw Error('Globe surface unavailable');const surface=await response.json();
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});renderer.setClearColor(0x071c30,0);renderer.outputColorSpace=THREE.SRGBColorSpace;stage.append(renderer.domElement);renderer.domElement.setAttribute('aria-label','全球协作与贡献三维地球');scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(43,1,.05,100);camera.position.fromArray(latLon(45,22,3.25));
 scene.add(new THREE.AmbientLight(0xa7cfe1,1.6));const key=new THREE.DirectionalLight(0xe1f6ff,2.1);key.position.set(-3,5,4);scene.add(key);const rim=new THREE.DirectionalLight(0x36a2cf,1.3);rim.position.set(3,1,-3);scene.add(rim);
 earth=new THREE.Mesh(new THREE.SphereGeometry(1,80,48),new THREE.MeshPhongMaterial({color:0x102e43,emissive:0x061320,shininess:12}));scene.add(earth);
 const atmosphere=new THREE.Mesh(new THREE.SphereGeometry(1.038,64,40),new THREE.ShaderMaterial({uniforms:{glow:{value:new THREE.Color(0x4fc5d9)}},vertexShader:'varying vec3 n; varying vec3 v; void main(){vec4 p=modelViewMatrix*vec4(position,1.0); n=normalize(normalMatrix*normal); v=normalize(-p.xyz); gl_Position=projectionMatrix*p;}',fragmentShader:'uniform vec3 glow; varying vec3 n; varying vec3 v; void main(){float f=pow(1.0-abs(dot(normalize(n),normalize(v))),3.0); gl_FragColor=vec4(glow,f*0.55);}',transparent:true,depthWrite:false,side:THREE.FrontSide}));scene.add(atmosphere);
 const dotPositions=[];surface.dots.forEach(([lon,lat])=>dotPositions.push(...latLon(lon,lat,1.006)));const dg=new THREE.BufferGeometry();dg.setAttribute('position',new THREE.Float32BufferAttribute(dotPositions,3));land=new THREE.Points(dg,new THREE.PointsMaterial({color:0x83cbd5,size:.012,sizeAttenuation:true,transparent:true,opacity:.55}));scene.add(land);
 const borders=[];for(const ring of surface.outlines)for(let i=1;i<ring.points.length;i++){borders.push(...latLon(...ring.points[i-1].slice(0,2),1.003),...latLon(...ring.points[i].slice(0,2),1.003));}const bg=new THREE.BufferGeometry();bg.setAttribute('position',new THREE.Float32BufferAttribute(borders,3));scene.add(new THREE.LineSegments(bg,new THREE.LineBasicMaterial({color:0x578395,transparent:true,opacity:.34})));
 const grid=[];for(let lat=-60;lat<=60;lat+=30)for(let lon=-180;lon<180;lon+=3)grid.push(...latLon(lon,lat,1.002),...latLon(lon+3,lat,1.002));for(let lon=-180;lon<180;lon+=30)for(let lat=-87;lat<87;lat+=3)grid.push(...latLon(lon,lat,1.002),...latLon(lon,lat+3,1.002));const gg=new THREE.BufferGeometry();gg.setAttribute('position',new THREE.Float32BufferAttribute(grid,3));scene.add(new THREE.LineSegments(gg,new THREE.LineBasicMaterial({color:0x82b0c1,transparent:true,opacity:.11})));
 camera.position.fromArray(latLon(5,62,3.25));flowGroup=new THREE.Group();scene.add(flowGroup);buildFlows();
 for(const code of new Set(F.edges.flatMap(e=>[e.source,e.target]))){const r=by[code];if(!r?.coordinates)continue;const targetNode=Boolean(F.targets[code]),color=code==='CN'?0x88baff:code==='US'?0x64d4d2:0xe0ebef;const mesh=new THREE.Mesh(new THREE.SphereGeometry(targetNode?.021:.012,14,10),new THREE.MeshBasicMaterial({color}));mesh.position.fromArray(latLon(...r.coordinates,1.025));mesh.userData.id=code;scene.add(mesh);nodes.push(mesh);}
 controls=new OrbitControls(camera,renderer.domElement);controls.enablePan=false;controls.enableDamping=!reduced;controls.dampingFactor=.1;controls.minDistance=2.1;controls.maxDistance=4.3;controls.autoRotateSpeed=.45;controls.autoRotate=false;controls.addEventListener('change',schedule);controls.addEventListener('start',()=>{cameraGoal=null;tooltip.hidden=true;});
 const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();let start=null;
 function hit(event){const rect=renderer.domElement.getBoundingClientRect();pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);raycaster.setFromCamera(pointer,camera);const hits=raycaster.intersectObjects(pickers.filter(p=>p.parent.visible),false),earthHit=raycaster.intersectObject(earth,false)[0];return hits.find(h=>!earthHit||h.distance<earthHit.distance+.005)?.object;}
 renderer.domElement.addEventListener('pointerdown',e=>start=[e.clientX,e.clientY]);renderer.domElement.addEventListener('pointerup',e=>{if(!start||Math.hypot(e.clientX-start[0],e.clientY-start[1])>6)return;const mesh=hit(e);if(!mesh)return;choose(mesh.userData.row.id);});
 renderer.domElement.addEventListener('pointermove',e=>{if(e.buttons)return;const mesh=hit(e);renderer.domElement.style.cursor=mesh?'pointer':'grab';if(mesh){const r=mesh.userData.row;tooltip.textContent=`${by[r.source].name} → ${by[r.target].name}项目 · ${exact(r.value)} OpenRank · ${r.share_pct.toFixed(2)}%`;tooltip.hidden=false;}else tooltip.hidden=true;});
 renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();showFallback(Error('WebGL context lost'));});q('.cm-globe-fallback').hidden=true;stage.dataset.renderStatus='webgl';hint.textContent='拖动旋转 · 滚轮缩放 · 点击连线或右侧记录';resize();new ResizeObserver(resize).observe(stage);updateScene();schedule();
 }catch(error){showFallback(error);}}
 updateText();if('IntersectionObserver' in window){new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;lastTime=0;if(visible){init();schedule();}else if(raf){cancelAnimationFrame(raf);raf=0;}},{rootMargin:'200px'}).observe(stage);}else init();
 document.addEventListener('visibilitychange',()=>{lastTime=0;if(document.hidden&&raf){cancelAnimationFrame(raf);raf=0;}else schedule();});window.addEventListener('resize',resize);
}
