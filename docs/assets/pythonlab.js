/* ==========================================================================
   CSE 101 — Interactive Python Lab with Skulpt & Memory Visualizer
   ========================================================================== */

(function (global) {
  'use strict';

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  // Python Syntax Highlighter
  const KEYWORDS = new Set(('def return if elif else for while in break continue and or not is True False None import from as pass lambda try except finally raise with global nonlocal class yield').split(' '));
  const BUILTINS = new Set(('print len range int float str bool list dict tuple set type sum min max abs round input sorted enumerate zip map filter any all id').split(' '));

  function highlightPython(code) {
    if (!code) return '';
    // Match: strings (triple, double, single), comments (#...), numbers, words, operators
    const tokenRegex = /("""[\s\S]*?"""|'''[\s\S]*?'''|f?"(?:\\.|[^"\\])*"|f?'(?:\\.|[^'\\])*')|(#.*)|(\b\d+(?:\.\d+)?\b)|(\b[A-Za-z_][A-Za-z0-9_]*\b)|([+\-*/%=<>!&|^~:]+)|([\s\S])/g;
    return code.replace(tokenRegex, (m, str, com, num, word, op, other) => {
      if (str) return `<span class="h-str">${esc(str)}</span>`;
      if (com) return `<span class="h-com">${esc(com)}</span>`;
      if (num) return `<span class="h-num">${esc(num)}</span>`;
      if (word) {
        if (word === 'True' || word === 'False' || word === 'None') return `<span class="h-bool">${esc(word)}</span>`;
        if (KEYWORDS.has(word)) return `<span class="h-kw">${esc(word)}</span>`;
        if (BUILTINS.has(word)) return `<span class="h-fn">${esc(word)}</span>`;
        return esc(word);
      }
      if (op) return `<span class="h-op">${esc(op)}</span>`;
      return esc(other || '');
    });
  }

  // Convert Skulpt Object to JS Native
  function skulptToJs(val) {
    if (val === null || val === undefined) return null;
    if (typeof val === 'number' || typeof val === 'string' || typeof val === 'boolean') return val;
    const Sk = global.Sk;
    if (Sk && Sk.builtin) {
      if (val instanceof Sk.builtin.int_ || val instanceof Sk.builtin.float_ || val instanceof Sk.builtin.str || val instanceof Sk.builtin.bool) {
        return val.v;
      }
      if (val instanceof Sk.builtin.list || val instanceof Sk.builtin.tuple || (val.v && Array.isArray(val.v))) {
        return (val.v || []).map(skulptToJs);
      }
      if (val instanceof Sk.builtin.none || val.tp$name === 'NoneType') return null;
    }
    if (Array.isArray(val)) return val.map(skulptToJs);
    if (val.v !== undefined && Array.isArray(val.v)) return val.v.map(skulptToJs);
    return val.v !== undefined ? val.v : String(val);
  }

  function jsToSk(v) {
    const Sk = global.Sk;
    if (!Sk || !Sk.builtin) return v;
    if (typeof v === 'number') return Number.isInteger(v) ? new Sk.builtin.int_(v) : new Sk.builtin.float_(v);
    if (typeof v === 'boolean') return new Sk.builtin.bool(v);
    if (typeof v === 'string') return new Sk.builtin.str(v);
    if (Array.isArray(v)) return new Sk.builtin.list(v.map(jsToSk));
    if (v === null || v === undefined) return Sk.builtin.none.none$;
    return new Sk.builtin.str(String(v));
  }

  function createPythonLab(host, slide) {
    const lab = {
      results: [],
      sim: { vars: {}, output: '', code: '', error: null },
    };

    let busy = false;
    let sessionHistory = [];
    const listeners = [];
    const cmdListeners = [];

    host.innerHTML = `
      <div class="python-lab">
        <div class="py-left">
          <div class="py-editor">
            <div class="py-bar">
              <span class="py-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z"/></svg>
                Python 3.12
              </span>
              <span class="py-hint">Ctrl + Enter to run</span>
              <button class="py-run" title="Run code (Ctrl + Enter)">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                Run
              </button>
            </div>
            <div class="py-code-wrap">
              <pre class="py-hl" aria-hidden="true"></pre>
              <textarea class="py-input" spellcheck="false" autocomplete="off" autocapitalize="off" autocorrect="off" placeholder="# Type Python code here..."></textarea>
            </div>
          </div>
          <div class="py-console">
            <div class="py-chead">
              <b>Console Output</b>
              <span class="py-meta"></span>
            </div>
            <div class="py-cbody"></div>
          </div>
        </div>
        <div class="py-right">
          <div class="py-panel">
            <div class="py-panel-head">
              <b>Variables &amp; State</b>
              <small class="py-var-count">0 variables</small>
            </div>
            <div class="py-vars-body">
              <table class="py-table">
                <thead><tr><th>Name</th><th>Type</th><th>Value</th></tr></thead>
                <tbody><tr><td colspan="3" style="color:var(--muted);font-style:italic">No variables defined</td></tr></tbody>
              </table>
            </div>
          </div>
          <div class="py-panel py-seq-panel" style="display:none">
            <div class="py-panel-head">
              <b>Sequence Inspector (Indices)</b>
              <small>0-based &amp; negative indexing</small>
            </div>
            <div class="seq-box-container"></div>
          </div>
        </div>
      </div>
    `;

    const editor = host.querySelector('.py-editor');
    const input = host.querySelector('.py-input');
    const hl = host.querySelector('.py-hl');
    const runBtn = host.querySelector('.py-run');
    const consoleBody = host.querySelector('.py-cbody');
    const meta = host.querySelector('.py-meta');
    const varCount = host.querySelector('.py-var-count');
    const varTableBody = host.querySelector('.py-table tbody');
    const seqPanel = host.querySelector('.py-seq-panel');
    const seqContainer = host.querySelector('.seq-box-container');

    function syncHl() {
      hl.innerHTML = highlightPython(input.value) + '\n';
      hl.scrollTop = input.scrollTop;
      hl.scrollLeft = input.scrollLeft;
    }

    input.addEventListener('input', syncHl);
    input.addEventListener('scroll', () => {
      hl.scrollTop = input.scrollTop;
      hl.scrollLeft = input.scrollLeft;
    });

    input.addEventListener('keydown', (e) => {
      e.stopPropagation();
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        execute(input.value);
      } else if (e.key === 'Tab') {
        e.preventDefault();
        const start = input.selectionStart;
        const end = input.selectionEnd;
        input.value = input.value.substring(0, start) + '    ' + input.value.substring(end);
        input.selectionStart = input.selectionEnd = start + 4;
        syncHl();
      }
    });

    runBtn.addEventListener('click', () => execute(input.value));

    // Ensure Skulpt standard files reader
    function builtinRead(x) {
      if (global.Sk && global.Sk.builtinFiles && global.Sk.builtinFiles["files"] && global.Sk.builtinFiles["files"][x]) {
        return global.Sk.builtinFiles["files"][x];
      }
      throw new Error("File not found: " + x);
    }

    function renderVariables(varsMap) {
      const keys = Object.keys(varsMap);
      varCount.textContent = `${keys.length} variable${keys.length === 1 ? '' : 's'}`;
      if (!keys.length) {
        varTableBody.innerHTML = `<tr><td colspan="3" style="color:var(--muted);font-style:italic">No variables defined</td></tr>`;
        seqPanel.style.display = 'none';
        return;
      }

      let rowsHtml = '';
      let sequences = [];

      for (const k of keys) {
        const item = varsMap[k];
        const valStr = typeof item.repr === 'string' ? item.repr : JSON.stringify(item.val);
        rowsHtml += `
          <tr class="${item.updated ? 'updated' : ''}">
            <td><strong>${esc(k)}</strong></td>
            <td><span class="py-type ${esc(item.type)}">${esc(item.type)}</span></td>
            <td><code>${esc(valStr)}</code></td>
          </tr>
        `;

        if ((item.type === 'str' || item.type === 'list') && item.val != null && item.val.length > 0 && item.val.length <= 15) {
          sequences.push({ name: k, type: item.type, items: Array.from(item.val) });
        }
      }
      varTableBody.innerHTML = rowsHtml;

      // Render Sequence Inspector
      if (sequences.length > 0) {
        seqPanel.style.display = 'flex';
        let seqHtml = '';
        sequences.forEach((sq) => {
          seqHtml += `<div class="seq-item-wrap">`;
          seqHtml += `<div class="seq-title">${esc(sq.name)} (${esc(sq.type)}, len=${sq.items.length})</div>`;
          seqHtml += `<div class="seq-row">`;
          const len = sq.items.length;
          sq.items.forEach((elem, idx) => {
            const negIdx = idx - len;
            const displayElem = typeof elem === 'string' ? `'${elem}'` : String(elem);
            seqHtml += `
              <div class="seq-cell">
                <span class="seq-idx-top">${idx}</span>
                <span class="seq-val">${esc(displayElem)}</span>
                <span class="seq-idx-bot">${negIdx}</span>
              </div>
            `;
          });
          seqHtml += `</div></div>`;
        });
        seqContainer.innerHTML = seqHtml;
      } else {
        seqPanel.style.display = 'none';
      }
    }

    async function execute(code) {
      if (!code.trim()) return;
      meta.textContent = 'Running...';
      meta.className = 'py-meta';
      consoleBody.innerHTML = '';

      let stdout = '';
      const Sk = global.Sk;

      if (!Sk) {
        consoleBody.innerHTML = `<div class="py-line-err">Python interpreter loading... please wait.</div>`;
        return;
      }

      Sk.configure({
        output: (text) => {
          stdout += text;
        },
        read: builtinRead,
        execLimit: 5000,
        __future__: Sk.python3
      });

      const t0 = performance.now();
      try {
        await Sk.misceval.asyncToPromise(() => {
          return Sk.importMainWithBody("<stdin>", false, code, true);
        });
        const elapsed = Math.round(performance.now() - t0);
        meta.textContent = `Completed in ${elapsed}ms`;

        consoleBody.innerHTML = stdout ? `<div class="py-line-out">${esc(stdout)}</div>` : `<div style="color:var(--muted);font-style:italic">Program finished with no output.</div>`;

        // Extract variables
        const currentVars = {};
        const jsVars = {};
        for (const k of Object.keys(Sk.globals)) {
          if (!k.startsWith('__')) {
            const skVal = Sk.globals[k];
            const tp = skVal.tp$name || typeof skVal;
            const jsVal = skulptToJs(skVal);
            jsVars[k] = jsVal;
            let repr = '';
            try {
              const r = Sk.misceval.objectRepr(skVal);
              repr = r ? (r.v !== undefined ? r.v : String(r)) : String(jsVal);
            } catch (e) {
              repr = String(jsVal);
            }
            currentVars[k] = {
              type: tp,
              val: jsVal,
              repr: repr,
              skVal: skVal,
              updated: true
            };
          }
        }

        lab.sim.vars = jsVars;
        lab.sim.output = stdout;
        lab.sim.code = code;
        lab.sim.error = null;
        lab.sim.hasFunction = (name) => typeof Sk.globals[name] === 'object';
        lab.sim.call = (name, ...args) => {
          const fn = Sk.globals[name];
          if (!fn) throw new Error(`Function ${name} not found`);
          const skArgs = args.map(jsToSk);
          const res = Sk.misceval.callsimOrSuspend(fn, ...skArgs);
          return skulptToJs(res);
        };

        renderVariables(currentVars);
        lab.results.push({ code, output: stdout, vars: jsVars });

      } catch (err) {
        const elapsed = Math.round(performance.now() - t0);
        meta.textContent = `Error (${elapsed}ms)`;
        meta.className = 'py-meta err';
        const errMsg = String(err.toString ? err.toString() : err);
        consoleBody.innerHTML = `<div class="py-line-err">${esc(errMsg)}</div>`;
        lab.sim.error = errMsg;
        lab.sim.output = stdout;
      }

      for (const fn of listeners) fn();
      for (const fn of cmdListeners) fn(code);
    }

    Object.assign(lab, {
      reset() {
        sessionHistory = [];
        input.value = slide.prefill || '';
        syncHl();
        consoleBody.innerHTML = '';
        meta.textContent = '';
        lab.sim = { vars: {}, output: '', code: input.value, error: null };
        lab.results = [];
        renderVariables({});
        if (slide.setup && slide.setup.length) {
          execute(slide.setup.join('\n'));
        }
      },
      refresh() {
        syncHl();
      },
      onChange(fn) {
        listeners.push(fn);
      },
      onCommand(fn) {
        cmdListeners.push(fn);
      },
      async run(code) {
        while (busy) await sleep(50);
        busy = true;

        sessionHistory.push(code);
        const accumulated = sessionHistory.join('\n\n');
        input.value = accumulated;
        syncHl();
        input.scrollTop = input.scrollHeight;

        await sleep(120);
        await execute(accumulated);
        busy = false;
        await sleep(180);
      }
    });

    return lab;
  }

  global.createPythonLab = createPythonLab;
  global.PythonHighlight = highlightPython;
})(window);
