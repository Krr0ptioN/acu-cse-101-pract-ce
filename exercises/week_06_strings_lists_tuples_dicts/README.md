# Weeks 06–08: Strings, Lists, Tuples, and Dictionaries

**Think Python:** Chapters 8, 10, 11, and 12. One combined data structures module;
there is no separate Week 08 submission.

## In class

[`practice.py`](practice.py) contains short prompts and empty functions for us to
complete together. Topics: string indexing and slicing, palindrome detection,
list accumulation and duplicate removal, dictionary frequency counting, dictionary
inversion, and tuple sorting.

We will discuss data structure mutability, references/aliasing, and syntax as we
write the code. Add calls and use **Play** or the Python Run button to try each function.

## Challenges

Complete the four simple functions in [`challenge.py`](challenge.py):

1. **Strings (`count_vowels`)**: Count all vowels (`a, e, i, o, u`) in a string, case-insensitive.
2. **Lists (`filter_positives`)**: Return a new list containing only positive numbers (`> 0`) in original order.
3. **Tuples (`min_max`)**: Return a `(smallest, largest)` tuple from a non-empty list of numbers.
4. **Dictionaries (`count_characters`)**: Return a frequency dictionary mapping each character to its count.

Return results and keep function names and parameters unchanged. Tests check
results; the TA reviews the requested techniques.

## Check and submit

Choose **Run Tests**, then `week_06_strings_lists_tuples_dicts`, to check the
challenges. Once they pass, choose **Submit** and the same module.
If the menu is missing, use **Command Palette → Tasks: Run Task**.

```bash
python3 -m pytest exercises/week_06_strings_lists_tuples_dicts/test_challenge.py
```

Check the in-class practice separately:

```bash
python3 -m pytest exercises/week_06_strings_lists_tuples_dicts/test_practice.py
```

Both sets of tests will fail until the corresponding functions are completed.
