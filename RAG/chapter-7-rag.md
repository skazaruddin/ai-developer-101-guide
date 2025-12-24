# Chapter 7: RAG - Retrieval Augmented Generation

## Supercharging LLMs with Your Data

---

## Table of Contents

1. [What is RAG?](#what-is-rag)
2. [Why RAG Matters](#why-rag-matters)
3. [How RAG Works](#how-rag-works)
4. [RAG Architecture](#rag-architecture)
5. [Building a RAG Pipeline](#building-a-rag-pipeline)
6. [Chunking Strategies](#chunking-strategies)
7. [Retrieval Strategies](#retrieval-strategies)
8. [Prompt Engineering for RAG](#prompt-engineering-for-rag)
9. [Evaluating RAG Systems](#evaluating-rag-systems)
10. [Complete RAG Implementation](#complete-rag-implementation)
11. [Best Practices](#best-practices)

---

## What is RAG?

### The Simple Explanation

**RAG (Retrieval Augmented Generation)** is a technique that makes AI smarter by giving it access to external knowledge at the time of answering.

Think of it like an open-book exam:
- **Without RAG**: The AI answers from memory only (what it learned during training)
- **With RAG**: The AI can look up relevant information before answering

### The RAG Process

```
User Question: "What's our refund policy?"
           │
           ▼
    ┌──────────────┐
    │   RETRIEVE   │  ──► Search knowledge base
    └──────────────┘      Find relevant documents
           │
           ▼
    ┌──────────────┐
    │   AUGMENT    │  ──► Add retrieved info to prompt
    └──────────────┘      "Based on this context..."
           │
           ▼
    ┌──────────────┐
    │   GENERATE   │  ──► LLM generates answer
    └──────────────┘      using the context
           │
           ▼
    Answer: "Our refund policy allows returns within
            30 days with original receipt..."
```

### Key Insight

**RAG = Retrieval + Augmented + Generation**

| Component | What It Does |
|-----------|--------------|
| **Retrieval** | Find relevant documents from knowledge base |
| **Augmented** | Add documents as context to the prompt |
| **Generation** | LLM generates answer using the context |

---

## Why RAG Matters

### Problems with LLMs Alone

```
Problem 1: Knowledge Cutoff
┌────────────────────────────────────────────────┐
│ LLM Training: "I know things up to Jan 2024"   │
│ User: "What happened in the 2024 Olympics?"    │
│ LLM: "I don't have information about that."    │
└────────────────────────────────────────────────┘

Problem 2: Hallucination
┌────────────────────────────────────────────────┐
│ User: "What's Acme Corp's revenue?"            │
│ LLM: "Acme Corp's revenue is $5.2 billion"     │
│      (Completely made up!)                      │
└────────────────────────────────────────────────┘

Problem 3: Private Data
┌────────────────────────────────────────────────┐
│ User: "What's our company's vacation policy?"  │
│ LLM: "I don't have access to your company's    │
│       internal policies."                       │
└────────────────────────────────────────────────┘
```

### How RAG Solves These Problems

```
✓ Knowledge Cutoff
  → Retrieve from up-to-date database

✓ Hallucination
  → Ground answers in retrieved facts

✓ Private Data
  → Search your own knowledge base

✓ Source Attribution
  → Point to where the info came from

✓ Easy Updates
  → Just update the documents, no retraining
```

### RAG vs Fine-Tuning

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Cost** | Low (just vector DB) | High (GPU training) |
| **Updates** | Easy (add/remove docs) | Hard (retrain) |
| **Transparency** | High (see sources) | Low (black box) |
| **Accuracy** | Depends on retrieval | Can be very high |
| **Best for** | Q&A, search, dynamic data | Style, specific domains |

---

## How RAG Works

### Step-by-Step Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      INDEXING PHASE (Offline)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Documents ──► Chunk ──► Embed ──► Store in Vector DB           │
│                                                                  │
│  "Our refund policy..."  ──►  [0.12, -0.34, ...]  ──►  💾       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     RETRIEVAL PHASE (Online)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User asks: "How do I get a refund?"                         │
│                                                                  │
│  2. Embed query: [0.11, -0.32, ...]                             │
│                                                                  │
│  3. Search vector DB for similar embeddings                      │
│                                                                  │
│  4. Retrieve top K documents                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    GENERATION PHASE (Online)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  5. Build prompt with context:                                   │
│     "Based on the following documents:                           │
│      [Retrieved docs here]                                       │
│      Answer: How do I get a refund?"                            │
│                                                                  │
│  6. LLM generates grounded answer                                │
│                                                                  │
│  7. Return answer with sources                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The Math Behind It

```
Query Embedding:     Q = [0.1, 0.2, 0.3, ...]

Document Embeddings:
  D1 = [0.11, 0.21, 0.29, ...]  → Similarity: 0.95 ✓
  D2 = [-0.5, 0.8, -0.2, ...]   → Similarity: 0.23
  D3 = [0.15, 0.18, 0.32, ...]  → Similarity: 0.89 ✓

Retrieve D1, D3 (top 2 most similar)
```

---

## RAG Architecture

### Basic RAG System

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG SYSTEM                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Document   │    │   Embedding  │    │   Vector     │       │
│  │   Loader     │───►│   Model      │───►│   Database   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                    RETRIEVER                          │       │
│  │  Query → Embed → Search → Rank → Return Top K        │       │
│  └───────────────────────┬──────────────────────────────┘       │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                    GENERATOR                          │       │
│  │  Context + Query → LLM → Answer                       │       │
│  └───────────────────────────────────────────────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Components Explained

| Component | Purpose | Example Tools |
|-----------|---------|---------------|
| **Document Loader** | Ingest various file types | PyPDF, Unstructured |
| **Text Splitter** | Break docs into chunks | LangChain splitters |
| **Embedding Model** | Convert text to vectors | OpenAI, Sentence Transformers |
| **Vector Store** | Store and search vectors | pgvector, Pinecone, Chroma |
| **Retriever** | Find relevant documents | Similarity search |
| **LLM** | Generate final answer | GPT-4, Claude |

---

## Building a RAG Pipeline

### Step 1: Load Documents

```python
def load_documents(directory: str) -> list:
    """Load documents from a directory."""
    documents = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if filename.endswith('.txt'):
            with open(filepath, 'r') as f:
                content = f.read()
                documents.append({
                    'content': content,
                    'source': filename,
                    'type': 'text'
                })

        elif filename.endswith('.md'):
            with open(filepath, 'r') as f:
                content = f.read()
                documents.append({
                    'content': content,
                    'source': filename,
                    'type': 'markdown'
                })

    return documents
```

### Step 2: Chunk Documents

```python
def chunk_document(document: dict, chunk_size: int = 500, overlap: int = 50) -> list:
    """Split document into overlapping chunks."""
    content = document['content']
    chunks = []

    start = 0
    while start < len(content):
        end = start + chunk_size

        # Find a good breaking point (end of sentence or paragraph)
        if end < len(content):
            # Look for paragraph break
            para_break = content.rfind('\n\n', start, end)
            if para_break > start:
                end = para_break + 2
            else:
                # Look for sentence break
                for sep in ['. ', '! ', '? ', '\n']:
                    sent_break = content.rfind(sep, start, end)
                    if sent_break > start:
                        end = sent_break + len(sep)
                        break

        chunk_content = content[start:end].strip()
        if chunk_content:
            chunks.append({
                'content': chunk_content,
                'source': document['source'],
                'chunk_index': len(chunks)
            })

        start = end - overlap  # Overlap for context continuity

    return chunks
```

### Step 3: Create Embeddings and Store

```python
from openai import OpenAI
import psycopg2

client = OpenAI()

def embed_and_store(chunks: list, table_name: str = "documents"):
    """Generate embeddings and store in pgvector."""
    conn = get_db_connection()

    for chunk in chunks:
        # Generate embedding
        response = client.embeddings.create(
            input=chunk['content'],
            model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding

        # Store in database
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {table_name} (content, source, chunk_index, embedding)
                VALUES (%s, %s, %s, %s)
            """, (
                chunk['content'],
                chunk['source'],
                chunk['chunk_index'],
                embedding
            ))

    conn.commit()
    conn.close()
```

### Step 4: Retrieve Relevant Chunks

```python
def retrieve(query: str, top_k: int = 5) -> list:
    """Retrieve the most relevant document chunks."""
    # Embed the query
    response = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    query_embedding = response.data[0].embedding

    # Search in vector database
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT content, source, 1 - (embedding <=> %s::vector) as similarity
            FROM documents
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, top_k))

        results = [
            {'content': row[0], 'source': row[1], 'similarity': row[2]}
            for row in cur.fetchall()
        ]

    conn.close()
    return results
```

### Step 5: Generate Answer

```python
def generate_answer(query: str, context_docs: list) -> str:
    """Generate an answer using retrieved context."""
    # Build context string
    context = "\n\n---\n\n".join([
        f"Source: {doc['source']}\n{doc['content']}"
        for doc in context_docs
    ])

    # Create prompt
    messages = [
        {
            "role": "system",
            "content": """You are a helpful assistant that answers questions based on the provided context.
Rules:
1. Only answer based on the context provided
2. If the context doesn't contain the answer, say "I don't have enough information"
3. Cite sources when possible
4. Be concise and direct"""
        },
        {
            "role": "user",
            "content": f"""Context:
{context}

Question: {query}

Answer:"""
        }
    ]

    # Generate response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content
```

---

## Chunking Strategies

### Why Chunking Matters

```
Too Large Chunks:
├── Exceed context window
├── Less precise retrieval
└── Wasteful token usage

Too Small Chunks:
├── Lose context
├── Incomplete information
└── Require more retrievals

Just Right:
├── Fits context window
├── Contains complete thoughts
└── Efficient retrieval
```

### Common Chunking Strategies

#### 1. Fixed Size Chunking

```python
def fixed_size_chunks(text: str, size: int = 500, overlap: int = 50) -> list:
    """Split text into fixed-size chunks with overlap."""
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start += size - overlap

    return chunks
```

#### 2. Sentence-Based Chunking

```python
import re

def sentence_chunks(text: str, sentences_per_chunk: int = 5) -> list:
    """Split text into chunks by sentences."""
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Group sentences into chunks
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = ' '.join(sentences[i:i + sentences_per_chunk])
        chunks.append(chunk)

    return chunks
```

#### 3. Semantic Chunking

```python
def semantic_chunks(text: str, max_tokens: int = 200) -> list:
    """Split text at natural boundaries (paragraphs, sections)."""
    # Split by paragraphs first
    paragraphs = text.split('\n\n')

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < max_tokens * 4:  # ~4 chars per token
            current_chunk += "\n\n" + para if current_chunk else para
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
```

### Chunk Size Recommendations

| Content Type | Recommended Size | Overlap |
|--------------|------------------|---------|
| Technical docs | 500-1000 chars | 100 |
| FAQ/Support | 200-500 chars | 50 |
| Legal docs | 1000-1500 chars | 200 |
| News articles | 500-800 chars | 100 |
| Code | By function/class | Minimal |

---

## Retrieval Strategies

### 1. Basic Similarity Search

```python
def basic_retrieve(query: str, k: int = 5) -> list:
    """Simple top-k similarity search."""
    query_embedding = get_embedding(query)

    return db.search(query_embedding, limit=k)
```

### 2. Hybrid Search (Vector + Keyword)

```python
def hybrid_retrieve(query: str, k: int = 5) -> list:
    """Combine vector similarity with keyword matching."""
    query_embedding = get_embedding(query)

    # Get vector search results
    vector_results = db.vector_search(query_embedding, limit=k*2)

    # Get keyword search results
    keyword_results = db.keyword_search(query, limit=k*2)

    # Combine and re-rank (Reciprocal Rank Fusion)
    combined = reciprocal_rank_fusion(vector_results, keyword_results)

    return combined[:k]

def reciprocal_rank_fusion(list1: list, list2: list, k: int = 60) -> list:
    """Combine two ranked lists using RRF."""
    scores = {}

    for rank, doc in enumerate(list1):
        scores[doc['id']] = scores.get(doc['id'], 0) + 1 / (k + rank + 1)

    for rank, doc in enumerate(list2):
        scores[doc['id']] = scores.get(doc['id'], 0) + 1 / (k + rank + 1)

    # Sort by combined score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### 3. Re-ranking

```python
def retrieve_and_rerank(query: str, k: int = 5) -> list:
    """Retrieve candidates and re-rank with a more powerful model."""
    # Get more candidates than needed
    candidates = basic_retrieve(query, k=k*3)

    # Re-rank using cross-encoder or LLM
    reranked = []
    for doc in candidates:
        relevance = score_relevance(query, doc['content'])
        reranked.append({**doc, 'relevance': relevance})

    # Sort by relevance and return top k
    reranked.sort(key=lambda x: x['relevance'], reverse=True)
    return reranked[:k]
```

### 4. Multi-Query Retrieval

```python
def multi_query_retrieve(query: str, k: int = 5) -> list:
    """Generate multiple query variations for broader retrieval."""
    # Generate query variations
    variations = generate_query_variations(query)

    # Retrieve for each variation
    all_results = []
    for variation in variations:
        results = basic_retrieve(variation, k=k)
        all_results.extend(results)

    # Deduplicate and rank
    unique_results = deduplicate(all_results)
    return unique_results[:k]

def generate_query_variations(query: str) -> list:
    """Use LLM to generate query variations."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Generate 3 alternative ways to ask this question."},
            {"role": "user", "content": query}
        ]
    )
    variations = response.choices[0].message.content.split('\n')
    return [query] + variations[:3]
```

---

## Prompt Engineering for RAG

### Basic RAG Prompt

```python
RAG_PROMPT = """You are a helpful assistant. Answer the question based on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Only use information from the context
- If the context doesn't contain the answer, say "I don't have enough information"
- Be concise and accurate
- Cite sources when appropriate

Answer:"""
```

### Structured RAG Prompt

```python
STRUCTURED_RAG_PROMPT = """You are an expert assistant for our company's documentation.

## Context Documents
{context}

## User Question
{question}

## Instructions
1. Answer based ONLY on the provided context documents
2. Structure your response clearly
3. If quoting directly, use quotation marks
4. If the answer requires multiple steps, use numbered lists
5. If you cannot find the answer in the context, respond with:
   "I couldn't find specific information about this in the available documents."

## Your Response:"""
```

### Chain-of-Thought RAG Prompt

```python
COT_RAG_PROMPT = """You are a helpful assistant that answers questions step by step.

## Available Context
{context}

## Question
{question}

## Your Task
1. First, identify which context documents are relevant to the question
2. Extract the key information needed to answer
3. Synthesize the information into a clear answer
4. Note any limitations or missing information

Think through this step by step:"""
```

### Citation-Focused Prompt

```python
CITATION_PROMPT = """Answer the question using only the provided sources. Cite each source used.

Sources:
{context}

Question: {question}

Provide your answer with inline citations in the format [Source: filename]. Example:
"The refund policy allows returns within 30 days [Source: refund-policy.md]."

Answer with citations:"""
```

---

## Evaluating RAG Systems

### Key Metrics

| Metric | What It Measures | How to Calculate |
|--------|------------------|------------------|
| **Retrieval Recall** | Are relevant docs retrieved? | Relevant retrieved / Total relevant |
| **Retrieval Precision** | Are retrieved docs relevant? | Relevant retrieved / Total retrieved |
| **Answer Relevance** | Does answer address question? | LLM evaluation |
| **Faithfulness** | Is answer grounded in context? | Verify claims against sources |
| **Answer Correctness** | Is the answer correct? | Compare to ground truth |

### Simple Evaluation Framework

```python
def evaluate_rag_response(
    question: str,
    retrieved_docs: list,
    generated_answer: str,
    ground_truth: str = None
) -> dict:
    """Evaluate a RAG response on multiple dimensions."""

    scores = {}

    # 1. Retrieval quality (using LLM as judge)
    retrieval_eval = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Rate how relevant these documents are to the question (1-5)."},
            {"role": "user", "content": f"Question: {question}\n\nDocuments:\n{retrieved_docs}"}
        ]
    )
    scores['retrieval_quality'] = parse_score(retrieval_eval.choices[0].message.content)

    # 2. Answer relevance
    relevance_eval = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Rate how well this answer addresses the question (1-5)."},
            {"role": "user", "content": f"Question: {question}\n\nAnswer: {generated_answer}"}
        ]
    )
    scores['answer_relevance'] = parse_score(relevance_eval.choices[0].message.content)

    # 3. Faithfulness (grounded in context)
    faithfulness_eval = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Check if every claim in the answer is supported by the context (1-5)."},
            {"role": "user", "content": f"Context: {retrieved_docs}\n\nAnswer: {generated_answer}"}
        ]
    )
    scores['faithfulness'] = parse_score(faithfulness_eval.choices[0].message.content)

    # 4. Correctness (if ground truth available)
    if ground_truth:
        correctness_eval = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Compare the answer to the ground truth. Rate accuracy (1-5)."},
                {"role": "user", "content": f"Ground Truth: {ground_truth}\n\nAnswer: {generated_answer}"}
            ]
        )
        scores['correctness'] = parse_score(correctness_eval.choices[0].message.content)

    return scores
```

---

## Complete RAG Implementation

### Full RAG System

```python
# rag_system.py
"""
Complete RAG System Implementation
"""

from openai import OpenAI
import psycopg2
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'rag_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}


class RAGSystem:
    """A complete RAG system for question answering."""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4o-mini",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 5,
        similarity_threshold: float = 0.5
    ):
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def get_connection(self):
        return psycopg2.connect(**DB_CONFIG)

    def setup_database(self):
        """Initialize the database schema."""
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rag_documents (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    source VARCHAR(500),
                    chunk_index INTEGER,
                    metadata JSONB,
                    embedding VECTOR(1536)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS rag_docs_embedding_idx
                ON rag_documents USING ivfflat (embedding vector_cosine_ops)
            """)
            conn.commit()
        conn.close()

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # Find natural break point
            if end < len(text):
                for sep in ['\n\n', '. ', '\n', ' ']:
                    break_point = text.rfind(sep, start + 100, end)
                    if break_point > start:
                        end = break_point + len(sep)
                        break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - self.chunk_overlap

        return chunks

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return response.data[0].embedding

    def add_document(self, content: str, source: str = None, metadata: dict = None):
        """Add a document to the knowledge base."""
        chunks = self.chunk_text(content)

        conn = self.get_connection()
        with conn.cursor() as cur:
            for idx, chunk in enumerate(chunks):
                embedding = self.get_embedding(chunk)
                cur.execute("""
                    INSERT INTO rag_documents (content, source, chunk_index, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                """, (chunk, source, idx, psycopg2.extras.Json(metadata or {}), embedding))

            conn.commit()
        conn.close()

        return len(chunks)

    def retrieve(self, query: str) -> List[Dict]:
        """Retrieve relevant document chunks."""
        query_embedding = self.get_embedding(query)

        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT content, source, 1 - (embedding <=> %s::vector) as similarity
                FROM rag_documents
                WHERE 1 - (embedding <=> %s::vector) >= %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (
                query_embedding,
                query_embedding,
                self.similarity_threshold,
                query_embedding,
                self.top_k
            ))

            results = [
                {'content': row[0], 'source': row[1], 'similarity': row[2]}
                for row in cur.fetchall()
            ]

        conn.close()
        return results

    def generate(self, query: str, context_docs: List[Dict]) -> str:
        """Generate answer using retrieved context."""
        if not context_docs:
            return "I don't have enough information to answer this question."

        # Format context
        context = "\n\n---\n\n".join([
            f"[Source: {doc.get('source', 'unknown')}]\n{doc['content']}"
            for doc in context_docs
        ])

        # Generate response
        response = client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant that answers questions based on provided context.

Rules:
1. Only answer based on the context provided
2. If the context doesn't contain enough information, say so
3. Cite sources when making specific claims
4. Be clear and concise"""
                },
                {
                    "role": "user",
                    "content": f"""Context:
{context}

Question: {query}

Please provide a helpful answer based on the context above:"""
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    def query(self, question: str) -> Dict:
        """Full RAG pipeline: retrieve and generate."""
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(question)

        # Generate answer
        answer = self.generate(question, retrieved_docs)

        return {
            'question': question,
            'answer': answer,
            'sources': [
                {'source': doc['source'], 'similarity': doc['similarity']}
                for doc in retrieved_docs
            ],
            'context_used': len(retrieved_docs)
        }


def main():
    """Demo the RAG system."""
    import psycopg2.extras

    print("=" * 60)
    print("  RAG System Demo")
    print("=" * 60)

    # Initialize system
    rag = RAGSystem()
    rag.setup_database()

    # Add sample documents
    documents = [
        {
            "content": """Password Reset Guide

To reset your password:
1. Go to the login page at app.example.com/login
2. Click the "Forgot Password" link
3. Enter your registered email address
4. Check your email for the reset link (valid for 24 hours)
5. Click the link and enter your new password

Password Requirements:
- Minimum 8 characters
- At least one uppercase letter
- At least one number
- At least one special character (!@#$%^&*)""",
            "source": "help/password-reset.md"
        },
        {
            "content": """Billing and Subscription Plans

We offer three subscription tiers:

Basic Plan - $9.99/month
- 5 projects maximum
- Email support (48h response)
- 10GB storage
- Basic analytics

Pro Plan - $24.99/month
- Unlimited projects
- Priority support (24h response)
- 100GB storage
- Advanced analytics
- API access

Enterprise Plan - Contact Sales
- Custom pricing
- Dedicated account manager
- Unlimited storage
- Custom integrations
- SLA guarantee""",
            "source": "help/pricing.md"
        }
    ]

    print("\n1. Adding documents to knowledge base...")
    for doc in documents:
        chunks = rag.add_document(doc["content"], doc["source"])
        print(f"   Added: {doc['source']} ({chunks} chunks)")

    # Test queries
    print("\n2. Testing RAG queries...")
    queries = [
        "How do I reset my password?",
        "What's included in the Pro plan?",
        "How much does the Basic plan cost?"
    ]

    for query in queries:
        print(f"\n   Q: {query}")
        result = rag.query(query)
        print(f"   A: {result['answer'][:200]}...")
        print(f"   Sources: {[s['source'] for s in result['sources']]}")


if __name__ == "__main__":
    main()
```

---

## Best Practices

### 1. Chunk Wisely

```
✓ Use semantic boundaries (paragraphs, sections)
✓ Include overlap to maintain context
✓ Keep chunks focused on single topics
✗ Don't split mid-sentence
✗ Don't make chunks too small (lose context)
✗ Don't make chunks too large (imprecise retrieval)
```

### 2. Optimize Retrieval

```
✓ Use hybrid search (vector + keyword)
✓ Implement re-ranking for better precision
✓ Filter by metadata when relevant
✓ Tune similarity thresholds
✗ Don't rely solely on top-1 result
✗ Don't retrieve too many documents (noise)
```

### 3. Engineer Good Prompts

```
✓ Be explicit about using only context
✓ Include instructions for handling missing info
✓ Ask for citations/sources
✓ Set the right tone and format
✗ Don't assume the LLM knows your domain
✗ Don't forget to test edge cases
```

### 4. Evaluate Continuously

```
✓ Test with real user queries
✓ Track retrieval and generation metrics
✓ Collect user feedback
✓ Monitor for hallucinations
✗ Don't deploy without testing
✗ Don't ignore failure cases
```

---

## Summary

You've learned:

1. **What RAG is**: Retrieval + Augmented + Generation
2. **Why it matters**: Grounds LLMs in your data
3. **How it works**: Embed → Store → Retrieve → Generate
4. **Chunking**: Breaking documents into searchable pieces
5. **Retrieval**: Finding relevant content efficiently
6. **Generation**: Prompting LLMs with context
7. **Evaluation**: Measuring RAG system quality

### Next Steps

1. Build a RAG system for your documents
2. Experiment with chunking strategies
3. Try hybrid search and re-ranking
4. Move on to [Chapter 8: AI Agents](../AI-Agents/chapter-8-langchain-langgraph.md)

---

[← Previous: Chapter 6 - Vector Databases](../Vector-DB/chapter-6-knowledge-bases-embeddings.md) | [Back to Main Guide](../README.md) | [Next: Chapter 8 - AI Agents →](../AI-Agents/chapter-8-langchain-langgraph.md)
