"""Weeks 04–05 workshop: build each example together in class.

Replace pass as we go. Use small non-negative integers for ages and n.
"""


# 1. Comparisons: ==, !=, >, >=, chained comparisons, and types.
# With age = 18, print these six comparisons in order:
# equal to 18, not equal to 18, above 18, at least 18, within 0–18, "18" equal to 18.
def comparison_examples():
    age = 18
    print(age == 18)
    print(age != 18)
    print(age > 18)
    print(age >= 18)
    print(0 <= age <= 18)
    print("18" == age)


# 2. if / elif / else: return "positive", "negative", or "zero".
# Discuss colons, indentation, return, and the zero boundary.
def describe_number(number):
    if number > 0:
        return "positive"
    elif number < 0:
        return "negative"
    else:
        return "zero"


# Branch order: price is 0 below age 6, 10 from 6–17, and 20 from 18 onward.
def ticket_price(age):
    if age < 6:
        return 0
    elif age < 18:
        return 10
    else:
        return 20


# 3. and: return whether someone is at least 12 AND has a ticket.
def can_enter(age, has_ticket):
    return age >= 12 and has_ticket


# or: return whether day is "Saturday" or "Sunday" (case-sensitive).
def is_weekend(day):
    return day == "Saturday" or day == "Sunday"


# Grouping / not: cardholders or staff can borrow, unless blocked.
def can_borrow(has_card, is_staff, is_blocked):
    return (has_card or is_staff) and not is_blocked


# 4. Short-circuiting: return whether total / count is below 10.
# Return False when count is zero. Discuss truthiness and safe evaluation.
def is_small_ratio(total, count):
    return count != 0 and total / count < 10


# 5. for / range: return the sum from 1 through n; for n = 0, return 0.
# Discuss range boundaries, steps, and where return belongs.
def sum_with_for(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


# 6. Condition inside a loop: sum only even numbers from 1 through n.
def sum_even_numbers(n):
    total = 0
    for i in range(1, n + 1):
        if i % 2 == 0:
            total += i
    return total


# 7. while: return the sum from 1 through n; for n = 0, return 0.
# Discuss the initial value, update, and stopping condition.
def sum_with_while(n):
    total = 0
    i = 1
    while i <= n:
        total += i
        i += 1
    return total



# 8. while loop with condition: count down from n to 1 by returning a list of numbers.
# For n <= 0, return [].
def countdown(n):
    numbers = []
    while n > 0:
        numbers.append(n)
        n -= 1
    return numbers


# 9. Loop through 1–5: skip 2, stop at 4, print the remaining visited numbers.
# Use continue and break.
def loop_control_examples():
    for i in range(1, 6):
        if i == 2:
            continue
        if i == 4:
            break
        print(i)


# 10. Recursion: return the sum from 1 through n; for n = 0, return 0.
# Discuss the base case and progress toward it.
def sum_with_recursion(n):
    if n == 0:
        return 0
    else:
        return n + sum_with_recursion(n - 1)


# Add calls here as we build the examples together.
comparison_examples()
print(describe_number(5))
print(ticket_price(18))
print(can_enter(12, True))
print(is_weekend("Saturday"))
print(can_borrow(True, False, False))
print(is_small_ratio(15, 3))
print(sum_with_for(5))
print(sum_even_numbers(6))
print(sum_with_while(5))
print(countdown(5))
loop_control_examples()
print(sum_with_recursion(5))