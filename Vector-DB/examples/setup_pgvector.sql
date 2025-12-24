-- pgvector Setup Script
-- Run this in PostgreSQL to set up your vector database

-- Create a new database for the knowledge base
CREATE DATABASE knowledge_db;

-- Connect to the new database
\c knowledge_db

-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the documents table
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500),
    content TEXT NOT NULL,
    source VARCHAR(500),
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(1536),  -- 1536 dimensions for OpenAI embeddings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index for fast similarity search
-- IVFFlat is good for medium-sized datasets
-- For large datasets, consider HNSW index instead
CREATE INDEX IF NOT EXISTS documents_embedding_idx
ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Optional: Create additional indexes for filtering
CREATE INDEX IF NOT EXISTS documents_source_idx ON documents(source);
CREATE INDEX IF NOT EXISTS documents_metadata_idx ON documents USING GIN (metadata);

-- Verify setup
SELECT
    e.extname AS extension,
    e.extversion AS version
FROM pg_extension e
WHERE e.extname = 'vector';

-- Show table structure
\d documents

-- Example: Insert a test document (you would normally do this from Python)
-- INSERT INTO documents (title, content, embedding)
-- VALUES (
--     'Test Document',
--     'This is a test document for the knowledge base.',
--     '[0.1, 0.2, 0.3, ...]'::vector  -- Replace with actual 1536-dim vector
-- );

-- Example: Search for similar documents
-- SELECT
--     id,
--     title,
--     content,
--     1 - (embedding <=> '[0.1, 0.2, 0.3, ...]'::vector) AS similarity
-- FROM documents
-- ORDER BY embedding <=> '[0.1, 0.2, 0.3, ...]'::vector
-- LIMIT 5;

COMMENT ON TABLE documents IS 'Knowledge base documents with vector embeddings for semantic search';
