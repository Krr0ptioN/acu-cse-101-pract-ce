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
    # TODO: Return vowel count
    count = 0
    for char in word.lower():
        if char in "aeiou":
            count += 1
    return count


# Challenge 2 (Lists): Filter Positive Numbers
# Return a new list containing only the numbers strictly greater than 0,
# preserving the original order of elements.
# Examples: filter_positives([2, -3, 5, 0]) returns [2, 5]
#           filter_positives([-1, -2]) returns []
#           filter_positives([1, 2, 3]) returns [1, 2, 3]
def filter_positives(numbers):
    # TODO: Return new list with only positive numbers
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
    # TODO: Return (smallest, largest) as a tuple
    return (min(numbers), max(numbers))


# Challenge 4 (Dictionaries): Character Frequency Count
# Return a dictionary mapping each character in text to its occurrence count.
# Examples: count_characters("banana") returns {"b": 1, "a": 3, "n": 2}
#           count_characters("hello") returns {"h": 1, "e": 1, "l": 2, "o": 1}
#           count_characters("") returns {}
def count_characters(text):
    # TODO: Return character count dictionary
    counts = {}
    for char in text:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1
    return counts


print("--- 1. count_vowels ---")
print(count_vowels("apple"))
print(count_vowels("Acibadem"))
print(count_vowels("Python"))
print(count_vowels(""))

print("\n--- 2. filter_positives ---")
print(filter_positives([2, -3, 5, 0]))
print(filter_positives([-1, -2]))
print(filter_positives([1, 2, 3]))

print("\n--- 3. min_max ---")
print(min_max([3, 1, 4, 1, 5]))
print(min_max([42]))
print(min_max([-5, 0, 10]))

print("\n--- 4. count_characters ---")
print(count_characters("banana"))
print(count_characters("hello"))
print(count_characters(""))
