"""Week 03 Guided Workshop: Functions — Think Python, Chapter 3.

Complete each function with your instructor / TA.
Replace pass with your code. No input(), loops, or conditions are needed.
"""


# Part 1: Define and call a function.
# A function groups statements under a name. Defining it does not run its body.
# Goal: print "Welcome to Python!" when say_welcome() is called.
def say_welcome():
    print('Welcome to Python!')
    print("asdfafd")



# Part 2: Use a parameter and return a value.
# A parameter receives an argument from the caller.
# return sends a result back; print displays a result on the screen.
# Goal: double(4) returns 8; double(7) returns 14.

def double(number):
    doubled = number * 2
    return f"doubled value {number} is {doubled}"



a = 123
returned_value = double(a)



# Part 3: Use two parameters.
# Goal: add(3, 5) returns 8; add(10, 2) returns 12.
def add(first_var = 12, second_var = 12):
    return first_var + second_var


# After completing the functions, try these calls in the Python terminal:

say_welcome()
print(double(3))

# Function compoistion
print(add())



