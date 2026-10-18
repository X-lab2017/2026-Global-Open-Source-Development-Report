/* Progressive enhancement: all observations and recommendations remain readable without JS. */
(() => {
  const root = document.querySelector('.executive-summary');
  if (!root) return;
  for (const group of root.querySelectorAll('[data-es-switcher]')) {
    const list = group.querySelector('[data-es-tabs]');
    const buttons = [...list.querySelectorAll('[data-es-target]')];
    const panels = [...group.querySelectorAll('[data-es-panel]')];
    list.setAttribute('role', 'tablist');
    buttons.forEach(button => {
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-controls', button.dataset.esTarget);
      const panel = panels.find(item => item.id === button.dataset.esTarget);
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', button.id);
      panel.tabIndex = 0;
    });
    function select(button, focus = false) {
      buttons.forEach(item => {
        const selected = item === button;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
      });
      panels.forEach(panel => { panel.hidden = panel.id !== button.dataset.esTarget; });
      if (focus) button.focus();
    }
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => select(button));
      button.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % buttons.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + buttons.length) % buttons.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = buttons.length - 1;
        else return;
        event.preventDefault();
        select(buttons[next], true);
      });
    });
    select(buttons[0]);
  }
})();
