/* Verifies evidence boundaries and map-state behavior without a browser. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const C=require('./atlas-core.js'),root=path.resolve(__dirname,'..'),out=path.resolve(process.argv[2]||path.join(root,'dist'));
const data=JSON.parse(fs.readFileSync(path.join(out,'assets/goso-atlas/map-data.json'))),geo=JSON.parse(fs.readFileSync(path.join(out,'assets/goso-atlas/geometry.json')));
const ids=Object.fromEntries(Object.entries(geo).map(([k,fs])=>[k,new Set(fs.map(x=>x.id))]));
for(const [scope,features] of Object.entries(geo))assert.equal(features.length,ids[scope].size);
for(const [key,set] of Object.entries(data.snapshot.sets)){
 const scope=key.split('-').at(-1),expected=scope==='china'?34:key.startsWith('influence')?29:100;assert.equal(set.rows.length,expected,key);
 for(const row of set.rows){assert(ids[scope].has(row.id),row.name);assert(Number.isFinite(row.value)&&row.value>=0);assert(row.display);}
}
assert(!data.snapshot.sets['influence-china']);
assert.equal(C.normalize('i',{metric:'influence',scope:'china'}).scope,'world');
assert.equal(C.normalize('t',{year:1999}).year,2026);
assert.equal(C.normalize('a',{metric:'<script>',scope:'china'}).metric,'models');
assert.equal(C.colorIndex(null,[0,20]),-1);assert.notEqual(C.colorIndex(0,[0,20]),-1);
for(const kind of 'vcitda'){
 const st=C.normalize(kind);const rows=C.records(data,kind,st);assert(rows.length);
 for(const row of rows)assert(ids[st.scope].has(row.id)||kind==='t');
}
assert.equal(C.records(data,'v',C.normalize('v',{scope:'china'})).length,34);
assert.equal(C.records(data,'i',C.normalize('i')).length,29);
assert.equal(C.records(data,'t',C.normalize('t',{year:2022})).find(r=>r.id==='成都').value,126);
assert.equal(C.records(data,'t',C.normalize('t',{year:2026})).find(r=>r.id==='成都').value,181);
assert.equal(data.assets.length,52);assert.equal(data.assets.reduce((n,r)=>n+r.models,0),71578);
assert.equal(C.records(data,'a',C.normalize('a',{metric:'downloads'})).find(r=>r.id==='CN').value,7250795572);
for(const target of ['CN','US']){let rows=C.records(data,'d',C.normalize('d',{target}));assert.equal(rows.length,10);assert.equal(rows.reduce((s,r)=>s+r.share,0).toFixed(2),target==='CN'?'93.24':'77.94');}
const originals=JSON.parse(fs.readFileSync(path.join(out,'assets/goso-atlas/originals.json')));assert.equal(Object.values(originals).reduce((s,o)=>s+o.images.length,0),24);
for(const o of Object.values(originals))for(const image of o.images)assert(fs.statSync(path.join(out,'assets/goso-atlas/original',image.file)).size>0);
console.log('PASS: geography mappings, 431 source snapshot rows, 20 contribution flows, 10 cities, 52 known model countries, null/zero handling, state guards, 24 original figures.');

assert(ids.world.has('CN'));for(const id of ['TW','HK','MO'])assert(!ids.world.has(id));assert(ids.china.has('710000'));assert.equal(geo.world.find(f=>f.id==='CN').components.length,4);

// Brand scale: P95 cap, finite missing values, unchanged real readings.
assert.equal(C.colorCap(Array.from({length:100},(_,i)=>i+1)),96);assert.equal(C.colorIndex(100,[1,2,3,4,100]),5);assert.equal(C.colorIndex(NaN,[1,2]),-1);
