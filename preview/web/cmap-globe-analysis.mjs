// All calculations use original records. Display multipliers never alter statistics.
export function selectedFlows(F,{target='all',filter='all'}={}){
 return F.edges.filter(e=>(target==='all'||e.target===target)&&(filter==='all'||(filter==='local')===(e.source===e.target))).sort((a,b)=>b.value-a.value);
}
export function visualWidth(value,maximum,multiplier=1){return .006*Math.sqrt(value/maximum)*multiplier;}
export function profileFlows(F,code){
 const out=F.edges.filter(e=>e.source===code&&e.target!==code),incoming=F.edges.filter(e=>e.target===code&&e.source!==code),local=F.edges.find(e=>e.target===code&&e.source===code),sum=rr=>rr.reduce((v,e)=>v+e.value,0);
 return {out:out.length?sum(out):null,in:F.targets[code]?sum(incoming):null,local:local?.value??null};
}
