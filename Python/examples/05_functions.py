"""
Python 101 - Example 5: Functions
Reusable blocks of code.
"""

# Simple function with no parameters
def say_hello():
    print("Hello, World!")

say_hello()

print("-" * 30)

# Function with parameters
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
greet("Bob")

print("-" * 30)

# Function with return value
def add(a, b):
    return a + b

result = add(5, 3)
print(f"5 + 3 = {result}")

print("-" * 30)

# Function with default parameters
def power(base, exponent=2):
    return base ** exponent

print(f"3 squared: {power(3)}")
print(f"2 cubed: {power(2, 3)}")

print("-" * 30)

# Function with multiple return values
def get_min_max(numbers):
    return min(numbers), max(numbers)

nums = [5, 2, 8, 1, 9, 3]
minimum, maximum = get_min_max(nums)
print(f"Numbers: {nums}")
print(f"Min: {minimum}, Max: {maximum}")

print("-" * 30)

# Function with keyword arguments
def describe_person(name, age, city):
    print(f"{name} is {age} years old and lives in {city}.")

describe_person(name="Alice", age=30, city="New York")
describe_person(city="Boston", name="Bob", age=25)  # Order doesn't matter

print("-" * 30)

# Practical example: Temperature converter
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

# Test conversions
temps_c = [0, 25, 100]
print("Celsius to Fahrenheit:")
for c in temps_c:
    f = celsius_to_fahrenheit(c)
    print(f"  {c}°C = {f}°F")

temps_f = [32, 77, 212]
print("\nFahrenheit to Celsius:")
for f in temps_f:
    c = fahrenheit_to_celsius(f)
    print(f"  {f}°F = {c:.1f}°C")
