# Project Overview

Document Agent is a Retrieval Augmented Generation (RAG) platform.

Users upload PDFs.

The backend

1. extracts text
2. splits text into chunks
3. generates embeddings
4. stores vectors
5. stores metadata
6. retrieves relevant chunks
7. sends context to LLM
8. streams responses

The frontend provides

1. Document management (upload, list, delete, reindex)
2. Semantic search with source citations
3. RAG query - ask questions and get AI-powered answers
4. Multi-turn chat with RAG context
5. System statistics dashboard

---

Current Stack

Backend

FastAPI

SQLAlchemy

ChromaDB

Ollama (embeddings + LLM)

LangChain

Frontend

React

JavaScript

React Query

Tailwind

---

Directory Structure

backend/

frontend/

skills/

docs/

---

Primary Goals

Fast

Scalable

Maintainable

Production Ready