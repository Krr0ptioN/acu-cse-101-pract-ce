# ==============================================================================
# ACU CSE 101: Week 01 Graded Challenge - The Way of the Program & Variables
# Think Python: Chapters 1 & 2
#
# GRADED INDEPENDENT CHALLENGE:
# Complete the 5 challenges below on your own.
# Run tests with the 'Run Tests' button or pytest to verify your solutions!
# ==============================================================================

import math  # noqa: F401

import math

# ------------------------------------------------------------------------------
# Challenge 1: Travel Currency Converter
# ------------------------------------------------------------------------------
euros = float(input("Enter amount in EUR: "))
rate = float(input("Enter exchange rate (EUR to USD): "))

gross_usd = euros * rate
fee = gross_usd * 0.02
net_usd = gross_usd - fee

print(f"Gross USD: ${gross_usd:.2f}")
print(f"Fee: ${fee:.2f}")
print(f"Net USD: ${net_usd:.2f}")


# ------------------------------------------------------------------------------
# Challenge 2: Pizza Party Slices & Leftovers
# ------------------------------------------------------------------------------
students = int(input("Enter number of students: "))
pizzas = int(input("Enter number of pizzas: "))
slices_per_pizza = int(input("Enter slices per pizza: "))

total_slices = pizzas * slices_per_pizza
slices_per_student = total_slices // students
leftover_slices = total_slices % students

print(f"Total slices: {total_slices}")
print(f"Slices per student: {slices_per_student}")
print(f"Leftover slices: {leftover_slices}")


# ------------------------------------------------------------------------------
# Challenge 3: Sphere Geometry (Volume & Surface Area)
# ------------------------------------------------------------------------------
radius = float(input("Enter sphere radius: "))

volume = (4 / 3) * math.pi * (radius ** 3)
surface_area = 4 * math.pi * (radius ** 2)

print(f"Sphere Volume: {volume:.2f}")
print(f"Sphere Surface Area: {surface_area:.2f}")


# ------------------------------------------------------------------------------
# Challenge 4: 3-Cup Shell Game (Cyclic Variable Rotation)
# ------------------------------------------------------------------------------
cup_a = input("Enter item in Cup A: ").strip()
cup_b = input("Enter item in Cup B: ").strip()
cup_c = input("Enter item in Cup C: ").strip()

cup_a, cup_b, cup_c = cup_c, cup_a, cup_b

print(cup_a, cup_b, cup_c, sep=" -> ")


# ------------------------------------------------------------------------------
# Challenge 5: Digital Event Badge Generator
# ------------------------------------------------------------------------------
name = input("Enter attendee name: ").strip().title()
dept = input("Enter department: ").strip().upper()
role = input("Enter role: ").strip().title()

border = "#" * 32
print(border)
print(f"NAME: {name}")
print(f"DEPT: {dept}")
print(f"ROLE: {role}")
print(f"NAME LENGTH: {len(name)}")
print(border)


