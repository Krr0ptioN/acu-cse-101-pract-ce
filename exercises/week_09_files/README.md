# Week 09: File Reading, Writing and Exceptions

**Think Python:** Chapter 14.

## In class

[`practice.py`](practice.py) contains short prompts and empty functions for us to
complete together. Topics: opening files with `with`, reading and writing lines,
appending to files, handling `FileNotFoundError` and `ValueError` with
`try` / `except`, and filtering or parsing file contents.

We will discuss file modes (`"r"`, `"w"`, `"a"`), newline handling, and exception
handling as we write the code. Add calls and use **Play** or the Python Run button
to try each function.

## Challenges

Complete the four functions in [`challenge.py`](challenge.py):

1. **File Reading (`count_lines`)**: Return the total number of lines in a text file.
2. **File Writing (`write_numbered_lines`)**: Write a list of strings to a file as numbered lines (`1. ...`, `2. ...`).
3. **Searching Files (`find_matching_lines`)**: Return all lines containing a keyword (case-insensitive), stripped of trailing newlines.
4. **Exception Handling (`safe_read_int`)**: Read an integer from a file, returning a default value if the file is missing or invalid.

Return results and keep function names and parameters unchanged. Tests check
results; the TA reviews the requested techniques.

## Check and submit

Choose **Run Tests**, then `week_09_files`, to check the challenges. Once they
pass, choose **Submit** and the same module.
If the menu is missing, use **Command Palette → Tasks: Run Task**.

```bash
python3 -m pytest exercises/week_09_files/test_challenge.py
```

Check the in-class practice separately:

```bash
python3 -m pytest exercises/week_09_files/test_practice.py
```

Both sets of tests will fail until the corresponding functions are completed.
