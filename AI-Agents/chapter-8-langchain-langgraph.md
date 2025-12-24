# Chapter 8: AI Agents with LangChain & LangGraph

## Building Intelligent Autonomous Systems

---

## Table of Contents

1. [What is an AI Agent?](#what-is-an-ai-agent)
2. [Agent vs Chatbot](#agent-vs-chatbot)
3. [Agent Architecture](#agent-architecture)
4. [Introduction to LangChain](#introduction-to-langchain)
5. [Tools and Function Calling](#tools-and-function-calling)
6. [Building Your First Agent](#building-your-first-agent)
7. [Introduction to LangGraph](#introduction-to-langgraph)
8. [Agent Workflows](#agent-workflows)
9. [Reflection and Self-Correction](#reflection-and-self-correction)
10. [Context Engineering](#context-engineering)
11. [Multi-Agent Systems](#multi-agent-systems)
12. [Best Practices](#best-practices)

---

## What is an AI Agent?

### The Simple Definition

An **AI Agent** is an autonomous system that can:
1. **Perceive** - Understand its environment and inputs
2. **Reason** - Think about what to do
3. **Act** - Take actions to achieve goals
4. **Learn** - Improve from feedback

### Agent vs Simple LLM

```
Simple LLM:
User: "What's the weather in Paris?"
LLM: "I don't have access to real-time weather data."

AI Agent:
User: "What's the weather in Paris?"
Agent: [Thinks: "I need current weather data"]
       [Action: Calls weather API for Paris]
       [Response: "It's currently 18°C and sunny in Paris!"]
```

### The Agent Loop

```
                    ┌─────────────────┐
                    │   User Goal     │
                    │ "Plan my trip"  │
                    └────────┬────────┘
                             │
                             ▼
         ┌──────────────────────────────────────┐
         │                                      │
    ┌────┴────┐                           ┌────┴────┐
    │ OBSERVE │◄──────────────────────────┤   ACT   │
    │ (Input) │                           │ (Tools) │
    └────┬────┘                           └────▲────┘
         │                                     │
         ▼                                     │
    ┌─────────┐      ┌─────────────┐          │
    │  THINK  │─────►│   DECIDE    │──────────┘
    │ (LLM)   │      │ (Reasoning) │
    └─────────┘      └─────────────┘
         │
         ▼
    ┌─────────────┐
    │   REFLECT   │ ──► Is the goal achieved?
    └─────────────┘     If no, loop again
```

---

## Agent vs Chatbot

### Key Differences

| Aspect | Chatbot | AI Agent |
|--------|---------|----------|
| **Autonomy** | Responds to prompts | Takes initiative |
| **Actions** | Text only | Uses tools |
| **Planning** | None | Multi-step |
| **Memory** | Limited | Persistent |
| **Goals** | Answer questions | Complete tasks |

### Chatbot Example

```
User: "Book a flight to Tokyo"
Chatbot: "I can't book flights. Here's how to do it:
         1. Go to airline website
         2. Enter your dates
         3. ..."
```

### Agent Example

```
User: "Book a flight to Tokyo"
Agent: [Searches for available flights]
       [Compares prices and schedules]
       [Selects best option based on preferences]
       [Makes booking through API]
       "Done! I've booked your flight to Tokyo:
        - JL001, March 15, 9:00 AM
        - Non-stop, 12h 30m
        - $850
        Confirmation sent to your email."
```

---

## Agent Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                        AI AGENT                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                       BRAIN                           │   │
│  │                   (Large Language Model)              │   │
│  │                                                       │   │
│  │  • Reasoning and planning                             │   │
│  │  • Decision making                                    │   │
│  │  • Natural language understanding                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│          ┌────────────────┼────────────────┐                │
│          │                │                │                 │
│          ▼                ▼                ▼                 │
│  ┌───────────────┐ ┌───────────┐ ┌────────────────┐         │
│  │    MEMORY     │ │   TOOLS   │ │   KNOWLEDGE    │         │
│  │               │ │           │ │     BASE       │         │
│  │ • Short-term  │ │ • Search  │ │                │         │
│  │ • Long-term   │ │ • APIs    │ │ • Documents    │         │
│  │ • Context     │ │ • Code    │ │ • Vectors      │         │
│  └───────────────┘ │ • Actions │ │ • RAG          │         │
│                    └───────────┘ └────────────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Types of Agents

#### 1. ReAct Agent (Reasoning + Acting)

```
Thought: I need to find the weather
Action: call weather_api("Paris")
Observation: {"temp": 18, "condition": "sunny"}
Thought: I have the weather data
Action: respond("It's 18°C and sunny in Paris")
```

#### 2. Plan-and-Execute Agent

```
Plan:
1. Search for flight options
2. Compare prices
3. Check user preferences
4. Book the best option
5. Send confirmation

Execute: [Runs each step in order]
```

#### 3. Reflexion Agent

```
Action: [Attempts task]
Reflection: "That didn't work because..."
Improved Action: [Tries again with improvements]
```

---

## Introduction to LangChain

### What is LangChain?

**LangChain** is a framework for building applications powered by language models. It provides:
- Modular components for LLM applications
- Easy integration with many LLM providers
- Tools for building agents
- Memory management
- Document loading and processing

### Installing LangChain

```bash
pip install langchain langchain-openai langchain-community
```

### Basic LangChain Usage

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize the model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Simple chat
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?")
]

response = llm.invoke(messages)
print(response.content)
```

### LangChain Components

```
LangChain
├── Models
│   ├── ChatOpenAI (OpenAI)
│   ├── ChatAnthropic (Claude)
│   └── ChatGoogleGenerativeAI (Gemini)
│
├── Prompts
│   ├── ChatPromptTemplate
│   └── PromptTemplate
│
├── Chains
│   ├── LLMChain
│   ├── SequentialChain
│   └── RouterChain
│
├── Memory
│   ├── ConversationBufferMemory
│   ├── ConversationSummaryMemory
│   └── VectorStoreMemory
│
├── Agents
│   ├── Tool-using agents
│   └── Custom agents
│
└── Tools
    ├── Search tools
    ├── API tools
    └── Custom tools
```

---

## Tools and Function Calling

### What are Tools?

**Tools** are functions that an agent can call to interact with the external world.

```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # Simulated weather API call
    weather_data = {
        "Paris": "18°C, Sunny",
        "London": "12°C, Cloudy",
        "Tokyo": "22°C, Clear"
    }
    return weather_data.get(city, "Weather data not available")

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    # Simulated search
    return f"Search results for: {query}"
```

### OpenAI Function Calling

```python
from openai import OpenAI

client = OpenAI()

# Define functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Use function calling
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

# Check if a function was called
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments
    print(f"Function: {function_name}")
    print(f"Arguments: {arguments}")
```

---

## Building Your First Agent

### Simple ReAct Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain import hub

# Define tools
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    weather_data = {
        "Paris": "18°C, Sunny",
        "London": "12°C, Cloudy",
        "Tokyo": "22°C, Clear"
    }
    return weather_data.get(city, f"Weather for {city}: 20°C, Partly cloudy")

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for '{query}': Found relevant information..."

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except:
        return "Could not calculate"

# Create the agent
tools = [get_weather, search, calculate]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Get the ReAct prompt
prompt = hub.pull("hwchase17/react")

# Create the agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent
result = agent_executor.invoke({
    "input": "What's the weather in Paris and what is 25 * 4?"
})
print(result["output"])
```

### Custom Agent from Scratch

```python
from openai import OpenAI
import json

client = OpenAI()

class SimpleAgent:
    """A simple agent that can use tools."""

    def __init__(self, tools: list, model: str = "gpt-4o-mini"):
        self.tools = {tool.__name__: tool for tool in tools}
        self.model = model
        self.tool_schemas = self._build_tool_schemas()

    def _build_tool_schemas(self) -> list:
        """Build OpenAI function schemas from tools."""
        schemas = []
        for name, func in self.tools.items():
            schema = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or "",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            schemas.append(schema)
        return schemas

    def run(self, query: str, max_iterations: int = 5) -> str:
        """Run the agent loop."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant with access to tools."},
            {"role": "user", "content": query}
        ]

        for _ in range(max_iterations):
            # Get LLM response
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tool_schemas if self.tool_schemas else None,
                tool_choice="auto" if self.tool_schemas else None
            )

            message = response.choices[0].message

            # If no tool call, we're done
            if not message.tool_calls:
                return message.content

            # Process tool calls
            messages.append(message)

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # Execute the tool
                if function_name in self.tools:
                    result = self.tools[function_name](**arguments)
                else:
                    result = f"Unknown tool: {function_name}"

                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        return "Max iterations reached"

# Usage
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 20°C, Sunny"

def calculate(expression: str) -> str:
    """Calculate a math expression."""
    return str(eval(expression))

agent = SimpleAgent([get_weather, calculate])
result = agent.run("What's the weather in Tokyo and what is 100 / 5?")
print(result)
```

---

## Introduction to LangGraph

### What is LangGraph?

**LangGraph** is a library for building stateful, multi-step agent applications. It models agent workflows as **graphs** where:
- **Nodes** = Processing steps (LLM calls, tool calls, etc.)
- **Edges** = Transitions between steps
- **State** = Information passed between nodes

### Why LangGraph?

```
LangChain Agents:
├── Good for simple tool use
├── Limited control flow
└── Hard to debug complex logic

LangGraph:
├── Full control over agent flow
├── Supports complex workflows
├── Built-in state management
├── Easy to visualize and debug
└── Supports human-in-the-loop
```

### Installing LangGraph

```bash
pip install langgraph
```

### LangGraph Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                       LANGGRAPH                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
│  │  START   │────►│  Node 1  │────►│  Node 2  │             │
│  └──────────┘     └──────────┘     └────┬─────┘             │
│                                         │                    │
│                        ┌────────────────┼────────────────┐   │
│                        │                │                │   │
│                        ▼                ▼                ▼   │
│                   ┌─────────┐     ┌─────────┐     ┌─────────┐│
│                   │ Node 3a │     │ Node 3b │     │   END   ││
│                   └────┬────┘     └────┬────┘     └─────────┘│
│                        │                │                    │
│                        └────────┬───────┘                    │
│                                 │                            │
│                                 ▼                            │
│                            ┌─────────┐                       │
│                            │   END   │                       │
│                            └─────────┘                       │
│                                                              │
│  State flows through the graph, modified by each node        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Workflows

### Basic LangGraph Agent

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Define state
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_action: str

# Define nodes
def analyze_input(state: AgentState) -> AgentState:
    """Analyze the user input and decide next action."""
    messages = state["messages"]
    last_message = messages[-1]["content"]

    if "weather" in last_message.lower():
        next_action = "get_weather"
    elif "calculate" in last_message.lower():
        next_action = "calculate"
    else:
        next_action = "respond"

    return {"messages": [], "next_action": next_action}

def get_weather_node(state: AgentState) -> AgentState:
    """Get weather information."""
    return {
        "messages": [{"role": "assistant", "content": "The weather is 20°C and sunny."}],
        "next_action": "end"
    }

def calculate_node(state: AgentState) -> AgentState:
    """Perform calculation."""
    return {
        "messages": [{"role": "assistant", "content": "The result is 42."}],
        "next_action": "end"
    }

def respond_node(state: AgentState) -> AgentState:
    """Generate a general response."""
    return {
        "messages": [{"role": "assistant", "content": "I'm here to help!"}],
        "next_action": "end"
    }

# Define routing
def route_action(state: AgentState) -> str:
    return state["next_action"]

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze", analyze_input)
workflow.add_node("get_weather", get_weather_node)
workflow.add_node("calculate", calculate_node)
workflow.add_node("respond", respond_node)

# Add edges
workflow.set_entry_point("analyze")
workflow.add_conditional_edges(
    "analyze",
    route_action,
    {
        "get_weather": "get_weather",
        "calculate": "calculate",
        "respond": "respond"
    }
)
workflow.add_edge("get_weather", END)
workflow.add_edge("calculate", END)
workflow.add_edge("respond", END)

# Compile
app = workflow.compile()

# Run
result = app.invoke({
    "messages": [{"role": "user", "content": "What's the weather?"}],
    "next_action": ""
})
print(result["messages"])
```

---

## Reflection and Self-Correction

### What is Reflection?

**Reflection** is when an agent evaluates its own outputs and improves them.

```
┌─────────────────────────────────────────────────────────────┐
│                    REFLECTION LOOP                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────┐     ┌───────────┐     ┌───────────────────┐  │
│  │  Generate │────►│  Reflect  │────►│ Good enough?      │  │
│  │  Response │     │  on Output│     │                   │  │
│  └───────────┘     └───────────┘     └─────────┬─────────┘  │
│       ▲                                        │             │
│       │                               ┌────────┴────────┐    │
│       │                               │                 │    │
│       │                               ▼                 ▼    │
│       │                         ┌─────────┐       ┌─────────┐│
│       │                         │   No    │       │   Yes   ││
│       │                         │ Improve │       │  Done   ││
│       │                         └────┬────┘       └─────────┘│
│       │                              │                       │
│       └──────────────────────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Implementing Reflection

```python
from openai import OpenAI

client = OpenAI()

def generate_with_reflection(task: str, max_reflections: int = 3) -> str:
    """Generate content with self-reflection and improvement."""

    # Initial generation
    initial_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": task}
        ]
    ).choices[0].message.content

    current_response = initial_response

    for i in range(max_reflections):
        # Reflect on the response
        reflection = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are a critical reviewer.
Analyze the response and identify:
1. Factual errors
2. Missing information
3. Areas for improvement
4. Overall quality (1-10)

Be specific and constructive."""},
                {"role": "user", "content": f"""Task: {task}

Response:
{current_response}

Provide your critique:"""}
            ]
        ).choices[0].message.content

        # Check if quality is good enough
        if "quality: 8" in reflection.lower() or "quality: 9" in reflection.lower() or "quality: 10" in reflection.lower():
            break

        # Improve based on reflection
        improved = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Improve the response based on the feedback."},
                {"role": "user", "content": f"""Original task: {task}

Current response:
{current_response}

Feedback:
{reflection}

Provide an improved response:"""}
            ]
        ).choices[0].message.content

        current_response = improved

    return current_response

# Usage
result = generate_with_reflection(
    "Explain how photosynthesis works in simple terms."
)
print(result)
```

---

## Context Engineering

### What is Context Engineering?

**Context Engineering** is the art and science of constructing the optimal context (system prompts, conversation history, retrieved documents, tool results) to get the best performance from an LLM.

### Why Context Engineering Matters in GenAI

```
Context Engineering = Prompt Engineering + Memory Management + RAG + Tool Results

┌─────────────────────────────────────────────────────────────┐
│                    LLM CONTEXT WINDOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ System Prompt                                          │ │
│  │ "You are a helpful travel assistant..."                │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Conversation History (summarized if long)              │ │
│  │ User: "I want to visit Paris"                          │ │
│  │ Assistant: "Great choice! When..."                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Retrieved Context (RAG)                                │ │
│  │ [Document: Paris travel guide...]                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Tool Results                                           │ │
│  │ [Weather API: 18°C, Sunny]                            │ │
│  │ [Flight API: $500, 7h]                                │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Current User Query                                     │ │
│  │ "What should I pack?"                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Context Engineering Strategies

#### 1. Prioritize Relevant Context

```python
def build_context(
    query: str,
    conversation_history: list,
    retrieved_docs: list,
    tool_results: list,
    max_tokens: int = 4000
) -> str:
    """Build optimal context within token limits."""

    # Start with most recent, most relevant
    context_parts = []

    # Always include tool results (most recent actions)
    for result in tool_results[-3:]:  # Last 3 tool results
        context_parts.append(f"[Tool Result]: {result}")

    # Add retrieved documents (most relevant to current query)
    for doc in retrieved_docs[:3]:  # Top 3 documents
        context_parts.append(f"[Knowledge]: {doc}")

    # Add recent conversation (summarize if needed)
    if len(conversation_history) > 10:
        # Summarize older messages
        summary = summarize_conversation(conversation_history[:-5])
        context_parts.append(f"[Previous Context]: {summary}")
        # Keep recent messages verbatim
        for msg in conversation_history[-5:]:
            context_parts.append(f"{msg['role']}: {msg['content']}")
    else:
        for msg in conversation_history:
            context_parts.append(f"{msg['role']}: {msg['content']}")

    return "\n\n".join(context_parts)
```

#### 2. Dynamic System Prompts

```python
def build_system_prompt(user_intent: str, available_tools: list) -> str:
    """Build a system prompt based on user intent."""

    base_prompt = "You are a helpful AI assistant."

    intent_prompts = {
        "travel": """You are an expert travel planner.
Help users plan trips by:
- Suggesting destinations
- Finding flights and hotels
- Creating itineraries
- Providing local tips""",

        "coding": """You are an expert programmer.
Help users by:
- Writing clean, documented code
- Debugging issues
- Explaining concepts
- Following best practices""",

        "research": """You are a research assistant.
Help users by:
- Finding relevant information
- Summarizing documents
- Citing sources
- Answering questions accurately"""
    }

    prompt = intent_prompts.get(user_intent, base_prompt)

    # Add available tools
    tool_descriptions = "\n".join([f"- {t.name}: {t.description}" for t in available_tools])
    prompt += f"\n\nAvailable tools:\n{tool_descriptions}"

    return prompt
```

---

## Multi-Agent Systems

### When to Use Multiple Agents

```
Single Agent:
├── Simple, well-defined tasks
├── Limited scope
└── Quick responses needed

Multi-Agent:
├── Complex, multi-step tasks
├── Requires different expertise
├── Benefits from collaboration
└── Needs checks and balances
```

### Multi-Agent Patterns

#### 1. Supervisor Pattern

```
                    ┌───────────────┐
                    │  SUPERVISOR   │
                    │    Agent      │
                    └───────┬───────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  Research   │  │   Writer    │  │   Critic    │
    │   Agent     │  │   Agent     │  │   Agent     │
    └─────────────┘  └─────────────┘  └─────────────┘
```

#### 2. Debate Pattern

```
    ┌─────────────┐           ┌─────────────┐
    │   Agent A   │◄─────────►│   Agent B   │
    │  (Propose)  │  Debate   │  (Critique) │
    └──────┬──────┘           └──────┬──────┘
           │                         │
           └───────────┬─────────────┘
                       │
                       ▼
               ┌─────────────┐
               │    Judge    │
               │   Agent     │
               └─────────────┘
```

#### 3. Pipeline Pattern

```
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │  Research   │────►│   Draft     │────►│   Edit      │
    │   Agent     │     │   Agent     │     │   Agent     │
    └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Best Practices

### 1. Keep Agents Focused

```python
# BAD: One agent does everything
class DoEverythingAgent:
    def run(self, task):
        # 500 lines of code handling every case

# GOOD: Specialized agents
class ResearchAgent:
    """Finds and analyzes information."""
    pass

class WriterAgent:
    """Generates written content."""
    pass

class CoordinatorAgent:
    """Orchestrates other agents."""
    pass
```

### 2. Implement Guardrails

```python
def safe_tool_execution(tool, args, max_retries=3):
    """Execute a tool with safety checks."""
    # Validate inputs
    if not validate_inputs(args):
        return "Invalid inputs"

    # Rate limiting
    if rate_limit_exceeded(tool):
        return "Rate limit exceeded, try again later"

    # Execute with timeout
    for attempt in range(max_retries):
        try:
            result = execute_with_timeout(tool, args, timeout=30)
            return result
        except TimeoutError:
            continue
        except Exception as e:
            log_error(e)
            if attempt == max_retries - 1:
                return f"Tool execution failed: {e}"

    return "Max retries exceeded"
```

### 3. Log Everything

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent")

def agent_step(state):
    logger.info(f"Current state: {state}")
    logger.info(f"Deciding next action...")

    action = decide_action(state)
    logger.info(f"Chosen action: {action}")

    result = execute_action(action)
    logger.info(f"Action result: {result}")

    return result
```

### 4. Handle Failures Gracefully

```python
def robust_agent_run(agent, task, max_attempts=3):
    """Run an agent with failure handling."""
    for attempt in range(max_attempts):
        try:
            result = agent.run(task)

            # Validate result
            if is_valid_result(result):
                return result
            else:
                logger.warning(f"Invalid result on attempt {attempt + 1}")

        except Exception as e:
            logger.error(f"Error on attempt {attempt + 1}: {e}")

            if attempt < max_attempts - 1:
                # Maybe try a different approach
                task = modify_task_for_retry(task, e)

    return "Unable to complete task after multiple attempts"
```

---

## Summary

You've learned:

1. **What AI Agents are**: Autonomous systems that observe, think, act, and learn
2. **Agent Architecture**: Brain (LLM) + Memory + Tools + Knowledge
3. **LangChain**: Framework for building LLM applications
4. **Tools**: How agents interact with the external world
5. **LangGraph**: Building complex agent workflows as graphs
6. **Reflection**: Self-improvement through evaluation
7. **Context Engineering**: Optimizing LLM context for best results
8. **Multi-Agent Systems**: Collaboration patterns

### Next Steps

1. Build a simple tool-using agent
2. Implement reflection in your agent
3. Try LangGraph for complex workflows
4. Move on to [Chapter 9: Memory in AI Agents](./chapter-9-memory-in-agents.md)

---

[← Previous: Chapter 7 - RAG](../RAG/chapter-7-rag.md) | [Back to Main Guide](../README.md) | [Next: Chapter 9 - Memory →](./chapter-9-memory-in-agents.md)
