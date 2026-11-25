"""Week 06–08 Graded Challenges: Strings, Lists, Tuples, and Dictionaries.

Complete the four functions below. Replace pass with your code.
Return results; do not use input().
Keep names and parameters unchanged so the automated tests can call them.
"""


# Challenge 1 (Strings): Count Vowels
def count_vowels(word):
    vowels = "aeiou"
    count = 0
    for char in word.lower():
        if char in vowels:
            count += 1
    return count


# Challenge 2 (Lists): Filter Positive Numbers
def filter_positives(numbers):
    positives = []
    for num in numbers:
        if num > 0:
            positives.append(num)
    return positives


# Challenge 3 (Tuples): Minimum and Maximum
def min_max(numbers):
    return (min(numbers), max(numbers))


# Challenge 4 (Dictionaries): Character Frequency Count
def count_characters(text):
    counts = {}
    for char in text:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1
    return counts
