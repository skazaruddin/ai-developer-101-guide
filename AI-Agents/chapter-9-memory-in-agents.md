# Chapter 9: Memory in AI Agents

## Giving Agents the Ability to Remember

---

## Table of Contents

1. [Why Memory Matters](#why-memory-matters)
2. [Types of Memory](#types-of-memory)
3. [Short-Term Memory](#short-term-memory)
4. [Long-Term Memory](#long-term-memory)
5. [Episodic Memory](#episodic-memory)
6. [Semantic Memory](#semantic-memory)
7. [Working Memory](#working-memory)
8. [Implementing Memory Systems](#implementing-memory-systems)
9. [Memory Management Strategies](#memory-management-strategies)
10. [Practical Examples](#practical-examples)
11. [Best Practices](#best-practices)

---

## Why Memory Matters

### The Problem Without Memory

```
Session 1:
User: "My name is Alice and I love hiking."
Agent: "Nice to meet you, Alice! Hiking is wonderful."

Session 2:
User: "What outdoor activities would you recommend for me?"
Agent: "I'd be happy to help! What activities do you enjoy?"
       (Forgot Alice loves hiking!)
```

### The Power of Memory

```
Session 1:
User: "My name is Alice and I love hiking."
Agent: "Nice to meet you, Alice! I'll remember that you love hiking."
       [Saves to memory: user_name=Alice, interests=[hiking]]

Session 2:
User: "What outdoor activities would you recommend for me?"
Agent: [Retrieves memory: Alice likes hiking]
       "Hi Alice! Given your love for hiking, you might enjoy:
        - Trail running
        - Mountain biking
        - Rock climbing"
```

### Benefits of Memory

| Benefit | Description |
|---------|-------------|
| **Personalization** | Remember user preferences |
| **Continuity** | Maintain context across sessions |
| **Learning** | Improve from past interactions |
| **Efficiency** | Don't repeat conversations |
| **Trust** | Users feel understood |

---

## Types of Memory

### Human Memory Analogy

```
Human Memory                          AI Agent Memory
─────────────────                     ─────────────────
Sensory Memory ──────────────────────► Input Buffer
(Immediate perception)                 (Current message)

Short-Term Memory ───────────────────► Conversation Buffer
(Working memory, 7±2 items)            (Recent messages)

Long-Term Memory:
├── Episodic ────────────────────────► Interaction History
│   (Personal experiences)              (Past conversations)
│
├── Semantic ────────────────────────► Knowledge Base
│   (Facts and concepts)                (User preferences, facts)
│
└── Procedural ──────────────────────► Learned Behaviors
    (Skills, how to do things)          (Patterns, preferences)
```

### Memory in AI Agents

```
┌─────────────────────────────────────────────────────────────┐
│                    AI AGENT MEMORY SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │  SHORT-TERM      │  │  WORKING         │                 │
│  │  MEMORY          │  │  MEMORY          │                 │
│  │                  │  │                  │                 │
│  │  • Current       │  │  • Active task   │                 │
│  │    conversation  │  │    context       │                 │
│  │  • Recent        │  │  • Tool results  │                 │
│  │    messages      │  │  • Scratch pad   │                 │
│  └──────────────────┘  └──────────────────┘                 │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    LONG-TERM MEMORY                   │   │
│  │                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │   │
│  │  │  EPISODIC   │  │  SEMANTIC   │  │ PROCEDURAL  │   │   │
│  │  │             │  │             │  │             │   │   │
│  │  │  Past       │  │  Facts      │  │  Learned    │   │   │
│  │  │  sessions   │  │  Preferences│  │  patterns   │   │   │
│  │  │  Events     │  │  Knowledge  │  │  Skills     │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Short-Term Memory

### What is Short-Term Memory?

Short-term memory holds the current conversation context. It's what the agent "sees" in its context window.

### Implementation: Conversation Buffer

```python
class ConversationBufferMemory:
    """Simple conversation buffer that stores all messages."""

    def __init__(self, max_messages: int = 50):
        self.messages = []
        self.max_messages = max_messages

    def add_message(self, role: str, content: str):
        """Add a message to the buffer."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # Trim if over limit
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_messages(self) -> list:
        """Get all messages in the buffer."""
        return self.messages

    def get_context_string(self) -> str:
        """Get conversation as a formatted string."""
        lines = []
        for msg in self.messages:
            lines.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(lines)

    def clear(self):
        """Clear the buffer."""
        self.messages = []
```

### Implementation: Sliding Window Memory

```python
class SlidingWindowMemory:
    """Memory with a sliding window of recent messages."""

    def __init__(self, window_size: int = 10):
        self.messages = []
        self.window_size = window_size

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_window(self) -> list:
        """Get the most recent messages within the window."""
        return self.messages[-self.window_size:]

    def get_full_history(self) -> list:
        """Get complete conversation history."""
        return self.messages
```

### Implementation: Summary Memory

```python
from openai import OpenAI

client = OpenAI()

class SummaryMemory:
    """Memory that summarizes old conversations to save tokens."""

    def __init__(self, summary_threshold: int = 10):
        self.messages = []
        self.summary = ""
        self.summary_threshold = summary_threshold

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        # Summarize if too many messages
        if len(self.messages) > self.summary_threshold:
            self._create_summary()

    def _create_summary(self):
        """Summarize older messages."""
        # Get messages to summarize (keep last few)
        to_summarize = self.messages[:-3]
        to_keep = self.messages[-3:]

        # Create summary
        summary_prompt = f"""Summarize this conversation concisely:

{self._format_messages(to_summarize)}

Previous summary (if any): {self.summary}

Provide a brief summary of key points, user preferences, and important context:"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=200
        )

        self.summary = response.choices[0].message.content
        self.messages = to_keep

    def _format_messages(self, messages: list) -> str:
        return "\n".join([f"{m['role']}: {m['content']}" for m in messages])

    def get_context(self) -> str:
        """Get summary + recent messages for context."""
        context = ""
        if self.summary:
            context = f"Previous context: {self.summary}\n\n"
        context += "Recent conversation:\n"
        context += self._format_messages(self.messages)
        return context
```

---

## Long-Term Memory

### What is Long-Term Memory?

Long-term memory persists across sessions and conversations. It stores:
- User preferences
- Important facts
- Past interactions
- Learned patterns

### Implementation: Simple Persistent Memory

```python
import json
from pathlib import Path

class PersistentMemory:
    """Simple file-based persistent memory."""

    def __init__(self, file_path: str = "memory.json"):
        self.file_path = Path(file_path)
        self.data = self._load()

    def _load(self) -> dict:
        """Load memory from file."""
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {
            "user_info": {},
            "preferences": {},
            "facts": [],
            "interactions": []
        }

    def _save(self):
        """Save memory to file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def set_user_info(self, key: str, value: any):
        """Store user information."""
        self.data["user_info"][key] = value
        self._save()

    def get_user_info(self, key: str) -> any:
        """Retrieve user information."""
        return self.data["user_info"].get(key)

    def add_preference(self, category: str, preference: str):
        """Add a user preference."""
        if category not in self.data["preferences"]:
            self.data["preferences"][category] = []
        self.data["preferences"][category].append(preference)
        self._save()

    def get_preferences(self, category: str = None) -> dict:
        """Get user preferences."""
        if category:
            return self.data["preferences"].get(category, [])
        return self.data["preferences"]

    def add_fact(self, fact: str):
        """Store a fact about the user."""
        self.data["facts"].append({
            "fact": fact,
            "timestamp": datetime.now().isoformat()
        })
        self._save()

    def get_facts(self) -> list:
        """Get all stored facts."""
        return self.data["facts"]

    def log_interaction(self, summary: str):
        """Log a conversation summary."""
        self.data["interactions"].append({
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
```

### Implementation: Vector-Based Memory

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

class VectorMemory:
    """Memory that uses embeddings for semantic retrieval."""

    def __init__(self):
        self.memories = []  # List of (text, embedding, metadata)

    def get_embedding(self, text: str) -> list:
        """Get embedding for text."""
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def add_memory(self, content: str, metadata: dict = None):
        """Add a memory with its embedding."""
        embedding = self.get_embedding(content)
        self.memories.append({
            "content": content,
            "embedding": embedding,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })

    def search(self, query: str, top_k: int = 5) -> list:
        """Search for relevant memories."""
        if not self.memories:
            return []

        query_embedding = self.get_embedding(query)

        # Calculate similarities
        results = []
        for memory in self.memories:
            similarity = self._cosine_similarity(
                query_embedding,
                memory["embedding"]
            )
            results.append({
                "content": memory["content"],
                "similarity": similarity,
                "metadata": memory["metadata"]
            })

        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, a: list, b: list) -> float:
        """Calculate cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

---

## Episodic Memory

### What is Episodic Memory?

Episodic memory stores specific events and experiences - past conversations, user actions, and notable interactions.

### Implementation

```python
class EpisodicMemory:
    """Stores and retrieves past episodes/interactions."""

    def __init__(self, max_episodes: int = 100):
        self.episodes = []
        self.max_episodes = max_episodes

    def add_episode(
        self,
        summary: str,
        key_points: list,
        outcome: str = None,
        metadata: dict = None
    ):
        """Record an episode."""
        episode = {
            "id": len(self.episodes) + 1,
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "key_points": key_points,
            "outcome": outcome,
            "metadata": metadata or {}
        }
        self.episodes.append(episode)

        # Trim old episodes
        if len(self.episodes) > self.max_episodes:
            self.episodes = self.episodes[-self.max_episodes:]

    def get_recent_episodes(self, n: int = 5) -> list:
        """Get the most recent episodes."""
        return self.episodes[-n:]

    def search_episodes(self, keywords: list) -> list:
        """Search episodes by keywords."""
        results = []
        for episode in self.episodes:
            score = 0
            text = f"{episode['summary']} {' '.join(episode['key_points'])}"
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    score += 1
            if score > 0:
                results.append({"episode": episode, "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)
        return [r["episode"] for r in results]

    def get_similar_episodes(self, query: str, vector_memory: VectorMemory) -> list:
        """Find episodes similar to a query using embeddings."""
        # This would use vector similarity to find relevant past episodes
        pass
```

---

## Semantic Memory

### What is Semantic Memory?

Semantic memory stores facts, concepts, and general knowledge about the user and the world.

### Implementation

```python
class SemanticMemory:
    """Stores facts and knowledge."""

    def __init__(self):
        self.facts = {}  # category -> list of facts
        self.entities = {}  # entity_name -> attributes

    def add_fact(self, category: str, fact: str, confidence: float = 1.0):
        """Add a fact to a category."""
        if category not in self.facts:
            self.facts[category] = []

        self.facts[category].append({
            "fact": fact,
            "confidence": confidence,
            "added_at": datetime.now().isoformat()
        })

    def get_facts(self, category: str = None) -> list:
        """Get facts, optionally filtered by category."""
        if category:
            return self.facts.get(category, [])

        all_facts = []
        for cat_facts in self.facts.values():
            all_facts.extend(cat_facts)
        return all_facts

    def add_entity(self, name: str, entity_type: str, attributes: dict):
        """Add or update an entity."""
        self.entities[name] = {
            "type": entity_type,
            "attributes": attributes,
            "updated_at": datetime.now().isoformat()
        }

    def get_entity(self, name: str) -> dict:
        """Get an entity's information."""
        return self.entities.get(name)

    def update_entity(self, name: str, updates: dict):
        """Update an entity's attributes."""
        if name in self.entities:
            self.entities[name]["attributes"].update(updates)
            self.entities[name]["updated_at"] = datetime.now().isoformat()

# Usage Example
memory = SemanticMemory()

# Store facts about the user
memory.add_fact("preferences", "User prefers vegetarian food")
memory.add_fact("preferences", "User is allergic to peanuts")
memory.add_fact("travel", "User has visited Paris and Tokyo")

# Store entity information
memory.add_entity("User", "person", {
    "name": "Alice",
    "location": "New York",
    "occupation": "Software Engineer"
})
```

---

## Working Memory

### What is Working Memory?

Working memory holds the current task context, intermediate results, and active goals.

### Implementation

```python
class WorkingMemory:
    """Active memory for current task execution."""

    def __init__(self):
        self.current_goal = None
        self.sub_goals = []
        self.context = {}
        self.tool_results = []
        self.scratch_pad = []

    def set_goal(self, goal: str):
        """Set the current goal."""
        self.current_goal = goal
        self.sub_goals = []
        self.tool_results = []
        self.scratch_pad = []

    def add_sub_goal(self, sub_goal: str):
        """Add a sub-goal."""
        self.sub_goals.append({
            "goal": sub_goal,
            "status": "pending",
            "result": None
        })

    def complete_sub_goal(self, index: int, result: str):
        """Mark a sub-goal as complete."""
        if 0 <= index < len(self.sub_goals):
            self.sub_goals[index]["status"] = "completed"
            self.sub_goals[index]["result"] = result

    def add_context(self, key: str, value: any):
        """Add context information."""
        self.context[key] = value

    def add_tool_result(self, tool_name: str, result: any):
        """Store a tool execution result."""
        self.tool_results.append({
            "tool": tool_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

    def add_to_scratch_pad(self, note: str):
        """Add a note to the scratch pad."""
        self.scratch_pad.append(note)

    def get_state(self) -> dict:
        """Get the current working memory state."""
        return {
            "current_goal": self.current_goal,
            "sub_goals": self.sub_goals,
            "context": self.context,
            "tool_results": self.tool_results[-5:],  # Last 5 results
            "scratch_pad": self.scratch_pad[-10:]  # Last 10 notes
        }

    def clear(self):
        """Clear working memory (task complete)."""
        self.current_goal = None
        self.sub_goals = []
        self.context = {}
        self.tool_results = []
        self.scratch_pad = []
```

---

## Implementing Memory Systems

### Complete Memory System

```python
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import json

@dataclass
class MemoryItem:
    content: str
    memory_type: str
    metadata: dict
    timestamp: str
    importance: float = 0.5

class AgentMemorySystem:
    """Complete memory system for an AI agent."""

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id

        # Initialize memory components
        self.short_term = ConversationBufferMemory(max_messages=20)
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory(max_episodes=100)
        self.semantic = SemanticMemory()
        self.vector = VectorMemory()

    def process_user_message(self, message: str):
        """Process a user message and update memories."""
        # Add to short-term memory
        self.short_term.add_message("user", message)

        # Extract and store any facts
        facts = self._extract_facts(message)
        for fact in facts:
            self.semantic.add_fact(fact["category"], fact["content"])
            self.vector.add_memory(fact["content"], {"type": "fact"})

    def process_assistant_response(self, response: str):
        """Process an assistant response."""
        self.short_term.add_message("assistant", response)

    def end_conversation(self):
        """Called when a conversation ends. Consolidates memories."""
        # Create episode from conversation
        conversation = self.short_term.get_messages()
        if conversation:
            summary = self._summarize_conversation(conversation)
            key_points = self._extract_key_points(conversation)

            self.episodic.add_episode(
                summary=summary,
                key_points=key_points,
                outcome="conversation_ended"
            )

    def get_relevant_context(self, query: str) -> dict:
        """Get relevant context for a query."""
        context = {
            "recent_conversation": self.short_term.get_messages()[-10:],
            "relevant_memories": self.vector.search(query, top_k=3),
            "user_facts": self.semantic.get_facts()[:10],
            "recent_episodes": self.episodic.get_recent_episodes(3),
            "working_memory": self.working.get_state()
        }
        return context

    def format_context_for_llm(self, query: str) -> str:
        """Format memory context for inclusion in LLM prompt."""
        context = self.get_relevant_context(query)

        parts = []

        # User information
        user_info = self.semantic.get_entity("User")
        if user_info:
            parts.append(f"User Info: {json.dumps(user_info['attributes'])}")

        # Relevant memories
        if context["relevant_memories"]:
            memories = [m["content"] for m in context["relevant_memories"]]
            parts.append(f"Relevant Context: {'; '.join(memories)}")

        # User preferences/facts
        if context["user_facts"]:
            facts = [f["fact"] for f in context["user_facts"][:5]]
            parts.append(f"Known Facts: {'; '.join(facts)}")

        # Working memory (if active task)
        if context["working_memory"]["current_goal"]:
            parts.append(f"Current Goal: {context['working_memory']['current_goal']}")

        return "\n".join(parts)

    def _extract_facts(self, message: str) -> list:
        """Extract facts from a message (simplified)."""
        facts = []

        # Simple pattern matching (in real system, use NLP/LLM)
        if "my name is" in message.lower():
            name = message.split("my name is")[-1].strip().split()[0]
            facts.append({"category": "user_info", "content": f"User's name is {name}"})

        if "i like" in message.lower() or "i love" in message.lower():
            facts.append({"category": "preferences", "content": message})

        if "i work" in message.lower() or "my job" in message.lower():
            facts.append({"category": "work", "content": message})

        return facts

    def _summarize_conversation(self, conversation: list) -> str:
        """Summarize a conversation (use LLM in real implementation)."""
        if len(conversation) < 3:
            return "Brief conversation"
        return f"Conversation with {len(conversation)} messages"

    def _extract_key_points(self, conversation: list) -> list:
        """Extract key points from conversation."""
        # Simplified - in real system, use LLM
        return [msg["content"][:50] for msg in conversation[-3:]]
```

---

## Memory Management Strategies

### 1. Importance-Based Retention

```python
def calculate_importance(memory: MemoryItem) -> float:
    """Calculate importance score for a memory."""
    importance = 0.5  # Base score

    # Recency boost
    age_hours = (datetime.now() - datetime.fromisoformat(memory.timestamp)).total_seconds() / 3600
    recency_score = 1.0 / (1.0 + age_hours / 24)  # Decay over days
    importance += recency_score * 0.2

    # Emotional/personal content boost
    emotional_keywords = ["love", "hate", "important", "remember", "never forget"]
    if any(kw in memory.content.lower() for kw in emotional_keywords):
        importance += 0.2

    # Accessed frequently boost
    importance += min(memory.metadata.get("access_count", 0) * 0.05, 0.2)

    return min(importance, 1.0)
```

### 2. Memory Consolidation

```python
def consolidate_memories(memories: list, threshold: int = 100) -> list:
    """Consolidate similar memories to reduce storage."""
    if len(memories) < threshold:
        return memories

    # Group similar memories
    clusters = cluster_similar_memories(memories)

    consolidated = []
    for cluster in clusters:
        if len(cluster) == 1:
            consolidated.append(cluster[0])
        else:
            # Merge similar memories
            merged = merge_memories(cluster)
            consolidated.append(merged)

    return consolidated
```

### 3. Adaptive Context Window

```python
def build_adaptive_context(
    query: str,
    memories: list,
    max_tokens: int = 2000
) -> str:
    """Build context that adapts to available token budget."""
    # Score and sort memories by relevance to query
    scored = []
    for memory in memories:
        score = calculate_relevance(query, memory)
        scored.append((score, memory))

    scored.sort(reverse=True)

    # Build context within token limit
    context_parts = []
    current_tokens = 0

    for score, memory in scored:
        memory_tokens = estimate_tokens(memory.content)

        if current_tokens + memory_tokens <= max_tokens:
            context_parts.append(memory.content)
            current_tokens += memory_tokens
        else:
            break

    return "\n---\n".join(context_parts)
```

---

## Practical Examples

### Example 1: Personal Assistant with Memory

```python
from openai import OpenAI
from datetime import datetime

client = OpenAI()

class PersonalAssistant:
    """AI assistant with memory capabilities."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory = AgentMemorySystem(user_id)

    def chat(self, user_message: str) -> str:
        """Process user message and generate response."""
        # Update memory with user message
        self.memory.process_user_message(user_message)

        # Get relevant context
        context = self.memory.format_context_for_llm(user_message)

        # Generate response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a helpful personal assistant with memory.
You remember information about the user from previous conversations.

{context}

Use this context to provide personalized responses.
If you learn new information about the user, acknowledge it."""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        assistant_response = response.choices[0].message.content

        # Update memory with response
        self.memory.process_assistant_response(assistant_response)

        return assistant_response

# Usage
assistant = PersonalAssistant("user_123")

# Conversation 1
print(assistant.chat("Hi! My name is Alice and I work as a data scientist."))
print(assistant.chat("I'm planning to learn machine learning this year."))

# Later conversation - assistant remembers!
print(assistant.chat("What should I focus on for my career?"))
# Response will reference that Alice is a data scientist interested in ML
```

### Example 2: Learning Agent

```python
class LearningAgent:
    """Agent that learns from interactions."""

    def __init__(self):
        self.memory = AgentMemorySystem()
        self.learned_patterns = {}

    def learn_from_feedback(self, action: str, feedback: str, success: bool):
        """Learn from user feedback on actions."""
        # Store the experience
        self.memory.episodic.add_episode(
            summary=f"Action: {action}",
            key_points=[f"Feedback: {feedback}"],
            outcome="success" if success else "failure"
        )

        # Update patterns
        if action not in self.learned_patterns:
            self.learned_patterns[action] = {"success": 0, "failure": 0}

        if success:
            self.learned_patterns[action]["success"] += 1
        else:
            self.learned_patterns[action]["failure"] += 1

    def should_try_action(self, action: str) -> bool:
        """Decide whether to try an action based on past experience."""
        if action not in self.learned_patterns:
            return True  # Try new actions

        stats = self.learned_patterns[action]
        total = stats["success"] + stats["failure"]

        if total < 3:
            return True  # Not enough data

        success_rate = stats["success"] / total
        return success_rate > 0.5
```

---

## Best Practices

### 1. Separate Memory Types

```python
# GOOD: Separate memory systems for different purposes
class Agent:
    def __init__(self):
        self.conversation_memory = ConversationBuffer()  # Current chat
        self.user_memory = SemanticMemory()  # User facts
        self.experience_memory = EpisodicMemory()  # Past sessions

# BAD: One giant memory blob
class Agent:
    def __init__(self):
        self.memory = []  # Everything in one list
```

### 2. Implement Memory Hygiene

```python
def cleanup_old_memories(memory_system, days_old: int = 30):
    """Remove old, unimportant memories."""
    cutoff = datetime.now() - timedelta(days=days_old)

    # Keep important memories regardless of age
    memory_system.memories = [
        m for m in memory_system.memories
        if m.importance > 0.8 or
           datetime.fromisoformat(m.timestamp) > cutoff
    ]
```

### 3. Privacy Considerations

```python
class PrivacyAwareMemory:
    """Memory system with privacy controls."""

    SENSITIVE_CATEGORIES = ["financial", "health", "passwords"]

    def add_memory(self, content: str, category: str):
        if category in self.SENSITIVE_CATEGORIES:
            # Encrypt or don't store
            content = self._anonymize(content)

        # Store with expiration
        self.memories.append({
            "content": content,
            "category": category,
            "expires_at": self._get_expiration(category)
        })

    def _get_expiration(self, category: str) -> str:
        if category in self.SENSITIVE_CATEGORIES:
            return (datetime.now() + timedelta(days=1)).isoformat()
        return (datetime.now() + timedelta(days=365)).isoformat()
```

---

## Summary

You've learned:

1. **Why memory matters**: Continuity, personalization, learning
2. **Types of memory**: Short-term, long-term, episodic, semantic, working
3. **Short-term memory**: Conversation buffers, sliding windows, summaries
4. **Long-term memory**: Persistent storage, vector-based retrieval
5. **Memory management**: Importance scoring, consolidation, adaptive context
6. **Implementation patterns**: Practical code for memory systems

### Key Takeaways

- Different memory types serve different purposes
- Use vector embeddings for semantic retrieval
- Consolidate memories to manage storage
- Consider privacy when storing user data
- Memory enables personalized, continuous experiences

### Next Steps

1. Implement a basic memory system for your agent
2. Add vector-based semantic memory
3. Build a learning agent that improves from feedback
4. Move on to [Chapter 10: Travel Assistant Project](../Projects/travel-assistant/README.md)

---

[← Previous: Chapter 8 - AI Agents](./chapter-8-langchain-langgraph.md) | [Back to Main Guide](../README.md) | [Next: Chapter 10 - Travel Assistant →](../Projects/travel-assistant/README.md)
