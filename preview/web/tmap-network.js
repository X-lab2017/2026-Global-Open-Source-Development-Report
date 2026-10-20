(()=>{'use strict';
const D=window.TMAP_NETWORK;if(!D)return;
const state={mode:'influence',scenario:'base',selected:null,step:D.checkpoints.length-1,playing:false};let timer=null;
const $=s=>document.querySelector(s),escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const data=()=>D.scenarios[state.scenario],mode=()=>D.modes.find(x=>x.id===state.mode),node=id=>D.nodes.find(x=>x.id===id);
const share=(s,i)=>{const sum=s.slice(0,6).reduce((a,b)=>a+b,0);return sum?s[i]/sum*100:0;};
const radius=(i,m=state.mode)=>m==='participation'?24:m==='contribution'?Math.sqrt(data().totals[i])*11:Math.max(12,Math.sqrt(data().steps[state.step][i])*118);
function route(e){const a=node(e.source),b=node(e.target),i=D.nodes.indexOf(a),j=D.nodes.indexOf(b),dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy),ra=radius(i)+5,rb=radius(j)+5;return {x1:a.x+dx/len*ra,y1:a.y+dy/len*ra,x2:b.x-dx/len*rb,y2:b.y-dy/len*rb};}
function network(){const m=state.mode,focus=state.selected,edges=data().edges,rank=data().steps[state.step],connected=new Set(focus?[focus,...edges.filter(e=>e.source===focus||e.target===focus).map(e=>e.source===focus?e.target:e.source)]:D.nodes.map(n=>n.id));
let svg=`<svg viewBox="0 0 800 510" role="group" aria-label="同一组六位开发者与三个项目的${mode().title}示意网络"><defs><marker id="tm-net-arrow" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto-start-reverse"><path d="M0 0L5 2.5L0 5" fill="var(--tm-cyan)"/></marker></defs>`;
edges.forEach((e,k)=>{const r=route(e),on=!focus||e.source===focus||e.target===focus,w=m==='participation'?1.4:1+Math.sqrt(e.weight)*1.3,p=`M${r.x1} ${r.y1}L${r.x2} ${r.y2}`;
svg+=`<g class="tm-net-link ${on?'is-related':''}" opacity="${on?1:.13}"><path d="${p}" stroke="${m==='participation'?'var(--tm-line)':'var(--tm-cyan)'}" stroke-width="${w}" fill="none" ${m==='influence'?'marker-end="url(#tm-net-arrow)" marker-start="url(#tm-net-arrow)"':''}/>`;
if(m==='influence'&&state.playing&&on){svg+=`<circle class="tm-net-pulse" r="4" fill="var(--tm-gold)"><animateMotion dur="${1.4+k*.09}s" repeatCount="indefinite" path="${p}"/></circle>`;}
svg+=`<title>${e.source} 与 ${node(e.target).name}：示意贡献强度 ${e.weight}</title></g>`;});
D.nodes.forEach((n,i)=>{const r=radius(i),chosen=n.id===focus,related=connected.has(n.id),project=n.kind==='project',fill=project?'var(--tm-raised)':chosen?'var(--tm-gold)':'var(--tm-cyan)',line=chosen?'var(--tm-gold)':project?'var(--tm-south)':'var(--tm-cyan)';
svg+=`<g data-tm-net-node="${n.id}" role="button" tabindex="0" aria-pressed="${chosen}" aria-label="${escape(n.name)}，点击查看关系" opacity="${related?1:.3}"><title>${escape(n.name)}</title>`;
if(chosen)svg+=`<circle cx="${n.x}" cy="${n.y}" r="${r+8}" fill="none" stroke="var(--tm-gold)" stroke-width="1.5" stroke-dasharray="3 5"/>`;
svg+=project?`<rect x="${n.x-r}" y="${n.y-r}" width="${r*2}" height="${r*2}" rx="${r*.3}" fill="${fill}" stroke="${line}" stroke-width="1.5"/>`:`<circle cx="${n.x}" cy="${n.y}" r="${r}" fill="${fill}"/>`;
svg+=`<text x="${n.x}" y="${n.y+6}" text-anchor="middle" class="${project?'tm-net-project-id':'tm-net-developer-id'}">${n.id}</text>`;
if(project)svg+=`<text x="${n.x}" y="${n.y+r+21}" text-anchor="middle" class="tm-net-label">${n.name}</text>`;
svg+='</g>';});return svg+'</svg>';}
function rows(){const m=state.mode,s=data().steps[state.step];return D.nodes.slice(0,6).map((n,i)=>({id:n.id,value:m==='participation'?1:m==='contribution'?data().totals[i]:share(s,i)})).sort((a,b)=>b.value-a.value||a.id.localeCompare(b.id));}
function detail(){const chosen=state.selected?node(state.selected):null,edges=chosen?data().edges.filter(e=>e.source===chosen.id||e.target===chosen.id):[],base=D.scenarios.base,alt=D.scenarios.rewired;
const focus=chosen?`<strong>${escape(chosen.name)}</strong><span>连接 ${edges.length} ${chosen.kind==='developer'?'个项目':'位开发者'} · 示意贡献强度 ${data().totals[D.nodes.indexOf(chosen)]}</span><button type="button" data-tm-net-clear>显示全部连接</button>`:`<strong>${mode().question}</strong><span>${mode().insight}</span>`;
return `<aside class="tm-network-side"><div><small>${state.mode==='influence'?'开发者内相对影响 · 教学模拟':state.mode==='contribution'?'贡献强度 · 教学模拟':'活跃参与 · 教学模拟'}</small><h5>${state.mode==='participation'?'6 位活跃开发者':state.mode==='contribution'?'投入强度各不相同':'相互连接，形成影响'}</h5></div><div class="tm-network-rank">${rows().map(r=>`<button type="button" data-tm-net-node="${r.id}" aria-pressed="${state.selected===r.id}"><span>开发者 ${r.id}</span><i><em style="width:${r.value/(state.mode==='participation'?1:state.mode==='contribution'?12:40)*100}%"></em></i><b>${state.mode==='influence'?r.value.toFixed(1)+'%':r.value}</b></button>`).join('')}</div><div class="tm-network-focus" role="status">${focus}</div><div class="tm-network-experiment"><button type="button" data-tm-net-experiment aria-pressed="${state.scenario==='rewired'}">${state.scenario==='base'?'试一试：让 B 连接基础库':'恢复原来的协作关系'}</button><p>贡献强度仍为 8，改变协作对象。</p>${state.scenario==='rewired'?`<p class="tm-network-result">B 的示意影响：${base.developer_shares[1].toFixed(1)}% → ${alt.developer_shares[1].toFixed(1)}%</p>`:''}</div></aside>`;}
function render(){const m=mode();return `<div class="tm-network-layout" data-tm-network><div class="tm-network-main"><div class="tm-network-controls" role="group" aria-label="选择参与贡献影响力视角">${D.modes.map(v=>`<button type="button" data-tm-net-mode="${v.id}" aria-pressed="${v.id===state.mode}"><small>${v.chapter}</small> ${v.title}</button>`).join('')}<span>同一协作网络</span></div><div class="tm-network-stage">${network()}</div><div class="tm-network-legend">${m.legend}</div><div class="tm-network-play"><span>教学模拟 · 非真实排名</span>${state.mode==='influence'?`<button type="button" data-tm-net-play>${state.playing?'暂停传播':state.step<D.checkpoints.length-1?'继续传播':'播放传播'}</button><small>${state.playing?'观察影响逐步传播':state.step===D.checkpoints.length-1?'传播趋稳':'已暂停'}</small>`:'<small>点选节点，查看关联对象</small>'}</div></div>${detail()}</div>`;}
function update(){const host=$('#tm-world');if(host?.querySelector('[data-tm-network]'))host.innerHTML=render();}
function stop(){if(timer!=null)clearTimeout(timer);timer=null;state.playing=false;}
function tick(){timer=setTimeout(()=>{if(!$('#tm-world [data-tm-network]')||document.hidden){stop();return;}state.step++;if(state.step>=D.checkpoints.length-1){state.step=D.checkpoints.length-1;stop();}update();if(state.playing)tick();},850);}
document.addEventListener('click',e=>{const b=e.target.closest('[data-tm-network] button,[data-tm-network] [data-tm-net-node]');if(!b)return;const x=b.dataset,focused=document.activeElement===b,action=[...b.attributes].find(a=>a.name.startsWith('data-tm-net-'));
if(x.tmNetMode){stop();state.mode=x.tmNetMode;state.step=D.checkpoints.length-1;}
else if(x.tmNetNode){state.selected=state.selected===x.tmNetNode?null:x.tmNetNode;}
else if('tmNetClear' in x)state.selected=null;
else if('tmNetExperiment' in x){stop();state.scenario=state.scenario==='base'?'rewired':'base';state.step=D.checkpoints.length-1;state.selected=null;}
else if('tmNetPlay' in x){if(state.playing)stop();else{if(state.step===D.checkpoints.length-1)state.step=0;state.playing=true;tick();}}
update();if(focused&&action){const target=[...document.querySelectorAll(`[${action.name}]`)].find(n=>n.tagName===b.tagName&&n.getAttribute(action.name)===action.value);target?.focus({preventScroll:true});}
});
document.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)&&e.target.matches('[data-tm-network] svg [role=button]')){e.preventDefault();e.target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}});
document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();update();}});
window.TMAP_CONCEPT={render,stop,state,radius,data};
})();
