"""Week 06–08 Graded Challenges: Strings, Lists, Tuples, and Dictionaries.

Complete the four functions below. Replace pass with your code.
Return results; do not use input().
Keep names and parameters unchanged so the automated tests can call them.
"""


# Challenge 1 (Strings): Count Vowels
def count_vowels(word):
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for char in word.lower() if char in vowels)


# Challenge 2 (Lists): Filter Positive Numbers
def filter_positives(numbers):
    return [num for num in numbers if num > 0]


# Challenge 3 (Tuples): Minimum and Maximum
def min_max(numbers):
    return (min(numbers), max(numbers))


# Challenge 4 (Dictionaries): Character Frequency Count
def count_characters(text):
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    return counts
