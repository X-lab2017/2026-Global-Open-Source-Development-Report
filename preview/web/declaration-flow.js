/* The artboard never reflows; motion and focus are progressive enhancements. */
(() => {
  'use strict';
  for (const figure of document.querySelectorAll('[data-declaration-flow]')) {
    const t = (zh, en) => figure.dataset.lang === 'zh' ? zh : en;
    const motion = figure.querySelector('[data-df-motion]'), fullscreen = figure.querySelector('[data-df-fullscreen]');
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    const nodes = [...figure.querySelectorAll('[data-df-node]')], edges = [...figure.querySelectorAll('.df-edge')];
    const layers = [[1, 2], [3, 4, 5], [6, 7]];
    let paused = false, inView = !('IntersectionObserver' in window), hovered = null;
    const syncMotion = () => {
      const enabled = !paused && !reduced.matches;
      figure.dataset.running = String(enabled && inView && !document.hidden);
      motion.setAttribute('aria-pressed', String(enabled));
      motion.disabled = reduced.matches;
      motion.textContent = reduced.matches ? t('静态模式', 'Reduced motion') : paused ? t('播放流线', 'Play flow') : t('暂停流线', 'Pause flow');
    };
    const focus = () => {
      const active = figure.contains(document.activeElement) ? document.activeElement.closest('[data-df-node]') : null;
      const key = (hovered || active)?.dataset.dfNode;
      const layer = layers.findIndex((items, i) => key === `layer-${i+1}` || items.some(n => key === `principle-${n}`)) + 1;
      figure.classList.toggle('has-focus', !!key);
      for (const edge of edges) edge.classList.toggle('is-active', !!key && (layer ? edge.dataset.layer === String(layer) || edge.dataset.common === 'true' : key === 'core' || key === 'title' || edge.dataset.keys.split(' ').includes(key)));
    };
    motion.hidden = false;
    motion.addEventListener('click', () => {paused = !paused; syncMotion();});
    reduced.addEventListener('change', syncMotion);
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => {inView = entries[0].isIntersecting; syncMotion();}).observe(figure);
    document.addEventListener('visibilitychange', syncMotion);
    for (const node of nodes) {
      node.addEventListener('pointerenter', () => {hovered = node; focus();});
      node.addEventListener('pointerleave', () => {hovered = null; focus();});
      node.addEventListener('focus', focus);
      node.addEventListener('blur', () => requestAnimationFrame(focus));
    }
    if (document.fullscreenEnabled && figure.requestFullscreen) {
      fullscreen.hidden = false;
      fullscreen.addEventListener('click', async () => {
        try {if (document.fullscreenElement === figure) await document.exitFullscreen(); else await figure.requestFullscreen();}
        catch {fullscreen.hidden = true;}
      });
      document.addEventListener('fullscreenchange', () => {
        const open = document.fullscreenElement === figure;
        fullscreen.textContent = open ? t('退出全屏', 'Exit full screen') : t('全屏', 'Full screen');
        fullscreen.setAttribute('aria-pressed', String(open));
        hovered = null; focus();
      });
      figure.addEventListener('click', async event => {
        const anchor = event.target.closest('a[href^="#"]');
        if (!anchor || document.fullscreenElement !== figure || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        try {await document.exitFullscreen();} catch {return;}
        location.hash = anchor.getAttribute('href');
        document.querySelector(anchor.getAttribute('href'))?.scrollIntoView({block:'start'});
      });
    }
    syncMotion();
  }
})();
