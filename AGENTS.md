# Document Agent

## Mission

Build a production-grade AI document search platform.

The application should allow users to

- Upload PDFs
- Parse documents
- Generate embeddings
- Store vectors
- Search semantically
- Chat with documents
- Cite sources
- Support multiple LLM providers

---

## Tech Stack

Backend
- Python 3.12
- FastAPI
- ChromaDB
- SQLAlchemy
- httpx
- LangChain

Frontend
- React
- JavaScript
- Vite
- React Query
- Tailwind CSS

AI
- Ollama (nomic-embed-text for embeddings, mistral for LLM)
- LangChain (text processing)

---

## Architecture

React

↓

FastAPI

↓

Service Layer

↓

ChromaDB

↓

Ollama LLM

---

## AI Responsibilities

Always

- understand the existing architecture
- preserve API compatibility
- prefer modular code
- avoid unnecessary dependencies
- write production-ready code
- explain architectural trade-offs before major changes

---

## Before Coding

Always explain

- design
- assumptions
- risks
- alternatives

before generating code.

---

## Never

- generate placeholder implementations
- hardcode secrets
- duplicate business logic
- ignore error handling