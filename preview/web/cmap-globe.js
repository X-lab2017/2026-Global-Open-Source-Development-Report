import * as THREE from './assets/cmap/vendor/three.module.js';
import {OrbitControls} from './assets/cmap/vendor/OrbitControls.js';
import {latLon,arcPoint,localLoop,DEMO_NODES,DEMO_EDGES} from './cmap-globe-math.mjs';
import {SOUTH_CODES,profileFlows,includeFlow} from './cmap-globe-analysis.mjs';

const root=document.querySelector('[data-cm-globe]'),dataNode=document.getElementById('cmap-data');
if(root&&dataNode){
const D=JSON.parse(dataNode.textContent),F=D.flows,stage=root.querySelector('[data-globe-stage]'),hint=root.querySelector('[data-globe-hint]'),badge=root.querySelector('[data-globe-badge]'),tooltip=root.querySelector('[data-globe-tooltip]');
const q=s=>root.querySelector(s),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=v=>v==null?'—':v>0&&v<100?'＜0.01':(Math.trunc((v/10000+1e-10)*100)/100).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const exact=v=>v.toLocaleString('en-US',{maximumFractionDigits:2}),press=(attr,value)=>root.querySelectorAll(`[data-${attr}]`).forEach(b=>b.setAttribute('aria-pressed',String(b.getAttribute('data-'+attr)===String(value))));
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches,by=Object.fromEntries(D.countries.map(r=>[r.id,r])),nodes=Object.fromEntries(DEMO_NODES.map(n=>[n.id,n]));
let renderer,scene,camera,controls,earth,land,demoGroup,dataGroup,edges,haloGroup,flowGroup,selectedRing,raf=0,started=false,failed=false,visible=true,mode='network',step=1,selected='CN',scope='report',flow='sample',target='all',lens='all',focus=null,motion=!reduced,clock=0,lastTime=0;
const particleBatches=new Map();
const pickers=[],animated=[],demoEdges=[],dataEdges=[],pins=[],halos=[],inboundHalos=[];
const explanations=[
 ['活动，是贡献的起点','96 位示意开发者与 18 个共享项目分布在不同地域。计数可以看见规模，尚未说明他们如何共同建设。','同一组节点，切换到关系视角，才能看见参与之间的连接。','活动有价值；还要理解它进入了怎样的协作。'],
 ['开发者与项目相互成就','384 条关系连接开发者与共享项目。本地社区、跨地域连接与共享枢纽交织；开发者与项目在参与中相互成就。','双向光点演示网络中的相互作用；粗细区分示意参与深度。点击节点可聚焦邻接关系。','让价值通过关系被识别，让协作增益得到支持。'],
 ['长期价值，需要持续投入','亮线与光环表示延续的关系；淡线表示投入中断后的衰减。历史积累影响下一期观察。','原理示意：历史继承与适当衰减共同强调长期建设；亮度与速度均不是 OpenRank 得分。','认可长期维护，也持续欢迎新的有效贡献。']
];
const flowNum=v=>v==null?'表未列':v>=10000?(v/10000).toFixed(2)+' 万':exact(v);
function stat(label,value,note){return `<span class="cm-globe-stat"><small>${label}</small><strong>${value}</strong><em>${note}</em></span>`;}
function insightCards(){
 if(lens==='all')return stat('贡献规模 · 报告2026','442.92 / 423.97 万','中国 / 美国 · 开发者贡献总量')+stat('中美定向连接 · 表列样本','12.3 倍','中国→美国项目 / 美国→中国项目')+stat('本土贡献份额 · 原表分母','79.22% / 38.28%','中国项目 / 美国项目 · 独立样本');
 if(lens==='south'){
  const obs=F.edges.filter(e=>e.kind==='observed'&&SOUTH_CODES.includes(e.source)&&e.source!==e.target).reduce((s,e)=>s+e.value,0),est=F.edges.filter(e=>e.kind==='estimated'&&SOUTH_CODES.includes(e.source)&&e.source!==e.target).reduce((s,e)=>s+e.value,0);
  return stat('南方观察 · 印度与六国',flowNum(obs),'表列来源贡献 · 当前仅印度在前十')+stat('未列来源 · 条件估算',flow==='scenario'?flowNum(est):'未开启','与表列分开读数 · 非未来预测')+stat('观察范围','仅中美项目样本','未列出 ≠ 无贡献 · 不推算全球总额');
 }
 const p=profileFlows(F,selected),scenario=flow==='scenario';return stat('所选地区 · 对外贡献',flowNum(p.out),scenario&&p.outEstimate?'另有估算 '+flowNum(p.outEstimate)+' · 独立列示':'只计向境外中美项目的表列贡献')+stat('所选地区 · 跨境汇入',p.in==null?'未覆盖':flowNum(p.in),p.in==null?'该地项目未纳入来源表':scenario?'另有估算 '+flowNum(p.inEstimate):'该地项目收到的表列境外贡献')+stat('所选地区 · 本土建设',p.local==null?'未覆盖':flowNum(p.local),'2026项目样本 · 单位 OpenRank');
}
function flowSummary(){
 if(flow==='none')return scope==='report'?'报告口径仅中、美、印有国家总值；其他地区留空。可切换 GitHub 参照查看完整分布。':'完整 GitHub2025 分布；点越大贡献越多。本视角关闭来源连线与汇入外环。';
 if(lens==='out')return `聚焦${by[selected].name}的对外贡献：只连向境外项目；下方分别显示表列输出、汇入与本土投入。样本只覆盖中美项目。`;
 if(lens==='in')return F.targets[selected]?`聚焦${by[selected].name}项目的跨境汇入：排除本土回环。外环大小按已列境外贡献绘制，虚线估算单独显示。`:'该地区的项目没有进入当前来源表；无法判断汇入，不能解释为零。可选择中国或美国继续观察。';
 if(lens==='south')return '印度与南方六国：实线为表列来源，金色虚线补充未列来源估算。权重未因展现需要调大；不能据此排名全球贡献。';
 return flow==='scenario'?'实线是表列样本；金色虚线按剩余份额与2025贡献权重估算。包含强连接与南方六国，不代表完整全球网络。':'实线粗细表达贡献强度，方向为来源→项目。外环表示表列跨境汇入。点与线总体不同，点击连线可读数。';
}
function updateText(){
 press('globe-mode',mode);press('globe-step',step);press('globe-scope',scope);press('globe-flow',flow);press('globe-lens',lens);q('[data-globe-lenses]').hidden=mode!=='data';
 q('[data-globe-network-panel]').hidden=mode!=='network';q('[data-globe-data-panel]').hidden=mode!=='data';
 badge.textContent=mode==='network'?'机制示意 · 虚构节点与连线 · 非真实跨国流量':(scope==='report'?'贡献点：报告2026':'贡献点：GitHub2025')+(flow==='none'?' · 无流向图层':flow==='scenario'?' · 实线样本＋虚线估算':' · 实线：2026项目样本');
 const e=explanations[step];q('[data-globe-title]').textContent=e[0];q('[data-globe-explanation]').innerHTML=`<p>${e[1]}</p><p>${e[2]}</p>`;q('[data-globe-principle]').textContent=e[3];q('[data-globe-clear]').hidden=!focus;
 const r=by[selected],value=scope==='report'?F.report_values[selected]:r.value;
 q('[data-globe-country-detail]').innerHTML=`<strong>${esc(r.name)} · ${num(value)}${value==null?'':' 万'}</strong><p>${scope==='report'?(value==null?'该国报告总量待补；小点仅作来源锚点。':'报告2026 · 开发者贡献总量'):`GitHub2025 · 贡献位次 ${r.rank}`}</p>`;
 q('[data-globe-country]').value=selected;q('[data-globe-target]').value=target;q('[data-globe-flow-detail]').textContent=flowSummary();q('[data-globe-target]').disabled=flow==='none'||lens!=='all';
 q('[data-globe-legend]').textContent=mode==='network'?(step===0?'青色：开发者 · 金色：共享项目':step===1?'双向光点：相互作用 · 粗细：示意参与深度':'亮线／光环：持续投入 · 淡线：中断衰减'):(flow==='none'?'点大小：贡献总量 · 缺失地区不推算':flow==='scenario'?'实线：来源 → 项目 · 金色虚线：估算 · 外环：表列跨境汇入':'实线：来源 → 项目 · 粗细：贡献强度 · 外环：表列跨境汇入');
 q('[data-globe-bottom]').innerHTML=mode==='network'?['活动：贡献的起点','关系：开发者 ↔ 共享项目','时间：历史继承与适当衰减'].map(s=>`<span>${s}</span>`).join(''):insightCards();
 q('[data-globe-motion]').setAttribute('aria-pressed',String(motion));q('[data-globe-motion]').textContent=motion?'暂停流动':'播放流动';
}
function schedule(){if(!raf&&renderer&&visible&&!document.hidden)raf=requestAnimationFrame(draw);}
function liveMotion(){return motion&&(mode==='network'?step>0:flow!=='none');}
function draw(time=0){raf=0;if(!renderer||!visible||document.hidden)return;const dt=lastTime?Math.min(50,Math.max(0,time-lastTime)):0;lastTime=time;if(liveMotion())clock+=dt/1000;
 for(const a of animated){const t=((clock*a.speed+a.offset)%1+1)%1;a.mesh.position.copy(a.curve.getPoint(a.reverse?1-t:t));if(a.batch){a.mesh.scale.setScalar(a.mesh.visible?1:0);a.mesh.updateMatrix();a.batch.setMatrixAt(a.slot,a.mesh.matrix);}}
 for(const batch of particleBatches.values())batch.instanceMatrix.needsUpdate=true;
 controls.update();renderer.render(scene,camera);if(controls.autoRotate||liveMotion())schedule();}
function face(lon,lat){if(!camera)return;camera.position.fromArray(latLon(lon,lat,camera.position.length()));camera.lookAt(0,0,0);controls.update();schedule();}
function updateScene(){updateText();tooltip.hidden=true;if(!scene)return;demoGroup.visible=mode==='network';dataGroup.visible=mode==='data';edges.visible=step>0;haloGroup.visible=step===2;land.material.opacity=mode==='network'?.45:.65;
 const related=new Set(focus?[focus]:DEMO_NODES.map(n=>n.id));for(const e of demoEdges){const chosen=!focus||e.a===focus||e.b===focus;if(chosen){related.add(e.a);related.add(e.b);}const alpha=chosen?(step===2?(e.persistent?.72:.07):.42):.025;e.material.opacity=alpha;e.particles.forEach(p=>p.visible=chosen&&(step!==2||e.persistent));}
 for(const p of pickers.filter(p=>p.userData.kind==='network')){p.material.opacity=related.has(p.userData.id)?1:.2;p.material.transparent=true;}
 for(const h of halos)h.visible=related.has(h.userData.node);
 const values=scope==='report'?Object.values(F.report_values):D.countries.map(r=>r.value),max=Math.max(...values);
 for(const p of pins){const value=scope==='report'?F.report_values[p.userData.id]:by[p.userData.id].value;const used=F.edges.some(e=>e.source===p.userData.id&&(e.kind==='observed'||(flow==='scenario'&&e.display)));p.visible=value!=null||used;p.scale.setScalar(value==null?.008:.009+.037*Math.sqrt(value/max));p.material.color.set(value==null?0x839aa7:0x8be2df);p.material.opacity=value==null?.65:1;}
 flowGroup.visible=flow!=='none';for(const e of dataEdges)e.group.visible=includeFlow(e.row,{flow,lens,selected,target});
 for(const h of inboundHalos)h.visible=flow!=='none'&&(lens==='all'?(target==='all'||target===h.userData.target):lens==='in'&&selected===h.userData.target);
 const pos=by[selected].coordinates;selectedRing.visible=mode==='data'&&!!pos;if(pos){const p=new THREE.Vector3(...latLon(...pos,1.055));selectedRing.position.copy(p);selectedRing.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),p.clone().normalize());}schedule();}
