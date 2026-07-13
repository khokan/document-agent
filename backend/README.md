# 📄 PDF Knowledge Assistant - RAG Engine

> **Local Retrieval-Augmented Generation (RAG) System for Document Intelligence**

A production-grade, locally-hosted PDF document analysis system powered by vector embeddings, semantic search, and large language models. Built with Python, FastAPI, ChromaDB, and Ollama.

## ✨ Features

- 📤 **Single & Batch PDF Upload** — Upload documents with drag-and-drop support
- 📑 **Intelligent Text Extraction** — PdfPlumber with PyPDF fallback
- ✂️ **Smart Chunking** — 500-word chunks with 100-word overlap
- 🔢 **Vector Embeddings** — nomic-embed-text (768-dimensional vectors)
- 💾 **Vector Database** — ChromaDB for fast semantic search (<100ms)
- 🧠 **LLM Integration** — Mistral via Ollama for context-aware answers
- 🔍 **Metadata Filtering** — Filter by company, year, document, department
- 📊 **Source Citations** — Every answer includes page numbers and scores
- 🏠 **Fully Offline** — Zero cloud dependencies, all local processing

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Ollama** — [Install here](https://ollama.ai)
- **Git**

### Installation

```bash
# 1. Clone the repository
git clone <repository_url>
cd pdf-knowledge-assistant

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate              # Linux/macOS
# venv\Scripts\activate               # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup Ollama models
ollama pull mistral
ollama pull nomic-embed-text

# 5. Configure environment
cp .env.example .env
# Edit .env with your settings (optional, defaults work fine)

# 6. Run the application
python main.py
# Or with Uvicorn directly:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at **http://localhost:8000**

### 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/unit/test_pdf.py
```

## 📋 API Endpoints

### 📤 Upload PDF
```http
POST /documents/upload
Content-Type: multipart/form-data

# File parameter: file (binary PDF)
```

**Response:**
```json
{
  "document_id": "AnnualReport2024_a1b2c3d4",
  "filename": "AnnualReport2024.pdf",
  "upload_date": "2024-07-09T10:30:00",
  "status": "indexed",
  "chunk_count": 142
}
```

### 🔍 Search Documents
```http
POST /search
Content-Type: application/json

{
  "question": "Why did revenue increase?",
  "filters": {
    "company": "ABC",
    "year": 2024
  },
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Revenue increased by 25% due to expanded market reach and improved operational efficiency...",
  "sources": [
    {
      "document_id": "AnnualReport2024_a1b2c3d4",
      "filename": "AnnualReport2024.pdf",
      "page": 34,
      "score": 0.95,
      "text": "Revenue increased..."
    }
  ],
  "query": "Why did revenue increase?",
  "response_time_ms": 2341.5
}
```

### 📋 List Documents
```http
GET /documents
```

### 🗑️ Delete Document
```http
DELETE /documents/{document_id}
```

### 🔄 Reindex Document
```http
POST /documents/reindex/{document_id}
```

### 📊 System Statistics
```http
GET /documents/stats
```

### 🩺 Health Check
```http
GET /health
```

## 📁 Project Structure

```
project/
├── app/
│   ├── api/              # FastAPI routes
│   ├── services/         # Business logic services (Sprint 2+)
│   ├── pdf/              # PDF extraction & cleaning
│   ├── chunking/         # Text chunking (Sprint 2)
│   ├── embeddings/       # Embedding generation (Sprint 2)
│   ├── rag/              # RAG pipeline (Sprint 3)
│   ├── models/           # Pydantic schemas
│   └── utils/            # Config, logging, validators
├── uploads/              # Stored PDFs & temporary files
├── chroma_db/            # ChromaDB vector database
├── logs/                 # Application logs
├── tests/                # Unit & integration tests
├── main.py               # FastAPI application entry
├── config.yaml           # Configuration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── README.md            # This file
```

## ⚙️ Configuration

Edit `config.yaml` or set environment variables:

```yaml
app:
  name: "PDF Knowledge Assistant"
  debug: true

pdf:
  max_size_mb: 100

chunking:
  chunk_size: 500
  chunk_overlap: 100

embeddings:
  model: "nomic-embed-text"
  ollama_endpoint: "http://localhost:11434"

chromadb:
  collection_name: "company_documents"
  persist_directory: "./chroma_db"

llm:
  model: "mistral"
  temperature: 0.1
  max_tokens: 500
```

## 🎯 Performance Targets

| Metric | Target |
|--------|--------|
| ⬆️ Upload Time | < 30 seconds |
| 🔢 Embedding Speed | ≥ 100 chunks/sec |
| 🔍 Search Latency | < 100ms |
| 🧠 LLM Response | 2–5 seconds |
| 📈 Scale | 1,000+ PDFs |

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test
pytest tests/unit/test_pdf.py::TestPDFExtractor::test_extract_text_by_page_file_not_found

# Generate coverage report
pytest --cov=app tests/ --cov-report=html
# Open htmlcov/index.html in browser
```

## 📊 Logging

Logs are written to `./logs/app.log` with rotation:
- **INFO** — Normal operations
- **WARNING** — Minor issues or retries
- **ERROR** — Failed operations
- **DEBUG** — Detailed flow (dev mode)

```bash
# Tail logs in real-time
tail -f logs/app.log
```

## 🐳 Docker Setup

```bash
# Build image
docker build -t pdf-assistant:latest .

# Run container
docker run -p 8000:8000 -v $(pwd)/chroma_db:/app/chroma_db pdf-assistant:latest

# Or with docker-compose
docker-compose up
```

## 🚀 Development Roadmap

### Sprint 1 ✅ — Foundation & PDF Ingestion
- [x] Project structure
- [x] Config & logging
- [x] PDF upload & extraction
- [x] Text cleaning
- [x] API routes (upload, list, delete, stats)

### Sprint 2 — Chunking, Embeddings & ChromaDB
- [ ] Text chunking (500 words, 100 overlap)
- [ ] Ollama embedding integration
- [ ] ChromaDB collection management
- [ ] Vector storage & retrieval

### Sprint 3 — Search & RAG Pipeline
- [ ] POST /search endpoint
- [ ] Semantic similarity search
- [ ] Metadata filtering
- [ ] LLM answer generation
- [ ] Source citations

### Sprint 4 — Testing & Validation
- [ ] Full test suite (unit + integration)
- [ ] End-to-end pipeline tests
- [ ] Error handling validation
- [ ] ≥ 80% code coverage

### Sprint 5 — Production Hardening
- [ ] Performance benchmarking
- [ ] Security hardening
- [ ] Docker containerization
- [ ] Production deployment

## 🔐 Security

- ✅ Local-only operation (no cloud calls)
- ✅ File type & size validation
- ✅ Input sanitization
- ✅ OS-level file permissions

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Commit changes: `git commit -am 'Add new feature'`
3. Push: `git push origin feature/new-feature`
4. Open a Pull Request

## 📝 License

MIT License — see LICENSE file for details

## 📧 Support

For issues, questions, or suggestions:
- Open a GitHub issue
- Check existing documentation in `/docs`
- Review the implementation plan in `implementaion plan.md`

---

**Version:** 1.0.0 | **Last Updated:** July 2026 | **Status:** 🟢 Active Development
