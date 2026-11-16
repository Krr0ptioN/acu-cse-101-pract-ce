# Weeks 04–05: Conditions, Loops, and Recursion

**Think Python:** Chapters 5 and 7. One combined module; later week numbers stay
unchanged and there is no separate Week 05 submission.

## In class

[`practice.py`](practice.py) contains short prompts and empty functions for us to
complete together. Topics: comparisons, `if` / `elif` / `else`, Boolean returns,
`and` / `or` / `not`, short-circuiting, `for`, `while`, and simple recursion.

We will discuss syntax and boundary cases as we write the code. Add calls and
use **Play** or the Python Run button to try each function.

## Challenges

Complete the four empty functions in [`challenge.py`](challenge.py):

- Classify a temperature using conditions (`if` / `elif` / `else`).
- Count even positive integers using a `for` loop.
- Count how many times a number can be halved until reaching 1 using a `while` loop.
- Calculate a power of two using recursion.

Return results and keep function names and parameters unchanged. Tests check
results; the TA reviews the requested techniques.

## Check and submit

Choose **Run Tests**, then `week_04_conditions_loops_recursion`, to check the
challenges. Once they pass, choose **Submit** and the same module.
If the menu is missing, use **Command Palette → Tasks: Run Task**.

```bash
python3 -m pytest exercises/week_04_conditions_loops_recursion/test_challenge.py
```

Check the in-class practice separately:

```bash
python3 -m pytest exercises/week_04_conditions_loops_recursion/test_practice.py
```

Both sets of tests will fail until the corresponding functions are completed.
