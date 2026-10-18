/* DOM regressions for original figures and one-canvas presentation, not browser QA. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),{parseHTML}=require('linkedom');
const root=path.resolve(__dirname,'../..'),out=path.resolve(process.argv[2]||root+'/_site');let checks=0;
for(const lang of ['zh','en']){
 const {window}=parseHTML(fs.readFileSync(`${out}/2026/${lang}/chapters/01/index.html`,'utf8')),d=window.document;
 window.console=console;window.URL=URL;window.URLSearchParams=URLSearchParams;window.location=new URL('https://example.test/report/2026/'+lang+'/chapters/01/');window.history={replaceState(a,b,u){window.location=new URL(u,window.location);}};window.requestAnimationFrame=fn=>{fn();return 1;};window.innerWidth=1440;window.innerHeight=900;
 Object.defineProperty(window.HTMLSelectElement.prototype,'value',{get(){return this.getAttribute('data-test-value')||'';},set(v){this.setAttribute('data-test-value',v);},configurable:true});
 window.ResizeObserver=class{observe(){}};window.HTMLElement.prototype.scrollIntoView=function(){};
 Object.defineProperty(window.HTMLElement.prototype,'clientWidth',{get(){return this.classList?.contains('explorer-slide-frame')?(this.closest('dialog')?window.innerWidth:886):800;},configurable:true});
 Object.defineProperty(window.HTMLElement.prototype,'clientHeight',{get(){return this.classList?.contains('explorer-slide-frame')?(this.closest('dialog')?window.innerHeight-52:parseFloat(this.style.height)||550):600;},configurable:true});
 window.HTMLElement.prototype.showModal=function(){this.open=true;};window.HTMLElement.prototype.close=function(){this.open=false;this.dispatchEvent(new window.Event('close'));};
 const context=vm.createContext(window);for(const name of ['chapter-visuals.js','chapter1-explorers.js','reading-experience.js','chapter1-restored.js','report-architecture.js','chapter1-theme-map.js'])vm.runInContext(fs.readFileSync(out+'/'+name,'utf8'),context,{filename:name});
 const q=s=>d.querySelector(s),qa=(s,r=d)=>[...r.querySelectorAll(s)],click=n=>{assert(n,'missing click target');n.click();checks++;};
 assert.equal(qa('.foundation-figure.screen-slide').length,7);assert.equal(qa('.ch1-review-figure,.c1-presentation').length,0);
 assert.equal(qa('[data-logic-chapter]').length,6);for(const b of qa('[data-logic-chapter]')){click(b);assert.equal(b.getAttribute('aria-expanded'),'true');assert(!d.getElementById(b.getAttribute('aria-controls')).hidden);}
 assert.equal(qa('[data-logic-framework]').length,0);click(q('[data-logic-chapter="6"]'));assert.equal(qa('#logic-detail-6 .architecture-section-links a').length,5);click(q('[data-architecture-reset]'));assert(!q('#logic-start').hidden);assert(qa('.logic-detail').every(x=>x.hidden));
 for(const type of ['contributors','organizations']){click(q('[data-linux-kind='+type+']'));assert.equal(qa('.linux-bar').length,10);for(const b of qa('.linux-bar')){click(b);assert(q('#linux-selection').textContent.includes(b.querySelector('.bar-name').textContent.slice(2)));}}
 const model=q('#fig-models'),slider=q('#model-month');assert.equal(qa('[data-month]').length,28);for(let i=0;i<28;i++)click(q('[data-month="'+i+'"]'));assert.equal(q('#model-china-share').textContent,'70');click(q('[data-month="8"]'));const month=q('#model-current-month').textContent;
 click(q('[data-model-story-view=qwen]'));assert(q('#model-story-macro').hidden);assert(!q('#model-story-qwen').hidden);assert.equal(qa('.qwen-story-node').length,5);assert.equal(qa('.qwen-edge').length,4);
 for(const b of qa('[data-qwen-node],[data-qwen-edge]')){click(b);assert.equal(b.getAttribute('aria-pressed'),'true');assert(q('#qwen-story-detail').textContent.includes('2026-10-16'));}
 click(q('[data-model-story-view=macro]'));assert.equal(q('#model-current-month').textContent,month);assert(!q('[data-model-story-scope=macro]').hidden);assert(q('[data-model-story-scope=qwen]').hidden);
 for(const b of qa('[data-sdg],[data-dpg],[data-goal]')){b.dispatchEvent(new window.Event('click'));assert.equal(b.getAttribute('aria-pressed'),'true');checks++;}
 assert.equal(qa('[data-sdg]').length,17);assert.equal(qa('[data-dpg]').length,9);assert.equal(qa('[data-goal]').length,14);
 const codes=new Set();for(const dim of qa('[data-osdi-dimension]')){click(dim);for(const b of qa('[data-screen-indicator]')){click(b);codes.add(b.dataset.screenIndicator);assert(q('.osdi-screen-reading h4').textContent.length);const tabs=qa('.osdi-screen-tabs button');click(tabs[1]);assert.equal(qa('.osdi-evidence-states>div').length,4);assert(q('.osdi-screen-body').textContent.includes('独立复现待核验'));}}
 assert.equal(codes.size,29);click(q('[data-osdi-dimension="3.2"]'));click(q('[data-screen-indicator=ModelRank]'));click(qa('.osdi-screen-tabs button')[1]);assert(q('.osdi-screen-body').textContent.includes('26'));assert(q('.osdi-screen-body').textContent.includes('2024-07'));
 // Seven real elements move into and out of dialogs; no clone, state loss or stale scale.
 const fixtures=[];for(const fig of qa('.foundation-figure.screen-slide')){
  const frame=fig.parentElement,home=frame.parentElement,launch=frame.previousElementSibling.querySelector('.reading-present');assert(launch);
  const title=fig.querySelector('h3,h4').textContent;const dialog=qa('dialog.explorer-presentation').find(n=>n.getAttribute('aria-label')===title);assert(dialog);
  const close=dialog.querySelector('.slide-presentation-bar>button');
  for(const [w,h] of [[1440,900],[1366,768],[1920,1080]]){window.innerWidth=w;window.innerHeight=h;window.dispatchEvent(new window.Event('resize'));const before=fig.style.transform;
   for(let i=0;i<3;i++){click(launch);assert.equal(fig.parentElement,frame);assert.equal(frame.parentElement,dialog);assert(dialog.open);const scale=parseFloat(fig.style.transform.match(/[\d.]+/)[0]);assert(scale*1280<=w+.1);assert(scale*800<=h-52+.1);click(close);assert.equal(frame.parentElement,home);assert.equal(fig.style.transform,before);assert.equal(d.documentElement.style.overflow||'','');}
  }
  fixtures.push(fig.id);checks++;
 }
 // Formal publication omits reference controls and preserves all seven reading links.
 assert.equal(qa('.reading-source-dialog,.reading-inline-source,.chapter-table-figure,.reading-reference,.viz-source').length,0);
 assert.equal(qa('.foundation-reading a').filter(a=>/^\d+$/.test(a.textContent.trim())).length,0);
 assert.equal(qa('#ch01-s03 .reading-module').length,3);
 const theme=q('#fig-theme-maps'),themeData=JSON.parse(q('#theme-map-data').textContent);
 assert.equal(qa('[data-theme-node]').length,7);assert.equal(qa('[data-theme-pillar]').length,4);
 for(const b of qa('[data-theme-node]')){click(b);assert.equal(b.getAttribute('aria-pressed'),'true');const m=themeData.maps.find(m=>m.id===b.dataset.themeNode);assert(q('#theme-map-detail').textContent.includes(m.question));assert(q('#theme-map-detail>a').getAttribute('href').endsWith(m.href));assert.equal(qa('.theme-map-edge.is-active').length,m.pillars.length);}
 for(const b of qa('[data-theme-pillar]')){click(b);assert.equal(b.getAttribute('aria-pressed'),'true');assert.equal(qa('.theme-map-related a').length,themeData.maps.filter(m=>m.pillars.includes(b.dataset.themePillar)).length);}
 click(q('[data-theme-reset]'));assert(!theme.classList.contains('has-selection'));const motion=q('[data-theme-motion]');click(motion);assert.equal(motion.getAttribute('aria-pressed'),'false');click(motion);assert.equal(motion.getAttribute('aria-pressed'),'true');
 assert.equal(qa('.chapter-print-figure').length,7);
 const ids=qa('[id]').map(n=>n.id);assert.equal(ids.length,new Set(ids).size);assert(!qa('.foundation-figure').some(n=>/undefined|NaN/.test(n.textContent)));
 const qaDir=path.join(require('os').tmpdir(),'gosd-chapter1-qa');fs.mkdirSync(qaDir,{recursive:true});fs.writeFileSync(path.join(qaDir,'chapter1-'+lang+'-dom.html'),d.documentElement.outerHTML);
 console.log(`PASS ${lang}: seven publication canvases; six chapters; 20 Linux rows; 28 months; 5 Qwen nodes and 4 edges; 17 SDGs; 9 DPGA requirements; 14 goals; 29 indicators; repeated 1440/1366/1920 presentation and restore.`);
}
console.log(`PASS: ${checks} DOM operations. No browser layout verification is claimed.`);
