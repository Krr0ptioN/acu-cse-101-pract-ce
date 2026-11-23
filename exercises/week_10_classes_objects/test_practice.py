"""ACU CSE 101 - Automated Unit Tests for Week 10 Practice."""

import pytest

from .practice import (
    Point,
    Rectangle,
    distance_between_points,
    find_center,
    grow_rectangle,
    make_point,
    move_point,
    move_rectangle_copy,
)


def test_make_point():
    p = make_point(3, -4)
    assert isinstance(p, Point)
    assert p.x == 3
    assert p.y == -4


def test_distance_between_points():
    assert distance_between_points(Point(0, 0), Point(3, 4)) == pytest.approx(5.0)
    assert distance_between_points(Point(-1, -1), Point(2, 3)) == pytest.approx(5.0)
    assert distance_between_points(Point(2, 5), Point(2, 5)) == pytest.approx(0.0)


def test_move_point():
    p = Point(1, 2)
    move_point(p, 3, -5)
    assert p.x == 4
    assert p.y == -3


def test_find_center():
    rect = Rectangle(Point(2, 4), 10, 20)
    center = find_center(rect)
    assert isinstance(center, Point)
    assert center.x == pytest.approx(7.0)
    assert center.y == pytest.approx(14.0)


def test_grow_rectangle():
    rect = Rectangle(Point(0, 0), 10, 20)
    grow_rectangle(rect, 5, -4)
    assert rect.width == 15
    assert rect.height == 16


def test_move_rectangle_copy():
    original = Rectangle(Point(1, 2), 10, 20)
    moved = move_rectangle_copy(original, 4, -6)

    assert isinstance(moved, Rectangle)
    assert moved is not original
    assert moved.corner is not original.corner
    assert moved.corner.x == 5
    assert moved.corner.y == -4
    assert moved.width == 10
    assert moved.height == 20
    assert original.corner.x == 1
    assert original.corner.y == 2
