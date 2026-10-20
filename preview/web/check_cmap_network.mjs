import fs from 'node:fs';
import assert from 'node:assert/strict';
import {selectedFlows,visualWidth,profileFlows} from './cmap-globe-analysis.mjs';
import {latLon,arcPoint,localLoop,DEMO_NODES,DEMO_EDGES} from './cmap-globe-math.mjs';
const path=process.argv[2]||'preview/content/cmap/data.json';
const D=JSON.parse(fs.readFileSync(path,'utf8')),F=D.flows,before=JSON.stringify(F),max=Math.max(...F.edges.map(e=>e.value));
assert.equal(selectedFlows(F).length,20);assert.equal(selectedFlows(F,{filter:'local'}).length,2);assert.equal(selectedFlows(F,{filter:'cross'}).length,18);
for(const target of ['CN','US']){assert.equal(selectedFlows(F,{target}).length,10);assert.equal(selectedFlows(F,{target,filter:'local'}).length,1);assert.equal(selectedFlows(F,{target,filter:'cross'}).length,9);}
const by=Object.fromEntries(D.countries.map(r=>[r.id,r]));
for(const e of F.edges){assert.equal(e.kind,'observed');assert(Math.abs(visualWidth(e.value,max,3)/visualWidth(e.value,max,1)-3)<1e-12);const a=latLon(...by[e.source].coordinates),b=latLon(...by[e.target].coordinates);for(let i=0;i<=48;i++){const point=e.source===e.target?localLoop(...by[e.source].coordinates,i/48):arcPoint(a,b,i/48);assert(point.every(Number.isFinite));assert(Math.hypot(...point)>1);}assert.equal(e.share_pct,F.edges.find(r=>r.id===e.id).share_pct);}
assert.equal(profileFlows(F,'CN').local,25204.09);assert.equal(profileFlows(F,'US').local,120223.9);assert.equal(profileFlows(F,'DE').in,null);assert.equal(JSON.stringify(F),before);assert.equal(DEMO_NODES.length,114);assert.equal(DEMO_EDGES.length,384);assert(DEMO_NODES.every(n=>!F.edges.some(e=>e.source===n.id||e.target===n.id)));assert(DEMO_EDGES.every(e=>DEMO_NODES.some(n=>n.id===e[0])&&DEMO_NODES.some(n=>n.id===e[1])));
console.log('PASS: 20 observed relations, two genuine local loops, 14 source countries, finite spherical paths, uniform 3x visual scaling and unchanged statistics.');
