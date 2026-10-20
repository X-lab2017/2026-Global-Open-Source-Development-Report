// +Y = latitude; longitude 0 is +Z, east is +X. Geometric helpers; they do not create statistical nodes or relations.
export function latLon(lon,lat,r=1){const a=lon*Math.PI/180,b=lat*Math.PI/180;return [r*Math.cos(b)*Math.sin(a),r*Math.sin(b),r*Math.cos(b)*Math.cos(a)];}
export function arcPoint(a,b,t,height=.18){const dot=Math.max(-1,Math.min(1,a.reduce((s,v,i)=>s+v*b[i],0))),angle=Math.acos(dot);let v;if(angle<1e-7)v=a.slice();else if(Math.PI-angle<1e-6){let q=[-a[1],a[0],0];if(Math.hypot(...q)<1e-6)q=[0,-a[2],a[1]];const n=Math.hypot(...q);v=a.map((x,i)=>x*Math.cos(Math.PI*t)+q[i]/n*Math.sin(Math.PI*t));}else{const denom=Math.sin(angle);v=a.map((x,i)=>(Math.sin((1-t)*angle)*x+Math.sin(t*angle)*b[i])/denom);}const norm=Math.hypot(...v)||1,r=1.018+height*Math.sin(Math.PI*t);return v.map(x=>x/norm*r);}
export function localLoop(lon,lat,t){const a=2*Math.PI*t;return latLon(lon+11*Math.sin(a),lat+6*(1-Math.cos(a)),1.026+.14*Math.sin(Math.PI*t));}

// Isolated fictional mechanism, restored from the previous reviewed web version.
const centers=[[105,30],[20,48],[-105,34],[-54,-15],[25,-12],[120,-8]];
export const DEMO_NODES=centers.flatMap(([lon,lat],c)=>[
 ...Array.from({length:16},(_,i)=>({id:`D${c*16+i+1}`,name:`示意开发者 ${c*16+i+1}`,type:'developer',lon:lon+Math.cos(i*2.4)*(8+i*.65),lat:lat+Math.sin(i*2.4)*(6+i*.45)})),
 ...Array.from({length:3},(_,i)=>({id:`P${c*3+i+1}`,name:`示意共享项目 ${c*3+i+1}`,type:'project',lon:lon-17+i*15,lat:lat-15+i*15}))
]);
// Four distinct projects per developer: local communities, bridges and shared hubs.
export const DEMO_EDGES=Array.from({length:96},(_,i)=>{
 const local=Math.floor(i/16)*3+i%3,ps=[...new Set([local,(local+1)%18,(i*5+3)%18,(i%3)*6])];
 for(let j=0;ps.length<4;j++)if(!ps.includes((local+j+4)%18))ps.push((local+j+4)%18);
 return ps.map((p,j)=>[`D${i+1}`,`P${p+1}`,1+(i+j*2)%5,(i+j)%4!==0]);
}).flat();
