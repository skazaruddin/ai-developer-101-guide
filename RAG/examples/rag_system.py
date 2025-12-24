"""
Complete RAG System Example
A fully functional Retrieval-Augmented Generation system.

Features:
- Document ingestion with chunking
- Semantic search with pgvector
- Context-aware answer generation
- Source citation

Prerequisites:
- pip install openai psycopg2-binary python-dotenv
- PostgreSQL with pgvector extension

Setup:
1. Create .env file with API keys and DB credentials
2. Run: python rag_system.py
"""

from openai import OpenAI
import psycopg2
import psycopg2.extras
import os
import re
from typing import List, Dict, Optional
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rag_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}


@dataclass
class Document:
    """Represents a document in the knowledge base."""
    content: str
    source: str
    metadata: dict = None


@dataclass
class RetrievedChunk:
    """Represents a retrieved chunk from the knowledge base."""
    content: str
    source: str
    similarity: float


class RAGSystem:
    """
    A complete RAG (Retrieval-Augmented Generation) system.

    This system allows you to:
    1. Add documents to a knowledge base
    2. Search for relevant information using semantic search
    3. Generate answers grounded in the retrieved context
    """

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4o-mini",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 5,
        similarity_threshold: float = 0.5
    ):
        """
        Initialize the RAG system.

        Args:
            embedding_model: OpenAI embedding model to use
            llm_model: OpenAI LLM model for generation
            chunk_size: Target size for document chunks (in characters)
            chunk_overlap: Overlap between chunks for context continuity
            top_k: Number of chunks to retrieve
            similarity_threshold: Minimum similarity score for retrieval
        """
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        self.table_name = "rag_documents"

    def get_connection(self):
        """Create a database connection."""
        return psycopg2.connect(**DB_CONFIG)

    def setup_database(self):
        """Create necessary tables and indexes."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Enable pgvector extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

                # Create documents table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        source VARCHAR(500),
                        chunk_index INTEGER,
                        metadata JSONB DEFAULT '{{}}'::jsonb,
                        embedding VECTOR(1536),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Create index for fast similarity search
                cur.execute(f"""
                    CREATE INDEX IF NOT EXISTS {self.table_name}_embedding_idx
                    ON {self.table_name}
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100)
                """)

                conn.commit()
                print("Database setup complete!")
        finally:
            conn.close()

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.

        Uses smart chunking that respects natural boundaries like
        paragraphs and sentences.
        """
        chunks = []
        text = text.strip()

        if len(text) <= self.chunk_size:
            return [text]

        start = 0
        while start < len(text):
            end = start + self.chunk_size

            # If not at the end, find a good break point
            if end < len(text):
                # Try to break at paragraph
                para_break = text.rfind('\n\n', start + 100, end)
                if para_break > start:
                    end = para_break + 2
                else:
                    # Try to break at sentence
                    for sep in ['. ', '! ', '? ', '\n']:
                        sent_break = text.rfind(sep, start + 100, end)
                        if sent_break > start:
                            end = sent_break + len(sep)
                            break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Move to next chunk with overlap
            start = max(start + 1, end - self.chunk_overlap)

        return chunks

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text string."""
        response = client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return response.data[0].embedding

    def add_document(
        self,
        content: str,
        source: str = None,
        metadata: dict = None
    ) -> int:
        """
        Add a document to the knowledge base.

        The document will be chunked and each chunk will be stored
        with its embedding.

        Returns the number of chunks created.
        """
        chunks = self.chunk_text(content)

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                for idx, chunk in enumerate(chunks):
                    embedding = self.get_embedding(chunk)

                    cur.execute(f"""
                        INSERT INTO {self.table_name}
                        (content, source, chunk_index, metadata, embedding)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        chunk,
                        source,
                        idx,
                        psycopg2.extras.Json(metadata or {}),
                        embedding
                    ))

                conn.commit()
        finally:
            conn.close()

        return len(chunks)

    def add_documents(self, documents: List[Document]) -> int:
        """Add multiple documents to the knowledge base."""
        total_chunks = 0
        for doc in documents:
            chunks = self.add_document(
                content=doc.content,
                source=doc.source,
                metadata=doc.metadata
            )
            total_chunks += chunks
        return total_chunks

    def retrieve(self, query: str) -> List[RetrievedChunk]:
        """
        Retrieve relevant chunks for a query.

        Uses semantic similarity search to find the most relevant
        document chunks.
        """
        query_embedding = self.get_embedding(query)

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT
                        content,
                        source,
                        1 - (embedding <=> %s::vector) as similarity
                    FROM {self.table_name}
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
                    RetrievedChunk(
                        content=row[0],
                        source=row[1],
                        similarity=float(row[2])
                    )
                    for row in cur.fetchall()
                ]
        finally:
            conn.close()

        return results

    def generate_answer(
        self,
        query: str,
        context_chunks: List[RetrievedChunk]
    ) -> str:
        """
        Generate an answer using retrieved context.

        Uses the LLM to synthesize an answer from the relevant chunks.
        """
        if not context_chunks:
            return "I don't have enough information to answer this question."

        # Format context
        context_parts = []
        for chunk in context_chunks:
            source = chunk.source or "Unknown"
            context_parts.append(f"[Source: {source}]\n{chunk.content}")

        context = "\n\n---\n\n".join(context_parts)

        # Build prompt
        system_prompt = """You are a helpful assistant that answers questions based on the provided context.

IMPORTANT RULES:
1. Only answer based on the information in the context
2. If the context doesn't contain enough information, say "I don't have enough information to fully answer this question"
3. When making specific claims, cite the source
4. Be clear and concise
5. If asked about something not in the context, don't make up information"""

        user_prompt = f"""Context:
{context}

---

Question: {query}

Please provide a helpful answer based on the context above. Cite sources when appropriate."""

        response = client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    def query(self, question: str) -> Dict:
        """
        Complete RAG pipeline: retrieve and generate.

        Args:
            question: The user's question

        Returns:
            Dictionary containing:
            - question: The original question
            - answer: The generated answer
            - sources: List of sources used
            - chunks_retrieved: Number of chunks retrieved
        """
        # Retrieve relevant context
        chunks = self.retrieve(question)

        # Generate answer
        answer = self.generate_answer(question, chunks)

        return {
            'question': question,
            'answer': answer,
            'sources': [
                {'source': c.source, 'similarity': round(c.similarity, 3)}
                for c in chunks
            ],
            'chunks_retrieved': len(chunks)
        }

    def clear_knowledge_base(self):
        """Clear all documents from the knowledge base."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(f"TRUNCATE {self.table_name} RESTART IDENTITY")
                conn.commit()
        finally:
            conn.close()

    def get_document_count(self) -> int:
        """Get the total number of chunks in the knowledge base."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {self.table_name}")
                return cur.fetchone()[0]
        finally:
            conn.close()


