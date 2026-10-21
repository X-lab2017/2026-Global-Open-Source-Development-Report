/* Reading contracts and independent interactions around unchanged source data. */
const fs=require('fs'),path=require('path'),assert=require('assert'),{JSDOM}=require('jsdom');
const out=path.resolve(process.argv[2]||'_site'),read=f=>fs.readFileSync(path.join(out,f),'utf8');
const dom=new JSDOM(read('2026/zh/chapters/04/index.html'),{url:'https://example.test/',runScripts:'outside-only',pretendToBeVisual:true}),w=dom.window,d=w.document,errors=[];
w.matchMedia=()=>({matches:false,addEventListener(){}});w.ResizeObserver=class{observe(){}};w.HTMLElement.prototype.scrollIntoView=function(){};w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'))};w.addEventListener('error',e=>errors.push(e.message));for(const f of ['landscape-atlas.js','landscape.js'])w.eval(read(f));
const $=s=>d.querySelector(s),$$=s=>[...d.querySelectorAll(s)];let n=0;const ok=(v,m)=>{assert(v,m);assert.deepEqual(errors,[]);n++},click=s=>{$(s).dispatchEvent(new w.MouseEvent('click',{bubbles:true}));assert.deepEqual(errors,[])},change=(s,v)=>{$(s).value=v;$(s).dispatchEvent(new w.Event('change',{bubbles:true}));assert.deepEqual(errors,[])};
ok($$('#ch04-s01 .al-panel').length===13,'all thirteen reviewed views retained');
$$('#ch04-s01 .al-panel').forEach((p,i)=>{ok(p.querySelectorAll('.lp-caption').length===1,'one caption');ok(p.querySelector('h4').textContent.startsWith('图 4-1-'+(i+1)+' '),'continuous numbered titles');ok(!!p.querySelector('.al-view svg'),'rendered SVG');ok(p.querySelector('.lp-caption').compareDocumentPosition(p.querySelector('.al-view'))&w.Node.DOCUMENT_POSITION_PRECEDING,'caption below graphic');if(i>=8)ok(!!p.querySelector('.al-sim'),'visible simulation badge');let svg=p.querySelector('.al-view svg'),h=svg.viewBox?.baseVal?.height||Number(svg.getAttribute('viewBox').split(' ')[3]);ok([...svg.querySelectorAll('text[y]')].every(t=>Number(t.getAttribute('y'))<=h),'no text below viewbox');});
ok($$('#ch04-s01 .lp-source').length===1,'one source entry');ok(!$('#ch04-s01 [data-csv]')&&!$('#ch04-s01 [data-svg]'),'technical export controls removed');ok(!$('#ch04-s01 .al-source'),'repeated source footers removed');ok(!/评审版|用于评审|深入样章/.test($('#ch04-s01').textContent),'reader copy cleaned');ok($$('[data-atlas-project]').length===145,'all map projects retained');
click('#al-agent [data-expand]');ok($('#al-fullscreen-body .lp-caption').textContent.includes('图 4-1-1'),'caption moves into fullscreen');click('#al-fullscreen .al-close');ok(!!$('#land-map #al-agent'),'panel restored');
change('#al-agent [data-atlas-month]','6');ok($('#al-agent .al-readout').textContent.includes('2025-09'),'local month changes');ok($('#al-model .al-readout').textContent.includes('2026-08'),'other map month unchanged');
click('#al-category-heat [data-action=window][data-value="18"]');ok($('#al-category-heat .al-readout').textContent.includes('2025-03'),'18 month window');
click('#al-concentration [data-action=scope][data-value="Model Infra"]');ok($('#al-concentration .al-view svg').textContent.includes('推理引擎'),'model concentration');click('#al-concentration [data-action=scope][data-value="all"]');ok($('#al-concentration .al-view svg').getAttribute('viewBox').endsWith('780'),'25 rows receive sufficient height');
ok($('#al-shift .al-readout').textContent.includes('107 个项目'),'107 project common cohort');click('#al-shift [data-action=window][data-value="18"]');ok($('#al-shift .al-readout').textContent.includes('18 个月'),'shift independent window');
const data=JSON.parse($('#landscape-data').textContent),M=w.LandscapeModel(data);ok(Math.abs(M.country('all','all',12,17).reduce((s,r)=>s+r.share,0)-1)<1e-12,'sim denominator includes all');ok(M.categories('all',17).reduce((s,r)=>s+r.coverage,0)===140,'latest coverage');
// Dense histories must retain the observations and independent scopes after regrouping.
ok($$('#al-category-heat rect[fill-opacity]').length===12*18,'all Agent category/month cells retained');
click('#al-category-heat [data-action=scope][data-value="Model Infra"]');
ok($$('#al-category-heat rect[fill-opacity]').length===13*18,'all Model category/month cells retained');
for(const [i,month] of data.months.entries())for(const r of M.categories('Model Infra',i)){
  ok($$('#al-category-heat .al-view title').some(t=>t.textContent===`${r.name} · ${month} · 第 ${r.rank} 位 · 覆盖 ${r.coverage}/${r.count}`),'matrix preserves exact rank and coverage');
}
ok($$('#al-category-trend .al-view text').filter(t=>t.textContent==='4,000').length===3,'three category facets share 0–4000 scale');
ok($$('#al-category-trend .al-view circle').length===36,'all 12 monthly values for each leading category retained');
click('#al-category-trend [data-action=metric][data-value="rank"]');
ok($$('#al-category-trend .al-view text').filter(t=>t.textContent==='25').length===3,'category rank facets share whole-sample denominator');
click('#al-category-trend [data-action=metric][data-value="value"]');
ok($$('#al-project-rank [data-action=open-project]').length===8,'all eight inference projects compared');
ok($('#al-project-rank .al-view').textContent.includes('0—800'),'project rows share one value scale');
const omni=$$('#al-project-rank [data-action=project-month]').filter(t=>t.getAttribute('aria-label').startsWith('vLLM Omni · '));
ok(omni.length===11&&!omni.some(t=>t.getAttribute('aria-label').includes('2025-10')),'missing project month remains absent');
click('#al-project-rank [data-action=project-month][data-value="6"]');
ok($('#al-project-rank .al-view').textContent.includes('2025-09 位次 / 项目'),'project point changes selected ranking month');
ok($('#al-category-rank .al-readout').textContent.includes('2026-08'),'project month does not change category ranking');
click('#al-project-rank [data-action=project-category][data-value="Agentic coding"]');
click('#al-project-rank [data-action=page][data-value="1"]');
ok($$('#al-project-rank [data-action=open-project]').length===8&&$('#al-project-rank .al-project-toolbar').textContent.includes('2 / 2'),'second project page remains available');
click('#al-project-rank [data-action=view][data-value="compare"]');
ok(!!$('#al-project-rank [data-action=pick-project]'),'optional overlay comparison remains available');
ok($$('#al-country-trend .al-view circle[tabindex]').length===2*4*12,'four countries in both monthly layer histories');
const share=(layer,code)=>M.country(layer,'all','month',17).find(r=>r.code===code).share;
for(const layer of ['Agent Infra','Model Infra']){
  ok(Math.abs(M.country(layer,'all','month',17).reduce((s,r)=>s+r.share,0)-1)<1e-12,'each layer keeps all nine sources in its denominator');
  for(const code of ['US','CN','DE','GB'])ok($('#al-country-trend .al-view').textContent.includes((share(layer,code)*100).toFixed(1)+'%'),'endpoint shares match full layer calculation');
}
for(const code of ['US','CN','DE','GB']){const diff=(share('Agent Infra',code)-share('Model Infra',code))*100;ok($('#al-country-trend .al-view').textContent.includes((diff>0?'+':'')+diff.toFixed(1)),'layer comparison preserves percentage-point difference');}
click('#al-country-trend [data-action=countries-none]');ok($('#al-country-trend .al-view').textContent.includes('选择国家查看趋势'),'empty country selection has an explanation');
click('#al-country-trend [data-action=countries-all]');ok($$('#al-country-trend .al-view circle[tabindex]').length===2*9*12,'all sources including other and unknown remain explorable');
click('#al-country-trend [data-action=countries-reset]');ok($$('#al-country-trend .al-view circle[tabindex]').length===2*4*12,'reset restores four-country comparison');
click('#al-country-trend [data-action=view][data-value="single"]');ok($$('#al-country-trend .al-view circle[tabindex]').length===4*12,'single-scope exploration retained');
console.log('PASS 4.1 publication: '+n+' reading, geometry, fullscreen, independent filter and simulation checks.');dom.window.close();
