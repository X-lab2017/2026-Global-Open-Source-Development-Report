/* Reading progress, accessible figure expansion, and source-file filtering. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const zh = document.documentElement.lang.startsWith('zh');
  const t = (z,e) => zh ? z : e;
  const progress = $('#reading-progress');
  if (progress) {
    let queued = false;
    const update = () => {
      const main = $('#main'), top = main.getBoundingClientRect().top + window.scrollY;
      const end = Math.max(1, main.offsetHeight - window.innerHeight + 100);
      progress.value = Math.min(100, Math.max(0, (window.scrollY - top + 100) / end * 100));
      queued = false;
    };
    window.addEventListener('scroll', () => { if (!queued) {queued = true; requestAnimationFrame(update);} }, {passive:true});
    window.addEventListener('resize', update); update();
  }
  const figures = [...document.querySelectorAll('[data-figure]')];
  if (figures.length && typeof HTMLDialogElement !== 'undefined') {
    const dialog=document.createElement('dialog');dialog.className='figure-dialog';
    const head=document.createElement('header'), title=document.createElement('strong');title.id='figure-dialog-title';
    dialog.setAttribute('aria-labelledby',title.id);
    const minus=document.createElement('button'), plus=document.createElement('button'), download=document.createElement('a'), close=document.createElement('button');
    minus.textContent='−';plus.textContent='+';close.textContent='×';close.className='figure-dialog-close';
    minus.setAttribute('aria-label',t('缩小图表','Zoom out'));plus.setAttribute('aria-label',t('放大图表','Zoom in'));close.setAttribute('aria-label',t('关闭图表','Close figure'));
    download.textContent=t('下载','Download');download.setAttribute('download','');
    head.append(title,minus,plus,download,close);
    const viewport=document.createElement('div');viewport.className='figure-viewport';viewport.tabIndex=0;viewport.setAttribute('role','region');viewport.setAttribute('aria-label',t('图表，可滚动查看','Scrollable figure'));
    const img=document.createElement('img');viewport.append(img);dialog.append(head,viewport);document.body.append(dialog);
    let scale=100;
    const zoom=n=>{scale=Math.max(100,Math.min(300,n));img.style.width=scale+'%';minus.disabled=scale===100;plus.disabled=scale===300;};
    figures.forEach(link=>link.addEventListener('click',e=>{if(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;e.preventDefault();const source=link.querySelector('img');img.src=source.src;img.alt=source.alt;title.textContent=source.alt;download.href=link.href;zoom(100);dialog.showModal();close.focus();}));
    close.addEventListener('click',()=>dialog.close());plus.addEventListener('click',()=>zoom(scale+25));minus.addEventListener('click',()=>zoom(scale-25));
    dialog.addEventListener('click',e=>{if(e.target===dialog){const box=dialog.getBoundingClientRect();if(e.clientX<box.left||e.clientX>box.right||e.clientY<box.top||e.clientY>box.bottom)dialog.close();}});
  }
  const form=$('#dataset-filters');
  if(form){
    const input=$('#dataset-q'),select=$('#dataset-chapter'),entries=[...document.querySelectorAll('.dataset-entry')];
    const read=()=>{const params=new URLSearchParams(location.search);input.value=params.get('q')||'';select.value=params.get('chapter')||'';};
    const apply=(save=true)=>{
      const q=input.value.trim().toLowerCase(),chapter=select.value;let count=0;
      entries.forEach(entry=>{const visible=(!q||entry.dataset.search.includes(q))&&(!chapter||entry.dataset.chapter===chapter);entry.hidden=!visible;if(visible)count++;});
      $('#dataset-count').textContent=t(`显示 ${count} / ${entries.length} 份数据文件`,`Showing ${count} / ${entries.length} data files`);$('#dataset-empty').hidden=count!==0;
      if(save){const url=new URL(location.href);q?url.searchParams.set('q',input.value.trim()):url.searchParams.delete('q');chapter?url.searchParams.set('chapter',chapter):url.searchParams.delete('chapter');history.replaceState(null,'',url);}
    };
    const reveal=()=>{let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const target=document.getElementById(id);if(target?.classList.contains('dataset-entry')){if(target.hidden){input.value='';select.value='';apply();}target.open=true;requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}};
    read();apply(false);reveal();form.addEventListener('submit',e=>e.preventDefault());input.addEventListener('input',()=>apply());select.addEventListener('change',()=>apply());
    form.addEventListener('reset',()=>setTimeout(()=>apply(),0));window.addEventListener('hashchange',reveal);window.addEventListener('popstate',()=>{read();apply(false);reveal();});
  }
})();
