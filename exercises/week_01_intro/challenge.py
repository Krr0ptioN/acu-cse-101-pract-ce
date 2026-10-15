# ==============================================================================
# ACU CSE 101: Week 01 Graded Challenge - The Way of the Program & Variables
# Think Python: Chapters 1 & 2
#
# GRADED INDEPENDENT CHALLENGE:
# Complete the 5 challenges below on your own.
# Run tests with the 'Run Tests' button or pytest to verify your solutions!
# ==============================================================================

import math  # noqa: F401

# ------------------------------------------------------------------------------
# Challenge 1: Travel Currency Converter
# A student is traveling abroad and exchanging Euros (EUR) to US Dollars (USD).
# The exchange desk charges a 2% transaction fee on the gross USD amount.
#
# Task:
# 1. Prompt user for:
#    - Amount in EUR (float): float(input("Enter amount in EUR: "))
#    - Exchange rate (float): float(input("Enter exchange rate (EUR to USD): "))
# 2. Calculate:
#    - gross_usd = euros * rate
#    - fee = gross_usd * 0.02
#    - net_usd = gross_usd - fee
# 3. Print the amounts formatted to 2 decimal places:
#    print(f"Gross USD: ${gross_usd:.2f}")
#    print(f"Fee: ${fee:.2f}")
#    print(f"Net USD: ${net_usd:.2f}")
# ------------------------------------------------------------------------------
# TODO: Write your code for Challenge 1 below:

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
# You are hosting a computer science pizza party!
# Slices must be distributed evenly among all students, and any leftover
# slices go to the hard-working TAs.
#
# Task:
# 1. Prompt user for:
#    - Number of students (int): int(input("Enter number of students: "))
#    - Number of pizzas (int): int(input("Enter number of pizzas: "))
#    - Slices per pizza (int): int(input("Enter slices per pizza: "))
# 2. Calculate:
#    - total_slices = pizzas * slices_per_pizza
#    - slices_per_student = total_slices // students  (integer division)
#    - leftover_slices = total_slices % students      (remainder / modulo)
# 3. Print the results:
#    print(f"Total slices: {total_slices}")
#    print(f"Slices per student: {slices_per_student}")
#    print(f"Leftover slices: {leftover_slices}")
# ------------------------------------------------------------------------------
# TODO: Write your code for Challenge 2 below:

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
# Think Python Exercise 2.2:
# The volume of a sphere with radius r is (4/3) * pi * r^3,
# and its surface area is 4 * pi * r^2.
#
# Task:
# 1. Prompt user for:
#    - Radius of the sphere (float): float(input("Enter sphere radius: "))
# 2. Calculate volume and surface area using math.pi and the ** operator.
# 3. Print the results formatted to 2 decimal places:
#    print(f"Sphere Volume: {volume:.2f}")
#    print(f"Sphere Surface Area: {surface_area:.2f}")
# ------------------------------------------------------------------------------
# TODO: Write your code for Challenge 3 below:

radius = float(input("Enter sphere radius: "))

volume = (4 / 3) * math.pi * radius ** 3
surface_area = 4 * math.pi * radius ** 2

print(f"Sphere Volume: {volume:.2f}")
print(f"Sphere Surface Area: {surface_area:.2f}")


# ------------------------------------------------------------------------------
# Challenge 4: 3-Cup Shell Game (Cyclic Variable Rotation)
# In class we swapped 2 variables (a, b = b, a).
# Now let's perform a 3-cup cyclic rotation in a single multiple assignment!
# Cup A receives Cup C's item, Cup B receives Cup A's item, and Cup C receives Cup B's item.
#
# Task:
# 1. Prompt user for:
#    - Item in Cup A: input("Enter item in Cup A: ").strip()
#    - Item in Cup B: input("Enter item in Cup B: ").strip()
#    - Item in Cup C: input("Enter item in Cup C: ").strip()
# 2. Perform the circular rotation in ONE assignment statement:
#    cup_a, cup_b, cup_c = cup_c, cup_a, cup_b
# 3. Print the rotated cups separated by ' -> ' using sep:
#    print(cup_a, cup_b, cup_c, sep=" -> ")
# ------------------------------------------------------------------------------
# TODO: Write your code for Challenge 4 below:

cup_a = input("Enter item in Cup A: ").strip()
cup_b = input("Enter item in Cup B: ").strip()
cup_c = input("Enter item in Cup C: ").strip()

cup_a, cup_b, cup_c = cup_c, cup_a, cup_b

print(cup_a, cup_b, cup_c, sep=" -> ")


# ------------------------------------------------------------------------------
# Challenge 5: Digital Event Badge Generator
# Generate a formatted conference badge for attendees using string methods
# (.strip, .title, .upper), string repetition (*), and character count (len).
#
# Task:
# 1. Prompt user for:
#    - Attendee full name (str): input("Enter attendee name: ").strip()
#    - Department (str): input("Enter department: ").strip()
#    - Role (str): input("Enter role: ").strip()
# 2. Transform the text:
#    - Format name in title case: name.title()
#    - Format department in uppercase: dept.upper()
#    - Format role in title case: role.title()
# 3. Print the badge decorated with a 32-character border of '#' characters:
#    border = "#" * 32
#    print(border)
#    print(f"NAME: {name}")
#    print(f"DEPT: {dept}")
#    print(f"ROLE: {role}")
#    print(f"NAME LENGTH: {len(name)}")
#    print(border)
# ------------------------------------------------------------------------------
# TODO: Write your code for Challenge 5 below:

name = input("Enter attendee name: ").strip()
dept = input("Enter department: ").strip()
role = input("Enter role: ").strip()

name = name.title()
dept = dept.upper()
role = role.title()

border = "#" * 32

print(border)
print(f"NAME: {name}")
print(f"DEPT: {dept}")
print(f"ROLE: {role}")
print(f"NAME LENGTH: {len(name)}")
print(border)
