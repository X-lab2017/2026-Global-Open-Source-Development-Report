// Sample-only comparisons. Missing destinations are unknown, never zero inflow.
export const SOUTH_CODES=['IN','BR','ID','VN','PH','EG','ZA'];
export function profileFlows(F,code){
 const observed=F.edges.filter(e=>e.kind==='observed'),estimated=F.edges.filter(e=>e.kind==='estimated');
 const outgoing=observed.filter(e=>e.source===code&&e.target!==code),incoming=observed.filter(e=>e.target===code&&e.source!==code),local=observed.find(e=>e.source===code&&e.target===code);
 const sum=rows=>rows.reduce((v,e)=>v+e.value,0);
 return {out:outgoing.length?sum(outgoing):null,in:F.targets[code]?sum(incoming):null,local:local?.value??null,outEstimate:sum(estimated.filter(e=>e.source===code&&e.target!==code)),inEstimate:F.targets[code]?sum(estimated.filter(e=>e.target===code&&e.source!==code)):null};
}
export function includeFlow(e,{flow,lens,selected,target}){
 if(flow==='none'||(e.kind==='estimated'&&flow!=='scenario')||!e.display)return false;
 if(lens==='out')return e.source===selected&&e.target!==selected;
 if(lens==='in')return e.target===selected&&e.source!==selected;
 if(lens==='south')return SOUTH_CODES.includes(e.source)&&e.target!==e.source;
 return target==='all'||e.target===target;
}
