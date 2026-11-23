"""Week 10 Guided Workshop: Classes, Objects and 2D Geometry.

Think Python: Chapter 15.
Build each example together in class with your instructor / TA.
Replace pass as you go.
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


# 1. Instantiation: Make Point
# Create and return a new Point object with attributes x and y.
# Example: p = make_point(3, 4) -> p.x == 3, p.y == 4
def make_point(x, y):
    pass


# 2. Reading Attributes: Distance Between Points
# Return the Euclidean distance between two Point objects p1 and p2.
# Example: distance_between_points(Point(0, 0), Point(3, 4)) returns 5.0
def distance_between_points(p1, p2):
    pass


# 3. Mutating Objects: Move Point In Place
# Shift p in place by adding dx to p.x and dy to p.y.
# Example: p = Point(1, 2); move_point(p, 3, -1) -> p.x == 4, p.y == 1
def move_point(p, dx, dy):
    pass


# 4. Returning Objects: Find Center of Rectangle
# Return a new Point located at the center of rect:
# (rect.corner.x + rect.width / 2, rect.corner.y + rect.height / 2).
# Example: find_center(Rectangle(Point(0, 0), 10, 20)) -> Point(5.0, 10.0)
def find_center(rect):
    pass


# 5. Mutating Objects: Grow Rectangle In Place
# Increase rect.width by dwidth and rect.height by dheight in place.
# Example: grow_rectangle(rect, 5, 10) updates rect.width and rect.height
def grow_rectangle(rect, dwidth, dheight):
    pass


# 6. Copying Objects: Move Rectangle Copy
# Return a NEW Rectangle shifted by (dx, dy) without modifying the original
# rect or its corner Point (avoid aliasing with copy.deepcopy or new instances).
def move_rectangle_copy(rect, dx, dy):
    pass


if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    print("1. Make point:", make_point(3, 4))
    print("2. Distance:", distance_between_points(p1, p2))
    box = Rectangle(Point(0, 0), 10, 20)
    print("4. Center:", find_center(box))
