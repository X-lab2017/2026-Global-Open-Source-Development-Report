/* Publication regression: supplied evidence, navigation and independent controls. */
const fs=require('fs'),path=require('path'),assert=require('assert'),{JSDOM}=require('jsdom');
const out=path.resolve(process.argv[2]||'_site'),read=f=>fs.readFileSync(path.join(out,f),'utf8');
const dom=new JSDOM(read('2026/zh/chapters/05/index.html'),{url:'https://example.test/',runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window,d=w.document,errors=[],downloads=[];
w.matchMedia=()=>({matches:false,addEventListener(){}});w.ResizeObserver=class{observe(){}};
w.HTMLElement.prototype.scrollIntoView=function(){};w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'))};
w.URL.createObjectURL=b=>{downloads.push(b);return 'blob:qa'};w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
w.addEventListener('error',e=>errors.push(e.message));
for(const f of ['assets/amap/d3.min.js','gosm-supply.js','gosm-influence.js','gosm-openness.js','gosm.js'])w.eval(read(f));
const $=s=>d.querySelector(s),$$=s=>[...d.querySelectorAll(s)];let n=0;
const ok=(v,m)=>{assert(v,m);assert.deepEqual(errors,[]);n++};
const click=s=>{const el=$(s);assert(el,s);el.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));assert.deepEqual(errors,[])};
const change=(s,v)=>{const el=$(s);el.value=v;el.dispatchEvent(new w.Event('change',{bubbles:true}));assert.deepEqual(errors,[])};

