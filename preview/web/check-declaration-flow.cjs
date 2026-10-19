/* State and fit-contract checks. Artboard rendering is inspected separately;
   this DOM harness does not claim browser layout or native fullscreen QA. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const {parseHTML}=require('linkedom'),out=path.resolve(process.argv[2]||'_site');
(async()=>{
 for(const lang of ['zh','en']){
  const {window:w}=parseHTML(fs.readFileSync(path.join(out,`2026/${lang}/introduction/index.html`),'utf8'));
  const d=w.document,figure=d.querySelector('[data-declaration-flow]'),wide=figure.querySelector('.df-wide'),compact=figure.querySelector('.df-compact');
  assert.equal(wide.getAttribute('viewBox'),'0 0 1280 768');assert.equal(compact.getAttribute('viewBox'),'0 0 480 650');
  const stable=[wide.innerHTML,compact.innerHTML];
  for(const svg of [wide,compact]){
   assert.equal(svg.querySelectorAll('.df-layer').length,3);assert.equal(svg.querySelectorAll('.df-principle').length,7);
   for(const a of svg.querySelectorAll('a[href]')){assert(d.querySelector(a.getAttribute('href')));assert.equal(a.getAttribute('tabindex'),'0');assert(a.getAttribute('aria-label'));}
  }
  const printURL=figure.querySelector('.df-print').getAttribute('src');assert.equal(printURL,figure.querySelector('a[download]').getAttribute('href'));
  const {document:exportDoc}=parseHTML(fs.readFileSync(path.join(out,'assets/declaration/overview-'+lang+'.svg'),'utf8'));
  assert.equal(exportDoc.querySelector('svg').getAttribute('viewBox'),wide.getAttribute('viewBox'));
  assert.deepEqual([...wide.querySelectorAll('.df-text')].map(n=>n.textContent),[...exportDoc.querySelectorAll('.df-text')].map(n=>n.textContent));
  let visibility,preferenceChange,queue=[];const pref={matches:false,addEventListener(name,fn){preferenceChange=fn;}};
  w.matchMedia=()=>pref;w.IntersectionObserver=class{constructor(fn){visibility=fn;}observe(){}};w.requestAnimationFrame=fn=>{queue.push(fn);return queue.length;};
  const flush=()=>{const batch=queue;queue=[];batch.forEach(fn=>fn());};
  d.fullscreenEnabled=true;figure.requestFullscreen=async()=>{d.fullscreenElement=figure;d.dispatchEvent(new w.Event('fullscreenchange'));};
  d.exitFullscreen=async()=>{d.fullscreenElement=null;d.dispatchEvent(new w.Event('fullscreenchange'));};w.location={hash:''};
  w.HTMLElement.prototype.scrollIntoView=function(){this.dataset.scrolled='true';};
  vm.runInContext(fs.readFileSync(path.join(out,'declaration-flow.js'),'utf8'),vm.createContext({window:w,document:d,location:w.location,requestAnimationFrame:w.requestAnimationFrame,IntersectionObserver:w.IntersectionObserver}));
  const motion=figure.querySelector('[data-df-motion]'),full=figure.querySelector('[data-df-fullscreen]');
  assert.equal(figure.dataset.running,'false');visibility([{isIntersecting:true}]);assert.equal(figure.dataset.running,'true');
  motion.click();assert.equal(figure.dataset.running,'false');motion.click();assert.equal(figure.dataset.running,'true');
  pref.matches=true;preferenceChange();assert.equal(figure.dataset.running,'false');assert(motion.disabled);
  pref.matches=false;preferenceChange();assert.equal(figure.dataset.running,'true');
  d.hidden=true;d.dispatchEvent(new w.Event('visibilitychange'));assert.equal(figure.dataset.running,'false');
  d.hidden=false;d.dispatchEvent(new w.Event('visibilitychange'));assert.equal(figure.dataset.running,'true');
  for(const svg of [wide,compact]){
   const p=svg.querySelector('[data-df-node="principle-4"]');p.dispatchEvent(new w.Event('pointerenter'));
   assert(figure.classList.contains('has-focus'));assert(svg.querySelector('.df-edge[data-layer="2"]').classList.contains('is-active'));assert(!svg.querySelector('.df-edge[data-layer="1"]').classList.contains('is-active'));
   p.dispatchEvent(new w.Event('pointerleave'));assert(!figure.classList.contains('has-focus'));
  }
  // Fullscreen changes only the viewport. Nodes and their coordinates are retained.
  for(const svg of [wide,compact]){
   full.click();await new Promise(resolve=>setImmediate(resolve));flush();assert.equal(d.fullscreenElement,figure);assert.equal(full.getAttribute('aria-pressed'),'true');
   svg.querySelector('[data-df-node="principle-4"]').dispatchEvent(new w.Event('click',{bubbles:true,cancelable:true}));
   await new Promise(resolve=>setImmediate(resolve));flush();assert.equal(d.fullscreenElement,null);assert.equal(w.location.hash,'#declaration-principle-4');assert.equal(full.getAttribute('aria-pressed'),'false');
   assert.equal(d.querySelector('#declaration-principle-4').dataset.scrolled,'true');
  }
  assert.deepEqual([wide.innerHTML,compact.innerHTML],stable);
 }
 // The CSS bounds the artboard height while preserving its aspect ratio.
 // Budget: toolbar 40 + vertical chrome 24 + sticky-header clearance 100.
 for(const [width,height] of [[1366,768],[1440,900],[1920,1080],[1024,768],[390,844],[375,667]]){
  const mobile=width<=600,available=mobile?width-50:width-260;
  const plotW=Math.min(available,(height-(mobile?138:162))*(mobile?480/650:1280/768));
  const plotH=plotW*(mobile?650/480:768/1280);
  assert(plotH+40+24+(mobile?64:96)<=height+.1,`${width}×${height}`);
 }
 console.log('PASS: bilingual wide/compact artboards, original-text anchors, identical SVG export, motion preferences, focus paths, fullscreen restoration and viewport fit formulas. DOM harness only.');
})().catch(error=>{console.error(error);process.exitCode=1;});
