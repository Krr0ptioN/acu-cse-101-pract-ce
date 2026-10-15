# ==============================================================================
# ACU CSE 101: Week 02 Graded Challenge - Variables, Expressions and Statements
# Think Python: Chapter 2
#
# Complete these three challenges using variables and print().
# No functions or user input are needed. Store the given values in variables.
# ==============================================================================

# ------------------------------------------------------------------------------
# Challenge 1: Notebook Cost
# One notebook costs 20 TL. You buy 3 notebooks.
# Calculate the total cost and print it labeled "Total cost:".
# ------------------------------------------------------------------------------
# TODO: Write your code for Challenge 1 below:

notebook_price = 20
quantity = 3

total_cost = notebook_price * quantity

print("Total cost:", total_cost)


# ------------------------------------------------------------------------------
# Challenge 2: Minutes to Seconds
# A break lasts 5 minutes. Each minute has 60 seconds.
# Calculate the break's length in seconds and print it labeled "Seconds:".
# ------------------------------------------------------------------------------
# TODO: Write your code for Challenge 2 below:

minutes = 5
seconds_per_minute = 60

seconds = minutes * seconds_per_minute

print("Seconds:", seconds)


# ------------------------------------------------------------------------------
# Challenge 3: Simple Greeting
# Store "Ada" in a name variable.
# Use the variable to print "Hello, Ada!".
# ------------------------------------------------------------------------------
# TODO: Write your code for Challenge 3 below:


name = "Ada"

print(f"Hello, {name}!")
