/* 5.2: two-dimensional lineage galaxy, directed flows, and ModelRank structure. */
window.createGOSM52 = function(D,H) {
  'use strict';
  const {esc,fmt,compact,txt,line,box,action,svg,btn,seg,note,link,asset,set}=H;
  const d3=window.d3,theme=()=>H.colors().C,palette=()=>H.colors().palette;
  const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
  const trim=(s,n=25)=>String(s).length>n?String(s).slice(0,n-1)+'…':String(s);
  const sum=(a,k)=>a.reduce((n,r)=>n+Number(r[k]||0),0);
  const totalFlows=sum(D.flows,'weight'),names=new Map(D.geography.map(r=>[r.id,r.name]));names.set('OTH','其他国家');
  const nm=c=>names.get(c)||c;
  const countryOrder=[...new Set(D.flows.flatMap(r=>[r.source,r.target]))].sort((a,b)=>sum(D.flows.filter(r=>r.source===b||r.target===b),'weight')-sum(D.flows.filter(r=>r.source===a||r.target===a),'weight'));
  const col=c=>c==='CN'?palette()[0]:c==='US'?palette()[1]:c==='OTH'?theme().unknown:palette()[(countryOrder.indexOf(c)+2)%palette().length];
  const byId=new Map(D.network.nodes.map(n=>[n.id,n])),parents=new Map(),children=new Map();
  D.network.edges.forEach(e=>{if(!parents.has(e.target))parents.set(e.target,[]);parents.get(e.target).push(e.source);if(!children.has(e.source))children.set(e.source,[]);children.get(e.source).push(e.target);});
  const months=[...new Set(D.head.map(r=>r.month))];
  const defaults={network:{view:'overview',node:'',neighbors:'down',page:0,query:'',year:'2026-09-13',zoom:1,panX:0,panY:0,focused:false,task:''},flows:{focus:'all',direction:'both',group:8,pin:'',country:'CN'},head:{k:100,months:26,month:months.at(-1),mode:'count',bands:'cumulative',unknown:true,playing:false}};
  const own=p=>Object.hasOwn(defaults,p.dataset.gmChart);
  const sb=(k,v,label,x,y,w,active=false,disabled=false)=>{const C=theme(),b=box(x,y,w,28,active?C.raised:C.bg,active?C.brand:C.line,4)+txt(x+w/2,y+19,label,14,disabled?C.unknown:active?C.brand:C.ink,'middle');return disabled?`<g aria-disabled="true">${b}</g>`:action(k,v,label,b);};
  const select=(key,options,value,label)=>`<label class="s52-select-label">${label}<select data-s52-select="${key}" aria-label="${label}">${options.map(([v,l])=>`<option value="${v}" ${String(v)===String(value)?'selected':''}>${esc(l)}</option>`).join('')}</select></label>`;
  function paint(p,s,controls,b,readout,rows,source,height=560){const keys=[...new Set(rows.flatMap(r=>Object.keys(r)))];set(p,controls,svg(b,1280,height,p.querySelector('h3').textContent),note(readout),rows.map(r=>Object.fromEntries(keys.map(k=>[k,r[k]??'']))),source);p.dataset.evidence='observed';p.s52State=s;const paper=p.querySelector('.s52-print-view');if(paper)paper.innerHTML=publication(p,s);}
  function source(keys,explanation){return H.source(keys,explanation)+`<p>${link(asset('influence-methods.md'),'5.2图表口径与交互说明')}</p>`;}
  const TASKS=[['language','语言生成','#79d8df'],['multimodal','多模态','#c1a1f0'],['vision','图像与视频','#a5cd85'],['speech','语音','#e6b875'],['other','其他任务','#819edb'],['unknown','任务未标注','#a2adb8']];
  function task(n){const t=n.task||'';return t==='unspecified-model'||!t?'unknown':t==='text-generation'?'language':['image-text-to-text','any-to-any'].includes(t)?'multimodal':/image|video|depth/.test(t)?'vision':/speech|audio/.test(t)?'speech':'other';}
  const taskColor=n=>TASKS.find(t=>t[0]===task(n))[2];
  const positions=new Map(D.network.nodes.map(n=>[n.id,{x:480+n.x*430,y:222+n.y*210,cluster:task(n)}]));
  const hubs=D.network.bases.map(r=>byId.get(r.id));
  const hubIds=new Set(hubs.map(n=>n.id));
  function related(s){const ids=new Set(s.node?[s.node]:[]);if(s.node){(parents.get(s.node)||[]).forEach(n=>ids.add(n));(children.get(s.node)||[]).forEach(n=>ids.add(n));}return ids;}
  function sliceNetwork(s){return{nodes:D.network.nodes,edges:D.network.edges,positions,related:related(s)};}
  const camera=s=>`translate(${480+s.panX} ${222+s.panY}) scale(${s.zoom}) translate(-480 -222)`;
  function focusCamera(s){const ids=[...related(s)],pts=ids.map(id=>positions.get(id));if(!pts.length)return;const xs=pts.map(q=>q.x),ys=pts.map(q=>q.y),left=Math.min(...xs),right=Math.max(...xs),top=Math.min(...ys),bottom=Math.max(...ys);s.zoom=clamp(Math.min(800/Math.max(150,right-left),310/Math.max(90,bottom-top)),.8,5);s.panX=(480-(left+right)/2)*s.zoom;s.panY=(222-(top+bottom)/2)*s.zoom;}
  function galaxy(s,slice){
    const bg='#071b29',ink='#d8e6ee',muted='#91a9b8',sel=related(s),active=n=>s.node?sel.has(n.id):s.task?task(n)===s.task:true;
    let b=box(18,4,928,434,bg,'#28485a',7)+txt(34,28,`模型派生网络 · ${fmt(slice.nodes.length)} 模型 / ${fmt(slice.edges.length)} 条声明关系`,14,muted)+txt(930,28,'2026-10-16',13,muted,'end');
    b+=`<defs><clipPath id="s52-graph-clip"><rect x="24" y="35" width="916" height="365" rx="4"/></clipPath><marker id="s52-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#f3c97a"/></marker></defs>`;
    let clouds=`<ellipse cx="480" cy="222" rx="432" ry="194" fill="none" pointer-events="none" stroke="#294352" stroke-opacity=".45"/><ellipse cx="480" cy="222" rx="316" ry="144" fill="none" pointer-events="none" stroke="#294352" stroke-opacity=".25" stroke-dasharray="2 8"/>`;
    const paths=new Map();for(const e of slice.edges){const a=positions.get(e.source),z=positions.get(e.target),key=task(byId.get(e.source));paths.set(key,(paths.get(key)||'')+`M${a.x.toFixed(1)},${a.y.toFixed(1)}L${z.x.toFixed(1)},${z.y.toFixed(1)}`);}
    for(const [key,d] of paths)clouds+=`<path d="${d}" fill="none" pointer-events="none" stroke="${TASKS.find(t=>t[0]===key)[2]}" stroke-width=".55" stroke-opacity="${s.node?.08:s.task?.09:.19}"/>`;
    if(s.node)for(const e of slice.edges.filter(e=>e.source===s.node||e.target===s.node)){const a=positions.get(e.source),z=positions.get(e.target);clouds+=`<path d="M${a.x},${a.y}L${z.x},${z.y}" fill="none" pointer-events="none" stroke="${e.source===s.node?'#79d8df':'#f3c97a'}" stroke-width="1.1" stroke-opacity=".8" marker-end="url(#s52-arrow)"><title>${esc(e.source+' → '+e.target)}</title></path>`;}
    for(const n of slice.nodes){const q=positions.get(n.id),isOn=n.id===s.node,r=isOn?6.5:Math.min(5.8,.85+Math.sqrt(n.downstreamCount)*.32),color=isOn?'#f3c97a':taskColor(n),opacity=active(n)?'.94':s.focused?'.035':'.16';
      if(hubIds.has(n.id)&&active(n))clouds+=`<circle cx="${q.x}" cy="${q.y}" r="${r+5}" fill="${color}" opacity=".10"/>`;
      clouds+=`<g role="button" tabindex="${hubIds.has(n.id)||isOn?'0':'-1'}" class="s52-node gm-svg-action" data-gm-action="node" data-value="${esc(n.id)}" opacity="${opacity}" aria-label="${esc(n.id)}"><circle cx="${q.x}" cy="${q.y}" r="${r}" fill="${color}" ${isOn?'stroke="#fff0c9" stroke-width="1"':''}/><title>${esc(n.id)} · 上游 ${n.upstreamCount} / 下游 ${n.downstreamCount}</title></g>`;
    }
    const labels=s.focused&&s.node?[byId.get(s.node)]:hubs;
    for(const side of [-1,1]){const ns=labels.filter(n=>(positions.get(n.id).x<480?-1:1)===side).sort((a,b)=>positions.get(a.id).y-positions.get(b.id).y);ns.forEach((n,i)=>{const q=positions.get(n.id),y=62+(i+.5)*310/Math.max(1,ns.length),tx=side<0?35:928,anchor=side<0?'start':'end',end=side<0?197:762,color=n.id===s.node?'#f3c97a':ink;clouds+=line(q.x,q.y,end,y-5,'#567185',.65,'stroke-dasharray="2 4"')+action('node',n.id,n.id,txt(tx,y,trim(n.name,23),13,color,anchor,`paint-order="stroke" stroke="${bg}" stroke-width="4" stroke-linejoin="round"`));});}
    b+=`<g clip-path="url(#s52-graph-clip)"><rect data-s52-pan="true" x="24" y="35" width="916" height="365" fill="${bg}"/><g data-s52-camera transform="${camera(s)}">${clouds}</g></g>`;
    b+=txt(35,421,'拖动平移 · 滚轮缩放 · 点击模型查看关系',13,muted);
    for(const [key,v,label,x,w] of [['zoom','out','−',758,32],['zoom','in','＋',796,32],['reset','','全景复位',835,94]])b+=action(key,v,label,box(x,402,w,26,'#102b3c','#365367',4)+txt(x+w/2,420,label,13,ink,'middle'));
    return b;
  }
  function networkSide(s){
    const C=theme(),x=970,r=1258;let b='';
    if(!s.node){
      b+=txt(x,30,'从一个基座开始探索',22,C.ink)+txt(x,56,'点选名称，查看上下游',14,C.muted)+txt(r-8,56,'下游',13,C.muted,'end');
      hubs.slice(0,6).forEach((n,i)=>{const y=79+i*43;b+=action('node',n.id,n.id,box(x-2,y-17,294,39,C.paper,'none',4)+txt(x+9,y,trim(n.name,23),16,C.ink)+txt(x+9,y+16,n.publisher,12,C.muted)+txt(r-7,y+5,fmt(n.downstreamCount),16,C.brand,'end'));});
      b+=txt(x,352,'任务着色 · 点选高亮',13,C.muted);
      TASKS.forEach(([k,l,c],i)=>{const xx=x+(i%2)*148,yy=377+Math.floor(i/2)*24;b+=action('task',k,'高亮'+l,`<circle cx="${xx+5}" cy="${yy-5}" r="4" fill="${c}"/>`+txt(xx+17,yy,l,13,s.task===k?C.brand:C.muted));});
    }else{
      const n=byId.get(s.node);b+=txt(x,29,trim(n.publisher,31),16,C.brand)+txt(x,58,trim(n.name,25),21,C.ink)+txt(x,87,'直接上游 '+n.upstreamCount,16,palette()[1])+txt(x+148,87,'直接下游 '+n.downstreamCount,16,palette()[0]);
      b+=sb('focusNode','',s.focused?'显示全网':'聚焦关联',x,102,102,s.focused)+sb('clearNode','','返回全景',x+114,102,102);
      b+=sb('neighbors','up','看上游',x,146,136,s.neighbors==='up')+sb('neighbors','down','看下游',x+148,146,136,s.neighbors==='down');
      const rows=((s.neighbors==='up'?parents:children).get(n.id)||[]).slice().sort((a,b)=>byId.get(b).downstreamCount-byId.get(a).downstreamCount||a.localeCompare(b)),last=Math.max(0,Math.ceil(rows.length/5)-1);s.page=clamp(s.page,0,last);
      rows.slice(s.page*5,s.page*5+5).forEach((id,i)=>{const m=byId.get(id),y=204+i*35;b+=action('node',id,id,box(x-2,y-20,294,31,C.paper,'none',3)+txt(x+8,y,trim(m.name,29),14,C.ink));});
      if(!rows.length)b+=txt(x+8,218,'样本中没有记录此方向的邻居',14,C.muted);
      b+=sb('neighborPage','prev','←',x,374,36,false,s.page===0)+txt(x+140,394,`${s.page+1} / ${last+1} · ${rows.length} 个`,13,C.muted,'middle')+sb('neighborPage','next','→',r-38,374,36,false,s.page===last);
      b+=`<a href="${esc(n.url)}" target="_blank" rel="noopener">${txt(x,430,'查看模型卡 ↗',14,C.brand)}</a>`+txt(r-4,430,'箭头：基座 → 派生',13,C.muted,'end');
    }return b;
  }
  function concept(){
    const C=theme();let b=box(18,4,1244,434,C.paper,C.line,7)+txt(42,43,'从已有能力出发，继续创造',26,C.ink)+txt(42,73,'一个派生模型可以有多个上游，也可以成为后续开发的新基座。',17,C.muted);
    const blocks=[[65,146,230,'基座 A','已有模型能力',palette()[0]],[65,285,230,'基座 B','另一上游来源',palette()[1]],[472,205,286,'派生模型','微调 · 量化 · 适配 · 合并',palette()[2]],[965,205,230,'后续派生','再一次复用与创新',palette()[0]]];
    blocks.forEach(([x,y,w,t,d,c])=>b+=box(x,y,w,88,C.bg,C.line,8)+txt(x+w/2,y+36,t,25,c,'middle')+txt(x+w/2,y+64,d,16,C.muted,'middle'));
    for(const d of ['M295 190C383 190 382 234 470 234','M295 329C383 329 382 264 470 264','M758 249H963'])b+=`<path d="${d}" fill="none" stroke="${C.brand}" stroke-width="2.5" marker-end="url(#s52-concept-arrow)"/>`;
    b+=`<defs><marker id="s52-concept-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="${C.brand}"/></marker></defs>`;
    return b+txt(42,412,'关系示意 · 网络连线只使用模型卡明确声明的基座关系，未逐条划分开发类型。',15,C.muted);
  }
  function growth(s){
    const C=theme(),rows=D.derivation,selected=rows.find(r=>r.date===s.year)||rows.at(-1),prev=rows[rows.indexOf(selected)-1];let b='';
    [['derived_models','可见派生模型 / 万',palette()[0],false],['derived_pct','派生模型占比 / %',palette()[1],true]].forEach(([key,title,color,pct],j)=>{
      const x=18+j*632,px=x+250,py=475,w=330,h=104,mx=pct?35:100,xx=i=>px+i*w/4,val=r=>pct?r[key]:r[key]/1e4,yy=v=>py+h-v/mx*h;
      b+=box(x,450,612,171,C.paper,C.line,6)+txt(x+16,477,title,16,C.muted)+txt(x+16,513,pct?fmt(selected[key],2)+'%':fmt(selected[key]/1e4,2)+'万',25,color)+txt(x+16,545,s.year.slice(0,4)+(prev?(pct?' · 较上年 '+fmt(selected[key]-prev[key],2)+' 个百分点':' · 较上年 +'+fmt((selected[key]/prev[key]-1)*100,1)+'%'):''),14,C.muted);
      b+=txt(x+16,605,'各年均为 9 月 13 日',14,C.muted);
      [0,mx/2,mx].forEach(v=>b+=line(px,yy(v),px+w,yy(v),C.line,.6)+txt(px-8,yy(v)+4,fmt(v,Number.isInteger(v)?0:1),13,C.muted,'end'));
      b+=`<path d="${rows.map((r,i)=>(i?'L':'M')+xx(i)+','+yy(val(r))).join(' ')}" fill="none" stroke="${color}" stroke-width="2.4"/>`;
      rows.forEach((r,i)=>b+=action('year',r.date,`${r.date} ${title} ${r[key]}`,`<circle cx="${xx(i)}" cy="${yy(val(r))}" r="10" fill="${C.paper}" fill-opacity="0"/><circle cx="${xx(i)}" cy="${yy(val(r))}" r="${r.date===s.year?4.5:3}" fill="${color}"/>`)+txt(xx(i),yy(val(r))-10,fmt(val(r),2),14,color,'middle')+txt(xx(i),605,r.date.slice(0,4),14,C.muted,'middle'));
    });return b;
  }
  function network(p,s){
    const slice=sliceNetwork(s),controls=seg('view',[['concept','读懂派生'],['overview','网络全景']],s.view)+(s.view==='overview'?`<div class="s52-search"><input type="search" data-s52-search="network" placeholder="搜索模型或发布账号" aria-label="搜索模型或发布账号" autocomplete="off"><div class="s52-search-results" hidden></div></div>`:'<span class="s52-caption">从基座到派生，再成为新的起点</span>');
    const b=(s.view==='concept'?concept():galaxy(s,slice)+networkSide(s))+growth(s);
    const rows=[...(s.view==='concept'?[]:slice.edges).map(e=>({记录类型:'声明关系样本',日期:'2026-10-16',基座:e.source,派生:e.target,关系类型:'模型卡声明'})),...D.derivation.map(r=>({记录类型:'全平台累计回溯',日期:r.date,模型总数:r.models,派生模型数:r.derived_models,派生占比_pct:r.derived_pct}))];
    paint(p,s,controls,b,'网络：2026-10-16非随机声明样本；增长：2026-09-13可见快照回溯。两套数据独立。',rows,source(['derivation'],`网络取自 ${link(D.network.meta.sourceFile,'参考项目固定快照')}；上游 ${link(D.network.meta.upstreamDataset,'hub-stats')}。默认全景显示5,777模型、5,111条明确声明的基座关系，来自前12,000模型的非随机输入样本。参考图还包括数据集、Space与推断关系，本图不将这些连接当作派生。保留参考坐标布局；坐标、距离只用于导航，颜色表示任务类别，节点大小为样本内直接下游数，不表示ModelRank。点选仅高亮或聚焦直接上下游，不改变完整样本和导出计数。模型卡声明不等于训练过程经过独立核验。网络没有完整历史日期，底部年份不生成网络回放。`)+`<p>${link(asset('network.json'),'网络JSON')} · ${link(asset('lineage-live-provenance.json'),'固定来源与抽取记录')}</p>`,630);
    p.s52Slice=slice;p.gmNetworkSlice=slice;if(s.view==='overview')bindPan(p,p.querySelector('.gm-svg'),s);
  }
  function bindPan(p,sv,s){let drag;const coords=e=>{const r=sv.getBoundingClientRect(),scale=Math.min(r.width/1280,r.height/630)||1;return{x:(e.clientX-r.left-(r.width-1280*scale)/2)/scale,y:(e.clientY-r.top-(r.height-630*scale)/2)/scale};};
    const update=()=>sv.querySelector('[data-s52-camera]')?.setAttribute('transform',camera(s));
    sv.addEventListener('pointerdown',e=>{if(e.button!==0||!e.target.hasAttribute('data-s52-pan'))return;const q=coords(e);drag={x:q.x,y:q.y,px:s.panX,py:s.panY};sv.setPointerCapture?.(e.pointerId);});
    sv.addEventListener('pointermove',e=>{if(!drag)return;const q=coords(e);s.panX=drag.px+q.x-drag.x;s.panY=drag.py+q.y-drag.y;update();});
    for(const type of ['pointerup','pointercancel'])sv.addEventListener(type,()=>drag=null);
    sv.addEventListener('wheel',e=>{const q=coords(e);if(q.x<24||q.x>940||q.y<35||q.y>400)return;e.preventDefault();const z=clamp(s.zoom*Math.exp(-e.deltaY*.0015),.6,8),f=z/s.zoom;s.panX=q.x-480-(q.x-480-s.panX)*f;s.panY=q.y-222-(q.y-222-s.panY)*f;s.zoom=z;update();},{passive:false});
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
    const C=theme(),left=145,right=480,bar=10,top=85,h=352,pad=10,total=sum(edges,'weight');
    const ids=k=>[...new Set(edges.map(r=>r[k]))].sort((a,b)=>a==='OTH'?1:b==='OTH'?-1:sum(edges.filter(r=>r[k]===b),'weight')-sum(edges.filter(r=>r[k]===a),'weight'));
    const src=ids('source'),dst=ids('target'),ky=Math.min((h-pad*(src.length-1))/(total||1),(h-pad*(dst.length-1))/(total||1));
    const layout=(ids,k)=>{let y=top;return new Map(ids.map(c=>{const value=sum(edges.filter(r=>r[k]===c),'weight'),q={y,h:value*ky,cursor:0,value};y+=q.h+pad;return[c,q];}));};
    const a=layout(src,'source'),b=layout(dst,'target');let out=txt(132,66,'基座来源国',15,C.muted,'middle')+txt(509,66,'派生发布国',15,C.muted,'middle');
    edges.forEach(e=>{const s=a.get(e.source),t=b.get(e.target),dy=e.weight*ky,sy=s.y+s.cursor+dy/2,ty=t.y+t.cursor+dy/2;s.cursor+=dy;t.cursor+=dy;
      out+=flowAction('flowPair',e.source+'|'+e.target,edgeDesc(e),`<path d="M${left+bar},${sy} C280,${sy} 378,${ty} ${right},${ty}" fill="none" stroke="${col(e.source)}" stroke-width="${Math.max(.2,dy)}"/>`,`data-s52-edge="${e.source}|${e.target}" opacity=".58"`);
    });
    const nodes=(ids,lay,x,isLeft)=>{
      const ys=[];let last=68;for(const c of ids){const q=lay.get(c);last=Math.max(last+24,q.y+q.h/2);ys.push(last);}
      if(ys.at(-1)>447){ys[ys.length-1]=447;for(let i=ys.length-2;i>=0;i--)ys[i]=Math.min(ys[i],ys[i+1]-24);}
      ids.forEach((c,i)=>{const q=lay.get(c),y=ys[i];out+=flowAction('flowNode',c,nm(c)+'：'+fmt(q.value)+' 对',box(x,q.y,bar,Math.max(.6,q.h),col(c),'none',0)+line(isLeft?x:x+bar,q.y+q.h/2,isLeft?x-7:x+bar+7,y,col(c),.8)+txt(isLeft?x-9:x+bar+9,y+5,trim(nm(c),4)+' '+fmt(q.value),14,C.ink,isLeft?'end':'start'),`data-s52-country="${c}"`);});
    };nodes(src,a,left,true);nodes(dst,b,right,false);return out;
  }
  function chord(edges,ids){
    const C=theme(),cx=836,cy=251,r=128,idx=new Map(ids.map((id,i)=>[id,i])),matrix=ids.map(()=>ids.map(()=>0));edges.forEach(e=>matrix[idx.get(e.source)][idx.get(e.target)]+=e.weight);
    const chords=d3.chordDirected().padAngle(.034).sortSubgroups(d3.descending)(matrix),arc=d3.arc().innerRadius(r+4).outerRadius(r+14),ribbon=d3.ribbonArrow().radius(r).padAngle(.002).headRadius(8);let b=txt(cx,66,'有向弦图 · 箭头指向派生发布国',14,C.muted,'middle');
    chords.forEach(ch=>{const a=ids[ch.source.index],z=ids[ch.target.index],e=edges.find(e=>e.source===a&&e.target===z);b+=flowAction('flowPair',a+'|'+z,edgeDesc(e),`<path d="${ribbon(ch)}" fill="${col(a)}"/>`,`data-s52-edge="${a}|${z}" opacity=".58" transform="translate(${cx} ${cy})"`);});
    // Label slots avoid overlap even when the smaller arcs cluster together.
    const groups=chords.groups.map(g=>{const a=(g.startAngle+g.endAngle)/2-Math.PI/2;return{g,c:ids[g.index],ax:cx+Math.cos(a)*(r+15),ay:cy+Math.sin(a)*(r+15),side:Math.cos(a)>=0?1:-1,y:cy+Math.sin(a)*165};});
    for(const side of [-1,1]){const gs=groups.filter(q=>q.side===side).sort((a,b)=>a.y-b.y);let y=80;for(const q of gs){q.y=Math.max(q.y,y);y=q.y+23;}if(gs.at(-1)?.y>441){gs.at(-1).y=441;for(let i=gs.length-2;i>=0;i--)gs[i].y=Math.min(gs[i].y,gs[i+1].y-23);}}
    groups.forEach(q=>{const tx=cx+q.side*166;b+=flowAction('flowNode',q.c,nm(q.c),`<path d="${arc(q.g)}" fill="${col(q.c)}" transform="translate(${cx} ${cy})"/>`+line(q.ax,q.ay,tx,q.y,col(q.c),.7)+txt(tx+q.side*3,q.y+4,q.c==='OTH'?'其他':trim(nm(q.c),3),13,C.ink,q.side>0?'start':'end'),`data-s52-country="${q.c}"`);});
    b+=txt(cx,461,'外弧合计两端连接；颜色表示基座来源',13,C.muted,'middle');return b;
  }
  function flowDetail(s,rows,agg){
    const C=theme(),x=1074,right=1248;let b=box(1060,42,202,432,C.paper,C.line,7),edge=agg.edges.find(e=>e.source+'|'+e.target===s.pin);
    if(s.pin.startsWith('node:')){
      const code=s.pin.slice(5),ins=rows.filter(r=>r.target===code),outs=rows.filter(r=>r.source===code);b+=txt(x,70,'所选国家 · 当前筛选',13,C.muted)+txt(x,107,trim(nm(code),8),22,col(code));
      if(code==='OTH')return b+txt(x,154,'合并显示的其他国家',16,C.ink)+txt(x,183,'请用顶部选择器',15,C.muted)+txt(x,210,'单独探索其中一国。',15,C.muted)+sb('flowClear','','清除高亮',x,429,174);
      b+=txt(x,150,'基座输出',14,C.muted)+txt(right,177,fmt(sum(outs,'weight')),27,C.ink,'end')+txt(x,210,'派生接收',14,C.muted)+txt(right,237,fmt(sum(ins,'weight')),27,C.ink,'end')+line(x,253,right,253,C.line)+txt(x,278,'主要伙伴 · 双向关系',13,C.muted);
      const partners=new Map();[...ins,...outs].forEach(e=>{const c=e.source===code?e.target:e.source;partners.set(c,(partners.get(c)||0)+e.weight);});[...partners].sort((a,b)=>b[1]-a[1]).slice(0,4).forEach(([c,n],i)=>b+=action('focus',c,'聚焦'+nm(c),txt(x,308+i*28,trim(nm(c),4),15,col(c))+txt(right,308+i*28,fmt(n),16,C.ink,'end')));
    }else{
      edge=edge||agg.edges[0];if(!edge)return b+txt(x,85,'暂无匹配关系',19,C.muted);
      const title=nm(edge.source)+' → '+nm(edge.target);b+=txt(x,70,s.pin?'所选流向':'当前最大流向',13,C.muted)+txt(x,108,trim(title,12),title.length>9?15:21,C.ink)+txt(x,154,fmt(edge.weight),34,col(edge.source))+txt(x,181,'对基座—派生关系',14,C.muted)+line(x,207,right,207,C.line);
      b+=txt(x,237,'占全部跨国样本',14,C.muted)+txt(right,271,fmt(edge.weight/totalFlows*100,1)+'%',27,C.ink,'end')+txt(x,311,'占当前筛选',14,C.muted)+txt(right,345,fmt(edge.weight/(sum(rows,'weight')||1)*100,1)+'%',27,C.ink,'end');
      b+=txt(x,385,edge.members.length>1?`合并 ${edge.members.length} 条流向`:'悬停联动 · 点击固定',13,C.muted);
    }
    b+=sb('flowClear','','清除高亮',x,429,174);return b;
  }
  function flows(p,s){
    const C=theme(),rows=filteredFlows(s),agg=aggregateFlows(rows,s),count=sum(rows,'weight');
    const controls=seg('focus',[['all','全球'],['CN','中国'],['US','美国'],['compare','中美']],s.focus)+select('direction',[['both','双向连接'],['out','基座输出'],['in','派生接收']],s.direction,'方向')+select('focus',[['all','选择国家'],...countryOrder.map(c=>[c,nm(c)])],s.focus,'国家')+`<details class="s52-options"><summary>显示 ▾</summary><div>${seg('group',[[6,'前6国'],[8,'前8国'],[10,'前10国']],s.group,'图面国家数')}<p>其余国家合并展示，关系数完整保留。</p></div></details>`;
    let b=txt(22,24,`${fmt(count)} 对关系 · ${new Set(rows.map(r=>r.source)).size} 个基座来源国 → ${new Set(rows.map(r=>r.target)).size} 个派生发布国`,16,C.ink)+txt(1259,24,`占完整跨国样本 ${fmt(count/totalFlows*100,1)}% · 2026-09-13`,14,C.muted,'end');
    b+=box(18,42,596,432,C.bg,C.line,7)+box(630,42,414,432,C.bg,C.line,7)+sankey(agg.edges)+chord(agg.edges,agg.ids)+flowDetail(s,rows,agg);
    for(const [code,i] of [['CN',0],['US',1]]){const x=18+i*632,out=sum(D.flows.filter(e=>e.source===code),'weight'),input=sum(D.flows.filter(e=>e.target===code),'weight'),other=code==='CN'?'US':'CN',bilateral=D.flows.find(e=>e.source===code&&e.target===other).weight;
      let q=box(x,486,612,66,C.paper,C.line,6)+txt(x+15,513,nm(code),21,col(code));[['输出',out],['接收',input],[code==='CN'?'对美':'对华',bilateral]].forEach(([l,v],j)=>{const xx=x+116+j*162;q+=txt(xx,513,l,14,C.muted)+txt(xx+42,514,fmt(v),22,j===2?col(code):C.ink);});q+=txt(x+15,539,'完整跨国样本 · 单位：关系对 · 点击聚焦',12,C.muted);b+=action('focus',code,'聚焦'+nm(code),q);
    }
    paint(p,s,controls,b,'基座来源→派生发布，单位为关系对。仅含双端国家可识别的跨国样本；底部中美读数采用完整样本。',rows.map(r=>({数据类型:'报告观测',日期:'2026-09-13',基座来源国家:r.source,派生发布国家:r.target,关系对数:r.weight,全部跨国样本份额_pct:r.weight/totalFlows*100,当前筛选份额_pct:r.weight/(count||1)*100})),source(['flows'],'原报告186条有向国家流向，共10,943对跨国关系。修订稿明确source为基座来源，target为派生发布；中国输出5,888、美国接收7,513、中国→美国4,639均与原表交叉核对。完整约89.22万对派生关系中，双端国家可识别约2.59%（含境内），本图为其中跨国子集。国家按发布主体归属，不是使用者位置。按当前入出量保留前6/8/10国，其他国家合并但不丢失计数；其他→其他仍是实际不同国家的跨国关系。弦图外弧计量两端连接，不表示独立模型数。CSV保留每条原始方向和两个分母。'));
    p.s52FlowRows=rows;p.s52Aggregated=agg;bindFlowHover(p,s);
  }
  function highlightFlow(p,key){
    p.querySelectorAll('[data-s52-edge]').forEach(g=>{const pair=g.dataset.s52Edge,match=!key||(key.startsWith('node:')?pair.split('|').includes(key.slice(5)):pair===key);g.setAttribute('opacity',!key?'.58':match?'.95':'.08');});
    p.querySelectorAll('[data-s52-country]').forEach(g=>{const c=g.dataset.s52Country,match=!key||(key.startsWith('node:')?c===key.slice(5):key.split('|').includes(c));g.setAttribute('opacity',match?'1':'.25');});
  }
  function bindFlowHover(p,s){highlightFlow(p,s.pin);for(const type of ['pointerover','focusin'])p.querySelector('.gm-view svg').addEventListener(type,e=>{const el=e.target.closest?.('[data-s52-edge],[data-s52-country]');if(el)highlightFlow(p,el.dataset.s52Edge||'node:'+el.dataset.s52Country);});for(const type of ['pointerout','focusout'])p.querySelector('.gm-view svg').addEventListener(type,()=>highlightFlow(p,s.pin));}
  function headRows(s){return D.head.filter(r=>r.k===s.k).slice(-s.months);}
  function head(p,s){
    const C=theme(),rows=headRows(s);if(!rows.some(r=>r.month===s.month))s.month=rows.at(-1).month;
    const chosen=rows.find(r=>r.month===s.month),start=rows[0],delta=chosen.us-chosen.china,idx=rows.indexOf(chosen);
    const controls=seg('k',[[20,'Top 20'],[100,'Top 100'],[1000,'Top 1000']],s.k)+select('months',[[6,'近6个月'],[12,'近12个月'],[18,'近18个月'],[26,'全部26个月']],s.months,'时间窗')+`<div class="s52-timeline"><input type="range" min="0" max="${rows.length-1}" step="1" value="${idx}" data-s52-month aria-label="选择ModelRank月份"><strong class="s52-month-label">${s.month}</strong>${btn('play','',s.playing?'暂停':'播放',s.playing)}</div>`;
    let b=txt(22,24,`${s.month} · Top ${s.k}　中国 ${chosen.china} 席　美国 ${chosen.us} 席`,17,C.ink)+txt(1258,24,`中美差距 ${Math.abs(delta)} 席${delta===0?'':delta>0?' · 美国较多':' · 中国较多'}`,15,C.muted,'end');
    b+=box(18,42,594,432,C.bg,C.line,7)+box(628,42,634,432,C.bg,C.line,7);
    b+=txt(35,74,'三档榜单结构',22,C.ink)+sb('bands','cumulative','累计榜单',338,55,112,s.bands==='cumulative')+sb('bands','segments','分段观察',458,55,112,s.bands==='segments');
    const keys=['china','us','other_known','unknown'],labels=['中国','美国','其他已识别','归属未知'],cs=[palette()[0],palette()[1],palette()[3],C.unknown];
    [20,100,1000].forEach((k,i)=>{const r=D.head.find(r=>r.k===k&&r.month===s.month),prev=i?D.head.find(r=>r.k===[20,100][i-1]&&r.month===s.month):null,segment=s.bands==='segments',den=segment?k-(prev?.k||0):k,y=128+i*104;
      const values=keys.map(key=>r[key]-(segment?(prev?.[key]||0):0));b+=action('k',k,'选择Top '+k,box(28,y-21,574,89,s.k===k?C.paper:C.bg,s.k===k?C.line:'none',5));
      b+=txt(40,y,segment?(i===0?'第1—20名':i===1?'第21—100名':'第101—1000名'):'Top '+k,18,C.ink)+txt(588,y,segment?`${den}个版本席位`:`已识别 ${fmt(r.coverage_pct,1)}%`,14,C.muted,'end');
      let x=40;values.forEach((v,j)=>{const w=v/den*546;b+=action('k',k,`${segment?'分段':'Top '+k} · ${labels[j]} ${v} 席`,box(x,y+16,w,36,cs[j],'none',0)+(w>34?txt(x+w/2,y+40,String(v),16,j===3?C.bg:'#fff','middle','font-weight="600"'):''));x+=w;});
    });
    labels.forEach((l,i)=>{const x=37+i*140;b+=box(x,435,9,9,cs[i],'none',1)+txt(x+15,444,l,13,C.muted);});
    b+=txt(647,74,`Top ${s.k} · 月度变化`,22,C.ink)+sb('mode','count','席位',1100,55,64,s.mode==='count')+sb('mode','share','占比',1172,55,72,s.mode==='share');
    b+=txt(649,103,`${rows[0].month}—${rows.at(-1).month}`,13,C.muted)+action('unknown','','显示或隐藏未知归属曲线',txt(1244,103,(s.unknown?'✓ ':'')+'未知归属',13,C.muted,'end'));
    const px=681,py=126,w=529,h=280,visible=s.unknown?['china','us','unknown']:['china','us'],mx=s.mode==='share'?Math.min(100,Math.ceil(Math.max(...rows.flatMap(r=>visible.map(k=>r[k]/s.k*100)))/10)*10+10):Math.ceil(Math.max(1,...rows.flatMap(r=>visible.map(k=>r[k])))*1.12/10)*10;
    const xx=i=>px+i*w/(rows.length-1),val=(r,k)=>s.mode==='share'?r[k]/s.k*100:r[k],yy=v=>py+h-v/mx*h;
    for(let t=0;t<=4;t++){const v=mx*t/4,y=yy(v);b+=line(px,y,px+w,y,C.line)+txt(px-9,y+4,fmt(v,0)+(s.mode==='share'?'%':''),13,C.muted,'end');}
    visible.forEach(key=>{const c=key==='china'?palette()[0]:key==='us'?palette()[1]:C.unknown;b+=`<path d="${rows.map((r,i)=>(i?'L':'M')+xx(i)+','+yy(val(r,key))).join(' ')}" fill="none" stroke="${c}" stroke-width="${key==='unknown'?2:2.7}" ${key==='unknown'?'stroke-dasharray="4 4"':''}/>`;rows.forEach((r,i)=>b+=`<circle cx="${xx(i)}" cy="${yy(val(r,key))}" r="${r.month===s.month?5:2.5}" fill="${c}"/>`);});
    b+=line(xx(idx),py-5,xx(idx),py+h,C.gold,1,'stroke-dasharray="4 4"');
    rows.forEach((r,i)=>{const step=w/(rows.length-1),tx=xx(i);b+=action('month',r.month,`${r.month} 中国 ${r.china} 美国 ${r.us} 未知 ${r.unknown}`,`<rect x="${Math.max(px,tx-step/2)}" y="${py-9}" width="${i===0||i===rows.length-1?step/2:step}" height="${h+18}" fill="${C.bg}" fill-opacity="0"/>`);if(i===0||i===rows.length-1||i%Math.ceil(rows.length/5)===0&&rows.length-1-i>=Math.ceil(rows.length/5))b+=txt(tx,431,r.month.slice(2),13,C.muted,'middle');});
    b+=txt(649,459,'点选月份，联动榜单结构',13,C.muted)+txt(1244,459,s.unknown?'虚线：归属未知':'未知始终计入分母',13,C.muted,'end');
    b+=box(18,487,1244,65,C.paper,C.line,6)+txt(34,511,`${start.month} → ${s.month}`,14,C.muted)+txt(34,538,`Top ${s.k} · 窗口变化`,13,C.muted);
    [['中国',start.china,chosen.china,palette()[0]],['美国',start.us,chosen.us,palette()[1]],['中美差距',Math.abs(start.us-start.china),Math.abs(delta),C.ink],['未知',start.unknown,chosen.unknown,C.unknown]].forEach(([l,a,z,c],i)=>{const x=252+i*248;b+=txt(x,510,l,13,C.muted)+txt(x,538,`${a} → ${z}`,23,c);});
    paint(p,s,controls,b,'按模型版本计席位，未知归属保留在分母；累计榜单相互包含，分段按同月相减。',D.head.filter(r=>rows.some(q=>q.month===r.month)).map(r=>({数据类型:'ModelRank原报告月表',月份:r.month,榜单深度:r.k,中国:r.china,美国:r.us,其他已识别:r.other_known,未知归属:r.unknown,中国份额_pct:r.china_pct,美国份额_pct:r.us_pct,国家识别覆盖_pct:r.coverage_pct})),source(['head'],'原表覆盖2024-07至2026-08，共26个月、78行TopK汇总。三档榜单各自以20/100/1000为分母，保留未知归属。分段为同月嵌套榜单相减，不跨月份减去不同集合。底部从当前窗口起点比较所选月；窗口变化时起点随之变化。席位数不是ModelRank分数份额或测试性能。不从聚合值生成具体模型名单；具体模型见第三章M-Ranking。'));
  }
  // One static projection serves SVG export, browser print and the private PDF.
  function publication(p,s){
    const original=p.querySelector('.gm-view svg');if(!original)return '';
    const el=original.cloneNode(true),kind=p.dataset.gmChart,C=theme();
    const removeActions=new Set(['zoom','reset','focusNode','clearNode','neighbors','neighborPage','flowClear','bands','mode','unknown']);
    el.querySelectorAll('[data-gm-action]').forEach(n=>{if(removeActions.has(n.dataset.gmAction))n.remove();else{n.removeAttribute('tabindex');n.removeAttribute('role');n.removeAttribute('class');n.removeAttribute('data-gm-action');n.removeAttribute('data-value');}});
    el.querySelectorAll('text').forEach(n=>{
      if(/拖动平移|点选名称|悬停联动|请用顶部选择器|单独探索其中一国|查看模型卡|点选月份/.test(n.textContent)){n.remove();return;}
      n.textContent=n.textContent.replace('从一个基座开始探索','代表基座与直接下游').replace('任务着色 · 点选高亮','任务类别').replace(' · 点击聚焦','').replace('点选高亮','');
      n.setAttribute('font-size',clamp(Number(n.getAttribute('font-size')||14),14,19));
      n.removeAttribute('paint-order');n.removeAttribute('stroke');n.removeAttribute('stroke-width');
    });
    el.querySelectorAll('title,circle[opacity=".10"]').forEach(n=>n.remove());
    const vb=el.getAttribute('viewBox').split(' ').map(Number),height=vb[3],width=vb[2];
    const notes=kind==='network'?['网络：2026-10-16，非随机样本；颜色为任务，节点大小为样本内直接下游数。','增长：2026-09-13 仍可见模型回溯，与网络样本独立；布局和距离无指标含义。']:kind==='flows'?['2026-09-13 · 基座来源→派生发布 · 单位：关系对；图面数值为当前筛选。','仅双端国家可识别的跨国样本；两图使用同一关系集合，底部中美读数使用完整样本。']:['ModelRank 月表 · 按模型版本计席位，归属未知始终保留在分母中。','三档累计榜单相互包含；席位数不等于模型家族数、分数份额或测试性能。'];
    if(kind==='head'){
      const r=k=>D.head.find(r=>r.month===s.month&&r.k===k),v=k=>['china','us','other_known','unknown'].map(key=>r(k)[key]).join(' / ');
      notes.push(`${s.month} · 中国 / 美国 / 其他已识别 / 归属未知：Top20 为 ${v(20)}；Top100 为 ${v(100)}；Top1000 为 ${v(1000)}。`);
    }
    const footerHeight=49+notes.length*23;
    const footer=document.createElementNS('http://www.w3.org/2000/svg','g');
    footer.innerHTML=box(0,height,width,footerHeight,C.bg,'none',0)+txt(width/2,height+28,p.querySelector('h3').textContent,17,C.ink,'middle')+notes.map((n,i)=>txt(18,height+55+i*23,n,14,C.muted)).join('');el.append(footer);
    el.setAttribute('viewBox',`0 0 ${width} ${height+footerHeight}`);el.setAttribute('width',width);el.setAttribute('height',height+footerHeight);el.removeAttribute('class');
    el.querySelectorAll('[id]').forEach(n=>{const id=n.id,newid='s52-paper-'+id;el.querySelectorAll('*').forEach(q=>{for(const a of [...q.attributes])if(a.value.includes('url(#'+id+')'))q.setAttribute(a.name,a.value.replaceAll('url(#'+id+')','url(#'+newid+')'));});n.id=newid;});
    return new XMLSerializer().serializeToString(el);
  }
  function resetCamera(s){s.zoom=1;s.panX=0;s.panY=0;}
  const timers=new Map();
  function stop(p,s){if(timers.has(p)){clearInterval(timers.get(p));timers.delete(p);}s.playing=false;}
  function handle(p,s,k,v){
    if(!own(p))return false;
    if(k==='table-page'){s.tablePage=Math.max(0,(s.tablePage||0)+(v==='next'?1:-1));return true;}
    s.tablePage=0;
    if(p.dataset.gmChart==='network'){
      if(k==='node'){if(byId.has(v)){s.node=v;s.page=0;s.task='';if(s.focused)focusCamera(s);}}
      else if(k==='neighborPage')s.page=Math.max(0,s.page+(v==='next'?1:-1));
      else if(k==='zoom')s.zoom=clamp(s.zoom*(v==='in'?1.3:1/1.3),.6,8);
      else if(k==='reset'||k==='clearNode'){resetCamera(s);s.node='';s.task='';s.focused=false;s.page=0;}
      else if(k==='focusNode'){s.focused=!s.focused;if(s.focused)focusCamera(s);else resetCamera(s);}
      else if(k==='view'){s.view=v;resetCamera(s);}
      else if(k==='neighbors'){s.neighbors=v;s.page=0;}
      else if(k==='task'){s.task=s.task===v?'':v;s.node='';s.focused=false;resetCamera(s);}
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
  function change(p,s,e){
    if(!own(p))return false;
    if(e.target.hasAttribute('data-s52-month')){stop(p,s);s.month=headRows(s)[+e.target.value].month;return true;}
    const key=e.target.dataset.s52Select;if(!key)return false;
    if(p.dataset.gmChart==='head')stop(p,s);
    s[key]=['months','group'].includes(key)?Number(e.target.value):e.target.value;s.pin='';s.tablePage=0;return true;
  }
  function stamp(p,s){return p.dataset.gmChart==='network'?'网络 2026-10-16 非随机样本；增长 2026-09-13快照回溯 · 两者独立':p.dataset.gmChart==='flows'?'报告 2026-09-13 · 基座来源→派生发布 · 双端已识别跨国关系样本':`ModelRank 2024-07—2026-08月表 · 当前${s.month} / Top${s.k} · 版本席位含未知`;}
  const baseHandle=handle;
  function dispatch(p,s,k,v){if(own(p)&&k==='searchNode'){s.node=v;s.view='overview';s.page=0;s.query='';s.focused=true;s.task='';focusCamera(s);return true;}return baseHandle(p,s,k,v);}
  return{defaults,publication,renderers:{network,flows,head},handle:dispatch,input,change,stamp,own,sliceNetwork,filteredFlows,aggregateFlows};
};
