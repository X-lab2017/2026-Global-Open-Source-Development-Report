/* Pure data/scoping operations shared by the atlas and its evidence checks. */
(function(root){
'use strict';
const defaultMetric={v:'developers',c:'contribution',i:'influence',t:'talent',d:'flows',a:'models'};
const metricNames={developers:'开发者数量',active:'活跃开发者',contribution:'开发者 OpenRank 贡献度',influence:'项目 OpenRank 影响力',talent:'核心人才',flows:'跨地域贡献',models:'模型数量',downloads:'累计下载量',likes:'点赞数'};
function normalize(kind,raw={}){
 const metrics=kind==='v'?['developers','active']:kind==='c'?['contribution']:kind==='i'?['influence']:kind==='a'?['models','downloads','likes']:[defaultMetric[kind]];
 const metric=metrics.includes(raw.metric)?raw.metric:defaultMetric[kind];
 const scope=kind==='t'?'china':('vci'.includes(kind)&&metric!=='influence'&&raw.scope==='china'?'china':'world');
 return {metric,scope,year:/^202[2-6]$/.test(String(raw.year))?Number(raw.year):2026,target:raw.target==='US'?'US':'CN',selected:raw.selected||''};
}
function records(data,kind,state){
 let rows;
 if('vci'.includes(kind))rows=data.snapshot.sets[state.metric+'-'+state.scope].rows.map(r=>({...r,approx:r.display.includes('万')}));
 else if(kind==='t')rows=data.cities.map(r=>({...r,value:r.series.find(s=>Number(s.year)===state.year).value}));
 else if(kind==='d')rows=data.flows.filter(r=>r.target===state.target).map(r=>({...r}));
 else rows=data.assets.map(r=>({...r,value:r[state.metric]}));
 return rows.sort((a,b)=>b.value-a.value);
}
function colorCap(values){const vv=values.filter(v=>Number.isFinite(v)&&v>0).sort((a,b)=>a-b);return Math.ceil(vv[Math.floor(vv.length*.95)]||1);}
function colorIndex(v,values){if(v==null||!Number.isFinite(v))return -1;return Math.min(5,Math.max(0,Math.floor(v/colorCap(values)*5.999)));}
const api={defaultMetric,metricNames,normalize,records,colorIndex,colorCap};if(typeof module==='object'&&module.exports)module.exports=api;else root.GosoAtlasCore=api;
})(globalThis);
