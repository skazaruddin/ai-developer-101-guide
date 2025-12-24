"""
Python 101 - Example 4: Loops
Repeating actions efficiently.
"""

# For loop with range
print("Counting from 0 to 4:")
for i in range(5):
    print(i)

print("\n" + "-" * 30 + "\n")

# For loop with a list
fruits = ["apple", "banana", "cherry", "date"]
print("My favorite fruits:")
for fruit in fruits:
    print(f"  - {fruit}")

print("\n" + "-" * 30 + "\n")

# For loop with range(start, stop, step)
print("Even numbers from 0 to 10:")
for i in range(0, 11, 2):
    print(i, end=" ")
print()

print("\n" + "-" * 30 + "\n")

# While loop
count = 5
print("Countdown:")
while count > 0:
    print(count)
    count -= 1
print("Blast off!")

print("\n" + "-" * 30 + "\n")

# Loop with break
print("Finding first number divisible by 7:")
for num in range(1, 100):
    if num % 7 == 0:
        print(f"Found it: {num}")
        break

print("\n" + "-" * 30 + "\n")

# Loop with continue
print("Odd numbers from 1 to 10:")
for i in range(1, 11):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i, end=" ")
print()

print("\n" + "-" * 30 + "\n")

# Nested loops - multiplication table
print("Multiplication table (1-5):")
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:3}", end=" ")
    print()
