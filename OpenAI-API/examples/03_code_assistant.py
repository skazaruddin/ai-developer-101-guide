"""
OpenAI API - Example 3: Code Assistant
An AI assistant specialized for coding tasks.

Features:
- Code generation
- Code explanation
- Code review
- Bug fixing
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_code(task: str, language: str = "python") -> str:
    """Generate code for a given task."""
    system_prompt = f"""You are an expert {language} programmer.
Generate clean, well-documented code for the given task.
Include:
- Clear comments explaining the code
- Example usage
- Handle edge cases

Output ONLY the code, no additional explanations."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ],
        temperature=0.2  # Low temperature for consistent code
    )

    return response.choices[0].message.content


def explain_code(code: str) -> str:
    """Explain what a piece of code does."""
    system_prompt = """You are a patient coding tutor.
Explain the given code in simple terms:
1. What does it do overall?
2. Explain each major section
3. Highlight any important patterns or techniques

Make it understandable for beginners."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Explain this code:\n\n```\n{code}\n```"}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


def review_code(code: str) -> str:
    """Review code and suggest improvements."""
    system_prompt = """You are a senior code reviewer.
Review the given code and provide:
1. Overall quality rating (1-10)
2. List of issues/bugs found
3. Suggestions for improvement
4. Security concerns (if any)
5. Refactored version (if needed)

Be constructive and specific."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Review this code:\n\n```\n{code}\n```"}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def fix_bug(code: str, error_message: str = None) -> str:
    """Fix bugs in code."""
    system_prompt = """You are an expert debugger.
Analyze the code for bugs and fix them:
1. Identify the bug(s)
2. Explain what's wrong
3. Provide the fixed code
4. Explain the fix"""

    user_content = f"Fix the bugs in this code:\n\n```\n{code}\n```"
    if error_message:
        user_content += f"\n\nError message: {error_message}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


def main():
    """Demo the code assistant."""
    print("=" * 60)
    print("  Code Assistant Demo")
    print("=" * 60)

    # Demo 1: Generate code
    print("\n" + "=" * 60)
    print("DEMO 1: Generate Code")
    print("=" * 60)
    task = "Create a function that checks if a string is a palindrome"
    print(f"Task: {task}\n")
    code = generate_code(task)
    print(code)

    # Demo 2: Explain code
    print("\n" + "=" * 60)
    print("DEMO 2: Explain Code")
    print("=" * 60)
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    print(f"Code to explain:\n{sample_code}")
    print("\nExplanation:")
    print(explain_code(sample_code))

    # Demo 3: Review code
    print("\n" + "=" * 60)
    print("DEMO 3: Review Code")
    print("=" * 60)
    code_to_review = """
def get_user_data(id):
    query = "SELECT * FROM users WHERE id = " + str(id)
    result = database.execute(query)
    return result
"""
    print(f"Code to review:\n{code_to_review}")
    print("\nReview:")
    print(review_code(code_to_review))

    # Demo 4: Fix bug
    print("\n" + "=" * 60)
    print("DEMO 4: Fix Bug")
    print("=" * 60)
    buggy_code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# This crashes with empty list
result = calculate_average([])
"""
    print(f"Buggy code:\n{buggy_code}")
    print("\nFix:")
    print(fix_bug(buggy_code, "ZeroDivisionError: division by zero"))


if __name__ == "__main__":
    main()
