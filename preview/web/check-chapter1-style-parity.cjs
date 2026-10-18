/* Targeted CSS cascade analysis. Detect prose inheritance after a canvas moves.
   This does not compute browser geometry or replace viewport QA. */
const fs=require('fs'),path=require('path'),assert=require('assert'),{parseHTML}=require('linkedom');
const root=path.resolve(__dirname,'../..'),out=path.resolve(process.argv[2]||root+'/_site');
const files=['style.css','reader.css','portal.css','report.css','chapter-visuals.css','chapter1-explorers.css','chapter1-slides.css','reading-experience.css','chapter1-restored.css','chapter1-release.css'];
function split(s){let level=0,start=0,arr=[];for(let i=0;i<s.length;i++){if('(['.includes(s[i]))level++;if(')]'.includes(s[i]))level--;if(s[i]===','&&level===0){arr.push(s.slice(start,i));start=i+1;}}arr.push(s.slice(start));return arr;}
function mediaOK(m,w,h){if(/print|prefers-reduced-motion/.test(m))return false;const checks=[...m.matchAll(/(min|max)-(width|height)\s*:\s*([\d.]+)px/g)];return checks.every(([,mode,axis,v])=>mode==='min'?(axis==='width'?w:h)>=+v:(axis==='width'?w:h)<=+v);}
function rules(css,w,h,result=[]){css=css.replace(/\/\*[\s\S]*?\*\//g,'');let i=0;while(i<css.length){let open=css.indexOf('{',i);if(open<0)break;const sel=css.slice(i,open).trim();let depth=1,j=open+1;for(;j<css.length&&depth;j++){if(css[j]==='{')depth++;if(css[j]==='}')depth--;}const body=css.slice(open+1,j-1);i=j;if(sel.startsWith('@media')){if(mediaOK(sel,w,h))rules(body,w,h,result);continue;}if(sel.startsWith('@'))continue;
 const declarations=body.split(';').map(v=>v.split(/:(.*)/s)).filter(x=>x.length>1).map(([k,v])=>[k.trim(),v.replace(/!important/g,'').trim(),/!important/.test(v)]);
 for(const selector of split(sel)){const clean=selector.trim();if(!clean||/::|:focus|:hover|:active|:checked/.test(clean))continue;const specificity=(clean.match(/#[\w-]+/g)||[]).length*10000+(clean.match(/\.[\w-]+|\[[^\]]+\]|:(?!:)[\w-]+/g)||[]).length*100+(clean.match(/(^|[\s>+~])(?:[a-z][\w-]*)/g)||[]).length;result.push({selector:clean,specificity,declarations});}
 }return result;}
const inherited=['font-size','font-family','font-weight','line-height','letter-spacing','text-align','color'];
function expand(k,v){if(['padding','margin','border-width'].includes(k)){let a=v.split(/\s+/);a=[a[0],a[1]||a[0],a[2]||a[0],a[3]||a[1]||a[0]];return ['top','right','bottom','left'].map((n,i)=>[k==='border-width'?'border-'+n+'-width':k+'-'+n,a[i]]);}
 if(k==='font'){let m=v.match(/(?:(\d{3}|normal|bold)\s+)?([\d.]+(?:px|pt))(?:\s*\/\s*([\d.]+(?:px|em)?|normal))?\s+(.+)/);if(m)return [['font-weight',m[1]||'400'],['font-size',m[2]],['line-height',m[3]||'normal'],['font-family',m[4]]];}return [[k,v]];}
let total=0,diffs=[];
for(const lang of ['zh','en'])for(const theme of ['light','dark'])for(const [width,height] of [[1366,768],[1440,900]]){
 const {document:d}=parseHTML(fs.readFileSync(path.join(require('os').tmpdir(),'gosd-chapter1-qa','chapter1-'+lang+'-dom.html'),'utf8'));d.documentElement.setAttribute('data-theme',theme);d.querySelector('#model-story-qwen')?.removeAttribute('hidden');const rs=files.flatMap(f=>rules(fs.readFileSync(out+'/'+f,'utf8'),width,height));
 let cache=new Map();function style(el){if(cache.has(el))return cache.get(el);const parent=el.parentElement?style(el.parentElement):{};let ledger={};for(let i=0;i<rs.length;i++){const r=rs[i];let matched=false;try{matched=el.matches(r.selector)}catch{}if(!matched)continue;for(const[k,v,important]of r.declarations)for(const[prop,value]of expand(k,v)){const rank=(important?1e9:0)+r.specificity*10000+i;if(!ledger[prop]||ledger[prop].rank<=rank)ledger[prop]={rank,value};}}
 const result={};for(const k of inherited)result[k]=parent[k]||'';for(const[k,v]of Object.entries(ledger)){if(k.startsWith('--')||['animation','transition','transform','left','top','scroll-margin-top'].includes(k))continue;result[k]=v.value==='inherit'?parent[k]||'':v.value;}
 cache.set(el,result);return result;}
 for(const fig of [...d.querySelectorAll('.foundation-figure')]){
  const elements=[fig,...fig.querySelectorAll('p,h3,h4,strong,button,span,dl,dt,dd')].filter(n=>!n.closest('[hidden],template,noscript'));
  const before=elements.map(el=>style(el));const home=fig.parentElement;const dialog=d.createElement('dialog');dialog.className='explorer-presentation foundation-presentation';d.body.append(dialog);dialog.append(fig);cache=new Map();
  elements.forEach((el,i)=>{const after=style(el),a=before[i];const changed=[...new Set([...Object.keys(a),...Object.keys(after)])].filter(k=>a[k]!==after[k]);if(changed.length)diffs.push({lang,width,figure:fig.id,tag:el.tagName,cls:el.className,text:el.textContent.trim().slice(0,45),changed:changed.map(k=>[k,a[k],after[k]])});total++;});home.append(fig);dialog.remove();cache=new Map();
 }
}
if(diffs.length){console.log(JSON.stringify(diffs.slice(0,25),null,2));throw new Error(`${diffs.length} embedded/full-screen CSS differences`);}
console.log(`PASS: ${total} targeted element-style comparisons in both themes at 1366/1440 widths; identical embedded and presented typography/spacing. Static cascade analysis only.`);
