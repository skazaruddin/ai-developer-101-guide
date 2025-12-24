# Chapter 5: OpenAI API with Python

## Building AI-Powered Applications

---

## Table of Contents

1. [What is an API Key?](#what-is-an-api-key)
2. [Getting Your OpenAI API Key](#getting-your-openai-api-key)
3. [Setting Up Your Environment](#setting-up-your-environment)
4. [Your First API Call](#your-first-api-call)
5. [Understanding the Response](#understanding-the-response)
6. [Chat Completions API](#chat-completions-api)
7. [Working with Roles](#working-with-roles)
8. [Parameters and Options](#parameters-and-options)
9. [Streaming Responses](#streaming-responses)
10. [Error Handling](#error-handling)
11. [Practical Examples](#practical-examples)
12. [Best Practices](#best-practices)

---

## What is an API Key?

### The Simple Explanation

An **API key** is like a password that:
1. **Identifies** who you are
2. **Authorizes** you to use the service
3. **Tracks** your usage for billing

Think of it like a library card - it identifies you and lets you borrow books (make API calls), and the library tracks how many books you've borrowed (usage/billing).

### Why You Need an API Key

```
Without API Key:
Your App → OpenAI API → "Who are you? Access denied!"

With API Key:
Your App + API Key → OpenAI API → "Welcome! Here's your response."
```

### Security Warning

**NEVER share your API key publicly!**

```python
# BAD - Don't do this!
api_key = "sk-abc123xyz789..."  # Hardcoded in code

# GOOD - Use environment variables
import os
api_key = os.getenv("OPENAI_API_KEY")
```

---

## Getting Your OpenAI API Key

### Step-by-Step Guide

#### Step 1: Create an OpenAI Account

1. Go to [platform.openai.com](https://platform.openai.com)
2. Click "Sign up"
3. Create an account (email or Google/Microsoft sign-in)
4. Verify your email

#### Step 2: Add Payment Method

1. Go to [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
2. Click "Add payment method"
3. Add a credit card
4. Set a usage limit (recommended: start with $10-20)

#### Step 3: Generate API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Give it a name (e.g., "My First App")
4. **Copy the key immediately** (you can't see it again!)
5. Store it securely

### API Key Format

```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- Starts with `sk-` (secret key)
- Followed by project identifier
- Long random string

---

## Setting Up Your Environment

### Installing the OpenAI SDK

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install OpenAI SDK
pip install openai

# Install python-dotenv for environment variables
pip install python-dotenv
```

### Setting Up Environment Variables

Create a `.env` file in your project root:

```
# .env
OPENAI_API_KEY=sk-proj-your-key-here
```

**Add `.env` to `.gitignore`**:
```
# .gitignore
.env
```

### Loading the API Key

```python
# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set!")
```

---

## Your First API Call

### The Simplest Example

```python
# first_call.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Make a simple API call
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Using the cost-effective model
    messages=[
        {"role": "user", "content": "Hello! What is 2 + 2?"}
    ]
)

# Print the response
print(response.choices[0].message.content)
```

**Output:**
```
2 + 2 equals 4.
```

### Running the Code

```bash
python first_call.py
```

Congratulations! You just made your first AI API call!

---

## Understanding the Response

### The Response Object

When you make an API call, you get back a response object:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)

# The full response looks like this:
print(response)
```

```python
ChatCompletion(
    id='chatcmpl-abc123',
    choices=[
        Choice(
            finish_reason='stop',
            index=0,
            message=ChatCompletionMessage(
                content='Hello! How can I help you today?',
                role='assistant'
            )
        )
    ],
    created=1705678901,
    model='gpt-4o-mini',
    object='chat.completion',
    usage=CompletionUsage(
        completion_tokens=9,
        prompt_tokens=10,
        total_tokens=19
    )
)
```

### Accessing Response Data

```python
# Get the main response text
message = response.choices[0].message.content
print(f"Response: {message}")

# Get the model used
model = response.model
print(f"Model: {model}")

# Get token usage (for cost tracking)
usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Get finish reason
finish_reason = response.choices[0].finish_reason
print(f"Finish reason: {finish_reason}")  # 'stop', 'length', etc.
```

---

## Chat Completions API

### The Message Format

The Chat API uses a **conversation format** with messages:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "How do I install it?"}
]
```

### Building a Conversation

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Start a conversation
conversation = [
    {"role": "system", "content": "You are a helpful coding tutor."}
]

def chat(user_message):
    """Send a message and get a response."""
    # Add user message to conversation
    conversation.append({"role": "user", "content": user_message})

    # Make API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )

    # Get assistant response
    assistant_message = response.choices[0].message.content

    # Add assistant response to conversation (for memory)
    conversation.append({"role": "assistant", "content": assistant_message})

    return assistant_message

# Have a conversation
print(chat("What is a variable in Python?"))
print("\n" + "="*50 + "\n")
print(chat("Can you show me an example?"))
print("\n" + "="*50 + "\n")
print(chat("What about data types?"))
```

---

## Working with Roles

### The Three Roles

| Role | Purpose | Example |
|------|---------|---------|
| `system` | Sets behavior/personality | "You are a helpful assistant" |
| `user` | The human's messages | "What is Python?" |
| `assistant` | The AI's responses | "Python is a programming language..." |

### System Message Examples

```python
# Technical expert
system_prompt = """You are a senior software engineer with 20 years of experience.
You explain technical concepts clearly and provide practical examples.
You always consider best practices and potential pitfalls."""

# Creative writer
system_prompt = """You are a creative writing assistant.
You help users write engaging stories, poems, and creative content.
Your writing is vivid, imaginative, and emotionally resonant."""

# Customer support
system_prompt = """You are a friendly customer support agent for TechStore.
You help customers with product questions, orders, and returns.
Always be polite, patient, and solution-oriented."""

# Code reviewer
system_prompt = """You are an expert code reviewer.
When given code, you:
1. Identify bugs and issues
2. Suggest improvements
3. Rate code quality (1-10)
4. Provide refactored version if needed"""
```

### Using System Messages Effectively

```python
def create_specialized_chat(persona):
    """Create a chatbot with a specific persona."""
    return [{"role": "system", "content": persona}]

# Create different specialized assistants
code_tutor = create_specialized_chat(
    "You are a patient Python tutor for beginners. "
    "Explain concepts simply and provide examples."
)

translator = create_specialized_chat(
    "You are a translator. Translate text between languages. "
    "Preserve meaning and tone. Format: '[Language]: translation'"
)

summarizer = create_specialized_chat(
    "You are a summarization expert. "
    "Provide concise summaries in bullet points."
)
```

---

## Parameters and Options

### Key Parameters

```python
response = client.chat.completions.create(
    # Required
    model="gpt-4o-mini",              # Which model to use
    messages=[...],                    # The conversation

    # Optional - Control output
    temperature=0.7,                   # Creativity (0=focused, 2=random)
    max_tokens=500,                    # Maximum response length
    top_p=1.0,                         # Nucleus sampling
    frequency_penalty=0.0,             # Reduce repetition
    presence_penalty=0.0,              # Encourage new topics

    # Optional - Control behavior
    n=1,                               # Number of responses to generate
    stop=["END", "###"],               # Stop sequences
    stream=False,                      # Stream response?
)
```

### Temperature: Controlling Creativity

```python
# Temperature examples

# Low temperature (0.0-0.3): More focused, deterministic
# Good for: Code generation, factual Q&A, structured output
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    temperature=0.0  # Always gives "4"
)

# Medium temperature (0.5-0.7): Balanced
# Good for: General conversation, explanations
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain gravity"}],
    temperature=0.7
)

# High temperature (0.8-1.5): More creative, varied
# Good for: Creative writing, brainstorming
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a haiku about coding"}],
    temperature=1.2
)
```

### Max Tokens: Controlling Length

```python
# Short response (for quick answers)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is Python?"}],
    max_tokens=50  # ~1-2 sentences
)

# Medium response (for explanations)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain Python in detail"}],
    max_tokens=500  # ~1-2 paragraphs
)

# Long response (for detailed content)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a tutorial on Python basics"}],
    max_tokens=2000  # Multiple sections
)
```

---

## Streaming Responses

### Why Streaming?

Without streaming: Wait for entire response → Display all at once (slow feeling)
With streaming: Display text as it's generated → Feels faster and more interactive

### Implementing Streaming

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a streaming response
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Tell me a short story about a robot."}],
    stream=True  # Enable streaming
)

# Print as chunks arrive
print("Response: ", end="")
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()  # New line at the end
```

### Collecting Streamed Response

```python
def stream_chat(messages):
    """Stream a chat response and return the full text."""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    full_response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="", flush=True)
            full_response += content

    print()
    return full_response

# Usage
messages = [{"role": "user", "content": "Explain machine learning briefly."}]
response = stream_chat(messages)
```

---

## Error Handling

### Common Errors

```python
from openai import OpenAI, APIError, RateLimitError, AuthenticationError
import os
import time
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def safe_chat(messages, max_retries=3):
    """Make an API call with error handling."""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content

        except AuthenticationError:
            # Invalid API key
            print("Error: Invalid API key. Check your OPENAI_API_KEY.")
            raise

        except RateLimitError:
            # Too many requests
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

        except APIError as e:
            # General API error
            print(f"API Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                raise

        except Exception as e:
            # Unexpected error
            print(f"Unexpected error: {e}")
            raise

    return None

# Usage
try:
    result = safe_chat([{"role": "user", "content": "Hello!"}])
    print(result)
except Exception as e:
    print(f"Failed after retries: {e}")
```

### Handling Token Limits

```python
def count_tokens_estimate(text):
    """Rough estimate: ~4 characters per token."""
    return len(text) // 4

def truncate_messages(messages, max_tokens=4000):
    """Truncate conversation to fit within token limit."""
    # Keep system message
    system_msg = [m for m in messages if m["role"] == "system"]
    other_msgs = [m for m in messages if m["role"] != "system"]

    # Count tokens
    total = sum(count_tokens_estimate(m["content"]) for m in messages)

    # Remove old messages if over limit
    while total > max_tokens and len(other_msgs) > 1:
        removed = other_msgs.pop(0)  # Remove oldest
        total -= count_tokens_estimate(removed["content"])

    return system_msg + other_msgs
```

---

## Practical Examples

### Example 1: Simple Q&A Bot

```python
# qa_bot.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_question(question):
    """Ask a question and get an answer."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Give concise, accurate answers."},
            {"role": "user", "content": question}
        ],
        temperature=0.3  # More focused for factual answers
    )
    return response.choices[0].message.content

# Test it
questions = [
    "What is the capital of France?",
    "Who wrote Romeo and Juliet?",
    "What is photosynthesis?"
]

for q in questions:
    print(f"Q: {q}")
    print(f"A: {ask_question(q)}")
    print()
```

### Example 2: Code Generator

```python
# code_generator.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_code(task, language="python"):
    """Generate code for a given task."""
    system_prompt = f"""You are an expert {language} programmer.
Generate clean, well-commented code for the given task.
Include example usage if appropriate.
Only output the code, no explanations before or after."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ],
        temperature=0.2  # Low temperature for consistent code
    )
    return response.choices[0].message.content

# Generate some code
task = "Create a function that calculates the factorial of a number"
code = generate_code(task)
print(code)
```

### Example 3: Text Summarizer

```python
# summarizer.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize(text, style="bullet_points"):
    """Summarize text in different styles."""
    styles = {
        "bullet_points": "Summarize in 3-5 bullet points.",
        "one_sentence": "Summarize in one sentence.",
        "paragraph": "Summarize in a short paragraph.",
        "eli5": "Explain like I'm 5 years old."
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a summarization expert. {styles.get(style, styles['bullet_points'])}"},
            {"role": "user", "content": f"Summarize this:\n\n{text}"}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

# Test with a long text
article = """
Artificial intelligence (AI) is transforming industries worldwide. Machine learning,
a subset of AI, enables computers to learn from data without being explicitly programmed.
Deep learning, which uses neural networks with many layers, has achieved remarkable results
in image recognition, natural language processing, and game playing. Companies are investing
billions in AI research, hoping to automate tasks, improve decision-making, and create new
products. However, AI also raises concerns about job displacement, privacy, and the ethical
use of autonomous systems. Researchers are working on making AI more transparent, fair, and
aligned with human values.
"""

print("=== Bullet Points ===")
print(summarize(article, "bullet_points"))
print("\n=== One Sentence ===")
print(summarize(article, "one_sentence"))
print("\n=== ELI5 ===")
print(summarize(article, "eli5"))
```

### Example 4: Interactive Chatbot

```python
# chatbot.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Chatbot:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.conversation = [
            {"role": "system", "content": system_prompt}
        ]

    def chat(self, user_input):
        """Send a message and get a response."""
        self.conversation.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.conversation,
            temperature=0.7
        )

        assistant_message = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def clear_history(self):
        """Clear conversation history (keep system prompt)."""
        self.conversation = [self.conversation[0]]

def main():
    """Interactive chat loop."""
    print("Chatbot initialized. Type 'quit' to exit, 'clear' to reset.")
    print("-" * 50)

    bot = Chatbot("You are a friendly and helpful assistant. Be conversational.")

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        if user_input.lower() == 'clear':
            bot.clear_history()
            print("Conversation cleared.")
            continue

        response = bot.chat(user_input)
        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main()
```

---

## Best Practices

### 1. Secure Your API Key

```python
# DO: Use environment variables
import os
api_key = os.getenv("OPENAI_API_KEY")

# DON'T: Hardcode keys
api_key = "sk-..."  # NEVER DO THIS
```

### 2. Handle Errors Gracefully

```python
# DO: Handle specific exceptions
try:
    response = client.chat.completions.create(...)
except RateLimitError:
    time.sleep(60)  # Wait and retry
except AuthenticationError:
    log.error("Invalid API key")
```

### 3. Monitor Usage and Costs

```python
# Track token usage
response = client.chat.completions.create(...)
tokens_used = response.usage.total_tokens
cost = tokens_used * 0.00001  # Approximate cost per token

# Log for monitoring
print(f"Tokens: {tokens_used}, Estimated cost: ${cost:.6f}")
```

### 4. Use Appropriate Models

```python
# Simple tasks → cheaper model
response = client.chat.completions.create(model="gpt-4o-mini", ...)

# Complex tasks → smarter model
response = client.chat.completions.create(model="gpt-4o", ...)
```

### 5. Craft Good Prompts

```python
# DO: Be specific and clear
system = """You are a Python code reviewer.
For each code snippet:
1. List any bugs
2. Suggest improvements
3. Rate quality 1-10
4. Provide fixed version"""

# DON'T: Be vague
system = "Review code"  # Too vague
```

### 6. Manage Conversation Length

```python
# Trim old messages to stay within limits
MAX_MESSAGES = 20
if len(conversation) > MAX_MESSAGES:
    # Keep system message and recent messages
    conversation = [conversation[0]] + conversation[-MAX_MESSAGES:]
```

---

## Summary

You've learned:

1. **API Keys**: How to get and securely use them
2. **OpenAI SDK**: Installing and configuring the Python client
3. **Chat Completions**: Making API calls and understanding responses
4. **Roles**: Using system, user, and assistant messages
5. **Parameters**: Controlling temperature, tokens, and other settings
6. **Streaming**: Real-time response delivery
7. **Error Handling**: Dealing with rate limits and errors
8. **Practical Applications**: Building chatbots, code generators, and more

### Next Steps

1. Experiment with different prompts and parameters
2. Build your own chatbot or tool
3. Try different models (GPT-4o for complex tasks)
4. Move on to [Chapter 6: Knowledge Bases & Vector Databases](../Vector-DB/chapter-6-knowledge-bases-embeddings.md)

---

[← Previous: Chapter 4 - Language Models](../AI-Models/chapter-4-language-models.md) | [Back to Main Guide](../README.md) | [Next: Chapter 6 - Knowledge Bases →](../Vector-DB/chapter-6-knowledge-bases-embeddings.md)
