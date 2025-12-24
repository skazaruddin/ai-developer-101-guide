# Chapter 1: Python Fundamentals

## The Complete Beginner's Guide to Python Programming

---

## Table of Contents

1. [What is Programming?](#what-is-programming)
2. [Why Python?](#why-python)
3. [Installing Python](#installing-python)
4. [Setting Up Your IDE](#setting-up-your-ide)
5. [Your First Python Program](#your-first-python-program)
6. [Variables and Data Types](#variables-and-data-types)
7. [Operators](#operators)
8. [Control Flow (If-Else)](#control-flow-if-else)
9. [Loops](#loops)
10. [Functions](#functions)
11. [Lists and Collections](#lists-and-collections)
12. [Dictionaries](#dictionaries)
13. [File Handling](#file-handling)
14. [Error Handling](#error-handling)
15. [Practice Exercises](#practice-exercises)

---

## What is Programming?

### The Simple Explanation

Imagine you're giving instructions to a very obedient but very literal helper. This helper will do exactly what you say, nothing more, nothing less. Programming is the art of writing these instructions in a language that computers understand.

### Real-World Analogy

Think of a recipe:

```
1. Take 2 eggs
2. Break them into a bowl
3. Add salt
4. Beat until mixed
5. Heat pan with oil
6. Pour mixture
7. Cook until done
```

This recipe is a "program" for making scrambled eggs! Programming is similar - you write step-by-step instructions for the computer to follow.

### Why Do We Need Programming?

- **Automation**: Do repetitive tasks automatically (like sending 1000 emails)
- **Data Processing**: Analyze millions of records in seconds
- **Problem Solving**: Create solutions for complex problems
- **Innovation**: Build apps, websites, games, AI systems, and more!

---

## Why Python?

### Python is Perfect for Beginners Because:

1. **Readable Syntax**: Python code looks almost like English
2. **Versatile**: Used in web development, AI, data science, automation
3. **Large Community**: Millions of developers to help you
4. **Rich Libraries**: Pre-built tools for almost everything
5. **In-Demand**: One of the most sought-after skills in tech

### Comparing Python with Other Languages

**Java:**
```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**Python:**
```python
print("Hello, World!")
```

See the difference? Python lets you focus on solving problems, not fighting with syntax!

---

## Installing Python

### For Windows

1. **Download Python**
   - Go to [python.org/downloads](https://python.org/downloads)
   - Click "Download Python 3.12.x" (or latest version)

2. **Run the Installer**
   - **IMPORTANT**: Check the box that says "Add Python to PATH"
   - Click "Install Now"

3. **Verify Installation**
   - Open Command Prompt (search "cmd" in Start menu)
   - Type: `python --version`
   - You should see: `Python 3.12.x`

### For macOS

1. **Using Homebrew (Recommended)**
   ```bash
   # Install Homebrew first (if not installed)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install Python
   brew install python
   ```

2. **Verify Installation**
   ```bash
   python3 --version
   ```

### For Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

---

## Setting Up Your IDE

An IDE (Integrated Development Environment) is like a super-powered text editor designed for coding. We'll cover two popular options.

### Option 1: Visual Studio Code (VS Code) - Recommended for Beginners

#### Installation

1. Download from [code.visualstudio.com](https://code.visualstudio.com)
2. Install with default settings
3. Open VS Code

#### Setting Up Python in VS Code

1. **Install Python Extension**
   - Click the Extensions icon (or press `Ctrl+Shift+X`)
   - Search for "Python"
   - Install the one by Microsoft (first result)

2. **Create Your First Project**
   - Click File → Open Folder
   - Create a new folder called `python-learning`
   - Open it

3. **Create a Python File**
   - Click File → New File
   - Save as `hello.py` (the `.py` extension tells VS Code it's Python)

4. **Select Python Interpreter**
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose the Python version you installed

5. **Run Your Code**
   - Write: `print("Hello, World!")`
   - Click the play button (▶) in the top right
   - Or press `F5`

### Option 2: PyCharm

#### Installation

1. Download PyCharm Community (free) from [jetbrains.com/pycharm](https://jetbrains.com/pycharm)
2. Install with default settings

#### Setting Up Your First Project

1. **Create New Project**
   - Open PyCharm
   - Click "New Project"
   - Choose a location (e.g., `python-learning`)
   - Ensure "Create a main.py welcome script" is checked
   - Click Create

2. **Run Your Code**
   - Right-click on `main.py`
   - Click "Run 'main'"
   - Or press `Shift+F10`

### VS Code vs PyCharm: Which to Choose?

| Feature | VS Code | PyCharm |
|---------|---------|---------|
| Speed | Faster, lighter | Slower, heavier |
| Setup | Needs extensions | Ready out of box |
| Best For | Multi-language | Python-focused |
| Price | Free | Free (Community) |

**Recommendation**: Start with VS Code for its simplicity, switch to PyCharm when you need advanced features.

---

## Your First Python Program

### The Classic "Hello, World!"

Create a file called `hello.py` and type:

```python
print("Hello, World!")
```

Run it, and you'll see:
```
Hello, World!
```

Congratulations! You've written your first program!

### Understanding the Code

- `print()` is a **function** - it does something (displays text)
- `"Hello, World!"` is a **string** - text enclosed in quotes
- The text inside `print()` is called an **argument**

### Try These Variations

```python
# This is a comment - Python ignores it
print("Hello, World!")
print("My name is Python")
print("I am learning to code!")

# You can print numbers too
print(42)
print(3.14)

# You can do math!
print(2 + 2)
print(10 * 5)
```

---

## Variables and Data Types

### What is a Variable?

A variable is like a labeled box where you store information.

```python
# Creating variables
name = "Alice"      # A box labeled 'name' containing "Alice"
age = 25            # A box labeled 'age' containing 25
height = 5.6        # A box labeled 'height' containing 5.6
is_student = True   # A box labeled 'is_student' containing True

# Using variables
print(name)         # Output: Alice
print(age)          # Output: 25
```

### Python Data Types

#### 1. Strings (str) - Text

```python
# Strings are text enclosed in quotes
first_name = "John"
last_name = 'Doe'           # Single or double quotes work
message = "Hello, World!"

# String operations
full_name = first_name + " " + last_name  # Concatenation
print(full_name)  # Output: John Doe

# String methods
print(message.upper())      # HELLO, WORLD!
print(message.lower())      # hello, world!
print(len(message))         # 13 (length of string)
```

#### 2. Numbers

```python
# Integers (int) - Whole numbers
age = 25
year = 2024
temperature = -5

# Floating-point (float) - Decimal numbers
price = 19.99
pi = 3.14159
percentage = 85.5

# Number operations
total = 10 + 5      # Addition: 15
diff = 10 - 5       # Subtraction: 5
product = 10 * 5    # Multiplication: 50
quotient = 10 / 3   # Division: 3.333...
floor_div = 10 // 3 # Floor division: 3
remainder = 10 % 3  # Modulus (remainder): 1
power = 2 ** 3      # Exponentiation: 8
```

#### 3. Boolean (bool) - True/False

```python
is_sunny = True
is_raining = False

# Booleans from comparisons
age = 25
is_adult = age >= 18    # True
is_teenager = age < 20  # False
```

#### 4. None - Represents "nothing"

```python
result = None  # Variable exists but has no value yet
```

### Type Conversion

```python
# Convert between types
age_str = "25"
age_int = int(age_str)      # String to Integer: 25

price = 19.99
price_int = int(price)      # Float to Integer: 19
price_str = str(price)      # Float to String: "19.99"

number = 42
number_float = float(number) # Integer to Float: 42.0

# Check type
print(type(age_str))        # <class 'str'>
print(type(age_int))        # <class 'int'>
```

### Variable Naming Rules

```python
# Valid names
name = "John"
my_name = "John"
myName = "John"
name2 = "John"
_private = "John"

# Invalid names (will cause errors)
# 2name = "John"      # Can't start with number
# my-name = "John"    # Can't use hyphens
# my name = "John"    # Can't have spaces
# class = "John"      # Can't use reserved words
```

### Best Practices

```python
# Use descriptive names
# Bad
x = 25
# Good
user_age = 25

# Use snake_case for variables in Python
# Bad
userName = "John"
# Good
user_name = "John"

# Use UPPERCASE for constants
MAX_SIZE = 100
PI = 3.14159
```

---

## Operators

### Arithmetic Operators

```python
a = 10
b = 3

print(a + b)    # Addition: 13
print(a - b)    # Subtraction: 7
print(a * b)    # Multiplication: 30
print(a / b)    # Division: 3.333...
print(a // b)   # Floor Division: 3
print(a % b)    # Modulus: 1
print(a ** b)   # Exponent: 1000
```

### Comparison Operators

```python
a = 10
b = 5

print(a == b)   # Equal to: False
print(a != b)   # Not equal to: True
print(a > b)    # Greater than: True
print(a < b)    # Less than: False
print(a >= b)   # Greater than or equal: True
print(a <= b)   # Less than or equal: False
```

### Logical Operators

```python
x = True
y = False

print(x and y)  # AND: False (both must be True)
print(x or y)   # OR: True (at least one True)
print(not x)    # NOT: False (inverts the value)

# Practical example
age = 25
has_license = True

can_drive = age >= 18 and has_license  # True
```

### Assignment Operators

```python
x = 10          # Assign 10 to x

x += 5          # Same as: x = x + 5 → x is now 15
x -= 3          # Same as: x = x - 3 → x is now 12
x *= 2          # Same as: x = x * 2 → x is now 24
x /= 4          # Same as: x = x / 4 → x is now 6.0
```

---

## Control Flow (If-Else)

### Making Decisions

Programs need to make decisions based on conditions. This is called **control flow**.

### The if Statement

```python
age = 20

if age >= 18:
    print("You are an adult")
```

**Important**: Python uses **indentation** (spaces) to define code blocks. Usually 4 spaces.

### if-else Statement

```python
age = 15

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

# Output: You are a minor
```

### if-elif-else Statement

```python
score = 85

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

print(f"Your grade is: {grade}")  # Output: Your grade is: B
```

### Nested if Statements

```python
age = 25
has_id = True

if age >= 18:
    if has_id:
        print("Welcome! You can enter.")
    else:
        print("Sorry, you need an ID.")
else:
    print("Sorry, you must be 18 or older.")
```

### Combining Conditions

```python
age = 25
is_member = True

# Using 'and'
if age >= 18 and is_member:
    print("Welcome, member!")

# Using 'or'
is_weekend = True
is_holiday = False

if is_weekend or is_holiday:
    print("The office is closed")

# Using 'not'
is_raining = False

if not is_raining:
    print("Let's go outside!")
```

### Practical Example: Login System

```python
correct_username = "admin"
correct_password = "secret123"

username = input("Enter username: ")
password = input("Enter password: ")

if username == correct_username and password == correct_password:
    print("Login successful! Welcome!")
elif username != correct_username:
    print("Username not found")
else:
    print("Incorrect password")
```

---

## Loops

### Why Do We Need Loops?

Instead of writing repetitive code:
```python
print("Hello")
print("Hello")
print("Hello")
print("Hello")
print("Hello")
```

We can use a loop:
```python
for i in range(5):
    print("Hello")
```

### The for Loop

```python
# Loop through a range
for i in range(5):
    print(i)
# Output: 0, 1, 2, 3, 4

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
# Output: apple, banana, cherry

# Loop through a string
for letter in "Python":
    print(letter)
# Output: P, y, t, h, o, n
```

### Range Function

```python
# range(stop) - 0 to stop-1
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop) - start to stop-1
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Counting backwards
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

### The while Loop

```python
# Basic while loop
count = 0
while count < 5:
    print(count)
    count += 1
# Output: 0, 1, 2, 3, 4

# Practical example: User input validation
password = ""
while password != "secret":
    password = input("Enter password: ")
print("Access granted!")
```

### Loop Control Statements

```python
# break - Exit the loop immediately
for i in range(10):
    if i == 5:
        break
    print(i)
# Output: 0, 1, 2, 3, 4

# continue - Skip current iteration
for i in range(5):
    if i == 2:
        continue
    print(i)
# Output: 0, 1, 3, 4

# pass - Do nothing (placeholder)
for i in range(3):
    pass  # TODO: implement later
```

### Nested Loops

```python
# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")
    print("---")

# Output:
# 1 x 1 = 1
# 1 x 2 = 2
# 1 x 3 = 3
# ---
# 2 x 1 = 2
# ... etc
```

### Practical Example: Sum Calculator

```python
# Calculate sum of numbers 1 to 100
total = 0
for num in range(1, 101):
    total += num
print(f"Sum of 1 to 100: {total}")
# Output: Sum of 1 to 100: 5050
```

---

## Functions

### What is a Function?

A function is a reusable block of code that performs a specific task. Think of it as a mini-program within your program.

### Why Use Functions?

1. **Reusability**: Write once, use many times
2. **Organization**: Break complex problems into smaller parts
3. **Readability**: Give meaningful names to code blocks
4. **Maintainability**: Fix bugs in one place

### Creating a Function

```python
# Define a function
def greet():
    print("Hello, World!")

# Call the function
greet()  # Output: Hello, World!
greet()  # Output: Hello, World!
```

### Functions with Parameters

```python
# Function with one parameter
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Output: Hello, Alice!
greet("Bob")    # Output: Hello, Bob!

# Function with multiple parameters
def add(a, b):
    print(f"{a} + {b} = {a + b}")

add(5, 3)   # Output: 5 + 3 = 8
```

### Functions with Return Values

```python
# Return a value
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8

# Use return value in expressions
total = add(10, 20) + add(5, 5)
print(total)  # Output: 40
```

### Default Parameters

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")                  # Output: Hello, Alice!
greet("Alice", "Good morning")  # Output: Good morning, Alice!
```

### Keyword Arguments

```python
def describe_pet(name, animal, age):
    print(f"{name} is a {age}-year-old {animal}")

# Using keyword arguments (order doesn't matter)
describe_pet(animal="dog", name="Max", age=3)
# Output: Max is a 3-year-old dog
```

### Multiple Return Values

```python
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    return minimum, maximum, average

nums = [1, 2, 3, 4, 5]
min_val, max_val, avg = get_stats(nums)
print(f"Min: {min_val}, Max: {max_val}, Avg: {avg}")
# Output: Min: 1, Max: 5, Avg: 3.0
```

### Variable Scope

```python
# Global variable
message = "Hello"

def greet():
    # Local variable
    name = "Alice"
    print(f"{message}, {name}")

greet()      # Output: Hello, Alice
print(message)  # Output: Hello
# print(name)  # Error! name is not defined outside function
```

### Practical Example: Temperature Converter

```python
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9

# Test the functions
temp_c = 25
temp_f = celsius_to_fahrenheit(temp_c)
print(f"{temp_c}°C = {temp_f}°F")
# Output: 25°C = 77.0°F

temp_f = 98.6
temp_c = fahrenheit_to_celsius(temp_f)
print(f"{temp_f}°F = {temp_c:.1f}°C")
# Output: 98.6°F = 37.0°C
```

---

## Lists and Collections

### What is a List?

A list is an ordered collection of items. Think of it as a container that can hold multiple values.

```python
# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty_list = []
```

### Accessing List Items

```python
fruits = ["apple", "banana", "cherry", "date"]

# Indexing (starts at 0)
print(fruits[0])    # apple (first item)
print(fruits[1])    # banana (second item)
print(fruits[-1])   # date (last item)
print(fruits[-2])   # cherry (second to last)

# Slicing
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[:2])    # ['apple', 'banana']
print(fruits[2:])    # ['cherry', 'date']
```

### Modifying Lists

```python
fruits = ["apple", "banana", "cherry"]

# Change an item
fruits[1] = "blueberry"
print(fruits)  # ['apple', 'blueberry', 'cherry']

# Add items
fruits.append("date")           # Add to end
fruits.insert(1, "avocado")     # Add at specific position
print(fruits)  # ['apple', 'avocado', 'blueberry', 'cherry', 'date']

# Remove items
fruits.remove("avocado")        # Remove by value
popped = fruits.pop()           # Remove and return last item
del fruits[0]                   # Remove by index
print(fruits)  # ['blueberry', 'cherry']
```

### List Operations

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Length
print(len(numbers))      # 8

# Sorting
numbers.sort()           # Sort in place
print(numbers)           # [1, 1, 2, 3, 4, 5, 6, 9]

sorted_nums = sorted([3, 1, 4])  # Returns new sorted list
print(sorted_nums)       # [1, 3, 4]

# Reverse
numbers.reverse()
print(numbers)           # [9, 6, 5, 4, 3, 2, 1, 1]

# Min, Max, Sum
print(min(numbers))      # 1
print(max(numbers))      # 9
print(sum(numbers))      # 31
```

### List Comprehension

A powerful Python feature to create lists concisely:

```python
# Traditional way
squares = []
for x in range(5):
    squares.append(x ** 2)
print(squares)  # [0, 1, 4, 9, 16]

# List comprehension
squares = [x ** 2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]

# With condition
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]
```

### Tuples - Immutable Lists

```python
# Tuples cannot be modified after creation
coordinates = (10, 20)
rgb_color = (255, 128, 0)

x, y = coordinates  # Unpacking
print(x)  # 10
print(y)  # 20

# Tuples are used for data that shouldn't change
days_of_week = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
```

---

## Dictionaries

### What is a Dictionary?

A dictionary stores data as key-value pairs. Think of it like a real dictionary where you look up a word (key) to find its definition (value).

```python
# Creating a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Accessing values
print(person["name"])     # Alice
print(person.get("age"))  # 30
print(person.get("job", "Not specified"))  # Not specified (default)
```

### Modifying Dictionaries

```python
person = {"name": "Alice", "age": 30}

# Add or update
person["city"] = "Boston"       # Add new key
person["age"] = 31              # Update existing key

# Remove
del person["city"]              # Remove by key
removed_age = person.pop("age") # Remove and return value

print(person)  # {'name': 'Alice'}
```

### Dictionary Operations

```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Get all keys
print(person.keys())    # dict_keys(['name', 'age', 'city'])

# Get all values
print(person.values())  # dict_values(['Alice', 30, 'New York'])

# Get all items (key-value pairs)
print(person.items())   # dict_items([('name', 'Alice'), ...])

# Check if key exists
print("name" in person)  # True
print("job" in person)   # False
```

### Looping Through Dictionaries

```python
person = {"name": "Alice", "age": 30, "city": "Boston"}

# Loop through keys
for key in person:
    print(key)

# Loop through values
for value in person.values():
    print(value)

# Loop through key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```

### Nested Dictionaries

```python
employees = {
    "emp1": {
        "name": "Alice",
        "department": "Engineering"
    },
    "emp2": {
        "name": "Bob",
        "department": "Marketing"
    }
}

print(employees["emp1"]["name"])  # Alice
```

### Practical Example: Contact Book

```python
contacts = {}

def add_contact(name, phone, email):
    contacts[name] = {"phone": phone, "email": email}
    print(f"Added {name} to contacts")

def get_contact(name):
    if name in contacts:
        contact = contacts[name]
        print(f"Name: {name}")
        print(f"Phone: {contact['phone']}")
        print(f"Email: {contact['email']}")
    else:
        print(f"{name} not found in contacts")

# Usage
add_contact("Alice", "555-1234", "alice@email.com")
add_contact("Bob", "555-5678", "bob@email.com")
get_contact("Alice")
```

---

## File Handling

### Why File Handling?

Programs need to save data permanently (not just in memory). Files let us:
- Store data between program runs
- Share data between programs
- Process large amounts of data

### Reading Files

```python
# Method 1: Basic reading
file = open("example.txt", "r")  # "r" = read mode
content = file.read()
print(content)
file.close()  # Always close the file!

# Method 2: Using 'with' (Recommended - auto-closes file)
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

# Read line by line
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())  # strip() removes newline characters

# Read all lines into a list
with open("example.txt", "r") as file:
    lines = file.readlines()
    print(lines)
```

### Writing Files

```python
# Write mode ("w") - overwrites existing content
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a new file.\n")

# Append mode ("a") - adds to existing content
with open("output.txt", "a") as file:
    file.write("This line is appended.\n")

# Write multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)
```

### Practical Example: Log File

```python
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("app.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

# Usage
log_message("Application started")
log_message("User logged in")
log_message("Processing data")
```

### Working with CSV Files

```python
import csv

# Writing CSV
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"]
]

with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Reading CSV
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

---

## Error Handling

### What are Errors?

Errors (exceptions) occur when something goes wrong during program execution. Good programs handle errors gracefully.

### Common Errors

```python
# ZeroDivisionError
result = 10 / 0

# TypeError
result = "hello" + 5

# ValueError
number = int("hello")

# FileNotFoundError
file = open("nonexistent.txt")

# KeyError
person = {"name": "Alice"}
print(person["age"])

# IndexError
numbers = [1, 2, 3]
print(numbers[10])
```

### Try-Except Blocks

```python
# Basic try-except
try:
    result = 10 / 0
except:
    print("An error occurred")

# Catching specific errors
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Multiple except blocks
try:
    number = int(input("Enter a number: "))
    result = 100 / number
except ValueError:
    print("Please enter a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### Try-Except-Else-Finally

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found!")
else:
    # Runs if no exception occurred
    print("File read successfully")
    print(content)
finally:
    # Always runs, even if exception occurred
    print("Cleanup complete")
```

### Practical Example: Safe Input

```python
def get_positive_number():
    while True:
        try:
            num = float(input("Enter a positive number: "))
            if num <= 0:
                print("Number must be positive!")
                continue
            return num
        except ValueError:
            print("Invalid input. Please enter a number.")

# Usage
number = get_positive_number()
print(f"You entered: {number}")
```

---

## Practice Exercises

### Exercise 1: Personal Information

Create a program that:
1. Asks for the user's name, age, and city
2. Stores them in variables
3. Prints a formatted introduction

```python
# Your solution here
name = input("What's your name? ")
age = input("How old are you? ")
city = input("Where do you live? ")

print(f"\nHello! My name is {name}.")
print(f"I am {age} years old and I live in {city}.")
```

### Exercise 2: Temperature Converter

Create a function that converts temperatures between Celsius and Fahrenheit:

```python
def convert_temperature(value, unit):
    """
    Convert temperature between Celsius and Fahrenheit.
    unit: 'C' for Celsius to Fahrenheit, 'F' for Fahrenheit to Celsius
    """
    if unit.upper() == 'C':
        result = (value * 9/5) + 32
        return f"{value}°C = {result}°F"
    elif unit.upper() == 'F':
        result = (value - 32) * 5/9
        return f"{value}°F = {result:.2f}°C"
    else:
        return "Invalid unit. Use 'C' or 'F'"

# Test
print(convert_temperature(100, 'C'))  # 100°C = 212°F
print(convert_temperature(32, 'F'))   # 32°F = 0.00°C
```

### Exercise 3: Number Guessing Game

```python
import random

def guessing_game():
    secret = random.randint(1, 100)
    attempts = 0

    print("I'm thinking of a number between 1 and 100!")

    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1

            if guess < secret:
                print("Too low! Try again.")
            elif guess > secret:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You got it in {attempts} attempts!")
                break
        except ValueError:
            print("Please enter a valid number.")

# Run the game
guessing_game()
```

### Exercise 4: Shopping List Manager

```python
shopping_list = []

def show_menu():
    print("\n--- Shopping List Manager ---")
    print("1. Add item")
    print("2. Remove item")
    print("3. View list")
    print("4. Clear list")
    print("5. Exit")

def add_item():
    item = input("Enter item to add: ")
    shopping_list.append(item)
    print(f"'{item}' added to the list!")

def remove_item():
    if not shopping_list:
        print("List is empty!")
        return

    item = input("Enter item to remove: ")
    if item in shopping_list:
        shopping_list.remove(item)
        print(f"'{item}' removed from the list!")
    else:
        print(f"'{item}' not found in the list.")

def view_list():
    if not shopping_list:
        print("Shopping list is empty!")
    else:
        print("\nYour shopping list:")
        for i, item in enumerate(shopping_list, 1):
            print(f"  {i}. {item}")

def clear_list():
    shopping_list.clear()
    print("Shopping list cleared!")

# Main program
while True:
    show_menu()
    choice = input("\nEnter your choice (1-5): ")

    if choice == '1':
        add_item()
    elif choice == '2':
        remove_item()
    elif choice == '3':
        view_list()
    elif choice == '4':
        clear_list()
    elif choice == '5':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
```

### Exercise 5: Student Grade Calculator

```python
def calculate_grade(scores):
    """Calculate average and letter grade from a list of scores."""
    if not scores:
        return None, "No scores provided"

    average = sum(scores) / len(scores)

    if average >= 90:
        letter = 'A'
    elif average >= 80:
        letter = 'B'
    elif average >= 70:
        letter = 'C'
    elif average >= 60:
        letter = 'D'
    else:
        letter = 'F'

    return average, letter

# Get student scores
student_name = input("Enter student name: ")
scores = []

print("Enter scores (type 'done' when finished):")
while True:
    entry = input("Score: ")
    if entry.lower() == 'done':
        break
    try:
        score = float(entry)
        if 0 <= score <= 100:
            scores.append(score)
        else:
            print("Score must be between 0 and 100")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Calculate and display results
average, grade = calculate_grade(scores)
if average:
    print(f"\n--- Results for {student_name} ---")
    print(f"Scores: {scores}")
    print(f"Average: {average:.2f}")
    print(f"Letter Grade: {grade}")
```

---

## Summary

Congratulations! You've completed Chapter 1. You now know:

- What programming is and why we use it
- How to install Python and set up an IDE
- Variables and data types
- Operators and expressions
- Control flow (if-else statements)
- Loops (for and while)
- Functions
- Lists and dictionaries
- File handling
- Error handling

### Next Steps

1. Practice the exercises multiple times
2. Modify the examples and experiment
3. Build small projects on your own
4. Move on to [Chapter 2: Database Fundamentals](../Database/chapter-2-database-fundamentals.md)

---

## Quick Reference

```python
# Variables
name = "value"
number = 42

# Print
print("Hello")
print(f"Name: {name}")

# Input
user_input = input("Enter: ")

# If-else
if condition:
    # code
elif other_condition:
    # code
else:
    # code

# For loop
for i in range(5):
    # code

# While loop
while condition:
    # code

# Function
def function_name(param):
    return result

# List
my_list = [1, 2, 3]
my_list.append(4)

# Dictionary
my_dict = {"key": "value"}
my_dict["new_key"] = "new_value"

# File handling
with open("file.txt", "r") as f:
    content = f.read()

# Error handling
try:
    # risky code
except ExceptionType:
    # handle error
```

---

[← Back to Main Guide](../README.md) | [Next: Chapter 2 - Database Fundamentals →](../Database/chapter-2-database-fundamentals.md)
