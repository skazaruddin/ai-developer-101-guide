# Chapter 6: Knowledge Bases & Vector Databases

## Making AI Smarter with Your Own Data

---

## Table of Contents

1. [The Problem: LLMs Don't Know Your Data](#the-problem-llms-dont-know-your-data)
2. [What is a Knowledge Base?](#what-is-a-knowledge-base)
3. [What are Embeddings?](#what-are-embeddings)
4. [How Embeddings Work](#how-embeddings-work)
5. [What is Semantic Search?](#what-is-semantic-search)
6. [Vector Databases](#vector-databases)
7. [Introduction to pgvector](#introduction-to-pgvector)
8. [Installing pgvector](#installing-pgvector)
9. [Creating Embeddings with OpenAI](#creating-embeddings-with-openai)
10. [Building a Knowledge Base](#building-a-knowledge-base)
11. [Semantic Search in Practice](#semantic-search-in-practice)
12. [Complete Example: Document Q&A System](#complete-example-document-qa-system)

---

## The Problem: LLMs Don't Know Your Data

### What LLMs Know

Large Language Models are trained on public internet data up to a certain date:

```
LLM Training Data:
├── Wikipedia
├── Books
├── News articles
├── Public websites
├── Open-source code
└── General knowledge

What LLMs DON'T know:
├── Your company's internal documents
├── Your product documentation
├── Your customer support tickets
├── Recent events after training
├── Private databases
└── Your personal files
```

### The Knowledge Gap

```
User: "What is our company's refund policy?"

LLM: "I don't have access to your company's specific policies.
      Generally, refund policies vary by company..."

User: "When was our last product launch?"

LLM: "I don't have information about your company's
      product launches..."
```

### The Solution: Knowledge Bases

```
Your Data → Embeddings → Vector Database
                              ↓
User Question → Semantic Search → Relevant Context
                              ↓
                    LLM + Context → Accurate Answer

User: "What is our company's refund policy?"

System: [Finds relevant policy document]

LLM: "According to your company policy, refunds are available
      within 30 days of purchase with original receipt..."
```

---

## What is a Knowledge Base?

### Simple Definition

A **knowledge base** is a collection of information that can be searched and retrieved to provide context to an AI system.

### Types of Knowledge Bases

```
Knowledge Base Types:
│
├── Document Store
│   └── PDFs, Word docs, text files
│
├── FAQ Database
│   └── Questions and answers
│
├── Wiki/Documentation
│   └── Technical docs, guides
│
├── Structured Data
│   └── Database records, spreadsheets
│
└── Conversation History
    └── Past chats, support tickets
```

### Traditional vs. Semantic Knowledge Base

| Traditional Search | Semantic Search |
|-------------------|-----------------|
| Keyword matching | Meaning matching |
| "refund policy" matches exact words | "money back guarantee" matches similar meaning |
| Limited to exact terms | Understands synonyms and context |
| Fast but limited | More accurate results |

---

## What are Embeddings?

### The Simple Explanation

An **embedding** is a way to convert text (or images, audio) into a list of numbers that captures its meaning.

```
Text: "The cat sat on the mat"
        ↓ (Embedding Model)
Embedding: [0.012, -0.034, 0.056, ..., 0.089]
           (1536 numbers for OpenAI's model)
```

### Why Numbers?

Computers understand numbers, not words. Embeddings let us:
1. **Compare** how similar two texts are
2. **Search** for related content
3. **Cluster** similar documents
4. **Store** meaning efficiently

### Key Insight: Similar Meaning = Close Numbers

```
"I love dogs"    → [0.8, 0.2, 0.5, ...]
"I adore puppies" → [0.78, 0.22, 0.48, ...]  ← Very close!
"I hate cats"    → [-0.3, 0.7, -0.2, ...]   ← Far away

"Bank" (financial) → [0.5, 0.3, 0.1, ...]
"Bank" (river)     → [-0.2, 0.8, 0.4, ...]  ← Different meaning, different embedding
```

---

## How Embeddings Work

### The Process

```
Step 1: Text Input
"How do I reset my password?"

Step 2: Tokenization
["How", "do", "I", "reset", "my", "password", "?"]

Step 3: Model Processing
Neural network processes tokens
Captures meaning, context, relationships

Step 4: Output Vector
[0.023, -0.045, 0.078, ..., 0.012]  (1536 dimensions)
```

### Visualizing Embeddings (Simplified to 2D)

```
                    Technology
                        ▲
                        │
    "Python code" ●     │     ● "JavaScript"
                        │
    "Programming" ●     │     ● "Software"
                        │
        ───────────────►─────────────────────► Food
                        │
    "Spaghetti" ●       │     ● "Pizza"
                        │
    "Pasta recipe" ●    │     ● "Italian food"
                        │
                        ▼
```

Similar concepts cluster together!

### Measuring Similarity: Cosine Distance

```
Cosine Similarity:
- 1.0 = Identical meaning
- 0.0 = Unrelated
- -1.0 = Opposite meaning

"happy" vs "joyful" → 0.92 (very similar)
"happy" vs "computer" → 0.12 (unrelated)
"happy" vs "sad" → -0.85 (opposite)
```

---

## What is Semantic Search?

### Traditional Keyword Search

```
Query: "laptop repair"

Document 1: "How to fix your laptop"           ❌ (no "repair")
Document 2: "Laptop repair service available"  ✓ (matches!)
Document 3: "Computer fixing and maintenance"  ❌ (no "laptop", "repair")
```

### Semantic Search

```
Query: "laptop repair"
Query Embedding: [0.45, 0.23, -0.12, ...]

Document 1: "How to fix your laptop"
Embedding: [0.44, 0.22, -0.11, ...]
Similarity: 0.96 ✓ (great match!)

Document 2: "Laptop repair service available"
Embedding: [0.43, 0.21, -0.13, ...]
Similarity: 0.94 ✓ (great match!)

Document 3: "Computer fixing and maintenance"
Embedding: [0.42, 0.24, -0.10, ...]
Similarity: 0.89 ✓ (good match!)
```

Semantic search understands that "fix", "repair", and "maintenance" are related!

### Benefits of Semantic Search

| Feature | Keyword Search | Semantic Search |
|---------|---------------|-----------------|
| Synonyms | ❌ | ✓ |
| Typos | ❌ | ✓ (somewhat) |
| Context | ❌ | ✓ |
| Multi-lingual | ❌ | ✓ (with right model) |
| Natural language | ❌ | ✓ |

---

## Vector Databases

### What is a Vector Database?

A **vector database** is a specialized database designed to store and search embeddings efficiently.

```
Traditional Database:
┌──────────────────────────────┐
│ id │ title        │ content  │
├────┼──────────────┼──────────┤
│ 1  │ "Doc A"      │ "..."    │
│ 2  │ "Doc B"      │ "..."    │
└──────────────────────────────┘
Search: WHERE title = "Doc A"

Vector Database:
┌─────────────────────────────────────────────────────┐
│ id │ title   │ content │ embedding                  │
├────┼─────────┼─────────┼────────────────────────────┤
│ 1  │ "Doc A" │ "..."   │ [0.1, 0.2, 0.3, ...]      │
│ 2  │ "Doc B" │ "..."   │ [0.4, 0.5, 0.6, ...]      │
└─────────────────────────────────────────────────────┘
Search: Find vectors closest to [0.15, 0.25, 0.35, ...]
```

### Popular Vector Databases

| Database | Type | Best For |
|----------|------|----------|
| **pgvector** | PostgreSQL extension | Teams already using PostgreSQL |
| **Pinecone** | Cloud-native | Serverless, fully managed |
| **Weaviate** | Open-source | Self-hosted, feature-rich |
| **Milvus** | Open-source | Large-scale deployments |
| **Chroma** | Open-source | Local development, prototyping |
| **Qdrant** | Open-source | High-performance search |

### Why pgvector?

```
Benefits of pgvector:
├── Uses familiar PostgreSQL
├── No new infrastructure needed
├── ACID transactions
├── Combine vector + regular queries
├── Free and open source
└── Easy to install
```

---

## Introduction to pgvector

### What is pgvector?

**pgvector** is a PostgreSQL extension that adds vector similarity search capabilities to your existing PostgreSQL database.

### Key Features

```
pgvector Capabilities:
├── Store embeddings as VECTOR type
├── Similarity search (L2, Inner Product, Cosine)
├── Indexing for fast search (IVFFlat, HNSW)
├── Combine with regular SQL
└── Scales to millions of vectors
```

### Vector Operations

```sql
-- Store vectors
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(1536)  -- 1536 dimensions for OpenAI
);

-- Find similar vectors (cosine distance)
SELECT content,
       1 - (embedding <=> query_vector) AS similarity
FROM documents
ORDER BY embedding <=> query_vector
LIMIT 5;
```

---

## Installing pgvector

### Option 1: Docker (Recommended for Learning)

```bash
# Pull PostgreSQL with pgvector
docker pull pgvector/pgvector:pg16

# Run the container
docker run -d \
  --name pgvector \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# Connect
psql -h localhost -U postgres
```

### Option 2: Install on Existing PostgreSQL

#### Ubuntu/Debian

```bash
# Install dependencies
sudo apt install postgresql-16-pgvector

# Or compile from source
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

#### macOS (Homebrew)

```bash
# Install PostgreSQL with pgvector
brew install postgresql
brew install pgvector
```

#### Windows

Download pre-built binaries from the [pgvector releases page](https://github.com/pgvector/pgvector/releases).

### Enable the Extension

```sql
-- Connect to your database
\c your_database

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify installation
SELECT * FROM pg_extension WHERE extname = 'vector';
```

---

## Creating Embeddings with OpenAI

### OpenAI Embedding Models

| Model | Dimensions | Best For |
|-------|------------|----------|
| text-embedding-3-small | 1536 | Cost-effective, most use cases |
| text-embedding-3-large | 3072 | Higher quality, more expensive |
| text-embedding-ada-002 | 1536 | Legacy model |

### Basic Embedding Creation

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    """Get embedding for a text string."""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

# Example
text = "How do I reset my password?"
embedding = get_embedding(text)
print(f"Embedding dimension: {len(embedding)}")  # 1536
print(f"First 5 values: {embedding[:5]}")
```

### Batch Embedding

```python
def get_embeddings_batch(texts: list, model: str = "text-embedding-3-small") -> list:
    """Get embeddings for multiple texts at once."""
    response = client.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]

# Example
documents = [
    "How do I reset my password?",
    "What are your business hours?",
    "How can I contact support?"
]
embeddings = get_embeddings_batch(documents)
print(f"Number of embeddings: {len(embeddings)}")
```

---

## Building a Knowledge Base

### Step 1: Create the Database Schema

```sql
-- Create the knowledge base table
CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT NOT NULL,
    source VARCHAR(255),
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index for fast similarity search
CREATE INDEX ON knowledge_base
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### Step 2: Python Setup

```python
# knowledge_base.py
import psycopg2
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'knowledge_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

def get_db_connection():
    """Create database connection."""
    return psycopg2.connect(**DB_CONFIG)

def get_embedding(text: str) -> list:
    """Get embedding for text."""
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
```

### Step 3: Add Documents

```python
def add_document(title: str, content: str, source: str = None):
    """Add a document to the knowledge base."""
    # Generate embedding
    embedding = get_embedding(content)

    # Store in database
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO knowledge_base (title, content, source, embedding)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (title, content, source, embedding))
            doc_id = cur.fetchone()[0]
            conn.commit()
            return doc_id
    finally:
        conn.close()

# Add sample documents
documents = [
    {
        "title": "Password Reset",
        "content": "To reset your password, click on 'Forgot Password' on the login page. Enter your email address and we'll send you a reset link. The link expires in 24 hours.",
        "source": "help/password.md"
    },
    {
        "title": "Business Hours",
        "content": "Our customer support is available Monday through Friday, 9 AM to 6 PM EST. On weekends, support is available via email only with a 24-hour response time.",
        "source": "help/hours.md"
    },
    {
        "title": "Refund Policy",
        "content": "We offer full refunds within 30 days of purchase. To request a refund, contact support with your order number. Refunds are processed within 5-7 business days.",
        "source": "policies/refund.md"
    }
]

for doc in documents:
    doc_id = add_document(doc["title"], doc["content"], doc["source"])
    print(f"Added: {doc['title']} (ID: {doc_id})")
```

### Step 4: Search the Knowledge Base

```python
def search_knowledge_base(query: str, limit: int = 5) -> list:
    """Search for similar documents."""
    # Generate query embedding
    query_embedding = get_embedding(query)

    # Search in database
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    id,
                    title,
                    content,
                    source,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM knowledge_base
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (query_embedding, query_embedding, limit))

            results = []
            for row in cur.fetchall():
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'source': row[3],
                    'similarity': float(row[4])
                })
            return results
    finally:
        conn.close()

# Search example
query = "How can I get my money back?"
results = search_knowledge_base(query)

print(f"\nSearch results for: '{query}'\n")
for result in results:
    print(f"Title: {result['title']}")
    print(f"Similarity: {result['similarity']:.2%}")
    print(f"Content: {result['content'][:100]}...")
    print()
```

---

## Semantic Search in Practice

### Handling Different Query Types

```python
# All these queries should find the password reset document:
queries = [
    "How do I reset my password?",      # Direct question
    "forgot password",                   # Keywords
    "can't log in need new password",   # Informal
    "I need to change my login credentials",  # Different wording
    "password recovery",                 # Technical term
]

for query in queries:
    results = search_knowledge_base(query, limit=1)
    if results:
        print(f"Query: '{query}'")
        print(f"Match: {results[0]['title']} ({results[0]['similarity']:.2%})")
        print()
```

### Filtering Results by Similarity Threshold

```python
def search_with_threshold(query: str, threshold: float = 0.7) -> list:
    """Search with minimum similarity threshold."""
    results = search_knowledge_base(query, limit=10)
    return [r for r in results if r['similarity'] >= threshold]

# Only return highly relevant results
results = search_with_threshold("refund process", threshold=0.75)
```

### Combining Vector and Traditional Search

```python
def hybrid_search(query: str, source_filter: str = None) -> list:
    """Combine semantic search with metadata filtering."""
    query_embedding = get_embedding(query)

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if source_filter:
                cur.execute("""
                    SELECT id, title, content, source,
                           1 - (embedding <=> %s::vector) AS similarity
                    FROM knowledge_base
                    WHERE source LIKE %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT 5
                """, (query_embedding, f"%{source_filter}%", query_embedding))
            else:
                cur.execute("""
                    SELECT id, title, content, source,
                           1 - (embedding <=> %s::vector) AS similarity
                    FROM knowledge_base
                    ORDER BY embedding <=> %s::vector
                    LIMIT 5
                """, (query_embedding, query_embedding))

            return cur.fetchall()
    finally:
        conn.close()

# Search only in help documents
results = hybrid_search("password", source_filter="help/")
```

---

## Complete Example: Document Q&A System

### Full Implementation

```python
# document_qa.py
"""
A complete document Q&A system using embeddings and pgvector.

This system:
1. Loads documents into a knowledge base
2. Searches for relevant documents using semantic search
3. Uses GPT to answer questions based on the context
"""

import psycopg2
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'knowledge_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}


class KnowledgeBase:
    """A knowledge base with semantic search capabilities."""

    def __init__(self):
        self.setup_database()

    def get_connection(self):
        return psycopg2.connect(**DB_CONFIG)

    def setup_database(self):
        """Create necessary tables and extensions."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Enable pgvector
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

                # Create table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255),
                        content TEXT NOT NULL,
                        metadata JSONB,
                        embedding VECTOR(1536),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Create index (if table has data)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS documents_embedding_idx
                    ON documents
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100)
                """)

                conn.commit()
        finally:
            conn.close()

    def get_embedding(self, text: str) -> list:
        """Generate embedding for text."""
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def add_document(self, title: str, content: str, metadata: dict = None) -> int:
        """Add a document to the knowledge base."""
        embedding = self.get_embedding(content)

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO documents (title, content, metadata, embedding)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (title, content, psycopg2.extras.Json(metadata), embedding))
                doc_id = cur.fetchone()[0]
                conn.commit()
                return doc_id
        finally:
            conn.close()

    def search(self, query: str, limit: int = 3) -> list:
        """Search for relevant documents."""
        query_embedding = self.get_embedding(query)

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        title,
                        content,
                        1 - (embedding <=> %s::vector) AS similarity
                    FROM documents
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """, (query_embedding, query_embedding, limit))

                return [
                    {
                        'title': row[0],
                        'content': row[1],
                        'similarity': float(row[2])
                    }
                    for row in cur.fetchall()
                ]
        finally:
            conn.close()


class DocumentQA:
    """Q&A system that uses the knowledge base to answer questions."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def answer_question(self, question: str) -> str:
        """Answer a question using the knowledge base."""
        # Search for relevant documents
        relevant_docs = self.kb.search(question, limit=3)

        if not relevant_docs:
            return "I couldn't find any relevant information to answer your question."

        # Build context from relevant documents
        context = "\n\n".join([
            f"Document: {doc['title']}\n{doc['content']}"
            for doc in relevant_docs
            if doc['similarity'] > 0.5  # Only use relevant docs
        ])

        if not context:
            return "I couldn't find any relevant information to answer your question."

        # Use GPT to answer based on context
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant that answers questions based on the provided context.
Only answer based on the information given in the context.
If the context doesn't contain the answer, say so.
Be concise and direct."""
                },
                {
                    "role": "user",
                    "content": f"""Context:
{context}

Question: {question}

Answer based only on the context provided:"""
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content


def main():
    """Demo the Document Q&A system."""
    print("=" * 60)
    print("  Document Q&A System")
    print("=" * 60)

    # Initialize knowledge base
    print("\nInitializing knowledge base...")
    kb = KnowledgeBase()

    # Add sample documents
    print("Adding sample documents...")
    documents = [
        {
            "title": "Password Reset Guide",
            "content": """To reset your password:
1. Go to the login page and click 'Forgot Password'
2. Enter your email address
3. Check your email for the reset link (expires in 24 hours)
4. Click the link and create a new password
5. Your password must be at least 8 characters with one number and one symbol"""
        },
        {
            "title": "Subscription Plans",
            "content": """We offer three subscription plans:
- Basic: $9.99/month - 5 projects, email support
- Pro: $24.99/month - Unlimited projects, priority support, advanced analytics
- Enterprise: Custom pricing - Custom integrations, dedicated support, SLA
All plans include a 14-day free trial. You can upgrade or downgrade anytime."""
        },
        {
            "title": "Data Export",
            "content": """You can export your data at any time:
1. Go to Settings > Data Management
2. Click 'Export Data'
3. Choose format: CSV, JSON, or PDF
4. Select date range and data types
5. Click 'Generate Export'
Your export will be ready within 24 hours and available for download for 7 days."""
        }
    ]

    for doc in documents:
        kb.add_document(doc["title"], doc["content"])
        print(f"  Added: {doc['title']}")

    # Create Q&A system
    qa = DocumentQA(kb)

    # Test questions
    print("\n" + "=" * 60)
    print("  Testing Q&A")
    print("=" * 60)

    questions = [
        "How do I change my password?",
        "What plans do you offer and how much do they cost?",
        "Can I download my data?",
        "What's the weather like today?"  # Not in knowledge base
    ]

    for question in questions:
        print(f"\nQ: {question}")
        answer = qa.answer_question(question)
        print(f"A: {answer}")


if __name__ == "__main__":
    # Need to import extras for Json
    import psycopg2.extras
    main()
```

---

## Summary

You've learned:

1. **Why Knowledge Bases Matter**: LLMs don't know your private data
2. **Embeddings**: Converting text to numbers that capture meaning
3. **Semantic Search**: Finding content by meaning, not just keywords
4. **Vector Databases**: Specialized storage for embeddings
5. **pgvector**: PostgreSQL extension for vector search
6. **Building a Knowledge Base**: From raw documents to searchable system
7. **Document Q&A**: Combining search with LLM for accurate answers

### Key Takeaways

- Embeddings capture **meaning** as numbers
- Similar meanings = **close vectors**
- pgvector adds vector search to PostgreSQL
- Combine **semantic search** with **LLM** for powerful Q&A

### Next Steps

1. Add more documents to your knowledge base
2. Experiment with different embedding models
3. Try hybrid search (vector + filters)
4. Move on to [Chapter 7: RAG](../RAG/chapter-7-rag.md) to build more sophisticated systems

---

[← Previous: Chapter 5 - OpenAI API](../OpenAI-API/chapter-5-openai-api.md) | [Back to Main Guide](../README.md) | [Next: Chapter 7 - RAG →](../RAG/chapter-7-rag.md)
