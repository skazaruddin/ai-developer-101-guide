"""
OpenAI API - Example 2: Interactive Chatbot
A simple chatbot that maintains conversation history.

Usage:
- Type your message and press Enter
- Type 'quit' to exit
- Type 'clear' to reset conversation
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatBot:
    """A simple chatbot with conversation memory."""

    def __init__(self, system_prompt: str = None):
        """Initialize the chatbot with an optional system prompt."""
        default_prompt = (
            "You are a helpful, friendly assistant. "
            "You provide clear and concise answers. "
            "You ask clarifying questions when needed."
        )
        self.system_prompt = system_prompt or default_prompt
        self.conversation = [
            {"role": "system", "content": self.system_prompt}
        ]

    def chat(self, user_message: str) -> str:
        """Send a message and get a response."""
        # Add user message to conversation
        self.conversation.append({
            "role": "user",
            "content": user_message
        })

        # Make API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.conversation,
            temperature=0.7
        )

        # Extract assistant's response
        assistant_message = response.choices[0].message.content

        # Add to conversation history
        self.conversation.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def clear_history(self):
        """Clear conversation history but keep system prompt."""
        self.conversation = [
            {"role": "system", "content": self.system_prompt}
        ]

    def get_conversation_length(self) -> int:
        """Get the number of messages in the conversation."""
        return len(self.conversation)


def main():
    """Run the interactive chatbot."""
    print("=" * 60)
    print("  ChatBot - Powered by OpenAI GPT-4o-mini")
    print("=" * 60)
    print("Commands:")
    print("  - Type your message to chat")
    print("  - 'quit' or 'exit' to end")
    print("  - 'clear' to reset conversation")
    print("  - 'history' to see conversation length")
    print("=" * 60)

    # Initialize chatbot
    bot = ChatBot()

    while True:
        # Get user input
        print()
        user_input = input("You: ").strip()

        # Handle empty input
        if not user_input:
            continue

        # Handle commands
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye! Have a great day!")
            break

        if user_input.lower() == 'clear':
            bot.clear_history()
            print("\n[Conversation cleared]")
            continue

        if user_input.lower() == 'history':
            print(f"\n[Conversation has {bot.get_conversation_length()} messages]")
            continue

        # Get response from chatbot
        try:
            response = bot.chat(user_input)
            print(f"\nAssistant: {response}")
        except Exception as e:
            print(f"\n[Error: {e}]")


if __name__ == "__main__":
    main()
