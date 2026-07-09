# 🚀 Sprint 2: Setup & Preparation Guide

## ✅ Current Status (End of Sprint 1)

### What's Complete
- ✅ **Project Structure**: Fully organized modular architecture
- ✅ **Configuration Management**: YAML config + environment variables
- ✅ **Structured Logging**: Production-ready logger
- ✅ **PDF Processing**: Text extraction (pdfplumber + pypdf) and cleaning
- ✅ **Input Validation**: Pydantic schemas and custom validators
- ✅ **FastAPI API**: Document management endpoints (upload, list, retrieve)
- ✅ **Testing**: Unit and integration tests with pytest
- ✅ **Documentation**: README, QUICK_START, installation guide
- ✅ **Dependencies**: All packages properly configured in requirements.txt

### Dependency Status
All dependencies are **production-ready**:
```
✅ fastapi >= 0.104.0
✅ uvicorn >= 0.24.0
✅ pdfplumber >= 0.10.0 (PDF extraction)
✅ pypdf >= 4.0.0 (PDF fallback)
✅ pydantic >= 2.5.0
✅ pyyaml >= 6.0
✅ chromadb >= 0.5.0
✅ langchain >= 0.1.0
✅ pytest >= 7.4.0 (testing)
❌ pypdfium2 (REMOVED - no longer needed)
```

## 🎯 Sprint 2 Objectives

### Phase 1: Text Chunking & Processing
- [ ] Implement text chunking strategies
- [ ] Create chunking service module
- [ ] Add tests for chunking logic
- [ ] Document chunking configuration

### Phase 2: Embedding Generation (Ollama)
- [ ] Setup Ollama integration
- [ ] Create embedding service
- [ ] Add Ollama configuration
- [ ] Create embedding cache

### Phase 3: ChromaDB Vector Storage
- [ ] Initialize ChromaDB
- [ ] Create vector storage service
- [ ] Add persistence layer
- [ ] Create collection management

### Phase 4: Vector Search & RAG Pipeline
- [ ] Implement semantic search
- [ ] Create RAG pipeline service
- [ ] Add search endpoints to API
- [ ] Create end-to-end workflow

## 📋 Before Starting Sprint 2

### Step 1: Verify Current Installation
```bash
# Navigate to project
cd "i:\Pro Hero\ai\document-intelligence-service"

# Create/activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run verification
python verify_installation.py
```

### Step 2: Verify No Dependency Conflicts
```bash
pip check
```

Expected output: `No broken requirements found.`

### Step 3: Run Existing Tests
```bash
pytest -v
```

All tests should pass ✅

### Step 4: Start Development Server (Optional Test)
```bash
python -m uvicorn main:app --reload
```

Server should start on `http://localhost:8000`

## 📁 Sprint 2 Module Structure

```
app/
├── chunking/              # NEW - Text chunking logic
│   ├── __init__.py
│   ├── strategies.py      # Different chunking strategies
│   ├── splitter.py        # Main chunking service
│   └── cache.py           # Caching for chunks
├── embeddings/            # NEW - Embedding generation
│   ├── __init__.py
│   ├── ollama_service.py  # Ollama integration
│   ├── client.py          # Ollama client wrapper
│   └── cache.py           # Embedding cache
├── vector_store/          # NEW - Vector storage
│   ├── __init__.py
│   ├── chromadb_service.py # ChromaDB wrapper
│   ├── collection.py      # Collection management
│   └── persistence.py     # Save/load collections
├── rag/                   # NEW - RAG pipeline
│   ├── __init__.py
│   ├── pipeline.py        # Main RAG pipeline
│   ├── retriever.py       # Retrieval logic
│   └── generator.py       # Response generation
├── api/
│   ├── __init__.py
│   ├── routes.py          # Document routes (Sprint 1)
│   ├── search.py          # NEW - Search endpoints
│   └── rag.py             # NEW - RAG endpoints
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic models
├── utils/
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── logger.py          # Logging
│   └── validators.py      # Validation
└── pdf/
    ├── __init__.py
    ├── extractor.py       # PDF extraction (Sprint 1)
    └── cleaner.py         # Text cleaning (Sprint 1)

tests/
├── unit/
│   ├── test_chunking.py    # NEW
│   ├── test_embeddings.py  # NEW
│   ├── test_vector_store.py # NEW
│   ├── test_rag_pipeline.py # NEW
│   ├── test_pdf.py         # Sprint 1
│   └── test_validators.py  # Sprint 1
└── integration/
    ├── test_chunking_integration.py # NEW
    ├── test_embeddings_integration.py # NEW
    ├── test_search_api.py  # NEW
    ├── test_rag_workflow.py # NEW
    └── test_api.py         # Sprint 1
```

## 🔧 Configuration Updates Needed for Sprint 2

Update `config.yaml` with new sections:

