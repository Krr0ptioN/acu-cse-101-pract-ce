"""Complete the four functions. Return results; do not use input().

Keep names and parameters unchanged. No imports are needed.
"""


# 1. Conditions
def describe_temperature(temperature):
    if temperature < 10:
        return "cold"
    elif temperature <= 25:
        return "warm"
    else:
        return "hot"


# 2. For Loop
def count_evens(n):
    count = 0
    for i in range(1, n + 1):
        if i % 2 == 0:
            count += 1
    return count


# 3. While Loop
def halve_until_one(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


# 4. Recursion
def power_of_two(n):
    if n == 0:
        return 1
    return 2 * power_of_two(n - 1)

