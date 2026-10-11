'use strict';
(() => {
  const root = document.documentElement;
  const button = document.getElementById('theme-toggle');
  const english = root.lang === 'en';
  function refreshTheme() {
    const dark = root.dataset.theme === 'dark';
    button.setAttribute('aria-pressed', String(dark));
    button.setAttribute('aria-label', english ? (dark ? 'Switch to light mode' : 'Switch to dark mode') : (dark ? '切换为浅色模式' : '切换为深色模式'));
    button.textContent = dark ? (english ? 'Light' : '浅色') : (english ? 'Dark' : '深色');
    document.querySelector('meta[name="theme-color"]').content = dark ? '#0A2C49' : '#F3F8FA';
  }
  button.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('osdg-theme', root.dataset.theme); } catch {}
    refreshTheme();
  });
  document.getElementById('language-link').addEventListener('click', event => {
    try { localStorage.setItem('osdg-language', english ? 'zh' : 'en'); } catch {}
    if (location.hash) event.currentTarget.href += location.hash;
  });
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
  refreshTheme();
})();
