/* Entry pages have distinct jobs. Chapter 1 owns the single reading map.
   DOM checks do not establish browser geometry. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),{parseHTML}=require('linkedom');
const out=path.resolve(process.argv[2]||'_site'),root=path.resolve(__dirname,'../..'),manifest=JSON.parse(fs.readFileSync(root+'/preview/content/manifest.json','utf8'));let checks=0;
for(const lang of ['zh','en'])for(const route of ['home','contents','summary','introduction']){
 const file=route==='home'?(lang==='zh'?'index.html':'en/index.html'):`2026/${lang}/${route==='contents'?'':route+'/'}index.html`;
 const {document:d}=parseHTML(fs.readFileSync(path.join(out,file),'utf8')),q=s=>d.querySelector(s),qa=s=>[...d.querySelectorAll(s)];
 assert.equal(qa('.architecture-flow').length,0);assert(!q('script[src*="report-architecture.js"]'));assert(q('link[href*="frontmatter.css"]'));
 assert.equal(d.body.dataset.frontmatter,'true');assert.equal(qa('.front-print-edition').length,1);assert(q('.front-print-edition a').getAttribute('href').includes('GOSD-2026-opening-and-chapter1.pdf'));
 for(const unused of ['chapter1-explorers.js','atlas-core.js','goso.js','landscape.js','assets/imap/data.js'])assert(!q(`script[src*="${unused}"]`));
 if(route!=='home'){
  const entries=qa('.front-entry-links a');assert.equal(entries.length,3);assert.equal(entries.filter(a=>a.getAttribute('aria-current')==='page').length,1);
  for(const a of qa('#section-nav .local-section'))assert(d.getElementById(a.getAttribute('href').slice(1)));
 }
 if(route==='summary'||route==='introduction')assert(!q('.reader-page-nav'),'Only one contextual onward-reading area');
 if(route==='summary')assert(q('.es-reading-links a').getAttribute('href').endsWith('/introduction/'));
 if(route==='contents')assert.equal(qa('.front-contents-entry a').length,2);
 if(route==='home'){assert.equal(qa('.home-reading-start nav a').length,3);assert.equal(qa('.reading-chapter-grid>a').length,4);assert(q('#chapter-6>a').getAttribute('href').endsWith('/chapters/06/'));for(let i=1;i<=6;i++)assert(q('#chapter-'+i));}
 if(route==='contents'){assert.equal(qa('.front-contents-group').length,3);const cards=qa('.front-chapter-card');assert.equal(cards.length,6);assert.equal(qa('.front-chapter-card nav a').length,30);manifest.chapters.forEach((c,i)=>c.sections.forEach((s,j)=>assert(cards[i].querySelectorAll('nav a')[j].getAttribute('href').endsWith(c.route+'#'+s.id))));}
 if(route==='introduction'){const prose=q('.declaration-introduction');assert(prose);assert.equal(qa('.declaration-principle').length,7);assert.equal(qa('.df-wide .df-layer').length,3);assert.equal(qa('.df-wide .df-principle').length,7);assert.equal(qa('.declaration-section').length,6);for(const a of qa('.df-principle'))assert(q(a.getAttribute('href')));assert(q('.front-next-primary').getAttribute('href').endsWith('/chapters/01/'));assert(!q('.declaration-document .declaration-bridge'));}
 if(route==='summary'){const prose=q('.executive-summary');assert(prose);assert.equal(prose.lang,lang==='zh'?'zh-CN':'en');assert.equal(qa('.executive-summary h2').length,4);assert.equal(qa('.es-observation').length,4);assert.equal(qa('.es-action-list>li').length,9);assert.equal(qa('.es-reading-links a').length,2);assert(!q('.reader-note'));}
 const ids=qa('[id]').map(x=>x.id);assert.equal(ids.length,new Set(ids).size,file);checks++;
}
// The summary remains complete without JS; enhancement exposes one panel per switcher.
for(const lang of ['zh','en']){
 const {window:w}=parseHTML(fs.readFileSync(path.join(out,`2026/${lang}/summary/index.html`),'utf8')),d=w.document;
 assert([...d.querySelectorAll('[data-es-panel]')].every(p=>!p.hidden));
 assert.equal(d.querySelectorAll('.es-observation-links a').length,4);assert.equal(d.querySelectorAll('.es-shared-tasks article').length,3);
 vm.runInContext(fs.readFileSync(path.join(out,'executive-summary.js'),'utf8'),vm.createContext(w));
 assert([...d.querySelectorAll('.es-observation')].every(p=>!p.hidden&&!p.hasAttribute('data-es-panel')));
 for(const group of d.querySelectorAll('[data-es-switcher]')){
  const tabs=[...group.querySelectorAll('[role=tab]')],panels=[...group.querySelectorAll('[role=tabpanel]')];
  assert.equal(panels.filter(p=>!p.hidden).length,1);
  for(const tab of tabs){tab.click();assert.equal(panels.filter(p=>!p.hidden).length,1);assert.equal(tab.getAttribute('aria-selected'),'true');assert(!d.getElementById(tab.getAttribute('aria-controls')).hidden);checks++;}
  for(const [key,index] of [['Home',0],['ArrowLeft',tabs.length-1],['ArrowRight',0],['End',tabs.length-1]]){
   const active=tabs.find(t=>t.getAttribute('aria-selected')==='true'),event=new w.Event('keydown',{bubbles:true,cancelable:true});event.key=key;active.dispatchEvent(event);assert.equal(tabs[index].getAttribute('aria-selected'),'true');
  }
 }
}
for(const lang of ['zh','en'])for(const reduced of [false,true]){
 const file=`2026/${lang}/chapters/01/index.html`,{window:w}=parseHTML(fs.readFileSync(path.join(out,file),'utf8')),d=w.document;
 w.console=console;w.URL=URL;w.URLSearchParams=URLSearchParams;w.location=new URL('https://example.test/'+file.replace('index.html',''));w.requestAnimationFrame=fn=>{fn();return 1;};w.innerWidth=1366;w.innerHeight=768;w.ResizeObserver=class{observe(){}};
 let preferenceChange;w.matchMedia=()=>({matches:reduced,addEventListener(n,fn){preferenceChange=fn;}});
 Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return this.classList?.contains('explorer-slide-frame')?(this.closest('dialog')?w.innerWidth:886):800;},configurable:true});
 Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return this.classList?.contains('explorer-slide-frame')?(this.closest('dialog')?w.innerHeight-52:parseFloat(this.style.height)||550):600;},configurable:true});
 w.HTMLElement.prototype.showModal=function(){this.open=true;};w.HTMLElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'));};w.HTMLElement.prototype.scrollIntoView=function(){};
 const context=vm.createContext(w);for(const f of ['chapter1-explorers.js','report-architecture.js'])vm.runInContext(fs.readFileSync(path.join(out,f),'utf8'),context,{filename:f});
 const q=s=>d.querySelector(s),qa=(s,r=d)=>[...r.querySelectorAll(s)],fig=q('.architecture-flow');assert(fig);assert.equal(qa('.architecture-flow').length,1);assert.equal(qa('.architecture-edge').length,8);assert.equal(qa('[data-logic-chapter]').length,6);assert.equal(qa('[data-logic-framework]').length,0);assert.equal(qa('.architecture-section-links a').length,30);
 assert(!q('#logic-start').hidden);assert(qa('.logic-detail').every(x=>x.hidden));assert(qa('[data-logic-chapter]').every(x=>x.getAttribute('aria-expanded')==='false'));
 for(const b of qa('[data-logic-chapter]')){b.click();assert.equal(b.getAttribute('aria-expanded'),'true');assert.equal(qa('.logic-detail').filter(x=>!x.hidden).length,1);assert(!d.getElementById(b.getAttribute('aria-controls')).hidden);assert(q('#logic-start').hidden);assert.equal(qa('.architecture-edge.is-active').length,['2','3','4','5'].includes(b.dataset.logicChapter)?2:8);checks++;}
 q('[data-architecture-reset]').click();assert(!q('#logic-start').hidden);assert(qa('.logic-detail').every(x=>x.hidden));assert(!fig.classList.contains('has-path'));
 const motion=q('[data-architecture-motion]');assert.equal(motion.getAttribute('aria-pressed'),String(!reduced));motion.click();assert.equal(motion.getAttribute('aria-pressed'),'false');motion.click();assert.equal(motion.getAttribute('aria-pressed'),String(!reduced));preferenceChange();assert.equal(motion.getAttribute('aria-pressed'),'false');
 q('[data-logic-chapter="4"]').click();const frame=fig.parentElement,home=frame.parentElement,launcher=frame.previousElementSibling.querySelector('button'),dialog=qa('dialog.explorer-presentation').find(x=>x.getAttribute('aria-label')===fig.querySelector('h3').textContent),close=dialog.querySelector('.slide-presentation-bar button');
 for(const [width,height] of [[1366,768],[1440,900],[1920,1080]]){w.innerWidth=width;w.innerHeight=height;w.dispatchEvent(new w.Event('resize'));const scale=fig.style.transform;launcher.click();assert(dialog.open);assert.equal(frame.parentElement,dialog);assert.equal(fig.parentElement,frame);const ratio=Number(fig.style.transform.match(/[\d.]+/)[0]);assert(ratio*1280<=width+.1);assert(ratio*800<=height-52+.1);close.click();assert.equal(frame.parentElement,home);assert.equal(fig.style.transform,scale);assert.equal(q('[data-logic-chapter="4"]').getAttribute('aria-expanded'),'true');checks++;}
}
console.log(`PASS: eight distinct bilingual entry pages, one chapter map per language, 30 section links, eight forward edges, neutral initial state, reset, reduced motion and ${checks} navigation/restore cases. DOM harness only.`);
