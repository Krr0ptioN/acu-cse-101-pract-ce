"""Week 10 Graded Challenges: Classes, Objects and 2D Geometry.

Complete the four functions below using the provided Point, Rectangle, and Circle
classes. Replace pass with your code.
Return results; do not use input().
Keep class and function names and parameters unchanged so the automated tests can call them.
"""

import copy
import math


class Point:
    """Represents a point in 2D space."""

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Rectangle:
    """Represents a rectangle with a bottom-left corner, width, and height."""

    def __init__(self, corner=None, width=0.0, height=0.0):
        self.corner = corner if corner is not None else Point(0.0, 0.0)
        self.width = width
        self.height = height


class Circle:
    """Represents a circle with a center Point and a radius."""

    def __init__(self, center=None, radius=0.0):
        self.center = center if center is not None else Point(0.0, 0.0)
        self.radius = radius


# Challenge 1 (Points): Distance Between Points
def distance_between_points(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)


# Challenge 2 (Rectangles): Rectangle Area
def rectangle_area(rect):
    return rect.width * rect.height


# Challenge 3 (Circles): Point in Circle
def point_in_circle(circle, point):
    return distance_between_points(circle.center, point) <= circle.radius


# Challenge 4 (Copying Objects): Move Rectangle Copy
def move_rectangle_copy(rect, dx, dy):
    new_rect = copy.deepcopy(rect)
    new_rect.corner.x += dx
    new_rect.corner.y += dy
    return new_rect
