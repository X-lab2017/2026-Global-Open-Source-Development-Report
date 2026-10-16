/* A-Map review v3: three independent, single-screen explorations. */
(() => {
'use strict';
const D=window.GOSD_AMAP, root=document.querySelector('.amap-review');
if(!D||!root||!window.d3)return;
const BASE=document.querySelector('meta[name="gosd-base"]')?.content||'';
const $=s=>document.querySelector(s), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=n=>Number(n).toLocaleString('zh-CN'), short=n=>n>=1e8?(n/1e8).toFixed(n>=1e10?0:1)+'亿':n>=1e4?(n/1e4).toFixed(n>=1e6?1:2)+'万':num(Math.round(n));
const C=['#156993','#007D87','#856AA5','#B67936','#4A83A5','#58745E','#A15F72','#607B98','#8A8163','#577B78','#8481A1','#75685D'];
const uncertain=s=>['simulated','forecast','image_estimate','scenario'].includes(s);
const badge=s=>`<span class="am-badge ${uncertain(s)?'forecast':''}">${D.statusLabels[s]||esc(s)}</span>`;
const S={world:'code',growth:'overview',structure:'code',mock:true,country:'CN',page:0,year:2026,gmode:'small',log:false,platform:'GitHub',smode:'tree',metric:'count',syear:2026,group:'',selected:''};
const mainLabel={code:'代码仓库',models:'模型仓库',datasets:'数据仓库',commits:'代码提交'};
function setFoot(k,t){$('#am-'+k+'-foot').textContent=t;}
function buttons(key,items,value){return items.map(([v,t])=>`<button data-am-${key}="${v}" aria-pressed="${v===value}">${t}</button>`).join('');}
function years(key,value){return `<label>年份 <select data-am-${key} aria-label="年份">${D.years.map(y=>`<option value="${y}" ${y===value?'selected':''}>${y}</option>`).join('')}</select></label>`;}
const point=(v,y)=>v.find(p=>p.year===y);
function line(series,{w=830,h=315,small=false,log=false,index=false,selected='',year=0,click='growth',labels=false}={}){
 const pad={l:small?54:66,r:28,t:22,b:32}, iw=w-pad.l-pad.r, ih=h-pad.t-pad.b;
 const values=series.flatMap(s=>s.series.map(p=>p.value)); let max=Math.max(...values,1),min=0;
 if(log)min=Math.pow(10,Math.floor(Math.log10(Math.min(...values.filter(v=>v>0)))));
 const step=window.d3.tickStep(0,max,4),ymax=log?Math.pow(10,Math.ceil(Math.log10(max))):Math.ceil(max/step)*step;
 const xx=y=>pad.l+(y-2022)/4*iw, yy=v=>pad.t+ih*(1-(log?(Math.log10(Math.max(min,v))-Math.log10(min))/(Math.log10(ymax)-Math.log10(min)) : v/ymax));
 const ticks=log?Array.from({length:Math.round(Math.log10(ymax/min))+1},(_,i)=>min*10**i):window.d3.ticks(0,ymax,4);
 let o=`<svg class="am-line ${small?'am-small-line':''}" viewBox="0 0 ${w} ${h}" role="group" aria-label="2022 至 2026 年趋势，虚线和空心点表示模拟、近似或预测"><title>${series.map(s=>s.label).join('、')}：五年趋势</title>`;
 for(const t of ticks)o+=`<path class="am-axis" d="M${pad.l},${yy(t)}H${w-pad.r}"/><text x="${pad.l-9}" y="${yy(t)+5}" text-anchor="end" style="font-size:${small?11:13}px">${index?Math.round(t):short(t)}</text>`;
 for(const y of D.years)o+=`<text x="${xx(y)}" y="${h-9}" text-anchor="middle" style="font-size:${small?12:14}px">${y}</text>`;
 if(year)o+=`<path d="M${xx(year)},${pad.t}V${h-pad.b}" stroke="var(--am-line)" stroke-dasharray="3 5"/>`;
 series.forEach((s,j)=>{
  const color=s.color||C[j%C.length],fade=selected&&selected!==s.id;
  o+=`<g opacity="${fade?.24:1}">`;
  s.series.slice(1).forEach((p,i)=>{const a=s.series[i];o+=`<path d="M${xx(a.year)},${yy(a.value)}L${xx(p.year)},${yy(p.value)}" fill="none" stroke="${['forecast','scenario'].includes(p.status)?'#B98628':color}" stroke-width="${small?2.2:3}" ${uncertain(p.status)||uncertain(a.status)?'stroke-dasharray="6 5"':''}/>`;});
  s.series.forEach(p=>{const warning=uncertain(p.status),a=click==='structure'?`data-am-category="${esc(s.id)}" data-am-pointyear="${p.year}"`:`data-am-yearpoint="${p.year}" data-am-platformpoint="${esc(s.id)}"`;
   o+=`<circle class="am-chart-button" ${click==='none'?'':a} cx="${xx(p.year)}" cy="${yy(p.value)}" r="${small?3.5:year===p.year?6.5:4.5}" fill="${warning?'var(--am-surface)':color}" stroke="${['forecast','scenario'].includes(p.status)?'#B98628':color}" stroke-width="2" ${click==='none'?'':'tabindex="0" role="button"'} aria-label="${esc(s.label)} ${p.year}：${num(p.value)}，${D.statusLabels[p.status]}"><title>${esc(s.label)} · ${p.year}：${num(p.value)} · ${D.statusLabels[p.status]}</title></circle>`;
   if(labels)o+=`<text x="${xx(p.year)}" y="${yy(p.value)-13}" text-anchor="middle" class="am-value" style="font-size:14px">${short(p.value)}</text>`;
  });o+='</g>';
 });return o+'</svg>';
}
const statusLegend=()=>'<div class="am-status-legend"><span>● 实心 / 实线：来源记录</span><span>◌ 空心 / 虚线：模拟或近似</span><span class="am-gold">◌ 金色：预测 / 情景</span></div>';
function renderWorld(){
 const k=S.world,g=D.geography[k],all=g.records.slice().sort((a,b)=>b.value-a.value),rows=all.filter(r=>S.mock||!uncertain(r.status)),rec=rows.find(r=>r.id===S.country),max=Math.max(...all.map(r=>r.value)),pages=Math.max(1,Math.ceil(rows.length/6));S.page=Math.min(S.page,pages-1);
 const colors=k==='code'?['#DCEBF2','#156993']:k==='models'?['#D8EEEC','#007D87']:['#EEE5F2','#856AA5'];const color=window.d3.scaleSequential(window.d3.interpolateRgb(...colors)).domain([0,Math.log10(max+1)]);
 const map=`<svg class="am-map" viewBox="0 0 880 470" role="group" aria-label="${mainLabel[k]}全球分布，${S.mock?'含模拟补齐':'仅显示已提供数据'}"><title>全球${mainLabel[k]}地图：中国包含台湾省；国家归属按供应方样本观察。</title><defs><pattern id="am-map-hatch" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0,5L5,0" stroke="#86651B" stroke-width=".55" opacity=".45"/></pattern></defs>${D.world.map(f=>{const r=rows.find(q=>q.id===f.id),st=r?.status;return `<g><path d="${f.d}" fill="${r?color(Math.log10(r.value+1)):'var(--am-empty)'}" ${r?`data-am-country="${f.id}" tabindex="0" role="button" aria-pressed="${f.id===S.country}" aria-label="${esc(r.name)}，${num(r.value)}，${D.statusLabels[st]}"`:''}><title>${esc(f.name)}：${r?num(r.value)+' · '+D.statusLabels[st]:'暂无已提供数据'}</title></path>${r&&uncertain(st)?`<path d="${f.d}" fill="url(#am-map-hatch)" pointer-events="none"/>`:''}</g>`;}).join('')}</svg>`;
 const warning=k==='code'?'模拟分布 · 国家数量尚无底表，不代表实测地理格局。':'原稿前 14 国读数 + 其余地区模拟补齐；仅代表 826 家发布单位样本。';
 $('#am-world').innerHTML=`<div class="am-split"><div class="am-main"><div class="am-controls">${buttons('mock',[['yes','含模拟补齐'],['no','仅看已提供数据']],S.mock?'yes':'no')}<label class="am-push">定位 <select data-am-location aria-label="定位国家"><option value="">选择国家</option>${rows.map(r=>`<option value="${r.id}" ${r.id===S.country?'selected':''}>${esc(r.name)}${uncertain(r.status)?' · 模拟':''}</option>`).join('')}</select></label></div><div class="am-evidence">${warning}</div>${map}<div class="am-map-key"><span>少</span><i style="background:linear-gradient(90deg,${colors.join(',')})"></i><span>多 · 对数色阶</span><span class="am-hatch-key"></span><span>斜纹＝模拟</span><em></em><span>暂无数据</span></div><div class="am-stat-strip"><div><small>${k==='code'?'GitHub 活跃仓库总数':'原稿组织样本总数'}</small><b>${num(g.total)}</b></div><div><small>已提供国家读数</small><b>${num(g.observed_sum)}</b></div><div><small>模拟分配${!S.mock?' · 已隐藏':''}</small><b>${num(g.simulated_sum)}</b></div>${g.unallocated?`<div><small>未分配</small><b>${num(g.unallocated)}</b></div>`:''}</div></div><aside class="am-side"><div class="am-readout"><span>${g.period}</span><h5>${rec?esc(rec.name):'国家归属待补'}</h5><strong class="am-big">${rec?short(rec.value):'—'}</strong>${rec?badge(rec.status):'<span class="am-badge forecast">无国家原表</span>'}<p class="am-quiet">${rec?'占当前样本 '+(100*rec.value/g.total).toFixed(2)+'% · '+num(rec.value)+' 个':S.mock?'在地图或列表中选择国家。':'切换“含模拟补齐”可查看设计演示。'}</p></div><div><div class="am-subtitle"><b>国家 / 地区</b><span>${rows.length?`${S.page*6+1}—${Math.min(rows.length,(S.page+1)*6)} / ${rows.length}`:'尚无已提供记录'}</span></div><div class="am-rank">${rows.slice(S.page*6,S.page*6+6).map((r,i)=>`<button data-am-country="${r.id}" aria-pressed="${r.id===S.country}"><small>${S.page*6+i+1}</small><span>${esc(r.name)}${uncertain(r.status)?'<small> · 模拟</small>':''}</span><b>${short(r.value)}</b></button>`).join('')}</div></div><div class="am-pager"><span>点击地图或国家联动</span><button data-am-page="-1" aria-label="上一页" ${!S.page?'disabled':''}>←</button><button data-am-page="1" aria-label="下一页" ${S.page===pages-1?'disabled':''}>→</button></div><div class="am-note">${k==='code'?'代码总量来自报告原表；各国权重为设计模拟。':'国家按发布单位归属；样本总量与平台全量分开观察。'}</div></aside></div>`;
 setFoot('world',`${mainLabel[k]} · ${g.scope} · 缺失不等于零 · 地图与排名随证据开关联动`);
}
const growthMeta={
 commits:{title:'GitHub 年度代码提交',unit:'次',note:'GitHub 平台口径不限公开开源仓库。2022—2024 模拟；2026 为全年预测。',foot:'2026：预计 140 亿次，约为 2025 的 14 倍。预测不等于全年实测。'},
 code:{title:'四平台活跃代码仓库',unit:'个',note:'各平台分别计量；AtomGit 2022—2023 为模拟补齐，其他点保留报告原表。',foot:'2026 使用报告原表口径；跨平台仓库可能重复，四平台不可直接相加。'},
 models:{title:'Hugging Face 模型仓库',unit:'个',note:'同一快照中的存续仓库，按创建年份累计回溯；并非五次独立历史快照。',foot:'系列截至 2026-09-13；10-11 最新总量为 314.21 万，未拼接进该历史序列。'},
 datasets:{title:'Hugging Face 数据仓库',unit:'个',note:'2022—2025 暂用模拟序列；2026 为 10-11 接口快照值，非年终预测。',foot:'历史值待逐年快照替换；模拟曲线不构成实际历史增长证据。'}
};
const growthSeries=k=>k==='code'?D.growth.platforms[S.platform]:D.growth[k];
function growthCard(k){const v=k==='code'?D.growth.platforms.GitHub:D.growth[k],p=v[4];return `<button class="am-overview-card" data-am-open-growth="${k}"><span class="am-subtitle"><b>${k==='code'?'GitHub 活跃代码仓库':growthMeta[k].title}</b><span>展开 →</span></span><strong>${short(p.value)}<small> ${growthMeta[k].unit} · 2026</small></strong>${line([{id:k,label:mainLabel[k],series:v}],{w:540,h:137,small:true,click:'none'})}<span class="am-card-caption">${k==='code'?'点开比较 GitHub / GitLab / Gitee / AtomGit':k==='commits'?'2026 全年预测；2022—2024 模拟':k==='models'?'2026-09-13 存续快照 · 创建队列回溯':'2026-10-11 快照；2022—2025 模拟'}</span></button>`;}
function renderGrowth(){
 const k=S.growth;
 if(k==='overview'){$('#am-growth').innerHTML=`<div class="am-overview"><div class="am-evidence">四个观察窗口 · 独立纵轴 · 空心虚线为模拟或预测 · 2026 各系列截止时间不同</div><div class="am-overview-grid">${['commits','code','models','datasets'].map(growthCard).join('')}</div></div>`;setFoot('growth','2022—2026 · 代码提交是活动量，仓库是资产容器 · 点击任一卡片深入比较');return;}
 const m=growthMeta[k],v=growthSeries(k),p=point(v,S.year),prev=point(v,S.year-1),ratio=prev?(p.value/prev.value-1)*100:null;
 let controls=years('gyear',S.year),chart='';
 if(k==='code'){
  controls+=buttons('gmode',[['small','四平台分面'],['compare','同轴规模'],['index','2024 = 100']],S.gmode);
  const all=Object.entries(D.growth.platforms).map(([name,s],i)=>({id:name,label:name,series:S.gmode==='index'?s.map(p=>({...p,value:p.value/s[2].value*100})):s,color:C[i]}));
  if(S.gmode==='small')chart=`<div class="am-platform-grid">${all.map(a=>`<div class="am-platform-card ${a.id===S.platform?'selected':''}"><button data-am-platform="${a.id}"><b style="color:${a.color}">${a.label}</b><span>${short(point(a.series,S.year).value)}</span></button>${line([a],{w:400,h:155,small:true,year:S.year})}</div>`).join('')}</div>`;
  else chart=line(all,{year:S.year,selected:S.platform,index:S.gmode==='index',h:330});
 }else{
  if(k==='commits')controls+=buttons('log',[['no','线性纵轴'],['yes','对数纵轴']],S.log?'yes':'no');
  chart=line([{id:k,label:m.title,series:v}],{year:S.year,log:k==='commits'&&S.log,labels:true,h:330});
 }
 $('#am-growth').innerHTML=`<div class="am-split"><div class="am-main"><div class="am-controls">${controls}</div><div class="am-evidence">${m.note}</div>${chart}${k==='code'?`<div class="am-color-legend">${Object.keys(D.growth.platforms).map((n,i)=>`<button data-am-platform="${n}" aria-pressed="${S.platform===n}"><i style="background:${C[i]}"></i>${n}</button>`).join('')}<span>${S.gmode==='small'?'各图独立纵轴':S.gmode==='index'?'2024 年为共同基准，刻度为指数':'同一纵轴，保留绝对规模差异'}</span></div>`:''}${statusLegend()}</div><aside class="am-side"><div class="am-readout"><span>${S.year} · ${k==='code'?S.platform:m.title}</span><strong class="am-big">${short(p.value)}<small>${m.unit}</small></strong>${badge(p.status)}<p class="am-quiet">${num(p.value)} ${m.unit}</p></div><div class="am-mini"><div><small>${prev?'较上一年':'序列起点'}</small><b>${prev?(ratio>=0?'+':'')+ratio.toFixed(1)+'%':'2022'}</b></div><div><small>${k==='commits'&&S.year===2026?'相对 2025':'观察窗口'}</small><b>${k==='commits'&&S.year===2026?'14×':'5 年'}</b></div></div><div class="am-series-table">${v.map(p=>`<button data-am-yearpoint="${p.year}" aria-pressed="${S.year===p.year}"><span>${p.year}</span><b>${short(p.value)}</b><small>${D.statusLabels[p.status]}</small></button>`).join('')}</div><div class="am-note">${m.foot}${uncertain(p.status)||prev&&uncertain(prev.status)?'<br>所选增幅涉及模拟或预测，仅作演示。':''}</div></aside></div>`;
 setFoot('growth',`${m.title} · ${S.gmode==='index'&&k==='code'?'指数基准选取四平台均有原表值的 2024 年':'点击数据点查看年份与证据状态'} · 2026 不代表统一年末`);
}
function categories(){return D.categories[S.structure==='code'&&S.metric==='influence'?'codeInfluence':S.structure];}
function categoryRows(){const all=categories(),g=all.find(v=>v.id===S.group);if(!g||!g.children)return all;const total=g.children.reduce((a,b)=>a+b.value,0);return g.children.map((c,i)=>({id:g.id+'~'+i,label:c.name,series:g.series.map(p=>({year:p.year,value:p.year===2026?c.value:Math.round(p.value*c.value/total),status:p.year===2026?'source':'simulated'}))}));}
function wrap(s,n){if(/[\u4e00-\u9fff]/.test(s))return s.match(new RegExp('.{1,'+Math.max(3,n)+'}','g'))||[s];const words=s.split(/[- /]/),out=[];let row='';words.forEach(w=>{if((row+' '+w).length>n&&row){out.push(row);row=w;}else row+=(row?' ':'')+w;});if(row)out.push(row);return out;}
function tree(rows){const w=830,h=335,data=window.d3.hierarchy({children:rows.map(r=>({...r,children:undefined,value:point(r.series,S.syear).value}))}).sum(d=>d.value||0).sort((a,b)=>b.value-a.value);window.d3.treemap().size([w,h]).paddingInner(5).round(true)(data);
 return `<svg class="am-treemap" viewBox="0 0 ${w} ${h}" role="group" aria-label="${S.syear} 年类别矩形树图，矩形面积与数值成比例"><title>点击类别${S.structure==='code'?'查看趋势':'查看细分任务'}，下拉框可选择较小类别。</title>${data.leaves().map(n=>{const r=n.data,x=n.x0,y=n.y0,rw=n.x1-x,rh=n.y1-y,ix=rows.findIndex(v=>v.id===r.id),p=point(r.series,S.syear),lines=wrap(r.label,Math.floor((rw-24)/(/[\u4e00-\u9fff]/.test(r.label)?16:8))),canText=rw>76&&rh>47,room=Math.max(1,Math.floor((rh-43)/20));return `<g data-am-tile="${esc(r.id)}" class="am-chart-button" tabindex="0" role="button" aria-label="${esc(r.label)}：${num(p.value)}，${D.statusLabels[p.status]}"><title>${esc(r.label)} · ${num(p.value)} · ${D.statusLabels[p.status]}</title><rect x="${x}" y="${y}" width="${rw}" height="${rh}" rx="5" fill="${C[ix%C.length]}" stroke="${S.selected===r.id?'var(--am-gold)':'none'}" stroke-width="3"/>${canText?`<text x="${x+12}" y="${y+25}" style="fill:#fff;font-size:15px;font-weight:600">${lines.slice(0,room).map((t,i)=>`<tspan x="${x+12}" dy="${i?20:0}">${esc(t)}${i===room-1&&lines.length>room?'…':''}</tspan>`).join('')}</text>${rh>73?`<text x="${x+12}" y="${y+rh-15}" style="fill:#fff;font-size:14px">${short(p.value)}</text>`:''}`:''}</g>`;}).join('')}</svg>`;
}
function renderStructure(){
 const k=S.structure,all=categories(),rows=categoryRows();if(!rows.some(r=>r.id===S.selected))S.selected=rows[0].id;
 const r=rows.find(x=>x.id===S.selected),p=point(r.series,S.syear),group=all.find(v=>v.id===S.group),total=rows.reduce((a,r)=>a+point(r.series,S.syear).value,0),isInf=k==='code'&&S.metric==='influence',unit=isInf?'OpenRank':k==='code'?'个仓库':'条标签记录';
 const notice=k==='code'?(isInf?'图像近似 + 情景外推 · 2022—2025 为附件读图，2026 为示意延伸。':'全序列模拟 · 按主类别分配的仓库数量，等待技术类别原表替换。'):(S.syear===2026?'当期任务标签来自接口 · 多标签可重复，面积不代表去重仓库数量。':'历史类别序列为模拟 · 按当前标签结构回溯设定，待历年快照替换。');
 const chart=S.smode==='tree'?tree(rows):line(rows.map((r,i)=>({...r,color:C[i%C.length]})),{h:335,selected:S.selected,click:'structure',year:S.syear});
 $('#am-structure').innerHTML=`<div class="am-split"><div class="am-main"><div class="am-controls">${buttons('smode',[['tree','当年树图'],['trend','五年折线']],S.smode)}${years('syear',S.syear)}${k==='code'?buttons('metric',[['count','仓库数量'],['influence','OpenRank 影响力']],S.metric):''}</div><div class="am-evidence">${notice}</div><div class="am-subtitle"><div class="am-breadcrumb">${group?`<button data-am-back>← 返回全部类别</button><span>${esc(group.label)}</span>`:`<b>${isInf?'技术类别影响力':k==='code'?'技术主类别数量':'按任务标签归组'}</b><span>${rows.length} 个${group?'任务':'类别'}</span>`}</div><span>${S.smode==='tree'?'面积 = '+unit:'纵轴：'+unit}</span></div>${chart}${S.smode==='tree'&&!group?`<div class="am-tree-legend">${rows.map((r,i)=>`<button data-am-tile="${esc(r.id)}" aria-pressed="${S.selected===r.id}"><i style="background:${C[i%C.length]}"></i>${esc(r.label)}</button>`).join('')}</div>`:''}<div class="am-category-hint">${S.smode==='tree'?(k==='code'?'点击矩形查看右侧五年趋势':'点击类别进入细分任务；较小矩形也可通过右侧列表选择'):'点击图中数据点，或用右侧列表切换强调的曲线'} · ${S.syear}</div>${S.smode==='trend'?statusLegend():''}</div><aside class="am-side"><label class="am-select-label">${group?'细分任务':'选择类别'}<select data-am-selection aria-label="选择类别">${rows.map(r=>`<option value="${esc(r.id)}" ${r.id===S.selected?'selected':''}>${esc(r.label)}</option>`).join('')}</select></label><div class="am-readout"><span>${S.syear} · ${esc(r.label)}</span><strong class="am-big">${short(p.value)}</strong>${badge(p.status)}<p class="am-quiet">${num(p.value)} ${unit} · 本层占比 ${(p.value/total*100).toFixed(1)}%</p></div><div class="am-mini-trend"><span>所选类别 · 五年趋势</span>${line([{...r,color:C[rows.indexOf(r)%C.length]}],{w:280,h:140,small:true,click:'structure',year:S.syear})}</div>${!group&&r.children?`<button data-am-drill="${r.id}">探索 ${r.children.length} 个细分任务 →</button>`:''}<div class="am-note">${isInf?'这里衡量 OpenRank 影响力，不是仓库数。原图见“口径与来源”。':k==='code'?'12 类采用原稿分类名称。数量为模拟主类别划分，不代表真实技术构成。':group?'当期为任务标签记录。历史细分值按该任务当前份额回推，仅为模拟。':'同一资产可有多个任务标签；本图仅覆盖已获取标签记录。按研究目的归为大类。'}</div></aside></div>`;
 setFoot('structure',`${mainLabel[k]} · ${unit} · ${k==='code'?(isInf?'近似读数与 2026 情景分开标记':'模拟数据供设计审阅'):'当期来源记录 / 历史模拟分开标记'} · 原始文件可下载替换`);
}
const sourceInfo={
 world:['全球资产地图：读数、模拟与归属','<p>代码地图：GitHub 活跃仓库总数 6,328,640 来自报告原表。国家归属缺失，95% 按设计权重模拟分配，5% 保持未分配。各国模拟值不能用于实际排名结论。</p><p>模型 / 数据地图：原稿的 826 家发布单位样本，模型 72,280、数据集 12,291。保留可读的前 14 国数值；其余差额按历史样本权重模拟分配。原稿快照日期待补。国家归属是发布单位口径，并非服务器或下载者所在地。</p><p>地图沿用此前确认的 OpenShare 几何形态；中国包含台湾省。斜纹代表模拟，灰色代表暂无数据。证据开关会同步过滤地图与国家列表。</p>','geography-v3.csv'],
 growth:['五年增长：各自的统计窗口','<p>代码仓库：GitHub / GitLab / Gitee / AtomGit 为报告原表中的活跃仓库；AtomGit 2022—2023 缺失，用模拟占位。2024 是四个平台均有原表值的最早年份，因此指数比较采用 2024 = 100。</p><p>代码提交：平台口径不限公开开源仓库，作为 AI 时代的生产背景。2022—2024 为模拟；2025 约 10 亿次来自 GitHub 管理层披露；2026 约 140 亿次为当时速率的全年预测，不能写成全年已实现。曲线不据此证明指数增长。</p><p>模型：2026-09-13 快照的存续仓库按创建年份累计回溯，有存活偏差。数据集：2026 为 10-11 接口总量，2022—2025 为模拟。各系列不具有同一截止日，也不能相加。</p>','growth-v3.csv'],
 structure:['类别演进：规模与影响力分开','<p>代码数量：沿用附件的 12 个技术类别名称，仓库数量全部模拟，每年合计与 GitHub 活跃仓库原表一致。OpenRank：2022—2025 为附件曲线近似读数；2026 为延续最近增量的情景，不是正式测算或预测。</p><p>模型 / 数据：2026 类别来自 OpenGauge 接口任务标签，按研究目的归组；可能重复标注，且并非所有仓库都有任务标签。树图面积表示标签记录数。2022—2025 按设定的增长节奏模拟，细分任务按当前份额回推。</p><p>模拟类别的份额、趋势与差距只供讨论图表结构，正式洞察需精确原表。<a href="/assets/amap/technology-openrank.png" target="_blank" rel="noopener">查看技术类别 OpenRank 原图 ↗</a></p>','categories-v3.csv']
};
function openSource(k){const o=$(`[data-am-overlay="${k}"]`),a=sourceInfo[k];o.innerHTML=`<button class="am-source-close" data-am-close="${k}">关闭 ×</button><span class="am-eyebrow">EVIDENCE & DEFINITIONS</span><h4>${a[0]}</h4>${a[1]}<p><a href="/assets/amap/${a[2]}" download>下载本图逐行数据 ↓</a> · <a href="/assets/amap/simulation-v3.json" download>模拟规则 ↓</a> · <a href="/assets/amap/source-manifest.json" download>来源清单 ↓</a></p><p class="am-quiet">2026 年度仍在进行中。报告样稿用于评审观察结构与交互，不把模拟当作事实。</p>`;o.innerHTML=o.innerHTML.replaceAll('href="/assets/',`href="${BASE}/assets/`);o.hidden=false;o.setAttribute('role','dialog');o.setAttribute('aria-label',a[0]);o.querySelector('button').focus();}
function closeSource(k){$(`[data-am-overlay="${k}"]`).hidden=true;$(`[data-am-source="${k}"]`).focus();}
function tab(k,v){S[k]=v;if(k==='world'){S.page=0;S.country='CN';}if(k==='structure'){S.group='';S.selected='';}document.querySelectorAll(`[data-am-tab^="${k}:"]`).forEach(b=>b.setAttribute('aria-pressed',b.dataset.amTab===k+':'+v));({world:renderWorld,growth:renderGrowth,structure:renderStructure})[k]();}
function chooseCountry(id){S.country=id;const a=D.geography[S.world].records.filter(r=>S.mock||!uncertain(r.status)).sort((a,b)=>b.value-a.value);S.page=Math.max(0,Math.floor(a.findIndex(r=>r.id===id)/6));renderWorld();}
document.addEventListener('click',e=>{
 if(!e.target.closest('.amap-review'))return;
 const el=e.target.closest('button,[data-am-country],[data-am-category],[data-am-yearpoint],[data-am-tile]');if(!el)return;const a=el.dataset;
 if(a.amTab){const [k,v]=a.amTab.split(':');tab(k,v);}
 else if(a.amOpenGrowth)tab('growth',a.amOpenGrowth);
 else if(a.amSource)openSource(a.amSource);else if(a.amClose)closeSource(a.amClose);
 else if(a.amCountry)chooseCountry(a.amCountry);
 else if(a.amMock){S.mock=a.amMock==='yes';S.page=0;renderWorld();}
 else if(a.amPage){S.page+=+a.amPage;renderWorld();}
 else if(a.amGmode){S.gmode=a.amGmode;renderGrowth();}
 else if(a.amLog){S.log=a.amLog==='yes';renderGrowth();}
 else if(a.amPlatform){S.platform=a.amPlatform;renderGrowth();}
 else if(a.amYearpoint){S.year=+a.amYearpoint;if(D.growth.platforms[a.amPlatformpoint])S.platform=a.amPlatformpoint;renderGrowth();}
 else if(a.amSmode){S.smode=a.amSmode;renderStructure();}
 else if(a.amMetric){S.metric=a.amMetric;S.selected='';renderStructure();}
 else if(a.amTile){S.selected=a.amTile;const r=categoryRows().find(r=>r.id===a.amTile);if(r?.children){S.group=r.id;S.selected='';}renderStructure();}
 else if(a.amCategory){S.selected=a.amCategory;S.syear=+a.amPointyear;renderStructure();}
 else if(a.amDrill){S.group=a.amDrill;S.selected='';renderStructure();}
 else if('amBack' in a){S.selected=S.group;S.group='';renderStructure();}
});
document.addEventListener('change',e=>{if(!e.target.closest('.amap-review'))return;const a=e.target.dataset,v=e.target.value;if('amLocation'in a)chooseCountry(v);else if('amGyear'in a){S.year=+v;renderGrowth();}else if('amSyear'in a){S.syear=+v;renderStructure();}else if('amSelection'in a){S.selected=v;renderStructure();}});
document.addEventListener('keydown',e=>{if(!e.target.closest('.amap-review'))return;if((e.key==='Enter'||e.key===' ')&&e.target.matches('svg [role="button"]')){e.preventDefault();e.target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}const o=document.querySelector('.am-source-overlay:not([hidden])');if(o&&e.key==='Escape'){e.preventDefault();e.stopPropagation();closeSource(o.dataset.amOverlay);}if(o&&e.key==='Tab'){const f=[...o.querySelectorAll('button,a')],first=f[0],last=f.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}});
renderWorld();renderGrowth();renderStructure();
})();
