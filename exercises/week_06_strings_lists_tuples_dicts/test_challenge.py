"""Automated unit tests for Week 06–08 Graded Challenges."""

import pytest

from .challenge import count_characters, count_vowels, filter_positives, min_max


@pytest.mark.parametrize(
    "word, expected",
    [
        ("apple", 2),
        ("Python", 1),
        ("Acibadem", 4),
        ("", 0),
        ("sky", 0),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("rhythm", 0),
        ("Hello World", 3),
    ],
)
def test_count_vowels(word, expected):
    assert count_vowels(word) == expected, "Count all vowels (a, e, i, o, u) case-insensitively."


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([2, -3, 5, 0], [2, 5]),
        ([-1, -2, -3], []),
        ([], []),
        ([1, 2, 3], [1, 2, 3]),
        ([0, 0, 4, -1, 7], [4, 7]),
        ([-10, 20, -30, 40], [20, 40]),
    ],
)
def test_filter_positives(numbers, expected):
    assert filter_positives(numbers) == expected, "Keep only numbers strictly greater than 0."


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([3, 1, 4, 1, 5], (1, 5)),
        ([42], (42, 42)),
        ([-5, 0, 10], (-5, 10)),
        ([10, -2, 8, -9, 3], (-9, 10)),
        ([7, 7, 7], (7, 7)),
        ([1.5, 3.2, 0.8, 2.1], (0.8, 3.2)),
    ],
)
def test_min_max(numbers, expected):
    result = min_max(numbers)
    assert isinstance(result, tuple), "The returned result must be a tuple."
    assert result == expected, "Return (smallest, largest) as a tuple."


@pytest.mark.parametrize(
    "text, expected",
    [
        ("banana", {"b": 1, "a": 3, "n": 2}),
        ("hello", {"h": 1, "e": 1, "l": 2, "o": 1}),
        ("", {}),
        ("aaa", {"a": 3}),
        ("abacaba", {"a": 4, "b": 2, "c": 1}),
    ],
)
def test_count_characters(text, expected):
    assert count_characters(text) == expected, "Map each character to its occurrence count."
