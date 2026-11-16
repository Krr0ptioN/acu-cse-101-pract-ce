"""Weeks 06-08 Guided Workshop: Strings, Lists, Tuples, and Dictionaries."""

import string


# 1. Strings: Palindrome Check
# Fixes: str has no .reverse() (use slicing [::-1]), and we must ignore
# whitespace/punctuation, so keep only letters and digits.
def is_palindrome(word):
    key = "".join(ch for ch in word.lower() if ch.isalnum())
    return key == key[::-1]


# 2. Lists: Cumulative Sum
# Fix: the original modified the input list; build a NEW list instead.
def cumulative_sum(numbers):
    result = []
    total = 0
    for n in numbers:
        total += n
        result.append(total)
    return result


# 3. Lists: Remove Duplicates (keeps first-appearance order)
def remove_duplicates(elements):
    seen = set()
    result = []
    for item in elements:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# 4. Dictionaries: Word Frequency Counter
def word_frequency(text):
    counts = {}
    for word in text.lower().split():
        word = word.strip(string.punctuation)
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts


# 5. Dictionaries: Invert Mapping
def invert_dictionary(d):
    inverted = {}
    for key, value in d.items():
        inverted.setdefault(value, []).append(key)
    return inverted


# 6. Tuples & Dictionaries: Most Frequent Letters
def most_frequent_letters(text, top_n):
    counts = {}
    for ch in text.lower():
        if ch.isalpha():
            counts[ch] = counts.get(ch, 0) + 1
    # Sort by count descending, then letter ascending for ties
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return ranked[:top_n]


if __name__ == "__main__":
    print("1. Palindrome:", is_palindrome("racecar"), is_palindrome("python"))
    print("2. Cumulative sum:", cumulative_sum([1, 2, 3]))
    print("3. Remove duplicates:", remove_duplicates([1, 2, 2, 3, 1]))
    print("4. Word frequency:", word_frequency("Hello world hello"))
    print("5. Invert dictionary:", invert_dictionary({"a": 1, "b": 2, "c": 1}))
    print("6. Most frequent letters:", most_frequent_letters("banana", top_n=2))