def demo():
    """Demonstrate the RAG system."""
    print("=" * 60)
    print("  RAG System Demo")
    print("=" * 60)

    # Initialize
    rag = RAGSystem(
        chunk_size=400,
        chunk_overlap=50,
        top_k=3,
        similarity_threshold=0.5
    )

    # Setup database
    print("\n1. Setting up database...")
    rag.setup_database()
    rag.clear_knowledge_base()

    # Add sample documents
    print("\n2. Adding sample documents...")

    documents = [
        Document(
            content="""# Password Reset Guide

If you've forgotten your password, follow these steps to reset it:

1. Navigate to the login page at app.example.com/login
2. Click the "Forgot Password" link below the login form
3. Enter your registered email address
4. Check your email inbox (and spam folder) for the reset link
5. Click the reset link - it's valid for 24 hours
6. Enter your new password twice to confirm

Password Requirements:
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one special character (!@#$%^&*)

If you don't receive the email within 5 minutes, contact support.""",
            source="help/password-reset.md"
        ),
        Document(
            content="""# Subscription Plans and Pricing

We offer three subscription plans to meet different needs:

## Basic Plan - $9.99/month
Perfect for individuals and small projects.
- Up to 5 projects
- Email support (response within 48 hours)
- 10GB storage
- Basic analytics dashboard
- Community forum access

## Pro Plan - $24.99/month
Ideal for professionals and growing teams.
- Unlimited projects
- Priority support (response within 24 hours)
- 100GB storage
- Advanced analytics with exports
- API access (10,000 calls/month)
- Team collaboration features

## Enterprise Plan - Custom Pricing
For large organizations with custom needs.
- Unlimited everything
- Dedicated account manager
- 24/7 phone support
- Unlimited storage
- Custom integrations
- SLA guarantee (99.9% uptime)
- On-premise deployment option

All plans include a 14-day free trial. Contact sales@example.com for Enterprise pricing.""",
            source="help/pricing.md"
        ),
        Document(
            content="""# API Rate Limits and Usage

Our API has rate limits to ensure fair usage and system stability.

## Rate Limits by Plan

### Basic Plan
- 100 requests per minute
- 1,000 requests per day
- Maximum payload size: 1MB

### Pro Plan
- 1,000 requests per minute
- 10,000 requests per day
- Maximum payload size: 10MB

### Enterprise Plan
- Custom limits based on your needs
- Dedicated API endpoints available

## Handling Rate Limits

When you exceed rate limits, the API returns a 429 status code with a Retry-After header indicating when you can retry.

Best practices:
1. Implement exponential backoff
2. Cache responses when possible
3. Use webhooks instead of polling
4. Contact support if you consistently hit limits""",
            source="docs/api-limits.md"
        )
    ]

    total_chunks = rag.add_documents(documents)
    print(f"   Added {len(documents)} documents ({total_chunks} chunks)")

    # Test queries
    print("\n3. Testing queries...")
    print("-" * 60)

    test_queries = [
        "How do I reset my password?",
        "What does the Pro plan include?",
        "What are the API rate limits?",
        "How much does the Basic plan cost?"
    ]

    for query in test_queries:
        print(f"\nQ: {query}")
        result = rag.query(query)
        print(f"A: {result['answer']}")
        print(f"Sources: {[s['source'] for s in result['sources']]}")
        print("-" * 60)


if __name__ == "__main__":
    demo()
