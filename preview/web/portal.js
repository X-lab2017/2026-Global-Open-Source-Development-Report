/* Shared navigation and interactions for all GOSD pages. */
(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const zh = document.documentElement.lang.startsWith('zh');
  const t = (z, e) => zh ? z : e;
  const lang = zh ? 'zh' : 'en';
  const base = document.querySelector('meta[name="gosd-base"]')?.content || '';
  const localPath = location.pathname.startsWith(base + '/') ? location.pathname.slice(base.length) : location.pathname;
  const readStore = key => { try { return JSON.parse(sessionStorage.getItem(key)); } catch { return null; } };
  const writeStore = (key, value) => { try { sessionStorage.setItem(key, JSON.stringify(value)); } catch {} };
  const here = () => location.pathname + location.search;
  const initialParams = new URLSearchParams(location.search);

  // Maintain old public links while making each new resource independently addressable.
  if (['/', '/index.html', '/en/', '/en/index.html'].includes(localPath)) {
    const targetLang = ['zh', 'en'].includes(initialParams.get('lang')) ? initialParams.get('lang') : lang;
    const h = location.hash;
    let target = targetLang === 'zh' ? '/' : '/en/';
    if (/^#dimension-\d-\d$/.test(h)) target = `/2026/${targetLang}/data/goals/` + h;
    else if (targetLang !== lang) target += h;
    else target = null;
    if (target) { location.replace(base + target); return; }
  }
  const theme = $('#theme-toggle');
  function showTheme() {
    const dark = document.documentElement.dataset.theme === 'dark';
    theme.setAttribute('aria-pressed', String(dark));
    theme.textContent = dark ? t('浅色', 'Light') : t('深色', 'Dark');
    theme.setAttribute('aria-label', dark ? t('切换浅色模式', 'Switch to light mode') : t('切换深色模式', 'Switch to dark mode'));
  }
  showTheme();
  theme.addEventListener('click', () => {
    const value = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = value;
    try { localStorage.setItem('osdg-theme', value); } catch {}
    showTheme(); document.dispatchEvent(new Event('gosdthemechange'));
  });
  const languageLink = $('#language-link');
  languageLink.addEventListener('click', () => {
    const url = new URL(languageLink.href);
    const params = new URLSearchParams(location.search); params.delete('lang');
    url.search = params.toString(); url.hash = location.hash;
    languageLink.href = url.href;
  });
  function drawer(button, panel) {
    if (!button || !panel) return;
    const close = () => { panel.classList.remove('is-open'); button.setAttribute('aria-expanded', 'false'); };
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(open)); panel.classList.toggle('is-open', open);
    });
    panel.addEventListener('click', e => { if (e.target.closest('a')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && panel.classList.contains('is-open')) { close(); button.focus(); } });
  }
  drawer($('#nav-toggle'), $('#site-nav'));
  drawer($('.side-toggle'), $('#section-nav'));
  $$('[data-print]').forEach(b => b.addEventListener('click', () => window.print()));

  // Store the exact referring page and scroll position for contextual links.
  const returnLink = $('#return-source');
  const origin = readStore('gosd-origin:' + here()) || readStore('gosd-origin:' + location.pathname);
  if (returnLink && origin) {
    try {
      const source = new URL(origin.href, location.origin);
      if (source.origin === location.origin && source.pathname !== location.pathname) {
        returnLink.href = source.pathname + source.search + source.hash;
        returnLink.textContent = '← ' + t('返回：', 'Return to: ') + origin.label;
        returnLink.hidden = false;
        returnLink.addEventListener('click', () => writeStore('gosd-restore', {url:source.pathname + source.search, y:origin.y}));
      }
    } catch {}
  }
  function restorePosition() {
    const restore = readStore('gosd-restore');
    if (restore && restore.url === here()) {
      requestAnimationFrame(() => window.scrollTo({top:restore.y || 0, behavior:'instant'}));
      try { sessionStorage.removeItem('gosd-restore'); } catch {}
    }
  }
  window.addEventListener('pageshow', restorePosition);
  document.addEventListener('click', e => {
    const link = e.target.closest('a[href]');
    if (!link || e.defaultPrevented || link.hasAttribute('download') || link.id === 'return-source' || link.id === 'language-link' || link.closest('.site-header, .site-footer, .breadcrumbs')) return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin || url.pathname === location.pathname || !url.pathname.endsWith('/')) return;
    const sourceState = {href:location.pathname + location.search + location.hash,label: $('h1')?.textContent.trim() || 'GOSD',y:window.scrollY};
    writeStore('gosd-origin:' + url.pathname + url.search, sourceState);
    writeStore('gosd-origin:' + url.pathname, sourceState);
  });
  const localLinks = $$('.book-nav .local-section');
  if ('IntersectionObserver' in window && localLinks.length) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(e => e.isIntersecting).sort((a,b) => a.boundingClientRect.top-b.boundingClientRect.top);
      if (!visible.length) return;
      localLinks.forEach(link => link.hash === '#' + visible[0].target.id ? link.setAttribute('aria-current','location') : link.removeAttribute('aria-current'));
    }, {rootMargin:'-110px 0px -45% 0px',threshold:0});
    localLinks.forEach(link => { const target=document.getElementById(link.hash.slice(1)); if(target) observer.observe(target); });
  }

  const dialog = $('#site-search'), searchInput = $('#search-input'), results = $('#search-results');
  let searchIndex = null;
  async function search() {
    const query = searchInput.value.trim().toLowerCase();
    results.replaceChildren();
    if (!searchIndex) return;
    const entries = searchIndex.filter(x => x.lang === lang && (!query || `${x.title} ${x.description} ${x.category}`.toLowerCase().includes(query))).slice(0,12);
    if (!entries.length) { const p=document.createElement('p');p.className='small-note';p.textContent=t('未找到结果，试试章节名称或指标代码。','No results. Try a chapter title or indicator code.');results.append(p);return; }
    entries.forEach(item => {
      const link=document.createElement('a'), strong=document.createElement('strong'), small=document.createElement('small');
      link.href=item.url; strong.textContent=item.title;small.textContent=item.category+' · '+item.description;
      link.append(strong,small);results.append(link);
    });
  }
  $('#search-open').addEventListener('click', async () => {
    dialog.showModal(); searchInput.focus();
    if (!searchIndex) {
      results.textContent=t('正在载入索引…','Loading the index…');
      try { const response=await fetch(base + '/assets/search-index.json');if(!response.ok) throw new Error();searchIndex=await response.json(); }
      catch { results.textContent=t('暂时无法载入搜索，可通过顶部栏目与左侧目录继续浏览。','Search is unavailable. Use the top navigation and section contents.');return; }
    }
    search();
  });
  $('#search-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click', e=>{if(e.target===dialog){const b=dialog.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)dialog.close();}});
  results.addEventListener('click',e=>{if(e.target.closest('a'))dialog.close();});
  searchInput.addEventListener('input',search);

  const filters = $('#indicator-filters');
  if(filters){
    const input=$('#indicator-q'), select=$('#indicator-pillar'), entries=$$('.indicator-entry');
    function readFilters(){const params=new URLSearchParams(location.search);input.value=params.get('q')||'';select.value=params.get('pillar')||'';}
    function applyFilters(save=true){
      const q=input.value.trim().toLowerCase(), pillar=select.value;
      let count=0;
      entries.forEach(entry=>{const visible=(!q||entry.dataset.search.includes(q))&&(!pillar||entry.dataset.pillar===pillar);entry.hidden=!visible;if(visible)count++;});
      $('#indicator-count').textContent=t(`显示 ${count} / ${entries.length} 项指标`,`Showing ${count} / ${entries.length} indicators`);
      $('#indicator-empty').hidden=count!==0;
      if(save){const url=new URL(location.href);q?url.searchParams.set('q',input.value.trim()):url.searchParams.delete('q');pillar?url.searchParams.set('pillar',pillar):url.searchParams.delete('pillar');history.replaceState(null,'',url);}
    }
    function revealHash(){
      const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if(target?.classList.contains('indicator-entry')){
        if(target.hidden){input.value='';select.value='';applyFilters();}
        target.open=true;requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
      }
    }
    readFilters();applyFilters(false);revealHash();
    filters.addEventListener('submit',e=>e.preventDefault());
    input.addEventListener('input',()=>applyFilters());select.addEventListener('change',()=>applyFilters());
    filters.addEventListener('reset',e=>{e.preventDefault();input.value='';select.value='';const url=new URL(location.href);url.hash='';history.replaceState(null,'',url);applyFilters();});
    window.addEventListener('hashchange',revealHash);
    window.addEventListener('popstate',()=>{readFilters();applyFilters(false);revealHash();});
  }
  const stage=$('#demo');
  if(stage){
    const slides=$$('[data-slide]'),outline=$$('[data-goto-slide]');
    let current=1;
    function show(number,save=true){
      current=Math.max(1,Math.min(slides.length,Number.isFinite(number)?number:1));
      slides.forEach((slide,i)=>slide.hidden=i!==current-1);
      outline.forEach((b,i)=>{i===current-1?b.setAttribute('aria-current','step'):b.removeAttribute('aria-current');});
      $('#demo-prev').disabled=current===1;$('#demo-next').disabled=current===slides.length;$('#demo-counter').textContent=`${current} / ${slides.length}`;
      if(save){const url=new URL(location.href);url.searchParams.set('slide',current);history.replaceState(null,'',url);}
    }
    show(parseInt(initialParams.get('slide'),10),false);
    $('#demo-prev').addEventListener('click',()=>show(current-1));$('#demo-next').addEventListener('click',()=>show(current+1));
    outline.forEach(b=>b.addEventListener('click',()=>show(Number(b.dataset.gotoSlide))));
    stage.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();show(current+(e.key==='ArrowRight'?1:-1));}});
    const fullscreen=$('#demo-fullscreen');
    if(!document.fullscreenEnabled){fullscreen.hidden=true;}
    fullscreen.addEventListener('click',async()=>{try{document.fullscreenElement?await document.exitFullscreen():await stage.requestFullscreen();}catch{fullscreen.hidden=true;}});
    document.addEventListener('fullscreenchange',()=>{fullscreen.textContent=document.fullscreenElement?t('退出全屏','Exit fullscreen'):t('全屏','Fullscreen');});
    window.addEventListener('popstate',()=>show(parseInt(new URLSearchParams(location.search).get('slide'),10),false));
  }
})();