function setMode(v){mode=v;updateScene();if(mode==='data'){if(lens==='all')face(5,62);else if(by[selected].coordinates)face(...by[selected].coordinates);}}
root.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
 if(b.dataset.globeMode)setMode(b.dataset.globeMode);
 else if(b.dataset.globeStep!==undefined){step=Number(b.dataset.globeStep);updateScene();}
 else if(b.dataset.globeScope){scope=b.dataset.globeScope;updateScene();}
 else if(b.dataset.globeFlow){flow=b.dataset.globeFlow;if(flow==='none')lens='all';updateScene();}
 else if(b.dataset.globeLens){lens=b.dataset.globeLens;target='all';if(lens==='south')flow='scenario';else if(flow==='none')flow='sample';updateScene();if(lens==='south')face(40,8);else if(lens==='all')face(5,62);else if(by[selected].coordinates)face(...by[selected].coordinates);}
 else if(b.hasAttribute('data-globe-clear')){focus=null;updateScene();}
 else if(b.hasAttribute('data-globe-motion')){motion=!motion;updateText();schedule();}
 else if(b.hasAttribute('data-globe-rotate')&&controls){controls.autoRotate=!controls.autoRotate;b.setAttribute('aria-pressed',String(controls.autoRotate));b.textContent=controls.autoRotate?'暂停旋转':'自动旋转';schedule();}
 else if(b.hasAttribute('data-globe-reset')&&camera){focus=null;controls.autoRotate=false;const auto=q('[data-globe-rotate]');auto.setAttribute('aria-pressed','false');auto.textContent='自动旋转';camera.position.fromArray(latLon(mode==='data'&&by[selected].coordinates?by[selected].coordinates[0]:45,mode==='data'&&by[selected].coordinates?by[selected].coordinates[1]:22,3.25));controls.target.set(0,0,0);controls.update();updateScene();}
});
q('[data-globe-country]').addEventListener('change',e=>{selected=e.target.value;updateScene();if(by[selected].coordinates)face(...by[selected].coordinates);});
q('[data-globe-target]').addEventListener('change',e=>{target=e.target.value;updateScene();if(target!=='all')face(...by[target].coordinates);});
stage.addEventListener('keydown',e=>{if(!camera||['SELECT','BUTTON'].includes(e.target.tagName))return;if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-'].includes(e.key))return;e.preventDefault();const s=new THREE.Spherical().setFromVector3(camera.position);if(e.key==='ArrowLeft')s.theta-=.12;if(e.key==='ArrowRight')s.theta+=.12;if(e.key==='ArrowUp')s.phi-=.1;if(e.key==='ArrowDown')s.phi+=.1;if(e.key==='+'||e.key==='=')s.radius-=.15;if(e.key==='-')s.radius+=.15;s.phi=Math.max(.15,Math.min(Math.PI-.15,s.phi));s.radius=Math.max(2.1,Math.min(4.3,s.radius));camera.position.setFromSpherical(s);controls.update();schedule();});
function resize(){if(!renderer)return;const w=stage.clientWidth,h=stage.clientHeight;if(!w||!h)return;renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();schedule();}
function showFallback(error){failed=true;if(raf){cancelAnimationFrame(raf);raf=0;}if(controls)controls.autoRotate=false;hint.textContent='3D 未启用；保留静态地球与右侧数据。来源及估算可下载查阅。';stage.dataset.renderStatus='fallback';['rotate','reset','motion'].forEach(k=>q(`[data-globe-${k}]`).disabled=true);if(renderer){renderer.dispose();renderer.domElement.remove();renderer=null;}q('.cm-globe-fallback').hidden=false;console.warn('C-Map globe fallback:',error?.message||'WebGL unavailable');}
function particle(group,curve,color,speed,offset,reverse=false,size=.008){
 if(group===edges){let batch=particleBatches.get(color);if(!batch){batch=new THREE.InstancedMesh(new THREE.SphereGeometry(size,8,6),new THREE.MeshBasicMaterial({color}),DEMO_EDGES.length);batch.count=0;batch.frustumCulled=false;particleBatches.set(color,batch);group.add(batch);}const p=new THREE.Object3D(),slot=batch.count++;animated.push({mesh:p,curve,speed,offset,reverse,batch,slot});return p;}
 const p=new THREE.Mesh(new THREE.SphereGeometry(size,8,6),new THREE.MeshBasicMaterial({color}));group.add(p);animated.push({mesh:p,curve,speed,offset,reverse});return p;
}
function curveFor(a,b,height=.15){const av=latLon(...a),bv=latLon(...b);return new THREE.CatmullRomCurve3(Array.from({length:49},(_,i)=>new THREE.Vector3(...arcPoint(av,bv,i/48,height))));}
function addFlow(row){const a=by[row.source]?.coordinates,b=by[row.target]?.coordinates;if(!a||!b)return;const group=new THREE.Group();group.userData={kind:'flow',row};flowGroup.add(group);const same=row.source===row.target,curve=same?new THREE.CatmullRomCurve3(Array.from({length:49},(_,i)=>new THREE.Vector3(...localLoop(...a,i/48)))):curveFor(a,b,.12+.14*Math.sqrt(row.value/120223.9));
 const estimate=row.kind==='estimated',color=estimate?0xf3cd6f:row.target==='CN'?0x88baff:0x64d4d2,radius=.001+.01*Math.sqrt(row.value/120223.9),material=new THREE.MeshBasicMaterial({color,transparent:true,opacity:estimate?.68:.7});
 if(estimate){for(let i=0;i<18;i+=2){const part=new THREE.CatmullRomCurve3(Array.from({length:5},(_,j)=>curve.getPoint((i+j/4)/18)));const m=new THREE.Mesh(new THREE.TubeGeometry(part,4,radius,4,false),material);m.userData={kind:'flow',row};group.add(m);pickers.push(m);}}
 else{const m=new THREE.Mesh(new THREE.TubeGeometry(curve,48,radius,5,false),material);m.userData={kind:'flow',row};group.add(m);pickers.push(m);}
 const arrow=new THREE.Mesh(new THREE.ConeGeometry(radius*2.5+.004,.025,7),new THREE.MeshBasicMaterial({color}));arrow.position.copy(curve.getPoint(.76));arrow.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),curve.getTangent(.76).normalize());group.add(arrow);
 particle(group,curve,color,.11,row.source.charCodeAt(0)/100,false,radius*1.7+.005);dataEdges.push({row,group});}
