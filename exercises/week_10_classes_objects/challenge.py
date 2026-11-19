"""Week 10 Graded Challenges: Classes, Objects and 2D Geometry.

Complete the four functions below using the provided Point, Rectangle, and Circle
classes. Replace pass with your code.
Return results; do not use input().
Keep class and function names and parameters unchanged so the automated tests can call them.
"""


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
# Return the Euclidean distance between two Point objects p1 and p2.
# Examples: distance_between_points(Point(0, 0), Point(3, 4)) returns 5.0
#           distance_between_points(Point(1, 1), Point(1, 1)) returns 0.0
def distance_between_points(p1, p2):
    # TODO: Return Euclidean distance between p1 and p2
    pass


# Challenge 2 (Rectangles): Rectangle Area
# Return the area (width * height) of the given Rectangle object.
# Examples: rectangle_area(Rectangle(Point(0, 0), 4, 5)) returns 20
#           rectangle_area(Rectangle(Point(2, 3), 2.5, 4.0)) returns 10.0
def rectangle_area(rect):
    # TODO: Return width * height of rect
    pass


# Challenge 3 (Circles): Point in Circle
# Return True if point lies inside or on the boundary of circle
# (distance from circle.center to point <= circle.radius), and False otherwise.
# Examples: c = Circle(Point(0, 0), 5)
#           point_in_circle(c, Point(3, 4)) returns True  (on boundary)
#           point_in_circle(c, Point(1, 1)) returns True  (inside)
#           point_in_circle(c, Point(6, 0)) returns False (outside)
def point_in_circle(circle, point):
    # TODO: Return True if point is inside or on the boundary of circle
    pass


# Challenge 4 (Copying Objects): Move Rectangle Copy
# Return a new Rectangle with the same width and height, whose corner is shifted
# by (dx, dy). The original rect and rect.corner must NOT be modified.
# Example: r1 = Rectangle(Point(1, 2), 10, 20)
#          r2 = move_rectangle_copy(r1, 5, -3)
#          -> r2.corner is at (6, -1), r1.corner is still at (1, 2)
def move_rectangle_copy(rect, dx, dy):
    # TODO: Return a moved copy of rect without mutating the original
    pass
