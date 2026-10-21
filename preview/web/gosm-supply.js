/* GOSD 5.1 — three views: global growth, China–US structure, China geography. */
window.createGOSM51 = function (D, H) {
  "use strict";
  const O = D.supply51;
  const {esc,fmt,compact,txt,line,box,action,svg,btn,seg,chips,note,link,asset,set} = H;
  const names = {models:"模型",datasets:"配套数据集"};
  const PAGE_SIZE = 6;
  const defaults = {
    world:{asset:"models",metric:"count",country:"",organization:"",list:"countries",query:"",page:0,trendMode:"annual",months:12,trendPoint:""},
    cnus:{asset:"models",metric:"downloads",mode:"share",detail:"ranking",selectedCN:"",selectedUS:"",pageCN:0,pageUS:0,query:""},
    china:{asset:"models",metric:"count",province:"",organization:"",list:"provinces",page:0,query:""},
  };
  const own = p => Object.hasOwn(defaults,p.dataset.gmChart);
  const theme = () => H.colors();
  const colors = () => theme().palette;
  const color = code => colors()[code==="US"?1:0];
  const A = s => O.assets[s.asset];
  const key = s => s.metric==="count"?s.asset:s.metric;
  const value = (r,k) => Number(r?.[k]||0);
  const total = (rows,k) => rows.reduce((a,r)=>a+value(r,k),0);
  const pct = (n,d) => d>0?100*n/d:0;
  const country = (s,c) => A(s).countries.find(r=>r.code===c);
  const orgs = c => O.organizationProfiles.filter(r=>!c||r.countryCode===c);
  const countryName = c => O.assets.models.countries.find(r=>r.code===c)?.name_zh||c;
  const label = s => ({count:names[s.asset]+"数",organizations:"发布组织",downloads:"累计下载",likes:"社区关注"})[s.metric];
  const unit = s => s.metric==="downloads"?"次":s.metric==="likes"?"赞":s.metric==="organizations"?"个账号":"个仓库";
  const trim = (s,n=24) => String(s).length>n?String(s).slice(0,n-1)+"…":s;
  const search = (s,placeholder) => `<input type="search" data-s51-search="${s}" aria-label="${placeholder}" placeholder="${placeholder}" autocomplete="off">`;
  const badge = (text="实测 · 2026-10-17读取",sim=false) => `<span class="s51-status${sim?" simulated":""}">${esc(text)}</span>`;
  const assetControls = s => seg("asset",[["models","模型"],["datasets","配套数据集"]],s.asset);
  const selectControl = (s,k,title,items) => `<label class="s51-metric-select">${title} <select data-s51-select="${k}" aria-label="${title}">${items.map(([v,l])=>`<option value="${v}" ${s[k]===v?"selected":""}>${l}</option>`).join("")}</select></label>`;
  function sources(s,extra="") {
    const c=A(s).coverage;
    extra=`<p>本次地域组织样本覆盖全平台仓库数约 ${fmt(c.repositories*100,2)}%，累计下载量约 ${fmt(c.downloads*100,2)}%。</p>`+extra;
    return `<p><b>实测补充快照。</b>2026-10-17读取 OpenGauge。平台总量标注2026-10-16；地理接口未给统一统计日，本图固定本次读取值。地域统计来自826个国家归属已关联的组织账号；配套数据集沿用这批模型发布组织，未覆盖全部数据集发布者。</p><p>下载为累计获取次数；点赞为关注信号。国家指发布组织归属，账号未归并为企业集团。地域接口的月／年增量字段因时间窗口未完整说明，未用于国别比较。</p>${extra}<p>${link("http://47.100.76.186:9529/geography","OpenGauge 地理页")} · ${link(asset("supply-observation.json"),"本图实测数据 JSON")} · ${link(asset("supply-methods.md"),"统计口径与核验")}</p>`;
  }
  function rowsExport(rows,kind,s) {
    return rows.map(r=>({数据类型:"实测",读取日期:"2026-10-17",观察范围:"已识别国家的模型发布组织及其配套数据集",对象类型:kind,...r}));
  }
  function paint(p,s,controls,body,readout,rows,extra="",height=560,sourceText=null) {
    const columns=[...new Set(rows.flatMap(r=>Object.keys(r)))];
    rows=rows.map(r=>Object.fromEntries(columns.map(k=>[k,r[k]??""])));
    set(p,controls,svg(body,1280,height,p.querySelector("h3").textContent),note(readout),rows,sourceText||sources(s,extra));
    const inp=p.querySelector("[data-s51-search]");if(inp)inp.value=s.query||"";
    p.dataset.evidence="observed";
    p.querySelectorAll('[data-gm-action]').forEach(el=>{
      const k=el.dataset.gmAction,v=el.dataset.value;
      if(['asset','metric','list','trendMode','months','trendPoint','detail','mode'].includes(k))el.setAttribute('aria-pressed',(String(s[k])===v&&(k!=='months'||s.trendMode!=='annual'))?'true':'false');
    });
  }
  function heading(x,y,title,subtitle="",w=0) {
    const C=theme().C;
    return txt(x,y,title,22,C.ink,"start",'font-weight="600"')+(subtitle?txt(x,y+28,subtitle,16,C.muted):"")+(w?line(x,y+42,x+w,y+42):"");
  }
  function fitText(text,width,size=17) {
    let out="",used=0;const chars=Array.from(String(text));
    for(let i=0;i<chars.length;i++){
      const c=chars[i],cw=(/[^\u0000-\u00ff]/.test(c)?1:/[MW@%]/.test(c)?.85:.58)*size;
      if(used+cw>width-size)return out+"…";
      out+=c;used+=cw;
    }
    return out;
  }
  function metricCard(x,y,w,v,l,sub="",c=null) {
    const C=theme().C;
    return box(x,y,w,64,C.paper,C.line,8)+txt(x+20,y+23,l,15,C.muted)+txt(x+20,y+51,v,26,c||C.ink,"start",'font-weight="600"')+(sub?txt(x+w-20,y+51,sub,14,C.muted,"end"):"");
  }
  function rankRows(rows,k,x,y,w,selected,act,selectValue,nameValue,start=0,limit=PAGE_SIZE,step=40,accent=null) {
    const C=theme().C,max=Math.max(1,...rows.map(r=>value(r,k))),cc=accent||C.brand;
    return rows.slice(start,start+limit).map((r,i)=>{
      const id=selectValue(r),name=nameValue(r),v=value(r,k),active=selected===id,ry=y+i*step;
      const content=box(x,ry,w,step-3,active?C.raised:C.bg,"none",5)
        +(active?box(x,ry+6,3,step-15,cc,"none",1):"")
        +txt(x+10,ry+20,String(start+i+1).padStart(2,"0"),14,C.muted)
        +txt(x+44,ry+20,fitText(name,w-174,17),17,active?cc:C.ink)
        +txt(x+w-12,ry+20,compact(v),18,C.ink,"end")
        +box(x+44,ry+step-5,Math.max(0,(w-60)*v/max),2,cc,"none",1);
      return `<g data-s51-row="${esc(id)}">${action(act,id,`${name}，${fmt(v)}`,content).replace('class="gm-svg-action"',`class="gm-svg-action" aria-pressed="${active}"`)}</g>`;
    }).join("");
  }
  function geography(s,scope,x,y,scale,selected) {
    const C=theme().C,k=key(s),rows=scope==="world"?A(s).countries:A(s).divisions.filter(r=>r.parent_id===":divisions/CN");
    const by=new Map(rows.map(r=>[r.code,r])),max=Math.max(1,...rows.map(r=>value(r,k)));
    let body="";
    for(const f of O.geometry[scope]) {
      if(f.kind==="line"){body+=`<path d="${f.d}" fill="none" stroke="${C.muted}" stroke-width="1"/>`;continue;}
      const code=scope==="world"?f.id:f.source_code,r=by.get(code),known=r&&r.organizations>0,n=known?value(r,k):null;
      const alpha=n===null?0.06:n===0?0.04:0.12+0.83*Math.log1p(n)/Math.log1p(max);
      let shape=`<path d="${f.d}" fill="${C.brand}" fill-opacity="${alpha}" stroke="${selected===code?C.gold:C.line}" stroke-width="${selected===code?3:0.8}" fill-rule="evenodd"/>`;
      if(f.id==="100000_JD")shape=`<path d="${f.d}" fill="${C.bg}" stroke="${C.line}" stroke-width="1"/>`;
      const info=known?`${f.name}：${fmt(n)} ${unit(s)}`:`${f.name}：暂无已识别组织记录`;
      body+=code?action(scope==="world"?"country":"province",code,info,shape):shape;
    }
    const wanted=scope==="world"?["US","CN","FR","DE","IN","BR"]:["110000","310000","440000","330000","710000"];
    for(const id of wanted){const f=O.geometry[scope].find(r=>r.id===id);if(!f)continue;const [ox,oy]=f.center;const offsets=scope==="china"?{"310000":[38,-15],"330000":[-22,18]}:{"FR":[-12,10],"DE":[10,-10]};const [dx,dy]=offsets[id]||[0,0],cx=ox+dx,cy=oy+dy;const name=f.name.replace(/省|市/g,"");if(dx||dy)body+=line(ox,oy,cx,cy-8,C.muted);body+=`<g pointer-events="none">${box(cx-name.length*(scope==="world"?10:8)-4,cy-19,name.length*(scope==="world"?20:16)+8,25,C.bg,"none",3)}${txt(cx,cy,name,scope==="world"?20:16,C.ink,"middle")}</g>`;}
    return `<g transform="translate(${x},${y}) scale(${scale})">${body}</g>`;
  }
  function selectedFooter(row,s,title,subtitle,org=null) {
    const C=theme().C,base=org?org[s.asset]:row,y=488;
    let b=box(18,y,1244,64,C.paper,C.line,7)+txt(38,y+25,fitText(title,440,20),20,C.ink,"start",'font-weight="600"');
    const hint=org?`${countryName(org.countryCode)} · 所选发布账号`:row?.organizations==null?"暂无已识别记录；不解释为零供给。":`关联发布组织 ${fmt(row.organizations)} 个`;
    b+=txt(38,y+50,hint,14,C.muted)+line(710,y+12,710,y+52,C.line);
    [[names[s.asset]+"数",base?.[s.asset]],["累计下载",base?.downloads],["社区关注",base?.likes]].forEach(([l,v],i)=>{const x=740+i*166;b+=txt(x,y+22,l,13,C.muted)+txt(x,y+50,v==null?"—":compact(v),24,C.ink);});
    if(org)b+=`<a href="https://huggingface.co/${encodeURIComponent(org.name)}" target="_blank" rel="noopener">${txt(680,y+37,"账号原页 ↗",14,C.brand,"end")}</a>`;
    else if(row?.organizations>0)b+=svgButton("list",s.list==="organizations"?"provinces":"organizations",s.list==="organizations"?"返回省级排名 ←":"查看发布组织 →",516,y+18,174,false,false,28);
    return b;
  }
  function worldSelection(row,s,org) {
    const C=theme().C,base=org?org[s.asset]:row||A(s).summary;
    const title=org?org.name:row?row.name_zh:"全球 · 地域组织样本";
    const hint=org?`${countryName(org.countryCode)} · 所选发布账号`:row?row.organizations==null?"暂无已识别组织记录":`关联发布组织 ${fmt(row.organizations)} 个`:"点击地图或右侧排名，查看国家供给。";
    let b=box(834,408,428,144,C.paper,C.line,7)+txt(852,436,fitText(title,390,20),20,C.ink,"start",'font-weight="600"')+txt(852,461,hint,14,C.muted);
    [[names[s.asset]+"数",base?.[s.asset]],["累计下载",base?.downloads],["社区关注",base?.likes]].forEach(([l,v],i)=>{
      const x=852+i*132;b+=txt(x,482,l,13,C.muted)+txt(x,508,v==null?"—":compact(v),22,C.ink);
    });
    if(org)b+=`<a href="https://huggingface.co/${encodeURIComponent(org.name)}" target="_blank" rel="noopener">${txt(1244,541,"账号原页 ↗",14,C.brand,"end")}</a>`;
    else if(row?.organizations>0)b+=svgButton("list",s.list==="organizations"?"countries":"organizations",s.list==="organizations"?"返回国家排名 ←":"查看发布组织 →",1066,518,178,false,false,28);
    else b+=txt(852,541,row?"未覆盖不解释为零供给。":"可继续进入各国发布组织。",13,C.muted);
    return `<g data-s51-selection>${b}</g>`;
  }
  function world(p,s) {
    const C=theme().C,a=A(s),k=key(s),global=O.global[s.asset].summary;
    const selected=country(s,s.country)||(s.country?{code:s.country,name_zh:O.geometry.world.find(r=>r.id===s.country)?.name||s.country}:null),org=O.organizationProfiles.find(r=>r.name===s.organization&&r.countryCode===s.country);
    const organizationMode=s.list==="organizations"&&!!selected;
    let rr=organizationMode?orgs(s.country).map(r=>({...r[s.asset],id:r.name,name:r.name})):a.countries.filter(r=>r.organizations>0).map(r=>({...r,id:r.code,name:r.name_zh}));
    rr=rr.filter(r=>!s.query||`${r.name} ${r.id}`.toLowerCase().includes(s.query.toLowerCase())).sort((a,b)=>value(b,k)-value(a,k)||a.name.localeCompare(b.name));
    const last=Math.max(0,Math.ceil(rr.length/PAGE_SIZE)-1);s.page=Math.min(Math.max(0,s.page),last);
    const controls=seg("asset",[["models","模型"],["datasets","配套数据集"]],s.asset)+`<label class="s51-metric-select">观察指标 <select data-s51-metric-select aria-label="全球地图观察指标">${[["count","数量"],["downloads","累计下载"],["likes","社区关注"]].map(([v,l])=>`<option value="${v}" ${s.metric===v?"selected":""}>${l}</option>`).join("")}</select></label><div class="s51-world-search">${search("world",organizationMode?"搜索所选国家的组织":"搜索国家或地区")}</div>`;
    let body=box(18,6,902,390,C.paper,C.line,6);
    body+=txt(34,29,`全平台公开${s.asset==="datasets"?"数据集":"模型"} ${compact(global.total)} · 地域样本 ${compact(a.summary[s.asset])} · ${fmt(a.summary.organizations)} 个组织`,15,C.muted);
    body+=`<g data-s51-map>${geography(s,"world",74,20,.90,s.country)}</g>`;
    body+=txt(36,381,"对数色阶 · 浅色为样本未覆盖",13,C.muted);
    if(s.country)body+=svgButton("clear","","全球视野",790,40,112,false,false,28);
    body+=txt(944,29,organizationMode?fitText(countryName(s.country)+" · 发布组织",305,21):"国家与地区",21,C.ink,"start",'font-weight="600"');
    body+=txt(944,55,`${label(s)} · ${unit(s)}`,14,C.muted)+line(944,68,1262,68,C.line);
    body+=rankRows(rr,k,940,82,322,organizationMode?s.organization:s.country,organizationMode?"organization":"country",r=>r.id,r=>r.name,s.page*PAGE_SIZE,PAGE_SIZE,44);
    if(!rr.length)body+=txt(1100,202,"没有匹配结果",17,C.muted,"middle")+txt(1100,229,"请调整上方搜索词",14,C.muted,"middle");
    body+=svgButton("page","prev","←",944,359,38,false,s.page===0,28)+txt(1101,380,`${s.page+1} / ${last+1} · ${rr.length} 项`,14,C.muted,"middle")+svgButton("page","next","→",1224,359,38,false,s.page===last,28);
    if(organizationMode)body+=svgButton("list","countries","国家排名 ←",790,78,112,false,false,28);
    body+=worldSelection(selected,s,org);
    const trend=growthPanel(s);body+=trend.body;
    const exported=[...rowsExport(rr.map(r=>({对象:r.name,编码:r.id,[label(s)]:value(r,k)})),organizationMode?"组织":"国家",s),...trend.rows];
    paint(p,s,controls,body,"地域为已识别组织样本，2026-10-17读取；趋势为全平台独立序列。公开可见不等于已核验开源资格。",exported,"",560,sources(s)+H.source(["supply"],"全球月度新增截至2026-07，提供6／12／18个月；年度积累来自2026-09-13仍可见模型的创建时间回溯，包含模型与发布账号。两类序列不与10月总量拼接。"));
  }
  function svgButton(k,v,label,x,y,w,active=false,disabled=false,h=34) {
    const C=theme().C,body=box(x,y,w,h,active?C.raised:C.bg,active?C.brand:C.line,5)+txt(x+w/2,y+h/2+6,label,14,disabled?C.line:active?C.brand:C.ink,"middle");
    return disabled?`<g aria-disabled="true">${body}</g>`:action(k,v,label,body);
  }
  function growthPanel(s) {
    const C=theme().C,annual=s.trendMode==="annual";
    const pairs=annual?[{id:"models",name:"累计模型",rows:D.supply.map(r=>({date:r.date,value:r.models})),color:colors()[0]},{id:"publishers",name:"累计发布账号",rows:D.supply.map(r=>({date:r.date,value:r.publishers})),color:colors()[1]}]:["models","datasets"].map((id,i)=>({id,name:i?"数据集月度新增":"模型月度新增",rows:O.global[id].monthlyNew.slice(-s.months).map(r=>({date:r.month,value:r.count})),color:colors()[i]}));
    if(!pairs[0].rows.some(r=>r.date===s.trendPoint))s.trendPoint=pairs[0].rows.at(-1).date;
    let b=txt(20,430,"全球增长",18,C.ink,"start",'font-weight="600"')+txt(125,430,annual?"2022—2026 · 各年9月13日回溯":"截至2026-07 · 月度新增",13,C.muted);
    [6,12,18].forEach((n,i)=>b+=svgButton("months",n,n+"个月",480+i*80,408,72,!annual&&s.months===n,false,28));
    b+=svgButton("trendMode","annual","年度积累",720,408,96,annual,false,28);
    const exports=[];
    pairs.forEach((se,j)=>{
      const left=18+j*408,px=left+162,py=470,w=212,h=58,rows=se.rows,chosen=rows.find(r=>r.date===s.trendPoint),max=Math.max(1,...rows.map(r=>r.value))*1.12;
      const xx=i=>px+i*w/Math.max(1,rows.length-1),yy=v=>py+h-v*h/max;
      b+=box(left,444,390,108,C.paper,C.line,7)+txt(left+16,468,se.name,15,se.color)+txt(left+16,499,compact(chosen.value),26,C.ink)+txt(left+16,528,chosen.date,13,C.muted);
      if(annual){const at=rows.indexOf(chosen),prev=rows[at-1];if(prev&&prev.value>0)b+=txt(left+16,547,"较上年同日 +"+fmt(100*(chosen.value/prev.value-1),1)+"%",12,C.muted);}
      b+=txt(px-6,py+5,compact(max),11,C.muted,"end")+txt(px-6,py+h+3,"0",11,C.muted,"end");
      b+=line(px,py+h,px+w,py+h,C.line);
      b+=`<path d="${rows.map((r,i)=>(i?'L':'M')+xx(i)+','+yy(r.value)).join(' ')}" fill="none" stroke="${se.color}" stroke-width="2.5"/>`;
      rows.forEach((r,i)=>{const selected=r.date===s.trendPoint;
        if(selected)b+=line(xx(i),py,xx(i),py+h,C.gold,1,'stroke-dasharray="3 4"');
        b+=action("trendPoint",r.date,`${se.name} ${r.date}：${fmt(r.value)}`,`<circle cx="${xx(i)}" cy="${yy(r.value)}" r="${Math.max(5,Math.min(10,w/rows.length/2))}" fill="${C.paper}" fill-opacity="0"/><circle cx="${xx(i)}" cy="${yy(r.value)}" r="${selected?4.5:2.5}" fill="${se.color}" stroke="${C.paper}" stroke-width="1"/>`);
        if(i===0||i===rows.length-1)b+=txt(xx(i),544,annual?r.date.slice(0,4):r.date.slice(2),12,C.muted,i===0?"start":"end");
        exports.push({数据类型:"实测",读取日期:annual?"2026-09-13":"2026-10-17",观察范围:annual?"报告快照的创建时间回溯":"全平台月度新增；截至2026-07",对象类型:"全球趋势",对象:se.name,日期:r.date,数值:r.value,单位:se.id==="publishers"?"账号":"仓库"});
      });
    });
    return {body:b,rows:exports};
  }
  function cnus(p,s) {
    const C=theme().C,a=A(s),cn=country(s,"CN"),us=country(s,"US"),k=key(s);
    const metrics=[["activeProviders","有资产的发布账号","账号",null],[s.asset,s.asset==="models"?"模型仓库":"配套数据集","仓库","count"],["downloads","累计下载","次","downloads"],["likes","社区关注","赞","likes"]];
    let b="",exports=[];
    metrics.forEach(([field,title,u,selector],i)=>{
      const x=18+i*316,den=a.summary[field],cv=value(cn,field),uv=value(us,field),max=s.mode==="share"?100:Math.max(cv,uv,1),active=s.metric===selector;
      let card=box(x,4,296,120,active?C.raised:C.paper,active?C.brand:C.line,8)+txt(x+18,29,title,17,C.ink,"start",'font-weight="600"');
      if(active)card+=`<circle cx="${x+276}" cy="23" r="4" fill="${C.brand}"/>`;
      [["中国",cv,color("CN")],["美国",uv,color("US")]].forEach(([name,v,c],j)=>{
        const left=x+16+j*142,vv=s.mode==="share"?pct(v,den):v;
        card+=`<g><title>${esc(name)}：${fmt(v)} ${u}；样本份额 ${fmt(pct(v,den),2)}%</title>${txt(left,59,name,13,c)}${txt(left+122,59,s.mode==="share"?fmt(vv,2)+"%":compact(v),21,c,"end")}${box(left,70,122,4,C.line,"none",2)}${box(left,70,122*vv/max,4,c,"none",2)}</g>`;
      });
      card+=line(x+16,90,x+280,90,C.line)+txt(x+16,108,s.mode==="share"?`样本分母 ${compact(den)} ${u}`:`已识别组织样本 · 单位：${u}`,13,C.muted);
      b+=`<g data-s51-metric="${field}">${selector?action("metric",selector,`按${title}比较发布者；样本分母 ${fmt(den)} ${u}`,card):card}</g>`;
      exports.push({数据类型:"实测",读取日期:"2026-10-17",观察范围:"已识别组织样本",对象类型:"中美指标",指标:title,中国:cv,美国:uv,样本总量:den,中国样本份额_pct:pct(cv,den),美国样本份额_pct:pct(uv,den)});
    });
    b+=line(640,145,640,552,C.line);
    ["CN","US"].forEach((code,i)=>{
      const x=22+i*640,cc=color(code),all=orgs(code).map(o=>({...o[s.asset],name:o.name,url:o.url,allAssets:o})).sort((a,b)=>value(b,k)-value(a,k)||a.name.localeCompare(b.name)),sum=total(all,k);
      const rows=s.detail==="ranking"?all.filter(o=>!s.query||o.name.toLowerCase().includes(s.query.toLowerCase())):all;
      const pageKey="page"+code,last=Math.max(0,Math.ceil(rows.length/PAGE_SIZE)-1);s[pageKey]=Math.min(Math.max(0,s[pageKey]),last);
      const chosen=rows.find(o=>o.name===s["selected"+code])||rows[s[pageKey]*PAGE_SIZE];
      b+=txt(x,165,countryName(code),25,cc,"start",'font-weight="600"')+txt(x+80,165,`${all.length} 个关联账号`,15,C.muted);
      b+=txt(x+302,165,`前三 ${fmt(pct(total(all.slice(0,3),k),sum),1)}%`,18,cc)+txt(x+450,165,`前十 ${fmt(pct(total(all.slice(0,10),k),sum),1)}%`,18,cc)+txt(x,194,`本国组织样本 · ${label(s)} / ${unit(s)}`,14,C.muted);
      if(s.detail==="ranking"){
        b+=svgButton(pageKey,"prev","←",x+420,180,40,false,s[pageKey]===0,28)+txt(x+505,200,`${s[pageKey]+1} / ${last+1}`,14,C.muted,"middle")+svgButton(pageKey,"next","→",x+554,180,40,false,s[pageKey]===last,28);
        b+=rankRows(rows,k,x,222,594,chosen?.name,"select"+code,r=>r.name,r=>r.name,s[pageKey]*PAGE_SIZE,PAGE_SIZE,44,cc);
        if(!rows.length)b+=txt(x+297,348,"没有匹配账号，请调整搜索词",17,C.muted,"middle");
      }else{
        const px=x+48,py=246,w=520,h=224;
        b+=txt(x+48,229,"累计份额 · 账号按指标从高到低排列",14,C.muted);
        for(let t=0;t<=4;t++){const y=py+h-h*t/4;b+=line(px,y,px+w,y)+txt(px-8,y+5,t*25+"%",14,C.muted,"end");}
        b+=`<path d="M${px},${py+h} L${px+w},${py}" fill="none" stroke="${C.line}" stroke-dasharray="4 5"/>`+concentrationCurve(all,k,px,py,w,h,cc)+txt(px,490,"0",14,C.muted)+txt(px+w,490,"100% 发布账号",14,C.muted,"end");
      }
      b+=box(x,506,594,46,C.paper,C.line,7);
      if(chosen){
        const info=`${chosen.name}；${label(s)} ${fmt(value(chosen,k))}；占本国 ${fmt(pct(value(chosen,k),sum),2)}%；模型 ${fmt(chosen.allAssets.models.models)}；配套数据集 ${fmt(chosen.allAssets.datasets.datasets)}`;
        b+=`<g role="img" aria-label="${esc(info)}"><title>${esc(info)}</title>${txt(x+16,535,fitText(chosen.name,310,18),18,cc)}${txt(x+346,535,`本国 ${fmt(pct(value(chosen,k),sum),1)}%`,14,C.muted)}</g><a href="${esc(chosen.url)}" target="_blank" rel="noopener">${txt(x+576,535,"账号 ↗",14,cc,"end")}</a>`;
      }else b+=txt(x+18,535,"暂无所选发布者",16,C.muted);
      exports.push(...rows.map(r=>({数据类型:"实测",读取日期:"2026-10-17",观察范围:"本国全部关联账号；配套数据沿用同一组织名录",对象类型:"发布账号",国家:countryName(code),账号:r.name,排名:all.indexOf(r)+1,指标:label(s),数值:value(r,k),本国份额_pct:pct(value(r,k),sum)})));
    });
    const controls=assetControls(s)+selectControl(s,"mode","对照",[["share","样本内份额"],["count","绝对量"]])+selectControl(s,"detail","主体",[["ranking","发布者排行"],["concentration","头部集中度"]])+(s.detail==="ranking"?`<div class="s51-world-search">${search("cnus","搜索中美发布账号")}</div>`:"");
    paint(p,s,controls,b,"上方份额以整个地域样本为分母；下方排行与集中度以本国对应资产为分母。搜索不改变分母，账号未归并为企业集团。"+(s.detail==="concentration"?"虚线为等量参考，曲线越早接近100%越集中。":""),exports,"",560);
  }
  function concentrationCurve(rows,k,x,y,w,h,c) {
    const sum=total(rows,k);let acc=0;
    let path=`M${x},${y+h}`;
    rows.forEach((r,i)=>{acc+=value(r,k);path+=` L${(x+w*(i+1)/Math.max(1,rows.length)).toFixed(2)},${(y+h-h*acc/(sum||1)).toFixed(2)}`;});
    return `<path d="${path}" fill="none" stroke="${c}" stroke-width="3.5"/>`;
  }
  function china(p,s) {
    const C=theme().C,k=key(s),cn=country(s,"CN"),divs=A(s).divisions.filter(r=>r.parent_id===":divisions/CN"&&r.organizations>0);
    const unknown={code:"unassigned",name_zh:"省级归属待补",...cn.unassignedDivision};
    let selected=s.province==="unassigned"?unknown:divs.find(r=>r.code===s.province);
    if(!selected&&s.province){const f=O.geometry.china.find(r=>r.source_code===s.province);selected={code:s.province,name_zh:f?.name||s.province};}
    const filteredOrgs=orgs("CN").filter(r=>!s.province||(s.province==="unassigned"?r.divisionCodes.length===0:r.divisionCodes.includes(s.province)));
    const org=filteredOrgs.find(r=>r.name===s.organization);
    let rows=s.list==="organizations"?filteredOrgs.map(r=>({...r[s.asset],organizations:1,id:r.name,name:r.name})):[...divs,unknown].map(r=>({...r,id:r.code,name:r.name_zh}));
    rows=rows.filter(r=>!s.query||`${r.name} ${r.id}`.toLowerCase().includes(s.query.toLowerCase())).sort((a,b)=>value(b,k)-value(a,k)||a.name.localeCompare(b.name));
    const last=Math.max(0,Math.ceil(rows.length/PAGE_SIZE)-1);s.page=Math.min(Math.max(0,s.page),last);
    const metricItems=[...(s.list==="organizations"?[]:[["organizations","发布组织"]]),["count","数量"],["downloads","累计下载"],["likes","社区关注"]];
    const controls=assetControls(s)+selectControl(s,"metric","观察指标",metricItems)+`<div class="s51-world-search">${search("china",s.list==="organizations"?"搜索当前地区的组织":"搜索省级地区")}</div>`;
    let b=box(18,6,902,468,C.paper,C.line,6)+txt(34,29,`中国已识别组织 ${fmt(cn.organizations)} · ${names[s.asset]} ${compact(cn[s.asset])} · 省级归属待补 ${compact(cn.unassignedDivision[s.asset])}`,15,C.muted);
    b+=`<g data-s51-map>${geography(s,"china",21,24,1.02,s.province)}</g>`+txt(36,458,"对数色阶 · 未覆盖不代表零 · 含台湾省及南海诸岛",13,C.muted);
    if(s.province||s.organization||s.list==="organizations")b+=svgButton("clear","","全国视野",790,40,112,false,false,28);
    if(s.list==="organizations")b+=svgButton("list","provinces","省级排名 ←",790,78,112,false,false,28);
    b+=txt(944,29,s.list==="organizations"?fitText((selected?selected.name_zh:"中国")+" · 组织",305,21):"省级地区",21,C.ink,"start",'font-weight="600"')+txt(944,55,`${label(s)} · ${unit(s)}`,14,C.muted)+line(944,68,1262,68,C.line);
    b+=rankRows(rows,k,940,84,322,s.list==="organizations"?s.organization:s.province,s.list==="organizations"?"organization":"province",r=>r.id,r=>r.name,s.page*PAGE_SIZE,PAGE_SIZE,52);
    if(!rows.length)b+=txt(1100,228,"没有匹配结果",17,C.muted,"middle")+txt(1100,255,"请调整上方搜索词",14,C.muted,"middle");
    b+=svgButton("page","prev","←",944,440,38,false,s.page===0,28)+txt(1101,461,`${s.page+1} / ${last+1} · ${rows.length} 项`,14,C.muted,"middle")+svgButton("page","next","→",1224,440,38,false,s.page===last,28);
    b+=selectedFooter(selected||cn,s,org?org.name:selected?selected.name_zh:"中国 · 全国",org?`${selected?.name_zh||"中国"} · 所选发布账号`:selected?"切换“发布组织”，查看当前地区的具体供给者。":"点击省级地区，再进入发布组织；也可直接查看全国组织榜。",org);
    paint(p,s,controls,b,"省级归属待补保留在全国总量中。地图未覆盖地区留白，不以估算分配全国余量。切换资产保持地区选择。",rowsExport(rows.map(r=>({对象:r.name,编码:r.id,[label(s)]:value(r,k)})),s.list==="organizations"?"中国组织":"中国省级",s));
  }
  const renderers={world,cnus,china};
  function handle(p,s,k,v) {
    if(!own(p))return false;
    if(k==="table-page"){s.tablePage=Math.max(0,(s.tablePage||0)+(v==="next"?1:-1));return true;}
    s.tablePage=0;
    if(k==="clear"){Object.assign(s,{country:"",province:"",organization:"",query:"",page:0,list:p.dataset.gmChart==="china"?"provinces":"countries"});}
    else if(k==="pageCN"||k==="pageUS"){s[k]=Math.max(0,s[k]+(v==="next"?1:-1));s["selected"+k.slice(4)]="";}
    else if(k==="page")s.page=Math.max(0,s.page+(v==="next"?1:-1));
    else if(k==="country"&&p.dataset.gmChart==="world"){s.country=v;s.organization="";s.page=0;s.query="";}
    else if(k==="province"){s.province=v;s.organization="";s.page=0;s.query="";}
    else if(k==="list"){s.list=v;s.query="";s.page=0;if(v==="organizations"&&s.metric==="organizations")s.metric="count";}
    else if(k==="months"){s.months=Number(v);s.trendMode="monthly";}
    else if(k==="organization")s.organization=v;
    else if(k==="selectCN")s.selectedCN=v;
    else if(k==="selectUS")s.selectedUS=v;
    else {s[k]=k==="months"?Number(v):v;if(["asset","metric","mode","list","country"].includes(k)){s.page=0;s.pageCN=0;s.pageUS=0;if(["metric","asset"].includes(k)){s.selectedCN="";s.selectedUS="";}}}
    if(p.dataset.gmChart==="world"&&s.list==="organizations"&&!s.country)s.list="countries";
    return true;
  }
  function change(p,s,e) {
    if(!own(p))return false;
    const k=e.target.dataset.s51Select||(e.target.hasAttribute("data-s51-metric-select")?"metric":null);
    return ["metric","mode","detail"].includes(k)?handle(p,s,k,e.target.value):false;
  }
  function input(p,s,e) {
    if(!own(p)||!e.target.hasAttribute("data-s51-search"))return false;
    s.query=e.target.value;s.page=0;s.pageCN=0;s.pageUS=0;s.tablePage=0;return true;
  }
  function stamp(p,s) {
    if(p.dataset.gmChart==="world")return "OpenGauge 2026-10-17地域读取 · 趋势："+(s.trendMode==="annual"?"2026-09-13年度回溯":"截至2026-07月表，"+s.months+"个月")+" · 两者独立";
    return "OpenGauge · 2026-10-17读取 · 已识别组织及其配套数据 · 地理统计日未注明";
  }
  return {defaults,renderers,handle,input,change,stamp,own};
};
