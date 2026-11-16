"""Weeks 06–08 Guided Workshop: Strings, Lists, Tuples, and Dictionaries.

Think Python: Chapters 8, 10, 11, and 12.
Build each example together in class with your instructor / TA.
Replace pass as you go.
"""

# 1. Strings: Palindrome Check
# Return True if word is a palindrome (reads same forward and backward),
# ignoring case and whitespace/punctuation.
# Examples: is_palindrome("racecar") returns True
#           is_palindrome("Noon") returns True
#           is_palindrome("Python") returns False
def is_palindrome(word):
    key = word.lower()
    return key == key.reverse()


# 2. Lists: Cumulative Sum
# Return a new list where each element is the sum of all elements up to that index.
# Examples: cumulative_sum([1, 2, 3]) returns [1, 3, 6]
#           cumulative_sum([]) returns []
def cumulative_sum(numbers):
    for i in range(1, len(numbers)):
        numbers[i] += numbers[i - 1]
    return numbers


# 3. Lists: Remove Duplicates
# Return a new list with duplicate elements removed, preserving first-appearance order.
# Examples: remove_duplicates([1, 2, 2, 3, 1, 4]) returns [1, 2, 3, 4]
#           remove_duplicates(["a", "b", "a"]) returns ["a", "b"]
def remove_duplicates(elements):
    pass


# 4. Dictionaries: Word Frequency Counter
# Return a dictionary mapping each cleaned, lowercased word to its occurrence count.
# Examples: word_frequency("Hello world hello") returns {"hello": 2, "world": 1}
# Examples: invert_dictionary({"a": 1, "b": 2, "c": 1}) returns {1: ["a", "c"], 2: ["b"]}
def word_frequency(text):
    pass


# 5. Dictionaries: Invert Mapping
# Invert a dictionary so that each value becomes a key pointing to a list of original keys.
def invert_dictionary(d):
    pass


# 6. Tuples & Dictionaries: Most Frequent Letters
# Return the top_n most frequent alphabetic characters as a list of (character, count) tuples,
# sorted descending by count, breaking ties alphabetically.
# Examples: most_frequent_letters("banana", top_n=2) returns [("a", 3), ("n", 2)]
def most_frequent_letters(text, top_n):
    pass


if __name__ == "__main__":
    print("1. Palindrome:", is_palindrome("racecar"), is_palindrome("python"))
    print("2. Cumulative sum:", cumulative_sum([1, 2, 3]))
    print("3. Remove duplicates:", remove_duplicates([1, 2, 2, 3, 1]))
    print("4. Word frequency:", word_frequency("Hello world hello"))
    print("5. Invert dictionary:", invert_dictionary({"a": 1, "b": 2, "c": 1}))
    print("6. Most frequent letters:", most_frequent_letters("banana", top_n=2))
