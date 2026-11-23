"""Week 10 Graded Challenges: Classes, Objects and 2D Geometry.

Complete the four functions below using the provided Point, Rectangle, and Circle
classes. Replace pass with your code.
Return results; do not use input().
Keep class and function names and parameters unchanged so the automated tests can call them.
"""

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
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt(dx ** 2 + dy ** 2)


# Challenge 2 (Rectangles): Rectangle Area
def rectangle_area(rect):
    return rect.width * rect.height


# Challenge 3 (Circles): Point in Circle
def point_in_circle(circle, point):
    distance = distance_between_points(circle.center, point)
    return distance <= circle.radius


# Challenge 4 (Copying Objects): Move Rectangle Copy
def move_rectangle_copy(rect, dx, dy):
    new_corner = Point(rect.corner.x + dx, rect.corner.y + dy)
    return Rectangle(new_corner, rect.width, rect.height)


if __name__ == "__main__":
    # Challenge 1
    print(distance_between_points(Point(0, 0), Point(3, 4)))  # 5.0
    print(distance_between_points(Point(1, 1), Point(1, 1)))  # 0.0

    # Challenge 2
    print(rectangle_area(Rectangle(Point(0, 0), 4, 5)))        # 20
    print(rectangle_area(Rectangle(Point(2, 3), 2.5, 4.0)))    # 10.0

    # Challenge 3
    c = Circle(Point(0, 0), 5)
    print(point_in_circle(c, Point(3, 4)))  # True
    print(point_in_circle(c, Point(1, 1)))  # True
    print(point_in_circle(c, Point(6, 0)))  # False

    # Challenge 4
    r1 = Rectangle(Point(1, 2), 10, 20)
    r2 = move_rectangle_copy(r1, 5, -3)
    print(r2.corner.x, r2.corner.y)  # 6 -1
    print(r1.corner.x, r1.corner.y)  # 1 2  (original unchanged)
