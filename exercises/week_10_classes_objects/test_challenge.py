"""Automated unit tests for Week 10 Graded Challenges."""

import pytest

from .challenge import (
    Circle,
    Point,
    Rectangle,
    distance_between_points,
    move_rectangle_copy,
    point_in_circle,
    rectangle_area,
)


@pytest.mark.parametrize(
    "p1, p2, expected",
    [
        (Point(0, 0), Point(3, 4), 5.0),
        (Point(1, 1), Point(1, 1), 0.0),
        (Point(-2, 1), Point(4, 9), 10.0),
        (Point(0, 0), Point(1, 1), 2**0.5),
    ],
)
def test_distance_between_points(p1, p2, expected):
    assert distance_between_points(p1, p2) == pytest.approx(expected), (
        "Compute the Euclidean distance between p1 and p2."
    )


@pytest.mark.parametrize(
    "width, height, expected",
    [
        (4, 5, 20),
        (2.5, 4.0, 10.0),
        (0, 10, 0),
        (7, 7, 49),
    ],
)
def test_rectangle_area(width, height, expected):
    rect = Rectangle(Point(1, 2), width, height)
    assert rectangle_area(rect) == pytest.approx(expected), (
        "Return width * height for the given Rectangle."
    )


@pytest.mark.parametrize(
    "center, radius, point, expected",
    [
        (Point(0, 0), 5, Point(0, 0), True),
        (Point(0, 0), 5, Point(3, 4), True),
        (Point(0, 0), 5, Point(2, 2), True),
        (Point(0, 0), 5, Point(5.1, 0), False),
        (Point(10, -5), 3, Point(12, -4), True),
        (Point(10, -5), 3, Point(14, -5), False),
    ],
)
def test_point_in_circle(center, radius, point, expected):
    circle = Circle(center, radius)
    assert point_in_circle(circle, point) is expected, (
        "Return True if the point is inside or on the boundary of the circle."
    )


def test_move_rectangle_copy():
    original = Rectangle(Point(3, 4), 12, 8)
    moved = move_rectangle_copy(original, -5, 10)

    assert isinstance(moved, Rectangle), "Return a Rectangle instance."
    assert moved is not original, "Return a new Rectangle instead of mutating the original."
    assert moved.corner is not original.corner, (
        "Do not share the same corner Point object between the original and the copy."
    )
    assert moved.corner.x == -2 and moved.corner.y == 14, (
        "Shift the copied rectangle's corner by (dx, dy)."
    )
    assert moved.width == 12 and moved.height == 8, "Preserve width and height."
    assert original.corner.x == 3 and original.corner.y == 4, (
        "Leave the original rectangle's corner unchanged."
    )
