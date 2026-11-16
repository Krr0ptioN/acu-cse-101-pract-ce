"""ACU CSE 101 - Automated Unit Tests for Weeks 06–08 Practice."""

from .practice import (
    cumulative_sum,
    invert_dictionary,
    is_palindrome,
    most_frequent_letters,
    remove_duplicates,
    word_frequency,
)


def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("Noon") is True
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("python") is False


def test_cumulative_sum():
    assert cumulative_sum([]) == []
    assert cumulative_sum([1, 2, 3]) == [1, 3, 6]
    assert cumulative_sum([5, -2, 4]) == [5, 3, 7]


def test_remove_duplicates():
    assert remove_duplicates([]) == []
    assert remove_duplicates([1, 2, 2, 3, 1, 4]) == [1, 2, 3, 4]
    assert remove_duplicates(["a", "b", "a", "c"]) == ["a", "b", "c"]


def test_word_frequency():
    text = "Hello world hello python world"
    freq = word_frequency(text)
    assert freq["hello"] == 2
    assert freq["world"] == 2
    assert freq["python"] == 1


def test_invert_dictionary():
    d = {"a": 1, "b": 2, "c": 1}
    inv = invert_dictionary(d)
    assert set(inv[1]) == {"a", "c"}
    assert inv[2] == ["b"]


def test_most_frequent_letters():
    text = "banana"
    top = most_frequent_letters(text, top_n=2)
    assert top[0] == ("a", 3)
    assert top[1] == ("n", 2)