async function init(){if(started)return;started=true;try{
 const response=await fetch(new URL('./assets/cmap/globe-surface.json',import.meta.url));if(!response.ok)throw Error('Globe surface unavailable');const surface=await response.json();
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});renderer.setClearColor(0x071c30,0);renderer.outputColorSpace=THREE.SRGBColorSpace;stage.append(renderer.domElement);renderer.domElement.setAttribute('aria-label','全球协作与贡献三维地球');scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(43,1,.05,100);camera.position.fromArray(latLon(45,22,3.25));
 scene.add(new THREE.AmbientLight(0xa7cfe1,1.6));const key=new THREE.DirectionalLight(0xe1f6ff,2.1);key.position.set(-3,5,4);scene.add(key);const rim=new THREE.DirectionalLight(0x36a2cf,1.3);rim.position.set(3,1,-3);scene.add(rim);
 earth=new THREE.Mesh(new THREE.SphereGeometry(1,80,48),new THREE.MeshPhongMaterial({color:0x102e43,emissive:0x061320,shininess:12}));scene.add(earth);
 const atmosphere=new THREE.Mesh(new THREE.SphereGeometry(1.038,64,40),new THREE.ShaderMaterial({uniforms:{glow:{value:new THREE.Color(0x4fc5d9)}},vertexShader:'varying vec3 n; varying vec3 v; void main(){vec4 p=modelViewMatrix*vec4(position,1.0); n=normalize(normalMatrix*normal); v=normalize(-p.xyz); gl_Position=projectionMatrix*p;}',fragmentShader:'uniform vec3 glow; varying vec3 n; varying vec3 v; void main(){float f=pow(1.0-abs(dot(normalize(n),normalize(v))),3.0); gl_FragColor=vec4(glow,f*0.55);}',transparent:true,depthWrite:false,side:THREE.FrontSide}));scene.add(atmosphere);
 const dotPositions=[];surface.dots.forEach(([lon,lat])=>dotPositions.push(...latLon(lon,lat,1.006)));const dg=new THREE.BufferGeometry();dg.setAttribute('position',new THREE.Float32BufferAttribute(dotPositions,3));land=new THREE.Points(dg,new THREE.PointsMaterial({color:0x83cbd5,size:.012,sizeAttenuation:true,transparent:true,opacity:.55}));scene.add(land);
 const borders=[];for(const ring of surface.outlines)for(let i=1;i<ring.points.length;i++){borders.push(...latLon(...ring.points[i-1].slice(0,2),1.003),...latLon(...ring.points[i].slice(0,2),1.003));}const bg=new THREE.BufferGeometry();bg.setAttribute('position',new THREE.Float32BufferAttribute(borders,3));scene.add(new THREE.LineSegments(bg,new THREE.LineBasicMaterial({color:0x578395,transparent:true,opacity:.34})));
 const grid=[];for(let lat=-60;lat<=60;lat+=30)for(let lon=-180;lon<180;lon+=3)grid.push(...latLon(lon,lat,1.002),...latLon(lon+3,lat,1.002));for(let lon=-180;lon<180;lon+=30)for(let lat=-87;lat<87;lat+=3)grid.push(...latLon(lon,lat,1.002),...latLon(lon,lat+3,1.002));const gg=new THREE.BufferGeometry();gg.setAttribute('position',new THREE.Float32BufferAttribute(grid,3));scene.add(new THREE.LineSegments(gg,new THREE.LineBasicMaterial({color:0x82b0c1,transparent:true,opacity:.11})));
 dataGroup=new THREE.Group();demoGroup=new THREE.Group();edges=new THREE.Group();haloGroup=new THREE.Group();flowGroup=new THREE.Group();dataGroup.add(flowGroup);demoGroup.add(edges,haloGroup);scene.add(dataGroup,demoGroup);dataGroup.name='observed';demoGroup.name='conceptual';flowGroup.name='source-flows';
 for(const r of D.countries){if(!r.coordinates)continue;const p=new THREE.Mesh(new THREE.SphereGeometry(1,12,8),new THREE.MeshBasicMaterial({color:0x80dadd,transparent:true}));p.position.fromArray(latLon(...r.coordinates,1.025));p.userData={kind:'data',id:r.id};dataGroup.add(p);pickers.push(p);pins.push(p);}
 selectedRing=new THREE.Mesh(new THREE.RingGeometry(.05,.057,40),new THREE.MeshBasicMaterial({color:0xffd76d,side:THREE.DoubleSide,transparent:true,opacity:.95,depthWrite:false}));dataGroup.add(selectedRing);
 const degree=Object.fromEntries(DEMO_NODES.map(n=>[n.id,DEMO_EDGES.filter(e=>e[0]===n.id||e[1]===n.id).length])),maxDegree=Math.max(...Object.values(degree));
 for(const n of DEMO_NODES){const material=new THREE.MeshPhongMaterial({color:n.type==='project'?0xf2ca65:0x77dee2,emissive:n.type==='project'?0x664317:0x14515b,shininess:30});const p=new THREE.Mesh(n.type==='project'?new THREE.OctahedronGeometry(.019+.025*Math.sqrt(degree[n.id]/maxDegree)):new THREE.SphereGeometry(.012,12,8),material);p.position.fromArray(latLon(n.lon,n.lat,1.035));p.userData={kind:'network',id:n.id};demoGroup.add(p);pickers.push(p);const ring=new THREE.Mesh(new THREE.RingGeometry(.027,.031,24),new THREE.MeshBasicMaterial({color:0xf2ca65,side:THREE.DoubleSide,transparent:true,opacity:.65,depthWrite:false}));ring.position.copy(p.position).multiplyScalar(1.015);ring.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),p.position.clone().normalize());ring.userData.node=n.id;haloGroup.add(ring);halos.push(ring);}
 for(const [i,pair] of DEMO_EDGES.entries()){const [a,b,weight,persistent]=pair,na=nodes[a],nb=nodes[b],curve=curveFor([na.lon,na.lat],[nb.lon,nb.lat],.05+i%5*.027),material=new THREE.MeshBasicMaterial({color:i%3?0x6ac9d4:0xe9c577,transparent:true,opacity:.6}),tube=new THREE.Mesh(new THREE.TubeGeometry(curve,32,.0007+weight*.00025,4,false),material);edges.add(tube);const particles=[particle(edges,curve,0x92f3ed,.09,i*.137,false,.0048),particle(edges,curve,0xffdc86,.075,i*.117,true,.0048)];demoEdges.push({a,b,persistent,material,particles});}
 for(const row of F.edges.filter(r=>r.display))addFlow(row);
 const incoming=['CN','US'].map(t=>({target:t,value:profileFlows(F,t).in})),maxIncoming=Math.max(...incoming.map(r=>r.value));
 for(const row of incoming){const radius=.055+.12*Math.sqrt(row.value/maxIncoming),ring=new THREE.Mesh(new THREE.RingGeometry(radius,radius+.004,64),new THREE.MeshBasicMaterial({color:row.target==='CN'?0x88baff:0x64d4d2,side:THREE.DoubleSide,transparent:true,opacity:.75,depthWrite:false}));const pos=new THREE.Vector3(...latLon(...by[row.target].coordinates,1.045));ring.position.copy(pos);ring.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),pos.clone().normalize());ring.userData.target=row.target;dataGroup.add(ring);inboundHalos.push(ring);}

 controls=new OrbitControls(camera,renderer.domElement);controls.enablePan=false;controls.enableDamping=!reduced;controls.dampingFactor=.1;controls.minDistance=2.1;controls.maxDistance=4.3;controls.autoRotateSpeed=.45;controls.autoRotate=false;controls.addEventListener('change',schedule);controls.addEventListener('start',()=>tooltip.hidden=true);
 const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();let start=null;
 function isVisible(p){for(let x=p;x;x=x.parent)if(!x.visible)return false;return true;}
 function hit(event){const rect=renderer.domElement.getBoundingClientRect();pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);raycaster.setFromCamera(pointer,camera);const hits=raycaster.intersectObjects(pickers.filter(p=>isVisible(p)&&(p.userData.kind===mode||(mode==='data'&&p.userData.kind==='flow'))),false),earthHit=raycaster.intersectObject(earth,false)[0];return hits.find(h=>!earthHit||h.distance<earthHit.distance+.005)?.object;}
 renderer.domElement.addEventListener('pointerdown',e=>start=[e.clientX,e.clientY]);renderer.domElement.addEventListener('pointerup',e=>{if(!start||Math.hypot(e.clientX-start[0],e.clientY-start[1])>6)return;const p=hit(e);if(!p)return;
 if(p.userData.kind==='flow'){const r=p.userData.row;tooltip.textContent=`${by[r.source].name} → ${by[r.target].name}项目 · ${r.kind==='observed'?'表列样本':'情景估算'} ${exact(r.value)} OpenRank · 份额 ${r.share_pct.toFixed(2)}%`;tooltip.hidden=false;}
 else if(mode==='data'){selected=p.userData.id;updateScene();}
 else{focus=focus===p.userData.id?null:p.userData.id;updateScene();const n=nodes[p.userData.id],count=DEMO_EDGES.filter(e=>e[0]===n.id||e[1]===n.id).length;tooltip.hidden=false;tooltip.textContent=n.name+` · ${count} 条参与关系 · `+(n.type==='project'?'项目与参与者相互成就':'深度参与连接共享项目')+'（虚构原理示意）';}});
 renderer.domElement.addEventListener('pointermove',e=>{if(e.buttons)return;renderer.domElement.style.cursor=hit(e)?'pointer':'grab';});renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();showFallback(Error('WebGL context lost'));});
 q('.cm-globe-fallback').hidden=true;stage.dataset.renderStatus='webgl';hint.textContent='拖动旋转 · 滚轮／双指缩放 · 点击节点或连线 · 可暂停流动';resize();new ResizeObserver(resize).observe(stage);updateScene();schedule();
 }catch(error){showFallback(error);}}
 updateText();if('IntersectionObserver' in window){new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;lastTime=0;if(visible){init();schedule();}else if(raf){cancelAnimationFrame(raf);raf=0;}},{rootMargin:'200px'}).observe(stage);}else init();
 document.addEventListener('visibilitychange',()=>{lastTime=0;if(document.hidden&&raf){cancelAnimationFrame(raf);raf=0;}else schedule();});window.addEventListener('resize',resize);window.addEventListener('beforeprint',()=>q('.cm-globe-fallback').hidden=false);window.addEventListener('afterprint',()=>{if(!failed)q('.cm-globe-fallback').hidden=true;});
}
