/* Publication contracts: true/default scope, original ranks, sample denominators, simulations. */
const fs=require('fs'),path=require('path'),assert=require('assert'),{JSDOM}=require('jsdom');
const out=path.resolve(process.argv[2]||'_site'),read=f=>fs.readFileSync(path.join(out,f),'utf8');
const dom=new JSDOM(read('2026/zh/chapters/03/index.html'),{url:'https://example.test/2026/zh/chapters/03/',runScripts:'outside-only',pretendToBeVisual:true}),w=dom.window,d=w.document,errors=[];
w.ResizeObserver=class{observe(){}};w.matchMedia=()=>({matches:true});w.HTMLElement.prototype.scrollIntoView=function(){};w.addEventListener('error',e=>errors.push(e.message));
for(const f of ['company-ranking.js','ranking-details.js','rankings.js'])w.eval(read(f));
const $=s=>d.querySelector(s),$$=s=>[...d.querySelectorAll(s)],main='#fig-3-4-1',aux='#fig-3-4-2',sim='#fig-3-4-3';let checks=0;
const ok=(v,m)=>{assert(v,m);assert.deepEqual(errors,[]);checks++},click=s=>{assert($(s),s);$(s).click();assert.deepEqual(errors,[])},change=(s,v)=>{$(s).value=v;$(s).dispatchEvent(new w.Event('change',{bubbles:true}));assert.deepEqual(errors,[])};
ok($(main+' select[data-rr-setting=evidence]').value==='report_source','default real records');ok($(main+' .cr-pagination').textContent.includes('/ 30'),'default total 30');
click(main+' [data-rr-page="2"]');ok($(main+' .cr-rank-no').textContent==='21','source ranks persist on third page');
click(main+' [data-rr-action=reset]');click(main+' [data-rr-sort=active_developers]');ok($(main+' .cr-rank-no').textContent==='25','secondary sort retains original rank');
change(main+' [data-rr-setting=evidence]','simulated');ok($(main+' .cr-head-right').textContent.includes('模拟'),'persistent simulation notice');ok($$(main+' .cr-rank-row').every(r=>r.dataset.evidence==='simulated'),'simulation filter isolated');
click(main+' [data-rr-action=reset]');ok($(main+' [data-rr-setting=evidence]').value==='report_source','reset returns real sample');
click(main+' [data-rr-scope=chinaProject]');ok($(main+' .cr-pagination').textContent.includes('/ 30'),'independent China 30');ok($(main+' .cr-body').textContent.includes('14,719.47'),'China source precision');
click(main+' [data-rr-view=compare]');ok($$(main+' .cr-comparison-table thead th').length===4,'three China project comparison');
click(aux+' [data-rr-view=country]');ok($$(aux+' tbody tr').length===13,'12 countries and unknown');ok($(aux+' tbody tr:last-child').textContent.includes('未识别'),'unknown retained last');ok($$(aux+' tbody tr').reduce((n,r)=>n+Number(r.querySelectorAll('td')[2].textContent.trim()),0)===100,'independent country denominator');
click(aux+' [data-rr-view=domain]');ok($(aux+' .pr-aux-caption').textContent.includes('30'),'domain default denominator');ok($$(aux+' tbody tr').reduce((n,r)=>n+Number(r.querySelectorAll('td')[1].textContent.trim()),0)===30,'domains sum30');
change(aux+' [data-rr-setting=auxScope]','review');ok($(aux+' .cr-head-right').textContent.includes('模拟'),'mixed domain warning');ok($$(aux+' tbody tr').reduce((n,r)=>n+Number(r.querySelectorAll('td')[1].textContent.trim()),0)===100,'mixed sample explicitly 100');
click(aux+' [data-rr-view=rising]');ok($(aux+' .cr-toolbar').textContent.includes('基期日期待确认'),'baseline missing explicit');ok($(aux+' .cr-body').textContent.includes('14,719.50'),'rising source precision differs');
ok($$(sim+' .pr-stack').length===10,'10 source projects');for(const s of $$(sim+' .pr-stack'))ok(Math.abs([...s.children].reduce((n,c)=>n+parseFloat(c.style.width),0)-100)<.001,'complete country shares');
click(sim+' [data-pr-contribution=OpenHarmony]');ok($(sim+' .pr-detail').textContent.includes('16,000'),'same simulation total');ok($(sim+' .pr-detail').textContent.includes('65.0%'),'same simulated China share');
change(sim+' [data-rr-setting=contributionProject]','NixOS');ok($(sim+' .pr-insight').textContent.includes('未识别份额可能改变'),'ambiguous first source not asserted');
for(const f of [main,aux,sim]){ok($$(f+' .rp-caption').length===1,'one bottom caption');ok(!$(f+' [data-rr-action=source]'),'no repeated source control');}
ok(!/NaN|undefined/.test($('#ch03-s04').innerHTML),'no invalid values');console.log('PASS project publication: '+checks+' scope, precision, simulation and reading checks');dom.window.close();
