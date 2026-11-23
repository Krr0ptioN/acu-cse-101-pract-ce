# Week 10: Classes, Objects and 2D Geometry

**Think Python:** Chapter 15.

## In class

[`practice.py`](practice.py) defines simple `Point` and `Rectangle` classes and
contains short prompts and empty functions for us to complete together. Topics:
programmer-defined types, attributes, instantiation, mutating objects in place,
returning new objects, aliasing, and shallow vs. deep copying (`copy.deepcopy`).

We will discuss how objects store state and how references behave when passed to
functions. Add calls and use **Play** or the Python Run button to try each function.

## Challenges

Complete the four functions in [`challenge.py`](challenge.py) using the provided
`Point`, `Rectangle`, and `Circle` classes:

1. **Points (`distance_between_points`)**: Return the Euclidean distance between two `Point` objects.
2. **Rectangles (`rectangle_area`)**: Return the area (`width * height`) of a `Rectangle`.
3. **Circles (`point_in_circle`)**: Return `True` if a `Point` lies inside or on the boundary of a `Circle`, else `False`.
4. **Copying Objects (`move_rectangle_copy`)**: Return a new `Rectangle` shifted by `(dx, dy)` without modifying the original `Rectangle` or its `corner`.

Return results and keep class/function names and parameters unchanged. Tests check
results; the TA reviews the requested techniques.

## Check and submit

Choose **Run Tests**, then `week_10_classes_objects`, to check the challenges.
Once they pass, choose **Submit** and the same module.
If the menu is missing, use **Command Palette → Tasks: Run Task**.

```bash
python3 -m pytest exercises/week_10_classes_objects/test_challenge.py
```

Check the in-class practice separately:

```bash
python3 -m pytest exercises/week_10_classes_objects/test_practice.py
```

Both sets of tests will fail until the corresponding functions are completed.
