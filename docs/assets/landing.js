/* Double reading: open the response, inspect its value, connect the failed assertion. */
(() => {
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = false, dispose = () => {};
  function mount() {
    dispose();
    const hero = document.querySelector('[data-er-hero]');
    const pause = hero?.querySelector('[data-er-pause]');
    const cue = hero?.querySelector('.er-scroll-cue');
    const search = document.querySelector('.er-search-trigger');
    const es = document.documentElement.lang === 'es';
    const cleanups = [];
    const scene = hero?.querySelector('[data-er-scene]');
    const frame = document.querySelector('.er-real-report iframe');
    let elapsed = 0, previous = null, raf = null, inView = true;
    const clamp = value => Math.max(0, Math.min(1, value));
    const smooth = value => { value = clamp(value); return value * value * (3 - 2 * value); };
    function render() {
      if (!scene) return;
      const t = motion.matches ? 5800 : elapsed % 10000;
      const opening = (1 - Math.cos(t / 10000 * Math.PI * 2)) / 2;
      const fade = 1 - smooth((t - 8000) / 1600);
      const value = smooth((t - 1800) / 1000) * fade;
      const cyan = smooth((t - 1200) / 2300) * fade;
      const rose = smooth((t - 3700) / 1500) * fade;
      const distance = Math.min(24, scene.clientWidth * .035);
      scene.querySelector('.er-piece-left').style.transform =
        `translate3d(${-opening * distance}px,${Math.sin(t / 10000 * Math.PI * 2) * 5}px,0) rotate(${-opening * 3}deg)`;
      scene.querySelector('.er-piece-right').style.transform =
        `translate3d(${opening * distance}px,${-Math.sin(t / 10000 * Math.PI * 2) * 5}px,0) rotate(${opening * 3}deg)`;
      scene.querySelector('.er-value-label').style.opacity = String(value);
      scene.querySelector('.er-response-label').style.opacity = String(.45 + .55 * cyan);
      const cyanLine = scene.querySelector('.er-cyan-connection');
      cyanLine.style.clipPath = `inset(0 0 ${(1 - cyan) * 100}% 0)`;
      cyanLine.style.opacity = String(cyan);
      const roseLine = scene.querySelector('.er-rose-connection');
      roseLine.style.clipPath = `inset(0 ${(1 - rose) * 100}% 0 0)`;
      roseLine.style.opacity = String(rose);
      scene.querySelector('.er-validation-label').style.opacity = String(rose);
      scene.dataset.focus = String(t >= 5200 && t < 6700);
      scene.dataset.stage = t < 1800 ? 'opening' : t < 3700 ? 'response' : t < 6700 ? 'assertion' : 'return';
    }
    function tick(now) {
      raf = null;
      if (paused || motion.matches || document.hidden || !inView) { previous = null; return; }
      if (previous !== null) elapsed += now - previous;
      previous = now;
      render();
      raf = requestAnimationFrame(tick);
    }
    function listen(element, event, callback) {
      if (!element) return;
      element.addEventListener(event, callback);
      cleanups.push(() => element.removeEventListener(event, callback));
    }
    function update() {
      document.body.dataset.erMotionPaused = String(paused || motion.matches);
      previous = null;
      if (raf !== null) cancelAnimationFrame(raf);
      raf = null;
      render();
      if (scene && !paused && !motion.matches && !document.hidden && inView) raf = requestAnimationFrame(tick);
      if (!pause) return;
      pause.hidden = false;
      pause.disabled = motion.matches;
      pause.setAttribute('aria-pressed', String(paused || motion.matches));
      pause.querySelector('span:last-child').textContent = motion.matches
        ? (es ? 'Movimiento reducido' : 'Reduced motion')
        : paused ? (es ? 'Reanudar animación' : 'Resume animation')
        : (es ? 'Pausar animación' : 'Pause animation');
      pause.querySelector('.er-icon').innerHTML = paused
        ? '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'
        : '<svg viewBox="0 0 24 24"><path d="M6 5h4v14H6zm8 0h4v14h-4z"/></svg>';
    }
    function syncHeaderMotion() {
      if (hero) return;
      const animation = selector => document.querySelector(selector)?.getAnimations?.()
        .find(item => item.animationName === 'er-header-flow');
      const header = animation('.md-header'), tabs = animation('.md-tabs');
      // Tabs restart when they reappear after a mobile viewport; restore the shared phase.
      if (header && tabs && header.currentTime !== null) tabs.currentTime = header.currentTime;
    }
    listen(pause, 'click', () => { paused = !paused; update(); });
    for (const link of [cue, hero?.querySelector('.er-action-secondary')]) listen(link, 'click', event => {
      const id = link.hash.slice(1);
      const content = document.getElementById(id);
      if (!content) return;
      event.preventDefault();
      history.replaceState(null, '', '#' + id);
      dispatchEvent(new HashChangeEvent('hashchange'));
      content.scrollIntoView({behavior: motion.matches ? 'auto' : 'smooth', block: 'start'});
      content.focus({preventScroll: true});
    });
    listen(search, 'keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        search.click();
      }
    });
    listen(motion, 'change', update);
    listen(document, 'visibilitychange', update);
    listen(window, 'resize', render);
    if (scene && typeof IntersectionObserver !== 'undefined') {
      const observer = new IntersectionObserver(entries => { inView = entries[0].isIntersecting; update(); });
      observer.observe(scene);
      cleanups.push(() => observer.disconnect());
    }
    // Preserve the native report view across full EN/ES navigation.
    const stateKey = 'rr-book-report-state';
    function reportState() {
      try {
        const doc = frame?.contentDocument;
        if (!doc?.querySelector('.sections')) return null;
        return {
          section: doc.querySelector('.sections [aria-pressed="true"]')?.dataset.section || 'summary',
          request: doc.querySelector('#requests [aria-pressed="true"]')?.dataset.request || '0',
          tab: doc.querySelector('[data-tab][aria-selected="true"]')?.dataset.tab || 'response',
          filter: doc.querySelector('[data-filter][aria-pressed="true"]')?.dataset.filter || 'all'
        };
      } catch { return null; }
    }
    function syncReportTheme() {
      try {
        const doc = frame?.contentDocument;
        const theme = document.body.dataset.mdColorScheme === 'slate' ? 'dark' : 'light';
        if (doc?.documentElement?.dataset.theme && doc.documentElement.dataset.theme !== theme)
          doc.getElementById('theme-toggle')?.click();
      } catch { /* A pending iframe load will retry on load. */ }
    }
    function restoreReport() {
      syncReportTheme();
      try {
        const raw = sessionStorage.getItem(stateKey);
        if (!raw || frame?.contentDocument?.readyState !== 'complete' ||
            !frame.contentDocument.querySelector('.sections')) return;
        const state = JSON.parse(raw), doc = frame.contentDocument;
        // Instant navigation can briefly remount the outgoing page. Only the
        // destination locale may consume the state saved for the language switch.
        if (state.language !== document.documentElement.lang ||
            state.language !== doc.documentElement.lang) return;
        sessionStorage.removeItem(stateKey);
        if (!['summary', 'failures', 'requests'].includes(state.section)) return;
        doc.querySelector(`[data-section="${state.section}"]`)?.click();
        if (state.section === 'requests') {
          if (/^\d+$/.test(state.request)) doc.querySelector(`[data-request="${state.request}"]`)?.click();
          if (['response', 'request', 'params', 'headers', 'assertions'].includes(state.tab)) doc.querySelector(`[data-tab="${state.tab}"]`)?.click();
          if (['all', 'pass', 'fail'].includes(state.filter)) doc.querySelector(`[data-filter="${state.filter}"]`)?.click();
        }
      } catch { /* Storage may be disabled; the report still works independently. */ }
    }
    function preserveReport(event) {
      const languageLink = event.target.closest('[data-doc-language]');
      if (!languageLink) return;
      try {
        const state = reportState();
        if (state) sessionStorage.setItem(stateKey, JSON.stringify({
          ...state, language: languageLink.dataset.docLanguage
        }));
        const bounds = frame?.getBoundingClientRect();
        if ((state && state.section !== 'summary') ||
            (bounds && bounds.top < innerHeight && bounds.bottom > 0)) {
          const destination = new URL(languageLink.href);
          destination.hash = 'report-preview';
          languageLink.href = destination.href;
        }
      } catch { /* Storage is optional. */ }
    }
    document.addEventListener('click', preserveReport, true);
    cleanups.push(() => document.removeEventListener('click', preserveReport, true));
    listen(frame, 'load', restoreReport);
    const themeObserver = new MutationObserver(syncReportTheme);
    themeObserver.observe(document.body, {attributes: true, attributeFilter: ['data-md-color-scheme']});
    cleanups.push(() => themeObserver.disconnect());
    restoreReport();
    listen(window, 'resize', syncHeaderMotion);
    update();
    syncHeaderMotion();
    dispose = () => {
      if (raf !== null) cancelAnimationFrame(raf);
      cleanups.forEach(cleanup => cleanup());
    };
  }
  if (typeof document$ !== 'undefined') document$.subscribe(mount);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
