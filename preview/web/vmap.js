/* Source-backed V-Map comparison; uses the shared Chapter 1 presentation lifecycle. */
(function(){
 'use strict';
const base=document.querySelector('meta[name="gosd-base"]')?.content||'';

 const dataEl=document.getElementById('vmap-data');
 const figure=document.getElementById('fig-vmap-comparison');
 if(!dataEl||!figure)return;
 const data=JSON.parse(dataEl.textContent),by=Object.fromEntries(data.countries.map(r=>[r.id,r]));
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const initial=new URLSearchParams(location.search);
 let mode=['countries','trend'].includes(initial.get('vmapView'))?initial.get('vmapView'):'regions';
 let trendYear=4,trendIndex=false,trendFocus=null;
 let scope=initial.get('vmapScope')==='extended'?'extended':'github';
 const chart=figure.querySelector('[data-vmap-chart]');
 const controls=figure.querySelector('.vmap-controls');controls.hidden=false;
 function endpoint(row,key){return row[key]+(key==='active'&&row.id==='CN'&&scope==='extended'&&mode==='countries'?data.domestic.active_approx:0);}
 function records(){
  if(mode==='countries')return data.countries.filter(r=>r.active!==null).sort((a,b)=>endpoint(b,'active')-endpoint(a,'active')).slice(0,10);
  return data.five_group_records;
 }
 function plot(key,rows){
  const limit=key==='total'?4000:mode==='regions'?800:500,ranked=mode==='countries';
  const title=key==='total'?'开发者总量':'活跃开发者';
  const suffix=mode==='regions'?'万人 · 五域统计':scope==='github'?'万人 · GitHub':'万人 · 中国含国内平台补充';
  const body=rows.map((row,i)=>{
   const value=row[key],extra=key==='active'&&row.id==='CN'&&scope==='extended'&&mode==='countries';
   const label=(ranked?String(i+1).padStart(2,'0')+'  ':'')+row.name;
   const display=value===null?'—':extra?'约'+Math.round(endpoint(row,key)):(Math.floor(value*100+1e-8)/100).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
   const marks=value===null?'<span class="vmap-missing">待同步</span>':'<i class="vmap-github" style="width:'+value/limit*100+'%"></i>'+(extra?'<i class="vmap-domestic" style="width:'+data.domestic.active_approx/limit*100+'%"></i>':'');
   return '<div class="vmap-bar-row" data-country="'+row.id+'"><span class="vmap-label">'+esc(label)+'</span><div class="vmap-track" aria-hidden="true">'+marks+'</div><b class="vmap-value" aria-label="'+esc(row.name+' '+(value===null?'待同步':display+'万人'))+'">'+display+'</b></div>';
  }).join('');
  return '<div class="vmap-plot" data-vmap-plot="'+key+'"><h5>'+title+'<small>'+suffix+'</small></h5><div class="vmap-bar-list">'+body+'</div><div class="vmap-axis"><span>0</span><span>'+limit.toLocaleString('en-US')+' 万人</span></div></div>';
 }
 function render(save){
  const rows=records(),trending=mode==='trend';
  chart.hidden=trending;
  figure.querySelector('[data-vmap-trend]').hidden=!trending;
  figure.classList.toggle('vmap-trend-mode',trending);
  figure.querySelectorAll('[data-vmap-scope]').forEach(b=>{b.disabled=mode!=='countries';b.closest('[role=group]').hidden=mode!=='countries';});
  chart.classList.toggle('vmap-country-mode',mode==='countries');
  if(!trending)chart.innerHTML=(mode==='regions'?plot('total',rows):'')+plot('active',rows);
  figure.querySelectorAll('[data-vmap-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.vmapView===mode)));
  figure.querySelectorAll('[data-vmap-scope]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.vmapScope===scope)));
  const expanded=scope==='extended'&&mode==='countries';
  figure.dataset.evidenceKind='confirmed';
  figure.querySelector('.vmap-status').textContent=mode==='regions'?'2026报告年度 · 编制组五域规模':expanded?'2026报告年度 · 中国含国内平台补充约370万':'2026报告年度 · GitHub 中国活跃250.48万';
  figure.querySelector('[data-vmap-domestic-legend]').hidden=!expanded;
  figure.querySelector('[data-vmap-base-legend]').innerHTML='<i></i>'+(mode==='regions'?'编制组五域统计':'GitHub');
  figure.querySelector('[data-vmap-note]').textContent=expanded?'国内约120万：报告编制组根据Gitee、AtomGit等官方平台数据，结合问卷调研去重得到。其他国家仅展示GitHub覆盖。':mode==='regions'?'五域按编制组原稿统计展示，不构成全球穷尽划分。国内补充量不重复叠加到五域中国值中。':'GitHub活跃规模前十；可切换国内平台补充，观察覆盖范围对中国读数的影响。';
  if(trending){
   figure.querySelector('.vmap-status').textContent='2022—2026报告年度 · 五域活跃规模演变';
   figure.querySelector('[data-vmap-note]').textContent='年份为报告年度：前一年7月1日至当年6月30日。来源：报告编制组五域历史统计。';
   figure.querySelector('.vmap-legend').hidden=true;renderTrend();
  }else figure.querySelector('.vmap-legend').hidden=false;
  if(save){const url=new URL(location.href);url.searchParams.set('vmapView',mode);url.searchParams.set('vmapScope',scope);history.replaceState(null,'',url);}
 }
 function renderTrend(){
  const years=data.trend.years,series=data.trend.series;
  const W=780,H=300,left=58,right=30,top=24,bottom=40,max=trendIndex?240:800;
  const val=(r,i)=>trendIndex?r.values[i]/r.values[0]*100:r.values[i];
  const x=i=>left+i*(W-left-right)/4,y=v=>H-bottom-v/max*(H-top-bottom);
  const color=i=>'var(--gv-s'+i+','+data.publication_style.colors[i]+')';
  const dash=i=>data.publication_style.dashes[i]?.join(' ')||'';
  let svg='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="五域2022至2026报告年度活跃开发者历史序列"><title>报告编制组五域历史统计</title>';
  [0,.25,.5,.75,1].forEach(f=>{const v=max*f;svg+='<path d="M'+left+' '+y(v)+'H'+(W-right)+'" stroke="var(--line)"/><text x="'+(left-10)+'" y="'+(y(v)+5)+'" text-anchor="end">'+v+'</text>';});
  years.forEach((yr,i)=>{svg+='<text x="'+x(i)+'" y="'+(H-12)+'" text-anchor="middle">'+yr+'</text>';});
  svg+='<path d="M'+x(trendYear)+' '+top+'V'+(H-bottom)+'" stroke="var(--muted)" stroke-dasharray="4 5"/>';
  series.forEach((r,j)=>{
   const dim=trendFocus&&trendFocus!==r.id;
   svg+='<g opacity="'+(dim?.2:1)+'"><path d="'+r.values.map((v,i)=>(i?'L':'M')+x(i)+','+y(val(r,i))).join(' ')+'" fill="none" stroke="'+color(j)+'" stroke-width="3" stroke-dasharray="'+dash(j)+'"/>';
   r.values.forEach((v,i)=>{svg+='<circle cx="'+x(i)+'" cy="'+y(val(r,i))+'" r="'+(i===trendYear?5:3)+'" fill="'+color(j)+'"><title>'+esc(r.name)+' '+years[i]+'：'+(trendIndex?val(r,i).toFixed(1):v.toFixed(2)+'万人')+'</title></circle>';});svg+='</g>';
  });svg+='</svg>';
  const modes='<div class="vm-trend-modes" role="group" aria-label="趋势量纲"><button type="button" data-trend-mode="absolute" aria-pressed="'+!trendIndex+'">人数 · 万人</button><button type="button" data-trend-mode="index" aria-pressed="'+trendIndex+'">起点对比 · 2022=100</button></div>';
  const groups=series.map((r,i)=>'<button type="button" data-trend-group="'+r.id+'" aria-pressed="'+(trendFocus===r.id)+'"><i style="background:'+color(i)+'"></i><span>'+esc(r.name)+'</span><b>'+val(r,trendYear).toFixed(trendIndex?1:2)+'</b></button>').join('');
  figure.querySelector('[data-vmap-trend]').innerHTML='<div class="vm-trend-chart">'+modes+svg+'<div class="vm-trend-years" role="group" aria-label="历史年份">'+years.map((yr,i)=>'<button type="button" data-trend-year="'+i+'" aria-pressed="'+(i===trendYear)+'">'+yr+'</button>').join('')+'</div></div><aside class="vm-trend-table"><h5>'+years[trendYear]+' · '+(trendIndex?'起点指数':'活跃万人')+'</h5>'+groups+'<p>点选组别突出曲线，再点恢复全部。<br>前一年7月至当年6月。</p><a href="'+base+'/assets/vmap/fig-2-1-2_five-year-source.csv" download>下载五年原表 CSV ↓</a></aside>';
 }
 figure.addEventListener('click',event=>{
  const b=event.target.closest('button');if(!b)return;
  if(b.dataset.vmapView){mode=b.dataset.vmapView;render(true);}
  if(b.dataset.vmapScope&&!b.disabled){scope=b.dataset.vmapScope;render(true);}
  if(b.dataset.trendMode){trendIndex=b.dataset.trendMode==='index';renderTrend();}
  if(b.dataset.trendYear){trendYear=Number(b.dataset.trendYear);renderTrend();}
  if(b.dataset.trendGroup){trendFocus=trendFocus===b.dataset.trendGroup?null:b.dataset.trendGroup;renderTrend();}
 });
 render(false);
})();

/* Native SVG map, source snapshot rankings and provincial detail share one state. */
(function(){
 'use strict';
 const el=document.getElementById('vmap-data');if(!el)return;
 const data=JSON.parse(el.textContent),countryBy=Object.fromEntries(data.countries.map(r=>[r.id,r]));
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const fmt=v=>v===null||v===undefined?'—':v>0&&v<.01?'＜0.01':(Math.trunc(v*100+Math.sign(v)*1e-8)/100).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
 const templates={world:document.querySelector('#fig-vmap-global .vm-map-cards').innerHTML,china:document.querySelector('#fig-vmap-china .vm-map-cards').innerHTML};
 document.querySelectorAll('.vm-map-layout').forEach(layout=>{
  const figure=layout.closest('figure'),isGlobal=figure.id==='fig-vmap-global';
  let scope=isGlobal?'world':'china',metric='active',selected=isGlobal?'CN':'110000',zoom=1;
  const rows=()=>scope==='world'?data.countries:data.provinces;
  const byId=id=>rows().find(r=>r.id===id);
  function detail(id,name){
   const r=byId(id),target=figure.querySelector('[data-map-card="detail"]');
   const geo=figure.querySelector('[data-map-layer="'+scope+'"] [data-map-id="'+id+'"]');
   const title=r?r.name:name||(geo?geo.dataset.mapName:'未收录地区');
   if(!r){target.innerHTML='<span class="vm-card-label">'+esc(title)+'</span><strong class="vm-no-data">本轮未收录读数</strong><p>保留地域轮廓；缺失值不按零处理。</p>';return;}
   const denominator=scope==='world'?data.global_active:countryBy.CN.active;
   target.innerHTML='<span class="vm-card-label">所选地区 · '+esc(title)+'</span><div class="vm-pair"><span>总量 / 万人<b>'+fmt(r.total)+'</b></span><span>活跃 / 万人<b>'+fmt(r.active)+'</b></span></div><p>'+ (r.active===null?'活跃数据待补':(scope==='world'?'占全球':'占全国')+'活跃 '+(r.active/denominator*100).toFixed(1)+'%')+' · 较上年 '+(r.increase===null?'待补':(r.increase>=0?'+':'')+fmt(r.increase)+'万')+'</p>';
  }
  function select(id,name,temporary){
   if(!temporary)selected=id;
   const r=byId(id),value=r?r[metric]:null;
   if(!name){const geo=figure.querySelector('[data-map-layer="'+scope+'"] [data-map-id="'+id+'"]');name=geo?geo.dataset.mapName:null;}
   figure.querySelector('[data-map-readout]').textContent=(r?r.name:name||'未收录地区')+' · '+(metric==='active'?'活跃':'总量')+' '+(value===null?'未收录':fmt(value)+' 万人')+(scope==='world'&&id==='CN'?' · 点击地图中国下钻':'');
   figure.querySelectorAll('[data-map-layer="'+scope+'"] [data-map-id]').forEach(p=>p.classList.toggle('vm-selected',p.dataset.mapId===id));
   figure.querySelectorAll('[data-map-row]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mapRow===id)));
   detail(id,name);
  }
  function render(){
   const rr=rows(),by=Object.fromEntries(rr.map(r=>[r.id,r])),maximum=Math.max(...rr.map(r=>r[metric]||0));
   figure.querySelectorAll('[data-map-layer]').forEach(l=>{l.hidden=l.dataset.mapLayer!==scope;});
   figure.querySelectorAll('[data-map-layer="'+scope+'"] [data-map-id]').forEach(p=>{
    const r=by[p.dataset.mapId],v=r?r[metric]:null;
    p.setAttribute('fill',v===null?'var(--vm-empty,#E6E8EA)':'var(--gv-m'+Math.min(5,Math.floor(v/maximum*5.999))+',#156993)');
    p.setAttribute('tabindex',v===null?'-1':'0');
    p.setAttribute('aria-label',p.dataset.mapName+'，'+(metric==='active'?'活跃':'总量')+(v===null?'未收录':fmt(v)+'万人'));
    p.querySelector('title').textContent=p.getAttribute('aria-label');
   });
   ['total','active'].forEach(key=>{
    const list=rr.filter(r=>r[key]!==null).sort((a,b)=>b[key]-a[key]).slice(0,10),max=list[0][key];
    const rank=figure.querySelector('[data-map-rank="'+key+'"]');rank.closest('aside').classList.toggle('vm-rank-emphasis',key===metric);
    rank.innerHTML=list.map((r,i)=>'<button type="button" data-map-row="'+r.id+'" data-rank-metric="'+key+'" aria-pressed="false"><span>'+String(i+1).padStart(2,'0')+'</span><strong>'+esc(r.name)+'</strong><b>'+fmt(r[key])+'</b><i style="width:'+r[key]/max*100+'%"></i></button>').join('');
   });
   figure.querySelectorAll('[data-map-metric]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mapMetric===metric)));
   figure.querySelectorAll('[data-map-scope]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mapScope===scope)));
   figure.querySelector('[data-map-context]').textContent=(scope==='world'?'全球 · 同版国家／地区底表':'中国 · 34个省级地区') ;
   figure.querySelector('[data-map-scale]').textContent='线性色阶：0—'+fmt(maximum)+' 万人';
   select(selected,null,false);
  }
  function zoomMap(action){
   zoom=action==='reset'?1:Math.max(1,Math.min(3,zoom+(action==='in'?.5:-.5)));
   const svg=figure.querySelector('[data-map-svg="'+scope+'"]'),p=svg.querySelector('[data-map-id="'+selected+'"]');
   const center=p?p.dataset.mapCenter.split(',').map(Number):[440,235],w=880/zoom,h=470/zoom;
   svg.setAttribute('viewBox',[Math.max(0,Math.min(880-w,center[0]-w/2)),Math.max(0,Math.min(470-h,center[1]-h/2)),w,h].join(' '));
  }
  function setScope(next){zoomMap('reset');scope=next;selected=next==='china'?'110000':'CN';figure.querySelector('.vm-map-cards').innerHTML=templates[scope];render();}
  figure.addEventListener('click',e=>{
   const b=e.target.closest('[data-map-metric],[data-map-scope],[data-map-row],[data-map-id],[data-map-zoom]');if(!b)return;
   if(b.dataset.mapZoom){zoomMap(b.dataset.mapZoom);return;}
   if(b.dataset.mapMetric){metric=b.dataset.mapMetric;render();return;}
   if(b.dataset.mapScope){setScope(b.dataset.mapScope);return;}
   const id=b.dataset.mapRow||b.dataset.mapId;
   if(b.dataset.mapId==='CN'&&scope==='world'){setScope('china');return;}
   if(b.dataset.rankMetric)metric=b.dataset.rankMetric;
   selected=id;render();select(id,b.dataset.mapName,false);
  });
  figure.addEventListener('keydown',e=>{
   const p=e.target.closest('[data-map-id]');if(!p||!['Enter',' '].includes(e.key))return;
   e.preventDefault();if(p.dataset.mapId==='CN'&&scope==='world')setScope('china');else select(p.dataset.mapId,p.dataset.mapName,false);
  });
  figure.addEventListener('mouseover',e=>{const p=e.target.closest('[data-map-id],[data-map-row]');if(p)select(p.dataset.mapId||p.dataset.mapRow,p.dataset.mapName,true);});
  figure.addEventListener('focusin',e=>{const p=e.target.closest('[data-map-id],[data-map-row]');if(p)select(p.dataset.mapId||p.dataset.mapRow,p.dataset.mapName,true);});
  figure.addEventListener('mouseout',e=>{if(e.target.closest('[data-map-id],[data-map-row]'))select(selected,null,true);});
  render();
 });
})();
