/* SVG wires follow measured HTML nodes; typography never scales with the canvas. */
(() => {
  'use strict';
  for (const figure of document.querySelectorAll('[data-declaration-flow]')) {
    const zh = figure.dataset.lang === 'zh', t = (a, b) => zh ? a : b;
    const board = figure.querySelector('.df-canvas'), svg = figure.querySelector('.df-wires');
    const motion = figure.querySelector('[data-df-motion]'), fullscreen = figure.querySelector('[data-df-fullscreen]');
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    let paused = false, inView = !('IntersectionObserver' in window), frame = 0, hovered = null;
    const nodes = new Map([...figure.querySelectorAll('[data-df-node]')].map(el => [el.dataset.dfNode, el]));
    const layers = [[1, 2], [3, 4, 5], [6, 7]];
    const NS = 'http://www.w3.org/2000/svg';
    const create = (tag, attributes) => {
      const el = document.createElementNS(NS, tag);
      for (const [key, value] of Object.entries(attributes)) el.setAttribute(key, String(value));
      return el;
    };
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
      const layer = layers.findIndex((items, i) => key === `layer-${i + 1}` || items.some(n => key === `principle-${n}`)) + 1;
      figure.classList.toggle('has-focus', !!key);
      for (const edge of svg.children) {
        edge.classList.toggle('is-active', !!key && (layer ? edge.dataset.layer === String(layer) || edge.dataset.common === 'true' : edge.dataset.keys.split(' ').includes(key)));
      }
    };
    function draw() {
      const bounds = board.getBoundingClientRect();
      if (!bounds.width || !bounds.height) return;
      const rect = el => {
        const r = el.getBoundingClientRect();
        return { x: r.left - bounds.left, y: r.top - bounds.top, w: r.width, h: r.height };
      };
      const r = key => rect(nodes.get(key));
      const point = (a, side) => side === 'top' ? [a.x + a.w / 2, a.y] : side === 'bottom' ? [a.x + a.w / 2, a.y + a.h] : side === 'left' ? [a.x, a.y + a.h / 2] : [a.x + a.w, a.y + a.h / 2];
      const vertical = (a, b) => { const y = (a[1] + b[1]) / 2; return `M${a}C${a[0]},${y} ${b[0]},${y} ${b}`; };
      svg.replaceChildren();
      svg.setAttribute('viewBox', `0 0 ${bounds.width} ${bounds.height}`);
      const edge = (d, end, keys, layer = 0, common = false) => {
        const group = create('g', {class: 'df-edge', 'data-keys': keys, 'data-layer': layer, 'data-common': common});
        group.append(create('path', {d, class: 'df-edge-base'}), create('path', {d, class: 'df-edge-pulse', pathLength: 100}), create('circle', {cx: end[0], cy: end[1], r: 2.2, class: 'df-edge-dot'}));
        svg.append(group);
      };
      const connect = (from, to, layer = 0, common = false) => {
        const start = point(r(from), 'bottom'), end = point(r(to), 'top');
        edge(vertical(start, end), end, `${from} ${to}`, layer, common);
      };
      const context = r('context'), vision = r('vision'), title = r('title');
      const begin = [context.x + context.w / 2, title.y + title.h], cTop = point(context, 'top');
      edge(vertical(begin, cTop), cTop, 'title context', 0, true);
      if (Math.abs(context.y - vision.y) < 10) {
        const start = point(context, 'right'), end = point(vision, 'left');
        edge(`M${start}L${end}`, end, 'context vision', 0, true);
      } else connect('context', 'vision', 0, true);
      connect('vision', 'core', 0, true);
      const groups = [...figure.querySelectorAll('[data-df-group]')];
      const stacked = groups.length > 1 && Math.abs(rect(groups[0]).y - rect(groups[1]).y) > 10;
      layers.forEach((items, index) => {
        const layer = index + 1, heading = r(`layer-${layer}`), group = rect(groups[index]);
        const start = point(r('core'), 'bottom'), end = point(heading, 'top');
        // On narrow screens each layer branches from a rail in the outer gutter.
        const railX = group.x - 5;
        edge(stacked ? `M${start}V${start[1]+8}H${railX}V${end[1]-7}H${end[0]}V${end[1]}` : vertical(start, end), end, `core layer-${layer}`, layer);
        for (const n of items) {
          const card = r(`principle-${n}`), source = point(heading, 'bottom'), dest = point(card, 'left'), rail = card.x - 5;
          edge(`M${source}V${source[1]+4}H${rail}V${dest[1]}H${dest[0]}`, dest, `layer-${layer} principle-${n}`, layer);
        }
        const from = point(group, 'bottom'), dest = point(r('action'), 'top');
        // Stack-mode return rail is on the opposite side, clear of all labels.
        const rightRail = group.x + group.w + 5;
        edge(stacked ? `M${from}V${from[1]+7}H${rightRail}V${dest[1]-10}H${dest[0]}V${dest[1]}` : vertical(from, dest), dest, `layer-${layer} action`, layer);
      });
      focus();
    }
    const schedule = () => { if (!frame) frame = requestAnimationFrame(() => { frame = 0; draw(); }); };
    motion.hidden = false;
    motion.addEventListener('click', () => { paused = !paused; syncMotion(); });
    reduced.addEventListener('change', syncMotion);
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => { inView = entries[0].isIntersecting; syncMotion(); }).observe(figure);
    document.addEventListener('visibilitychange', syncMotion);
    for (const node of nodes.values()) {
      node.addEventListener('pointerenter', () => { hovered = node; focus(); });
      node.addEventListener('pointerleave', () => { hovered = null; focus(); });
      node.addEventListener('focus', focus);
      node.addEventListener('blur', () => requestAnimationFrame(focus));
    }
    if (document.fullscreenEnabled && figure.requestFullscreen) {
      fullscreen.hidden = false;
      fullscreen.addEventListener('click', async () => {
        try { if (document.fullscreenElement === figure) await document.exitFullscreen(); else await figure.requestFullscreen(); }
        catch { fullscreen.hidden = true; }
      });
      document.addEventListener('fullscreenchange', () => {
        const open = document.fullscreenElement === figure;
        fullscreen.textContent = open ? t('退出全屏', 'Exit full screen') : t('全屏', 'Full screen');
        fullscreen.setAttribute('aria-pressed', String(open));
        schedule();
      });
      // A principle always takes the reader to the original prose, including from full screen.
      figure.addEventListener('click', async event => {
        const anchor = event.target.closest('a[href^="#"]');
        if (!anchor || document.fullscreenElement !== figure || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        try { await document.exitFullscreen(); } catch { return; }
        location.hash = anchor.getAttribute('href');
        document.querySelector(anchor.getAttribute('href'))?.scrollIntoView({block: 'start'});
      });
    }
    if ('ResizeObserver' in window) new ResizeObserver(schedule).observe(board);
    window.addEventListener('resize', schedule, {passive: true});
    document.fonts?.ready.then(schedule);
    syncMotion();
    schedule();
  }
})();
