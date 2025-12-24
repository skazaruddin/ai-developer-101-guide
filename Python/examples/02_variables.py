"""
Python 101 - Example 2: Variables and Data Types
Understanding how to store and work with data in Python.
"""

# String variables (text)
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(f"Full name: {full_name}")

# Integer variables (whole numbers)
age = 25
year_born = 2024 - age
print(f"Age: {age}")
print(f"Year born: {year_born}")

# Float variables (decimal numbers)
height = 5.9  # feet
weight = 150.5  # pounds
print(f"Height: {height} feet")
print(f"Weight: {weight} pounds")

# Boolean variables (True/False)
is_student = True
has_job = False
print(f"Is student: {is_student}")
print(f"Has job: {has_job}")

# Type conversion
age_str = "30"
age_int = int(age_str)
print(f"Age as string: {age_str}, type: {type(age_str)}")
print(f"Age as integer: {age_int}, type: {type(age_int)}")

# Multiple assignment
x, y, z = 10, 20, 30
print(f"x={x}, y={y}, z={z}")
