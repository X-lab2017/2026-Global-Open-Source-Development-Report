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

const data=JSON.parse($('#gosm-data').textContent),paperDir=process.argv[3];
if(paperDir)fs.mkdirSync(paperDir,{recursive:true});
ok($$('#ch05-s02 .s52-panel').length===3,'three figures retained');
ok($$('#ch05-s02 .s52-source').length===1&&!$('#ch05-s02 [data-gm-source]'),'one common source entrance');
for(const [i,p] of $$('#ch05-s02 .s52-panel').entries()){
 ok(p.querySelector('h3').textContent.startsWith('图 5-2-'+(i+1)+' '),'numbered caption');
 ok(p.querySelector('.s52-figure-caption').compareDocumentPosition(p.querySelector('.gm-view'))&w.Node.DOCUMENT_POSITION_PRECEDING,'caption below');
 const paper=p.querySelector('.s52-print-view svg');
 ok(paper&&!paper.querySelector('[data-gm-action]'),'static projection has no controls');
 ok([...paper.querySelectorAll('text')].every(t=>+t.getAttribute('font-size')>=14&&+t.getAttribute('font-size')<=19),'print type range');
 if(paperDir)fs.writeFileSync(path.join(paperDir,p.dataset.gmChart+'.svg'),new w.XMLSerializer().serializeToString(paper));
}
const headPaper=$('#gm-head .s52-print-view svg'),headBox=headPaper.getAttribute('viewBox').split(' ').map(Number);
ok(headBox[2]<headBox[3],'head publication uses portrait reflow');
ok(headPaper.textContent.includes('其他已识别 1')&&headPaper.textContent.includes('归属未知 330'),'small segment values retained');
ok($('#gm-network').gmRows.length===5116,'all 5111 relations and five growth rows export');
ok($$('#gm-network .gm-view .s52-node').length===5777,'full network preserved');
ok($('#gm-network .gm-view').textContent.includes('85.87')&&$('#gm-network .gm-view').textContent.includes('28.04'),'precise growth values visible');
click('#gm-network [data-gm-action="view"][data-value="concept"]');ok($('#gm-network .gm-view').textContent.includes('关系示意'),'concept clearly marked');
click('#gm-network [data-gm-action="view"][data-value="overview"]');
const input=$('#gm-network input');input.value='Qwen';input.dispatchEvent(new w.Event('input',{bubbles:true}));
ok($$('#gm-network [data-gm-action="searchNode"]').length>0,'search results');click('#gm-network [data-gm-action="searchNode"]');
ok($('#gm-network .gm-view').textContent.includes('直接上游'),'search focuses a model');
click('#gm-network [data-gm-action="neighbors"][data-value="up"]');click('#gm-network [data-gm-action="clearNode"]');
ok($('#gm-network').gmRows.length===5116,'search/reset preserves complete export');
click('#gm-network [data-gm-action="year"][data-value="2025-09-13"]');ok($('#gm-network .gm-view').textContent.includes('56.38万'),'year changes growth only');
ok($$('#gm-network .gm-view .s52-node').length===5777,'year does not invent network history');
click('#gm-network [data-gm-action="year"][data-value="2026-09-13"]');
ok($('#gm-flows').gmRows.reduce((n,r)=>n+r['关系对数'],0)===10943,'complete directional total');
ok($('#gm-flows .gm-view').textContent.includes('中国 5,888')&&$('#gm-flows .gm-view').textContent.includes('美国 7,513'),'national quantities labelled');
click('#gm-flows [data-gm-action="focus"][data-value="CN"]');change('#gm-flows [data-s52-select="direction"]','out');
ok($('#gm-flows').gmRows.reduce((n,r)=>n+r['关系对数'],0)===5888,'China outgoing direction');
for(const group of [6,8,10]){click('#gm-flows [data-gm-action="group"][data-value="'+group+'"]');ok($('#gm-flows').s52Aggregated.edges.reduce((n,r)=>n+r.weight,0)===5888,'aggregation lossless '+group)}
change('#gm-flows [data-s52-select="direction"]','both');click('#gm-flows [data-gm-action="focus"][data-value="all"]');
click('#gm-flows [data-gm-action="flowPair"][data-value="CN|US"]');ok($('#gm-flows .gm-view').textContent.includes('4,639'),'fixed detail retains direction');
click('#gm-flows [data-gm-action="flowClear"]');
for(const k of [20,100,1000]){click('#gm-head [data-gm-action="k"][data-value="'+k+'"]');ok($('#gm-head .gm-view').textContent.includes('Top '+k+' · 月度变化'),'depth '+k)}
click('#gm-head [data-gm-action="bands"][data-value="segments"]');ok($('#gm-head .gm-view').textContent.includes('第101—1000名'),'nonoverlapping segments');
click('#gm-head [data-gm-action="bands"][data-value="cumulative"]');click('#gm-head [data-gm-action="k"][data-value="100"]');
click('#gm-head [data-gm-action="month"][data-value="2024-07"]');ok($('#gm-head .gm-view').textContent.includes('中国 7 席　美国 66 席'),'historical month');
change('#gm-head [data-s52-select="months"]','6');ok($('#gm-head .gm-view').textContent.includes('2026-08'),'window resets outside month');
click('#gm-head [data-gm-action="mode"][data-value="share"]');click('#gm-head [data-gm-action="unknown"]');
ok($('#gm-head .gm-view').textContent.includes('未知始终计入分母'),'unknown denominator stays');
change('#gm-head [data-s52-select="months"]','26');ok($('#gm-head').gmRows.length===78,'all month/depth records retained');
for(const id of ['network','flows','head']){
 const p=$('#gm-'+id),trigger=p.querySelector('[data-gm-full]');trigger.focus();click('#gm-'+id+' [data-gm-full]');
 ok(!!$('#gm-fullscreen[open] #gm-'+id+' .s52-figure-caption'),'fullscreen caption');click('[data-gm-close]');
 ok(p.closest('#ch05-s02')&&d.activeElement===trigger,'return restores location and focus');
 click('#gm-'+id+' [data-gm-table]');ok(p.querySelector('.gm-table').open&&p.querySelector('table'),'table opens');
 d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));ok(!p.querySelector('.gm-table').open,'Escape closes');
 click('#gm-'+id+' [data-gm-svg]');click('#gm-'+id+' [data-gm-csv]');
}
ok(downloads.length===6,'all static SVG and CSV exports');
ok($('#gm-cnus').dataset.gmReady==='true'&&$('#gm-openness').dataset.gmReady==='true','adjacent sections still render');
console.log('PASS 5.2 publication: '+n+' source, graph, flow, history, print, fullscreen and export checks.');dom.window.close();
