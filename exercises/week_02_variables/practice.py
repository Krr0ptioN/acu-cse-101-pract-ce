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
discount = 0.40
copies = 60
 
discounted_price = cover_price * (1 - discount)
books_cost = discounted_price * copies
shipping = 3 + 0.75 * (copies - 1)
total = books_cost + shipping
 
print(f"Total wholesale cost: ${total:.2f}")

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
start_seconds = 6 * 3600 + 52 * 60          # 6:52 AM, gece yarisindan beri saniye
 
easy_pace = 8 * 60 + 15                     # 8 dk 15 sn / mil
tempo_pace = 7 * 60 + 12                    # 7 dk 12 sn / mil
run_seconds = 2 * easy_pace + 3 * tempo_pace
 
arrival_seconds = start_seconds + run_seconds
arrival_hour = arrival_seconds // 3600
arrival_minute = (arrival_seconds % 3600) // 60
 
print(f"{arrival_hour:02d}:{arrival_minute:02d}")

# ------------------------------------------------------------------------------
# Part 3: Centering & Formatting Strings
# String centering adds padding around text to reach a chosen width.
#
# In-Class Goal:
# Center "PYTHON CSE 101" in a 30-character banner using "=" as padding.
# Print the banner.
# ------------------------------------------------------------------------------
# TODO: Write Part 3 together in class below:
banner = "PYTHON CSE 101".center(30, "=")
print(banner)