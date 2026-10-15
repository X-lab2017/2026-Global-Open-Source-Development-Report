/* Dated, local geographic observations. No login, API token or external runtime calls. */
(()=>{
'use strict';
const payload=document.getElementById('goso-atlas-data');if(!payload)return;
const data=JSON.parse(payload.textContent),C=globalThis.GosoAtlasCore,NS='http://www.w3.org/2000/svg';
const base=document.querySelector('meta[name="gosd-base"]')?.content||'';
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=v=>v==null?'—':v>=1e8?(v/1e8).toLocaleString('zh-CN',{maximumFractionDigits:2})+'亿':v>=1e4?(v/1e4).toLocaleString('zh-CN',{maximumFractionDigits:2})+'万':v.toLocaleString('zh-CN',{maximumFractionDigits:2});
const exact=v=>v.toLocaleString('zh-CN',{maximumFractionDigits:2});
const palette=['var(--gv-m0, #DCEBF2)','var(--gv-m1, #BCD8E4)','var(--gv-m2, #8FBFD3)','var(--gv-m3, #5B9FBE)','var(--gv-m4, #337FA6)','var(--gv-m5, #156993)'];
const els=[];
const download=(text,name,type)=>{let u=URL.createObjectURL(new Blob([globalThis.GosoBrand?.resolve(text)||text],{type})),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};
for(const panel of document.querySelectorAll('[data-atlas]')){
 const kind=panel.dataset.atlas,prefix='atlas-'+kind,$=s=>panel.querySelector(s);let state,rows,svg,view=[0,0,880,470],filter='';
 const getUrlState=()=>{const u=new URL(location.href),raw={};for(const k of ['metric','scope','year','target','selected'])raw[k]=u.searchParams.get(prefix+'-'+k);return C.normalize(kind,raw);};
 state=getUrlState();
 const unit=()=>['developers','active','talent'].includes(state.metric)?'人':['contribution','influence','flows'].includes(state.metric)?'OpenRank':state.metric==='downloads'?'次':'个';
 const snapshot='vci'.includes(kind);
 const period=()=>snapshot?'OpenShare 2026-10 页面快照':kind==='a'?'2026-09-13 快照':kind==='d'?'2026 报告年项目样本':state.year===2026?'2026 年 7 月快照':state.year+' 报告年 · 固定十城市';
 const record=id=>rows.find(r=>(r.id||r.name)===id);
 const geom=id=>data.geometry[state.scope].find(g=>g.id===id);
 function save(){const u=new URL(location.href);for(const k of ['metric','scope','year','target','selected']){if(k==='year'&&kind!=='t'||k==='target'&&kind!=='d')continue;state[k]?u.searchParams.set(prefix+'-'+k,state[k]):u.searchParams.delete(prefix+'-'+k);}history.replaceState(null,'',u);}
 function detail(id){
  const r=record(id),f=geom(id),name=r?.name||f?.name||'选择地区';
  if(!r){$('[data-atlas-detail]').innerHTML='<span>'+esc(period())+'</span><strong>'+esc(name)+'</strong><p>本视图未收录数值；不代表零。</p>';return;}
  let more=kind==='d'?`占所选项目样本贡献的 ${r.share.toFixed(2)}%；来源前十合计 ${rows.reduce((s,x)=>s+x.share,0).toFixed(2)}%。`:kind==='a'?`已识别国家样本中的模型份额 ${r.share.toFixed(2)}%；未知归属模型单独保留。`:kind==='t'?`固定十城市样本；2022 年 ${r.series[0].value} 人，2026 年 ${r.series[4].value} 人。`:r.approx?'来源页面按“万”显示，保留近似读数。':'来源页面显示读数；仅用于本次快照。';
  $('[data-atlas-detail]').innerHTML='<span>'+esc(period())+'</span><strong>'+esc(name)+' <b>'+(r.approx?'约 ':'')+esc(r.display||exact(r.value))+'</b> <small>'+unit()+'</small></strong><p>'+esc(more)+'</p>';
 }
 function highlight(id){panel.querySelectorAll('[data-geo]').forEach(el=>el.classList.toggle('is-selected',el.dataset.geo===id));panel.querySelectorAll('[data-select]').forEach(el=>{let on=el.dataset.select===id;el.classList.toggle('is-selected',on);el.setAttribute('aria-pressed',String(on));});}
 function choose(id,drill=false){if(drill&&snapshot&&state.scope==='world'&&id==='CN'&&state.metric!=='influence'){state.scope='china';state.selected='110000';view=[0,0,880,470];render();save();return;}state.selected=id;highlight(id);detail(id);save();}
 function tip(id,e){const r=record(id),f=geom(id);if(!r&&!f)return;const tt=$('[data-atlas-tooltip]');tt.innerHTML='<strong>'+esc(r?.name||f.name)+'</strong><span>'+(r?(r.approx?'约 ':'')+esc(r.display||num(r.value))+' '+unit():'本视图未收录')+'</span>';tt.hidden=false;const b=$('.atlas-map-wrap').getBoundingClientRect();tt.style.left=Math.max(8,Math.min(b.width-190,(e.clientX||b.x+20)-b.x+12))+'px';tt.style.top=Math.max(8,Math.min(b.height-80,(e.clientY||b.y+30)-b.y-50))+'px';}
 function ranking(){const rr=rows.filter(r=>!filter||r.name.toLowerCase().includes(filter)||String(r.id).toLowerCase().includes(filter));$('[data-atlas-ranking]').innerHTML=rr.length?rr.map(r=>{const rank=rows.indexOf(r)+1;return '<button type="button" data-select="'+esc(r.id||r.name)+'" aria-pressed="'+(state.selected===(r.id||r.name))+'"><span>'+String(rank).padStart(2,'0')+'</span><strong>'+esc(r.name)+'</strong><b>'+esc(r.display||num(r.value))+'</b></button>';}).join(''):'<p class="atlas-empty">没有匹配地区。可尝试国家代码，例如 CN。</p>';}
 function map(){
  const values=rows.map(r=>r.value),by=new Map(rows.map(r=>[r.id,r]));
  let p=['<svg xmlns="'+NS+'" viewBox="'+view.join(' ')+'" role="group" aria-label="'+esc(C.metricNames[state.metric])+'地图"><rect x="-2000" y="-1000" width="5000" height="2500" fill="var(--atlas-ocean)"/>'];
  for(const y of [120,235,350])p.push('<path d="M25 '+y+'H855" stroke="var(--atlas-grid)" stroke-width=".6" stroke-dasharray="3 6"/>');
  for(const f of data.geometry[state.scope]){
   const r=by.get(f.id),ci=C.colorIndex(r?.value,values),fill=kind==='t'?'var(--atlas-land)':ci<0?'var(--atlas-land)':palette[ci];
   const focus=kind!=='t'&&r?' tabindex="0" role="button" aria-label="'+esc(f.name+'，'+(r.display||num(r.value))+' '+unit()+(f.id==='CN'&&snapshot&&state.scope==='world'&&state.metric!=='influence'?'，进入中国省级地图':''))+'"':'';
   p.push('<use href="#geo-'+state.scope+'-'+esc(f.id)+'" data-geo="'+esc(f.id)+'" fill="'+fill+'" fill-rule="evenodd" stroke="var(--atlas-border)" stroke-width=".65" vector-effect="non-scaling-stroke"'+focus+'><title>'+esc(f.name)+(r?' · '+esc(r.display||num(r.value)):' · 本视图未收录')+'</title></use>');
  }
  if(kind==='d'){
   const to=data.geometry.world.find(f=>f.id===state.target).center;
   p.push('<defs><marker id="arrow-'+kind+'" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L8 4L0 8" fill="var(--gv-s0, #156993)"/></marker></defs>');
   for(const r of rows){const from=data.geometry.world.find(f=>f.id===r.id)?.center;if(!from||r.id===state.target)continue;const [x,y]=from,[xx,yy]=to;const mid=(x+xx)/2,raise=Math.min(140,Math.abs(xx-x)*.22+30);p.push('<path d="M'+x+','+y+' Q'+mid+','+(Math.min(y,yy)-raise)+' '+xx+','+yy+'" fill="none" stroke="var(--gv-s0, #156993)" stroke-opacity=".65" stroke-width="'+(1+Math.sqrt(r.value/Math.max(...values))*9)+'" marker-end="url(#arrow-'+kind+')" data-geo="'+esc(r.id)+'" tabindex="0" role="button" aria-label="'+esc(r.name)+'贡献流向，'+r.share+'%"><title>'+esc(r.name)+' → '+(state.target==='CN'?'中国':'美国')+' · '+r.share+'%</title></path>');}
   p.push('<circle cx="'+to[0]+'" cy="'+to[1]+'" r="10" fill="var(--gv-s0, #156993)" stroke="white" stroke-width="2"/><text x="'+(to[0]+14)+'" y="'+(to[1]+4)+'" class="atlas-map-label">'+(state.target==='CN'?'中国项目':'美国项目')+'</text>');
  }
  if(kind==='t')for(const r of [...rows].reverse()){
   const [x,y]=r.center,rr=Math.max(3,Math.sqrt(r.value/Math.max(...values))*18);
   p.push('<circle cx="'+x+'" cy="'+y+'" r="'+rr+'" fill="var(--gv-s0, #156993)" fill-opacity=".76" stroke="white" stroke-width="1.5" data-geo="'+esc(r.id)+'" tabindex="0" role="button" aria-label="'+esc(r.name)+'，'+r.value+'人"><title>'+esc(r.name)+' · '+r.value+' 人</title></circle>');
  }
  if(kind==='t')for(const name of ['北京','上海','杭州','深圳','台北','成都','武汉']){const r=rows.find(x=>x.id===name);if(!r)continue;let [x,y]=r.center,dx=15,dy=4;if(name==='上海'){dx=26;dy=-9;}if(name==='杭州'){dx=-30;dy=23;}if(name==='台北'){dx=14;dy=16;}p.push('<text x="'+(x+dx)+'" y="'+(y+dy)+'" class="atlas-map-label">'+(name==='台北'?'台北（台湾省）':name)+'</text>');}
  else for(const code of state.scope==='world'?['US','CN','BR','IN','AU']:['110000','440000','510000','310000','710000']){const f=geom(code);if(f&&by.has(code)){let [x,y]=f.center;p.push('<text x="'+x+'" y="'+y+'" class="atlas-map-label" text-anchor="middle">'+esc(f.id==='710000'?'台湾省':f.name.replace(/省|市/g,''))+'</text>');}}
  if(state.scope==='china')p.push('<rect x="690" y="260" width="135" height="188" fill="none" stroke="var(--atlas-muted)" stroke-width=".7"/><text x="700" y="465" fill="var(--atlas-muted)" font-size="11">南海诸岛</text>');
  p.push('</svg>');$('[data-atlas-map]').innerHTML=p.join('');svg=$('[data-atlas-map] svg');
  let drag=null;
  svg.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY,view:[...view],moved:false};});
  svg.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>5){drag.moved=true;svg.setPointerCapture(e.pointerId);const b=svg.getBoundingClientRect();view=[drag.view[0]-dx/b.width*view[2],drag.view[1]-dy/b.height*view[3],view[2],view[3]];svg.setAttribute('viewBox',view.join(' '));$('[data-atlas-tooltip]').hidden=true;}});
  svg.addEventListener('pointerup',e=>{const moved=drag?.moved;drag=null;if(moved)return;const target=e.target.closest('[data-geo]');if(target)choose(target.dataset.geo,true);});
  svg.addEventListener('pointercancel',()=>{drag=null;});
  svg.addEventListener('pointerover',e=>{const el=e.target.closest('[data-geo]');if(el&&!drag)tip(el.dataset.geo,e);});
  svg.addEventListener('pointerleave',()=>{$('[data-atlas-tooltip]').hidden=true;drag=null;});
  svg.addEventListener('focusin',e=>{const el=e.target.closest('[data-geo]');if(el)detail(el.dataset.geo);});
  svg.addEventListener('keydown',e=>{const el=e.target.closest('[data-geo]');if(el&&['Enter',' '].includes(e.key)){e.preventDefault();choose(el.dataset.geo,true);}});
 }
 function render(){
  state=C.normalize(kind,state);rows=C.records(data,kind,state);if(!record(state.selected))state.selected=kind==='t'?'北京':state.scope==='china'?'110000':kind==='d'?state.target:'CN';if(!record(state.selected))state.selected=rows[0]?.id||'';
  $('[data-atlas-context]').textContent=(state.scope==='china'?'中国':'全球')+' / '+C.metricNames[state.metric]+' · '+rows.length+' 个'+(kind==='t'?'城市':'地区')+'条目';
  $('[data-atlas-hint]').textContent=state.metric==='influence'?'来源平台未提供项目影响力省级下钻':snapshot&&state.scope==='world'?'点击中国下钻 · 拖动平移':'悬停查看 · 点选锁定 · 拖动平移';
  panel.querySelectorAll('[data-atlas-metric]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.atlasMetric===state.metric)));
  panel.querySelectorAll('[data-scope]').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.scope===state.scope));b.disabled=b.dataset.scope==='china'&&state.metric==='influence';b.title=b.disabled?'原始平台未提供项目影响力省级数据':'';});
  if($('[data-atlas-target]'))$('[data-atlas-target]').value=state.target;
  if($('[data-atlas-year]')){$('[data-atlas-year]').value=state.year;$('[data-atlas-year-label]').textContent=state.year;}
  if(kind==='t')$('.atlas-period').textContent=period();
  $('[data-atlas-legend]').innerHTML=kind==='t'?'<span class="atlas-size-dots">● ● ●</span><span>圆面积 = 人才数量 · 固定十城市</span>':kind==='d'?'<span class="atlas-flow-key">→</span><span>开发者所在地 → 项目归属地 · 线宽 = 贡献度</span>':'<i></i><span>'+'0 — '+num(C.colorCap(rows.map(r=>r.value)))+' · P95 封顶；≥上限同色，原值见读数</span><b></b><span>本视图未收录</span>';
  map();ranking();highlight(state.selected);detail(state.selected);
 }
 panel.querySelectorAll('[data-atlas-enhanced],[data-atlas-export],[data-atlas-share]').forEach(e=>e.hidden=false);
 panel.addEventListener('click',async e=>{
  const b=e.target.closest('button');if(!b)return;
  if(b.dataset.atlasMetric){state.metric=b.dataset.atlasMetric;view=[0,0,880,470];filter='';$('[data-atlas-search]').value='';render();save();}
  if(b.dataset.scope){state.scope=b.dataset.scope;state.selected='';filter='';$('[data-atlas-search]').value='';view=[0,0,880,470];render();save();}
  if(b.dataset.select)choose(b.dataset.select,false);
  if(b.dataset.zoom){const factor=b.dataset.zoom==='in'?.75:1/.75;const w=Math.max(220,Math.min(1320,view[2]*factor)),h=w*470/880;view=b.dataset.zoom==='reset'?[0,0,880,470]:[view[0]+(view[2]-w)/2,view[1]+(view[3]-h)/2,w,h];svg.setAttribute('viewBox',view.join(' '));}
  if(b.hasAttribute('data-atlas-share')){const u=new URL(location.href);u.hash=prefix;try{await navigator.clipboard.writeText(u.href);$('[data-atlas-status]').textContent='当前视图链接已复制';}catch{$('[data-atlas-status]').innerHTML='<a href="'+esc(u.href)+'">打开此视图后复制地址</a>';}}
  if(b.hasAttribute('data-atlas-export')){
   const clone=svg.cloneNode(true);clone.setAttribute('viewBox','0 0 880 540');clone.setAttribute('xmlns',NS);
   clone.querySelectorAll('.is-selected').forEach(el=>{el.setAttribute('fill','var(--gv-goldDisplay)');el.setAttribute('stroke','var(--gv-ink)');});
   clone.querySelectorAll('use').forEach(u=>{const path=document.createElementNS(NS,'path'),def=document.querySelector(u.getAttribute('href'));for(const a of u.attributes)if(a.name!=='href')path.setAttribute(a.name,a.value);path.setAttribute('d',def.getAttribute('d'));u.replaceWith(path);});
   clone.querySelectorAll('text').forEach(t=>{t.setAttribute('font-family','Arial, Noto Sans SC, sans-serif');t.setAttribute('font-size','12');t.setAttribute('fill','var(--gv-ink)');t.setAttribute('stroke','none');});
   const title=document.createElementNS(NS,'text');title.setAttribute('fill','var(--gv-ink)');title.setAttribute('x','24');title.setAttribute('y','493');title.setAttribute('font-size','15');title.textContent='GOSO · '+C.metricNames[state.metric]+' · '+period();clone.append(title);
   const note=document.createElementNS(NS,'text');note.setAttribute('fill','var(--gv-muted)');note.setAttribute('x','24');note.setAttribute('y','519');note.setAttribute('font-size','10');note.textContent=snapshot?'来源：OpenShare 公开排行榜显示值；灰色为本视图未收录。非报告年度测算；P95 封顶。':'来源：GOSD GitHub 底表；样本范围与未知归属详见报告。';clone.append(note);
   const scale=document.createElementNS(NS,'text');scale.setAttribute('x','24');scale.setAttribute('y','538');scale.setAttribute('font-size','10');scale.setAttribute('fill','var(--gv-muted)');scale.textContent=$('[data-atlas-legend]').textContent;clone.append(scale);
   clone.setAttribute('viewBox','0 0 880 550');
   download(new XMLSerializer().serializeToString(clone),'GOSO-'+kind+'-'+state.metric+'-'+state.scope+'.svg','image/svg+xml');
  }
 });
 $('[data-atlas-search]').addEventListener('input',e=>{filter=e.target.value.trim().toLowerCase();ranking();highlight(state.selected);});
 $('[data-atlas-target]')?.addEventListener('change',e=>{state.target=e.target.value;state.selected='';render();save();});
 $('[data-atlas-year]')?.addEventListener('input',e=>{state.year=Number(e.target.value);render();save();});
 render();els.push(()=>{state=getUrlState();view=[0,0,880,470];render();});
}
window.addEventListener('popstate',()=>els.forEach(f=>f()));
// Original draft images retain a regular image link as the no-JS fallback.
const dialog=document.createElement('dialog');dialog.className='atlas-image-dialog';dialog.innerHTML='<div><strong>带图初稿 · 原图对照</strong><button type="button" aria-label="关闭原图">关闭 ×</button></div><img alt="">';document.body.append(dialog);dialog.querySelector('button').onclick=()=>dialog.close();
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
document.querySelectorAll('[data-original-image]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();const img=dialog.querySelector('img');img.src=a.href;img.alt=a.querySelector('img').alt;dialog.showModal();}));
})();
