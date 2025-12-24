"""
Python 101 - Example 3: Control Flow (If-Else)
Making decisions in your programs.
"""

# Simple if statement
age = 20

if age >= 18:
    print("You are an adult")

# If-else statement
temperature = 15

if temperature >= 25:
    print("It's hot outside!")
else:
    print("It's cool outside.")

# If-elif-else statement
score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")

# Combining conditions with 'and' and 'or'
age = 25
has_license = True
has_car = False

if age >= 18 and has_license:
    print("You can legally drive")

if has_car or has_license:
    print("You have some driving capability")

# Using 'not'
is_raining = False

if not is_raining:
    print("Let's go for a walk!")

# Nested if statements
user_age = 16
has_parent_permission = True

if user_age >= 18:
    print("Welcome to the website!")
else:
    if has_parent_permission:
        print("Welcome! (with parental consent)")
    else:
        print("Sorry, you need parental permission.")
