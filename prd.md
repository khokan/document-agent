# 📄 Product Requirements Document (PRD)
## 🤖 PDF Knowledge Assistant — RAG Engine

> **Document Version:** 1.0 &nbsp;|&nbsp; **Last Updated:** July 2026 &nbsp;|&nbsp; **Status:** 🟢 Active Development  
> **Owner:** Engineering Team

---

## 📋 Table of Contents

1. [Project Overview](#1--project-overview)
2. [Objectives](#2--objectives)
3. [Technology Stack](#3--technology-stack)
4. [High-Level Architecture](#4--high-level-architecture)
5. [Functional Requirements](#5--functional-requirements)
6. [API Design](#6--api-design)
7. [Chroma Collection Design](#7--chroma-collection-design)
8. [Folder Structure](#8--folder-structure)
9. [Retrieval Flow](#9--retrieval-flow)
10. [Metadata Filtering](#10--metadata-filtering)
11. [Performance Goals](#11--performance-goals)
12. [Error Handling](#12--error-handling)
13. [Logging](#13--logging)
14. [Future Enhancements](#14--future-enhancements)
15. [Installation & Setup](#15--installation--setup)
16. [Configuration Parameters](#16--configuration-parameters)
17. [Security Considerations](#17--security-considerations)
18. [Testing Strategy](#18--testing-strategy)
19. [Monitoring & Maintenance](#19--monitoring--maintenance)
20. [Documentation](#20--documentation)
21. [Success Metrics](#21--success-metrics)
22. [Risks & Mitigations](#22--risks--mitigations)


---

## 1. 🎯 Project Overview

### 📌 Project Name
**PDF Knowledge Assistant (RAG Engine)**

### 🏁 Goal
Build a **local Retrieval-Augmented Generation (RAG)** system that:

- 📤 Uploads one or multiple PDFs
- 📑 Extracts text from PDFs
- ✂️ Splits text into semantic chunks
- 🔢 Converts chunks into vector embeddings
- 💾 Stores embeddings in ChromaDB
- 🔍 Allows natural language semantic search
- 🧠 Uses Ollama (Mistral) to answer questions using retrieved context

> ⚡ **Key Principle:** Everything runs **locally** — zero cloud dependencies.

---

## 2. 🎯 Objectives

| Objective | Description |
|-----------|-------------|
| 📈 **Scalability** | Handle thousands of PDFs and millions of chunks |
| ⚡ **Performance** | Fast semantic search with `<100ms` retrieval |
| 🔄 **Data Management** | Incremental updates, delete, and re-index documents |
| 🔎 **Transparency** | Return source pages and similarity scores with every answer |
| 🔌 **Independence** | Operate completely offline with no internet access |

---

## 3. 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| 🐍 Language | Python | 3.12+ |
| 🧠 LLM | Ollama (Mistral) | Latest |
| 🔢 Embedding Model | nomic-embed-text | Latest |
| 💾 Vector DB | ChromaDB | 0.4.22+ |
| 📄 PDF Extraction | PdfPlumber | Latest |
| ✂️ Chunking | LangChain TextSplitter / Custom | 0.1.0+ |
| 🌐 API | FastAPI | 0.104.1+ |
| 🗃️ Storage | Local Filesystem | — |
| 📋 Metadata | SQLite (optional) | — |

---

## 4. 🏗️ High-Level Architecture

### 📥 Ingestion Pipeline

```
📤 Upload PDF
      │
      ▼
📑 PDF Extraction
      │
      ▼
🧹 Text Cleaning
      │
      ▼
✂️ Chunk Generator
      │
      ▼
🔢 Embedding Generator
   (nomic-embed-text)
      │
      ▼
💾 ChromaDB (Vector Store)
```

### 🔍 Query Pipeline

```
❓ User Question
      │
      ▼
🔢 Embed Question (nomic-embed-text)
      │
      ▼
🔍 ChromaDB Similarity Search
      │
      ▼
📦 Top K Chunks Retrieved
      │
      ▼
📝 Prompt Builder (Context + Question)
      │
      ▼
🧠 Mistral LLM
      │
      ▼
💬 Answer with Source Citations
```

---

## 5. ⚙️ Functional Requirements

### 📤 Module 1 — PDF Upload

**Features:**
- ✅ Upload single PDF
- ✅ Upload multiple PDFs (batch)
- ✅ Drag & Drop support
- ✅ Validate PDF format and integrity
- ✅ Configurable maximum file size

**📤 Output Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `documentId` | String | Unique document identifier |
| `filename` | String | Original file name |
| `uploadDate` | DateTime | ISO 8601 upload timestamp |
| `status` | Enum | `pending` / `indexed` / `failed` |

---

### 📑 Module 2 — PDF Parsing

**✅ Extract:**
- Page text content
- Page numbers
- Document title
- Document metadata

**🚫 Ignore:**
- Images
- Signatures
- Headers
- Footers

**📄 Store Format:**
```
Page 1: [Content]
Page 2: [Content]
...
Page N: [Content]
```

---

### ✂️ Module 3 — Chunking

**⚙️ Configuration:**

| Parameter | Value |
|-----------|-------|
| Chunk Size | 500 words |
| Overlap | 100 words |
| Min Chunk Size | 50 words |

**📦 Each Chunk Stores:**
```json
{
  "chunkId": "abc_2024_page_12_chunk_3",
  "documentId": "doc_123",
  "page": 12,
  "chunkNumber": 3,
  "text": "content..."
}
```

---

### 🔢 Module 4 — Embedding Generation

| Property | Value |
|----------|-------|
| **Model** | `nomic-embed-text` |
| **Ollama Endpoint** | `POST /api/embed` |
| **Input** | Chunk text (string) |
| **Output** | 768-dimension float vector |

---

### 💾 Module 5 — ChromaDB Collection

**Collection Name:** `company_documents`

**📋 Stores:**
- Unique chunk ID
- 768-dimension embedding vector
- Raw chunk text
- Full metadata object

**🏷️ Metadata Schema:**
```json
{
  "document": "AnnualReport2024.pdf",
  "page": 42,
  "company": "ABC",
  "year": 2024,
  "chunkNumber": 2
}
```

---

### 🔍 Module 6 — Search

**Input:** Natural language question  
**Example:** `"Why did revenue increase?"`

**Flow:**
```
Question → Embed → ChromaDB Similarity Search → Top 5 Chunks → Return Results
```

**📤 Response Format:**
```json
{
  "answer": "Revenue increased due to...",
  "sources": [
    {
      "documentId": "abc_2024",
      "filename": "AnnualReport2024.pdf",
      "page": 34,
      "score": 0.95,
      "text": "Revenue increased..."
    }
  ]
}
```

---

### 🧠 Module 7 — LLM Answer Generation

**📝 Prompt Template:**
```
Answer ONLY using the provided context.
If the answer is unavailable, say "I couldn't find this information."

Context:
{retrieved_chunks}

Question: {user_question}

Answer:
```

**Output:** Natural language answer with page-level source citations

---

### 📂 Module 8 — Document Management

| Function | Endpoint | Description |
|----------|----------|-------------|
| ⬆️ Upload | `POST /documents/upload` | Add new documents to the system |
| 🗑️ Delete | `DELETE /documents/{id}` | Remove document and all its chunks |
| 🔄 Reindex | `POST /documents/reindex/{id}` | Re-process and re-embed a document |
| 📋 List | `GET /documents` | View all indexed documents |
| 📊 Statistics | `GET /documents/stats` | System-wide stats (chunks, docs, disk) |

---

## 6. 🔌 API Design

### ⬆️ Upload PDF
```http
POST /documents/upload
Content-Type: multipart/form-data
```
**Response:**
```json
{
  "documentId": "abc_2024",
  "filename": "AnnualReport2024.pdf",
  "status": "indexed",
  "chunkCount": 142
}
```

---

### 🔍 Search
```http
POST /search
Content-Type: application/json
```
**Request:**
```json
{
  "question": "Why did revenue increase?",
  "filters": {
    "company": "ABC",
    "year": 2024
  },
  "topK": 5
}
```
**Response:**
```json
{
  "answer": "Revenue increased due to...",
  "sources": [
    {
      "documentId": "abc_2024",
      "filename": "AnnualReport2024.pdf",
      "page": 34,
      "score": 0.95,
      "text": "Revenue increased..."
    }
  ]
}
```

---

### 🗑️ Delete Document
```http
DELETE /documents/{id}
```

---

### 📋 List Documents
```http
GET /documents
```

---

### 🔄 Reindex Document
```http
POST /documents/reindex/{id}
```

---

## 7. 🗃️ Chroma Collection Design

**Collection:** `company_documents`

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Unique chunk identifier |
| `embedding` | Vector | 768-dimension float array |
| `document` | String | Source PDF filename |
| `company` | String | Company name |
| `year` | Integer | Document year |
| `page` | Integer | Source page number |
| `chunkNumber` | Integer | Chunk sequence index |
| `text` | String | Raw chunk content |

**🔑 Example ID Format:**
```
abc_2024_page_35_chunk_2
```

---

## 8. 📁 Folder Structure

```
project/
├── app/
│   ├── api/
│   │   ├── routes.py              # FastAPI route definitions
│   │   └── models.py              # Request/Response Pydantic models
│   ├── services/
│   │   ├── pdf_service.py         # PDF upload & file management
│   │   ├── chunking_service.py    # Text chunking orchestration
│   │   ├── embedding_service.py   # Embedding generation
│   │   ├── vector_service.py      # ChromaDB operations
│   │   └── llm_service.py         # Ollama LLM interaction
│   ├── embeddings/
│   │   └── generator.py           # Embedding generator wrapper
│   ├── chunking/
│   │   └── splitter.py            # Chunk splitting strategies
│   ├── pdf/
│   │   ├── extractor.py           # PdfPlumber text extraction
│   │   └── cleaner.py             # Text cleaning & normalization
│   ├── rag/
│   │   ├── pipeline.py            # Full RAG orchestration
│   │   └── retriever.py           # Retrieval & re-ranking logic
│   ├── models/
│   │   └── schemas.py             # Shared Pydantic data models
│   └── utils/
│       ├── config.py              # Config loader (YAML + .env)
│       ├── logger.py              # Logging setup
│       └── validators.py          # Input validators
├── chroma_db/
│   └── collections/               # Persisted ChromaDB vector data
├── uploads/
│   ├── pdfs/                      # Stored original PDFs
│   └── temp/                      # Temporary processing files
├── logs/
│   ├── app.log
│   └── error.log
├── tests/
│   ├── unit/                      # Unit test modules
│   └── integration/               # End-to-end pipeline tests
├── requirements.txt
├── main.py                        # FastAPI app entrypoint
├── config.yaml                    # Application configuration
├── .env.example                   # Environment variable template
├── Dockerfile
├── docker-compose.yaml
└── README.md
```

---

## 9. 🔄 Retrieval Flow

```
👤 User
  │
  ▼
❓ Question Input
  │
  ▼
🔢 Embedding (nomic-embed-text)
  │
  ▼
💾 ChromaDB Similarity Search
  │
  ▼
📦 Top 5 Chunks Retrieved
  │
  ▼
📝 Prompt Builder (Context + Question)
  │
  ▼
🧠 Mistral LLM
  │
  ▼
💬 Answer with Source Citations
```

---

## 10. 🏷️ Metadata Filtering

**Supported Filter Fields:**

| Filter | Type | Example Value |
|--------|------|---------------|
| `company` | String | `"ABC"` |
| `year` | Integer | `2024` |
| `document` | String | `"AnnualReport2024.pdf"` |
| `department` | String | `"Finance"` |
| `reportType` | String | `"Annual"` |

**📌 Example Filter Query:**
```
company = "ABC" AND year = 2024
```

> Only chunks matching the applied filter are included in the similarity search.

---

## 11. ⚡ Performance Goals

| Metric | Target |
|--------|--------|
| ⬆️ Upload Time | < 30 seconds per document |
| 🔢 Embedding Speed | ≥ 100 chunks / second |
| 🔍 Search Latency | < 100 ms |
| 🧠 LLM Answer Time | 2 – 5 seconds |
| 📈 Scale Support | 1,000+ PDFs |

---

## 12. 🛡️ Error Handling

| Error Type | HTTP Code | Strategy |
|------------|-----------|----------|
| ❌ Invalid PDF | `400` | Return error with validation details |
| 🔁 Duplicate Upload | `409` | Skip or overwrite with user confirmation |
| 💥 Corrupted File | `422` | Log error, reject upload |
| 🔢 Embedding Failure | `500` | Retry with exponential backoff (max 3 attempts) |
| ⏱️ LLM Timeout | `504` | Return partial answer or timeout message |
| 💾 Chroma Unavailable | `503` | Graceful degradation with structured error response |

---

## 13. 📊 Logging

### 📋 Log Events

- ⬆️ Upload timestamp and document details
- ✂️ Chunk count per document
- 🔢 Embedding generation duration
- 🔍 Search query and total response time
- 📦 Retrieved chunk count and top scores
- 🧠 LLM response time and token count
- ❌ Error details with full stack traces

### 🎚️ Log Levels

| Level | Usage |
|-------|-------|
| `INFO` | Successful operations |
| `WARNING` | Minor issues (retries, fallbacks) |
| `ERROR` | Failed operations requiring attention |
| `DEBUG` | Detailed execution flow (dev/staging only) |

---

## 14. 🚀 Future Enhancements

### Phase 2 — 🔡 OCR Support
- Tesseract OCR integration
- PaddleOCR support
- Full scanned PDF processing

### Phase 3 — 🔀 Hybrid Retrieval
- Vector search + BM25 keyword search (dense + sparse)
- Reranking with cross-encoder models
- Improved precision and recall

### Phase 4 — 📂 Multi-Format Support
- DOCX documents
- Excel spreadsheets
- PowerPoint presentations
- HTML pages
- Markdown files

### Phase 5 — 🌟 Advanced Features
- Incremental indexing (re-process only changed sections)
- Multi-user collections with RBAC
- Streaming LLM responses (Server-Sent Events)
- Citation deep-linking to source pages
- SQL-based AI assistant integration
- Hybrid database + PDF question answering

---

## 15. 🛠️ Installation & Setup

### ✅ Prerequisites

```bash
# Install Python 3.12+

# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull mistral
ollama pull nomic-embed-text
```

### 🚀 Project Setup

```bash
# Clone repository
git clone <repository_url>
cd pdf-knowledge-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run the application
uvicorn main:app --reload
```

### 📦 `requirements.txt`

```txt
fastapi==0.104.1
uvicorn==0.24.0
chromadb==0.4.22
pdfplumber==0.10.3
pypdf==3.17.4
langchain==0.1.0
pypdfium2==4.18.1
sqlalchemy==2.0.23
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
aiofiles==23.2.1
httpx==0.25.0
```

---

## 16. ⚙️ Configuration Parameters

**`config.yaml`:**
```yaml
app:
  name: "PDF Knowledge Assistant"
  version: "1.0.0"
  debug: true

pdf:
  max_size_mb: 100
  allowed_extensions: [".pdf"]
  extraction:
    use_pdfplumber: true
    fallback_pypdf: true

chunking:
  chunk_size: 500
  chunk_overlap: 100
  min_chunk_size: 50

embeddings:
  model: "nomic-embed-text"
  dimension: 768
  ollama_endpoint: "http://localhost:11434"

chromadb:
  collection_name: "company_documents"
  persist_directory: "./chroma_db"
  batch_size: 100

llm:
  model: "mistral"
  temperature: 0.1
  max_tokens: 500
  timeout_seconds: 30

search:
  top_k: 5
  similarity_threshold: 0.3
  use_metadata_filters: true

logging:
  level: "INFO"
  file: "./logs/app.log"
  max_size_mb: 100
  backup_count: 5
```

---

## 17. 🔐 Security Considerations

- 🏠 Local-only operation (zero cloud dependencies)
- 🔍 File type and size validation on every upload
- 🛡️ Input sanitization for all search queries
- 🚫 No external API calls made at any time
- 📁 Local file storage with proper OS-level permissions
- 🔒 SQLite database encryption (optional, Phase 2)

---

## 18. 🧪 Testing Strategy

### 🔬 Unit Tests
- PDF extraction functions
- Chunking algorithms
- Embedding generation
- ChromaDB CRUD operations

### 🔗 Integration Tests
- Full upload-to-answer pipeline
- Document management operations
- Error handling and edge cases

### ⚡ Performance Tests
- Load testing with concurrent PDF uploads
- Search latency benchmarks
- Memory usage profiling

### 📂 Sample Test Data

| Category | Description |
|----------|-------------|
| 📄 Small | 1–5 pages |
| 📋 Medium | 50–100 pages |
| 📚 Large | 500+ pages |
| 💥 Corrupted | Invalid or truncated PDF |
| 🔒 Protected | Password-protected PDFs |

---

## 19. 📈 Monitoring & Maintenance

### 🩺 System Health Checks

- 💾 ChromaDB connection status
- 🧠 Ollama service availability
- 💿 Disk space monitoring
- 🖥️ Memory usage tracking

### 🔧 Maintenance Tasks

- 🗜️ Database compaction
- 📋 Log rotation (configured via `backup_count`)
- 💾 Regular backup of ChromaDB vector store
- ⚡ Index optimization

---

## 20. 📖 Documentation

- 🔌 API documentation via OpenAPI/Swagger (`/docs`)
- 📘 User guide — setup and configuration
- 👨‍💻 Developer guide — custom extensions and service layer
- 🐛 Troubleshooting guide
- ⚡ Performance tuning guide

---

## 21. 📊 Success Metrics

| Metric | Target |
|--------|--------|
| 🎯 Accuracy | Correct answer rate > 85% on benchmark queries |
| ⚡ Speed | Average search latency < 100ms |
| ✅ Reliability | System uptime > 99% |
| 📈 Scalability | Handles 10,000+ PDFs without degradation |
| 😊 User Satisfaction | Response quality rating > 4.5 / 5 |

---

## 22. ⚠️ Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 🤥 LLM Hallucination | High | Strict prompt engineering; context-only answers enforced |
| 💾 Memory Overload | High | Batch processing; garbage collection; configurable memory limits |
| 🐢 Slow Embedding | Medium | GPU acceleration; embedding result caching |
| 💥 Data Corruption | High | Regular backups; ChromaDB integrity checks |
| 🔧 Compatibility Issues | Medium | Docker containerization; strict version pinning |

---

