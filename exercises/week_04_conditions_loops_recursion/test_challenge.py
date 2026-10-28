"""Result checks for the beginner challenges; approach is reviewed by the TA."""

import pytest

from .challenge import count_evens, describe_temperature, halve_until_one, power_of_two


@pytest.mark.parametrize("temperature, expected", [
    (-3, "cold"), (0, "cold"), (9.5, "cold"), (10, "warm"),
    (18, "warm"), (25, "warm"), (25.5, "hot"), (30, "hot"),
])
def test_describe_temperature(temperature, expected):
    assert describe_temperature(temperature) == expected, "10 and 25 both belong to warm."


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 0), (2, 1), (5, 2), (6, 3), (10, 5)])
def test_count_evens(n, expected):
    assert count_evens(n) == expected, "Count matching positive numbers, including n if it is even."


@pytest.mark.parametrize("n, expected", [(1, 0), (2, 1), (3, 1), (5, 2), (8, 3), (16, 4), (100, 6)])
def test_halve_until_one(n, expected):
    assert halve_until_one(n) == expected, "Count how many times n is integer-divided by 2 until it reaches 1."


@pytest.mark.parametrize("n, expected", [(0, 1), (1, 2), (2, 4), (3, 8), (5, 32), (8, 256)])
def test_power_of_two(n, expected):
    assert power_of_two(n) == expected, "Start with 1 at n = 0; double for each next power."

