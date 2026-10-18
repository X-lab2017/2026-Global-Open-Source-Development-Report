/* Fixed-position reading links; authored relationships, no remote runtime. */
(()=>{'use strict';
const fig=document.getElementById('fig-theme-maps');if(!fig)return;
const data=JSON.parse(fig.querySelector('#theme-map-data').textContent),detail=fig.querySelector('#theme-map-detail'),overview=detail.innerHTML;
const zh=fig.dataset.lang==='zh',t=(z,e)=>zh?z:e,base=document.querySelector('meta[name="gosd-base"]')?.content||'';
const nodes=[...fig.querySelectorAll('[data-theme-node]')],pillars=[...fig.querySelectorAll('[data-theme-pillar]')],edges=[...fig.querySelectorAll('[data-theme-edge]')];
const el=(tag,text,cls)=>{const n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n;};
function link(m){const a=el('a',m.number+' '+m.title+' →');a.href=base+m.href;return a;}
function select(kind,id){
 const map=data.maps.find(m=>m.id===id),pillar=data.pillars.find(p=>p.id===id);
 nodes.forEach(b=>{const active=kind==='map'?b.dataset.themeNode===id:kind==='pillar'?data.maps.find(m=>m.id===b.dataset.themeNode).pillars.includes(id):false;b.setAttribute('aria-pressed',String(kind==='map'&&active));b.classList.toggle('is-linked',active);});
 pillars.forEach(b=>{const active=kind==='pillar'?b.dataset.themePillar===id:kind==='map'?map.pillars.includes(b.dataset.themePillar):false;b.setAttribute('aria-pressed',String(kind==='pillar'&&active));b.classList.toggle('is-linked',active);});
 edges.forEach(e=>{const[p,m]=e.dataset.themeEdge.split(':');e.classList.toggle('is-active',kind==='map'?m===id:kind==='pillar'?p===id:false);});
 fig.dataset.themeSelection=kind+':'+id;fig.classList.toggle('has-selection',kind!=='all');
 if(kind==='all'){detail.innerHTML=overview;return;}
 detail.replaceChildren();
 if(kind==='map'){
  detail.append(el('small',map.number+' / '+id+'-MAP'),el('h4',map.title),el('p',map.question,'theme-map-question'),el('p',map.description));
  const tags=el('div','','theme-map-tags');map.pillars.forEach(p=>tags.append(el('span',p+' '+data.pillars.find(x=>x.id===p).title)));detail.append(tags,link(map));
 }else{
  detail.append(el('small',id+' / OSDGs'),el('h4',pillar.title),el('p',pillar.question),el('p',t('从这些主题观察这个目标：','Explore this goal through these themes:')));
  const links=el('div','','theme-map-related');data.maps.filter(m=>m.pillars.includes(id)).forEach(m=>links.append(link(m)));detail.append(links);
 }
}
nodes.forEach(b=>b.addEventListener('click',()=>select('map',b.dataset.themeNode)));
pillars.forEach(b=>b.addEventListener('click',()=>select('pillar',b.dataset.themePillar)));
fig.querySelector('[data-theme-reset]').addEventListener('click',()=>select('all',''));
const motion=fig.querySelector('[data-theme-motion]'),reduced=window.matchMedia?.('(prefers-reduced-motion: reduce)');
function setMotion(on){const active=on&&!reduced?.matches;fig.classList.toggle('is-flowing',active);motion.setAttribute('aria-pressed',String(active));motion.textContent=active?t('暂停连线','Pause motion'):t('流动连线','Animate links');}
motion.addEventListener('click',()=>setMotion(motion.getAttribute('aria-pressed')!=='true'));reduced?.addEventListener?.('change',()=>setMotion(false));
select('all','');setMotion(true);
})();
