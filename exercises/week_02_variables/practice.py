# ==============================================================================
# ACU CSE 101: Week 02 Guided Workshop - Variables, Expressions and Statements
# Think Python: Chapter 2
#
# Write each part with your instructor / TA. No functions are needed yet.
# ==============================================================================

# ------------------------------------------------------------------------------
# Part 1: Variables & Discount Calculations
# Variables store values that expressions can use to calculate new values.
# A percentage discount reduces the original price; shipping adds to the total.
#
# In-Class Goal:
# Calculate the wholesale cost of 60 books with a cover price of $24.95
# and a 40% discount. Shipping is $3 for the first copy and $0.75 for
# each additional copy. Print the total with two decimal places.
# ------------------------------------------------------------------------------
# TODO: Write Part 1 together in class below:
cover_price = 24.95
discount_rate = 0.40
discounted_price = cover_price * (1 - discount_rate)

copies = 60
books_cost = discounted_price * copies

shipping_cost = 3.00 + 0.75 * (copies - 1)
total_wholesale_cost = books_cost + shipping_cost

print(f"Total Wholesale Cost: ${total_wholesale_cost:.2f}")


# ------------------------------------------------------------------------------
# Part 2: Time Arithmetic with // and %
# Use seconds as a common unit when adding durations.
# Floor division finds complete units; modulo finds the remainder.
#
# In-Class Goal:
# Find the arrival time after leaving at 6:52 AM and running 2 miles
# at 8 minutes 15 seconds per mile and 3 miles at 7 minutes 12 seconds
# per mile. Print the arrival hour and minute in HH:MM format.
# ------------------------------------------------------------------------------
# TODO: Write Part 2 together in class below:
start_hour = 6
start_minute = 52
start_time_seconds = (start_hour * 3600) + (start_minute * 60)

run_1_seconds = 2 * (8 * 60 + 15)
run_2_seconds = 3 * (7 * 60 + 12)
total_run_seconds = run_1_seconds + run_2_seconds

total_time_seconds = start_time_seconds + total_run_seconds

arrival_hour = (total_time_seconds // 3600) % 24
arrival_minute = (total_time_seconds % 3600) // 60

print(f"Arrival Time: {arrival_hour:02d}:{arrival_minute:02d}")


# TODO: Write Part 3 together in class below:
text = "PYTHON CSE 101"
banner = text.center(30, "=")
print(banner)
