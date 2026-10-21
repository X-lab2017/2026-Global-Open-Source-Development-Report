/* Chapter-wide publication contract: independent figures and one optional source entry. */
const fs=require('fs'),path=require('path'),assert=require('assert'),{JSDOM}=require('jsdom');
const out=path.resolve(process.argv[2]||'_site'),read=f=>fs.readFileSync(path.join(out,f),'utf8');
const dom=new JSDOM(read('2026/zh/chapters/03/index.html'),{url:'https://example.test/2026/zh/chapters/03/',runScripts:'outside-only',pretendToBeVisual:true}),w=dom.window,d=w.document,errors=[];
w.ResizeObserver=class{observe(){}};w.matchMedia=()=>({matches:true});w.HTMLElement.prototype.scrollIntoView=function(){};w.addEventListener('error',e=>errors.push(e.message));
for(const f of ['chapter1-explorers.js','company-ranking.js','ranking-details.js','rankings.js'])w.eval(read(f));
let checks=0;const ok=(v,m)=>{assert(v,m);assert.deepEqual(errors,[]);checks++},$=s=>d.querySelector(s),$$=s=>[...d.querySelectorAll(s)];
for(let section=1;section<=6;section++)for(let i=1;i<=3;i++){
 const id=`#fig-3-${section}-${i}`,figure=$(id);ok(figure,`${id} exists`);
 const captions=$$(id+' .rp-caption');ok(captions.length===1,`${id} one caption`);
 ok(captions[0].textContent.replace(/\s/g,'').length>9,`${id} complete title`);
 ok(figure.compareDocumentPosition(captions[0])&w.Node.DOCUMENT_POSITION_CONTAINED_BY,`${id} self-contained caption`);
 ok(figure.querySelector('.slide-launcher button'),`${id} fullscreen retained`);
 ok(!$(id+' [data-rr-action=image]')&&!$(id+' [data-rr-action=export]'),`${id} no technical export clutter`);
}
ok($$('[data-rr-action=source]').length===1,'one chapter source entry');
$('#fig-3-1-1 [data-rr-action=source]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
ok($('.rp-source-intro'),'source panel opens');
const groups=$$('.rp-source-groups details');ok(groups.length===6,'six optional section groups');ok(groups.every(x=>!x.open),'notes initially collapsed');
const links=$$('.rp-source-links a');ok(links.length===25,'24 source tables and full model snapshot');
for(const link of links){const suffix=link.getAttribute('href').split('/assets/')[1];ok(suffix&&fs.existsSync(path.join(out,'assets',suffix)),`source link exists: ${suffix}`)}
ok(!/undefined|NaN/.test($('.rp-source-groups').innerHTML),'source content complete');
ok(!$('#gosr-review details'),'no repeated chapter-end methods');
ok(!$('#ch03-s06 [data-rr-view=history]'),'model history stays removed');
const snapshot=JSON.parse(read('assets/gosr/model-rankings-snapshot.json')).rows;
// The editorial comparison must follow the original sample, not a synthesized organization score.
const owner=r=>r.model_id.split('/')[0];
ok(snapshot.filter(r=>owner(r)==='google').length===15&&snapshot.every(r=>owner(r)!=='google'||r.rank>20),'google breadth / head comparison');
for(const account of ['lerobot','krea'])ok(snapshot.filter(r=>owner(r)===account).length===2&&snapshot.filter(r=>owner(r)===account&&r.rank<=20).length===1,account+' comparison');
console.log('PASS chapter 3: '+checks+' figure, source-link and editorial checks');dom.window.close();