const data=w.GOSM.data,paperDir=process.argv[3];if(paperDir)fs.mkdirSync(paperDir,{recursive:true});
function save(id,name){const svg=$('#gm-'+id+' .s53-print-view svg');ok(svg&&!svg.querySelector('[data-gm-action]'),'static SVG without controls '+name);ok([...svg.querySelectorAll('text')].every(t=>+t.getAttribute('font-size')>=14&&+t.getAttribute('font-size')<=19),'publication type range '+name);if(paperDir)fs.writeFileSync(path.join(paperDir,name+'.svg'),new w.XMLSerializer().serializeToString(svg));}
ok($$('#ch05-s03 .s53-panel').length===3,'three figures');ok($$('#ch05-s03 .s53-source').length===1&&!$('#ch05-s03 [data-gm-source]'),'one common method entrance');
for(const [i,p] of $$('#ch05-s03 .s53-panel').entries()){ok(p.querySelector('h3').textContent.startsWith('图 5-3-'+(i+1)+' '),'caption number');ok(p.querySelector('.s53-figure-caption').compareDocumentPosition(p.querySelector('.gm-view'))&w.Node.DOCUMENT_POSITION_PRECEDING,'caption below figure');}
ok($('#gm-framework .gm-framework-caption').compareDocumentPosition($('#gm-framework .gm-view'))&w.Node.DOCUMENT_POSITION_PRECEDING,'opening caption below the chart');
ok($('#gm-framework .gm-framework-print svg')&&!$('#gm-framework .gm-framework-print [data-gm-action]'),'framework has a publication view');
if(paperDir)fs.writeFileSync(path.join(paperDir,'framework.svg'),new w.XMLSerializer().serializeToString($('#gm-framework .gm-framework-print svg')));
save('openness','standard');
click('#gm-openness [data-gm-action="overviewLevel"][data-value="5"]');click('#gm-openness [data-gm-action="standardDetails"]');
ok($('#gm-openness .gm-source').open&&$$('#gm-openness .s53-rules ol li').length===19,'complete 19 material requirements');
d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));ok(!$('#gm-openness .gm-source').open,'Escape closes standard');
click('#gm-openness [data-gm-action="overviewO"][data-value="2"]');ok($('#gm-openness .gm-view').textContent.includes('相同或兼容许可'),'O2 obligations retained');
click('#gm-openness [data-gm-action="view"][data-value="sample"]');save('openness','sample');
ok($('#gm-openness').gmRows.reduce((n,r)=>n+r['模型数'],0)===870,'report total 870');
click('#gm-openness [data-gm-action="sample"][data-value="current"]');ok($('#gm-openness').gmRows.reduce((n,r)=>n+r['模型数'],0)===884,'separate platform 884');
click('#gm-openness [data-gm-action="sample"][data-value="report"]');
save('open-groups','regions');ok($('#gm-open-groups').gmRows.reduce((n,r)=>n+r['本组样本数'],0)===870,'five groups sum 870');
click('#gm-open-groups [data-gm-action="regionToggle"][data-value="归属未知"]');ok($('#gm-open-groups').gmRows.length===4&&$('#gm-open-groups').gmRows[0]['本组样本数']===404,'filter does not change denominators');
click('#gm-open-groups [data-gm-action="allRegions"]');
click('#gm-open-groups [data-gm-action="mode"][data-value="map"]');save('open-groups','map');
ok($('#gm-open-groups').gmRows.reduce((n,r)=>n+r['模型数'],0)===884,'map uses separate 884');ok($('#gm-open-groups .gm-view').textContent.includes('820'),'known map total');
click('#gm-open-groups [data-gm-action="mapCountry"][data-value="CN"]');ok($('#gm-open-groups .gm-view').textContent.includes('双高'),'country detail');click('#gm-open-groups [data-gm-action="mapClear"]');
change('#gm-open-groups [data-s53-map-metric]','high_open');ok($('#gm-open-groups .gm-view').textContent.includes('按比例线性映射'),'map metric semantics');
save('dossiers','publishers');ok($('#gm-dossiers').gmRows.find(r=>r['主体类型']==='企业')['双高数']===69,'enterprise numerator');
click('#gm-dossiers [data-gm-action="metric"][data-value="high_open"]');ok($('#gm-dossiers .s53-print-view').textContent.includes('462 / 600'),'high-open contribution denominator');
click('#gm-dossiers [data-gm-action="view"][data-value="map"]');click('#gm-dossiers [data-gm-action="mapType"][data-value="community"]');ok($('#gm-dossiers').gmRows.every(r=>r['主体类型']==='社区'),'publisher map type filtering');
click('#gm-dossiers [data-gm-action="view"][data-value="models"]');change('#gm-dossiers [data-s53-pool]','joined');
ok($('#gm-dossiers').gmRows.filter(r=>r['记录类型']==='884平台快照').length===38,'38 complete-ID matches');
change('#gm-dossiers [data-s53-pool]','review');ok($('#gm-dossiers').gmRows.filter(r=>r['记录类型']==='884平台快照').length===22,'22 review records preserved');
change('#gm-dossiers [data-s53-pool]','platform');const input=$('#gm-dossiers [data-s53-search]');input.focus();input.value='OLMo';input.dispatchEvent(new w.Event('input',{bubbles:true}));ok(d.activeElement===$('#gm-dossiers [data-s53-search]'),'search preserves focus');ok($('#gm-dossiers').gmRows.filter(r=>r['记录类型']==='884平台快照').every(r=>r['模型ID'].toLowerCase().includes('olmo')),'search filters model IDs');
change('#gm-dossiers [data-s53-pool]','cases');click('#gm-dossiers [data-gm-action="model"][data-value="allenai/OLMo-2-1124-7B"]');ok($('#gm-dossiers .s53-print-view').textContent.includes('7df9a82518afdecae4e8c026b27adccc8c1f0032'),'OLMo fixed full commit');click('#gm-dossiers [data-gm-action="model"][data-value="meta-llama/Llama-3.1-8B"]');save('dossiers','case');
ok($('#gm-dossiers .s53-print-view').textContent.includes('d04e592bb4f6aa9cfee91e2e20afa771667e1d4b'),'fixed full commit in publication');
click('#gm-dossiers [data-gm-action="evidence"]');ok(!!$('#gm-dossiers .s53-evidence-sheet'),'case evidence opens');click('#gm-dossiers [data-gm-action="closeEvidence"]');ok(!$('#gm-dossiers .s53-evidence-sheet'),'case evidence closes');
for(const id of ['openness','open-groups','dossiers']){const p=$('#gm-'+id),trigger=p.querySelector('[data-gm-full]');trigger.focus();click('#gm-'+id+' [data-gm-full]');ok(!!$('#gm-fullscreen[open] #gm-'+id+' .s53-figure-caption'),'fullscreen caption');click('[data-gm-close]');ok(p.closest('#ch05-s03')&&d.activeElement===trigger,'return restores location and focus');click('#gm-'+id+' [data-gm-table]');ok(p.querySelector('.gm-table').open&&p.querySelector('table'),'table opens');d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));ok(!p.querySelector('.gm-table').open,'table Escape');click('#gm-'+id+' [data-gm-svg]');click('#gm-'+id+' [data-gm-csv]');}
ok(downloads.length===6,'static SVG and CSV exports');ok($('#gm-head').dataset.gmReady==='true','5.2 still renders');
console.log('PASS 5.3 publication: '+n+' source, reflow, evidence, map, search, fullscreen and export checks.');dom.window.close();
