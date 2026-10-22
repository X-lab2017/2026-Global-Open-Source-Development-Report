/* Chapter 6 diagrams share authored action records; edges are conceptual. */
(()=>{'use strict';
const source=document.getElementById('chapter6-action-data');if(!source)return;
const D=JSON.parse(source.textContent),base=document.querySelector('meta[name="gosd-base"]')?.content||'';
const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text)n.textContent=text;if(cls)n.className=cls;return n;};
for(const fig of document.querySelectorAll('[data-action-figure]')){
 const lang=fig.dataset.lang==='en'?'en':'zh',L=x=>typeof x==='object'?x[lang]:x,t=(z,e)=>lang==='zh'?z:e,q=s=>fig.querySelector(s),qa=s=>[...fig.querySelectorAll(s)];
 const link=(label,url)=>{const a=el('a',L(label)+' ↗');a.href=base+'/2026/'+lang+'/'+url;return a;};
 if(fig.dataset.actionFigure==='overview'){
  const detail=q('#ac-overview-detail'),caption=q('[data-ac-caption-note]'),defaultCaption=caption.textContent;let taskId='commons';
  const task=()=>D.tasks.find(x=>x.id===taskId),recommendation=actor=>D.actions.find(a=>a.actor===actor&&a.task===taskId);
  function highlight(evidence=null,actor=null){qa('.ac-edge').forEach(p=>{const connected=p.dataset.to===taskId||p.dataset.from===taskId;const focus=connected&&(!evidence||p.dataset.from===evidence||p.dataset.from===taskId)&&(!actor||p.dataset.to===taskId||p.dataset.to===actor);p.classList.toggle('is-active',focus);});}
  function reset(){qa('[data-ac-evidence],[data-ac-actor]').forEach(b=>b.setAttribute('aria-pressed','false'));caption.textContent=defaultCaption;}
  function panel(kicker,title,body,links=[],note=''){
   detail.replaceChildren();const head=el('div','','ac-detail-title');head.append(el('small',kicker),el('h4',title));const copy=el('div','','ac-detail-copy');copy.append(el('p',body));if(note)copy.append(el('span',note));if(links.length){const nav=el('nav','','ac-detail-links');links.forEach(a=>nav.append(link(a.label,a.url)));copy.append(nav);}detail.append(head,copy);
  }
  function selectTask(id){taskId=id;reset();qa('[data-ac-task]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.acTask===id)));qa('[data-ac-actor]').forEach(b=>{const a=recommendation(b.dataset.acActor);b.querySelector('span').textContent=a.number+' · '+L(a.short);});highlight();const v=task();panel(t('共同任务 ','SHARED TASK ')+v.n+' · '+v.pillars,L(v.short),L(v.body),[],t('持续观察：','Observe: ')+L(v.watch));}
  qa('[data-ac-task]').forEach(b=>b.addEventListener('click',()=>selectTask(b.dataset.acTask)));
  qa('[data-ac-evidence]').forEach(b=>b.addEventListener('click',()=>{const e=D.evidence.find(x=>x.id===b.dataset.acEvidence);if(!e.tasks.includes(taskId))selectTask(e.tasks[0]);reset();b.setAttribute('aria-pressed','true');highlight(e.id);panel(e.code,L(e.title),L(e.summary),e.links);caption.textContent=L(e.boundary);}));
  qa('[data-ac-actor]').forEach(b=>b.addEventListener('click',()=>{reset();b.setAttribute('aria-pressed','true');const a=recommendation(b.dataset.acActor);highlight(null,b.dataset.acActor);panel(t('建议 ','ACTION ')+a.number,L(a.short),L(a.why),[{label:t('阅读完整建议','Read the full recommendation'),url:'chapters/06/#action-'+a.id}],t('观察：','Observe: ')+a.watch.map(w=>L(w.label)).join(' · '));}));selectTask(taskId);
 }else if(fig.dataset.actionFigure==='cycle'){
  const detail=q('#ac-cycle-detail');qa('[data-ac-cycle]').forEach(b=>b.addEventListener('click',()=>{const v=D.cycle.find(x=>x.id===b.dataset.acCycle);qa('[data-ac-cycle]').forEach(n=>n.setAttribute('aria-pressed',String(n===b)));qa('.ac-edge').forEach(p=>p.classList.toggle('is-active',p.dataset.from===v.id));fig.classList.add('has-selection');detail.replaceChildren();const h=el('div','','ac-cycle-selected');h.append(el('h4',L(v.title)),link(v.link.label,v.link.url));detail.append(h,el('p',L(v.body)));}));
 }else{
  const actor=fig.dataset.actionFigure;function select(id){const a=D.actions.find(x=>x.id===id&&x.actor===actor);if(!a)return;qa('[data-ac-action]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.acAction===id)));fig.dataset.selectedAction=id;const task=D.tasks.find(x=>x.id===a.task);q('[data-ac-task-label]').textContent=t('共同任务 · ','SHARED TASK · ')+L(task.short);for(let i=0;i<3;i++)for(const [key,value]of [['step-title',a.steps[i].title],['step-body',a.steps[i].body],['role-who',a.roles[i].who],['role-work',a.roles[i].work],['watch-label',a.watch[i].label],['watch-detail',a.watch[i].detail]])q('[data-ac-'+key+'="'+i+'"]').textContent=L(value);}
  qa('[data-ac-action]').forEach(b=>b.addEventListener('click',()=>select(b.dataset.acAction)));select(D.actions.find(x=>x.actor===actor).id);
 }
}
})();
