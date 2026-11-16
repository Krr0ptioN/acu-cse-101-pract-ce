"""Week 06–08 Graded Challenges: Strings, Lists, Tuples, and Dictionaries.

Complete the four functions below. Replace pass with your code.
Return results; do not use input().
Keep names and parameters unchanged so the automated tests can call them.
"""


# Challenge 1 (Strings): Count Vowels
# Return the total count of vowels ('a', 'e', 'i', 'o', 'u') in word, case-insensitive.
# Examples: count_vowels("apple") returns 2
#           count_vowels("Acibadem") returns 4
#           count_vowels("Python") returns 1
#           count_vowels("") returns 0
def count_vowels(word):

    vowels = "aeiou"
    count = 0

    for letter in word.lower():
        if letter in vowels:
            count += 1

    return count


# Challenge 2 (Lists): Filter Positive Numbers
# Return a new list containing only the numbers strictly greater than 0,
# preserving the original order of elements.
# Examples: filter_positives([2, -3, 5, 0]) returns [2, 5]
#           filter_positives([-1, -2]) returns []
#           filter_positives([1, 2, 3]) returns [1, 2, 3]
def filter_positives(numbers):
    result = []

    for num in numbers:
        if num > 0:
            result.append(num)

    return result

# Challenge 3 (Tuples): Minimum and Maximum
# Return a tuple (smallest, largest) containing the minimum and maximum values
# from a non-empty list of numbers.
# Examples: min_max([3, 1, 4, 1, 5]) returns (1, 5)
#           min_max([42]) returns (42, 42)
#           min_max([-5, 0, 10]) returns (-5, 10)
def min_max(numbers):
    smallest = min(numbers)
    largest = max(numbers)

    return (smallest, largest)


# Challenge 4 (Dictionaries): Character Frequency Count
# Return a dictionary mapping each character in text to its occurrence count.
# Examples: count_characters("banana") returns {"b": 1, "a": 3, "n": 2}
#           count_characters("hello") returns {"h": 1, "e": 1, "l": 2, "o": 1}
#           count_characters("") returns {}
def count_characters(text):
    result = {}

    for char in text:
        if char in result:
            result[char] += 1
        else:
            result[char] = 1

    return result