"""Weeks 06–08 Guided Workshop: Strings, Lists, Tuples, and Dictionaries.

Think Python: Chapters 8, 10, 11, and 12.
Build each example together in class with your instructor / TA.
Replace pass as you go.
"""
import string
# 1. Strings: Palindrome Check
# Return True if word is a palindrome (reads same forward and backward),
# ignoring case and whitespace/punctuation.
# Examples: is_palindrome("racecar") returns True
#           is_palindrome("Noon") returns True
#           is_palindrome("Python") returns False


def is_palindrome(word):
    # Keep only letters and digits, all lowercase
    key = ""
    for char in word.lower():
        if char.isalnum():
            key += char
    # Strings have no .reverse(); slicing [::-1] gives the reversed string
    return key == key[::-1]


# 2. Lists: Cumulative Sum
# Return a new list where each element is the sum of all elements up to that index.
# Examples: cumulative_sum([1, 2, 3]) returns [1, 3, 6]
#           cumulative_sum([]) returns []

def cumulative_sum(numbers):
    # Build a NEW list instead of modifying the input list
    result = []
    total = 0
    for num in numbers:
        total += num
        result.append(total)
    return result

# 3. Lists: Remove Duplicates
# Return a new list with duplicate elements removed, preserving first-appearance order.
# Examples: remove_duplicates([1, 2, 2, 3, 1, 4]) returns [1, 2, 3, 4]
#           remove_duplicates(["a", "b", "a"]) returns ["a", "b"]


def remove_duplicates(elements):
    result = []
    for item in elements:
        if item not in result:
            result.append(item)
    return result

# 4. Dictionaries: Word Frequency Counter
# Return a dictionary mapping each cleaned, lowercased word to its occurrence count.
# Examples: word_frequency("Hello world hello") returns {"hello": 2, "world": 1}
# Examples: invert_dictionary({"a": 1, "b": 2, "c": 1}) returns {1: ["a", "c"], 2: ["b"]}


def word_frequency(text):
    counts = {}
    for word in text.split():
        # Remove punctuation from both ends and lowercase
        cleaned = word.strip(string.punctuation).lower()
        if cleaned == "":
            continue
        counts[cleaned] = counts.get(cleaned, 0) + 1
    return counts

# 5. Dictionaries: Invert Mapping
# Invert a dictionary so that each value becomes a key pointing to a list of original keys.


def invert_dictionary(d):
    inverse = {}
    for key in d:
        value = d[key]
        if value in inverse:
            inverse[value].append(key)
        else:
            inverse[value] = [key]
    return inverse

# 6. Tuples & Dictionaries: Most Frequent Letters
# Return the top_n most frequent alphabetic characters as a list of (character, count) tuples,
# sorted descending by count, breaking ties alphabetically.
# Examples: most_frequent_letters("banana", top_n=2) returns [("a", 3), ("n", 2)]


def most_frequent_letters(text, top_n):
    counts = {}
    for char in text.lower():
        if char.isalpha():
            counts[char] = counts.get(char, 0) + 1
    # items() gives (char, count) tuples
    # Sort key: -count -> larger counts first; char -> alphabetical on ties
    pairs = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return pairs[:top_n]


if __name__ == "__main__":
    print("1. Palindrome:", is_palindrome("racecar"), is_palindrome("python"))
    print("2. Cumulative sum:", cumulative_sum([1, 2, 3]))
    print("3. Remove duplicates:", remove_duplicates([1, 2, 2, 3, 1]))
    print("4. Word frequency:", word_frequency("Hello world hello"))
    print("5. Invert dictionary:", invert_dictionary({"a": 1, "b": 2, "c": 1}))
    print("6. Most frequent letters:", most_frequent_letters("banana", top_n=2))

