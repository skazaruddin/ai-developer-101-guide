"""
OpenAI API - Example 1: Your First API Call
This script demonstrates the simplest way to call the OpenAI API.

Before running:
1. Install: pip install openai python-dotenv
2. Create a .env file with: OPENAI_API_KEY=sk-your-key-here
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Make a simple API call
print("Making API call...")
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Cost-effective model
    messages=[
        {"role": "user", "content": "Hello! What is 2 + 2?"}
    ]
)

# Print the response
print("\n" + "=" * 50)
print("RESPONSE:")
print("=" * 50)
print(response.choices[0].message.content)

# Print usage info
print("\n" + "=" * 50)
print("USAGE INFO:")
print("=" * 50)
print(f"Model: {response.model}")
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Completion tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
