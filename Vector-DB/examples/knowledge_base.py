"""
Knowledge Base with pgvector
A complete example of building a semantic search knowledge base.

Prerequisites:
1. PostgreSQL with pgvector extension
2. pip install openai psycopg2-binary python-dotenv

Setup:
1. Create .env file with:
   OPENAI_API_KEY=your-key
   DB_HOST=localhost
   DB_NAME=knowledge_db
   DB_USER=postgres
   DB_PASSWORD=your-password

2. In PostgreSQL, create database and enable pgvector:
   CREATE DATABASE knowledge_db;
   \c knowledge_db
   CREATE EXTENSION vector;
"""

import psycopg2
import psycopg2.extras
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'knowledge_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}


class KnowledgeBase:
    """A knowledge base with semantic search using pgvector."""

    def __init__(self, table_name: str = "documents"):
        self.table_name = table_name
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimensions = 1536

    def get_connection(self):
        """Create a database connection."""
        return psycopg2.connect(**DB_CONFIG)

    def setup(self):
        """Set up the database table and index."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Enable pgvector extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

                # Create documents table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(500),
                        content TEXT NOT NULL,
                        source VARCHAR(500),
                        metadata JSONB DEFAULT '{{}}'::jsonb,
                        embedding VECTOR({self.embedding_dimensions}),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                print(f"Table '{self.table_name}' created successfully!")

        finally:
            conn.close()

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI."""
        response = openai_client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return response.data[0].embedding

    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = openai_client.embeddings.create(
            input=texts,
            model=self.embedding_model
        )
        return [item.embedding for item in response.data]

    def add_document(
        self,
        content: str,
        title: str = None,
        source: str = None,
        metadata: dict = None
    ) -> int:
        """Add a single document to the knowledge base."""
        embedding = self.get_embedding(content)

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO {self.table_name}
                    (title, content, source, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    title,
                    content,
                    source,
                    psycopg2.extras.Json(metadata or {}),
                    embedding
                ))
                doc_id = cur.fetchone()[0]
                conn.commit()
                return doc_id
        finally:
            conn.close()

    def add_documents_batch(self, documents: List[Dict]) -> List[int]:
        """Add multiple documents at once."""
        # Get all embeddings in one API call
        contents = [doc['content'] for doc in documents]
        embeddings = self.get_embeddings_batch(contents)

        conn = self.get_connection()
        try:
            doc_ids = []
            with conn.cursor() as cur:
                for doc, embedding in zip(documents, embeddings):
                    cur.execute(f"""
                        INSERT INTO {self.table_name}
                        (title, content, source, metadata, embedding)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        doc.get('title'),
                        doc['content'],
                        doc.get('source'),
                        psycopg2.extras.Json(doc.get('metadata', {})),
                        embedding
                    ))
                    doc_ids.append(cur.fetchone()[0])

                conn.commit()
            return doc_ids
        finally:
            conn.close()

    def search(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.0
    ) -> List[Dict]:
        """Search for similar documents using semantic search."""
        query_embedding = self.get_embedding(query)

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT
                        id,
                        title,
                        content,
                        source,
                        metadata,
                        1 - (embedding <=> %s::vector) AS similarity
                    FROM {self.table_name}
                    WHERE 1 - (embedding <=> %s::vector) >= %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """, (
                    query_embedding,
                    query_embedding,
                    threshold,
                    query_embedding,
                    limit
                ))

                results = []
                for row in cur.fetchall():
                    results.append({
                        'id': row[0],
                        'title': row[1],
                        'content': row[2],
                        'source': row[3],
                        'metadata': row[4],
                        'similarity': float(row[5])
                    })
                return results
        finally:
            conn.close()

    def delete_document(self, doc_id: int) -> bool:
        """Delete a document by ID."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    DELETE FROM {self.table_name} WHERE id = %s
                """, (doc_id,))
                deleted = cur.rowcount > 0
                conn.commit()
                return deleted
        finally:
            conn.close()

    def get_document_count(self) -> int:
        """Get the total number of documents."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {self.table_name}")
                return cur.fetchone()[0]
        finally:
            conn.close()

    def clear_all(self):
        """Delete all documents (use with caution!)."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(f"TRUNCATE {self.table_name} RESTART IDENTITY")
                conn.commit()
        finally:
            conn.close()


def demo():
    """Demonstrate the knowledge base functionality."""
    print("=" * 60)
    print("  Knowledge Base Demo")
    print("=" * 60)

    # Initialize
    kb = KnowledgeBase()
    kb.setup()

    # Clear any existing data
    kb.clear_all()

    # Sample documents
    documents = [
        {
            "title": "Password Reset",
            "content": """To reset your password, follow these steps:
1. Go to the login page
2. Click 'Forgot Password'
3. Enter your email address
4. Check your inbox for the reset link
5. Click the link and create a new password

Your new password must be at least 8 characters long and include
at least one number and one special character.""",
            "source": "help/account.md",
            "metadata": {"category": "account", "priority": "high"}
        },
        {
            "title": "Subscription Plans",
            "content": """We offer three subscription tiers:

**Basic Plan - $9.99/month**
- Up to 5 projects
- Email support
- 10GB storage

**Pro Plan - $24.99/month**
- Unlimited projects
- Priority support
- 100GB storage
- Advanced analytics

**Enterprise Plan - Custom pricing**
- Custom integrations
- Dedicated support
- Unlimited storage
- SLA guarantee""",
            "source": "pricing/plans.md",
            "metadata": {"category": "pricing", "priority": "high"}
        },
        {
            "title": "Data Export Guide",
            "content": """You can export your data anytime:

1. Navigate to Settings > Data Management
2. Click 'Export Data'
3. Select the format (CSV, JSON, or Excel)
4. Choose which data to include
5. Click 'Generate Export'

Your export will be ready within 24 hours. You'll receive
an email notification when it's available for download.
Exports are available for 7 days.""",
            "source": "help/data.md",
            "metadata": {"category": "data", "priority": "medium"}
        },
        {
            "title": "Two-Factor Authentication",
            "content": """Enable two-factor authentication (2FA) for extra security:

1. Go to Settings > Security
2. Click 'Enable 2FA'
3. Scan the QR code with an authenticator app
4. Enter the verification code
5. Save your backup codes securely

Supported authenticator apps:
- Google Authenticator
- Authy
- Microsoft Authenticator""",
            "source": "help/security.md",
            "metadata": {"category": "security", "priority": "high"}
        }
    ]

    # Add documents
    print("\n1. Adding documents...")
    doc_ids = kb.add_documents_batch(documents)
    print(f"   Added {len(doc_ids)} documents")

    # Search examples
    print("\n2. Testing semantic search...")

    queries = [
        "How do I change my password?",
        "What are the pricing options?",
        "Can I download my information?",
        "How to set up 2FA?",
        "What's the weather like?"  # Should have low similarity
    ]

    for query in queries:
        print(f"\n   Query: '{query}'")
        results = kb.search(query, limit=2)

        if results:
            for result in results:
                print(f"   - {result['title']} (similarity: {result['similarity']:.2%})")
        else:
            print("   - No results found")

    # Document count
    print(f"\n3. Total documents in knowledge base: {kb.get_document_count()}")


if __name__ == "__main__":
    demo()
