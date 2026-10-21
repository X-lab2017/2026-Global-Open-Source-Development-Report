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
ok($$('#ch05-s01 .s51-panel').length===3,'three retained figures');
ok($$('#ch05-s01 .s51-source').length===1&&!$('#ch05-s01 [data-gm-source]'),'one methodology entrance');
for(const [i,p] of $$('#ch05-s01 .s51-panel').entries()){
 ok(p.querySelector('h3').textContent.startsWith('图 5-1-'+(i+1)+' '),'consistent numbered caption');
 ok(!!p.querySelector('.gm-view svg'),'rendered figure');
 ok(p.querySelector('.s51-caption').compareDocumentPosition(p.querySelector('.gm-view'))&w.Node.DOCUMENT_POSITION_PRECEDING,'caption below figure');
 ok([...p.querySelectorAll('svg text[y]')].every(t=>Number(t.getAttribute('y'))<=560),'labels within canvas height');
}
ok($('#gm-world .gm-view').textContent.includes('+58.3%')&&$('#gm-world .gm-view').textContent.includes('+48.4%'),'default view supports both annual findings');
click('#gm-world [data-gm-action="months"][data-value="6"]');ok($('#gm-world .gm-view').textContent.includes('截至2026-07'),'monthly alternative retained');
click('#gm-world [data-gm-action="country"][data-value="CN"]');click('#gm-world [data-gm-action="list"][data-value="organizations"]');ok($('#gm-world .gm-view').textContent.includes('Qwen'),'country to publisher drilldown');
click('#gm-world [data-gm-action="asset"][data-value="datasets"]');ok($('#gm-world .gm-view').textContent.includes('配套数据集'),'asset switch keeps drilldown');
click('#gm-world [data-gm-action="clear"]');ok($('#gm-world .gm-view').textContent.includes('国家与地区'),'reset restores country view');
ok(!$('#gm-cnus [data-s51-select="detail"]')&&!$('#gm-cnus [data-s51-select="mode"]'),'ranking-only controls');
ok(!$('#gm-cnus .gm-view').textContent.includes('%')&&!$('#gm-cnus .gm-view').textContent.includes('累计份额')&&!$('#gm-cnus .gm-view').textContent.includes('同一地域组织样本'),'no share cards, curves or sample banners');
ok($$('#gm-cnus [data-s51-row]').length===16,'eight accounts per country');
ok($('#gm-cnus').gmRows.length===497&&$('#gm-cnus').gmRows.every(r=>r['对象类型']==='发布账号'),'complete unpaged ranking export');
const qwen=$('#gm-cnus [data-s51-row="Qwen"]'),sentence=$('#gm-cnus [data-s51-row="sentence-transformers"]');
const qv=$('#gm-cnus').gmRows.find(r=>r['账号']==='Qwen')['数值'],sv=$('#gm-cnus').gmRows.find(r=>r['账号']==='sentence-transformers')['数值'];
ok(Math.abs(Number(qwen.querySelector('rect').getAttribute('width'))/Number(sentence.querySelector('rect').getAttribute('width'))-qv/sv)<1e-9,'both countries share one absolute scale');
const baaiWidth=$('#gm-cnus [data-s51-row="BAAI"] rect').getAttribute('width');
const query=value=>{const el=$('#gm-cnus input');el.value=value;el.dispatchEvent(new w.Event('input',{bubbles:true}));assert.deepEqual(errors,[])};
query('BAAI');ok($('#gm-cnus [data-s51-row="BAAI"]').dataset.s51Rank==='2'&&$('#gm-cnus [data-s51-row="BAAI"] rect').getAttribute('width')===baaiWidth,'search preserves rank and scale');
ok($('#gm-cnus').gmRows[0]['排名']===2,'filtered export preserves original rank');
query('no-such-publisher');ok($('#gm-cnus .gm-view').textContent.includes('没有匹配账号'),'search empty state');
query('');click('#gm-cnus [data-gm-action="pageCN"][data-value="next"]');ok($('#gm-cnus [data-s51-row]').dataset.s51Rank==='9'&&$('#gm-cnus').gmRows.length===497,'independent page retains full export');
click('#gm-cnus [data-gm-action="asset"][data-value="datasets"]');ok($('#gm-cnus .gm-view').textContent.includes('InternRobotics')&&$('#gm-cnus .gm-view').textContent.includes('allenai'),'dataset ranking resets pagination');
change('#gm-cnus [data-s51-select="metric"]','count');ok($('#gm-cnus').gmRows.find(r=>r['账号']==='InternRobotics')['指标']==='配套数据集数','quantity ranking available');
change('#gm-cnus [data-s51-select="metric"]','likes');ok($('#gm-cnus').gmRows.every(r=>r['单位']==='赞'),'attention ranking retains unit');
ok($$('#gm-cnus [data-s51-row] a').every(a=>a.getAttribute('href').startsWith('https://huggingface.co/')),'account links retained');
change('#gm-cnus [data-s51-select="metric"]','downloads');click('#gm-cnus [data-gm-action="asset"][data-value="models"]');
click('#gm-china [data-gm-action="province"][data-value="CN-ZJ"]');click('#gm-china [data-gm-action="list"][data-value="organizations"]');ok($('#gm-china .gm-view').textContent.includes('Qwen'),'province to organization drilldown');
click('#gm-china [data-gm-action="clear"]');ok($('#gm-china .gm-view').textContent.includes('149'),'unassigned records retained');
for(const id of ['world','cnus','china']){
 const p=$('#gm-'+id),trigger=p.querySelector('[data-gm-full]');trigger.focus();click('#gm-'+id+' [data-gm-full]');
 ok(!!$('#gm-fullscreen[open] #gm-'+id+' .s51-caption'),'caption retained fullscreen');click('[data-gm-close]');
 ok(p.closest('#ch05-s01')&&d.activeElement===trigger,'panel and focus restored');
 click('#gm-'+id+' [data-gm-table]');ok(p.querySelector('.gm-table').open&&p.querySelector('table'),'data table works without repeated source popup');
 d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));ok(!p.querySelector('.gm-table').open,'table Escape closes');
 click('#gm-'+id+' [data-gm-svg]');click('#gm-'+id+' [data-gm-csv]');
}
ok(downloads.length===6,'all three SVG and CSV exports work');
ok($('#gm-network').dataset.gmReady==='true'&&$('#gm-openness').dataset.gmReady==='true','adjacent sections still render');
console.log('PASS 5.1 publication: '+n+' evidence, caption, independent control, denominator, drilldown, fullscreen, table and export checks.');dom.window.close();
