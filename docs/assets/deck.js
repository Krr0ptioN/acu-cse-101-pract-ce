/* Interactive lecture deck engine.
 *
 * Deck.init({ id, course, title, slides, createLab })
 *
 * Slide types:
 *   title     – custom html, no header
 *   section   – part divider ({num, title, sub})
 *   concept   – header + html
 *   demo      – explanation + scripted steps on the left, live lab on the right
 *   predict   – question + options; "Reveal" runs the steps and shows the answer
 *   challenge – tasks checked live against the lab, with a solution
 *
 * Keys: → / Space next · ← back · Enter run next demo step · O overview
 *       D dark mode · F fullscreen · R reset demo · Esc leave terminal
 */
(function () {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const h = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };
  const ICON = {
    grid: '<svg viewBox="0 0 24 24"><path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    moon: '<svg viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 019.5 4a8 8 0 1010.5 10.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    full: '<svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    prev: '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    next: '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    play: '<svg viewBox="0 0 24 24"><path d="M7 5l12 7-12 7z" fill="currentColor"/></svg>',
    reset: '<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 108-8H8M8 4l-3 3 3 3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 1)"/></svg>',
    check: '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    eye: '<svg viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    plus: '<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    minus: '<svg viewBox="0 0 24 24"><path d="M5 12h14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
  };
  const TYPE_BADGE = { demo: ['Live demo', 'b-demo'], predict: ['Predict', 'b-predict'], challenge: ['Your turn', 'b-challenge'] };

  const S = { i: 0, el: [], labs: new Map(), zoom: 1.0 };

  function init(cfg) {
    S.cfg = cfg;
    document.body.dataset.course = cfg.id;
    document.body.classList.toggle('single', !!cfg.single);
    const theme = store.get('deck.theme');
    if (theme) document.documentElement.dataset.theme = theme;
    const textSize = store.get('deck.textSize') || 'normal';
    document.documentElement.dataset.textSize = textSize;
    S.zoom = parseFloat(store.get('deck.zoom')) || 1.0;

    S.sections = [];
    cfg.slides.forEach((s, i) => {
      const last = S.sections[S.sections.length - 1];
      if (!last || last.name !== s.section) S.sections.push({ name: s.section, from: i, to: i });
      else last.to = i;
    });

    buildShell();
    window.addEventListener('resize', fit);
    window.addEventListener('wheel', (e) => {
      if (e.ctrlKey) {
        e.preventDefault();
        const delta = e.deltaY < 0 ? 0.1 : -0.1;
        setZoom(S.zoom + delta);
      }
    }, { passive: false });
    fit();
    document.addEventListener('keydown', onKey);
    window.addEventListener('hashchange', () => { const n = fromHash(); if (n !== S.i) go(n, { instant: false }); });
    go(fromHash(), { instant: true });
    document.fonts && document.fonts.ready.then(() => { const lab = S.labs.get(S.i); lab && lab.refresh && lab.refresh(); });
  }

  function fromHash() { if (S.cfg.single) return 0; const n = parseInt(location.hash.slice(1), 10); return Number.isFinite(n) ? Math.min(Math.max(n - 1, 0), S.cfg.slides.length - 1) : 0; }

  // ---------------------------------------------------------------- shell
  function buildShell() {
    const cfg = S.cfg;
    const vp = h('div', 'viewport');
    const stageWrap = h('div', 'stage-wrap');
    const stage = h('div', 'stage');
    stageWrap.appendChild(stage);
    vp.appendChild(stageWrap);
    document.body.appendChild(vp);
    S.viewport = vp;
    S.stageWrap = stageWrap;
    S.stage = stage;
    S.slidesBox = h('div', 'slides');
    stage.appendChild(S.slidesBox);

    const hud = h('div', 'hud');
    hud.innerHTML = `
      <div class="hud-left"><a class="hud-course" href="../index.html" title="All lectures">${esc(cfg.course)}</a><span class="hud-title">${esc(cfg.title)}</span><span class="hud-sep">/</span><span class="hud-section"></span></div>
      <div class="hud-progress"></div>
      <div class="hud-right">
        <button class="hud-btn" data-act="prev" title="Previous (←)">${ICON.prev}</button>
        <span class="hud-count"></span>
        <button class="hud-btn" data-act="next" title="Next (→)">${ICON.next}</button>
        <div class="hud-zoom-grp">
          <button class="hud-btn" data-act="zoom-out" title="Zoom out (- / Ctrl+Wheel)">${ICON.minus}</button>
          <button class="hud-btn hud-zoom-lbl" data-act="zoom-reset" title="Reset Zoom (0)">Fit</button>
          <button class="hud-btn" data-act="zoom-in" title="Zoom in (+ / Ctrl+Wheel)">${ICON.plus}</button>
        </div>
        <button class="hud-btn hud-text-size" data-act="text-size" title="Toggle presentation text size (Z)">A<span class="size-ind">A</span></button>
        <button class="hud-btn" data-act="overview" title="Overview (O)">${ICON.grid}</button>
        <button class="hud-btn" data-act="theme" title="Dark / light (D)">${ICON.moon}</button>
        <button class="hud-btn" data-act="full" title="Fullscreen (F)">${ICON.full}</button>
      </div>`;
    stage.appendChild(hud);
    S.hud = hud;
    const prog = $('.hud-progress', hud);
    for (const sec of S.sections) {
      const seg = h('button', 'seg', '<i></i>');
      seg.style.flex = String(sec.to - sec.from + 1);
      seg.title = sec.name;
      seg.addEventListener('click', () => go(sec.from));
      prog.appendChild(seg);
      sec.seg = seg;
    }
    hud.addEventListener('click', (e) => {
      const b = e.target.closest('[data-act]'); if (!b) return;
      const a = b.dataset.act;
      if (a === 'prev') prev(); else if (a === 'next') next();
      else if (a === 'zoom-in') setZoom(S.zoom + 0.15);
      else if (a === 'zoom-out') setZoom(S.zoom - 0.15);
      else if (a === 'zoom-reset') setZoom(1.0);
      else if (a === 'text-size') cycleTextSize();
      else if (a === 'overview') toggleOverview();
      else if (a === 'theme') toggleTheme(); else if (a === 'full') toggleFull();
    });
    S.exBig = h('div', 'ex-big');
    S.exBig.addEventListener('click', hideExercise);
    stage.appendChild(S.exBig);
    S.overview = h('div', 'overview');
    stage.appendChild(S.overview);
    buildOverview();

    S.el = cfg.slides.map(() => null);
  }

  function fit() {
    const W = 1600, H = 900;
    const baseScale = Math.min(window.innerWidth / W, window.innerHeight / H);
    const s = baseScale * (S.zoom || 1.0);
    S.scale = s;
    if (S.stageWrap) {
      const visualW = Math.round(W * s);
      const visualH = Math.round(H * s);
      S.stageWrap.style.width = visualW + 'px';
      S.stageWrap.style.height = visualH + 'px';
      S.stage.style.transform = `scale(${s})`;
      S.stage.style.transformOrigin = '0 0';
    } else {
      S.stage.style.transform = `translate(-50%, -50%) scale(${s})`;
    }
    updateZoomHud();
  }

  function setZoom(val) {
    val = Math.max(0.75, Math.min(val, 2.25));
    if (Math.abs(val - 1.0) < 0.04) val = 1.0;
    S.zoom = Math.round(val * 100) / 100;
    store.set('deck.zoom', S.zoom);
    fit();
  }

  function updateZoomHud() {
    if (!S.hud) return;
    const lbl = $('.hud-zoom-lbl', S.hud);
    if (lbl) {
      const pct = Math.round((S.zoom || 1.0) * 100);
      lbl.textContent = pct === 100 ? 'Fit' : pct + '%';
      lbl.classList.toggle('zoomed', pct !== 100);
    }
    const txtBtn = $('.hud-text-size .size-ind', S.hud);
    if (txtBtn) {
      const cur = document.documentElement.dataset.textSize || 'normal';
      txtBtn.textContent = cur.toUpperCase();
    }
  }

  const TEXT_SIZES = ['normal', 'large', 'xl'];
  function cycleTextSize(targetSize) {
    const cur = document.documentElement.dataset.textSize || 'normal';
    const next = targetSize || TEXT_SIZES[(TEXT_SIZES.indexOf(cur) + 1) % TEXT_SIZES.length];
    document.documentElement.dataset.textSize = next;
    store.set('deck.textSize', next);
    updateZoomHud();
    S.labs.forEach((l) => l.refresh && l.refresh());
  }

  function buildOverview() {
    const o = S.overview;
    o.innerHTML = `<div class="ov-head"><h3>${esc(S.cfg.course)} · ${esc(S.cfg.title)}</h3><span>${S.cfg.slides.length} slides</span><button class="hud-btn ov-close" title="Close (Esc)">✕</button></div><div class="ov-grid"></div>`;
    const grid = $('.ov-grid', o);
    S.sections.forEach((sec, si) => {
      const col = h('div', 'ov-sec');
      col.innerHTML = `<div class="ov-sec-h"><b>${esc(sec.name)}</b></div>`;
      for (let i = sec.from; i <= sec.to; i++) {
        const s = S.cfg.slides[i];
        const b = h('button', 'ov-item t-' + s.type, `<span class="n">${i + 1}</span><span class="t">${esc(s.navTitle || s.title || '')}</span>${TYPE_BADGE[s.type] ? `<span class="b ${TYPE_BADGE[s.type][1]}">${TYPE_BADGE[s.type][0]}</span>` : ''}`);
        b.addEventListener('click', () => { toggleOverview(false); go(i); });
        b.dataset.i = i;
        col.appendChild(b);
      }
      grid.appendChild(col);
    });
    $('.ov-close', o).addEventListener('click', () => toggleOverview(false));
  }

  // ---------------------------------------------------------------- slides
  function header(s) {
    const badge = TYPE_BADGE[s.type];
    return `<header class="sl-head"><div><div class="kicker">${esc(s.section || '')}</div><h2>${s.title}</h2></div>${badge ? `<span class="type-badge ${badge[1]}">${badge[0]}</span>` : ''}</header>`;
  }

  function buildSlide(i) {
    const s = S.cfg.slides[i];
    const el = h('section', `slide t-${s.type} ${s.cls || ''}`);
    el.dataset.i = i;
    if (s.type === 'title') el.innerHTML = s.html;
    else if (s.type === 'section') {
      el.innerHTML = `<div class="sec-wrap"><div class="sec-num rv">${String(s.num).padStart(2, '0')}</div><div class="sec-body"><div class="kicker rv">Part ${s.num}</div><h1 class="rv">${s.title}</h1><p class="sec-sub rv">${s.sub || ''}</p>${s.html || ''}</div></div>`;
    } else if (s.type === 'concept') {
      el.innerHTML = header(s) + `<div class="sl-body">${s.html || ''}</div>`;
    } else {
      el.innerHTML = header(s) + `<div class="lab"><aside class="lab-side"></aside><div class="lab-main"></div></div>`;
      buildLabSide(el, s, i);
    }
    $$('.rv', el).forEach((e, k) => e.style.setProperty('--d', `${80 + k * 70}ms`));
    S.slidesBox.appendChild(el);
    S.el[i] = el;
    if (s.mount) s.mount(el, s);
    return el;
  }

  function buildLabSide(el, s, i) {
    const side = $('.lab-side', el);
    if (s.html) side.appendChild(h('div', 'lab-intro rv', s.html));
    if (s.type === 'demo') {
      if (s.steps && s.steps.length) {
        const ol = h('ol', 'steps rv');
        s.steps.forEach((st, k) => {
          const li = h('li', 'step');
          const isSim = st.cmd.startsWith('sim ');
          const formattedCode = typeof window.PythonHighlight === 'function' && !isSim
            ? window.PythonHighlight(st.cmd.trim())
            : esc(st.cmd.trim());
          li.innerHTML = `<button class="step-btn" title="Run this step">${isSim ? `<span class="step-sim">⚙ ${esc(st.simLabel || 'Simulate')}</span>` : `<code class="py-step-code">${formattedCode}</code>`}${st.say ? `<span class="say">${st.say}</span>` : ''}</button>`;
          li.querySelector('button').addEventListener('click', () => runStep(i, k));
          ol.appendChild(li);
        });
        side.appendChild(ol);
        side.appendChild(h('div', 'step-explain'));
      }
      const ctrl = h('div', 'lab-ctrl rv');
      if (s.steps && s.steps.length) ctrl.innerHTML = `<button class="btn primary" data-a="next">${ICON.play}<span>Run next</span><kbd>Enter</kbd></button>`;
      ctrl.innerHTML += `<button class="btn ghost" data-a="reset">${ICON.reset}<span>Reset</span><kbd>R</kbd></button>`;
      ctrl.addEventListener('click', (e) => { const b = e.target.closest('[data-a]'); if (!b) return; if (b.dataset.a === 'next') { if (!runNext(i)) go(i + 1); } else resetLab(i); });
      side.appendChild(ctrl);
    } else if (s.type === 'predict') {
      side.appendChild(h('div', 'question rv', s.question));
      const opts = h('div', 'options rv');
      s.options.forEach((o, k) => {
        const b = h('button', 'opt', `<span class="opt-l">${'ABCD'[k]}</span><span class="opt-t">${o}</span>`);
        b.addEventListener('click', () => { if (el.classList.contains('revealed')) return; $$('.opt', opts).forEach((x) => x.classList.remove('picked')); b.classList.add('picked'); });
        opts.appendChild(b);
      });
      side.appendChild(opts);
      const ctrl = h('div', 'lab-ctrl rv', `<button class="btn primary" data-a="reveal">${ICON.eye}<span>Reveal</span><kbd>Enter</kbd></button><button class="btn ghost" data-a="reset">${ICON.reset}<span>Reset</span></button>`);
      ctrl.addEventListener('click', (e) => { const b = e.target.closest('[data-a]'); if (!b) return; if (b.dataset.a === 'reveal') reveal(i); else { el.classList.remove('revealed'); $$('.opt', opts).forEach((x) => x.classList.remove('picked', 'right', 'wrong')); resetLab(i); } });
      side.appendChild(ctrl);
      side.appendChild(h('div', 'explain', s.explain || ''));
    } else if (s.type === 'challenge') {
      const ul = h('ul', 'tasks rv');
      s.tasks.forEach((t) => ul.appendChild(h('li', 'task', `<span class="tick">${ICON.check}</span><span>${t.text}</span>`)));
      side.appendChild(ul);
      // The solution is only available in the presentation, not on the students' exercise pages.
      const canReveal = !S.cfg.single && (s.solution || []).length > 0;
      const ctrl = h('div', 'lab-ctrl rv', `${canReveal ? `<button class="btn ghost" data-a="solution">${ICON.eye}<span>Solution</span></button>` : ''}<button class="btn ghost" data-a="reset">${ICON.reset}<span>Reset</span></button>`);
      ctrl.addEventListener('click', (e) => { const b = e.target.closest('[data-a]'); if (!b) return; if (b.dataset.a === 'solution') el.classList.toggle('show-solution'); else resetLab(i); });
      side.appendChild(ctrl);
      if (canReveal) {
        const solWrap = h('div', 'solution');
        s.solution.forEach((cmd) => {
          const card = h('div', 'sol-card');
          const bar = h('div', 'sol-bar', `<span class="sol-title"><b>Reference Solution</b></span><button class="btn-load-sol" type="button">${ICON.play}<span>Load &amp; Run</span></button>`);
          const formatted = typeof window.PythonHighlight === 'function' ? window.PythonHighlight(cmd.trim()) : esc(cmd.trim());
          const pre = h('pre', 'sol-code', `<code>${formatted}</code>`);
          bar.querySelector('.btn-load-sol').addEventListener('click', () => { const lab = ensureLab(i); lab.run(cmd); });
          pre.addEventListener('click', () => { const lab = ensureLab(i); lab.run(cmd); });
          pre.title = 'Click to load into editor and run';
          card.appendChild(bar);
          card.appendChild(pre);
          solWrap.appendChild(card);
        });
        side.appendChild(solWrap);
      }
      side.appendChild(h('div', 'done-banner', `${ICON.check}<span>All tasks done — nice work!</span>`));
    }
  }

  function ensureLab(i) {
    if (S.labs.has(i)) return S.labs.get(i);
    const s = S.cfg.slides[i], el = S.el[i];
    const lab = S.cfg.createLab($('.lab-main', el), s);
    S.labs.set(i, lab);
    lab.stepPos = 0;
    lab.reset();
    if (s.type === 'challenge') lab.onChange(() => checkTasks(i));
    if (s.type === 'demo' && lab.onCommand) lab.onCommand((cmd) => typedCommand(i, cmd));
    return lab;
  }

  // A command typed by hand that matches the next step counts as running that step.
  // Steps chained with && may also be typed one part at a time.
  const normCmd = (c) => c.trim().replace(/\s+/g, ' ').replace(/\s*;$/, '').replace(/'/g, '"').toLowerCase();
  function typedCommand(i, cmd) {
    const lab = S.labs.get(i), s = S.cfg.slides[i];
    if (!lab || lab.running || !s.steps || lab.stepPos >= s.steps.length) return;
    const step = s.steps[lab.stepPos];
    const parts = step.cmd.split(/\s*&&\s*/);
    const typed = normCmd(cmd);
    lab.partIdx = lab.partIdx || 0;
    if (typed === normCmd(step.cmd)) lab.partIdx = parts.length;
    else if (parts.length > 1 && typed === normCmd(parts[lab.partIdx] || '')) lab.partIdx++;
    else return;
    if (lab.partIdx < parts.length) return;
    lab.partIdx = 0;
    const steps = $$('.lab-side > .steps:not(.solution) .step', S.el[i]);
    steps[lab.stepPos] && steps[lab.stepPos].classList.add('done');
    const ex = $('.step-explain', S.el[i]);
    if (ex) { ex.innerHTML = step.say || ''; ex.classList.remove('swap'); void ex.offsetWidth; ex.classList.add('swap'); }
    lab.stepPos++;
    markCurrentStep(i);
  }

  function resetLab(i) {
    const lab = ensureLab(i);
    lab.reset();
    lab.stepPos = 0;
    lab.partIdx = 0;
    $$('.step', S.el[i]).forEach((x) => x.classList.remove('done', 'current'));
    const s = S.cfg.slides[i];
    if (s.type === 'challenge') { checkTasks(i); S.el[i].classList.remove('show-solution', 'all-done'); }
    markCurrentStep(i);
  }

  function markCurrentStep(i) {
    const lab = S.labs.get(i); if (!lab) return;
    const steps = $$('.lab-side > .steps:not(.solution) .step', S.el[i]);
    steps.forEach((x, k) => x.classList.toggle('current', k === lab.stepPos));
    const cur = steps[lab.stepPos];
    if (cur && lab.stepPos > 0) cur.scrollIntoView({ block: 'nearest' });
    if (lab.stepPos === 0) { const ex = $('.step-explain', S.el[i]); if (ex) ex.innerHTML = ''; }
    const btn = $('.lab-ctrl [data-a="next"] span', S.el[i]);
    if (btn) btn.textContent = steps.length && lab.stepPos >= steps.length ? 'Next slide' : 'Run next';
  }

  // Runs steps in order: clicking step k first runs every earlier step that hasn't run yet.
  async function runStep(i, k) {
    const lab = ensureLab(i), s = S.cfg.slides[i];
    if (lab.running || k < lab.stepPos) return;
    lab.running = true;
    const steps = $$('.lab-side > .steps:not(.solution) .step', S.el[i]);
    const ex = $('.step-explain', S.el[i]);
    for (let j = lab.stepPos; j <= k; j++) {
      steps.forEach((x, n) => x.classList.toggle('current', n === j));
      steps[j] && steps[j].classList.add('running');
      if (ex) { ex.innerHTML = s.steps[j].say || ''; ex.classList.remove('swap'); void ex.offsetWidth; ex.classList.add('swap'); }
      await lab.run(s.steps[j].cmd);
      steps[j] && steps[j].classList.remove('running');
      steps[j] && steps[j].classList.add('done');
      lab.stepPos = j + 1;
    }
    lab.running = false;
    markCurrentStep(i);
  }

  function runNext(i) {
    const lab = ensureLab(i), s = S.cfg.slides[i];
    if (!s.steps || lab.stepPos >= s.steps.length) return false;
    runStep(i, lab.stepPos);
    return true;
  }

  async function reveal(i) {
    const el = S.el[i], s = S.cfg.slides[i], lab = ensureLab(i);
    if (el.classList.contains('revealed') || lab.running) return;
    lab.running = true;
    for (const st of s.steps || []) await lab.run(st.cmd);
    lab.running = false;
    el.classList.add('revealed');
    $$('.opt', el).forEach((o, k) => { if (k === s.answer) o.classList.add('right'); else if (o.classList.contains('picked')) o.classList.add('wrong'); });
  }

  function checkTasks(i) {
    const s = S.cfg.slides[i], lab = S.labs.get(i), el = S.el[i];
    if (!lab) return;
    let all = true;
    $$('.task', el).forEach((li, k) => {
      let ok = false;
      try { ok = !!s.tasks[k].check(lab.sim); } catch (e) { ok = false; }
      if (ok && !li.classList.contains('ok')) li.classList.add('just');
      li.classList.toggle('ok', ok);
      if (!ok) all = false;
    });
    el.classList.toggle('all-done', all);
  }

  // ---------------------------------------------------------------- navigation
  function go(n, opts = {}) {
    if (S.stage) hideExercise();
    const slides = S.cfg.slides;
    n = Math.min(Math.max(n, 0), slides.length - 1);
    for (let k = n - 1; k <= n + 1; k++) if (k >= 0 && k < slides.length && !S.el[k]) buildSlide(k);
    const el = S.el[n];
    S.el.forEach((e, k) => {
      if (!e) return;
      e.classList.toggle('active', k === n);
      e.classList.toggle('past', k < n);
      e.classList.toggle('future', k > n);
    });
    if (opts.instant) { el.classList.add('instant'); requestAnimationFrame(() => requestAnimationFrame(() => el.classList.remove('instant'))); }
    S.i = n;
    const want = '#' + (n + 1);
    if (!S.cfg.single && location.hash !== want) history.replaceState(null, '', want);
    if (['demo', 'predict', 'challenge'].includes(slides[n].type)) {
      const fresh = !S.labs.has(n);
      const lab = ensureLab(n);
      if (fresh) markCurrentStep(n); else lab.refresh && lab.refresh();
    }
    document.activeElement && document.activeElement.blur && document.activeElement.blur();
    updateHud();
  }

  function next() {
    go(S.i + 1);
  }
  function prev() { go(S.i - 1); }

  function updateHud() {
    const s = S.cfg.slides[S.i];
    $('.hud-section', S.hud).textContent = s.section || '';
    $('.hud-count', S.hud).textContent = `${S.i + 1} / ${S.cfg.slides.length}`;
    for (const sec of S.sections) {
      const fill = sec.seg.querySelector('i');
      const p = S.i > sec.to ? 1 : S.i < sec.from ? 0 : (S.i - sec.from + 1) / (sec.to - sec.from + 1);
      fill.style.transform = `scaleX(${p})`;
      sec.seg.classList.toggle('cur', S.i >= sec.from && S.i <= sec.to);
    }
    $$('.ov-item', S.overview).forEach((b) => b.classList.toggle('cur', +b.dataset.i === S.i));
  }

  function toggleOverview(force) {
    const on = force === undefined ? !S.stage.classList.contains('overview-open') : force;
    S.stage.classList.toggle('overview-open', on);
  }
  function toggleTheme() {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    store.set('deck.theme', root.dataset.theme);
    S.labs.forEach((l) => l.refresh && l.refresh());
  }
  function toggleFull() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen && document.documentElement.requestFullscreen().catch(() => {});
  }

  function onKey(e) {
    if (e.target.closest && e.target.closest('input, textarea, [contenteditable]')) return;
    const k = e.key;

    // Zoom shortcuts (allow with Ctrl/Cmd or bare keys)
    if ((e.ctrlKey || e.metaKey) && (k === '=' || k === '+')) { e.preventDefault(); setZoom(S.zoom + 0.15); return; }
    if ((e.ctrlKey || e.metaKey) && (k === '-' || k === '_')) { e.preventDefault(); setZoom(S.zoom - 0.15); return; }
    if ((e.ctrlKey || e.metaKey) && k === '0') { e.preventDefault(); setZoom(1.0); return; }

    if (e.metaKey || e.ctrlKey || e.altKey) return;

    if (k === '+' || k === '=') { e.preventDefault(); setZoom(S.zoom + 0.15); return; }
    if (k === '-' || k === '_') { e.preventDefault(); setZoom(S.zoom - 0.15); return; }
    if (k === '0') { e.preventDefault(); setZoom(1.0); return; }
    if (k === 'z' || k === 'Z') { e.preventDefault(); cycleTextSize(); return; }

    const s = S.cfg.slides[S.i];
    if (S.stage.classList.contains('ex-big-open')) {
      if (k === 'Escape' || k === 'q' || k === 'Q' || k === 'Enter' || k === ' ') { hideExercise(); e.preventDefault(); }
      return;
    }
    if (S.stage.classList.contains('overview-open')) {
      if (k === 'Escape' || k === 'o' || k === 'O') { toggleOverview(false); e.preventDefault(); }
      return;
    }
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ') { e.preventDefault(); next(); }
    else if (k === 'ArrowLeft' || k === 'PageUp') { e.preventDefault(); prev(); }
    else if (k === 'Home') go(0);
    else if (k === 'End') go(S.cfg.slides.length - 1);
    else if (k === 'Enter') {
      e.preventDefault();
      if (s.type === 'demo') { if (!runNext(S.i)) next(); }
      else if (s.type === 'predict') { if (S.el[S.i].classList.contains('revealed')) next(); else reveal(S.i); }
      else next();
    }
    else if (k === 'o' || k === 'O') toggleOverview();
    else if (k === 'q' || k === 'Q') showExercise(S.el[S.i]);
    else if (k === 'd' || k === 'D') toggleTheme();
    else if (k === 'f' || k === 'F') toggleFull();
    else if ((k === 'r' || k === 'R') && S.labs.has(S.i)) resetLab(S.i);
  }

  // ---------------------------------------------------------------- shared helpers for slide content
  // Address of the deck folder (siteUrl overrides the address the deck is opened from).
  const deckBase = (siteUrl) => (siteUrl || location.href).split('#')[0].split('?')[0].replace(/index\.html$/, '').replace(/\/?$/, '/');

  // mount hook for exercise slides: shows the link that opens this exercise alone (x/?<n>).
  const linkHtml = (url) => esc(url.replace(/^https?:\/\//, '')).replace(/\//g, '/<wbr>');
  const qrSvg = (url) => { const qr = qrcode(0, 'L'); qr.addData(url); qr.make(); return qr.createSvgTag({ cellSize: 4, margin: 1, scalable: true }); };

  // mount hook for exercise slides: shows the link that opens this exercise alone (x/?<n>).
  // Clicking the QR code (or pressing Q) shows it full screen for the classroom.
  function exerciseLink(siteUrl) {
    return (el, s) => {
      if (document.body.classList.contains('single')) return;
      const url = deckBase(siteUrl) + 'x/?' + s.exercise;
      const box = h('div', 'ex-link', `<a class="ex-text" href="${esc(url)}" target="_blank" rel="noopener"><span>Do it on your laptop</span><b>${linkHtml(url)}</b></a>`);
      if (typeof qrcode === 'function') {
        const btn = h('button', 'ex-qr', qrSvg(url));
        btn.title = 'Show full screen (Q)';
        btn.setAttribute('aria-label', 'Show the exercise link full screen');
        btn.addEventListener('click', () => showExercise(el));
        box.appendChild(btn);
      }
      box.dataset.url = url;
      box.dataset.title = `Exercise ${s.exercise}: ${s.title.replace(/<[^>]+>/g, '')}`;
      $('.lab-side', el).prepend(box);
    };
  }

  function showExercise(el) {
    const box = el && $('.ex-link', el);
    if (!box || typeof qrcode !== 'function') return;
    S.exBig.innerHTML = `<div class="ex-big-card"><div class="kicker">${esc(box.dataset.title)}</div><div class="ex-big-qr">${qrSvg(box.dataset.url)}</div><div class="ex-big-url">${linkHtml(box.dataset.url)}</div><div class="ex-big-hint">Open this on your laptop · click or press Esc to close</div></div>`;
    S.stage.classList.add('ex-big-open');
  }
  function hideExercise() { S.stage.classList.remove('ex-big-open'); }

  // mount hook for the closing slide: renders a QR code (needs the qrcode-generator script) for the deck address.
  function qrMount(siteUrl) {
    return (el) => {
      const url = deckBase(siteUrl);
      $('.qr-url', el).textContent = url.replace(/^https?:\/\//, '');
      const box = $('.qr', el);
      if (typeof qrcode === 'function') {
        const qr = qrcode(0, 'M'); qr.addData(url); qr.make();
        box.innerHTML = qr.createSvgTag({ cellSize: 8, margin: 2, scalable: true });
      } else box.textContent = 'QR code needs an internet connection';
    };
  }

  window.Deck = { init, go, ICON, util: { exerciseLink, qrMount } };
})();
