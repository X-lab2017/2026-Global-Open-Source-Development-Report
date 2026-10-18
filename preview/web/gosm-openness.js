/* 5.3 — dual-axis explanation, fixed-cohort comparisons, model evidence. */
window.createGOSM53 = function(D,H){
 'use strict';
 const {esc,fmt,txt,line,box,action,svg,btn,seg,note,link,asset,set}=H;
 const R=D.openness53, LS=R.standard.levels, OS=R.standard.openness;
 const C=()=>H.colors().C, P=()=>H.colors().palette;
 const Q=['高完整-高开放','低完整-高开放','高完整-低开放','低完整-低开放'];
 const qcolor=i=>[P()[0],P()[2],P()[1],C().unknown][i];
 const countryName=c=>({'United States of America':'美国','Unknown':'归属未知'}[c]||D.geography.find(g=>g.en===c)?.name||c);
 const trim=(v,n=32)=>String(v).length>n?String(v).slice(0,n-1)+'…':String(v);
 const pct=(v,n)=>fmt(n?v/n*100:0,1)+'%';
 const sum=(rs,k)=>rs.reduce((n,r)=>n+(Number(r[k])||0),0);
 const models=new Map(D.opennessCurrent.models.map(m=>[m.model_id,m]));
 const cases=new Map(D.cases.models.map(m=>[m.model_id,m]));
 const defaults={openness:{view:'overview',overviewDetail:'materials',l:3,o:3,sample:'report',quad:Q[1],demo:''},'open-groups':{mode:'map',mapMetric:'count',mapCountry:'',mapPage:0,regions:D.openRegions.map(r=>r.group),region:'中国',quad:Q[0]},dossiers:{view:'map',mapType:'all',pubCountry:'',pubPage:0,pubSelected:'',metric:'double_high',publisher:'企业',pool:'platform',query:'',page:0,model:'meta-llama/Llama-3.1-8B',level:'L3',field:'',detail:false}};
 const own=p=>Object.hasOwn(defaults,p.dataset.gmChart);
 const sb=(k,v,label,x,y,w,on=false,disabled=false)=>{let b=box(x,y,w,29,on?C().raised:C().bg,on?C().brand:C().line,5)+txt(x+w/2,y+20,label,14,disabled?C().unknown:on?C().brand:C().ink,'middle');return disabled?`<g aria-disabled="true">${b}</g>`:action(k,v,label,b);};
 function wrap(text,x,y,width,size=16,color=C().muted,leading=26){let lines=[],s='',units=0;for(const ch of String(text)){const u=ch.charCodeAt(0)>255?1:.55;if(units+u>width/size&&s){lines.push(s);s='';units=0;}s+=ch;units+=u;}if(s)lines.push(s);return lines.map((l,i)=>txt(x,y+i*leading,l,size,color)).join('');}
 const safe=u=>/^https?:\/\//.test(u||'');
 function paint(p,controls,b,readout,rows,source){const keys=[...new Set(rows.flatMap(r=>Object.keys(r)))];set(p,controls,svg(b,1280,560,p.querySelector('h3').textContent),note(readout),rows.map(r=>Object.fromEntries(keys.map(k=>[k,r[k]??'']))),source);p.dataset.evidence='observed-with-labeled-teaching-example';if(p.s53StandardLevel){const sheet=p.querySelector('.gm-source');sheet.open=true;const target=sheet.querySelector('[data-standard-level="'+p.s53StandardLevel+'"]');if(target)sheet.scrollTop=Math.max(0,target.offsetTop-60);p.s53StandardLevel='';}}
 function sources(keys,text){return H.source(keys,text)+`<p>${link(asset('openness53-methods.md'),'5.3 方法与样本边界')} · ${link('http://47.100.76.186:9529/openness','开放评估平台')} · ${link('http://47.100.76.186:9529/modelrank','ModelRank 平台')}</p>`;}
 function standardSource(){return `<p><strong>先 L 后 O：以具体模型发布单元（MRU）评估。</strong>较高 L 必须满足全部较低等级要求；文件存在与验证通过分别记录。本标准已发布；既有870/884样本仍保留源评估结果，不宣称已经按正式标准逐条重评。</p><div class="s53-rules">${LS.map(l=>`<section data-standard-level="${l.id}"><h4>${l.id} ${l.label} · 第7.1.${Number(l.id.slice(1))+1}条</h4><p>${l.id==='L1'?'以下为本级必备材料。':'继承全部较低等级要求；以下为本级新增要求。'}</p><ol>${R.standard.requirements[l.id].map(([title,body])=>`<li><strong>${esc(title)}</strong>：${esc(body)}</li>`).join('')}</ol><p><strong>有效性验证：</strong>${esc(R.standard.requirements.verification[l.id])}</p></section>`).join('')}${OS.map(o=>`<section><h4>${o.id} ${o.label}</h4><p>${o.detail}</p></section>`).join('')}</div><p><strong>特殊情形：</strong>核心材料缺乏可验证许可，结论为“开放性不合格（未声明许可）”，不得归入O1—O4。多材料组合需考虑限制较强的许可条件；非核心材料缺失许可如被排除，应明确记录。安全合规、侵权风险和许可兼容性不在本分级结论范围内。</p><p>${link(R.standard.publication.announcement_url,'工信部正式公告')} · ${link(R.standard.publication.annex_url,'公告附件第465项')} · ${link(asset(R.standard.pdf),'规范参考全文')} · ${esc(R.standard.version_note)} 本图依用户提供文本第6—8章及附录解释，原统计保留源评估等级。教学示例 Atlas-Demo v1.0 为模拟，不进入统计。</p>`;}
 function overview(s){
  const c=C(),l=LS[s.l-1],o=OS[s.o-1],license=s.overviewDetail==='license';
  let b=txt(22,29,'从部署到全链复现，读懂模型开放的五层交付',22,c.ink)+`<a href="${esc(R.standard.publication.announcement_url)}" target="_blank" rel="noopener">${txt(1258,29,'行业标准 SJ/T 12304—2026 ↗',15,c.brand,'end')}</a>`;
  const titles=['本地运行推理','理解原理与边界','复用组件再训练','独立验证性能','全流程端到端复现'];
  [...LS].reverse().forEach((lev,i)=>{const n=5-i,y=64+i*66,top=164+i*84,bottom=top+78,cx=338,on=s.l===n;
   const path=`M${cx-top/2} ${y} L${cx+top/2} ${y} L${cx+bottom/2} ${y+59} L${cx-bottom/2} ${y+59} Z`;
   b+=action('overviewLevel',n,lev.id+' '+lev.label+':'+titles[n-1],`<path d="${path}" fill="${on?c.brand:c.raised}" stroke="${on?c.brand:c.line}" stroke-width="${on?2:1}"/>`+txt(cx,y+24,lev.id+' '+lev.label,18,on?c.bg:c.ink,'middle','font-weight="600"')+txt(cx,y+46,titles[n-1],14,on?c.bg:c.muted,'middle'));
   b+=line(cx+bottom/2+12,y+32,683,y+32,on?c.brand:c.line,1,on?'':'stroke-dasharray="3 4"');
  });
  b+=line(32,368,32,80,c.brand,1.5)+`<path d="M27 88L32 78L37 88" fill="none" stroke="${c.brand}" stroke-width="1.5"/>`+txt(50,88,'完整性',13,c.muted)+txt(50,108,'逐级累进',13,c.muted)+txt(50,382,'高等级包含低等级全部要求',13,c.muted);
  b+=box(705,57,557,340,c.paper,c.line,8)+sb('overviewDetail','materials','材料要求',725,70,105,!license)+sb('overviewDetail','license','许可条件',839,70,105,license)+sb('standardDetails',l.id,'本级完整材料清单 →',963,70,278);
  b+=txt(725,137,license?o.id+' '+o.label:l.id+' '+l.label,27,c.brand);
  if(license){b+=wrap(o.detail,725,175,512,18,c.ink,29)+line(725,282,1241,282,c.line)+wrap('开放性 O 单独描述使用、修改与再分发的权利和义务。先确定材料的 L，再按相应材料范围判断 O。',725,311,512,16,c.muted,25)+txt(725,378,'核心材料未声明许可时，不归入 O1—O4。',15,c.muted);}
  else {b+=wrap(l.detail,725,176,512,15,c.ink,23)+line(725,324,1241,324,c.line)+txt(725,349,'如何验证',14,c.brand)+wrap(l.verify,725,374,512,15,c.muted,22);}
  b+=txt(25,423,'L 看材料与验证；O 看许可权利与义务。两维组合为 LkOy。',17,c.ink)+txt(1258,423,'层宽仅为结构示意，不表示模型数量',12,c.muted,'end');
  OS.forEach((o,i)=>{const x=18+i*314,on=s.o===i+1;b+=action('overviewO',i+1,o.id+' '+o.label,box(x,440,302,91,on?c.raised:c.paper,on?c.brand:c.line,7)+txt(x+17,470,o.id+' '+o.label,19,on?c.brand:c.ink)+txt(x+17,498,o.short,15,c.muted)+txt(x+285,516,on?'已选择':'点选解释 →',12,c.muted,'end'));});
  return b;
 }
 const typeDefs=[['all','全部主体'],['company','企业'],['user','个人账号'],['nonprofit','高校 / 非营利'],['community','社区']];
 const typeKey=m=>['non-profit','university'].includes(m.org_type)?'nonprofit':m.org_type;
 const countryIndex=new Map(D.geography.map(g=>[g.en,g.id]));
 [['United States of America','US'],['South Korea','KR'],['Czech Republic','CZ'],['Unknown','unknown']].forEach(([n,id])=>countryIndex.set(n,id));
 const codeOf=m=>countryIndex.get(m.country)||'unknown';
 const geo=D.supply51.geometry.world,geoBy=new Map(geo.map(f=>[f.id,f]));
 const geoName=id=>id==='unknown'?'归属未知':geoBy.get(id)?.name||D.geography.find(g=>g.id===id)?.name||id;
 function countries(ms){const m=new Map();ms.forEach(o=>{const code=codeOf(o);if(!m.has(code))m.set(code,{code,name:geoName(code),models:[],n:0,high_open:0,double_high:0,q:Q.map(()=>0)});const r=m.get(code);r.models.push(o);r.n++;if(['O2','O3','O4'].includes(o.openness_level))r.high_open++;if(['L3','L4','L5'].includes(o.strict_completeness_level)&&['O2','O3','O4'].includes(o.openness_level))r.double_high++;r.q[Q.indexOf(o.strict_quadrant)]++;});return [...m.values()].sort((a,b)=>b.n-a.n||a.code.localeCompare(b.code));}
 const allCountries=countries([...models.values()]);
 function worldMap(rows,selected,metric,bubbles=false){
  const c=C(),by=new Map(rows.map(r=>[r.code,r])),max=Math.max(1,...rows.map(r=>r.n));let b='';
  for(const f of geo){const r=by.get(f.id),active=selected===f.id,value=r?(metric==='count'?r.n:r[metric]/r.n):null,alpha=!r?.n?.06:bubbles?.10:metric==='count'?.18+.77*Math.log1p(value)/Math.log1p(max):.12+.83*value;
   const path=`<path d="${f.d}" fill="${c.brand}" fill-opacity="${alpha}" stroke="${active?c.gold:c.line}" stroke-width="${active?2.7:.75}" fill-rule="evenodd"/>`;
   b+=action('mapCountry',f.id,f.name+(r?'：'+r.n+'个模型':'：补充样本未覆盖'),path);
  }
  if(bubbles)rows.filter(r=>r.code!=='unknown'&&geoBy.get(r.code)).sort((a,b)=>b.n-a.n).forEach(r=>{const [x,y]=geoBy.get(r.code).center,radius=4+26*Math.sqrt(r.n/max);b+=action('mapCountry',r.code,r.name+'：'+r.n+'个模型',`<circle cx="${x}" cy="${y}" r="${radius}" fill="${c.brand}" fill-opacity=".46" stroke="${selected===r.code?c.gold:c.brand}" stroke-width="${selected===r.code?3:1}"/>`);});
  const labels=[...new Set(['CN','US',...rows.filter(r=>r.code!=='unknown').slice(0,3).map(r=>r.code),selected])].filter(id=>geoBy.has(id));
  labels.forEach(id=>{const f=geoBy.get(id),[x,y]=f.center,name=f.name;let dy=bubbles?-39:-5;b+=`<g pointer-events="none">${box(x-name.length*9-5,y+dy-20,name.length*18+10,27,c.bg,'none',4)}${txt(x,y+dy,name,17,c.ink,'middle')}</g>`;});
  return `<g data-s53-world transform="translate(54,50) scale(.90)">${b}</g>`;
 }
 function countryRowsExport(rows){return rows.map(r=>({记录类型:'884平台国家汇总',读取日期:'2026-10-17',国家或地区:r.name,代码:r.code,模型数:r.n,高开放数:r.high_open,高开放_pct:r.high_open/r.n*100,双高数:r.double_high,双高_pct:r.double_high/r.n*100,...Object.fromEntries(Q.map((q,i)=>[q,r.q[i]]))}));}
 function regionMap(p,s){
  const c=C(),selected=allCountries.find(r=>r.code===s.mapCountry),metric=s.mapMetric||'count',ml=metric==='count'?'模型数量':metric==='high_open'?'高开放比例':'双高比例',known=allCountries.filter(r=>r.code!=='unknown'),n=sum(allCountries,'n'),unknown=allCountries.find(r=>r.code==='unknown'),right=933;
  const controls=seg('mode',[['map','地图'],['share','比例'],['count','数量']],s.mode)+`<label class="s53-select">地图指标<select data-s53-map-metric aria-label="开放地图指标">${[['count','模型数量'],['high_open','高开放比例'],['double_high','高完整且高开放比例']].map(([v,l])=>`<option value="${v}" ${metric===v?'selected':''}>${l}</option>`).join('')}</select></label><span class="s53-caption">地图 · 平台884 / 比例、数量 · 报告870</span>`;
  let b=txt(22,29,'开放模型在哪里 · '+ml,22,c.ink)+txt(1258,29,'2026-10-17 · 884 条平台记录',14,c.muted,'end');
  b+=box(18,47,890,404,c.paper,c.line,7)+worldMap(allCountries,s.mapCountry,metric)+box(923,47,339,404,c.paper,c.line,7);
  if(!s.mapCountry){
   const maxPage=Math.max(0,Math.ceil(known.length/7)-1);s.mapPage=Math.min(s.mapPage||0,maxPage);b+=txt(right+8,78,'国家与地区 · 点选查看',18,c.ink);
   const ranked=known.slice().sort((a,b)=>metric==='count'?b.n-a.n:b[metric]/b.n-a[metric]/a.n);
   ranked.slice(s.mapPage*7,s.mapPage*7+7).forEach((r,i)=>{const y=111+i*39;const label=metric==='count'?r.n+' 个':pct(r[metric],r.n);b+=action('mapCountry',r.code,r.name,box(934,y-19,314,35,c.bg,'none',3)+txt(944,y+2,trim(r.name,9),16,c.ink)+txt(1238,y+2,label,17,c.brand,'end'));});
   b+=sb('mapPage','prev','←',941,399,38,false,s.mapPage===0)+txt(1090,420,`${s.mapPage+1} / ${maxPage+1}`,13,c.muted,'middle')+sb('mapPage','next','→',1208,399,38,false,s.mapPage===maxPage);
  }else{
   b+=txt(942,80,geoName(s.mapCountry),25,c.brand)+sb('mapClear','','返回列表',1145,59,99);
   if(selected){b+=txt(942,116,selected.n+' 个模型',23,c.ink)+txt(1240,115,'占884：'+pct(selected.n,884),14,c.muted,'end');b+=txt(942,154,'高开放 '+pct(selected.high_open,selected.n),17,P()[2])+txt(1240,154,'双高 '+pct(selected.double_high,selected.n),17,P()[0],'end');
    Q.forEach((q,i)=>{const y=203+i*43;b+=box(942,y-11,8,8,qcolor(i),'none',2)+txt(958,y,q.replace('-',' · '),14,c.muted)+txt(1240,y,String(selected.q[i]),17,c.ink,'end');});
    b+=wrap('比例仅描述所选样本。小样本比例应结合模型数阅读。',942,392,298,14,c.muted,23);
   }else b+=wrap('补充样本未覆盖该地区，不能据此判断当地没有开放模型。',942,136,296,17,c.muted,28);
  }
  b+=txt(34,438,metric==='count'?'颜色深浅按数量对数连续映射':'颜色深浅按比例线性映射',12,c.muted)+txt(890,438,'浅灰蓝：样本未覆盖',12,c.muted,'end');
  [['样本模型',n,''],['已识别归属的模型',n-unknown.n,''],['归属未知',unknown.n,'unknown']].forEach(([l,v,id],i)=>{const x=18+i*419,content=box(x,468,406,79,c.paper,s.mapCountry==='unknown'&&id?c.brand:c.line,7)+txt(x+16,496,l,15,c.muted)+txt(x+16,529,fmt(v),27,c.brand)+txt(x+390,525,id?'点选查看 →':i===1?known.length+' 个国家和地区':'独立于报告870样本',13,c.muted,'end');b+=id?action('mapCountry',id,l,content):content;});
  paint(p,controls,b,'地图使用884条模型级记录；比例与数量使用870条报告汇总。国家按发布主体归属，未知单列。',countryRowsExport(allCountries),sources(['openRegions'],'地图从884条平台strict记录按country字段逐条汇总，820条已识别国家、64条未知；25个有记录国家和地区。报告870仅有五组地域汇总，不能拆成国家，所以地图不回填870。两套样本不可作前后增长比较。地图几何沿用5.1已审地图，台湾为中国的一部分。图面颜色并非国家整体开放能力排名。'));
 }
 function publisherGeo(p,s){
  const c=C(),chosenType=s.mapType||'all',subset=[...models.values()].filter(m=>chosenType==='all'||typeKey(m)===chosenType),rs=countries(subset),filtered=subset.filter(m=>!s.pubCountry||codeOf(m)===s.pubCountry),bag=new Map();
  filtered.forEach(m=>{const k=m.story_org+'|'+codeOf(m)+'|'+typeKey(m);if(!bag.has(k))bag.set(k,{key:k,name:m.story_org,country:codeOf(m),type:typeKey(m),n:0,high_open:0,double_high:0,models:[]});let r=bag.get(k);r.models.push(m);r.n++;if(['O2','O3','O4'].includes(m.openness_level)){r.high_open++;if(['L3','L4','L5'].includes(m.strict_completeness_level))r.double_high++;}});
  const publishers=[...bag.values()].sort((a,b)=>b.n-a.n||a.name.localeCompare(b.name)),maxPage=Math.max(0,Math.ceil(publishers.length/6)-1);s.pubPage=Math.min(s.pubPage||0,maxPage);if(s.pubSelected&&!bag.has(s.pubSelected))s.pubSelected='';const sel=bag.get(s.pubSelected),unknown=rs.find(r=>r.code==='unknown')?.n||0;
  const controls=seg('view',[['map','主体地图'],['publishers','主体比较'],['models','模型与证据']],s.view)+`<div class="s53-type-picks" aria-label="选择发布主体类型">${typeDefs.map(([v,l])=>btn('mapType',v,l,chosenType===v)).join('')}</div>`;
  let b=txt(22,29,'发布主体的地域分布 · '+typeDefs.find(t=>t[0]===chosenType)[1],22,c.ink)+txt(1258,29,'平台补充样本 · 2026-10-17',14,c.muted,'end');
  b+=box(18,47,890,404,c.paper,c.line,7)+worldMap(rs,s.pubCountry,'count',true)+box(923,47,339,404,c.paper,c.line,7);
  b+=txt(941,78,s.pubCountry?geoName(s.pubCountry)+' · 发布主体':'发布主体 · 按模型数量',18,c.ink)+txt(941,104,`当前 ${filtered.length} 个模型 / ${publishers.length} 个主体标签`,13,c.muted);
  if(s.pubCountry)b+=sb('mapClear','','全球',1192,57,53);
  publishers.slice(s.pubPage*6,s.pubPage*6+6).forEach((r,i)=>{const y=135+i*42;b+=action('publisherSelect',r.key,r.name+' '+geoName(r.country),box(934,y-20,314,39,s.pubSelected===r.key?c.raised:c.bg,s.pubSelected===r.key?c.brand:'none',4)+txt(944,y,trim(r.name,27),15,c.ink)+txt(944,y+16,geoName(r.country)+' · '+typeDefs.find(t=>t[0]===r.type)?.[1],11,c.muted)+txt(1238,y+3,String(r.n),20,c.brand,'end'));});
  if(!publishers.length)b+=wrap('当前类型在所选地区暂无记录，可点击“全球”重选。',942,145,299,16,c.muted,26);
  b+=sb('pubPage','prev','←',941,399,38,false,s.pubPage===0)+txt(1090,420,`${s.pubPage+1} / ${maxPage+1}`,13,c.muted,'middle')+sb('pubPage','next','→',1208,399,38,false,s.pubPage===maxPage);
  b+=txt(34,438,'圆点大小示意模型数 · 点击国家筛选主体',13,c.muted)+action('pubUnknown','','查看未知归属',txt(889,438,'归属未知 '+unknown+' 个模型 →',13,c.brand,'end'));
  if(sel){b+=box(18,468,1244,79,c.paper,c.line,7)+txt(35,497,trim(sel.name,44),22,c.brand)+txt(35,528,geoName(sel.country)+' · '+sel.n+' 个模型',15,c.muted)+txt(730,497,'高开放',15,c.muted)+txt(730,530,pct(sel.high_open,sel.n),26,P()[2])+txt(970,497,'高完整且高开放',15,c.muted)+txt(970,530,pct(sel.double_high,sel.n),26,P()[0]);}
  else{b+=box(18,468,1244,79,c.paper,c.line,7)+txt(35,497,'从地域进入发布主体',20,c.ink)+txt(35,528,'同图完成：选类型 → 点国家 → 看主体与开放结构',15,c.muted)+txt(840,497,'位置表示主体所属国家，非机构地址。',14,c.muted)+txt(840,525,'模型数与主体标签数分别计数。',14,c.muted);}
  paint(p,controls,b,'地图按884条模型记录聚合，主体比较沿用870条报告。源站主体标签尚未合并为法律实体。',publishers.map(r=>({记录类型:'884平台发布主体地域',读取日期:'2026-10-17',源站主体:r.name,国家或地区:geoName(r.country),国家代码:r.country,主体类型:typeDefs.find(t=>t[0]===r.type)?.[1],模型数:r.n,高开放数:r.high_open,双高数:r.double_high,高开放_pct:r.high_open/r.n*100,双高_pct:r.double_high/r.n*100})),sources(['openPublishers'],'主体地图按884记录的country、org_type和story_org聚合；高校与非营利合并展示。点位使用国家示意中心，不代表城市、总部或实际贡献者所在地。同名主体跨国家/类型分别保留，不合并为法律实体。源站标签数与870报告的organizations列口径不同，不能作增减比较。无记录地区不按零供给解释。'));
 }

 function learn(s){
  const c=C(),l=LS[s.l-1],o=OS[s.o-1];let b=txt(22,29,'L 看材料是否齐备，O 看使用与改进的权利和条件。',20,c.ink);
  b+=txt(24,63,'完整性 L ↑ 逐级累进',14,c.muted)+txt(772,63,'许可开放性 O →',14,c.muted,'end');
  OS.forEach((o,i)=>{const x=252+i*132;b+=action('o',i+1,o.label,txt(x+58,96,o.id+' '+o.label,16,s.o===i+1?c.brand:c.ink,'middle'));});
  [...LS].reverse().forEach((l,row)=>{const y=114+row*65,n=5-row;b+=action('l',n,l.label,txt(24,y+26,l.id+' '+l.label,17,s.l===n?c.brand:c.ink)+txt(24,y+49,['权重 · 配置 · 分词 · 推理','原理 · 训练说明 · 测试结果','训练代码 · 数据 · 环境','测试材料 · 无重叠声明','数据处理 · 配方 · 复现指南'][n-1],12,c.muted));
   OS.forEach((o,i)=>{const x=252+i*132,on=s.l===n&&s.o===i+1;b+=action('cell',n+'|'+(i+1),`${l.id}${o.id}：${l.label}，${o.label}`,box(x,y,122,56,on?c.brand:s.l===n||s.o===i+1?c.raised:c.paper,on?c.brand:c.line,6)+txt(x+61,y+35,l.id+o.id,19,on?c.bg:c.muted,'middle',on?'font-weight="700"':''));});
  });
  b+=box(804,76,458,363,c.paper,c.line,8)+txt(826,107,s.demo?'教学示例 · '+R.teaching_example.name:'所选开放坐标',14,c.muted)+txt(826,152,l.id+o.id,38,c.brand)+txt(1250,149,l.short+' · '+o.label,18,c.ink,'end');
  b+=txt(826,189,'材料范围 · '+l.label,16,c.ink)+wrap((s.l>1?'继承 L1'+(s.l>2?'—L'+(s.l-1):'')+'；新增：':'必备材料：')+l.addition,826,216,410,16)+txt(826,277,'许可条件 · '+o.label,16,c.ink)+wrap(o.detail,826,304,410,15,c.muted,24);
  b+=txt(826,414,'先满足全部材料要求，再结合证据与运行验证判级。',14,c.muted);
  b+=box(18,454,1244,95,c.paper,c.line,7)+txt(34,478,'动手读懂两个维度',16,c.ink)+txt(34,505,'教学模拟 · 非真实模型',13,c.muted)+txt(34,531,'假设相应材料与验证均已满足',12,c.muted);
  b+=sb('demo','start','① 从 L2O3 出发',295,473,170,s.demo==='start')+sb('demo','materials','② 补齐训练材料',478,473,190,s.demo==='materials')+sb('demo','license','③ 增加商用限制',681,473,190,s.demo==='license')+sb('demo','reset','复位',884,473,68);
  const msg=s.demo==='materials'?'L2 → L3：补齐训练代码、数据或完整配方及环境；许可条件保持 O3。':s.demo==='license'?'L3O3 → L3O1：材料范围不变，因许可增加商用限制而改变 O。':s.demo==='start'?'L2O3：已满足部署与理解的材料要求，宽松许可不代表完整训练链已公开。':'点击任意坐标查看含义，或用三个步骤理解材料与许可怎样分别变化。';
  b+=txt(295,532,msg,14,c.muted);return b;
 }
 function sample(s){
  const c=C(),rows=s.sample==='report'?D.quadrants.map(r=>({name:r.completeness+'-'+r.openness,n:r.models})):D.opennessCurrent.quadrants.map(r=>({name:r.name,n:r.models})),n=sum(rows,'n'),selected=rows.find(r=>r.name===s.quad)||rows[0],hiO=sum(rows.filter(r=>r.name.endsWith('高开放')),'n'),hh=rows.find(r=>r.name===Q[0]).n;
  let b=txt(23,30,s.sample==='report'?'870 个模型 · 报告固定样本':'884 个模型 · 平台补充快照',23,c.ink)+txt(1258,30,s.sample==='report'?'提取于 2026-09-14':'读取于 2026-10-17',14,c.muted,'end');
  b+=txt(22,66,'高完整 L3—L5 ↑',14,c.muted)+txt(769,66,'高开放 O2—O4 →',14,c.muted,'end');
  const cells=[[Q[2],22,82],[Q[0],410,82],[Q[3],22,275],[Q[1],410,275]];
  cells.forEach(([name,x,y])=>{const r=rows.find(r=>r.name===name),i=Q.indexOf(name),on=s.quad===name;b+=action('quad',name,name,box(x,y,370,176,c.paper,on?qcolor(i):c.line,8)+box(x+18,y+22,5,30,qcolor(i),'none',2)+txt(x+35,y+44,name.replace('-',' · '),19,c.ink)+txt(x+24,y+101,fmt(r.n),42,qcolor(i))+txt(x+344,y+99,pct(r.n,n),24,c.ink,'end')+txt(x+24,y+144,'占当前样本 · 点选查看解释',14,c.muted));});
  b+=box(804,82,458,369,c.paper,c.line,8)+txt(826,116,'所选结构',14,c.muted)+txt(826,154,selected.name.replace('-',' · '),26,qcolor(Q.indexOf(selected.name)))+txt(826,195,fmt(selected.n)+' / '+fmt(n)+' 个模型',22,c.ink);
  const detail={'高完整-高开放':'材料达到训练公开及以上层级，许可归入互惠、宽松或零义务。仍需查看具体 L、O 与验证范围。','低完整-高开放':'许可较开放，但材料归入部署或理解层级。使用权利与完整训练材料，并非同一件事。','高完整-低开放':'材料达到训练公开及以上层级，同时存在实质性许可限制，需核对具体使用目的。','低完整-低开放':'材料归入部署或理解层级，且存在实质性许可限制；两方面条件都需具体检查。'};
  b+=wrap(detail[selected.name],826,234,405,18,c.muted,30)+line(826,345,1240,345,c.line)+txt(826,378,'高开放模型中，同时高完整',15,c.muted)+txt(826,420,pct(hh,hiO),32,c.brand)+txt(1240,417,`${hh} / ${hiO}`,18,c.muted,'end');
  b+=box(18,469,1244,80,c.paper,c.line,6)+txt(35,499,'读图提醒',16,c.ink)+wrap(s.sample==='report'?'“高”是报告分组口径。原870模型身份清单未取得，不生成20格细分或具体模型名单。':'补充样本可在第三幅图逐项查证；884与870未对齐身份，二者相差14不表示净增长14个模型。',160,499,1072,16,c.muted,26);return {b,rows:rows.map(r=>({记录类型:s.sample==='report'?'870报告汇总':'884平台快照',提取日期:s.sample==='report'?'2026-09-14':'2026-10-17',分类:r.name,模型数:r.n,分母:n,占比_pct:r.n/n*100}))};
 }
 function openness(p,s){
  const controls=seg('view',[['overview','分级全貌'],['learn','读懂分级'],['sample','样本全景']],s.view)+(s.view==='sample'?seg('sample',[['report','报告 870'],['current','补充 884']],s.sample):'<span class="s53-caption">点选分级，读懂材料与许可</span>');
  const result=s.view!=='sample'?{b:s.view==='overview'?overview(s):learn(s),rows:LS.flatMap(l=>OS.map(o=>({记录类型:'规范释义_非模型统计',完整性:l.id,完整性名称:l.label,许可开放性:o.id,开放性名称:o.label,材料要求:l.detail,验证:l.verify,许可条件:o.detail,依据版本:R.standard.version_note})))}:sample(s);
  paint(p,controls,result.b,s.view!=='sample'?'SJ/T 12304—2026 · 工信部2026年第22号公告发布 · 2026-12-01实施。分级关注材料与许可；教学例另标模拟。':'高完整：L3—L5；高开放：O2—O4。当前两个样本独立保留，非同一群体的前后变化。',result.rows,standardSource()+sources(['quadrants'],'原报告候选来自年度每周点赞增量Top100，经去重并保留官方基座/官方衍生，排除第三方改包及基础材料不足者；精确年窗与870身份清单待补。884为单独平台补充记录，未按本规范重新判级。'));
 }
 function regions(p,s){
  if(s.mode==='map')return regionMap(p,s);
  const c=C(),rows=D.openRegions.filter(r=>s.regions.includes(r.group));if(!rows.some(r=>r.group===s.region))s.region=rows[0].group;const selected=rows.find(r=>r.group===s.region),mx=s.mode==='share'?100:Math.max(...rows.map(r=>r.n)),px=161,w=604;
  let controls=seg('mode',[['map','地图'],['share','比例'],['count','数量']],s.mode)+`<div class="s53-region-picks" aria-label="选择比较地域">${D.openRegions.map(r=>btn('regionToggle',r.group,r.group,s.regions.includes(r.group))).join('')}${btn('allRegions','','全部')}</div>`;
  let b=txt(22,29,'开放条件的差异，与完整交付的差异分别观察',21,c.ink)+txt(1258,29,`当前展示 ${rows.length} 组 · 报告样本 870`,14,c.muted,'end');
  for(let i=0;i<=4;i++){let x=px+i*w/4;b+=line(x,80,x,450,c.line,1,'stroke-dasharray="3 5"')+txt(x,68,fmt(mx*i/4,0)+(s.mode==='share'?'%':''),13,c.muted,'middle');}
  rows.forEach((r,i)=>{const y=98+i*(340/Math.max(rows.length,4));b+=action('region',r.group,r.group,box(18,y-9,767,66,s.region===r.group?c.paper:c.bg,s.region===r.group?c.line:'none',5)+txt(31,y+16,r.group,19,s.region===r.group?c.brand:c.ink)+txt(31,y+41,'n = '+r.n,14,c.muted));let x=px;Q.forEach((q,j)=>{let v=r[q],width=(s.mode==='share'?v/r.n*100:v)/mx*w;b+=action('regionPart',r.group+'|'+q,`${r.group} ${q}：${v}个，${pct(v,r.n)}`,box(x,y+2,width,36,qcolor(j),'none',0)+(width>56?txt(x+width/2,y+26,s.mode==='share'?pct(v,r.n):String(v),14,c.bg,'middle','font-weight="600"'):''));x+=width;});});
  b+=box(810,65,452,386,c.paper,c.line,8)+txt(834,99,'所选地域 · 点击条形查看分类',14,c.muted)+txt(834,143,selected.group,28,c.brand)+txt(1238,143,'n = '+selected.n,17,c.muted,'end');
  const measures=[['高开放',selected.high_open,'O2—O4'],['高完整且高开放',selected[Q[0]],'L3—L5 且 O2—O4']];measures.forEach(([label,n,scope],i)=>{let y=189+i*82;b+=txt(834,y,label,17,c.ink)+txt(834,y+27,scope,13,c.muted)+txt(1238,y+6,pct(n,selected.n),29,i?P()[0]:P()[2],'end')+txt(1238,y+30,n+' 个',14,c.muted,'end');});
  b+=line(834,327,1238,327,c.line)+txt(834,357,s.quad.replace('-',' · '),17,qcolor(Q.indexOf(s.quad)))+txt(1238,357,`${selected[s.quad]} 个 · ${pct(selected[s.quad],selected.n)}`,18,c.ink,'end')+wrap('比例分母为本组样本；地域归属不表示研发、使用或贡献全部发生在当地。',834,393,400,15,c.muted,24);
  Q.forEach((q,i)=>{let x=25+i*306;b+=box(x,475,10,10,qcolor(i),'none',2)+txt(x+19,486,q.replace('-',' · '),15,c.muted);});
  b+=txt(25,529,'中 / 美 / 欧双高比例：13.9% / 13.2% / 13.6%　·　规模与比例均需结合样本覆盖阅读。',17,c.ink);
  paint(p,controls,b,'可点选2—3个地域比较，未知归属保留在870总样本中；仅比较报告样本，不外推地域总体。',rows.map(r=>({记录类型:'870报告分组',提取日期:'2026-09-14',地域:r.group,本组样本数:r.n,...Object.fromEntries(Q.flatMap(q=>[[q+'_数',r[q]],[q+'_pct',r[q]/r.n*100]])),高开放_pct:r.high_open/r.n*100})),sources(['openRegions'],'五组样本互斥合计870；各比例用本组n计算，原组数不随图面筛选改变。图中的高完整/高开放是报告分组，欧洲不自动解释为欧盟；成员范围与原报告精确统计年窗待补。地区与发布主体仅有各自边际汇总，不提供未经支持的交叉筛选。'));
 }
 function publishers(s){
  const c=C(),rows=D.openPublishers,selected=rows.find(r=>r.publisher_type===s.publisher)||rows[0],mode=s.metric,high=mode==='high_open',den=high?600:117;
  let b=txt(22,29,'供给规模与组内开放比例，放在一起阅读',21,c.ink)+txt(1258,29,'870 个报告模型 · 按发布主体类型分组',14,c.muted,'end');
  b+=txt(189,72,'模型数量',17,c.ink)+txt(759,72,high?'高开放比例 · O2—O4':'双高比例 · L3—L5 且 O2—O4',17,c.ink);
  [0,200,400,600,800].forEach(v=>{let x=189+v/800*475;b+=line(x,95,x,430,c.line,1,'stroke-dasharray="3 5"')+txt(x,94,v,12,c.muted,'middle');});
  [0,25,50,75,100].forEach(v=>{let x=759+v/100*366;b+=line(x,95,x,430,c.line,1,'stroke-dasharray="3 5"')+txt(x,94,v+'%',12,c.muted,'middle');});
  rows.forEach((r,i)=>{const y=129+i*83,on=s.publisher===r.publisher_type,rate=r[mode]/r.models*100;b+=action('publisher',r.publisher_type,r.publisher_type,box(18,y-20,1244,71,on?c.paper:c.bg,on?c.line:'none',5)+txt(31,y+8,r.publisher_type==='非营利组织和高校'?'非营利组织 / 高校':r.publisher_type,18,on?c.brand:c.ink)+txt(31,y+32,r.organizations+' 个发布主体',13,c.muted)+box(189,y-1,r.models/800*475,25,c.brand,'none',3)+txt(202+r.models/800*475,y+19,r.models+'',20,c.ink)+box(759,y-1,rate/100*366,25,high?P()[2]:P()[0],'none',3)+txt(1240,y+16,pct(r[mode],r.models),23,high?P()[2]:P()[0],'end')+txt(1240,y+37,r[mode]+' / '+r.models,13,c.muted,'end'));});
  b+=box(18,462,1244,87,c.paper,c.line,7)+txt(35,490,'所选主体 · '+selected.publisher_type,17,c.ink)+txt(35,524,`占全部供给 ${pct(selected.models,870)}`,18,c.brand)+txt(465,490,high?'占全部高开放模型':'占全部双高模型',15,c.muted)+txt(465,527,pct(selected[mode],den),30,high?P()[2]:P()[0])+txt(608,526,`${selected[mode]} / ${den}`,16,c.muted)+wrap('组内比例与全体贡献不同。企业双高比例为9.7%，但提供全体双高模型的59.0%。',836,490,400,16,c.muted,26);
  return {b,rows:rows.map(r=>({记录类型:'870报告发布主体',提取日期:'2026-09-14',主体类型:r.publisher_type,模型数:r.models,发布主体数:r.organizations,高开放数:r.high_open,高开放组内_pct:r.high_open/r.models*100,双高数:r.double_high,双高组内_pct:r.double_high/r.models*100,全部双高贡献_pct:r.double_high/117*100}))};
 }
 function matches(s){
  let rows=s.pool==='cases'?[...cases.values()].map(m=>({model_id:m.model_id,story_org:m.publisher,display_name:m.title,case:true})):[...models.values()];
  if(s.pool==='joined')rows=rows.filter(m=>R.modelrank.rows[m.model_id]);
  if(s.pool==='review')rows=rows.filter(m=>m.license_evidence_differs_from_grade);
  const q=s.query.trim().toLowerCase();if(q)rows=rows.filter(m=>[m.model_id,m.story_org,m.country,m.strict_final_grade].join(' ').toLowerCase().includes(q));
  return rows.sort((a,b)=>(R.modelrank.rows[a.model_id]?.rank??10000)-(R.modelrank.rows[b.model_id]?.rank??10000)||a.model_id.localeCompare(b.model_id));
 }
 function rankChart(id){
  const c=C(),x=948,w=292,px=x+35,py=244,pw=238,ph=180,rank=R.modelrank.rows[id],hist=R.modelrank.history[id]||{},months=R.modelrank.months,pts=months.map(m=>hist[m]||null);
  let b=txt(x,104,'ModelRank · 独立观察',16,c.ink)+txt(x,132,'2026-08 月榜 · Top 100',14,c.muted)+txt(x,182,rank?'# '+rank.rank:'未被该月 Top 100 覆盖',rank?37:19,rank?c.brand:c.muted);
  b+=txt(x,212,'近12个月位次 · 越靠上位次越高',13,c.muted);
  [1,25,50,75,100].forEach(v=>{let y=py+(v-1)/99*ph;b+=line(px,y,px+pw,y,c.line)+txt(px-9,y+4,String(v),12,c.muted,'end');});
  const xx=i=>px+i*pw/(months.length-1),yy=v=>py+(v-1)/99*ph;let path='',active=false;
  pts.forEach((p,i)=>{if(!p){active=false;return;}path+=(active?'L':'M')+xx(i)+','+yy(p.rank);active=true;});
  b+=`<path d="${path}" fill="none" stroke="${c.brand}" stroke-width="2.4"/>`;
  pts.forEach((p,i)=>{if(p)b+=`<circle cx="${xx(i)}" cy="${yy(p.rank)}" r="3.6" fill="${c.brand}"><title>${months[i]} · 第${p.rank}名</title></circle>`;else b+=txt(xx(i),444,'·',17,c.unknown,'middle');});
  [0,3,6,9,11].forEach(i=>b+=txt(xx(i),465,months[i].slice(2),12,c.muted,'middle'));
  if(!pts.some(Boolean))b+=box(px+5,310,pw-10,64,c.paper,'none',4)+txt(px+pw/2,338,'已存月榜暂无此模型',16,c.muted,'middle')+txt(px+pw/2,361,'不补为 0 或第 101 名',14,c.muted,'middle');
  b+=wrap('断线或底部点：该月Top 100未覆盖。不是首次发布或退出生态的判断。',x,497,w,14,c.muted,23);return b;
 }
 let evidence=null,evidencePromise=null,evidenceError=false;
 function loadEvidence(p){if(evidence||evidencePromise||evidenceError)return;evidencePromise=fetch(asset('openness-evidence-884.json')).then(r=>{if(!r.ok)throw new Error('evidence');return r.json();}).then(d=>{evidence=new Map(d.models.map(m=>[m.model_id,m]));if(p.isConnected&&H.state(p).detail){const focus=p.querySelector('.s53-evidence-sheet')?.contains(document.activeElement);H.draw(p);if(focus)p.querySelector('[data-gm-action=closeEvidence]')?.focus();}}).catch(()=>{evidenceError=true;if(p.isConnected&&H.state(p).detail){const focus=p.querySelector('.s53-evidence-sheet')?.contains(document.activeElement);H.draw(p);if(focus)p.querySelector('[data-gm-action=closeEvidence]')?.focus();}});}
 function urls(e){try{const a=typeof e?.urls==='string'?JSON.parse(e.urls):e?.urls||[];return a.filter(safe);}catch{return [];}}
 const status={complete:'源站：完整',partial:'源站：部分',missing:'源站：缺失'};
 function modelBody(s,rows){
  const c=C(),pages=Math.max(1,Math.ceil(rows.length/8));s.page=Math.min(s.page,pages-1);let b=box(18,50,300,499,c.paper,c.line,7)+box(334,50,592,499,c.paper,c.line,7)+box(942,50,320,499,c.paper,c.line,7);
  b+=txt(33,80,`${rows.length} 个匹配对象`,17,c.ink)+txt(302,80,s.pool==='cases'?'独立核验':'源站分级',13,c.muted,'end');
  rows.slice(s.page*8,s.page*8+8).forEach((m,i)=>{const y=108+i*46,rank=R.modelrank.rows[m.model_id];b+=action('model',m.model_id,m.model_id,box(26,y-18,284,43,s.model===m.model_id?c.raised:c.paper,s.model===m.model_id?c.brand:'none',4)+txt(35,y,trim(m.display_name||m.model_id.split('/').at(-1),29),14,s.model===m.model_id?c.brand:c.ink)+txt(35,y+17,trim(m.story_org,21),12,c.muted)+txt(299,y+17,rank?'#'+rank.rank:s.pool==='cases'?'固定版本':m.strict_final_grade,12,c.muted,'end'));});
  if(!rows.length)b+=txt(35,131,'没有匹配模型，请调整搜索。',16,c.muted);
  b+=sb('modelPage','prev','←',33,502,40,false,s.page===0)+txt(168,523,`${s.page+1} / ${pages}`,14,c.muted,'middle')+sb('modelPage','next','→',263,502,40,false,s.page===pages-1);
  let m=rows.find(m=>m.model_id===s.model);if(!m){m=rows[0];s.model=m?.model_id||'';}if(!m)return {b:b+txt(362,108,'先选择模型',23,c.muted),monthly:[]};
  const id=m.model_id,cm=cases.get(id),om=models.get(id),isCase=s.pool==='cases',grade=om?.strict_final_grade;
  b+=txt(22,29,isCase?'固定提交的独立案例 · 4 个目的性案例':'平台开放证据 · 2026-10-17 快照 · 严格模式',19,c.ink)+txt(1258,29,'影响力月份与开放快照分别标注',13,c.muted,'end');
  b+=txt(355,80,trim(id,52),18,c.ink)+txt(355,115,isCase?'独立材料核验':`源站等级  ${grade||'未覆盖'}`,24,c.brand)+txt(905,113,isCase?cm.revision.slice(0,9):trim(countryName(m.country),23),14,c.muted,'end');
  if(isCase){
   b+=wrap(cm.summary,355,149,548,16,c.muted,23);
   Object.entries(cm.fields).forEach(([key,f],i)=>{const y=203+i*43;b+=action('evidence',key,D.cases.field_labels[key],box(351,y-20,557,38,c.bg,c.line,4)+txt(363,y+3,D.cases.field_labels[key],16,c.ink)+txt(893,y+3,f.status==='unknown'?'待核实 · '+trim(f.label,19):trim(f.label,23),14,f.status==='unknown'?c.gold:c.brand,'end'));});
   b+=txt(355,482,'已观察仅表示看到了具体材料，不授予 L/O 等级。',14,c.muted)+`<a href="${esc(cm.fixed_card_url)}" target="_blank" rel="noopener">${txt(355,528,'固定版本模型卡 ↗',15,c.brand)}</a>`;
  }else{
   const warning=om?.license_evidence_differs_from_grade;b+=txt(355,149,warning?'许可字段与源等级不一致 · 待复核':'源站判断保留原值 · 点选材料查看证据',15,warning?c.gold:c.muted);
   [...LS.map(l=>[l.id,l.id+' '+l.short]),['license','许可']].forEach(([key,label],i)=>b+=sb('level',key,label,354+i*93,171,86,s.level===key));
   const fields=s.level==='license'?D.method.license_fields:D.method.completeness_levels.find(l=>l.id===s.level).indicators;
   fields.forEach((f,i)=>{const y=242+i*43,v=R.indicators[id]?.[f.id];b+=action('evidence',f.id,f.label,box(351,y-23,557,38,c.bg,c.line,4)+txt(363,y+1,f.label,16,c.ink)+txt(893,y+1,s.level==='license'?'查看源字段与解释 →':status[v]||'源站：未记录',14,v==='complete'?c.brand:v==='partial'?c.gold:c.muted,'end'));});
   const tail=s.level==='license'?'许可字段是源站资质判断，complete不等于许可文件存在；需查看原值、说明及具体许可。':LS.find(l=>l.id===s.level).verify;
   b+=wrap(tail,355,475,548,15,c.muted,23)+`<a href="${esc(om.official_url)}" target="_blank" rel="noopener">${txt(355,528,'模型卡 ↗',15,c.brand)}</a>`+txt(905,528,'材料记录不等于独立运行验证',13,c.muted,'end');
  }
  b+=rankChart(id);return {b,monthly:R.modelrank.months.map(month=>({记录类型:'所选模型月榜覆盖',模型ID:id,月份:month,位次:R.modelrank.history[id]?.[month]?.rank??'',覆盖状态:R.modelrank.history[id]?.[month]?'在Top100内':'Top100未覆盖'}))};
 }
 function evidenceSheet(p,s){
  if(!s.detail)return;const cm=cases.get(s.model),isCase=s.pool==='cases',om=models.get(s.model),entry=isCase?cm?.fields[s.field]:evidence?.get(s.model)?.evidence[s.field],field=D.method.completeness_levels.flatMap(l=>l.indicators).concat(D.method.license_fields).find(f=>f.id===s.field),label=isCase?D.cases.field_labels[s.field]:field?.label||s.field;
  const links=isCase?entry?.sources||[]:urls(entry),raw=entry?.raw_value??R.indicators[s.model]?.[s.field];
  let body=isCase?`<p><strong>${esc(entry.label)}</strong></p><p>${esc(entry.detail)}</p><p class="s53-evidence-note">核验：${cm.checked_at} · 固定提交 ${cm.revision}</p>`:!evidence?`<p>${evidenceError?'暂时未载入逐项说明，可下载完整证据记录。':'正在载入平台逐项证据…'}</p>`:`<p><strong>源字段原值：${esc(raw??'未提供')}</strong></p><p>${esc(entry?.explanation||'源站未附该字段的文字说明。')}</p><p class="s53-evidence-note">${s.field.includes('license')?'许可资质字段不能按“完整/部分/缺失”解释为许可文件是否存在。请核对原值与许可文本。':'保留源站材料判断；来源链接仅是查证入口，不表示已经完成独立运行验证。'} ${om?.license_evidence_differs_from_grade?'此模型存在许可字段与源等级不一致的线索，待复核。':''}</p>`;
  body+=links.length?'<ol class="s53-evidence-links">'+links.map(u=>`<li>${link(u,u)}</li>`).join('')+'</ol>':'<p>本项未提供可重建的直接来源链接，请结合完整档案继续核对。</p>';
  const host=document.createElement('section');host.className='s53-evidence-sheet';host.setAttribute('role','region');host.setAttribute('aria-label','所选材料证据');host.innerHTML=`<div class="s53-sheet-head"><div><span>逐项证据 · ${esc(s.model)}</span><h4>${esc(label)}</h4></div>${btn('closeEvidence','','关闭 ×')}</div>${body}<p>${link(asset(isCase?'cases.json':'openness-evidence-884.json'),'下载完整证据记录')}</p>`;p.querySelector('.gm-view').append(host);
 }
 function dossiers(p,s){
  if(s.view==='map')return publisherGeo(p,s);
  let controls=seg('view',[['map','主体地图'],['publishers','主体比较'],['models','模型与证据']],s.view),result;
  if(s.view==='publishers'){controls+=seg('metric',[['double_high','高完整且高开放'],['high_open','高开放']],s.metric);result=publishers(s);}
  else{
   const options=[['platform','平台记录 · 884'],['joined','榜单交集 · 38'],['cases','固定案例 · 4'],['review','许可待复核 · 22']];controls+=`<label class="s53-select">范围<select data-s53-pool aria-label="模型记录范围">${options.map(([v,l])=>`<option value="${v}" ${s.pool===v?'selected':''}>${l}</option>`).join('')}</select></label><input type="search" data-s53-search placeholder="搜索模型、发布者或等级" aria-label="搜索模型、发布者或等级" value="${esc(s.query)}">`;
   const rows=matches(s),r=modelBody(s,rows);result={b:r.b,rows:[...rows.map(m=>({记录类型:s.pool==='cases'?'独立固定版本案例':'884平台快照',模型ID:m.model_id,开放快照:'2026-10-17',源站完整性:s.pool==='cases'?'':m.strict_completeness_level,源站开放性:s.pool==='cases'?'':m.openness_level,源站等级:s.pool==='cases'?'':m.strict_final_grade,许可字段待复核:s.pool==='cases'?'':m.license_evidence_differs_from_grade?'是':'否',榜单月份:'2026-08',ModelRank位次:R.modelrank.rows[m.model_id]?.rank??'',月榜覆盖:R.modelrank.rows[m.model_id]?'Top100已覆盖':'Top100未覆盖'})),...r.monthly]};
  }
  paint(p,controls,result.b,s.view==='publishers'?'数量按模型计；组内比例与全体贡献分别计算。发布主体类型沿用原报告，非随机抽样。':'884平台记录、4个固定案例、月榜分别呈现。38为完整ID交集；日期与提交未完全对齐，不据此推断因果。',result.rows,sources(['openPublishers'],'发布主体表只有模型数、高开放数与双高数，不据此拼造四象限交叉表。企业69个双高占117个双高模型的59.0%。')+`<p>模型档案：${link(asset('openness-current.json'),'884补充记录')} · ${link(asset('openness-evidence-884.json'),'逐项材料与许可')} · ${link(asset('cases.json'),'4个固定版本案例')}。22条源站记录许可字段与最终等级不一致，仅标为待复核；材料状态沿用源站，未逐条重新评估。</p><p>ModelRank：${link(R.modelrank.source_url,'2026-08 Top100来源')}；读取于2026-10-17。使用已保存的月榜快照。按完整模型ID精确关联，38条交集；不做模型家族、大小写或别名模糊匹配。12个月覆盖2025-09—2026-08，各月Top100之外不补位次；曲线以位次为主，不把跨月归一化分数当作增长率。开放与影响力时间不同，不能计算因果或未经控制的总体相关性。</p>`);
  if(s.view==='models'&&s.detail){if(s.pool!=='cases')loadEvidence(p);evidenceSheet(p,s);}
 }
 function handle(p,s,k,v){
  if(!own(p))return false;
  const id=p.dataset.gmChart;
  if(k==='view'){s.view=v;s.detail=false;}
  else if(id==='openness'){
   if(k==='standardDetails'){p.s53StandardLevel=v;}else if(k==='overviewLevel'){s.l=+v;s.overviewDetail='materials';}else if(k==='overviewO'){s.o=+v;s.overviewDetail='license';}else if(k==='overviewDetail')s.overviewDetail=v;else if(k==='cell'){[s.l,s.o]=v.split('|').map(Number);s.demo='';}else if(k==='l'||k==='o'){s[k]=+v;s.demo='';}else if(k==='sample')s.sample=v;else if(k==='quad')s.quad=v;else if(k==='demo'){s.demo=v==='reset'?'':v;s.l=v==='materials'||v==='license'?3:2;s.o=v==='license'?1:3;}else return false;
  }else if(id==='open-groups'){
   if(k==='mapCountry')s.mapCountry=v;else if(k==='mapClear')s.mapCountry='';else if(k==='mapPage')s.mapPage=Math.max(0,s.mapPage+(v==='next'?1:-1));else if(k==='mode')s.mode=v;else if(k==='region')s.region=v;else if(k==='regionPart')[s.region,s.quad]=v.split('|');else if(k==='allRegions')s.regions=D.openRegions.map(r=>r.group);else if(k==='regionToggle'){if(s.regions.includes(v)){if(s.regions.length>1)s.regions=s.regions.filter(x=>x!==v);}else s.regions.push(v);}else return false;
  }else{
   if(k==='mapType'){s.mapType=v;s.pubPage=0;s.pubSelected='';}else if(k==='mapCountry'){s.pubCountry=v;s.pubPage=0;s.pubSelected='';}else if(k==='mapClear'){s.pubCountry='';s.pubPage=0;s.pubSelected='';}else if(k==='pubUnknown'){s.pubCountry='unknown';s.pubPage=0;s.pubSelected='';}else if(k==='publisherSelect')s.pubSelected=v;else if(k==='pubPage')s.pubPage=Math.max(0,s.pubPage+(v==='next'?1:-1));else if(k==='metric')s.metric=v;else if(k==='publisher')s.publisher=v;else if(k==='model'){s.model=v;s.detail=false;}else if(k==='modelPage'){s.page=Math.max(0,s.page+(v==='next'?1:-1));s.detail=false;}else if(k==='level'){s.level=v;s.detail=false;}else if(k==='evidence'){s.field=v;s.detail=true;}else if(k==='closeEvidence')s.detail=false;else return false;
  }return true;
 }
 function input(p,s,e){if(!own(p)||!e.target.hasAttribute('data-s53-search'))return false;const cursor=e.target.selectionStart;s.query=e.target.value;s.page=0;s.detail=false;H.draw(p);const input=p.querySelector('[data-s53-search]');input?.focus();try{input?.setSelectionRange(cursor,cursor);}catch{}return true;}
 function change(p,s,e){if(!own(p))return false;if(e.target.hasAttribute('data-s53-map-metric')){s.mapMetric=e.target.value;s.mapPage=0;return true;}if(!e.target.hasAttribute('data-s53-pool'))return false;s.pool=e.target.value;s.page=0;s.query='';s.detail=false;return true;}
 const stamp=(p,s)=>p.dataset.gmChart==='openness'?(s.view!=='sample'?'SJ/T 12304-2026 · 工信部2026年第22号公告；2026-12-01实施':s.sample==='report'?'870原评估 · 2026-09-14提取':'884平台补充 · 2026-10-17'):p.dataset.gmChart==='open-groups'?(s.mode==='map'?'884平台补充 · 国家逐条汇总 · 2026-10-17':'870原评估 · 地域组内分母 · 2026-09-14'):s.view==='map'?'884平台补充 · 主体国家示意 · 2026-10-17':s.view==='publishers'?'870原评估 · 组内比例与全体贡献 · 2026-09-14':'开放2026-10-17 / ModelRank 2026-08 Top100；完整ID关联';
 return {defaults,own,handle,input,change,stamp,renderers:{openness,'open-groups':regions,dossiers},matches,allCountries,typeDefs,codeOf};
};
