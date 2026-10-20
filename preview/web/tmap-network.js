(()=>{'use strict';
const D=window.TMAP_NETWORK;if(!D)return;
const state={mode:'contribution',selected:D.default_selected,playing:true};
const $=s=>document.querySelector(s),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const node=id=>D.nodes.find(n=>n.id===id),mode=()=>D.modes.find(m=>m.id===state.mode),users=D.nodes.filter(n=>n.kind==='developer');
const fmt=(v,d=3)=>v==null?'—':v.toFixed(d),color=n=>D.colors[n.kind];
const value=n=>state.mode==='participation'?n.neighbors.length:state.mode==='contribution'?n.community:n.global_value;
const radius=n=>n.kind==='repo'?17:n.kind!=='developer'?Math.min(12,6+Math.sqrt(n.community)*2):state.mode==='participation'?14:Math.min(33,11+Math.sqrt(value(n)||0)*6);
function network(){const chosen=node(state.selected),related=new Set(chosen?[chosen.id,...chosen.neighbors]:D.nodes.map(n=>n.id));
let svg='<svg viewBox="0 0 800 560" role="group" aria-label="OpenDigger 2024 年 9 月真实协作网络：8 个账户、18 个 Issue、10 个 PR"><defs><marker id="tm-community-arrow" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0L5 2.5L0 5" fill="var(--tm-cyan)"/></marker></defs>';
D.pairs.forEach((e,k)=>{const a=node(e.source),b=node(e.target),on=!chosen||chosen.id===a.id||chosen.id===b.id,dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy),ra=radius(a)+3,rb=radius(b)+3;let start=[a.x+dx/len*ra,a.y+dy/len*ra],end=[b.x-dx/len*rb,b.y-dy/len*rb];
if(chosen?.id===a.id)[start,end]=[end,start];const path=`M${start[0]} ${start[1]}L${end[0]} ${end[1]}`;
svg+=`<path d="${path}" fill="none" stroke="${on?color(b):'var(--tm-line)'}" stroke-width="${on?1.5+e.weight*2:1}" opacity="${on?.65:.5}" ${state.mode==='contribution'&&chosen&&on?'marker-end="url(#tm-community-arrow)"':''}/>`;
if(state.mode==='contribution'&&state.playing&&on)svg+=`<circle class="tm-net-pulse" r="2.7" fill="${color(b)}"><animateMotion dur="${2.8+k%6*.3}s" repeatCount="indefinite" path="${path}"/></circle>`;
});
if(chosen&&chosen.kind!=='repo'&&state.mode==='contribution'){const repo=D.nodes.find(n=>n.kind==='repo');svg+=`<path d="M${repo.x} ${repo.y}L${chosen.x} ${chosen.y}" stroke="${color(repo)}" stroke-width="1" stroke-dasharray="3 5" opacity=".45"/><text x="${(repo.x+chosen.x)/2}" y="${(repo.y+chosen.y)/2-8}" text-anchor="middle" class="tm-net-label">项目背景</text>`;}
D.nodes.filter(n=>n.kind!=='developer').concat(users).forEach(n=>{const r=radius(n),selected=n.id===state.selected,on=related.has(n.id),missing=state.mode==='influence'&&n.kind==='developer'&&n.global_value==null,fill=missing?'var(--tm-bg)':color(n);
svg+=`<g data-tm-net-node="${n.id}" role="button" tabindex="0" aria-pressed="${selected}" aria-label="${esc(n.label)}，${n.kind==='developer'?'参与账户':n.kind==='issue'?'问题与讨论':n.kind==='pull'?'变更请求':'项目'}，点击查看" opacity="${on?1:.58}"><title>${esc(n.name)}</title>`;
if(selected)svg+=`<circle cx="${n.x}" cy="${n.y}" r="${r+7}" fill="none" stroke="var(--tm-ink)" stroke-width="1.6" stroke-dasharray="3 4"/>`;
if(n.kind==='issue')svg+=`<path d="M${n.x} ${n.y-r}l${r} ${r}l${-r} ${r}l${-r} ${-r}z" fill="${fill}"/>`;
else if(n.kind==='pull'||n.kind==='repo')svg+=`<rect x="${n.x-r}" y="${n.y-r}" width="${r*2}" height="${r*2}" rx="${n.kind==='repo'?5:3}" fill="${fill}"/>`;
else svg+=`<circle cx="${n.x}" cy="${n.y}" r="${r}" fill="${fill}" stroke="${color(n)}" stroke-width="2" ${missing?'stroke-dasharray="3 3"':''}/>`;
if(n.kind==='developer'||n.kind==='repo'||(chosen&&on))svg+=`<text x="${n.x}" y="${n.y+r+20}" text-anchor="middle" class="tm-net-label ${n.kind==='developer'?'tm-net-user':''}">${esc(n.label)}</text>`;
svg+='</g>';});return svg+'</svg>';}
function rows(){return users.map(n=>({n,v:value(n)})).sort((a,b)=>(b.v??-1)-(a.v??-1)||a.n.name.localeCompare(b.n.name));}
function ranking(){const rs=rows(),max=rs[0].v||1;return `<aside class="tm-network-ranking"><small>${state.mode==='participation'?'参与账户 · 关联 Issue / PR':state.mode==='contribution'?'项目内贡献 · 社区 OpenRank':'全域影响力 · 全域 OpenRank'}</small><div class="tm-network-rank">${rs.map(({n,v})=>`<button type="button" data-tm-net-node="${n.id}" aria-pressed="${state.selected===n.id}" title="${esc(n.name)}"><span>${esc(n.name)}</span><b>${state.mode==='participation'?v:fmt(v,state.mode==='influence'?2:3)}</b><i><em style="width:${v==null?0:v/max*100}%"></em></i></button>`).join('')}</div><small>${state.mode==='influence'?'6 个账户有公开值；— 表示未取得。':state.mode==='participation'?'每个账户计一次；右侧数字为关联工作项数。':'选择账户，查看它的协作对象与贡献来源。'}</small></aside>`;}
function detail(){const n=node(state.selected);if(!n)return `<aside class="tm-network-detail"><small>协作网络</small><h5>具体工作，连接共同贡献</h5><p>点选账户、Issue 或 PR，查看其关联对象。</p><div class="tm-network-key"><span>● 8 个参与账户</span><span>◆ 18 个 Issue · 问题与讨论</span><span>■ 10 个 PR · 变更请求</span></div><p>社区贡献与全域影响力采用不同网络范围，分值不作大小比较。</p></aside>`;
const parts=n.components.filter(c=>c.value>0),shown=parts.length>6?[...parts.slice(0,4),{id:'more',label:'其余关系与保留项',value:parts.slice(4).reduce((s,c)=>s+c.value,0)}]:parts;
return `<aside class="tm-network-detail" aria-live="polite"><div><small>${n.kind==='developer'?'参与账户':n.kind==='repo'?'项目':'协作工作项'}</small><h5>${esc(n.label)}</h5>${n.kind==='issue'||n.kind==='pull'?`<p>${esc(n.short)}</p>`:''}<button type="button" data-tm-net-clear>显示全部连接</button></div><div class="tm-network-metrics"><div><small>项目内贡献</small><strong>${fmt(n.community)}</strong></div>${n.kind==='developer'?`<div><small>全域影响力</small><strong>${fmt(n.global_value,2)}</strong></div>`:''}</div>${state.mode==='contribution'?`<div class="tm-network-sources"><h6>社区值从哪里来</h6>${shown.map(c=>`<div><span>${esc(c.label)}</span><b>${fmt(c.value)}</b><i style="width:${Math.min(100,c.value/n.community*100)}%"></i></div>`).join('')}<p>关系传播＋自身保留＋项目背景。分项按公开值还原，末位可能有舍入差。</p></div>`:state.mode==='participation'?`<div class="tm-network-focus"><strong>${n.neighbors.length} 个关联对象</strong><p>点亮的关系展示这个账户或工作项连接着谁。人数与关系数量分别统计。</p></div>`:`<div class="tm-network-focus"><strong>同一个人，两种观察范围</strong><p>项目内贡献聚焦 OpenDigger；全域影响力来自更广的协作网络。这里的连线只展示前者。</p></div>`}</aside>`;}
function render(){return `<div class="tm-network-layout" data-tm-network><div class="tm-network-controls" role="group" aria-label="选择参与贡献影响力视角">${D.modes.map(m=>`<button type="button" data-tm-net-mode="${m.id}" aria-pressed="${m.id===state.mode}"><small>${m.chapter}</small> ${m.title}</button>`).join('')}<span>OpenDigger · 2024.09</span>${state.mode==='contribution'?`<button type="button" data-tm-net-play aria-pressed="${state.playing}">${state.playing?'暂停流动':'显示流动'}</button>`:''}</div><div class="tm-network-body">${ranking()}<div class="tm-network-main"><div class="tm-network-stage">${network()}</div><div class="tm-network-legend"><span style="color:${D.colors.developer}">● 账户</span><span style="color:${D.colors.issue}">◆ Issue</span><span style="color:${D.colors.pull}">■ PR</span><span style="color:${D.colors.repo}">■ 项目</span></div></div>${detail()}</div><div class="tm-network-foot">${mode().insight}</div></div>`;}
function update(){const host=$('#tm-world');if(host?.querySelector('[data-tm-network]'))host.innerHTML=render();}
function stop(){state.playing=false;}
document.addEventListener('click',e=>{const b=e.target.closest('[data-tm-network] button,[data-tm-network] [data-tm-net-node]');if(!b)return;const x=b.dataset,focused=document.activeElement===b,action=[...b.attributes].find(a=>a.name.startsWith('data-tm-net-'));
if(x.tmNetMode)state.mode=x.tmNetMode;
else if(x.tmNetNode)state.selected=state.selected===x.tmNetNode?null:x.tmNetNode;
else if('tmNetClear' in x)state.selected=null;
else if('tmNetPlay' in x)state.playing=!state.playing;
update();if(focused&&action)[...document.querySelectorAll(`[${action.name}]`)].find(n=>n.tagName===b.tagName&&n.getAttribute(action.name)===action.value)?.focus({preventScroll:true});
});
document.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)&&e.target.matches('[data-tm-network] svg [role=button]')){e.preventDefault();e.target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}});
document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();update();}});
window.TMAP_CONCEPT={render,stop,state,radius,data:()=>D};
})();
