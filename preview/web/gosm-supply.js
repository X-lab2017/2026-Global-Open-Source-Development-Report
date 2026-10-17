/* GOSD 5.1 — three views: global growth, China–US structure, China geography. */
window.createGOSM51 = function (D, H) {
  "use strict";
  const O = D.supply51;
  const {esc,fmt,compact,txt,line,box,action,svg,btn,seg,chips,note,link,asset,set} = H;
  const names = {models:"模型",datasets:"配套数据集"};
  const CN = "中国", US = "美国";
  const defaults = {
    world:{asset:"models",metric:"count",country:"",organization:"",list:"countries",query:"",page:0,trendMode:"monthly",months:12,trendPoint:""},
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
  const assetControls = s => seg("asset",[["models","模型"],["datasets","配套数据集"]],s.asset,"资产");
  const metricControls = (s,organization=false) => seg("metric",[...(organization?[["organizations","发布组织"]]:[]),["count","数量"],["downloads","累计下载"],["likes","社区关注"]],s.metric,"观察");
  function pageControls(s,length,size=10) {
    const last=Math.max(0,Math.ceil(length/size)-1);s.page=Math.min(Math.max(0,s.page),last);
    return `<div class="gm-control-group">${btn("page","prev","←",false,s.page===0?'disabled aria-label="上一页"':'aria-label="上一页"')}<span>${s.page+1} / ${last+1} · ${length} 项</span>${btn("page","next","→",false,s.page===last?'disabled aria-label="下一页"':'aria-label="下一页"')}</div>`;
  }
  function sources(s,extra="") {
    return `<p><b>实测补充快照。</b>2026-10-17读取 OpenGauge。平台总量标注2026-10-16；地理接口未给统一统计日，本图固定本次读取值。地域统计来自826个国家归属已关联的组织账号；配套数据集沿用这批模型发布组织，未覆盖全部数据集发布者。</p><p>下载为累计获取次数；点赞为关注信号。国家指发布组织归属，账号未归并为企业集团。地域接口的月／年增量字段因时间窗口未完整说明，未用于国别比较。</p>${extra}<p>${link("http://47.100.76.186:9529/geography","OpenGauge 地理页")} · ${link(asset("supply-observation.json"),"本图实测数据 JSON")} · ${link(asset("supply-methods.md"),"统计口径与核验")}</p>`;
  }
  function rowsExport(rows,kind,s) {
    return rows.map(r=>({数据类型:"实测",读取日期:"2026-10-17",观察范围:"已识别国家的模型发布组织及其配套数据集",对象类型:kind,...r}));
  }
  function paint(p,s,controls,body,readout,rows,extra="",height=650,sourceText=null) {
    const columns=[...new Set(rows.flatMap(r=>Object.keys(r)))];
    rows=rows.map(r=>Object.fromEntries(columns.map(k=>[k,r[k]??""])));
    set(p,controls,svg(body,1280,height,p.querySelector("h3").textContent),note(readout),rows,sourceText||sources(s,extra));
    const inp=p.querySelector("[data-s51-search]");if(inp)inp.value=s.query||"";
    p.dataset.evidence="observed";
  }
  function heading(x,y,title,subtitle="",w=0) {
    const C=theme().C;
    return txt(x,y,title,22,C.ink,"start",'font-weight="600"')+(subtitle?txt(x,y+28,subtitle,16,C.muted):"")+(w?line(x,y+42,x+w,y+42):"");
  }
  function metricCard(x,y,w,v,l,sub="",c=null) {
    const C=theme().C;
    return box(x,y,w,88,C.paper)+txt(x+17,y+25,l,16,C.muted)+txt(x+17,y+60,v,30,c||C.ink,"start",'font-weight="600"')+(sub?txt(x+w-14,y+61,sub,15,C.muted,"end"):"");
  }
  function rankRows(rows,k,x,y,w,selected,act,selectValue,nameValue,start=0,limit=10) {
    const C=theme().C,max=Math.max(1,...rows.map(r=>value(r,k)));
    return rows.slice(start,start+limit).map((r,i)=>{
      const id=selectValue(r),name=nameValue(r),v=value(r,k),active=selected===id,ry=y+i*35;
      return action(act,id,`${name}，${fmt(v)}`,box(x,ry,w,32,active?C.raised:C.bg,"none",4)+txt(x+6,ry+21,String(start+i+1).padStart(2,"0"),15,C.muted)+txt(x+36,ry+21,trim(name,w>400?26:19),17,active?C.brand:C.ink)+txt(x+w-8,ry+21,compact(v),17,C.ink,"end")+box(x+36,ry+29,Math.max(0,(w-50)*v/max),2,C.brand,"none",0));
    }).join("");
  }
  function coverage(s,x,y,w) {
    const C=theme().C,c=A(s).coverage,share=s.metric==="downloads"?c.downloads:s.metric==="count"?c.repositories:null;
    if(share==null)return txt(x,y,"地域比较使用已识别组织样本；完整范围见图内来源。",16,C.muted);
    return txt(x,y,`本次快照约覆盖全平台${s.metric==="downloads"?"下载量":"仓库数"}的 ${fmt(share*100,2)}%`,16,C.muted)+box(x,y+12,w,8,C.line,"none",3)+box(x,y+12,w*share,8,C.brand,"none",3)+txt(x,y+44,"■ 已识别组织样本",15,C.brand)+txt(x+w,y+44,"其余：个人、未关联组织及未覆盖资产",15,C.muted,"end");
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
    for(const id of wanted){const f=O.geometry[scope].find(r=>r.id===id);if(!f)continue;const [ox,oy]=f.center;const offsets=scope==="china"?{"310000":[38,-15],"330000":[-22,18]}:{};const [dx,dy]=offsets[id]||[0,0],cx=ox+dx,cy=oy+dy;const name=f.name.replace(/省|市/g,"");if(dx||dy)body+=line(ox,oy,cx,cy-8,C.muted);body+=`<g pointer-events="none">${box(cx-name.length*8-4,cy-19,name.length*16+8,25,C.bg,"none",3)}${txt(cx,cy,name,16,C.ink,"middle")}</g>`;}
    return `<g transform="translate(${x},${y}) scale(${scale})">${body}</g>`;
  }
  function selectedFooter(row,s,title,subtitle,org=null) {
    const C=theme().C,k=key(s),base=org?org[s.asset]:row;
    let b=box(18,526,1244,108,C.paper)+txt(36,554,title,21,C.ink,"start",'font-weight="600"')+txt(36,582,trim(subtitle,42),16,C.muted);
    [[names[s.asset]+"数",base?.[s.asset]],["累计下载",base?.downloads],["社区关注",base?.likes]].forEach(([l,v],i)=>{const x=645+i*205;b+=txt(x,553,l,15,C.muted)+txt(x,585,v==null?"—":compact(v),25,C.ink);});
    if(org)b+=`<a href="https://huggingface.co/${encodeURIComponent(org.name)}" target="_blank" rel="noopener">${txt(36,613,"查看发布账号 ↗",16,C.brand)}</a>`;
    else b+=txt(36,613,row?(row.organizations==null?"暂无已识别组织记录；不解释为零供给。":`关联发布组织 ${fmt(row.organizations)} 个 · ${label(s)} ${fmt(value(row,k))} ${unit(s)}`):"点击地图或排名，查看国家与发布组织。",16,C.muted);
    return b;
  }
  function world(p,s) {
    const C=theme().C,a=A(s),k=key(s),global=O.global[s.asset].summary;
    const selected=country(s,s.country)||(s.country?{code:s.country,name_zh:O.geometry.world.find(r=>r.id===s.country)?.name||s.country}:null),org=O.organizationProfiles.find(r=>r.name===s.organization&&r.countryCode===s.country);
    const organizationMode=s.list==="organizations"&&!!selected;
    let rr=organizationMode?orgs(s.country).map(r=>({...r[s.asset],id:r.name,name:r.name})):a.countries.filter(r=>r.organizations>0).map(r=>({...r,id:r.code,name:r.name_zh}));
    rr=rr.filter(r=>!s.query||`${r.name} ${r.id}`.toLowerCase().includes(s.query.toLowerCase())).sort((a,b)=>value(b,k)-value(a,k)||a.name.localeCompare(b.name));
    let controls=assetControls(s)+metricControls(s)+btn("clear","","清除选择")+badge();
    controls+=`<div class="s51-control-line">${seg("list",[["countries","国家排名"],["organizations","所选国家组织"]],organizationMode?"organizations":"countries","右侧列表")}${search("world","搜索国家或组织")}${pageControls(s,rr.length)}</div>`;
    let body=metricCard(18,4,390,compact(global.total),`全平台公开${s.asset==="datasets"?"数据集":"模型"}`,"仓库")+metricCard(426,4,390,compact(a.summary[s.asset]),"地域组织样本","仓库")+metricCard(834,4,428,fmt(a.summary.organizations),"已识别国家的发布组织","账号");
    body+=geography(s,"world",0,107,.91,s.country)+txt(25,492,"地图色阶：log(1＋所选指标) · 浅色为样本未覆盖",15,C.muted);
    body+=heading(850,126,organizationMode?`${countryName(s.country)} · 发布组织`:"国家与地区",`${label(s)} · ${unit(s)} · 点击查看`,390);
    body+=rankRows(rr,k,844,176,418,organizationMode?s.organization:s.country,organizationMode?"organization":"country",r=>r.id,r=>r.name,s.page*10);
    body+=selectedFooter(selected,s,org?org.name:selected?selected.name_zh:"全球供给，保持完整视野",org?`${countryName(s.country)} · 所选发布账号`:selected?"在上方切换“所选国家组织”，继续查看供给者。":"模型与配套数据分别观察；地图默认不选国家。",org);
    body+=coverage(s,28,662,1224);
    const trend=growthPanel(s);body+=trend.body;
    const exported=[...rowsExport(rr.map(r=>({对象:r.name,编码:r.id,[label(s)]:value(r,k)})),organizationMode?"组织":"国家",s),...trend.rows];
    paint(p,s,controls,body,"上方为当前组织地域快照，下方为全平台增长序列。国家选择不改变全球趋势；月度新增与年度积累各自标注时间。点击趋势点可查当期数值。",exported,"",1090,sources(s)+H.source(["supply"],"全球月度新增截至2026-07，提供6／12／18个月；年度积累来自2026-09-13仍可见模型的创建时间回溯，包含模型与发布账号。两类序列不与10月总量拼接。"));
  }
  function svgButton(k,v,label,x,y,w,active=false,disabled=false) {
    const C=theme().C,body=box(x,y,w,30,active?C.raised:C.bg,active?C.brand:C.line,5)+txt(x+w/2,y+20,label,14,disabled?C.line:active?C.brand:C.ink,"middle");
    return disabled?`<g aria-disabled="true">${body}</g>`:action(k,v,label,body);
  }
  function growthPanel(s) {
    const C=theme().C,annual=s.trendMode==="annual";
    const pairs=annual?[{id:"models",name:"累计模型",rows:D.supply.map(r=>({date:r.date,value:r.models})),color:colors()[0]},{id:"publishers",name:"累计发布账号",rows:D.supply.map(r=>({date:r.date,value:r.publishers})),color:colors()[1]}]:["models","datasets"].map((id,i)=>({id,name:i?"数据集月度新增":"模型月度新增",rows:O.global[id].monthlyNew.slice(-s.months).map(r=>({date:r.month,value:r.count})),color:colors()[i]}));
    if(!pairs[0].rows.some(r=>r.date===s.trendPoint))s.trendPoint=pairs[0].rows.at(-1).date;
    let b=box(18,736,1244,340,C.paper,C.line,8)+txt(38,766,"全球增长",21,C.ink,"start",'font-weight="600"');
    b+=svgButton("trendMode","monthly","月度新增",185,745,114,!annual)+svgButton("trendMode","annual","年度积累",311,745,114,annual);
    if(!annual)[6,12,18].forEach((n,i)=>b+=svgButton("months",n,n+"个月",990+i*80,745,70,s.months===n));
    b+=txt(38,798,annual?"2022—2026年9月13日 · 同一快照回溯，非逐年独立存档":"截至2026-07的全平台月表 · 与上方当前地域快照分别观察",15,C.muted);
    const exports=[];
    pairs.forEach((se,j)=>{
      const left=38+j*625,px=left+64,py=883,w=505,h=137,rows=se.rows,chosen=rows.find(r=>r.date===s.trendPoint),max=Math.max(1,...rows.map(r=>r.value))*1.12;
      const xx=i=>px+i*w/Math.max(1,rows.length-1),yy=v=>py+h-v*h/max;
      b+=txt(left,832,se.name,18,se.color)+txt(left+170,832,compact(chosen.value),25,C.ink)+txt(left+575,832,annual?chosen.date:chosen.date+" 新增",15,C.muted,"end");
      const last=rows.at(-1),before=annual?rows.at(-2):null;
      b+=txt(left,858,annual?`末两年同日回溯值变化 ＋${fmt((last.value/before.value-1)*100,1)}%`:`${s.months}个可用月份内新增 ${compact(rows.reduce((a,r)=>a+r.value,0))} 个仓库`,15,C.muted);
      for(let t=0;t<=2;t++){const val=max*t/2,y=yy(val);b+=line(px,y,px+w,y,C.line)+txt(px-9,y+4,compact(val),13,C.muted,"end");}
      b+=`<path d="${rows.map((r,i)=>(i?'L':'M')+xx(i)+','+yy(r.value)).join(' ')}" fill="none" stroke="${se.color}" stroke-width="2.8"/>`;
      const step=Math.max(1,Math.ceil((rows.length-1)/4));
      rows.forEach((r,i)=>{const selected=r.date===s.trendPoint;
        if(selected)b+=line(xx(i),py,xx(i),py+h,C.gold,1,'stroke-dasharray="3 4"');
        b+=action("trendPoint",r.date,`${se.name} ${r.date}：${fmt(r.value)}`,`<circle cx="${xx(i)}" cy="${yy(r.value)}" r="12" fill="transparent"/><circle cx="${xx(i)}" cy="${yy(r.value)}" r="${selected?5.5:3.3}" fill="${se.color}" stroke="${C.paper}" stroke-width="1.2"/>`);
        if(i===0||i===rows.length-1||(i%step===0&&rows.length-1-i>=step))b+=txt(xx(i),1043,annual?r.date.slice(0,4):r.date.slice(2),13,C.muted,"middle");
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
      let card=box(x,5,296,165,active?C.raised:C.paper,active?C.brand:C.line,7)+txt(x+15,34,title,19,C.ink,"start",'font-weight="600"');
      [["中国",cv,color("CN")],["美国",uv,color("US")]].forEach(([name,v,c],j)=>{
        const y=67+j*49,vv=s.mode==="share"?pct(v,den):v;
        card+=txt(x+15,y,name,15,c)+txt(x+280,y,s.mode==="share"?fmt(vv,2)+"%":compact(v),22,c,"end")+box(x+15,y+10,265,6,C.line,"none",2)+box(x+15,y+10,265*vv/max,6,c,"none",2);
      });
      card+=txt(x+15,155,s.mode==="share"?`样本分母 ${fmt(den)} ${u}`:`中国 ${compact(cv)} · 美国 ${compact(uv)} ${u}`,12,C.muted);
      b+=selector?action("metric",selector,`按${title}比较发布者`,card):card;
      exports.push({数据类型:"实测",读取日期:"2026-10-17",观察范围:"已识别组织样本",对象类型:"中美指标",指标:title,中国:cv,美国:uv,样本总量:den,中国样本份额_pct:pct(cv,den),美国样本份额_pct:pct(uv,den)});
    });
    b+=txt(24,204,`当前比较：${label(s)} · 点击上方数量、下载或关注，联动下方发布者。`,17,C.muted);
    ["CN","US"].forEach((code,i)=>{
      const x=22+i*640,cc=color(code),all=orgs(code).map(o=>({...o[s.asset],name:o.name,url:o.url,allAssets:o})).sort((a,b)=>value(b,k)-value(a,k)||a.name.localeCompare(b.name)),sum=total(all,k);
      const rows=s.detail==="ranking"?all.filter(o=>!s.query||o.name.toLowerCase().includes(s.query.toLowerCase())):all;
      const pageKey="page"+code,last=Math.max(0,Math.ceil(rows.length/8)-1);s[pageKey]=Math.min(Math.max(0,s[pageKey]),last);
      const chosen=rows.find(o=>o.name===s["selected"+code])||rows[0];
      b+=txt(x,248,countryName(code),25,cc,"start",'font-weight="600"')+txt(x+84,248,`${all.length} 个关联账号`,16,C.muted);
      b+=txt(x,283,`前三 ${fmt(pct(total(all.slice(0,3),k),sum),1)}%`,20,cc)+txt(x+210,283,`前十 ${fmt(pct(total(all.slice(0,10),k),sum),1)}%`,20,cc)+txt(x,309,`占本国组织样本${label(s)} · ${unit(s)}`,14,C.muted);
      if(s.detail==="ranking"){
        b+=svgButton(pageKey,"prev","←",x+414,291,36,false,s[pageKey]===0)+txt(x+504,312,`${s[pageKey]+1} / ${last+1}`,14,C.muted,"middle")+svgButton(pageKey,"next","→",x+558,291,36,false,s[pageKey]===last);
        b+=rankRows(rows,k,x,339,594,chosen?.name,"select"+code,r=>r.name,r=>r.name,s[pageKey]*8,8);
        if(!rows.length)b+=txt(x+297,450,"没有匹配账号",18,C.muted,"middle");
      }else{
        const px=x+48,py=357,w=520,h=235;
        b+=txt(x+48,339,"累计指标份额 · 账号按指标从高到低排列",14,C.muted);
        for(let t=0;t<=4;t++){const y=py+h-h*t/4;b+=line(px,y,px+w,y)+txt(px-8,y+5,t*25+"%",14,C.muted,"end");}
        b+=`<path d="M${px},${py+h} L${px+w},${py}" fill="none" stroke="${C.line}" stroke-dasharray="4 5"/>`+concentrationCurve(all,k,px,py,w,h,cc)+txt(px,622,"0",14,C.muted)+txt(px+w,622,"100% 发布账号",14,C.muted,"end");
      }
      b+=box(x,650,594,111,C.paper,C.line,6);
      if(chosen){b+=txt(x+14,677,trim(chosen.name,31),19,cc)+txt(x+578,677,compact(value(chosen,k)),24,C.ink,"end")+txt(x+14,708,`占本国${label(s)} ${fmt(pct(value(chosen,k),sum),2)}%`,16,C.muted)+txt(x+14,741,`模型 ${fmt(chosen.allAssets.models.models)} · 配套数据集 ${fmt(chosen.allAssets.datasets.datasets)}`,15,C.muted)+`<a href="${esc(chosen.url)}" target="_blank" rel="noopener">${txt(x+578,741,"账号原页 ↗",15,cc,"end")}</a>`;}
      else b+=txt(x+14,681,"暂无所选发布者",18,C.muted);
      exports.push(...rows.map((r,n)=>({数据类型:"实测",读取日期:"2026-10-17",观察范围:"本国全部关联账号；配套数据沿用同一组织名录",对象类型:"发布账号",国家:countryName(code),账号:r.name,排名:all.indexOf(r)+1,指标:label(s),数值:value(r,k),本国份额_pct:pct(value(r,k),sum)})));
    });
    let controls=assetControls(s)+seg("mode",[["share","样本内份额"],["count","绝对量"]],s.mode,"上方对照")+seg("detail",[["ranking","发布者排行"],["concentration","头部集中度"]],s.detail,"下方观察");
    if(s.detail==="ranking")controls+=search("cnus","搜索中美发布账号");
    paint(p,s,controls,b,"上方份额以全部已识别组织样本为分母；下方头部份额以本国组织样本为分母。搜索只查找账号，不改变集中度分母。账号尚未归并为企业集团。"+(s.detail==="concentration"?"曲线越早接近100%，供给越集中；虚线为各账号等量的参考。":""),exports,"",780);
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
    let controls=assetControls(s)+metricControls(s,true)+btn("clear","","全国视野")+badge();
    controls+=`<div class="s51-control-line">${seg("list",[["provinces","省级地区"],["organizations","发布组织"]],s.list,"右侧列表")}${search("china","搜索地区或组织")}${pageControls(s,rows.length)}</div>`;
    let b=metricCard(18,4,390,fmt(cn.organizations),"中国已识别发布组织","账号")+metricCard(426,4,390,fmt(cn[s.asset]),names[s.asset]+"供给","仓库")+metricCard(834,4,428,fmt(cn.unassignedDivision[s.asset]),"省级归属待补","仓库");
    b+=geography(s,"china",-56,110,.95,s.province)+txt(25,494,"对数色阶 · 未覆盖不代表零 · 含台湾省及南海诸岛",15,C.muted);
    b+=heading(850,126,s.list==="organizations"?(selected?trim(selected.name_zh,12):"中国")+" · 组织":"省级地区",`${label(s)} · ${unit(s)} · 点击下钻`,390);
    b+=rankRows(rows,k,844,176,418,s.list==="organizations"?s.organization:s.province,s.list==="organizations"?"organization":"province",r=>r.id,r=>r.name,s.page*10);
    b+=selectedFooter(selected||cn,s,org?org.name:selected?selected.name_zh:"中国 · 全国",org?`${selected?.name_zh||"中国"} · 所选发布账号`:selected?"切换“发布组织”，查看当前地区的具体供给者。":"点击省级地区，再进入发布组织；也可直接查看全国组织榜。",org);
    paint(p,s,controls,b,"省级归属待补保留在全国总量中。地图未覆盖地区留白，不以估算分配全国余量。切换资产保持地区选择。",rowsExport(rows.map(r=>({对象:r.name,编码:r.id,[label(s)]:value(r,k)})),s.list==="organizations"?"中国组织":"中国省级",s));
  }
  const renderers={world,cnus,china};
  function handle(p,s,k,v) {
    if(!own(p))return false;
    if(k==="table-page"){s.tablePage=Math.max(0,(s.tablePage||0)+(v==="next"?1:-1));return true;}
    s.tablePage=0;
    if(k==="clear"){Object.assign(s,{country:"",province:"",organization:"",query:"",page:0,list:p.dataset.gmChart==="china"?"provinces":"countries"});}
    else if(k==="pageCN"||k==="pageUS")s[k]=Math.max(0,s[k]+(v==="next"?1:-1));
    else if(k==="page")s.page=Math.max(0,s.page+(v==="next"?1:-1));
    else if(k==="country"&&p.dataset.gmChart==="world"){s.country=v;s.organization="";s.page=0;s.query="";}
    else if(k==="province"){s.province=v;s.organization="";s.page=0;s.query="";}
    else if(k==="organization")s.organization=v;
    else if(k==="selectCN")s.selectedCN=v;
    else if(k==="selectUS")s.selectedUS=v;
    else {s[k]=k==="months"?Number(v):v;if(["asset","metric","mode","list","country"].includes(k)){s.page=0;s.pageCN=0;s.pageUS=0;}}
    if(p.dataset.gmChart==="world"&&s.list==="organizations"&&!s.country)s.list="countries";
    return true;
  }
  function input(p,s,e) {
    if(!own(p)||!e.target.hasAttribute("data-s51-search"))return false;
    s.query=e.target.value;s.page=0;s.pageCN=0;s.pageUS=0;s.tablePage=0;return true;
  }
  function stamp(p,s) {
    if(p.dataset.gmChart==="world")return "OpenGauge 2026-10-17地域读取 · 趋势："+(s.trendMode==="annual"?"2026-09-13年度回溯":"截至2026-07月表，"+s.months+"个月")+" · 两者独立";
    return "OpenGauge · 2026-10-17读取 · 已识别组织及其配套数据 · 地理统计日未注明";
  }
  return {defaults,renderers,handle,input,stamp,own};
};
