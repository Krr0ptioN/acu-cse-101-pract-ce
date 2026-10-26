"""Week 03 Graded Challenge: Functions — Think Python, Chapter 3.

Complete the three functions below. Replace pass with your code.
Use the supplied parameters and return the answer instead of printing it.
Do not use input(). No imports, loops, or conditions are needed.
Keep the function names and parameters unchanged so the tests can call them.
"""


# Challenge 1: Personal Greeting
# Return a greeting using the supplied name.
# Examples: greet("Ada") returns "Hello, Ada!"
#           greet("Deniz") returns "Hello, Deniz!"
def greet(name):
    return "Hello, " + name + "!"


# Challenge 2: Square a Number
# Return the given number multiplied by itself.
# Examples: square(4) returns 16; square(7) returns 49.
def square(number):
    return number * number


# Challenge 3: Minutes to Seconds
# Return the number of seconds in the supplied number of minutes.
# There are 60 seconds in one minute.
# Examples: minutes_to_seconds(2) returns 120.
#           minutes_to_seconds(5) returns 300.
def minutes_to_seconds(minutes):
    return minutes * 60