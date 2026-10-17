/* Section 5.2: declared lineage, directed country flows, and ModelRank structure. */
window.createGOSM52 = function(D,H) {
  'use strict';
  const {esc,fmt,compact,txt,line,box,action,svg,btn,seg,note,link,asset,set}=H;
  const d3=window.d3;
  const theme=()=>H.colors().C, palette=()=>H.colors().palette;
  const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
  const trim=(s,n=25)=>String(s).length>n?String(s).slice(0,n-1)+'…':String(s);
  const sum=(a,k)=>a.reduce((n,r)=>n+Number(r[k]||0),0);
  const totalFlows=sum(D.flows,'weight');
  const names=new Map(D.geography.map(r=>[r.id,r.name]));names.set('OTH','其他国家');
  const nm=c=>names.get(c)||c;
  const countryOrder=[...new Set(D.flows.flatMap(r=>[r.source,r.target]))].sort((a,b)=>sum(D.flows.filter(r=>r.source===b||r.target===b),'weight')-sum(D.flows.filter(r=>r.source===a||r.target===a),'weight'));
  const col=c=>c==='CN'?palette()[0]:c==='US'?palette()[1]:c==='OTH'?theme().unknown:palette()[(countryOrder.indexOf(c)+2)%palette().length];
  const byId=new Map(D.network.nodes.map(n=>[n.id,n])),parents=new Map(),children=new Map();
  D.network.edges.forEach(e=>{if(!parents.has(e.target))parents.set(e.target,[]);parents.get(e.target).push(e.source);if(!children.has(e.source))children.set(e.source,[]);children.get(e.source).push(e.target);});
  const months=[...new Set(D.head.map(r=>r.month))];
  const defaults={
    network:{view:'overview',dimension:'2d',node:D.network.bases[0].id,hops:1,direction:'both',neighbors:'down',page:0,query:'',year:'2026-09-13',zoom:1,panX:0,panY:0},
    flows:{focus:'all',direction:'both',group:8,pin:'',country:'CN'},
    head:{k:100,months:26,month:months.at(-1),mode:'count',bands:'cumulative',unknown:true,playing:false}
  };
  const own=p=>Object.hasOwn(defaults,p.dataset.gmChart);
  const sb=(k,v,label,x,y,w,active=false,disabled=false)=>{
    const C=theme();const b=box(x,y,w,28,active?C.raised:C.bg,active?C.brand:C.line,4)+txt(x+w/2,y+19,label,14,disabled?C.unknown:active?C.brand:C.ink,'middle');
    return disabled?`<g aria-disabled="true">${b}</g>`:action(k,v,label,b);
  };
  const card=(x,y,w,title,value,sub='',c)=>box(x,y,w,62,theme().paper,theme().line,6)+txt(x+14,y+21,title,14,theme().muted)+txt(x+14,y+49,value,27,c||theme().ink)+txt(x+w-13,y+49,sub,13,theme().muted,'end');
  function paint(p,s,controls,b,readout,rows,source,height=650){
    const keys=[...new Set(rows.flatMap(r=>Object.keys(r)))];
    set(p,controls,svg(b,1280,height,p.querySelector('h3').textContent),note(readout),rows.map(r=>Object.fromEntries(keys.map(k=>[k,r[k]??'']))),source);
    p.dataset.evidence='observed';
  }
  function source(keys,explanation){return H.source(keys,explanation)+`<p>${link(asset('influence-methods.md'),'5.2图表口径与交互说明')}</p>`;}
  function miniTrend(rows,key,title,x,y,w,h,selected,color,percent=false) {
    const C=theme(),mx=Math.max(1,...rows.map(r=>r[key]))*1.12,px=x+55,py=y+33,iw=w-77,ih=h-61;
    const xx=i=>px+i*iw/(rows.length-1),yy=v=>py+ih-v/mx*ih,chosen=rows.find(r=>r.date===selected)||rows.at(-1);
    let b=txt(x+12,y+20,title,16,C.muted)+txt(x+w-12,y+20,percent?fmt(chosen[key],2)+'%':compact(chosen[key]),23,color,'end');
    for(let t=0;t<=2;t++){const v=mx*t/2,cy=yy(v);b+=line(px,cy,px+iw,cy,C.line)+txt(px-8,cy+4,percent?fmt(v,0)+'%':compact(v),12,C.muted,'end');}
    b+=`<path d="${rows.map((r,i)=>(i?'L':'M')+xx(i)+','+yy(r[key])).join(' ')}" stroke="${color}" stroke-width="2.5" fill="none"/>`;
    rows.forEach((r,i)=>{b+=action('year',r.date,`${r.date} ${title} ${r[key]}`,`<circle cx="${xx(i)}" cy="${yy(r[key])}" r="11" fill="${C.bg}" fill-opacity="0"/><circle cx="${xx(i)}" cy="${yy(r[key])}" r="${r.date===selected?5:3.5}" fill="${color}"/>`)+txt(xx(i),y+h-8,r.date.slice(0,4),13,C.muted,'middle');});return b;
  }
  function sliceNetwork(s){
    let nodes,positions=new Map(),levels=new Map();
    if(s.view==='overview'){
      nodes=D.network.overview.map(r=>byId.get(r.id));
      D.network.overview.forEach(r=>positions.set(r.id,{x:48+r.overviewX/1600*828,y:110+r.overviewY/1120*285,cluster:r.overviewCluster}));
    }else if(s.view==='all'){
      nodes=D.network.nodes;const xs=nodes.map(n=>n.x),ys=nodes.map(n=>n.y),xmin=Math.min(...xs),xmax=Math.max(...xs),ymin=Math.min(...ys),ymax=Math.max(...ys);
      nodes.forEach(n=>positions.set(n.id,{x:52+(n.x-xmin)/(xmax-xmin)*818,y:114+(n.y-ymin)/(ymax-ymin)*278,cluster:n.sourceCommunity%12}));
    }else{
      levels.set(s.node,0);
      for(const dir of s.direction==='both'?[-1,1]:s.direction==='up'?[-1]:[1]){
        let front=[s.node];for(let h=1;h<=s.hops;h++){const next=[];front.forEach(id=>(dir<0?parents:children).get(id)?.forEach(n=>{if(!levels.has(n)){levels.set(n,dir*h);next.push(n);}}));front=next;}
      }
      nodes=[...levels.keys()].map(id=>byId.get(id)).filter(Boolean);positions.set(s.node,{x:460,y:255,cluster:0});
      for(const l of [-2,-1,1,2]){
        const ns=nodes.filter(n=>levels.get(n.id)===l).sort((a,b)=>a.id.localeCompare(b.id));
        ns.forEach((n,i)=>{const a=-1.25+(i+.5)*2.5/ns.length,r=Math.abs(l)===1?210:382;positions.set(n.id,{x:460+Math.sign(l)*Math.cos(a)*r,y:255+Math.sin(a)*135,cluster:l<0?1:0});});
      }
    }
    const ids=new Set(nodes.map(n=>n.id)),edges=D.network.edges.filter(e=>ids.has(e.source)&&ids.has(e.target));return{nodes,edges,positions,levels};
  }
  function graph(s,slice){
    const C=theme(),{nodes,edges,positions}=slice;let b='';
    edges.forEach(e=>{const a=positions.get(e.source),z=positions.get(e.target),active=e.source===s.node||e.target===s.node;
      b+=`<path d="M${a.x},${a.y} Q${(a.x+z.x)/2},${(a.y+z.y)/2-8} ${z.x},${z.y}" stroke="${active?C.brand:C.line}" stroke-opacity="${active?.9:s.view==='all'?.28:.55}" stroke-width="${active?1.6:.7}" fill="none" ${active&&nodes.length<100?'marker-end="url(#s52-arrow)"':''}><title>${esc(e.source+' → '+e.target)}</title></path>`;
    });
    nodes.forEach(n=>{const p=positions.get(n.id),on=n.id===s.node,r=on?8:Math.min(7,2+Math.sqrt(n.downstreamCount)*.43);b+=action('node',n.id,`${n.id}，样本内直接下游 ${n.downstreamCount}`,`<circle cx="${p.x}" cy="${p.y}" r="${r+3}" fill="${C.bg}" fill-opacity="0"/><circle cx="${p.x}" cy="${p.y}" r="${r}" fill="${on?C.gold:palette()[(p.cluster||0)%palette().length]}" stroke="${on?C.ink:C.bg}" stroke-width="${on?1.5:.35}"/>`);});
    const labels=s.view==='overview'?D.network.bases.map(r=>byId.get(r.id)):nodes.filter(n=>n.id===s.node||(s.view==='lineage'&&nodes.length<=13));
    labels.forEach(n=>{const p=positions.get(n.id);if(p)b+=txt(p.x,p.y-13,trim(n.name,24),12,C.ink,'middle',`paint-order="stroke" stroke="${C.bg}" stroke-width="4" stroke-linejoin="round" pointer-events="none"`);});
    return `<defs><clipPath id="s52-graph-clip"><rect x="20" y="94" width="880" height="316" rx="6"/></clipPath><marker id="s52-arrow" viewBox="0 0 10 10" refX="12" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="${C.brand}"/></marker></defs><g class="s52-net-2d" clip-path="url(#s52-graph-clip)"><rect data-s52-pan="true" x="20" y="94" width="880" height="316" fill="${C.bg}"/><g data-s52-camera transform="${camera(s)}">${b}</g></g>`;
  }
  const camera=s=>`translate(${460+s.panX} ${255+s.panY}) scale(${s.zoom}) translate(-460 -255)`;
  function concept(){
    const C=theme();let b=txt(40,125,'派生表示“在已有模型基础上继续开发”',22,C.ink)+txt(40,156,'关系示意 · 一个模型可有多个上游，也可成为新的基座',15,C.muted);
    for(const [x,y,w,title,sub,c] of [[48,206,190,'基座 A','已有的模型能力',palette()[0]],[48,314,190,'基座 B','可作为另一上游',palette()[1]],[338,233,235,'派生模型','调整、适配或合并',palette()[2]],[683,233,190,'后续派生','继续成为创新起点',palette()[0]]]){
      b+=box(x,y,w,74,C.paper,C.line,7)+txt(x+w/2,y+29,title,21,c,'middle')+txt(x+w/2,y+55,sub,15,C.muted,'middle');
    }
    b+=`<path d="M238 243 C285 243 285 250 338 250" fill="none" stroke="${C.brand}" stroke-width="2.5" marker-end="url(#s52-concept-arrow)"/>`;
    b+=`<path d="M238 350 C290 350 290 290 338 290" fill="none" stroke="${C.brand}" stroke-width="2.5" marker-end="url(#s52-concept-arrow)"/><path d="M573 270 H683" fill="none" stroke="${C.brand}" stroke-width="2.5" marker-end="url(#s52-concept-arrow)"/>`;
    b+=`<defs><marker id="s52-concept-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="${C.brand}"/></marker></defs>`;return b;
  }
  function networkSide(s){
    const C=theme(),n=byId.get(s.node);let b=box(924,94,338,316,C.paper,C.line,7);
    if(s.view==='concept')return b+txt(942,126,'怎样读这张图？',21,C.ink)+txt(942,166,'点：一个公开模型仓库',17,C.muted)+txt(942,198,'箭头：基座 → 派生',17,C.muted)+txt(942,230,'大小：样本内直接下游数',17,C.muted)+txt(942,268,'微调、量化、适配与合并',17,C.ink)+txt(942,294,'是常见开发活动；关系样本',16,C.muted)+txt(942,319,'未逐条区分这些技术类型。',16,C.muted)+txt(942,382,'切换“网络全景”探索真实记录 →',15,C.brand);
    b+=txt(942,118,'所选模型 · 样本内记录',13,C.muted)+txt(942,144,trim(n.publisher,33),17,C.brand)+txt(942,168,trim(n.name,31),18,C.ink);
    b+=txt(942,199,`上游 ${n.upstreamCount}`,19,palette()[1])+txt(1074,199,`下游 ${n.downstreamCount}`,19,palette()[0]);
    b+=sb('view','lineage','展开谱系',942,212,102,s.view==='lineage')+sb('neighbors','up','看上游',1052,212,91,s.neighbors==='up')+sb('neighbors','down','看下游',1151,212,91,s.neighbors==='down');
    let rows=(s.neighbors==='up'?parents:children).get(n.id)||[];rows=rows.slice().sort((a,b)=>byId.get(b).downstreamCount-byId.get(a).downstreamCount||a.localeCompare(b));
    const last=Math.max(0,Math.ceil(rows.length/4)-1);s.page=clamp(s.page,0,last);
    rows.slice(s.page*4,s.page*4+4).forEach((id,i)=>{const m=byId.get(id),y=251+i*27;b+=action('node',id,id,box(939,y,307,25,C.bg,'none',3)+txt(949,y+18,trim(m.id,37),14,C.ink));});
    if(!rows.length)b+=txt(942,282,'当前样本没有记录此方向的邻居。',15,C.muted);
    b+=sb('neighborPage','prev','←',942,372,34,false,s.page===0)+txt(1007,391,`${s.page+1}/${last+1}`,13,C.muted,'middle')+sb('neighborPage','next','→',1036,372,34,false,s.page===last)+`<a href="${esc(n.url)}" target="_blank" rel="noopener">${txt(1241,391,'模型卡 ↗',15,C.brand,'end')}</a>`;return b;
  }
  let threePromise;
  function network(p,s){
    if(p.gm3d){s.orbit=p.gm3d.snapshot();p.gm3d.dispose();p.gm3d=null;}
    p.gmRenderToken=(p.gmRenderToken||0)+1;
    const C=theme(),slice=sliceNetwork(s),yr=D.derivation.find(r=>r.date===s.year)||D.derivation.at(-1),prev=D.derivation[D.derivation.indexOf(yr)-1];
    let controls=seg('view',[['concept','读懂派生'],['overview','网络全景'],['all','全部样本'],['lineage','所选谱系']],s.view)+seg('dimension',[['2d','2D'],['3d','3D']],s.dimension)+`<div class="s52-search"><input type="search" data-s52-search="network" placeholder="搜索模型或发布账号" aria-label="搜索模型或发布账号" autocomplete="off"><div class="s52-search-results" hidden></div></div>`;
    controls+=`<div class="s51-control-line">${s.view==='lineage'?seg('direction',[['both','上下游'],['up','上游'],['down','下游']],s.direction)+seg('hops',[[1,'1层'],[2,'2层']],s.hops):'<span class="s52-caption">基座 → 派生 · 位置用于导航，节点大小不是ModelRank</span>'}${btn('zoom','in','＋')}${btn('zoom','out','−')}${btn('reset','','复位')}<span class="s52-caption">网络快照 2026-10-16</span></div>`;
    let b=card(18,4,402,'可见派生模型 · '+s.year.slice(0,4),compact(yr.derived_models),prev?'同比 +'+fmt((yr.derived_models/prev.derived_models-1)*100,1)+'%':'起始观测',palette()[0])+card(438,4,402,'占同期可见模型',fmt(yr.derived_pct,2)+'%',prev?'较上年 '+fmt(yr.derived_pct-prev.derived_pct,2)+'pp':'',palette()[1])+card(858,4,404,'完整声明关系样本',fmt(D.network.nodes.length)+' 模型',fmt(D.network.edges.length)+' 条关系');
    b+=txt(24,87,s.view==='concept'?'关系入门 · 概念示意':`${s.view==='lineage'?'所选模型谱系':s.view==='all'?'完整非随机样本':'12个发布账号的基座簇群'} · ${fmt(slice.nodes.length)} 模型 / ${fmt(slice.edges.length)} 条关系`,15,C.muted);
    b+=s.view==='concept'?concept():graph(s,slice);b+=networkSide(s);
    b+=box(18,430,1244,202,C.paper,C.line,7)+txt(34,455,'复用增长',20,C.ink)+txt(167,455,'点击年份联动两条曲线；网络不随年份回放',14,C.muted)+txt(1241,455,'各年9月13日 · 同一快照回溯',14,C.muted,'end');
    b+=miniTrend(D.derivation,'derived_models','累计可识别派生模型',26,468,606,160,s.year,palette()[0])+miniTrend(D.derivation,'derived_pct','派生模型占比',646,468,606,160,s.year,palette()[1],true);
    const rows=[...(s.view==='concept'?[]:slice.edges).map(e=>({记录类型:'声明关系样本',日期:'2026-10-16',基座:e.source,派生:e.target,关系类型:'模型卡声明'})),...D.derivation.map(r=>({记录类型:'全平台累计回溯',日期:r.date,模型总数:r.models,派生模型数:r.derived_models,派生占比_pct:r.derived_pct}))];
    paint(p,s,controls,b,'网络与增长为独立证据。声明关系样本非全平台；缺少基座声明不等于原创。拖动空白处平移，点击节点探索。',rows,source(['derivation'],`网络取自 ${link(D.network.meta.sourceFile,'参考项目固定关系快照')}；上游 ${link(D.network.meta.upstreamDataset,'hub-stats')}。只保留明确声明的基座关系，排除同作者与任务相似等推断连线。677节点概览选12个发布账号，完整样本含5,777模型、5,111条边，来自前12,000模型的非随机输入样本。模型卡声明尚不等于训练过程经过独立核验。布局、颜色与三维纵深用于阅读，不表示ModelRank。网络没有完整创建日期，因此年份选择只改变增长读数。`)+`<p>${link(asset('network.json'),'完整网络JSON')} · ${link(asset('lineage-live-provenance.json'),'抽取与固定来源')}</p>`);
    p.gmNetworkSlice=slice;p.s52Slice=slice;
    const sv=p.querySelector('.gm-svg');bindPan(p,sv,s);
    if(s.dimension==='3d'&&s.view!=='concept'){
      const fo=document.createElementNS('http://www.w3.org/2000/svg','foreignObject');fo.setAttribute('x','20');fo.setAttribute('y','94');fo.setAttribute('width','880');fo.setAttribute('height','316');fo.innerHTML='<div xmlns="http://www.w3.org/1999/xhtml" class="s52-three-host"><span>正在载入3D…</span></div>';sv.append(fo);const host=fo.firstElementChild,token=p.gmRenderToken;
      (threePromise||(threePromise=import(`${H.base}/gosm-network.mjs?v=${D.version}`))).then(m=>{
        if(p.gmRenderToken!==token||!host.isConnected)return;
        host.innerHTML='';p.gm3d=m.mount(host,{nodes:slice.nodes,edges:slice.edges,positions:[...slice.positions].map(([id,q])=>[id,{x:(q.x-20)/880*1200,y:(q.y-94)/316*820,cluster:q.cluster}]),orbit:s.orbit,selected:s.node,colors:{...theme(),palette:palette()},onSelect:id=>{s.node=id;s.page=0;H.draw(p);},onContextLost:()=>{fo.remove();sv.classList.remove('s52-three-ready');p.querySelector('.gm-readout').innerHTML=note('3D上下文已中断，已保留完整2D交互。');}});sv.classList.add('s52-three-ready');
      }).catch(()=>{if(host.isConnected){fo.remove();p.querySelector('.gm-readout').innerHTML=note('此环境无法启用3D，已保留完整2D交互。网络与趋势为独立样本。');}});
    }
  }
  function bindPan(p,sv,s){let drag;
    sv.addEventListener('pointerdown',e=>{if(e.button!==0||!e.target.hasAttribute('data-s52-pan'))return;drag={x:e.clientX,y:e.clientY,px:s.panX,py:s.panY};sv.setPointerCapture?.(e.pointerId);});
    sv.addEventListener('pointermove',e=>{if(!drag)return;const r=sv.getBoundingClientRect(),scale=Math.min(r.width/1280,r.height/650)||1;s.panX=drag.px+(e.clientX-drag.x)/scale;s.panY=drag.py+(e.clientY-drag.y)/scale;sv.querySelector('[data-s52-camera]')?.setAttribute('transform',camera(s));});
    for(const type of ['pointerup','pointercancel'])sv.addEventListener(type,()=>drag=null);
  }
  function filteredFlows(s){
    const focus=s.focus==='all'?[]:s.focus==='compare'?['CN','US']:[s.focus];
    return D.flows.filter(r=>!focus.length||(s.direction==='out'?focus.includes(r.source):s.direction==='in'?focus.includes(r.target):focus.includes(r.source)||focus.includes(r.target)));
  }
  function aggregateFlows(rows,s){
    const totals=new Map();rows.forEach(r=>{totals.set(r.source,(totals.get(r.source)||0)+r.weight);totals.set(r.target,(totals.get(r.target)||0)+r.weight);});
    const keep=[...totals].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,s.group).map(r=>r[0]);
    for(const c of s.focus==='compare'?['CN','US']:s.focus==='all'?[]:[s.focus])if(!keep.includes(c))keep.push(c);
    const bag=new Map();rows.forEach(r=>{const a=keep.includes(r.source)?r.source:'OTH',b=keep.includes(r.target)?r.target:'OTH',key=a+'|'+b;if(!bag.has(key))bag.set(key,{source:a,target:b,weight:0,members:[]});const e=bag.get(key);e.weight+=r.weight;e.members.push(r);});
    const edges=[...bag.values()].sort((a,b)=>b.weight-a.weight),ids=[...new Set(edges.flatMap(e=>[e.source,e.target]))].sort((a,b)=>a==='OTH'?1:b==='OTH'?-1:countryOrder.indexOf(a)-countryOrder.indexOf(b));return{edges,ids,keep};
  }
  const edgeDesc=e=>`${nm(e.source)} → ${nm(e.target)}：${fmt(e.weight)} 对${e.source==='OTH'||e.target==='OTH'?'（合并显示）':''}`;
  function flowAction(key,v,label,b,attrs=''){return `<g role="button" tabindex="0" data-gm-action="${key}" data-value="${esc(v)}" ${attrs} class="gm-svg-action">${b}<title>${esc(label)}</title></g>`;}
  function sankey(edges){
    const C=theme(),left=111,right=539,bar=10,top=130,h=310,pad=10,total=sum(edges,'weight');
    const ids=k=>[...new Set(edges.map(r=>r[k]))].sort((a,b)=>a==='OTH'?1:b==='OTH'?-1:sum(edges.filter(r=>r[k]===b),'weight')-sum(edges.filter(r=>r[k]===a),'weight'));
    const src=ids('source'),dst=ids('target'),ky=Math.min((h-pad*(src.length-1))/(total||1),(h-pad*(dst.length-1))/(total||1));
    const layout=(ids,k)=>{let y=top;return new Map(ids.map(c=>{const value=sum(edges.filter(r=>r[k]===c),'weight'),q={y,h:value*ky,cursor:0,value};y+=q.h+pad;return[c,q];}));};
    const a=layout(src,'source'),b=layout(dst,'target');let out=txt(103,112,'基座来源国',15,C.muted,'middle')+txt(549,112,'派生发布国',15,C.muted,'middle');
    edges.forEach(e=>{const s=a.get(e.source),t=b.get(e.target),dy=e.weight*ky,sy=s.y+s.cursor+dy/2,ty=t.y+t.cursor+dy/2;s.cursor+=dy;t.cursor+=dy;
      out+=flowAction('flowPair',e.source+'|'+e.target,edgeDesc(e),`<path d="M${left+bar},${sy} C280,${sy} 378,${ty} ${right},${ty}" fill="none" stroke="${col(e.source)}" stroke-width="${Math.max(.2,dy)}"/>`,`data-s52-edge="${e.source}|${e.target}" opacity=".58"`);
    });
    const nodes=(ids,lay,x,isLeft)=>{
      const ys=[];let last=112;for(const c of ids){const q=lay.get(c);last=Math.max(last+21,q.y+q.h/2);ys.push(last);}
      if(ys.at(-1)>449){ys[ys.length-1]=449;for(let i=ys.length-2;i>=0;i--)ys[i]=Math.min(ys[i],ys[i+1]-21);}
      ids.forEach((c,i)=>{const q=lay.get(c),y=ys[i];out+=flowAction('flowNode',c,nm(c)+'：'+fmt(q.value)+' 对',box(x,q.y,bar,Math.max(.6,q.h),col(c),'none',0)+line(isLeft?x:x+bar,q.y+q.h/2,isLeft?x-7:x+bar+7,y,col(c),.8)+txt(isLeft?x-9:x+bar+9,y+5,trim(nm(c),4),14,C.ink,isLeft?'end':'start'),`data-s52-country="${c}"`);});
    };nodes(src,a,left,true);nodes(dst,b,right,false);return out;
  }
  function chord(edges,ids){
    const C=theme(),cx=826,cy=279,r=104,idx=new Map(ids.map((id,i)=>[id,i])),matrix=ids.map(()=>ids.map(()=>0));edges.forEach(e=>matrix[idx.get(e.source)][idx.get(e.target)]+=e.weight);
    const chords=d3.chordDirected().padAngle(.034).sortSubgroups(d3.descending)(matrix),arc=d3.arc().innerRadius(r+4).outerRadius(r+14),ribbon=d3.ribbonArrow().radius(r).padAngle(.002).headRadius(8);let b=txt(cx,112,'有向弦图 · 箭头指向派生发布国',14,C.muted,'middle');
    chords.forEach(ch=>{const a=ids[ch.source.index],z=ids[ch.target.index],e=edges.find(e=>e.source===a&&e.target===z);b+=flowAction('flowPair',a+'|'+z,edgeDesc(e),`<path d="${ribbon(ch)}" fill="${col(a)}"/>`,`data-s52-edge="${a}|${z}" opacity=".58" transform="translate(${cx} ${cy})"`);});
    // Label slots avoid overlap even when the smaller arcs cluster together.
    const groups=chords.groups.map(g=>{const a=(g.startAngle+g.endAngle)/2-Math.PI/2;return{g,c:ids[g.index],ax:cx+Math.cos(a)*(r+15),ay:cy+Math.sin(a)*(r+15),side:Math.cos(a)>=0?1:-1,y:cy+Math.sin(a)*165};});
    for(const side of [-1,1]){const gs=groups.filter(q=>q.side===side).sort((a,b)=>a.y-b.y);let y=126;for(const q of gs){q.y=Math.max(q.y,y);y=q.y+23;}if(gs.at(-1)?.y>441){gs.at(-1).y=441;for(let i=gs.length-2;i>=0;i--)gs[i].y=Math.min(gs[i].y,gs[i+1].y-23);}}
    groups.forEach(q=>{const tx=cx+q.side*134;b+=flowAction('flowNode',q.c,nm(q.c),`<path d="${arc(q.g)}" fill="${col(q.c)}" transform="translate(${cx} ${cy})"/>`+line(q.ax,q.ay,tx,q.y,col(q.c),.7)+txt(tx+q.side*3,q.y+4,q.c==='OTH'?'其他':trim(nm(q.c),3),13,C.ink,q.side>0?'start':'end'),`data-s52-country="${q.c}"`);});
    b+=txt(cx,468,'外弧合计两端连接；颜色表示基座来源',13,C.muted,'middle');return b;
  }
  function flowDetail(s,rows,agg){
    const C=theme(),x=1039;let b=box(1025,84,237,394,C.paper,C.line,7),edge=agg.edges.find(e=>e.source+'|'+e.target===s.pin);
    if(s.pin.startsWith('node:')){
      const code=s.pin.slice(5),inRows=rows.filter(r=>r.target===code),outRows=rows.filter(r=>r.source===code);b+=txt(x,111,'所选国家 · 当前筛选内',13,C.muted)+txt(x,142,nm(code),22,col(code));
      if(code==='OTH'){b+=txt(x,181,'合并显示的其他国家',16,C.ink)+txt(x,210,'包含多个实际国家。',15,C.muted)+txt(x,238,'请用上方选择器单独探索。',15,C.muted);return b;}
      b+=txt(x,183,'提供基座',15,C.muted)+txt(1247,183,fmt(sum(outRows,'weight')),22,C.ink,'end')+txt(x,219,'接收派生',15,C.muted)+txt(1247,219,fmt(sum(inRows,'weight')),22,C.ink,'end');
      const partners=new Map();[...inRows,...outRows].forEach(e=>{const c=e.source===code?e.target:e.source;partners.set(c,(partners.get(c)||0)+e.weight);});b+=txt(x,258,'主要伙伴 · 双向连接数',14,C.muted);
      [...partners].sort((a,b)=>b[1]-a[1]).slice(0,4).forEach(([c,n],i)=>b+=action('focus',c,'聚焦'+nm(c),txt(x,290+i*32,nm(c),16,col(c))+txt(1247,290+i*32,fmt(n),17,C.ink,'end')));return b;
    }
    edge=edge||agg.edges[0];if(!edge)return b+txt(x,123,'暂无匹配关系',20,C.muted);
    b+=txt(x,111,s.pin?'所选流向':'当前最大流向',13,C.muted)+txt(x,143,trim(nm(edge.source)+' → '+nm(edge.target),14),(nm(edge.source)+' → '+nm(edge.target)).length>10?15:21,C.ink)+txt(x,188,fmt(edge.weight),34,col(edge.source))+txt(x,214,'对基座—派生关系',15,C.muted);
    b+=line(x,235,1247,235)+txt(x,263,'占全部跨国样本',14,C.muted)+txt(1247,289,fmt(edge.weight/totalFlows*100,1)+'%',26,C.ink,'end')+txt(x,322,'占当前筛选关系',14,C.muted)+txt(1247,348,fmt(edge.weight/(sum(rows,'weight')||1)*100,1)+'%',26,C.ink,'end');
    b+=txt(x,389,edge.members.length>1?`合并 ${edge.members.length} 条国家流向`:'点击连线可固定查看',14,C.muted)+txt(x,419,'悬停：两图同步高亮',14,C.muted)+txt(x,446,'点击外弧：查看国家角色',14,C.muted);return b;
  }
  function flows(p,s){
    const C=theme(),rows=filteredFlows(s),agg=aggregateFlows(rows,s),count=sum(rows,'weight'),largest=agg.edges[0];
    let controls=seg('focus',[['all','全球'],['CN','中国'],['US','美国'],['compare','中美']],s.focus)+seg('direction',[['both','双向连接'],['out','基座输出'],['in','派生接收']],s.direction)+`<label class="s52-select-label">更多国家 <select data-s52-select="focus" aria-label="选择派生关系国家"><option value="all">选择国家</option>${countryOrder.map(c=>`<option value="${c}" ${s.focus===c?'selected':''}>${esc(nm(c))}</option>`).join('')}</select></label>`;
    controls+=`<div class="s51-control-line">${seg('group',[[6,'前6国'],[8,'前8国'],[10,'前10国']],s.group,'图面')}${btn('flowClear','','清除高亮')}<span class="s52-caption">其余国家合并展示，全部关系计数保留 · 2026-09-13</span></div>`;
    let b=card(18,4,298,'当前筛选关系',fmt(count),'对',palette()[0])+card(334,4,298,'基座来源国家',fmt(new Set(rows.map(r=>r.source)).size),'个')+card(650,4,298,'派生发布国家',fmt(new Set(rows.map(r=>r.target)).size),'个')+card(966,4,296,'占全部已识别跨国关系',fmt(count/totalFlows*100,1)+'%','共 '+fmt(totalFlows)+' 对');
    b+=box(18,84,610,394,C.bg,C.line,7)+box(644,84,365,394,C.bg,C.line,7)+sankey(agg.edges)+chord(agg.edges,agg.ids)+flowDetail(s,rows,agg);
    b+=txt(27,507,'中美角色对照',18,C.ink)+txt(186,507,'完整跨国样本 · 不随上方筛选改变',14,C.muted);
    for(const [code,i] of [['CN',0],['US',1]]){const x=18+i*632,output=sum(D.flows.filter(e=>e.source===code),'weight'),input=sum(D.flows.filter(e=>e.target===code),'weight'),other=code==='CN'?'US':'CN',bilateral=D.flows.find(e=>e.source===code&&e.target===other).weight;
      let v=box(x,523,612,99,C.paper,C.line,6)+txt(x+16,550,nm(code),21,col(code));
      [['提供基座',output],['接收派生',input],[`${nm(code)} → ${nm(other)}`,bilateral]].forEach(([l,n],j)=>{const px=x+116+j*160;v+=txt(px,550,l,14,C.muted)+txt(px,583,fmt(n),25,j===2?col(code):C.ink);});
      v+=txt(x+16,607,'单位：关系对',13,C.muted);b+=action('focus',code,'聚焦'+nm(code),v);
    }
    paint(p,s,controls,b,'同一有向关系集：基座来源 → 派生发布。其他→其他仍是不同实际国家之间的跨国连接；关系不表示人员迁移或部署量。',rows.map(r=>({数据类型:'报告观测',日期:'2026-09-13',基座来源国家:r.source,派生发布国家:r.target,关系对数:r.weight,全部跨国样本份额_pct:r.weight/totalFlows*100,当前筛选份额_pct:r.weight/(count||1)*100})),source(['flows'],'原报告底表186条有向国家流向，共10,943对跨国关系。用户提供的5.2修订稿明确source为基座来源，target为派生发布，并以中国输出5,888、美国接收7,513、中国→美国4,639与原表逐项核对。完整89.22万对派生关系中，双端国家可识别约2.59%（含境内）；本图仅为其中的跨国子集，不把10,943/89.22万当作2.59%。国家按发布主体归属，不是使用者位置。小国合并只影响图面，CSV保留每条原始方向。弦图外弧按入出两端计量，不表示独立模型数。'));
    p.s52FlowRows=rows;p.s52Aggregated=agg;bindFlowHover(p,s);
  }
  function highlightFlow(p,key){
    p.querySelectorAll('[data-s52-edge]').forEach(g=>{const pair=g.dataset.s52Edge,match=!key||(key.startsWith('node:')?pair.split('|').includes(key.slice(5)):pair===key);g.setAttribute('opacity',!key?'.58':match?'.95':'.08');});
    p.querySelectorAll('[data-s52-country]').forEach(g=>{const c=g.dataset.s52Country,match=!key||(key.startsWith('node:')?c===key.slice(5):key.split('|').includes(c));g.setAttribute('opacity',match?'1':'.25');});
  }
  function bindFlowHover(p,s){highlightFlow(p,s.pin);for(const type of ['pointerover','focusin'])p.querySelector('.gm-view').addEventListener(type,e=>{const el=e.target.closest?.('[data-s52-edge],[data-s52-country]');if(el)highlightFlow(p,el.dataset.s52Edge||'node:'+el.dataset.s52Country);});for(const type of ['pointerout','focusout'])p.querySelector('.gm-view').addEventListener(type,()=>highlightFlow(p,s.pin));}
  function headRows(s){return D.head.filter(r=>r.k===s.k).slice(-s.months);}
  function head(p,s){
    const C=theme(),rows=headRows(s);if(!rows.some(r=>r.month===s.month))s.month=rows.at(-1).month;
    const chosen=rows.find(r=>r.month===s.month),start=rows[0],latest=rows.at(-1),delta=chosen.us-chosen.china,idx=rows.indexOf(chosen);
    let controls=seg('k',[[20,'Top 20'],[100,'Top 100'],[1000,'Top 1000']],s.k)+seg('months',[[6,'6个月'],[12,'12个月'],[18,'18个月'],[26,'全部26个月']],s.months)+seg('mode',[['count','席位数'],['share','占比']],s.mode);
    controls+=`<div class="s51-control-line">${btn('monthStep','prev','←',false,idx===0?'disabled aria-label="上个月"':'aria-label="上个月"')}<input type="range" min="0" max="${rows.length-1}" step="1" value="${idx}" data-s52-month aria-label="选择ModelRank月份"><strong class="s52-month-label">${s.month}</strong>${btn('monthStep','next','→',false,idx===rows.length-1?'disabled aria-label="下个月"':'aria-label="下个月"')}${btn('play','',s.playing?'暂停':'播放',s.playing)}${btn('unknown','',s.unknown?'未知曲线：显示':'未知曲线：隐藏',s.unknown)}</div>`;
    const show=v=>s.mode==='share'?fmt(v/s.k*100,1)+'%':fmt(v)+' 席';
    let b=card(18,4,402,`中国 · ${s.month} · Top ${s.k}`,show(chosen.china),`较${start.month} ${chosen.china-start.china>=0?'+':''}${chosen.china-start.china}席`,palette()[0])+card(438,4,402,`美国 · ${s.month} · Top ${s.k}`,show(chosen.us),`较${start.month} ${chosen.us-start.us>=0?'+':''}${chosen.us-start.us}席`,palette()[1])+card(858,4,404,'当月中美差距',fmt(Math.abs(delta))+' 席',delta===0?'席位相同':(delta>0?'美国':'中国')+'较多');
    b+=box(18,84,594,364,C.bg,C.line,7)+box(628,84,634,364,C.bg,C.line,7);
    b+=txt(35,112,`${s.month} · 三档榜单结构`,20,C.ink)+sb('bands','cumulative','累计榜单',338,92,112,s.bands==='cumulative')+sb('bands','segments','分段观察',458,92,112,s.bands==='segments');
    const keys=['china','us','other_known','unknown'],labels=['中国','美国','其他已识别','归属未知'],cs=[palette()[0],palette()[1],palette()[3],C.unknown];
    [20,100,1000].forEach((k,i)=>{
      const r=D.head.find(r=>r.k===k&&r.month===s.month),prev=i?D.head.find(r=>r.k===[20,100][i-1]&&r.month===s.month):null,segment=s.bands==='segments',den=segment?k-(prev?.k||0):k,y=164+i*87;
      const values=keys.map(key=>r[key]-(segment?(prev?.[key]||0):0));
      b+=action('k',k,'选择Top '+k,box(28,y-24,574,76,s.k===k?C.paper:C.bg,s.k===k?C.line:'none',5));
      b+=txt(39,y-4,segment?(i===0?'第1—20名':i===1?'第21—100名':'第101—1000名'):'Top '+k,16,C.ink)+txt(588,y-4,segment?`${den}个版本席位`:`已识别 ${fmt(r.coverage_pct,1)}%`,13,C.muted,'end');
      let x=40;values.forEach((v,j)=>{const width=v/den*546;b+=action('k',k,`${segment?'分段':'Top '+k} · ${labels[j]} ${v} 席`,box(x,y+8,width,30,cs[j],'none',0)+(width>34?txt(x+width/2,y+29,String(v),14,j===3?C.bg:'#FFFFFF','middle','font-weight="600"'):''));x+=width;});
    });
    labels.forEach((l,i)=>{const x=36+(i%2)*282,y=418+Math.floor(i/2)*20;b+=box(x,y-10,9,9,cs[i],'none',1)+txt(x+15,y,l,13,C.muted);});
    b+=txt(647,112,`Top ${s.k} · 月度${s.mode==='share'?'席位占比':'席位数'}`,20,C.ink)+txt(1243,112,`${rows[0].month}—${rows.at(-1).month}`,14,C.muted,'end');
    const px=682,py=151,w=529,h=238,visible=s.unknown?['china','us','unknown']:['china','us'],mx=s.mode==='share'?Math.min(100,Math.ceil(Math.max(...rows.flatMap(r=>visible.map(k=>r[k]/s.k*100)))/10)*10+10):Math.ceil(Math.max(1,...rows.flatMap(r=>visible.map(k=>r[k])))*1.12/10)*10;
    const xx=i=>px+i*w/(rows.length-1),val=(r,k)=>s.mode==='share'?r[k]/s.k*100:r[k],yy=v=>py+h-v/mx*h;
    for(let t=0;t<=4;t++){const v=mx*t/4,y=yy(v);b+=line(px,y,px+w,y,C.line)+txt(px-9,y+4,fmt(v,0)+(s.mode==='share'?'%':''),13,C.muted,'end');}
    visible.forEach(key=>{const c=key==='china'?palette()[0]:key==='us'?palette()[1]:C.unknown;b+=`<path d="${rows.map((r,i)=>(i?'L':'M')+xx(i)+','+yy(val(r,key))).join(' ')}" fill="none" stroke="${c}" stroke-width="${key==='unknown'?2:2.7}" ${key==='unknown'?'stroke-dasharray="4 4"':''}/>`;rows.forEach((r,i)=>b+=`<circle cx="${xx(i)}" cy="${yy(val(r,key))}" r="${r.month===s.month?5:2.5}" fill="${c}"/>`);});
    b+=line(xx(idx),py-8,xx(idx),py+h,C.gold,1,'stroke-dasharray="4 4"');
    rows.forEach((r,i)=>{const step=w/(rows.length-1),tx=xx(i);b+=action('month',r.month,`${r.month} 中国 ${r.china} 美国 ${r.us} 未知 ${r.unknown}`,`<rect x="${Math.max(px,tx-step/2)}" y="${py-9}" width="${i===0||i===rows.length-1?step/2:step}" height="${h+18}" fill="${C.bg}" fill-opacity="0"/>`);if(i===0||i===rows.length-1||i%Math.ceil(rows.length/5)===0&&rows.length-1-i>=Math.ceil(rows.length/5))b+=txt(tx,414,r.month.slice(2),12,C.muted,'middle');});
    b+=txt(648,438,'点选月份同步左侧结构与上方读数',13,C.muted)+txt(1244,438,s.unknown?'虚线：归属未知':'未知仍计入份额分母',13,C.muted,'end');
    b+=box(18,470,1244,150,C.paper,C.line,7)+txt(35,498,`Top ${s.k} · 从窗口起点到所选月份`,18,C.ink)+txt(1241,498,`${start.month} → ${s.month}`,15,C.muted,'end');
    [['中国席位',start.china,chosen.china,palette()[0]],['美国席位',start.us,chosen.us,palette()[1]],['中美席位差',Math.abs(start.us-start.china),Math.abs(delta),C.ink],['未知归属',start.unknown,chosen.unknown,C.unknown]].forEach(([l,a,z,c],i)=>{const x=35+i*310;b+=txt(x,532,l,15,C.muted)+txt(x,566,`${a} → ${z}`,28,c);});
    b+=txt(35,602,s.bands==='segments'?'分段席位由同月Top100−Top20、Top1000−Top100计算；累计与分段分别阅读。':'累计榜单相互包含，不能把Top20、Top100与Top1000的席位相加。',14,C.muted);
    paint(p,s,controls,b,'按模型版本计席位，未知归属保留在每档榜单分母。ModelRank描述生态影响，席位数不等于影响力分数份额或测试性能。',D.head.filter(r=>rows.some(q=>q.month===r.month)).map(r=>({数据类型:'ModelRank原报告月表',月份:r.month,榜单深度:r.k,中国:r.china,美国:r.us,其他已识别:r.other_known,未知归属:r.unknown,中国份额_pct:r.china_pct,美国份额_pct:r.us_pct,国家识别覆盖_pct:r.coverage_pct})),source(['head'],'原表覆盖2024-07至2026-08，共26个月、78行TopK汇总。每月Top20/100/1000分别计数，份额分别除以20/100/1000，不排除未知归属。图面不据这些聚合值生成具体模型名单；具体模型查第三章M-Ranking。分段为同月嵌套榜单相减，不跨月份减去不同集合。滚动窗口起点变化时，“较起点”随之变化。'));
  }
  function resetCamera(s){s.zoom=1;s.panX=0;s.panY=0;s.orbit=null;}
  const timers=new Map();
  function stop(p,s){if(timers.has(p)){clearInterval(timers.get(p));timers.delete(p);}s.playing=false;}
  function handle(p,s,k,v){
    if(!own(p))return false;
    if(k==='table-page'){s.tablePage=Math.max(0,(s.tablePage||0)+(v==='next'?1:-1));return true;}
    s.tablePage=0;
    if(p.dataset.gmChart==='network'){
      if(k==='node'){if(byId.has(v)){s.node=v;s.page=0;if(s.view==='concept')s.view='lineage';if(s.view==='lineage')resetCamera(s);}}
      else if(k==='neighborPage')s.page=Math.max(0,s.page+(v==='next'?1:-1));
      else if(k==='zoom'){if(s.dimension==='3d'&&p.gm3d)p.gm3d.zoom(v==='in'?.8:1.25);else s.zoom=clamp(s.zoom*(v==='in'?1.3:1/1.3),.5,5);}
      else if(k==='reset'){resetCamera(s);p.gm3d?.reset();}
      else if(k==='view'){s.view=v;resetCamera(s);}
      else if(k==='neighbors'){s.neighbors=v;s.page=0;}
      else if(k==='hops'){s.hops=Number(v);resetCamera(s);}
      else s[k]=v;
    }else if(p.dataset.gmChart==='flows'){
      if(k==='flowPair'){s.pin=s.pin===v?'':v;}
      else if(k==='flowNode'){s.pin=s.pin==='node:'+v?'':'node:'+v;}
      else if(k==='flowClear')s.pin='';
      else{s[k]=k==='group'?Number(v):v;s.pin='';}
    }else{
      if(k==='play'){
        if(s.playing)stop(p,s);else{let rows=headRows(s);if(s.month===rows.at(-1).month)s.month=rows[0].month;s.playing=true;timers.set(p,setInterval(()=>{if(!p.isConnected||document.hidden){stop(p,s);H.draw(p);return;}const r=headRows(s),i=r.findIndex(r=>r.month===s.month);if(i>=r.length-1){stop(p,s);H.draw(p);return;}s.month=r[i+1].month;H.draw(p);},1300));}
      }else{stop(p,s);if(k==='monthStep'){const r=headRows(s),i=r.findIndex(r=>r.month===s.month);s.month=r[clamp(i+(v==='next'?1:-1),0,r.length-1)].month;}else if(k==='unknown')s.unknown=!s.unknown;else{s[k]=['k','months'].includes(k)?Number(v):v;}}
    }
    return true;
  }
  function input(p,s,e){
    if(!own(p))return false;
    if(e.target.hasAttribute('data-s52-month')){p.querySelector('.s52-month-label').textContent=headRows(s)[+e.target.value].month;return true;}
    if(e.target.hasAttribute('data-s52-search')){
      const q=e.target.value.trim().toLowerCase(),host=p.querySelector('.s52-search-results');s.query=e.target.value;
      const found=q?D.network.nodes.filter(n=>n.id.toLowerCase().includes(q)).sort((a,b)=>b.downstreamCount-a.downstreamCount).slice(0,7):[];
      host.hidden=!q;host.innerHTML=found.length?found.map(n=>btn('searchNode',n.id,n.id)).join(''):'<span>没有匹配模型</span>';return true;
    }
    return false;
  }
  function change(p,s,e){if(!own(p))return false;if(e.target.hasAttribute('data-s52-month')){stop(p,s);s.month=headRows(s)[+e.target.value].month;return true;}if(!e.target.hasAttribute('data-s52-select'))return false;s.focus=e.target.value;s.pin='';return true;}
  function stamp(p,s){return p.dataset.gmChart==='network'?'网络 2026-10-16 非随机样本；增长 2026-09-13快照回溯 · 两者独立':p.dataset.gmChart==='flows'?'报告 2026-09-13 · 基座来源→派生发布 · 双端已识别跨国关系样本':`ModelRank 2024-07—2026-08月表 · 当前${s.month} / Top${s.k} · 版本席位含未知`;}
  const baseHandle=handle;
  function dispatch(p,s,k,v){if(own(p)&&k==='searchNode'){s.node=v;s.view='lineage';s.page=0;s.query='';resetCamera(s);return true;}return baseHandle(p,s,k,v);}
  return{defaults,renderers:{network,flows,head},handle:dispatch,input,change,stamp,own,sliceNetwork,filteredFlows,aggregateFlows};
};
