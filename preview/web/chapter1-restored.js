/* Additional content inside the original fixed canvas. No second full-screen system. */
(()=>{'use strict';
const fig=document.getElementById('fig-models');
if(fig&&document.getElementById('qwen-story-data')){
 const q=s=>fig.querySelector(s),qa=s=>[...fig.querySelectorAll(s)],zh=fig.dataset.lang==='zh',t=(z,e)=>zh?z:e;
 const d=JSON.parse(document.getElementById('qwen-story-data').textContent),detail=q('#qwen-story-detail'),initial=detail.innerHTML;
 const base=document.querySelector('meta[name="gosd-base"]')?.content||'',lang=zh?'zh':'en';
 const params=new URLSearchParams(location.search);
 const remember=(key,value)=>{const url=new URL(location.href);url.searchParams.set(key,String(value));history.replaceState(null,'',url);};
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function showView(key,save=false){if(!['macro','qwen'].includes(key))return;qa('[data-model-story-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.modelStoryView===key)));qa('[data-model-story-panel]').forEach(p=>p.hidden=p.dataset.modelStoryPanel!==key);qa('[data-model-story-scope]').forEach(p=>p.hidden=p.dataset.modelStoryScope!==key);fig.dataset.modelStoryMode=key;if(save)remember('modelView',key);}
 const views=qa('[data-model-story-view]');
 views.forEach((b,i)=>{b.addEventListener('click',()=>showView(b.dataset.modelStoryView,true));b.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const next=e.key==='Home'?views[0]:e.key==='End'?views[1]:views[1-i];next.focus();showView(next.dataset.modelStoryView,true);});});
 function select(index,isEdge=false,save=true){if(!Number.isInteger(index)||!d.nodes[index])return;qa('[data-qwen-node]').forEach(b=>b.setAttribute('aria-pressed',String(!isEdge&&Number(b.dataset.qwenNode)===index)));qa('[data-qwen-edge]').forEach(b=>b.setAttribute('aria-pressed',String(isEdge&&Number(b.dataset.qwenEdge)===index)));fig.classList.toggle('has-qwen-selection',index!==0);qa('[data-qwen-path]').forEach(p=>p.classList.toggle('is-selected',Number(p.dataset.qwenPath)===index));if(save)remember('qwenSelection',(isEdge?'edge:':'node:')+index);if(index===0&&!isEdge){detail.innerHTML=initial;return;}
 const name=d.nodes[index],title=isEdge?t('声明的基础模型关系','Declared base-model relationship'):name.split('/')[1];
 const description=isEdge?t('连线表示发布者声明的基础模型关系。一次开放发布，连接后续不同用途的创造。','The edge records a publisher-declared base model, connecting a release to subsequent development.'):t('用途：','Use: ')+d.uses[index]+t('。该模型声明以 Qwen2.5-7B 为基础。','; this release declares Qwen2.5-7B as its base model.');
 detail.innerHTML=`<span class="viz-label">${t('局部案例 · 来源声明','LOCAL CASE · SOURCE DECLARATION')}</span><strong>${esc(title)}</strong><p>${esc(description)}</p><dl><dt>${t('下游 ID','Downstream ID')}</dt><dd>${esc(name)}</dd><dt>${t('基础模型','Base model')}</dt><dd>${esc(d.base)}</dd><dt>${t('来源快照','Snapshot')}</dt><dd>${d.snapshot}</dd></dl><div class="qwen-story-links"><a class="inline-link" href="${base}/2026/${lang}/chapters/05/#ch05-s02">${t('进入 5.2 完整网络 →','Full network in 5.2 →')}</a></div>`;
 }
 qa('[data-qwen-node]').forEach(b=>b.addEventListener('click',()=>select(Number(b.dataset.qwenNode))));qa('[data-qwen-edge]').forEach(b=>b.addEventListener('click',()=>select(Number(b.dataset.qwenEdge),true)));
 const saved=/^(node|edge):([0-4])$/.exec(params.get('qwenSelection')||'');if(saved&&!(saved[1]==='edge'&&saved[2]==='0'))select(Number(saved[2]),saved[1]==='edge',false);
 showView(params.get('modelView')==='qwen'?'qwen':'macro');
}
const framework=document.querySelector('[data-logic-framework="osdg"]');
if(framework&&!framework.closest('.architecture-flow'))framework.addEventListener('click',()=>{const box=document.getElementById('logic-framework-detail'),zh=document.documentElement.lang.startsWith('zh');const list=document.createElement('div');list.className='logic-pillar-summary';const names=zh?['人才规模与多样性','技术产出与开放供给','全球连接与网络效应','开源善治与公共价值']:['Talent scale and diversity','Technology and open supply','Global connections and network effects','Governance and public value'];names.forEach((n,i)=>{const p=document.createElement('p'),code=document.createElement('b');code.textContent='X'+(i+1);p.append(code,document.createTextNode(n));list.append(p)});box.insertBefore(list,box.querySelector('a'));});
})();
