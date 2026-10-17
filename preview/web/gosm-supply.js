/* GOSD 5.1 — observed supply and independently labelled scenarios. */
window.createGOSM51 = function (D, H) {
  "use strict";
  const O = D.supply51;
  const {esc,fmt,compact,txt,line,box,action,svg,btn,seg,chips,note,link,asset,set} = H;
  const names = {models:"模型",datasets:"配套数据集"};
  const CN = "中国", US = "美国";
  const defaults = {
    world:{asset:"models",metric:"count",country:"",organization:"",list:"countries",query:"",page:0},
    cnus:{asset:"models",mode:"share"},
    publishers:{asset:"models",metric:"downloads",mode:"ranking",selectedCN:"",selectedUS:"",page:0},
    china:{asset:"models",metric:"count",province:"",organization:"",list:"provinces",page:0,query:""},
    supply:{mode:"monthly",asset:"models",months:18,index:false},
    release:{months:12,countries:["CN","US","FR","DE"],month:"2026-07",mode:"count"},
    portfolio:{country:"CN",metric:"count",selected:"",query:"",page:0},
    scenarios:{preset:"balanced",retention:75,newcomers:200,months:12,focus:""},
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
    return `<p><b>实测补充快照。</b>2026-10-17读取 OpenGauge。平台总量标注2026-10-16；地理接口未给统一统计日，本图固定本次读取值。地域统计来自826个国家归属已关联的组织账号；配套数据集沿用这批模型发布组织，未覆盖全部数据集发布者。</p><p>下载为累计获取次数；点赞为关注信号。国家指发布组织归属，账号未归并为企业集团。月／年增量字段因时间窗口未完整说明，未用于本图。</p>${extra}<p>${link("http://47.100.76.186:9529/geography","OpenGauge 地理页")} · ${link(asset("supply-observation.json"),"本图实测数据 JSON")} · ${link(asset("supply-methods.md"),"统计口径与核验")}</p>`;
  }
  function rowsExport(rows,kind,s) {
    return rows.map(r=>({数据类型:"实测",读取日期:"2026-10-17",观察范围:"已识别国家的模型发布组织及其配套数据集",对象类型:kind,...r}));
  }
  function paint(p,s,controls,body,readout,rows,extra="",height=650,sourceText=null) {
    set(p,controls,svg(body,1280,height,p.querySelector("h3").textContent),note(readout),rows,sourceText||sources(s,extra));
    const inp=p.querySelector("[data-s51-search]");if(inp)inp.value=s.query||"";
    p.dataset.evidence=p.dataset.gmChart==="scenarios"?"simulated":"observed";
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
    paint(p,s,controls,body,`${names[s.asset]}地域样本与全平台规模分别展示。${s.asset==="datasets"?"配套数据集来自同一批模型发布组织，不能外推全部数据集生态。":"公开模型仓库包含不同任务、规模与适配版本。"}`,rowsExport(rr.map(r=>({对象:r.name,编码:r.id,[label(s)]:value(r,k)})),organizationMode?"组织":"国家",s),"",715);
  }
  function cnus(p,s) {
    const C=theme().C,a=A(s),cn=country(s,"CN"),us=country(s,"US");
    const metrics=[["activeProviders",`有${s.asset==="datasets"?"数据集":"模型"}的发布账号`,"个账号"],[s.asset,names[s.asset]+"数","个仓库"],["downloads","累计下载","次"],["likes","社区关注","赞"]];
    let b=heading(30,40,"中国",`同一地域组织样本`,540)+heading(730,40,"美国",`同一地域组织样本`,520);
    b+=txt(350,83,"中国",17,color("CN"))+txt(1060,83,"美国",17,color("US"));
    const exports=[];
    metrics.forEach(([k,l,u],i)=>{
      const y=130+i*104,den=a.summary[k],cv=value(cn,k),uv=value(us,k),cshare=pct(cv,den),ushare=pct(uv,den),max=s.mode==="share"?100:Math.max(cv,uv)*1.08;
      const v1=s.mode==="share"?cshare:cv,v2=s.mode==="share"?ushare:uv;
      b+=txt(30,y,l,20,C.ink)+txt(230,y,s.mode==="share"?"占全部已识别组织样本":"绝对量 · "+u,15,C.muted);
      b+=box(30,y+18,530,11,C.raised,"none",4)+box(30,y+18,530*v1/max,11,color("CN"),"none",4)+box(730,y+18,530,11,C.raised,"none",4)+box(730,y+18,530*v2/max,11,color("US"),"none",4);
      b+=txt(560,y,s.mode==="share"?fmt(cshare,2)+"%":compact(cv),25,color("CN"),"end")+txt(1260,y,s.mode==="share"?fmt(ushare,2)+"%":compact(uv),25,color("US"),"end");
      b+=txt(30,y+57,`中国 ${fmt(cv)} ${u}`,16,C.muted)+txt(730,y+57,`美国 ${fmt(uv)} ${u}`,16,C.muted);
      exports.push({指标:l,中国:cv,美国:uv,样本总量:den,中国样本份额_pct:cshare,美国样本份额_pct:ushare});
    });
    b+=box(30,562,1230,64,C.paper)+txt(48,588,"比较提示",16,C.brand)+txt(150,588,s.asset==="datasets"?"数据集是模型发布组织的配套资产；研究主体范围固定。":"同一账号可能提供多个模型与适配版本；数量、下载、关注分别解释。",17,C.ink)+txt(150,613,"份额的分母包含中美之外的已识别国家。组织数不等于企业集团数。",15,C.muted);
    paint(p,s,assetControls(s)+seg("mode",[["share","样本内份额"],["count","绝对量"]],s.mode)+badge(),b,"模型与数据集分别对照，单位和分母随当前资产显示。没有把下载次数作为用户数或性能分数。",rowsExport(exports,"中美指标",s));
  }
  function concentrationCurve(rows,k,x,y,w,h,c) {
    const sum=total(rows,k);let acc=0;
    let path=`M${x},${y+h}`;
    rows.forEach((r,i)=>{acc+=value(r,k);path+=` L${(x+w*(i+1)/Math.max(1,rows.length)).toFixed(2)},${(y+h-h*acc/(sum||1)).toFixed(2)}`;});
    return `<path d="${path}" fill="none" stroke="${c}" stroke-width="3.5"/>`;
  }
  function publishers(p,s) {
    const C=theme().C,k=key(s);const groups=["CN","US"].map(c=>({code:c,rows:orgs(c).map(o=>({...o[s.asset],name:o.name})).sort((a,b)=>value(b,k)-value(a,k)||a.name.localeCompare(b.name))}));
    let controls=assetControls(s)+metricControls(s)+seg("mode",[["ranking","发布账号排名"],["concentration","头部与长尾"]],s.mode)+badge();
    if(s.mode==="ranking")controls+=pageControls(s,Math.max(...groups.map(g=>g.rows.length)));
    let b="",exports=[];
    groups.forEach((g,gi)=>{
      const x=22+gi*640,cc=color(g.code),sum=total(g.rows,k),top3=total(g.rows.slice(0,3),k),top10=total(g.rows.slice(0,10),k),selected=s["selected"+g.code];
      b+=heading(x,36,`${countryName(g.code)} · ${g.rows.length} 个发布账号`,`${label(s)} · ${unit(s)}`,590);
      b+=metricCard(x,94,280,fmt(pct(top3,sum),1)+"%","前三账号份额","",cc)+metricCard(x+300,94,290,fmt(pct(top10,sum),1)+"%","前十账号份额","",cc);
      if(s.mode==="ranking")b+=rankRows(g.rows,k,x,205,590,selected,"select"+g.code,r=>r.name,r=>r.name,s.page*10);
      else{
        const px=x+42,py=225,w=520,h=255;
        for(let i=0;i<=4;i++){const yy=py+h-h*i/4;b+=line(px,yy,px+w,yy)+txt(px-7,yy+5,25*i+"%",14,C.muted,"end");}
        b+=`<path d="M${px},${py+h} L${px+w},${py}" fill="none" stroke="${C.line}" stroke-dasharray="5 5"/>`+concentrationCurve(g.rows,k,px,py,w,h,cc)+txt(px,py+h+30,"0",15,C.muted)+txt(px+w,py+h+30,"100% 发布账号",15,C.muted,"end");
        b+=txt(x,550,"从当前指标最高的账号依次累计",16,C.muted);
      }
      const chosen=g.rows.find(r=>r.name===selected)||g.rows[0];
      b+=box(x,580,590,57,C.paper)+txt(x+12,603,trim(chosen?.name||"暂无账号",27),17,cc)+txt(x+578,603,chosen?compact(value(chosen,k)):"—",20,C.ink,"end")+txt(x+12,626,`占本国组织样本 ${fmt(pct(value(chosen,k),sum),2)}% · 账号归属沿用平台`,15,C.muted);
      exports.push(...g.rows.map((r,i)=>({国家:countryName(g.code),账号:r.name,排名:i+1,指标:label(s),数值:value(r,k),本国份额_pct:pct(value(r,k),sum)})));
    });
    paint(p,s,controls,b,"排名和集中度使用当前所选指标，同一账号的模型数量、累计下载与点赞分别计算。企业集团尚未归并。",rowsExport(exports,"发布账号",s));
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
  function linePlot(rows,series,x,y,w,h,{index=false,selectMonth="",clickMonth=false}={}) {
    const C=theme().C;const transformed=series.map(se=>({...se,vals:rows.map(r=>index?value(r,se.key)/(value(rows[0],se.key)||1)*100:value(r,se.key))}));
    const max=Math.max(1,...transformed.flatMap(s=>s.vals))*1.12;
    let b="";
    for(let i=0;i<=4;i++){const yy=y+h-h*i/4;b+=line(x,yy,x+w,yy)+txt(x-12,yy+5,index?fmt(max*i/4):compact(max*i/4),15,C.muted,"end");}
    const px=i=>x+(rows.length<2?w/2:i*w/(rows.length-1));
    transformed.forEach(se=>{let path="";se.vals.forEach((v,i)=>{path+=(i?" L":"M")+px(i)+","+(y+h-h*v/max);});b+=`<path d="${path}" fill="none" stroke="${se.color}" stroke-width="3.2"/>`;se.vals.forEach((v,i)=>{const m=rows[i].month||rows[i].date,cy=y+h-h*v/max;const dot=`<circle cx="${px(i)}" cy="${cy}" r="${selectMonth===m?6:3.5}" fill="${se.color}" stroke="${C.bg}" stroke-width="1.2"/>`;b+=clickMonth?action("month",m,`${se.label} ${m}：${fmt(v)}`,dot):dot;});});
    const step=Math.max(1,Math.ceil((rows.length-1)/Math.max(2,Math.floor(w/110))));
    rows.forEach((r,i)=>{if(i===0||i===rows.length-1||(i%step===0&&rows.length-1-i>=step))b+=txt(px(i),y+h+30,(r.month||r.date).slice(0,7),14,C.muted,"middle");});
    if(selectMonth){const i=rows.findIndex(r=>(r.month||r.date)===selectMonth);if(i>=0)b+=line(px(i),y,px(i),y+h,C.gold,1.5,'stroke-dasharray="4 5"');}
    transformed.forEach((se,i)=>{const lx=x+i*240;b+=box(lx,y-44,12,12,se.color,"none",3)+txt(lx+21,y-32,se.label,17,C.ink);});
    return b;
  }
  function supply(p,s) {
    const C=theme().C;
    let controls=seg("mode",[["monthly","平台月度新增"],["annual","报告年度回溯"]],s.mode)+seg("index",[["false","数量"],["true","期初=100"]],String(s.index));
    let b="",rows,sourceText;
    if(s.mode==="monthly"){
      controls+=seg("months",[[6,"6个月"],[12,"12个月"],[18,"18个月"]],s.months)+badge("实测月表 · 截至2026-07");
      const m=new Map(O.global.datasets.monthlyNew.map(r=>[r.month,r.count]));rows=O.global.models.monthlyNew.filter(r=>m.has(r.month)).slice(-s.months).map(r=>({month:r.month,models:r.count,datasets:m.get(r.month)}));
      b+=heading(34,44,"模型与数据集的月度新增",`${rows[0].month} — ${rows.at(-1).month} · 两类资产使用同一月度窗口`);
      b+=linePlot(rows,[{key:"models",label:"模型",color:colors()[0]},{key:"datasets",label:"数据集",color:colors()[1]}],105,165,1090,330,{index:s.index});
      b+=metricCard(36,554,590,compact(total(rows,"models")),"窗口内新增模型","仓库")+metricCard(654,554,590,compact(total(rows,"datasets")),"窗口内新增数据集","仓库");
      sourceText=sources(s,"<p>月度序列接口返回2022-03至2026-07，共53个月。未与10月总量拼接。该序列的历史留存与下架处理方法尚未完整说明，按平台发布月计数展示。</p>");
    }else{
      controls+=badge("报告基线 · 2026-09-13回溯");rows=D.supply;
      b+=heading(34,44,"模型与发布账号的积累过程","每年9月13日 · 同一批仍可见模型回溯");
      b+=linePlot(rows,[{key:"models",label:"模型仓库",color:colors()[0]},{key:"publishers",label:"发布账号",color:colors()[1]}],105,165,1090,330,{index:s.index});
      const now=rows.at(-1),prev=rows.at(-2);
      b+=metricCard(36,554,590,fmt((now.models/prev.models-1)*100,1)+"%","末两年同日模型回溯值变化")+metricCard(654,554,590,fmt((now.publishers/prev.publishers-1)*100,1)+"%","末两年同日发布账号回溯值变化");
      sourceText=H.source(["supply"],"报告2026-09-13仍可见模型的创建时间回溯；发布账号包含组织与个人，不等于开发者人数，不是历年独立全量快照。");
    }
    paint(p,s,controls,b,"年度回溯和月度新增独立呈现；期初指数只比较变化幅度，不改变原始计数。",rows.map(r=>({数据类型:"实测",统计视角:s.mode==="monthly"?"平台发布月序列":"报告年度回溯",...r})),"",660,sourceText);
  }
  function release(p,s) {
    const C=theme().C,rows=D.monthly.slice(-s.months);if(!rows.some(r=>r.month===s.month))s.month=rows.at(-1).month;
    const controls=seg("months",[[6,"6个月"],[12,"12个月"]],s.months)+seg("mode",[["count","新增数量"],["index","期初=100"]],s.mode)+chips("countries",[["CN","中国"],["US","美国"],["FR","法国"],["DE","德国"]],s.countries,"对比")+badge("报告基线 · 2025-09—2026-08");
    const cc={CN:colors()[0],US:colors()[1],FR:colors()[2],DE:colors()[3]};
    let b=heading(30,38,"各国发布节奏与集中发布事件","点击曲线上的月份，查看同月新增；原稿事件解释单独标注。");
    b+=linePlot(rows,s.countries.map(c=>({key:c,label:countryName(c),color:cc[c]})),90,151,1100,250,{index:s.mode==="index",selectMonth:s.month,clickMonth:true});
    const r=rows.find(r=>r.month===s.month);s.countries.forEach((c,i)=>{const w=1220/s.countries.length;b+=metricCard(30+i*w,458,w-16,fmt(r[c]),`${countryName(c)} · ${s.month}`,"新增",cc[c]);});
    b+=box(30,565,1220,74,C.paper);
    if(s.month==="2026-07")b+=txt(48,590,"原稿案例 · 法国 / OpenMed",18,C.brand)+txt(48,618,"法国当月新增784个；原稿核对其中755个来自OpenMed，主要为设备适配版本。",17,C.ink);
    else b+=txt(48,590,`${s.month} · 发布记录观察`,18,C.brand)+txt(48,618,"该月份尚未附具名事件核验；可比较新增节奏，不据此推断研发突破或模型性能。",17,C.ink);
    paint(p,s,controls,b,"OpenMed事件归因来自用户原稿核对；本次未重新逐仓库审计。适配可改善可用性，新增仓库数不等于基础模型研发数。",rows.map(r=>({数据类型:"实测",month:r.month,...Object.fromEntries(s.countries.map(c=>[c,r[c]]))})),"",660,H.source(["monthly"],"2025-09—2026-08，按2026-09-13仍可见模型创建时间回溯。法国2026-07事件说明来自原稿，细项发布记录待复核。"));
  }
  function portfolio(p,s) {
    const C=theme().C;let rows=orgs(s.country==="ALL"?"":s.country).filter(r=>!s.query||r.name.toLowerCase().includes(s.query.toLowerCase()));
    const mk=s.metric==="count"?"models":"downloads",dk=s.metric==="count"?"datasets":"downloads";
    rows.sort((a,b)=>value(b.models,mk)+value(b.datasets,dk)-value(a.models,mk)-value(a.datasets,dk));
    const selected=rows.find(r=>r.name===s.selected)||null;
    const controls=seg("country",[["CN","中国"],["US","美国"],["ALL","全部已识别组织"]],s.country)+seg("metric",[["count","资产数量"],["downloads","累计下载"]],s.metric)+search("portfolio","搜索发布账号")+pageControls(s,rows.length,8)+badge();
    let b=heading(30,38,"模型 × 配套数据集",s.metric==="count"?"每个点是一个发布账号 · 对数坐标 log(1＋仓库数)":"每个点是一个发布账号 · 对数坐标 log(1＋下载量)");
    [["中国",color("CN")],["美国",color("US")],["其他",C.unknown]].forEach(([label,c],i)=>{b+=box(890+i*120,51,12,12,c,"none",3)+txt(910+i*120,63,label,15,C.muted);});
    const px=100,py=131,w=700,h=335,maxX=Math.max(1,...rows.map(r=>value(r.models,mk))),maxY=Math.max(1,...rows.map(r=>value(r.datasets,dk)));
    for(let i=0;i<=4;i++){const xx=px+w*i/4,yy=py+h-h*i/4;b+=line(xx,py,xx,py+h)+line(px,yy,px+w,yy)+txt(xx,py+h+27,compact(Math.expm1(Math.log1p(maxX)*i/4)),14,C.muted,"middle")+txt(px-12,yy+5,compact(Math.expm1(Math.log1p(maxY)*i/4)),14,C.muted,"end");}
    b+=txt(px+w/2,py+h+58,s.metric==="count"?"模型仓库数":"模型累计下载",17,C.muted,"middle")+txt(px,py-18,s.metric==="count"?"数据集仓库数":"数据集累计下载",17,C.muted);
    const dots=[...rows.filter(r=>r.name!==s.selected),...rows.filter(r=>r.name===s.selected)];
    for(const r of dots){const xx=px+w*Math.log1p(value(r.models,mk))/Math.log1p(maxX),yy=py+h-h*Math.log1p(value(r.datasets,dk))/Math.log1p(maxY),active=r.name===s.selected;
      b+=action("selected",r.name,`${r.name}：模型${fmt(value(r.models,mk))}，数据集${fmt(value(r.datasets,dk))}`,`<circle cx="${xx}" cy="${yy}" r="${active?9:5}" fill="${r.countryCode==="CN"?color("CN"):r.countryCode==="US"?color("US"):C.unknown}" fill-opacity="${active?1:.58}" stroke="${active?C.gold:C.bg}" stroke-width="${active?3:1}"/>`);
    }
    b+=heading(850,119,"发布账号",`${rows.length} 个匹配账号 · 点击定位`,390);
    b+=rankRows(rows.map(r=>({name:r.name,combined:value(r.models,mk)+value(r.datasets,dk)})),"combined",846,176,410,s.selected,"selected",r=>r.name,r=>r.name,s.page*8,8);
    b+=box(30,557,1220,79,C.paper)+txt(48,583,selected?trim(selected.name,35):"选择一个账号，查看配套资产",20,C.brand);
    if(selected)b+=txt(48,615,`${countryName(selected.countryCode)} · ${selected.divisionCodes.length?selected.divisionCodes.join(" / "):"省级归属待补"}`,16,C.muted)+txt(700,585,`模型 ${fmt(selected.models.models)}`,20,C.ink)+txt(700,616,`数据集 ${fmt(selected.datasets.datasets)}`,20,C.ink)+`<a href="${esc(selected.url)}" target="_blank" rel="noopener">${txt(1230,615,"账号原页 ↗",16,C.brand,"end")}</a>`;
    else b+=txt(48,614,"这是组织的资产组合；模型与数据集的直接使用关系需另查模型卡和数据说明。",17,C.muted);
    paint(p,s,controls,b,"样本来自模型发布组织名录，不包含完整的数据集独立发布者。右侧列表按当前两类资产数值之和排序，仅用于查找。",rowsExport(rows.map(r=>({账号:r.name,国家:countryName(r.countryCode),模型:r.models.models,模型累计下载:r.models.downloads,数据集:r.datasets.datasets,数据集累计下载:r.datasets.downloads})),"组织资产组合",s));
  }
  function scenarios(p,s) {
    const C=theme().C,presets={balanced:[20,35,25,20],base:[40,30,15,15],adapt:[10,25,30,35]},roleNames=["基础训练","微调改进","量化转换","部署适配"],shares=presets[s.preset];
    let controls=badge("模拟情景 · 非实测，不用于国家排名",true)+seg("preset",[["balanced","均衡供给"],["base","基础开发加强"],["adapt","适配支持加强"]],s.preset,"假设");
    controls+=`<div class="s51-control-line">${seg("retention",[[60,"60%"],[75,"75%"],[90,"90%"]],s.retention,"每月继续发布比例")}${seg("newcomers",[[100,"100"],[200,"200"],[300,"300"]],s.newcomers,"每月新增发布者")}${seg("months",[[6,"6个月"],[12,"12个月"],[18,"18个月"]],s.months,"观察")}</div>`;
    let b=heading(30,38,"模拟实验：从供给构成到持续参与","以下数值全部由假设生成，不代表中美或任何真实组织。");
    b+=txt(640,355,"模拟情景",96,C.gold,"middle",'opacity="0.10" font-weight="700"');
    b+=heading(35,126,"供给构成假设","固定1,000项供给活动，按单一主角色分组");
    let exports=[],y=196;
    shares.forEach((v,i)=>{b+=txt(35,y,roleNames[i],18,C.ink)+box(190,y-16,340*v/100,21,colors()[i],"none",4)+txt(565,y,`${v}% · ${v*10}项`,18,C.ink,"end");exports.push({数据类型:"模拟",情景:s.preset,观察:"角色构成",角色:roleNames[i],数值:v*10,单位:"项"});y+=69;});
    const rows=[];let active=0;for(let i=1;i<=s.months;i++){active=s.newcomers+active*s.retention/100;rows.push({month:`第${i}月`,active:Math.round(active),newcomers:s.newcomers});exports.push({数据类型:"模拟",情景:s.preset,观察:"持续参与",月份:i,每月新增:s.newcomers,继续发布比例_pct:s.retention,数值:Math.round(active),单位:"账号"});}
    b+=heading(720,126,"持续参与假设","每月新增＋上月继续发布者");
    b+=linePlot(rows,[{key:"active",label:"当月发布者（模拟）",color:colors()[0]}],740,235,475,230);
    b+=box(30,562,1220,76,C.paper,C.gold)+txt(48,587,"假设计算",17,C.gold)+txt(163,587,`当月发布者 = ${s.newcomers} ＋ 上月发布者 × ${s.retention}%`,19,C.ink)+txt(48,618,"两组假设独立调整；供给角色构成不被解释为留存变化的原因。未模拟真实国家或组织。",16,C.muted);
    paint(p,s,controls,b,"模拟用于评审图形和提出研究问题。下一步需补供给角色标注、首次发布、持续发布与退出记录，再替换为实测。",exports,"",660,`<p><b>全部为模拟情景。</b>固定1,000项供给活动，角色份额为预设假设；参与序列从0开始，按“每月新增＋上月发布者×继续发布比例”递推。角色构成与参与序列没有因果连接，不对实际增长作预测。每条CSV记录均保留“模拟”标识。</p><p>${link(asset("supply-scenarios.json"),"预设与公式 JSON")} · ${link(asset("supply-methods.md"),"模拟与实测边界")}</p>`);
  }
  const renderers={world,cnus,publishers,china,supply,release,portfolio,scenarios};
  function handle(p,s,k,v) {
    if(!own(p))return false;
    if(k==="table-page"){s.tablePage=Math.max(0,(s.tablePage||0)+(v==="next"?1:-1));return true;}
    s.tablePage=0;
    if(k==="clear"){Object.assign(s,{country:"",province:"",organization:"",query:"",page:0,list:p.dataset.gmChart==="china"?"provinces":"countries"});}
    else if(k==="page")s.page=Math.max(0,s.page+(v==="next"?1:-1));
    else if(k==="countries") {if(s.countries.includes(v)){if(s.countries.length>1)s.countries=s.countries.filter(c=>c!==v);}else s.countries.push(v);}
    else if(k==="country"&&p.dataset.gmChart==="world"){s.country=v;s.organization="";s.page=0;s.query="";}
    else if(k==="province"){s.province=v;s.organization="";s.page=0;s.query="";}
    else if(k==="organization")s.organization=v;
    else if(k==="selectCN")s.selectedCN=v;
    else if(k==="selectUS")s.selectedUS=v;
    else if(k==="index")s.index=v==="true";
    else {s[k]=["months","retention","newcomers"].includes(k)?Number(v):v;if(["asset","metric","mode","list","country"].includes(k))s.page=0;}
    if(p.dataset.gmChart==="world"&&s.list==="organizations"&&!s.country)s.list="countries";
    return true;
  }
  function input(p,s,e) {
    if(!own(p)||!e.target.hasAttribute("data-s51-search"))return false;
    s.query=e.target.value;s.page=0;s.tablePage=0;return true;
  }
  function stamp(p,s) {
    if(p.dataset.gmChart==="scenarios")return "全部模拟 · 角色构成与持续参与独立假设 · 不用于国家排名";
    if(p.dataset.gmChart==="release")return "OpenGauge报告基线 · 2025-09—2026-08 · 发布事件沿用原稿说明";
    if(p.dataset.gmChart==="supply")return s.mode==="annual"?"报告2026-09-13仍可见样本回溯 · 模型与发布账号":"OpenGauge月度序列 · 截至2026-07 · 与10月总量独立";
    return "OpenGauge · 2026-10-17读取 · 已识别组织及其配套数据 · 地理统计日未注明";
  }
  return {defaults,renderers,handle,input,stamp,own};
};
