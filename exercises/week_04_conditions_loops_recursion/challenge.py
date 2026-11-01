"""Complete the four functions. Return results; do not use input().

Keep names and parameters unchanged. No imports are needed.
"""


# 1. Conditions: Use if / elif / else: below 10 → "cold", 10–25 → "warm", above 25 → "hot".
# temperature is a number; both 10 and 25 are warm.
def describe_temperature(temperature):
    if temperature < 10:
        return "cold"
    elif temperature <= 25:
        return "warm"
    else:
        return "hot"


# 2. For Loop: Use a for loop to count even positive integers from 1 through n.
# n is non-negative. Examples: 0 → 0, 5 → 2, 6 → 3.
def count_evens(n):
    count = 0

    for number in range(1, n + 1):
        if number % 2 == 0:
            count += 1

    return count


# 3. While Loop: Use a while loop to count how many times n can be halved (n // 2)
# until it reaches 1. Stop when n <= 1. n is an integer >= 1.
# Examples: 1 → 0, 2 → 1, 5 → 2, 16 → 4.
def halve_until_one(n):
    count = 0

    while n > 1:
        n = n // 2
        count += 1

    return count

# 4. Recursion: Use recursion to return 2 raised to power n, without ** or pow().
# n is a small non-negative integer. Examples: 0 → 1, 3 → 8.
def power_of_two(n):
    if n == 0:
        return 1

    return 2 * power_of_two(n - 1)
    

