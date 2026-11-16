"""Week 06-08 Graded Challenges: Strings, Lists, Tuples, and Dictionaries."""


# Challenge 1 (Strings): Count Vowels
def count_vowels(word):
    count = 0
    for ch in word.lower():
        if ch in "aeiou":
            count += 1
    return count


# Challenge 2 (Lists): Filter Positive Numbers
def filter_positives(numbers):
    result = []
    for n in numbers:
        if n > 0:
            result.append(n)
    return result


# Challenge 3 (Tuples): Minimum and Maximum
def min_max(numbers):
    return (min(numbers), max(numbers))


# Challenge 4 (Dictionaries): Character Frequency Count
def count_characters(text):
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


if __name__ == "__main__":
    print(count_vowels("Acibadem"), count_vowels(""))
    print(filter_positives([2, -3, 5, 0]))
    print(min_max([-5, 0, 10]))
    print(count_characters("banana"))
