"""
Python 101 - Example 6: Lists and Dictionaries
Working with collections of data.
"""

# ===== LISTS =====
print("=" * 40)
print("LISTS")
print("=" * 40)

# Creating and accessing lists
fruits = ["apple", "banana", "cherry", "date"]
print(f"Fruits: {fruits}")
print(f"First fruit: {fruits[0]}")
print(f"Last fruit: {fruits[-1]}")
print(f"First three: {fruits[:3]}")

print("-" * 30)

# Modifying lists
fruits.append("elderberry")  # Add to end
print(f"After append: {fruits}")

fruits.insert(1, "avocado")  # Insert at position
print(f"After insert: {fruits}")

fruits.remove("banana")  # Remove by value
print(f"After remove: {fruits}")

popped = fruits.pop()  # Remove and return last item
print(f"Popped: {popped}")
print(f"After pop: {fruits}")

print("-" * 30)

# List operations
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Numbers: {numbers}")
print(f"Length: {len(numbers)}")
print(f"Sum: {sum(numbers)}")
print(f"Min: {min(numbers)}")
print(f"Max: {max(numbers)}")

numbers.sort()
print(f"Sorted: {numbers}")

numbers.reverse()
print(f"Reversed: {numbers}")

print("-" * 30)

# List comprehension
squares = [x**2 for x in range(1, 6)]
print(f"Squares of 1-5: {squares}")

even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"Squares of even numbers 1-10: {even_squares}")

# ===== DICTIONARIES =====
print("\n" + "=" * 40)
print("DICTIONARIES")
print("=" * 40)

# Creating and accessing dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "job": "Engineer"
}

print(f"Person: {person}")
print(f"Name: {person['name']}")
print(f"Age: {person.get('age')}")
print(f"Country (with default): {person.get('country', 'Unknown')}")

print("-" * 30)

# Modifying dictionaries
person["email"] = "alice@example.com"  # Add new key
person["age"] = 31  # Update existing key
print(f"Updated person: {person}")

del person["job"]  # Remove key
print(f"After deletion: {person}")

print("-" * 30)

# Looping through dictionaries
print("Person details:")
for key, value in person.items():
    print(f"  {key}: {value}")

print("-" * 30)

# Nested data structures
students = [
    {"name": "Alice", "grade": 92},
    {"name": "Bob", "grade": 85},
    {"name": "Charlie", "grade": 78}
]

print("Student grades:")
for student in students:
    print(f"  {student['name']}: {student['grade']}")

# Calculate average
average = sum(s["grade"] for s in students) / len(students)
print(f"Class average: {average:.1f}")