```yaml
# CHUNKING
chunking:
  strategy: "recursive"  # Options: "fixed", "recursive", "semantic"
  chunk_size: 1000
  overlap: 200
  min_chunk_size: 100

# EMBEDDINGS (Ollama)
embeddings:
  provider: "ollama"
  model: "nomic-embed-text"  # or "mistral", "neural-chat"
  base_url: "http://localhost:11434"
  timeout: 60
  cache_embeddings: true

# VECTOR STORE (ChromaDB)
vector_store:
  db_path: "./chroma_db"
  collection_name: "documents"
  distance_metric: "cosine"  # Options: "cosine", "l2", "ip"
  persist_directory: "./chroma_db"

# RAG PIPELINE
rag:
  retriever:
    k: 5  # Number of chunks to retrieve
    score_threshold: 0.5
  generator:
    model: "mistral"  # Ollama model for generation
    temperature: 0.7
    max_tokens: 500
```

## 🚀 Getting Started with Sprint 2

### Quick Start Commands

```bash
# 1. Activate environment
cd "i:\Pro Hero\ai\document-intelligence-service"
venv\Scripts\activate

# 2. Verify installation
python verify_installation.py

# 3. Run tests
pytest -v

# 4. Start server
python -m uvicorn main:app --reload --port 8000
```

### Development Workflow

1. **Create feature branch**: `git checkout -b sprint-2-chunking`
2. **Implement module**: Write code in `app/chunking/`
3. **Write tests**: Add tests in `tests/unit/` and `tests/integration/`
4. **Run tests**: `pytest -v`
5. **Commit changes**: `git add . && git commit -m "feat: add chunking"`

## 📊 Sprint 2 Implementation Order

### Week 1: Text Chunking
1. Create `app/chunking/strategies.py` - Define chunking strategies
2. Create `app/chunking/splitter.py` - Main chunking service
3. Add unit tests for chunking
4. Add integration tests with PDF extraction
5. Update API with chunking endpoints

### Week 2: Embeddings with Ollama
1. Create `app/embeddings/ollama_service.py` - Ollama integration
2. Create `app/embeddings/cache.py` - Embedding caching
3. Add unit tests for embeddings
4. Add integration tests with Ollama
5. Create embedding management API

### Week 3: ChromaDB Vector Storage
1. Create `app/vector_store/chromadb_service.py` - ChromaDB wrapper
2. Create `app/vector_store/collection.py` - Collection management
3. Add persistence layer
4. Add unit tests for vector storage
5. Add integration tests with ChromaDB

### Week 4: RAG Pipeline & Search
1. Create `app/rag/pipeline.py` - Main RAG pipeline
2. Create `app/rag/retriever.py` - Retrieval logic
3. Add search API endpoints
4. Add end-to-end tests
5. Create RAG workflow documentation

## 🔗 Dependencies Already Installed

These packages from Sprint 1 will support Sprint 2:

```
chromadb >= 0.5.0      # Vector database
langchain >= 0.1.0     # LLM orchestration (optional)
pydantic >= 2.5.0      # Data validation
fastapi >= 0.104.0     # API framework
```

### Additional Ollama Setup (Manual)

You'll need to download and run Ollama separately:

```bash
# Install from https://ollama.ai
# Then run in terminal:
ollama pull nomic-embed-text  # For embeddings
ollama pull mistral            # For generation
ollama serve                   # Start Ollama server (http://localhost:11434)
```

## ✅ Checklist for Sprint 2 Start

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] No conflicts (`pip check`)
- [ ] Sprint 1 tests passing (`pytest -v`)
- [ ] Server starts (`uvicorn main:app --reload`)
- [ ] Configuration updated with new Sprint 2 sections
- [ ] Ollama downloaded and tested locally
- [ ] Git branch created for Sprint 2
- [ ] Project structure updated (directories created)

## 📝 Next Actions

1. **Immediate**: Follow verification steps in "Before Starting Sprint 2"
2. **Today**: Create Sprint 2 git branch and update config.yaml
3. **Tomorrow**: Begin implementation of text chunking module
4. **This week**: Complete Phase 1 (Text Chunking)
5. **Ongoing**: Maintain test coverage at >80%

## 📚 Documentation to Reference

- `README.md` - Project overview
- `QUICK_START.md` - Installation & setup
- `INSTALLATION_GUIDE.md` - Detailed install steps
- `FILE_INDEX.md` - File organization
- `FINAL_STATUS.md` - Sprint 1 completion details

## 🎓 Resources for Sprint 2

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Advanced Features](https://fastapi.tiangolo.com/advanced/)
- [Pydantic V2 Guide](https://docs.pydantic.dev/latest/)

---

**Status**: Ready for Sprint 2 ✅  
**Last Updated**: Sprint 1 Complete  
**Next Milestone**: Sprint 2 - Text Chunking & Embeddings
