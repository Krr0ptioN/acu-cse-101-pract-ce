/* CSE 101 · Python Fundamentals — Comprehensive Interactive Lecture Deck
 * Covering: The Way of the Program -> Arithmetic -> Variables -> Functions ->
 *           Conditionals -> Iterations -> Strings -> Lists -> Synthesis
 */
(function (global) {
  'use strict';

  const SITE_URL = '';
  const getDeck = () => global.Deck || (typeof window !== 'undefined' ? window.Deck : null);
  const exerciseLink = (el, s) => {
    const D = getDeck();
    if (D && D.util && D.util.exerciseLink) D.util.exerciseLink(SITE_URL)(el, s);
  };
  const qrMount = (el) => {
    const D = getDeck();
    if (D && D.util && D.util.qrMount) D.util.qrMount(SITE_URL)(el);
  };
  const PythonHighlight = (code) => {
    const fn = global.PythonHighlight || (typeof window !== 'undefined' ? window.PythonHighlight : null);
    return fn ? fn(code) : code;
  };

  const SEC = {
    intro: 'Welcome',
    p1: 'Part 1 · The Program & Arithmetic',
    p2: 'Part 2 · Variables & Expressions',
    p3: 'Part 3 · Functions & Modularity',
    p4: 'Part 4 · Conditionals & Logic',
    p5: 'Part 5 · Iteration & Loops',
    p6: 'Part 6 · Strings & Text',
    p7: 'Part 7 · Lists & Collections',
    p8: 'Part 8 · Synthesis & Wrap-up',
  };

  const I = {
    py: '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    gear: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    code: '<svg viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><polyline points="8 6 2 12 8 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    check: '<svg viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    bug: '<svg viewBox="0 0 24 24"><circle cx="12" cy="14" r="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 9V5M9 6l6 6M15 6l-6 6M6 13H2M22 13h-4M6 17l-3 2M21 19l-3-2M6 10l-3-2M21 8l-3 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    list: '<svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6" stroke="currentColor" stroke-width="2"/><line x1="8" y1="12" x2="21" y2="12" stroke="currentColor" stroke-width="2"/><line x1="8" y1="18" x2="21" y2="18" stroke="currentColor" stroke-width="2"/><circle cx="4" cy="6" r="1.5" fill="currentColor"/><circle cx="4" cy="12" r="1.5" fill="currentColor"/><circle cx="4" cy="18" r="1.5" fill="currentColor"/></svg>',
    box: '<svg viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" fill="none" stroke="currentColor" stroke-width="2"/><polyline points="3.27 6.96 12 12.01 20.73 6.96" fill="none" stroke="currentColor" stroke-width="2"/><line x1="12" y1="22.08" x2="12" y2="12" stroke="currentColor" stroke-width="2"/></svg>',
    repeat: '<svg viewBox="0 0 24 24"><path d="M17 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 11V9a4 4 0 014-4h14M7 23l-4-4 4-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 13v2a4 4 0 01-4 4H3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  };

  const slides = [
    // =========================================================================
    // WELCOME & INTRO
    // =========================================================================
    {
      type: 'title',
      section: SEC.intro,
      title: 'Python Fundamentals',
      html: `<div class="title-wrap">
        <div>
          <div class="kicker rv">ACU CSE 101 · Introduction to Programming · Fall 2026</div>
          <h1 class="rv">Python<br><span>Fundamentals</span></h1>
          <p class="lead rv">From the way of the program to iterations, strings, and lists. Every snippet today executes directly in a real Python 3 environment in your browser.</p>
          <div class="meta rv">
            <span class="tag accent">Live Python 3</span>
            <span class="tag">Memory Inspector</span>
            <span class="tag">Sequence Visualizer</span>
            <span class="tag">Think Python</span>
          </div>
        </div>
        <div class="title-art rv">
          <pre class="codeblock" style="font-size:16px;line-height:1.5">${PythonHighlight(`def summarize_scores(scores):
    """Compute average and top performers."""
    valid = [s for s in scores if s >= 0]
    avg = sum(valid) / len(valid)
    top = [s for s in valid if s >= 85]
    return f"Avg: {avg:.1f}, Honors: {len(top)}"

print(summarize_scores([95, 78, 88, 92, 60]))`)}</pre>
          <div style="margin-top:14px;padding:12px 16px;background:var(--surface);border:1px solid var(--line);border-radius:12px;font-family:var(--mono);font-size:14px;color:var(--green)">
            &gt;&gt;&gt; Avg: 82.6, Honors: 3
          </div>
        </div>
      </div>`,
    },

    {
      type: 'concept',
      section: SEC.intro,
      title: 'Course roadmap',
      navTitle: 'Roadmap',
      html: '<!--agenda-->',
    },

    {
      type: 'concept',
      section: SEC.intro,
      title: 'What is a program?',
      html: `<p class="lead">A program is a sequence of precise instructions that tells a computer how to perform a computation.</p>
      <div class="diagram-box">
        <div class="flow-step"><b>Input</b><br><small>keyboard, files, sensors</small></div>
        <div class="flow-arrow">&rarr;</div>
        <div class="flow-step active"><b>Processing</b><br><small>math, logic, repetition</small></div>
        <div class="flow-arrow">&rarr;</div>
        <div class="flow-step"><b>Output</b><br><small>screen, files, network</small></div>
      </div>
      <div class="grid2" style="margin-top:24px">
        <div class="card good">
          <h3>${I.gear} The Core Building Blocks</h3>
          <ul class="points tight">
            <li><b>Input / Output:</b> Get data and display results</li>
            <li><b>Math:</b> Basic arithmetic operations (+, -, *, /)</li>
            <li><b>Conditionals:</b> Make decisions based on conditions (if/else)</li>
            <li><b>Repetition:</b> Repeat instructions repeatedly (loops)</li>
          </ul>
        </div>
        <div class="card">
          <h3>${I.code} Why Python in CSE 101?</h3>
          <ul class="points tight">
            <li><b>High-level:</b> Close to human thought and English grammar</li>
            <li><b>Interpreted:</b> Runs line-by-line without slow compilation cycles</li>
            <li><b>Batteries included:</b> Rich standard library for math, strings, and data</li>
            <li><b>Industry standard:</b> Dominates Artificial Intelligence, Data Science, and Web</li>
          </ul>
        </div>
      </div>`,
    },

    // =========================================================================
    // PART 1 — THE WAY OF THE PROGRAM & ARITHMETIC
    // =========================================================================
    {
      type: 'section',
      section: SEC.p1,
      num: 1,
      title: 'The Way of the Program & Arithmetic',
      navTitle: 'Part 1 · The Program & Math',
      sub: 'Values, data types, arithmetic operators, precedence, and debugging errors.',
      html: '<div class="sec-goals rv"><code>int</code><code>float</code><code>str</code><code>+ - * / // % **</code><code>PEMDAS</code></div>',
    },

    {
      type: 'concept',
      section: SEC.p1,
      title: 'Values and data types',
      html: `<p class="lead">Every piece of data in Python has a specific <b>type</b> that determines what operations can be performed on it.</p>
      <div class="grid4" style="margin-top:14px">
        <div class="card">
          <h3><span class="py-type int">int</span> Integer</h3>
          <p>Whole numbers without fractional parts (positive, negative, or zero).</p>
          <pre class="codeblock">${PythonHighlight(`age = 19
count = -5
print(type(42))`)}</pre>
        </div>
        <div class="card">
          <h3><span class="py-type float">float</span> Float</h3>
          <p>Numbers with fractional components or decimal points.</p>
          <pre class="codeblock">${PythonHighlight(`pi = 3.14159
ratio = 0.5
print(type(3.14))`)}</pre>
        </div>
        <div class="card">
          <h3><span class="py-type str">str</span> String</h3>
          <p>Sequences of text characters enclosed in quotes.</p>
          <pre class="codeblock">${PythonHighlight(`name = "Ada"
greet = 'Hi'
digits = "123"`)}</pre>
        </div>
        <div class="card">
          <h3><span class="py-type bool">bool</span> Boolean</h3>
          <p>Logical truth values: only two possibilities, True or False.</p>
          <pre class="codeblock">${PythonHighlight(`is_ok = True
passed = False
print(type(True))`)}</pre>
        </div>
      </div>
      <div class="callout" style="margin-top:16px">
        <b>Use <code>type(x)</code></b> to inspect what type Python assigned to any value or variable.
      </div>`,
    },

    {
      type: 'demo',
      section: SEC.p1,
      title: 'Arithmetic operators in action',
      html: `<p>Watch how Python evaluates division, integer division, modulo, and exponents.</p>`,
      steps: [
        { cmd: '# Addition: evaluates sum of two numbers\nprint(40 + 2)', say: 'Basic addition: produces an integer <code>42</code>.' },
        { cmd: '# Float division: / always returns a float in Python 3\nprint(7 / 2, type(7 / 2))', say: 'Standard division <code>/</code> ALWAYS returns a <b>float</b> in Python 3 (here <code>3.5</code>).' },
        { cmd: '# Floor division: // discards fractional part and rounds down\nprint(7 // 2, type(7 // 2))', say: 'Floor division <code>//</code> truncates the fraction and keeps only the whole quotient (<code>3</code>).' },
        { cmd: '# Modulus: % returns the remainder of integer division\nprint(17 % 5)', say: 'Modulus <code>%</code> gives the remainder: 17 divided by 5 is 3 with remainder <b>2</b>.' },
        { cmd: '# Exponentiation: ** raises base to the exponent\nprint(2 ** 8)', say: 'Exponentiation <code>**</code> computes 2 to the power of 8 (<code>256</code>).' },
      ],
    },

    {
      type: 'concept',
      section: SEC.p1,
      title: 'Three kinds of programming errors',
      html: `<p class="lead">Understanding error categories helps you diagnose and fix bugs systematically.</p>
      <div class="grid3" style="margin-top:14px">
        <div class="card bad">
          <h3>${I.bug} Syntax Errors <span class="tag red">grammar</span></h3>
          <p>Violations of Python grammar. Python catches these before running any code!</p>
          <pre class="codeblock">${PythonHighlight(`print("Hello"  # missing )
7 = x          # invalid target`)}</pre>
        </div>
        <div class="card bad">
          <h3>${I.gear} Runtime Errors <span class="tag amber">exceptions</span></h3>
          <p>Syntax is legal, but an illegal operation crashes the running program.</p>
          <pre class="codeblock">${PythonHighlight(`print(10 / 0)      # ZeroDivision
print(unknown_var) # NameError`)}</pre>
        </div>
        <div class="card good" style="border-color:color-mix(in srgb, var(--blue) 45%, var(--line))">
          <h3>${I.code} Semantic Errors <span class="tag blue">logic bugs</span></h3>
          <p>Runs cleanly without crashing, but computes the wrong answer.</p>
          <pre class="codeblock">${PythonHighlight(`# Precedence bug:
bad = a + b / 2    # Bug!
good = (a + b) / 2 # Correct`)}</pre>
        </div>
      </div>
      <div class="callout blue" style="margin-top:16px">
        <b>Debugging Strategy:</b> Fix Syntax errors first &rarr; test inputs to prevent Runtime exceptions &rarr; verify results against unit tests.
      </div>`,
    },

    {
      type: 'predict',
      section: SEC.p1,
      title: 'Floor division and modulus',
      html: `<p>What will Python print when this expression is evaluated?</p>
      <pre class="codeblock" style="font-size:18px">${PythonHighlight(`res = (19 // 4) + (19 % 4)
print(res)`)}</pre>`,
      options: ['4.75', '7', '8', '3'],
      answer: 1,
      explain: '19 // 4 is 4 (the quotient), and 19 % 4 is 3 (the remainder). 4 + 3 = <b>7</b>.',
      steps: [
        { cmd: '# Calculate quotient and remainder\nq = 19 // 4  # 4\nr = 19 % 4   # 3\nprint("Quotient:", q, "Remainder:", r)\nprint("Result:", q + r)' },
      ],
    },

    {
      type: 'challenge',
      exercise: 1,
      mount: exerciseLink,
      section: SEC.p1,
      title: 'Calculate running pace',
      html: `<p>A runner completes a <b>10-kilometer</b> run in <b>42 minutes and 42 seconds</b>.</p>
      <p>Write Python calculations to define the required variables.</p>`,
      prefill: `# Total time: 42 minutes and 42 seconds
# 1 mile = 1.61 kilometers

total_seconds = 
total_minutes = 
miles = 
pace_minutes_per_mile = 
`,
      tasks: [
        {
          text: 'Define <code>total_seconds</code>: total duration in seconds (42 * 60 + 42 = 2562).',
          check: (sim) => sim.vars.total_seconds === 2562,
        },
        {
          text: 'Define <code>miles</code>: 10 kilometers converted to miles (10 / 1.61).',
          check: (sim) => typeof sim.vars.miles === 'number' && Math.abs(sim.vars.miles - (10 / 1.61)) < 0.01,
        },
        {
          text: 'Define <code>pace_minutes_per_mile</code>: minutes per mile (total_minutes / miles).',
          check: (sim) => typeof sim.vars.pace_minutes_per_mile === 'number' && sim.vars.pace_minutes_per_mile > 6 && sim.vars.pace_minutes_per_mile < 8,
        },
      ],
      solution: [
        '# 1. Total elapsed time in seconds and minutes\ntotal_seconds = 42 * 60 + 42\ntotal_minutes = total_seconds / 60\n\n# 2. Convert 10 km distance to miles (1.61 km per mile)\nmiles = 10 / 1.61\n\n# 3. Calculate running pace in minutes per mile\npace_minutes_per_mile = total_minutes / miles\nprint(f"Pace: {pace_minutes_per_mile:.2f} min/mile")',
      ],
    },

    // =========================================================================
    // PART 2 — VARIABLES, EXPRESSIONS & STATEMENTS
    // =========================================================================
    {
      type: 'section',
      section: SEC.p2,
      num: 2,
      title: 'Variables, Expressions & Statements',
      navTitle: 'Part 2 · Variables & State',
      sub: 'Variables as labels, assignment statements, reassignment, multiple assignment, and type casting.',
      html: '<div class="sec-goals rv"><code>=</code><code>snake_case</code><code>a, b = b, a</code><code>int()</code><code>str()</code></div>',
    },

    {
      type: 'concept',
      section: SEC.p2,
      title: 'Variables are name tags in memory',
      html: `<p class="lead">An assignment statement <code>variable = value</code> attaches a name tag to a value stored in memory.</p>
      <div class="diagram-box">
        <div class="mem-box"><b>name</b>: <code>message</code></div>
        <div class="flow-arrow">&rarr; points to &rarr;</div>
        <div class="flow-step"><code>"Hello CSE 101"</code> <span class="py-type str">str</span></div>
      </div>
      <div class="grid2" style="margin-top:20px">
        <div class="card good">
          <h3>${I.check} Legal Python Variable Names</h3>
          <ul class="points tight">
            <li>Can contain letters, numbers, and underscores <code>_</code></li>
            <li>Must start with a letter or underscore: <code>student_score</code>, <code>_count</code></li>
            <li><b>PEP 8 Convention:</b> Use <code>snake_case</code> for variables and functions</li>
          </ul>
        </div>
        <div class="card bad">
          <h3>${I.bug} Illegal Variable Names</h3>
          <ul class="points tight">
            <li>Cannot start with a digit: <code>2nd_score</code> &rarr; <i>SyntaxError</i></li>
            <li>Cannot contain spaces or hyphens: <code>user-name</code>, <code>my score</code></li>
            <li>Cannot use reserved Python keywords: <code>for</code>, <code>class</code>, <code>def</code></li>
          </ul>
        </div>
      </div>`,
    },

    {
      type: 'demo',
      section: SEC.p2,
      title: 'Reassignment & multiple assignment',
      html: `<p>Watch the <b>Variables &amp; State</b> table on the right update as each line runs!</p>`,
      steps: [
        { cmd: '# Initial variable assignment\na = 10\nb = 20\nprint("Before:", a, b)', say: 'Variables <code>a</code> and <code>b</code> are bound to 10 and 20.' },
        { cmd: '# Tuple unpacking: swap values without temporary variable\na, b = b, a\nprint("Swapped:", a, b)', say: 'Python evaluates the right side (<code>20, 10</code>) then assigns to <code>a</code> and <code>b</code> simultaneously. Zero temporary variables needed!' },
        { cmd: '# String concatenation (+) and string repetition (*)\nmessage = "Python" + "!" * 3\nprint(message)', say: 'String operations: <code>+</code> concatenates, and <code>*</code> repeats strings!' },
        { cmd: '# Type conversion: convert string digits into an integer\nnum_str = "100"\nval = int(num_str) + 5\nprint(val)', say: '<code>int("100")</code> converts string text to an integer so arithmetic works.' },
      ],
    },

    {
      type: 'predict',
      section: SEC.p2,
      title: 'Reassignment puzzle',
      html: `<p>What is printed at the end of this script?</p>
      <pre class="codeblock" style="font-size:18px">${PythonHighlight(`x = 5
y = x
x = 10
print(y)`)}</pre>`,
      options: ['10', '5', '15', 'Error: x was overwritten'],
      answer: 1,
      explain: 'When <code>y = x</code> runs, <code>y</code> is bound to the current value of <code>x</code> (which is 5). Reassigning <code>x = 10</code> does not change <code>y</code>!',
      steps: [
        { cmd: '# Variable values are independent copies in memory\nx = 5\ny = x   # y receives 5\nx = 10  # modifying x does not affect y\nprint("x =", x, "y =", y)' },
      ],
    },

    {
      type: 'challenge',
      exercise: 2,
      mount: exerciseLink,
      section: SEC.p2,
      title: 'Temperature converter',
      html: `<p>Convert temperature from Celsius to Fahrenheit using the formula:</p>
      <div style="font-family:var(--mono);font-size:16px;padding:8px 14px;background:var(--surface-2);border-radius:8px;display:inline-block;margin-bottom:12px">
        F = (C &times; 9/5) + 32
      </div>`,
      prefill: `celsius = 25.0

# Calculate fahrenheit below:
fahrenheit = 
`,
      tasks: [
        {
          text: 'Set <code>celsius</code> to <code>25.0</code>.',
          check: (sim) => sim.vars.celsius === 25.0,
        },
        {
          text: 'Compute <code>fahrenheit</code> accurately (25.0 &rarr; 77.0).',
          check: (sim) => typeof sim.vars.fahrenheit === 'number' && Math.abs(sim.vars.fahrenheit - 77.0) < 0.001,
        },
      ],
      solution: [
        '# Celsius to Fahrenheit conversion formula: F = (C * 9/5) + 32\ncelsius = 25.0\nfahrenheit = (celsius * 9 / 5) + 32\nprint(f"{celsius}°C = {fahrenheit}°F")',
      ],
    },

    // =========================================================================
    // PART 3 — FUNCTIONS, PARAMETERS & RETURN VALUES
    // =========================================================================
    {
      type: 'section',
      section: SEC.p3,
      num: 3,
      title: 'Functions & Modularity',
      navTitle: 'Part 3 · Functions',
      sub: 'Encapsulating reusable logic, arguments, local vs global scope, and return values.',
      html: '<div class="sec-goals rv"><code>def</code><code>return</code><code>scope</code><code>parameters</code><code>None</code></div>',
    },

    {
      type: 'concept',
      section: SEC.p3,
      title: 'Anatomy of a function definition',
      html: `<div class="grid-6-4" style="align-items:center">
        <div class="clause">
          <div class="kw">def</div><div>Keyword that defines a new function</div>
          <div class="kw">name</div><div>Identifier followed by parentheses <code>(a, b)</code></div>
          <div class="kw">:</div><div>Header ends with a colon; body is <b>indented 4 spaces</b></div>
          <div class="kw">return</div><div>Passes the calculated result back to caller</div>
        </div>
        <div class="stack">
          <pre class="codeblock" style="font-size:16px">${PythonHighlight(`def calculate_tax(price, rate=0.20):
    """Calculate tax for a given price."""
    tax = price * rate
    return tax

net = calculate_tax(150.0)
print(net)  # 30.0`)}</pre>
          <ul class="points tight">
            <li>Parameters: variables in the function header (<code>price, rate</code>)</li>
            <li>Arguments: concrete values passed when calling (<code>150.0</code>)</li>
            <li>Default arguments (e.g. <code>rate=0.20</code>) make arguments optional</li>
          </ul>
        </div>
      </div>`,
    },

    {
      type: 'concept',
      section: SEC.p3,
      title: 'print() vs. return — The classic beginner trap',
      html: `<div class="grid2">
        <div class="card bad">
          <h3>print() <span class="tag amber">displays text only</span></h3>
          <ul class="points tight">
            <li>Outputs characters onto the terminal screen</li>
            <li><b>Does not</b> hand data back to the calling code</li>
            <li>The function evaluation results in <code>None</code></li>
            <li>Cannot use the result in further math or assign it</li>
          </ul>
          <pre class="codeblock">${PythonHighlight(`def bad_add(a, b):
    print(a + b)  # prints 7, but returns None!

ans = bad_add(3, 4)
# ans * 2 -> TypeError: unsupported operand None * int!`)}</pre>
        </div>
        <div class="card good">
          <h3>return <span class="tag green">yields a value</span></h3>
          <ul class="points tight">
            <li>Hands the computed value back to caller</li>
            <li>Immediately terminates execution of the function</li>
            <li>Can be saved in a variable or passed to another function</li>
            <li>The core mechanism of modular software</li>
          </ul>
          <pre class="codeblock">${PythonHighlight(`def good_add(a, b):
    return a + b  # returns 7 to caller

ans = good_add(3, 4)
print(ans * 2)    # 14 -> works perfectly!`)}</pre>
        </div>
      </div>`,
    },

    {
      type: 'demo',
      section: SEC.p3,
      title: 'Defining and composing functions',
      html: `<p>Functions can call other functions. Watch the execution flow and return values.</p>`,
      steps: [
        {
          cmd: `# Function definition: calculates the square of parameter n
def square(n):
    return n * n

print("square(6):", square(6))`,
          say: 'Defined <code>square(n)</code> and executed it with argument 6 &rarr; returns 36.',
        },
        {
          cmd: `# Function composition: sum_of_squares calls square() internally
def sum_of_squares(x, y):
    return square(x) + square(y)

print("sum_of_squares(3, 4):", sum_of_squares(3, 4))`,
          say: '<code>sum_of_squares</code> calls <code>square(3)</code> (9) and <code>square(4)</code> (16) &rarr; 25.',
        },
        {
          cmd: `# Optional parameter with default value: formal defaults to False
def greet(name, formal=False):
    prefix = "Dr. " if formal else "Hello, "
    return prefix + name

print(greet("Ada", formal=True))`,
          say: 'Optional parameter with default value: <code>greet("Ada", formal=True)</code> returns "Dr. Ada".',
        },
      ],
    },

    {
      type: 'predict',
      section: SEC.p3,
      title: 'What does this function return?',
      html: `<p>Carefully inspect this function and determine what <code>result</code> contains:</p>
      <pre class="codeblock" style="font-size:18px">${PythonHighlight(`def check_even(n):
    if n % 2 == 0:
        print("Even number")

result = check_even(4)
print("result is:", result)`)}</pre>`,
      options: ['"Even number"', 'True', 'None', '4'],
      answer: 2,
      explain: 'The function calls <code>print()</code>, but lacks a <code>return</code> statement. In Python, any function that ends without returning explicitly evaluates to <b>None</b>.',
      steps: [
        { cmd: '# Functions without an explicit return statement return None\ndef check_even(n):\n    if n % 2 == 0:\n        print("Even number")\n\nresult = check_even(4)\nprint("result is:", repr(result))' },
      ],
    },

    {
      type: 'challenge',
      exercise: 3,
      mount: exerciseLink,
      section: SEC.p3,
      title: 'Write a temperature conversion function',
      html: `<p>Implement a function <code>to_celsius(fahrenheit)</code> that converts Fahrenheit to Celsius and returns the result.</p>`,
      prefill: `def to_celsius(fahrenheit):
    # Complete the function:
    pass
`,
      tasks: [
        {
          text: 'Define a function named <code>to_celsius(fahrenheit)</code>.',
          check: (sim) => sim.hasFunction && sim.hasFunction('to_celsius'),
        },
        {
          text: '<code>to_celsius(32)</code> must return <code>0.0</code> (freezing point).',
          check: (sim) => sim.call && Math.abs(sim.call('to_celsius', 32) - 0.0) < 0.01,
        },
        {
          text: '<code>to_celsius(212)</code> must return <code>100.0</code> (boiling point).',
          check: (sim) => sim.call && Math.abs(sim.call('to_celsius', 212) - 100.0) < 0.01,
        },
      ],
      solution: [
        '# Function converting Fahrenheit to Celsius\ndef to_celsius(fahrenheit):\n    return (fahrenheit - 32) * 5 / 9\n\nprint("32F ->", to_celsius(32))\nprint("212F ->", to_celsius(212))',
      ],
    },

    // =========================================================================
    // PART 4 — CONDITIONALS & LOGIC
    // =========================================================================
    {
      type: 'section',
      section: SEC.p4,
      num: 4,
      title: 'Conditionals & Logic',
      navTitle: 'Part 4 · Conditionals',
      sub: 'Boolean expressions, relational operators, if / elif / else branches, and short-circuit evaluation.',
      html: '<div class="sec-goals rv"><code>== != &lt; &gt; &lt;= &gt;=</code><code>if / elif / else</code><code>and or not</code><code>short-circuit</code></div>',
    },

    {
      type: 'concept',
      section: SEC.p4,
      title: 'Relational & logical operators',
      html: `<div class="grid2">
        <div class="card">
          <h3>Relational Comparisons</h3>
          <table class="py-table" style="margin-top:8px">
            <tr><td><code>x == y</code></td><td>Equal to</td></tr>
            <tr><td><code>x != y</code></td><td>Not equal to</td></tr>
            <tr><td><code>x &gt; y</code></td><td>Greater than</td></tr>
            <tr><td><code>x &lt;= y</code></td><td>Less than or equal</td></tr>
            <tr><td><code>0 &lt;= x &lt;= 100</code></td><td>Chained range check!</td></tr>
          </table>
        </div>
        <div class="card">
          <h3>Logical Operators</h3>
          <table class="py-table" style="margin-top:8px">
            <tr><td><code>A and B</code></td><td>True if <b>both</b> conditions are True</td></tr>
            <tr><td><code>A or B</code></td><td>True if <b>at least one</b> is True</td></tr>
            <tr><td><code>not A</code></td><td>Inverts True &rarr; False, False &rarr; True</td></tr>
          </table>
          <div class="callout" style="margin-top:12px;font-size:13px">
            <b>Equality check:</b> Remember <code>==</code> tests equality, whereas <code>=</code> performs variable assignment!
          </div>
        </div>
      </div>`,
    },

    {
      type: 'concept',
      section: SEC.p4,
      title: 'Short-circuit evaluation',
      html: `<p class="lead">Python evaluates logical expressions from left to right and stops the moment the overall outcome is certain.</p>
      <div class="grid2" style="margin-top:20px">
        <div class="card">
          <h3><code>A and B</code> Short-Circuit</h3>
          <p>If <code>A</code> is <code>False</code>, the entire expression cannot possibly be True. Python <b>skips evaluating B</b> entirely!</p>
          <pre class="codeblock">${PythonHighlight(`count = 0
total = 100
# Safe! count != 0 is False, so total / count is NEVER executed!
if count != 0 and (total / count) > 5:
    print("Valid ratio")`)}</pre>
        </div>
        <div class="card">
          <h3><code>A or B</code> Short-Circuit</h3>
          <p>If <code>A</code> is <code>True</code>, the entire expression is already guaranteed to be True. Python skips <code>B</code>!</p>
          <pre class="codeblock">${PythonHighlight(`is_admin = True
# If is_admin is True, check_network_permissions() never runs
if is_admin or check_network_permissions():
    grant_access()`)}</pre>
        </div>
      </div>`,
    },

    {
      type: 'demo',
      section: SEC.p4,
      title: 'Multi-branch grading system',
      html: `<p>Notice how only the single matching branch executes in an <code>if / elif / else</code> ladder.</p>`,
      steps: [
        {
          cmd: `# Chained conditionals: only the first matching branch executes
score = 88
if score >= 90:
    letter = "A"
elif score >= 80:
    letter = "B"
elif score >= 70:
    letter = "C"
else:
    letter = "F"

print(f"Score {score} -> Grade {letter}")`,
          say: 'Evaluates top-down: 88 >= 90 is False, 88 >= 80 is True &rarr; letter is "B", remaining branches are skipped.',
        },
        {
          cmd: `# Conditional expression (ternary operator): <val_if_true> if <cond> else <val_if_false>
score = 95
letter = "A" if score >= 90 else "B"
print("Ternary expression:", letter)`,
          say: 'Python also supports single-line conditional expressions: <code>value_if_true if condition else value_if_false</code>.',
        },
      ],
    },

    {
      type: 'predict',
      section: SEC.p4,
      title: 'Boolean logic precedence',
      html: `<p>What will this expression print?</p>
      <pre class="codeblock" style="font-size:18px">${PythonHighlight(`val = not (5 > 2 and 3 == 4) or 10 < 5
print(val)`)}</pre>`,
      options: ['False', 'True', 'SyntaxError', 'None'],
      answer: 1,
      explain: '1. (5 > 2 and 3 == 4) &rarr; (True and False) &rarr; False.<br>2. not False &rarr; <b>True</b>.<br>3. True or 10 < 5 &rarr; <b>True</b>.',
      steps: [
        { cmd: '# Precedence order: parentheses first, then not, then and, then or\nstep1 = 5 > 2 and 3 == 4   # True and False -> False\nstep2 = not step1          # not False -> True\nstep3 = step2 or 10 < 5    # True or False -> True\nprint("Inner:", step1)\nprint("Not inner:", step2)\nprint("Final:", step3)' },
      ],
    },

    {
      type: 'challenge',
      exercise: 4,
      mount: exerciseLink,
      section: SEC.p4,
      title: 'Ticket pricing rules',
      html: `<p>Implement a function <code>ticket_price(age)</code> with these university museum discount rules:</p>
      <ul class="points tight">
        <li>Under age 6 (age &lt; 6): <b>0</b> (free admission)</li>
        <li>Ages 6 through 17: <b>10</b> (student discount)</li>
        <li>Ages 18 and older: <b>20</b> (standard adult)</li>
      </ul>`,
      prefill: `def ticket_price(age):
    # Implement pricing logic:
    pass
`,
      tasks: [
        {
          text: 'Define function <code>ticket_price(age)</code>.',
          check: (sim) => sim.hasFunction && sim.hasFunction('ticket_price'),
        },
        {
          text: 'Under 6 is free: <code>ticket_price(4) == 0</code>.',
          check: (sim) => sim.call && sim.call('ticket_price', 4) === 0,
        },
        {
          text: 'Ages 6 to 17 cost 10: <code>ticket_price(12) == 10</code> and <code>ticket_price(6) == 10</code>.',
          check: (sim) => sim.call && sim.call('ticket_price', 12) === 10 && sim.call('ticket_price', 6) === 10,
        },
        {
          text: 'Adults cost 20: <code>ticket_price(18) == 20</code> and <code>ticket_price(35) == 20</code>.',
          check: (sim) => sim.call && sim.call('ticket_price', 18) === 20 && sim.call('ticket_price', 35) === 20,
        },
      ],
      solution: [
        '# Function calculating ticket price based on age category\ndef ticket_price(age):\n    if age < 6:\n        return 0    # Under age 6: free\n    elif age <= 17:\n        return 10   # School age (6-17): $10\n    else:\n        return 20   # Adults (18+): $20\n\nprint("Age 4:", ticket_price(4))\nprint("Age 12:", ticket_price(12))\nprint("Age 22:", ticket_price(22))',
      ],
    },

    // =========================================================================
    // PART 5 — ITERATION & LOOPS
    // =========================================================================
    {
      type: 'section',
      section: SEC.p5,
      num: 5,
      title: 'Iteration & Loops',
      navTitle: 'Part 5 · Loops',
      sub: 'The while loop, for loops, range() intervals, accumulator variables, break and continue.',
      html: '<div class="sec-goals rv"><code>while</code><code>for</code><code>range(start, stop, step)</code><code>break</code><code>continue</code></div>',
    },

    {
      type: 'concept',
      section: SEC.p5,
      title: 'while loops vs. for loops',
      html: `<div class="grid2">
        <div class="card">
          <h3><code>while</code> Condition-Controlled</h3>
          <p>Repeats as long as a boolean condition remains <code>True</code>. Used when number of iterations is unknown in advance.</p>
          <pre class="codeblock">${PythonHighlight(`n = 3
while n > 0:
    print(n)
    n -= 1  # MUST update loop variable!
print("Blastoff!")`)}</pre>
          <div class="callout" style="margin-top:10px">
            <b>Warning:</b> If loop variable is never updated towards terminating condition, an <b>infinite loop</b> occurs!
          </div>
        </div>
        <div class="card good">
          <h3><code>for</code> Collection-Controlled</h3>
          <p>Iterates over items in any sequence (range, string, list). Much safer and more idiomatic in Python.</p>
          <pre class="codeblock">${PythonHighlight(`total = 0
for i in range(1, 6):
    total += i  # 1 + 2 + 3 + 4 + 5

print("Sum:", total)  # 15`)}</pre>
        </div>
      </div>`,
    },

    {
      type: 'concept',
      section: SEC.p5,
      title: 'Understanding range(start, stop, step)',
      html: `<p class="lead"><code>range()</code> produces a sequence of integers up to <i>but not including</i> the stop bound.</p>
      <div class="grid2" style="margin-top:20px">
        <div class="card">
          <h3>Common Signatures</h3>
          <table class="py-table">
            <tr><td><code>range(5)</code></td><td><code>0, 1, 2, 3, 4</code> (starts at 0)</td></tr>
            <tr><td><code>range(2, 7)</code></td><td><code>2, 3, 4, 5, 6</code></td></tr>
            <tr><td><code>range(0, 10, 2)</code></td><td><code>0, 2, 4, 6, 8</code> (step by 2)</td></tr>
            <tr><td><code>range(5, 0, -1)</code></td><td><code>5, 4, 3, 2, 1</code> (counting down)</td></tr>
          </table>
        </div>
        <div class="card">
          <h3>Loop Control Statements</h3>
          <ul class="points tight">
            <li><b><code>break</code>:</b> Immediately terminates the innermost loop.</li>
            <li><b><code>continue</code>:</b> Skips the remainder of current iteration and moves to next.</li>
          </ul>
          <pre class="codeblock">${PythonHighlight(`for n in range(10):
    if n % 2 == 1:
        continue  # skip odds
    if n == 6:
        break     # stop at 6`)}</pre>
        </div>
      </div>`,
    },

    {
      type: 'demo',
      section: SEC.p5,
      title: 'The accumulator pattern',
      html: `<p>A classic computational pattern: initialize an accumulator before loop, update each step, use result after.</p>`,
      steps: [
        {
          cmd: `# 1. Addition accumulator pattern
running_sum = 0
for num in range(1, 6):       # Generates 1, 2, 3, 4, 5
    running_sum += num        # Add current number to running total
    print(f"Added {num}, total now = {running_sum}")`,
          say: 'Computes sum 1 + 2 + 3 + 4 + 5 = 15.',
        },
        {
          cmd: `# 2. Multiplication accumulator (factorial)
factorial = 1                 # Starts at 1 (multiplicative identity)
for factor in range(1, 6):    # Multiply by 1, 2, 3, 4, 5
    factorial *= factor

print("5! =", factorial)`,
          say: 'Multiplicative accumulator: computes 5! = 120.',
        },
        {
          cmd: `# 3. List accumulator (filter & collect pattern)
evens = []                    # Empty list accumulator
for n in range(1, 11):        # Check numbers 1 through 10
    if n % 2 == 0:            # Even number check (remainder 0)
        evens.append(n)       # Collect matching element

print("Even numbers:", evens)`,
          say: 'List accumulator: filters and collects items matching a criteria.',
        },
      ],
    },

    {
      type: 'predict',
      section: SEC.p5,
      title: 'Range bounds puzzle',
      html: `<p>What is the output of this code snippet?</p>
      <pre class="codeblock" style="font-size:18px">${PythonHighlight(`# range(start, stop, step): stop bound 9 is non-inclusive!
res = 0
for k in range(2, 9, 3):      # Sequence: 2, 5, 8 (next 11 >= 9, stops)
    res += k
print(res)`)}</pre>`,
      options: ['15', '24', '10', '18'],
      answer: 0,
      explain: 'range(2, 9, 3) generates values: <b>2</b>, <b>5</b>, <b>8</b> (11 exceeds stop bound 9).<br>Sum: 2 + 5 + 8 = <b>15</b>.',
      steps: [
        { cmd: '# range(2, 9, 3) generates sequence with step 3\nnums = list(range(2, 9, 3))\nprint("Generated sequence:", nums)\nprint("Sum:", sum(nums))' },
      ],
    },

    {
      type: 'challenge',
      exercise: 5,
      mount: exerciseLink,
      section: SEC.p5,
      title: 'Sum of squares accumulator',
      html: `<p>Write a function <code>sum_of_squares(n)</code> that calculates the sum of squares from 1 through n:</p>
      <div style="font-family:var(--mono);padding:8px 14px;background:var(--surface-2);border-radius:8px;display:inline-block;margin-bottom:12px">
        1&sup2; + 2&sup2; + 3&sup2; + ... + n&sup2;
      </div>`,
      prefill: `def sum_of_squares(n):
    # Accumulate 1^2 + 2^2 + ... + n^2
    # Hint: initialize total = 0, loop for i in range(1, n + 1)
    pass
`,
      tasks: [
        {
          text: 'Define function <code>sum_of_squares(n)</code>.',
          check: (sim) => sim.hasFunction && sim.hasFunction('sum_of_squares'),
        },
        {
          text: 'For n = 1: <code>sum_of_squares(1) == 1</code>.',
          check: (sim) => sim.call && sim.call('sum_of_squares', 1) === 1,
        },
        {
          text: 'For n = 3: 1 + 4 + 9 = <code>14</code>.',
          check: (sim) => sim.call && sim.call('sum_of_squares', 3) === 14,
        },
        {
          text: 'For n = 5: 1 + 4 + 9 + 16 + 25 = <code>55</code>.',
          check: (sim) => sim.call && sim.call('sum_of_squares', 5) === 55,
        },
      ],
      solution: [
        'def sum_of_squares(n):\n    # Initialize accumulator to 0\n    total = 0\n    for i in range(1, n + 1):  # Loop 1 through n (inclusive)\n        total += i * i         # Add square of i\n    return total\n\n# Test cases\nprint("sum_of_squares(3) =", sum_of_squares(3))\nprint("sum_of_squares(5) =", sum_of_squares(5))',
      ],
    },

    // =========================================================================
    // PART 6 — STRINGS & TEXT PROCESSING
    // =========================================================================
    {
      type: 'section',
      section: SEC.p6,
      num: 6,
      title: 'Strings & Text Processing',
      navTitle: 'Part 6 · Strings',
      sub: 'Zero-based indexing, negative indexing, slicing [start:stop:step], immutability, and string methods.',
      html: '<div class="sec-goals rv"><code>s[i]</code><code>s[start:stop:step]</code><code>len()</code><code>.strip()</code><code>.split()</code><code>immutability</code></div>',
    },

    {
      type: 'concept',
      section: SEC.p6,
      title: 'Strings as indexed sequences',
      html: `<p class="lead">Strings are ordered sequences of characters. Every character has a zero-based positive index and a negative index from the right.</p>
      <div style="margin:10px 0 16px;padding:12px 18px;background:var(--surface);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow-sm)">
        <div style="font-family:var(--mono);font-size:12.5px;color:var(--muted);margin-bottom:6px">String: <code>s = "Python"</code></div>
        <div style="display:flex;gap:6px;overflow-x:auto">
          <div class="seq-cell"><span class="seq-idx-top">0</span><span class="seq-val">P</span><span class="seq-idx-bot">-6</span></div>
          <div class="seq-cell"><span class="seq-idx-top">1</span><span class="seq-val">y</span><span class="seq-idx-bot">-5</span></div>
          <div class="seq-cell"><span class="seq-idx-top">2</span><span class="seq-val">t</span><span class="seq-idx-bot">-4</span></div>
          <div class="seq-cell"><span class="seq-idx-top">3</span><span class="seq-val">h</span><span class="seq-idx-bot">-3</span></div>
          <div class="seq-cell"><span class="seq-idx-top">4</span><span class="seq-val">o</span><span class="seq-idx-bot">-2</span></div>
          <div class="seq-cell"><span class="seq-idx-top">5</span><span class="seq-val">n</span><span class="seq-idx-bot">-1</span></div>
        </div>
      </div>
      <div class="grid2">
        <div class="card">
          <h3>Indexing Syntax</h3>
          <ul class="points tight">
            <li><code>s[0]</code> &rarr; First character (<code>'P'</code>)</li>
            <li><code>s[-1]</code> &rarr; Last character (<code>'n'</code>)</li>
            <li><code>s[len(s) - 1]</code> &rarr; Also the last character</li>
            <li><b>IndexError:</b> Accessing an out-of-range index crashes!</li>
          </ul>
        </div>
        <div class="card good">
          <h3>Slicing Syntax <code>s[start:stop:step]</code></h3>
          <ul class="points tight">
            <li><code>s[0:3]</code> &rarr; <code>"Pyt"</code> (stop bound excluded!)</li>
            <li><code>s[:3]</code> &rarr; From beginning up to index 3</li>
            <li><code>s[2:]</code> &rarr; From index 2 to the end (<code>"thon"</code>)</li>
            <li><code>s[::-1]</code> &rarr; Step -1 reverses the entire string!</li>
          </ul>
        </div>
      </div>`,
    },

    {
      type: 'concept',
      section: SEC.p6,
      title: 'Strings are immutable',
      html: `<div class="grid2">
        <div class="card bad">
          <h3>Cannot mutate in-place <span class="tag red">TypeError</span></h3>
          <p>Once created, the characters inside a Python string cannot be altered or overwritten.</p>
          <pre class="codeblock" style="font-size:15px">${PythonHighlight(`word = "cat"
word[0] = "b"  # TypeError: 'str' object does not support item assignment!`)}</pre>
        </div>
        <div class="card good">
          <h3>Construct a new string instead</h3>
          <p>String methods and operations always return a <b>new</b> string; they leave the original string unchanged.</p>
          <pre class="codeblock" style="font-size:15px">${PythonHighlight(`word = "cat"
new_word = "b" + word[1:]  # "bat"
print(new_word)             # "bat"
print(word)                 # still "cat" (untouched!)`)}</pre>
        </div>
      </div>`,
    },

    {
      type: 'demo',
      section: SEC.p6,
      title: 'String methods in real-time',
      html: `<p>Watch how string inspection, slicing, and methods manipulate text.</p>`,
      steps: [
        {
          cmd: `# 1. String length and positive / negative indexing
text = "Acibadem University"
print("Length:", len(text))
# First character is at index 0, last character is at index -1
print("First letter:", text[0], "| Last letter:", text[-1])`,
          say: 'Zero-based indexing: <code>text[0]</code> is "A" and <code>text[-1]</code> is "y". Length is 19.',
        },
        {
          cmd: `# 2. Method chaining: strip whitespace, then uppercase
raw_input = "   cse 101: python   \\n"
# .strip() removes whitespace; .upper() converts case
cleaned = raw_input.strip().upper()
print("Cleaned:", repr(cleaned))`,
          say: 'Method chaining: <code>.strip()</code> removes whitespace, and <code>.upper()</code> converts to uppercase.',
        },
        {
          cmd: `# 3. Splitting into tokens and rejoining with delimiter
csv_row = "Ada,Lovelace,1815,London"
# Split string on comma delimiter into list of strings
tokens = csv_row.split(",")
print("Tokens list:", tokens)
# Join list elements back together with custom separator
rejoined = " - ".join(tokens)
print("Rejoined:", rejoined)`,
          say: '<code>.split(",")</code> parses delimited text into a list. <code>" - ".join(...)</code> combines them back.',
        },
      ],
    },

    {
      type: 'predict',
      section: SEC.p6,
      title: 'String slicing with negative step',
      html: `<p>What will this reverse slicing expression print?</p>
      <pre class="codeblock" style="font-size:18px">${PythonHighlight(`# Index mapping: 0='U', 1='n', 2='i', 3='v', 4='e', 5='r', 6='s'...
word = "University"
# Slicing with negative step: start=6 ('s'), stop=2 ('i', excluded), step=-1
print(word[6:2:-1])`)}</pre>`,
      options: ['"srev"', '"ersi"', '"srevi"', '"ive"'],
      answer: 0,
      explain: 'Indices in "University":<br>Index 6 is "s", index 5 is "r", index 4 is "e", index 3 is "v", and index 2 ("i") is excluded by stop bound.<br>Result: <b>"srev"</b>.',
      steps: [
        { cmd: '# Step through backwards from index 6 to 3\nword = "University"\nprint("Indices 6, 5, 4, 3:", word[6], word[5], word[4], word[3])\nprint("Slice word[6:2:-1]:", word[6:2:-1])' },
      ],
    },

    {
      type: 'challenge',
      exercise: 6,
      mount: exerciseLink,
      section: SEC.p6,
      title: 'Count vowels in a string',
      html: `<p>Implement a function <code>count_vowels(s)</code> that counts all vowels (<code>a, e, i, o, u</code>) in string <code>s</code>, case-insensitive.</p>`,
      prefill: `def count_vowels(s):
    # Return total vowel count (a, e, i, o, u) - case-insensitive
    # Hint: convert s.lower(), iterate characters, check if in "aeiou"
    pass
`,
      tasks: [
        {
          text: 'Define function <code>count_vowels(s)</code>.',
          check: (sim) => sim.hasFunction && sim.hasFunction('count_vowels'),
        },
        {
          text: '<code>count_vowels("apple") == 2</code>.',
          check: (sim) => sim.call && sim.call('count_vowels', 'apple') === 2,
        },
        {
          text: 'Must be case-insensitive: <code>count_vowels("Acibadem") == 4</code>.',
          check: (sim) => sim.call && sim.call('count_vowels', 'Acibadem') === 4,
        },
        {
          text: 'Handles empty string: <code>count_vowels("") == 0</code>.',
          check: (sim) => sim.call && sim.call('count_vowels', '') === 0,
        },
      ],
      solution: [
        'def count_vowels(s):\n    # Initialize counter\n    count = 0\n    # Convert string to lowercase to handle uppercase letters seamlessly\n    for char in s.lower():\n        if char in "aeiou":    # Membership test for vowels\n            count += 1\n    return count\n\n# Verification\nprint("apple:", count_vowels("apple"))\nprint("Acibadem:", count_vowels("Acibadem"))',
      ],
    },

    // =========================================================================
    // PART 7 — LISTS & COLLECTIONS
    // =========================================================================
    {
      type: 'section',
      section: SEC.p7,
      num: 7,
      title: 'Lists & Collections',
      navTitle: 'Part 7 · Lists',
      sub: 'Mutable sequences, list operations, appending, sorting, slicing, and the aliasing vs cloning trap.',
      html: '<div class="sec-goals rv"><code>[1, 2, 3]</code><code>.append()</code><code>.pop()</code><code>.sort()</code><code>aliasing vs copy</code></div>',
    },

    {
      type: 'concept',
      section: SEC.p7,
      title: 'Lists are mutable sequences',
      html: `<p class="lead">Unlike strings, Python lists are <b>mutable</b>: elements can be added, deleted, or changed in-place without creating a new list.</p>
      <div class="grid2" style="margin-top:20px">
        <div class="card good">
          <h3>In-Place Element Modification</h3>
          <p>You can directly overwrite elements by index:</p>
          <pre class="codeblock" style="font-size:14px">${PythonHighlight(`grades = [70, 85, 90]
grades[0] = 78  # legal! modifies list in-place
print(grades)   # [78, 85, 90]`)}</pre>
        </div>
        <div class="card">
          <h3>Essential List Methods</h3>
          <table class="py-table">
            <tr><td><code>lst.append(x)</code></td><td>Adds <code>x</code> to the end</td></tr>
            <tr><td><code>lst.insert(i, x)</code></td><td>Inserts <code>x</code> at index <code>i</code></td></tr>
            <tr><td><code>lst.pop()</code></td><td>Removes and returns last element</td></tr>
            <tr><td><code>lst.remove(x)</code></td><td>Removes first occurrence of <code>x</code></td></tr>
            <tr><td><code>lst.sort()</code></td><td>Sorts list in-place</td></tr>
          </table>
        </div>
      </div>`,
    },

    {
      type: 'concept',
      section: SEC.p7,
      title: 'Aliasing vs. Cloning lists — Crucial mental model',
      html: `<div class="grid2">
        <div class="card bad">
          <h3>Aliasing <code>b = a</code> <span class="tag red">shared reference</span></h3>
          <p>Does NOT duplicate the list. Both variables point to the <b>exact same list</b> in memory!</p>
          <pre class="codeblock" style="font-size:14px">${PythonHighlight(`a = [1, 2, 3]
b = a          # b points to the same object!
b.append(99)
print(a)       # [1, 2, 3, 99] -> a changed too!`)}</pre>
        </div>
        <div class="card good">
          <h3>Cloning <code>b = a.copy()</code> <span class="tag green">independent clone</span></h3>
          <p>Creates an independent shallow copy. Modifying <code>b</code> leaves <code>a</code> untouched.</p>
          <pre class="codeblock" style="font-size:14px">${PythonHighlight(`a = [1, 2, 3]
b = a.copy()   # or b = a[:]
b.append(99)
print(a)       # [1, 2, 3] -> a is preserved!
print(b)       # [1, 2, 3, 99]`)}</pre>
        </div>
      </div>`,
    },

    {
      type: 'demo',
      section: SEC.p7,
      title: 'List transformations in memory',
      html: `<p>Watch how lists grow, shrink, and reorder in the Sequence Inspector on the right.</p>`,
      steps: [
        {
          cmd: `# 1. Appending to a list (mutates list in-place)
scores = [78, 92, 85, 60]
scores.append(100)            # Adds 100 to the end of scores
print("After append(100):", scores)`,
          say: '<code>.append()</code> adds 100 to the end of the list. Notice the sequence inspector updating!',
        },
        {
          cmd: `# 2. In-place sorting (descending order)
scores.sort(reverse=True)     # Modifies original list directly
print("Sorted descending:", scores)
highest = scores[0]           # First element is now maximum
print("Highest score:", highest)`,
          say: '<code>.sort(reverse=True)</code> sorts the list in-place from highest to lowest.',
        },
        {
          cmd: `# 3. Slicing creates a new list (original untouched)
top_three = scores[:3]        # First 3 elements (indices 0, 1, 2)
print("Top 3 subset:", top_three)
print("Sum of top 3:", sum(top_three))`,
          say: 'List slicing <code>scores[:3]</code> creates a new list with the first 3 elements.',
        },
      ],
    },

    {
      type: 'predict',
      section: SEC.p7,
      title: 'The list aliasing trap',
      html: `<p>What will be printed when this script executes?</p>
      <pre class="codeblock" style="font-size:18px">${PythonHighlight(`# Aliasing: y and x point to the EXACT same list in memory!
x = [1, 2]
y = x
y.append(3)                   # Modifies the shared underlying list
print(len(x))`)}</pre>`,
      options: ['2', '3', 'Error', '1'],
      answer: 1,
      explain: '<code>y = x</code> aliases the same list. Mutating <code>y.append(3)</code> modifies the shared object, so <code>len(x)</code> is now <b>3</b>.',
      steps: [
        { cmd: '# Both variables share the exact same id/memory location\nx = [1, 2]\ny = x\nprint("id(x) == id(y)?", id(x) == id(y))\ny.append(3)\nprint("x after y.append:", x)\nprint("len(x):", len(x))' },
      ],
    },

    {
      type: 'challenge',
      exercise: 7,
      mount: exerciseLink,
      section: SEC.p7,
      title: 'Filter and double positive numbers',
      html: `<p>Implement a function <code>double_positives(nums)</code> that takes a list of numbers, filters only the numbers strictly greater than 0, and returns a <b>new list</b> with each positive number doubled.</p>`,
      prefill: `def double_positives(nums):
    # Return a new list containing doubled positive numbers (> 0)
    # Hint: create result = [], loop over nums, append n * 2 if n > 0
    pass
`,
      tasks: [
        {
          text: 'Define function <code>double_positives(nums)</code>.',
          check: (sim) => sim.hasFunction && sim.hasFunction('double_positives'),
        },
        {
          text: '<code>double_positives([2, -3, 5, 0]) == [4, 10]</code>.',
          check: (sim) => {
            if (!sim.call) return false;
            const res = sim.call('double_positives', [2, -3, 5, 0]);
            return Array.isArray(res) && res.length === 2 && res[0] === 4 && res[1] === 10;
          },
        },
        {
          text: 'All negative numbers: <code>double_positives([-1, -2]) == []</code>.',
          check: (sim) => {
            if (!sim.call) return false;
            const res = sim.call('double_positives', [-1, -2]);
            return Array.isArray(res) && res.length === 0;
          },
        },
      ],
      solution: [
        'def double_positives(nums):\n    # Accumulate transformed positive values into a new list\n    result = []\n    for n in nums:\n        if n > 0:              # Filter: only strictly positive numbers\n            result.append(n * 2)  # Double and collect\n    return result\n\n# Verification\nprint(double_positives([2, -3, 5, 0]))  # Expected: [4, 10]\nprint(double_positives([-1, -2]))       # Expected: []',
      ],
    },

    // =========================================================================
    // PART 8 — COURSE SYNTHESIS & WRAP-UP
    // =========================================================================
    {
      type: 'section',
      section: SEC.p8,
      num: 8,
      title: 'Synthesis & Wrap-up',
      navTitle: 'Part 8 · Synthesis',
      sub: 'Putting everything together: strings, lists, loops, functions, and GitHub Codespaces workflows.',
      html: '<div class="sec-goals rv"><code>Data pipelines</code><code>Cheat Sheet</code><code>GitHub Codespaces</code><code>pytest</code></div>',
    },

    {
      type: 'demo',
      section: SEC.p8,
      title: 'Synthesis demo: Text analysis pipeline',
      html: `<p>Combining loops, conditions, string cleaning, and list aggregation in a single real-world function.</p>`,
      steps: [
        {
          cmd: `corpus = """
Python is an easy to learn, powerful programming language.
Python has efficient high-level data structures and simple approaches.
Programming in Python is productive and enjoyable.
"""

# Step 1: Normalize case, strip punctuation, and split into word tokens
raw_words = corpus.lower().replace(",", "").replace(".", "").split()
print(f"Total words parsed: {len(raw_words)}")
print("Sample:", raw_words[:6])`,
          say: 'Step 1: Clean punctuation, convert to lowercase, and split into tokens.',
        },
        {
          cmd: `# Step 2: Filter words longer than 6 chars, remove duplicates, sort
long_words = []
for w in raw_words:
    # Only collect words longer than 6 chars without duplicates
    if len(w) > 6 and w not in long_words:
        long_words.append(w)

long_words.sort()  # Sort alphabetically
print(f"Unique long words ({len(long_words)}):", long_words)`,
          say: 'Step 2: Filter words longer than 6 letters without duplicates, then sort alphabetically.',
        },
        {
          cmd: `# Step 3: Compute aggregate statistics across the dataset
total_characters = sum(len(w) for w in raw_words)
avg_len = total_characters / len(raw_words)
print(f"Average word length across corpus: {avg_len:.2f} characters")`,
          say: 'Step 3: Compute aggregate statistics over the collected dataset.',
        },
      ],
    },

    {
      type: 'concept',
      section: SEC.p8,
      title: 'Python fundamentals cheat sheet',
      navTitle: 'Cheat sheet',
      html: `<div class="grid2" style="font-size:13.5px">
        <div class="card">
          <h3>Types &amp; Conversions</h3>
          <ul class="points tight">
            <li><code>int(x)</code>, <code>float(x)</code>, <code>str(x)</code>, <code>bool(x)</code></li>
            <li>Arithmetic: <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, <code>//</code>, <code>%</code>, <code>**</code></li>
            <li>f-strings: <code>f"Score: {val:.2f}"</code></li>
          </ul>
          <h3 style="margin-top:12px">Functions</h3>
          <pre class="codeblock" style="font-size:12.5px">${PythonHighlight(`def func(param, default=0):
    return param + default`)}</pre>
        </div>
        <div class="card">
          <h3>Strings &amp; Lists</h3>
          <ul class="points tight">
            <li>Zero-based: <code>seq[0]</code>, last: <code>seq[-1]</code></li>
            <li>Slices: <code>seq[start:stop:step]</code> (stop excluded!)</li>
            <li>Strings: <b>immutable</b> (<code>.strip()</code>, <code>.split()</code>)</li>
            <li>Lists: <b>mutable</b> (<code>.append()</code>, <code>.pop()</code>, <code>.sort()</code>)</li>
          </ul>
          <h3 style="margin-top:12px">Iteration</h3>
          <pre class="codeblock" style="font-size:12.5px">${PythonHighlight(`for item in list: ...
for i in range(1, 10, 2): ...
while condition: ...`)}</pre>
        </div>
      </div>`,
    },

    {
      type: 'concept',
      section: SEC.p8,
      title: 'Your practice workspace: GitHub Codespaces',
      navTitle: 'Codespaces & Practice',
      html: `<p class="lead">Everything learned today is configured for zero-setup practice in your ACU repository.</p>
      <div class="grid2" style="margin-top:20px">
        <div class="card good">
          <h3>Instant Cloud Environment</h3>
          <ul class="points tight">
            <li>Fork the repo: <code>Krr0ptioN/acu-cse-101-pract-ce</code></li>
            <li>Open with green button: <b>Code &rarr; Codespaces &rarr; Create codespace</b></li>
            <li>Pre-installed with Python 3.12, VS Code extensions, auto-save &amp; git background watcher</li>
          </ul>
        </div>
        <div class="card">
          <h3>Course Tasks Menu (Bottom Status Bar)</h3>
          <ul class="points tight">
            <li><b>$(checklist) Course Tasks &rarr; Play:</b> Run your current exercise</li>
            <li><b>Run Tests:</b> Automated pytest check of your challenge solutions</li>
            <li><b>Submit:</b> Creates your submission PR to the teaching assistants</li>
            <li><b>Sync Course:</b> Fetches new weekly exercise modules seamlessly</li>
          </ul>
        </div>
      </div>`,
    },

    {
      type: 'concept',
      section: SEC.p8,
      title: 'Questions?',
      navTitle: 'Questions & Website',
      mount: qrMount,
      html: `<div class="grid-6-4" style="align-items:center">
        <div>
          <p class="lead" style="font-size:26px">Great work completing the lecture today!</p>
          <p>Scan the QR code or use the link on the right to revisit these slides, interactive labs, and visual sequence inspectors at any time.</p>
          <div class="callout" style="margin-top:20px">
            <b>Controls reminder:</b>
            <div style="margin-top:6px;line-height:1.8">
              <kbd>→</kbd> / <kbd>Space</kbd> next · <kbd>←</kbd> back · <kbd>Enter</kbd> run step · <kbd>+</kbd> / <kbd>-</kbd> zoom (<kbd>0</kbd> reset) · <kbd>Z</kbd> text size · <kbd>O</kbd> grid · <kbd>D</kbd> dark mode · <kbd>F</kbd> fullscreen
            </div>
          </div>
        </div>
        <div class="qr-wrap" style="text-align:center">
          <div class="qr" style="display:inline-block;padding:12px;background:#fff;border-radius:14px;box-shadow:var(--shadow)"></div>
          <div class="qr-url" style="font-family:var(--mono);font-size:14px;margin-top:12px;color:var(--muted)"></div>
        </div>
      </div>`,
    },
  ];

  global.CSE101_SLIDES = slides;
})(window);
