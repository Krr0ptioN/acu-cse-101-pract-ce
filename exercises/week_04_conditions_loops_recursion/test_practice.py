"""Check the in-class exercises after completion, including boundaries and empty loops."""

import pytest

from . import practice


@pytest.mark.parametrize("number, expected", [(-1, "negative"), (0, "zero"), (1, "positive")])
def test_describe_number(number, expected):
    assert practice.describe_number(number) == expected


@pytest.mark.parametrize("age, expected", [(0, 0), (5, 0), (6, 10), (17, 10), (18, 20)])
def test_ticket_boundaries(age, expected):
    assert practice.ticket_price(age) == expected


@pytest.mark.parametrize("age, ticket, expected", [(11, True, False), (12, True, True), (12, False, False)])
def test_can_enter(age, ticket, expected):
    assert practice.can_enter(age, ticket) is expected


@pytest.mark.parametrize("day, expected", [("Saturday", True), ("Sunday", True), ("Monday", False), ("sunday", False)])
def test_weekend(day, expected):
    assert practice.is_weekend(day) is expected


@pytest.mark.parametrize("card", [False, True])
@pytest.mark.parametrize("staff", [False, True])
@pytest.mark.parametrize("blocked", [False, True])
def test_borrow_grouping(card, staff, blocked):
    expected = (card, staff, blocked) in {
        (True, False, False), (False, True, False), (True, True, False),
    }
    assert practice.can_borrow(card, staff, blocked) is expected


@pytest.mark.parametrize("total, count, expected", [(12, 2, True), (20, 2, False), (12, 0, False)])
def test_short_circuit(total, count, expected):
    assert practice.is_small_ratio(total, count) is expected


@pytest.mark.parametrize("function", [practice.sum_with_for, practice.sum_with_while, practice.sum_with_recursion])
@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (3, 6), (5, 15)])
def test_three_ways_to_sum(function, n, expected):
    assert function(n) == expected


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 0), (2, 2), (5, 6), (6, 12)])
def test_condition_in_loop(n, expected):
    assert practice.sum_even_numbers(n) == expected


def test_comparisons(capsys):
    practice.comparison_examples()
    assert capsys.readouterr().out.splitlines() == ["True", "False", "False", "True", "True", "False"]


def test_break_and_continue(capsys):
    practice.loop_control_examples()
    assert capsys.readouterr().out.splitlines() == ["1", "3"]


@pytest.mark.parametrize("n, expected", [(0, []), (-2, []), (1, [1]), (3, [3, 2, 1]), (5, [5, 4, 3, 2, 1])])
def test_countdown(n, expected):
    assert practice.countdown(n) == expected

