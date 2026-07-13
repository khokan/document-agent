# Backend Documentation

Essential documentation for the PDF Knowledge Assistant RAG Engine backend.

---

## 📖 Documentation Index

### Getting Started
- **[QUICK_START.md](./QUICK_START.md)** ⭐ — Start here! One-command setup and testing guide

### Setup & Installation
- **[INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md)** — Detailed installation steps and troubleshooting

### Project Reference
- **[prd.md](./prd.md)** — Product Requirements Document (complete specifications)
- **[ROADMAP.md](./ROADMAP.md)** — Project roadmap and future enhancements

---

## 🚀 Quick Navigation

### For New Developers
1. **Start:** [QUICK_START.md](./QUICK_START.md) (5 minutes)
2. **Install:** [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md) (10 minutes)
3. **Understand:** [prd.md](./prd.md) (reference as needed)

### For Understanding the Project
→ [prd.md](./prd.md) - Complete product requirements and design

### For Future Development
→ [ROADMAP.md](./ROADMAP.md) - Planned features and enhancements

---

## 📋 What's Included

| File | Purpose | When to Read |
|------|---------|--------------|
| **QUICK_START.md** | One-command setup & testing | First time setup |
| **INSTALLATION_GUIDE.md** | Detailed install steps | Troubleshooting setup |
| **prd.md** | Complete project specs | Understanding requirements |
| **ROADMAP.md** | Future enhancements | Planning new features |

---

## ⚡ Quick Commands

```bash
# Setup (Windows)
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python main.py

# Setup (Linux/macOS)
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py

# Test
pytest --cov=app tests/ -v
```

---

## 🎯 Key Files

- **`main.py`** — FastAPI application entry point
- **`config.yaml`** — Application configuration
- **`requirements.txt`** — Python dependencies
- **`.env.example`** — Environment variables template

---

## 📁 Backend Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── config.yaml             # Configuration
├── requirements.txt        # Dependencies
├── pytest.ini              # Test configuration
├── docs/                   # Documentation (you are here)
├── app/
│   ├── main.py
│   ├── api/               # API routes
│   ├── models/            # Pydantic schemas
│   ├── services/          # Business logic
│   ├── pdf/               # PDF processing
│   ├── embeddings/        # Embedding services
│   ├── vector_store/      # ChromaDB integration
│   ├── rag/               # RAG pipeline
│   ├── chunking/          # Text chunking
│   └── utils/             # Utilities
├── tests/                 # Test files
└── uploads/               # PDF upload directory
```

---

## ✨ Features

- ✅ FastAPI web server
- ✅ PDF text extraction and processing
- ✅ Vector embeddings (Ollama)
- ✅ ChromaDB vector store
- ✅ Natural language semantic search
- ✅ RAG pipeline implementation
- ✅ Comprehensive API endpoints
- ✅ Error handling & logging

---

## 🔧 Requirements

- Python 3.8+
- pip package manager
- Virtual environment recommended

---

## 🎓 Learn More

For complete project specifications, see [prd.md](./prd.md)

---

**Last Updated:** July 2026  
**Status:** ✅ Complete  
**Ready for Development:** YES
