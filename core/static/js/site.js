(() => {
  // Sticky nav border once the page scrolls
  const nav = document.querySelector('[data-nav]');
  if (nav) {
    const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Mobile menu
  const toggle = document.querySelector('[data-nav-toggle]');
  const menu = document.getElementById('mnav');
  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      menu.hidden = open;
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth > 960 && !menu.hidden) { menu.hidden = true; toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Work page industry filter
  const filters = document.querySelector('[data-filters]');
  const grid = document.querySelector('[data-grid]');
  if (filters && grid) {
    const empty = document.querySelector('[data-empty]');
    filters.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-filter]');
      if (!btn) return;
      const f = btn.dataset.filter;
      filters.querySelectorAll('[data-filter]').forEach(b => {
        const on = b === btn; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', String(on));
      });
      let shown = 0;
      grid.querySelectorAll('.wcard').forEach(c => {
        const match = f === 'all' || c.dataset.industry === f;
        c.hidden = !match; if (match) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    });
  }
})();
