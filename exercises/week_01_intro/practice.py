# ==============================================================================
# ACU CSE 101: Week 01 Guided Workshop - The Way of the Program & Variables
# Think Python: Chapters 1 & 2
#
# INSTRUCTOR & STUDENT IN-CLASS WORKSHOP:
# Welcome to Python! Do not worry about solving this alone.
# You will write the code for each part below together with your instructor / TA
# during our live lecture & lab session.
#
# Follow along with your instructor as we explore:
# 1. Using input() to read strings from the user
# 2. Converting user input with int() and float()
# 3. Cleaning user input with .strip()
# 4. Floating-point comparison pitfalls (math.isclose)
# 5. Exact decimal arithmetic for financial calculations (Decimal)
# 6. Multiple assignment & variable swapping (a, b = b, a)
# 7. Chained assignment (x = y = 50) and independent re-binding
# 8. String operations (+ concatenation, * repetition, len, methods)
# 9. String formatting for print() (f-string precision, alignment, sep & end)
# ==============================================================================

import math  # noqa: F401
from decimal import Decimal  # noqa: F401

# ------------------------------------------------------------------------------
# Part 1: Reading Text with input()
# input() pauses execution and waits for the user to type something.
# It ALWAYS returns the entered value as a string (str).
#
# In-Class Goal:
# 1. Ask for the user's name: user_name = input("Enter your name: ")
# 2. Greet the user: print(f"Hello, {user_name}! Welcome to CSE 101.")
# ------------------------------------------------------------------------------
# TODO: Write Part 1 together in class below:
user_name = input("Enter your name: ")
print(f"Hello, {user_name}! Welcome to CSE 101.")


# ------------------------------------------------------------------------------
# Part 2: Integer Input & Type Conversion - int()
# If we need a whole number for arithmetic, convert the string using int().
#
# In-Class Goal:
# 1. Ask user for birth year: birth_year = int(input("Enter your birth year: "))
# 2. Calculate age: age = 2026 - birth_year
# 3. Print: print(f"You will turn {age} years old in 2026.")
# ------------------------------------------------------------------------------
# TODO: Write Part 2 together in class below:
birth_year = int(input("Enter your birth year: "))
age = 2026 - birth_year
print(f"You will turn {age} years old in 2026.")

# ------------------------------------------------------------------------------
# Part 3: Float Input & Type Conversion - float()
# If the number has decimal places, convert the string using float().
#
# In-Class Goal:
# 1. Ask user for Celsius: celsius = float(input("Enter temperature in Celsius: "))
# 2. Convert to Fahrenheit: fahrenheit = (celsius * 9 / 5) + 32
# 3. Print: print("Fahrenheit:", fahrenheit)
# ------------------------------------------------------------------------------
# TODO: Write Part 3 together in class below:
celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = (celsius * 9 / 5) + 32
print("Fahrenheit:", fahrenheit)


# ------------------------------------------------------------------------------
# Part 4: Cleaning Input with .strip()
# Users often type extra leading/trailing spaces. .strip() removes them.
#
# In-Class Goal:
# 1. Ask for student ID and clean it:
#    student_id = input("Enter your student ID: ").strip()
# 2. Print: print(f"Registered student ID: '{student_id}'")
# ------------------------------------------------------------------------------
# TODO: Write Part 4 together in class below:
student_id = input("Enter your student ID: ").strip()
print(f"Registered student ID: '{student_id}'")

# ------------------------------------------------------------------------------
# Part 5: Float Comparison Pitfall & math.isclose()
# In binary floating-point (IEEE 754), 0.1 and 0.2 cannot be represented
# exactly. 0.1 + 0.2 is actually 0.30000000000000004!
#
# In-Class Goal:
# 1. Set float_sum = 0.1 + 0.2
# 2. Demonstrate that float_sum == 0.3 is False
# 3. Demonstrate that math.isclose(float_sum, 0.3) is True
# ------------------------------------------------------------------------------
# TODO: Write Part 5 together in class below:
float_sum = 0.1 + 0.2
print(float_sum == 0.3)
print(math.isclose(float_sum, 0.3))

# ------------------------------------------------------------------------------
# Part 6: Exact Financial Arithmetic with Decimal
# When calculating money or accounting figures, use Decimal.
#
# In-Class Goal:
# 1. Calculate exact_sum = Decimal("0.1") + Decimal("0.2")
# 2. Print: print("Exact Decimal sum:", exact_sum)
# ------------------------------------------------------------------------------
# TODO: Write Part 6 together in class below:
exact_sum = Decimal("0.1") + Decimal("0.2")
print("Exact Decimal sum:", exact_sum)

# ------------------------------------------------------------------------------
# Part 7: Multiple Assignment & Variable Swapping
# Python allows unpacking multiple values and swapping in a single line.
#
# In-Class Goal:
# 1. Initialize a, b = 12, 34
# 2. Swap them cleanly: a, b = b, a
# 3. Print the swapped values: print(f"Swapped: a={a}, b={b}")
# ------------------------------------------------------------------------------
# TODO: Write Part 7 together in class below:
a, b = 12, 34
a, b = b, a
print(f"Swapped: a={a}, b={b}")


# ------------------------------------------------------------------------------
# Part 8: Chained Assignment & Re-binding
# In Python, variables are names pointing to values, not linked equations.
#
# In-Class Goal:
# 1. Assign: x = y = 50
# 2. Re-bind: x = x + 10
# 3. Print: print(f"Rebound: x={x}, y={y}")
# ------------------------------------------------------------------------------
# TODO: Write Part 8 together in class below:
x = y = 50
x = x + 10
print(f"Rebound: x={x}, y={y}")


# ------------------------------------------------------------------------------
# Part 9: String Operations (+, *, len, and string methods)
# Strings can be joined with +, repeated with *, and measured with len().
# Methods like .upper(), .lower(), and .title() return transformed copies.
#
# In-Class Goal:
# 1. Create first_name = "ada", last_name = "lovelace"
# 2. Join and title-case: full_name = (first_name + " " + last_name).title()
# 3. Create a repeated border: greeting_banner = "=" * 30
# 4. Print the banner, full_name, full_name.upper(), and len(full_name)
# ------------------------------------------------------------------------------
# TODO: Write Part 9 together in class below:
first_name = "ada"
last_name = "lovelace"

full_name = (first_name + " " + last_name).title()
greeting_banner = "=" * 30

print(greeting_banner)
print(full_name)
print(full_name.upper())
print(len(full_name))


# ------------------------------------------------------------------------------
# Part 10: String Formatting for print() (f-strings, precision & print parameters)
# F-strings allow precision formatting (:.2f), column alignment (<, >),
# and print() supports custom separators (sep) and line endings (end).
#
# In-Class Goal:
# 1. Format float price (49.9567) with 2 decimals: f"${price:.2f}"
# 2. Format percentage (0.08): f"{tax_rate:.1%}"
# 3. Use sep parameter: print("Python", "CSE101", "Acibadem", sep=" :: ")
# 4. Use end parameter: print("Saving progress", end="... "); print("Done!")
# ------------------------------------------------------------------------------
# TODO: Write Part 10 together in class below:

price = 49.9567
tax_rate = 0.08

print(f"${price:.2f}")
print(f"{tax_rate:.1%}")

print("Python", "CSE101", "Acibadem", sep=" :: ")

print("Saving progress", end="... ")
print("Done!")
