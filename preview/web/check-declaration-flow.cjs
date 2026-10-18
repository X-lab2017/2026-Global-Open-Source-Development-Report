/* Interaction/state checks using synthetic rectangles, not a browser geometry test.
   Run with the same linkedom dependency as check-frontmatter.cjs. */
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert');
const {parseHTML} = require('linkedom');
const out = path.resolve(process.argv[2] || '_site');

(async () => {
  for (const lang of ['zh', 'en']) {
    const {window:w} = parseHTML(fs.readFileSync(path.join(out, `2026/${lang}/introduction/index.html`), 'utf8'));
    const d = w.document, figure = d.querySelector('[data-declaration-flow]'), board = figure.querySelector('.df-canvas');
    assert(figure && d.querySelector('link[href*="declaration-flow.css"]'));
    assert(!d.querySelector('.declaration-principles-map'), 'Replace the old navigator instead of duplicating it');
    for (const a of figure.querySelectorAll('a[href^="#"]')) assert(d.querySelector(a.getAttribute('href')), 'Every node must reach the declaration');
    const printURL = figure.querySelector('.df-print').getAttribute('src');
    assert.equal(printURL, figure.querySelector('a[download]').getAttribute('href'));
    assert(fs.existsSync(path.join(out, 'assets/declaration/overview-' + lang + '.svg')));

    let resize, visibility, preferenceChange, small = false, queue = [];
    const pref = {matches:false, addEventListener(name, fn) {preferenceChange = fn;}};
    w.matchMedia = () => pref;
    w.ResizeObserver = class {constructor(fn) {resize = fn;} observe() {}};
    w.IntersectionObserver = class {constructor(fn) {visibility = fn;} observe() {}};
    w.requestAnimationFrame = fn => {queue.push(fn); return queue.length;};
    const flush = () => {const batch = queue; queue = []; batch.forEach(fn => fn());};
    const box = (x,y,width,height) => ({left:x,top:y,width,height});
    board.getBoundingClientRect = () => box(0,0,small ? 350 : 950,small ? 1500 : 600);
    for (const node of figure.querySelectorAll('[data-df-node], [data-df-group]')) {
      node.getBoundingClientRect = () => {
        const key = node.dataset.dfNode, g = Number(node.dataset.dfGroup);
        const group = key?.startsWith('layer-') ? Number(key.split('-')[1]) : g;
        if (group) return small ? box(10,320+(group-1)*300,330,key ? 45 : 280) : box(10+(group-1)*310,260,290,key ? 45 : 230);
        if (key?.startsWith('principle-')) {
          const n = Number(key.split('-')[1]), groupNo = n < 3 ? 1 : n < 6 ? 2 : 3, row = n < 3 ? n-1 : n < 6 ? n-3 : n-6;
          return small ? box(30,380+(groupNo-1)*300+row*70,300,55) : box(30+(groupNo-1)*310,320+row*55,260,45);
        }
        const boxes = small ? {title:[0,0,350,80],context:[0,105,350,65],vision:[0,195,350,65],core:[80,280,180,30],action:[10,1270,330,80]} : {title:[0,0,950,75],context:[10,100,440,70],vision:[500,100,440,70],core:[360,205,230,30],action:[10,525,930,75]};
        return box(...boxes[key]);
      };
    }
    d.fullscreenEnabled = true;
    figure.requestFullscreen = async () => {d.fullscreenElement = figure; d.dispatchEvent(new w.Event('fullscreenchange'));};
    d.exitFullscreen = async () => {d.fullscreenElement = null; d.dispatchEvent(new w.Event('fullscreenchange'));};
    w.location = {hash:''};
    w.HTMLElement.prototype.scrollIntoView = function() {this.dataset.scrolled = 'true';};
    vm.runInContext(fs.readFileSync(path.join(out,'declaration-flow.js'),'utf8'), vm.createContext({window:w, document:d, location:w.location, requestAnimationFrame:w.requestAnimationFrame, IntersectionObserver:w.IntersectionObserver, ResizeObserver:w.ResizeObserver}));
    flush();
    const motion = figure.querySelector('[data-df-motion]'), full = figure.querySelector('[data-df-fullscreen]');
    assert.equal(figure.dataset.running, 'false', 'Do not animate outside the viewport');
    visibility([{isIntersecting:true}]);
    assert.equal(figure.dataset.running,'true');
    motion.click(); assert.equal(figure.dataset.running,'false');
    motion.click(); assert.equal(figure.dataset.running,'true');
    pref.matches = true; preferenceChange();
    assert.equal(figure.dataset.running,'false'); assert(motion.disabled);
    pref.matches = false; preferenceChange(); assert.equal(figure.dataset.running,'true');
    d.hidden = true; d.dispatchEvent(new w.Event('visibilitychange')); assert.equal(figure.dataset.running,'false');
    d.hidden = false; d.dispatchEvent(new w.Event('visibilitychange')); assert.equal(figure.dataset.running,'true');
    const principle = figure.querySelector('[data-df-node="principle-4"]');
    principle.dispatchEvent(new w.Event('pointerenter'));
    assert(figure.classList.contains('has-focus'));
    assert(figure.querySelector('.df-edge[data-layer="2"]').classList.contains('is-active'));
    assert(!figure.querySelector('.df-edge[data-layer="1"]').classList.contains('is-active'));
    principle.dispatchEvent(new w.Event('pointerleave')); assert(!figure.classList.contains('has-focus'));
    const links = [...figure.querySelectorAll('.df-node[href]')].map(n => n.getAttribute('href'));
    for (const stacked of [false,true,false]) {
      small = stacked; resize(); flush();
      assert(figure.querySelectorAll('.df-edge').length > 7);
      for (const edge of figure.querySelectorAll('path')) assert(!/NaN|undefined|Infinity/.test(edge.getAttribute('d')));
    }
    full.click(); await new Promise(resolve => setImmediate(resolve)); flush();
    assert.equal(d.fullscreenElement,figure); assert.equal(full.getAttribute('aria-pressed'),'true');
    principle.click(); await new Promise(resolve => setImmediate(resolve)); flush();
    assert.equal(d.fullscreenElement,null); assert.equal(w.location.hash,'#declaration-principle-4');
    assert.equal(d.querySelector('#declaration-principle-4').dataset.scrolled,'true');
    assert.equal(full.getAttribute('aria-pressed'),'false');
    assert.deepEqual([...figure.querySelectorAll('.df-node[href]')].map(n=>n.getAttribute('href')), links);
  }
  console.log('PASS: bilingual declaration anchors, static exports, viewport/pause/reduced-motion state, highlight, resize, full-screen exit and original-text navigation. DOM harness only.');
})().catch(error => {console.error(error); process.exitCode=1;});
