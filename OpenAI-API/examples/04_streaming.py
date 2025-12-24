"""
OpenAI API - Example 4: Streaming Responses
Demonstrates how to stream responses for a better user experience.

Streaming shows text as it's generated, making the app feel more responsive.
"""

from openai import OpenAI
import os
import sys
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def stream_response(prompt: str, system_prompt: str = None) -> str:
    """Stream a response and return the full text."""
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    # Create a streaming response
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    # Collect and print chunks as they arrive
    full_response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="", flush=True)
            full_response += content

    print()  # New line at the end
    return full_response


def stream_story():
    """Stream a creative story."""
    print("=" * 60)
    print("Streaming a Story...")
    print("=" * 60)
    print()

    system = "You are a creative storyteller. Write engaging, vivid stories."
    prompt = "Tell me a short story about a robot who learns to paint."

    stream_response(prompt, system)


def stream_code_explanation():
    """Stream a code explanation."""
    print("=" * 60)
    print("Streaming a Code Explanation...")
    print("=" * 60)
    print()

    code = """
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
"""

    system = "You are a patient coding tutor. Explain code clearly."
    prompt = f"Explain this JavaScript code step by step:\n\n```javascript\n{code}\n```"

    stream_response(prompt, system)


def interactive_stream():
    """Interactive streaming chat."""
    print("=" * 60)
    print("Interactive Streaming Chat")
    print("Type your message and see the response stream!")
    print("Type 'quit' to exit")
    print("=" * 60)

    system = "You are a helpful assistant. Be conversational and friendly."

    while True:
        print()
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        print("\nAssistant: ", end="")
        stream_response(user_input, system)


def main():
    """Run all streaming demos."""
    print("\n" + "=" * 60)
    print("  OpenAI Streaming Demo")
    print("=" * 60 + "\n")

    # Demo 1: Stream a story
    stream_story()

    print("\n" + "-" * 60 + "\n")

    # Demo 2: Stream code explanation
    stream_code_explanation()

    print("\n" + "-" * 60 + "\n")

    # Demo 3: Interactive streaming
    print("Would you like to try interactive streaming? (y/n): ", end="")
    if input().strip().lower() == 'y':
        interactive_stream()


if __name__ == "__main__":
    main()
