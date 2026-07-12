# 🚀 Sprint 3 — Search API & RAG Pipeline — Change Log

**Sprint**: 3 — Search API & End-to-End RAG Pipeline  
**Date**: July 2026  
**Status**: ✅ Code Generation Complete

---

## 📌 Summary

Sprint 3 enhances the existing Sprint 2 foundation (chunking, embeddings, ChromaDB, basic RAG stubs) into a **fully functional, production-grade Search API and RAG pipeline**. Key additions include result re-ranking, prompt templates, response caching, multi-turn chat, document summarization, streaming responses, and graceful timeout handling.

---

## 📊 Sprint 3 By The Numbers

| Metric | Value |
|--------|-------|
| **New Python Files** | 7 |
| **Modified Python Files** | 9 |
| **Modified Config Files** | 2 |
| **New API Endpoints** | 3 |
| **Enhanced API Endpoints** | 2 |
| **New Unit Tests** | ~25 test cases |
| **New Integration Tests** | ~10 test cases |
| **New Pydantic Models** | 6 |
| **New Config Properties** | 7 |

---

## 🆕 New Files Created

### 1. `app/rag/ranker.py` — Result Re-Ranking

**Purpose**: Re-orders retrieved chunks before injecting them into the LLM prompt to improve answer quality.

**3 strategies available** (configurable via `config.yaml`):

| Strategy | Description |
|----------|-------------|
| `score_based` (default) | Sort by raw cosine similarity score descending |
| `recency_bias` | Boost documents from recent years (up to +10% for current year) |
| `diversity_aware` | Penalize multiple chunks from the same page/document to diversify context |

```python
from app.rag.ranker import ResultRanker

ranker = ResultRanker(strategy="diversity_aware")
ranked = ranker.rank(retrieved_chunks)
```

---

### 2. `app/rag/prompt_templates.py` — Prompt Template System

**Purpose**: Clean separation of prompt engineering from business logic. Provides reusable templates with `{variable}` injection.

**3 predefined templates**:

| Template | Use Case |
|----------|----------|
| `QA_TEMPLATE` | Factual question answering with context |
| `SUMMARY_TEMPLATE` | Document summarization |
| `CHAT_TEMPLATE` | Multi-turn conversation with history |

```python
from app.rag.prompt_templates import PromptTemplate

# Quick usage
prompt = PromptTemplate.build_qa_prompt("What is revenue?", ["Revenue was $10M."])
prompt = PromptTemplate.build_chat_prompt("Follow up?", chunks, history)
prompt = PromptTemplate.build_summary_prompt(chunks)

# Custom template
t = PromptTemplate(template="Q: {question}\nA:")
rendered = t.render(question="What is AI?")
```

---

### 3. `app/rag/cache.py` — Response Cache (LRU + TTL)

**Purpose**: Avoids redundant LLM calls for repeated or similar queries. Stores responses in-memory with automatic eviction.

**Features**:
- SHA-256 hash of `(query + filters)` as cache key
- Case-insensitive query matching
- Configurable max entries (LRU eviction when full)
- Configurable TTL (time-to-live) expiry per entry
- Cache hit/miss statistics tracking
- Enable/disable via config

```python
from app.rag.cache import response_cache

# Automatic — pipeline uses it internally
# Manual usage:
response_cache.set("query", {"answer": "..."})
cached = response_cache.get("query")  # Returns None on miss/expiry
stats = response_cache.get_stats()    # {"hits": 5, "misses": 2, ...}
```

---

### 4. `tests/unit/test_ranker.py` — Ranker Unit Tests

**11 test cases** covering:
- Score-based sorting (descending)
- Recency bias boost for recent documents
- Missing year metadata handling
- Score capped at 1.0
- Diversity-aware penalty for same-page chunks
- Different documents receive no penalty
- Empty input handling

---

### 5. `tests/unit/test_prompt_templates.py` — Template Unit Tests

**8 test cases** covering:
- QA template rendering with chunks
- Summary template rendering
- Chat template with conversation history
- Chat template without history (fallback text)
- Custom template rendering
- Missing variable raises `ValueError`
- Empty context chunks

---

### 6. `tests/unit/test_response_cache.py` — Cache Unit Tests

**12 test cases** covering:
- Basic set/get operations
- Cache miss returns `None`
- Case-insensitive key matching
- Filters affect cache key
- TTL expiry returns `None`
- Non-expired entries work
- LRU eviction of oldest entry
- Access refreshes LRU position
- Disabled cache always misses
- Statistics tracking (hits, misses, hit rate)
- Clear all entries
- Invalidate specific entry

---

### 7. `tests/integration/test_rag_chat_api.py` — Chat & Summarize API Tests

**9 test cases** covering:
- `POST /rag/chat` success with conversation history
- `POST /rag/chat` empty message rejected (422)
- `POST /rag/chat` message too long rejected (422)
- `POST /rag/summarize` success
- `POST /rag/summarize` missing document_id rejected (422)
- `POST /rag/query` with score_threshold parameter
- `POST /rag/query` response includes timing breakdown
- `POST /rag/query` cached response flag

---

## ✏️ Modified Files

### 8. `config.yaml` — New Configuration Keys

```yaml
# NEW in Sprint 3:
rag:
  ranker:
    strategy: "score_based"        # NEW — "score_based", "recency_bias", "diversity_aware"
  generator:
    timeout_seconds: 120           # NEW — graceful LLM timeout
    system_prompt: "You are..."    # NEW — configurable system prompt
  cache:
    enabled: true                  # NEW — response caching on/off
    max_entries: 100               # NEW — LRU cache max size
    ttl_seconds: 3600              # NEW — cache entry lifetime
```

---

### 9. `app/utils/config.py` — 7 New Config Properties

| Property | Type | Default |
|----------|------|---------|
| `rag_generator_timeout_seconds` | `int` | `120` |
| `rag_generator_system_prompt` | `str` | (system prompt text) |
| `rag_ranker_strategy` | `str` | `"score_based"` |
| `rag_cache_enabled` | `bool` | `True` |
| `rag_cache_max_entries` | `int` | `100` |
| `rag_cache_ttl_seconds` | `int` | `3600` |

---

### 10. `app/rag/retriever.py` — Metadata Enrichment

**Change**: After threshold filtering, the retriever now enriches each chunk's metadata with `original_filename` (copied from `filename`) if missing. This ensures downstream components (pipeline, API) always have consistent filename metadata for source citations.

---

### 11. `app/rag/generator.py` — Major Enhancements

| Feature | Description |
|---------|-------------|
| **Prompt Templates** | Uses `PromptTemplate` system instead of hardcoded strings |
| **Multi-turn Chat** | New `_build_chat_prompt()` using `CHAT_TEMPLATE` with history |
| **Summarization** | New `generate_summary()` method with `SUMMARY_TEMPLATE` |
| **Graceful Timeout** | Uses `asyncio.wait_for()` with configurable timeout; returns friendly message on timeout instead of crashing |
| **Streaming** | New `generate_streaming_response()` async generator for SSE token-by-token output |

---

### 12. `app/rag/pipeline.py` — Major Enhancements

| Feature | Description |
|---------|-------------|
| **Ranking Step** | Calls `ResultRanker.rank()` between retrieval and generation |
| **Response Caching** | Checks cache before retrieval; stores results after generation |
| **`chat()` method** | Multi-turn conversation with history passed to generator |
| **`summarize()` method** | Document-level summarization: retrieves all chunks for a doc, sorts by page, generates summary |
| **Timing Breakdown** | Response includes `retrieval_time_ms`, `generation_time_ms`, `response_time_ms`, `cached` flag |
| **`_format_sources()` helper** | Extracted source citation formatting into reusable method |

---

### 13. `app/rag/__init__.py` — New Exports

Added: `ResultRanker`, `ResponseCache`, `response_cache`, `PromptTemplate`

---

### 14. `app/models/schemas.py` — 6 New Pydantic Models

| Model | Purpose |
|-------|---------|
| `ChatMessage` | Single message with `role` + `content` |
| `ChatRequest` | Multi-turn chat request (message, history, filters, top_k, score_threshold) |
| `ChatResponse` | Chat response (answer, sources, query, timing) |
| `SummarizeRequest` | Summarization request (document_id, filters, max_chunks) |
| `SummarizeResponse` | Summary response (summary, document_id, chunks_used, timing) |

**Modified models**:
- `SearchRequest` — Added optional `score_threshold` field
- `SearchResponse` — Added `retrieval_time_ms`, `generation_time_ms`, `cached` fields

---

### 15. `app/api/rag.py` — 3 New Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/rag/chat` | POST | Multi-turn conversation with history and RAG context |
| `/rag/summarize` | POST | Generate summary of a specific indexed document |
| `/rag/stream` | POST | Stream RAG response via Server-Sent Events (SSE) |

**Enhanced**: `/rag/query` now passes `score_threshold` to pipeline.

---

### 16. `app/api/search.py` — Score Threshold & Logging

- Added `score_threshold` pass-through from `SearchRequest` to retriever
- Added filter logging when metadata filters are applied
- Improved result count logging

---

### 17. `app/api/deps.py` — New Singletons

- Added `ResultRanker` singleton (`ranker_service`)
- Wired `ranker_service` and `response_cache` into `RAGPipeline` constructor
- Added `get_ranker_service()` dependency getter

---

### 18. `main.py` — Enhanced Startup Logging

Added 4 new log lines at startup:
```
[INFO] RAG Ranker strategy: score_based
[INFO] RAG Cache enabled: True
[INFO] RAG Generator model: mistral
[INFO] RAG Generator timeout: 120s
```

---

### 19. `tests/unit/test_rag_pipeline.py` — Updated for Sprint 3

- Updated `RAGPipeline` constructor to pass `ranker` and `cache=None`
- Added assertions for `retrieval_time_ms`, `generation_time_ms`, `cached`
- Added `test_pipeline_chat()` — tests multi-turn chat method
- Added `test_pipeline_summarize()` — tests document summarization method

---

## 🔌 API Endpoints Summary (After Sprint 3)

### Health & Info
```
GET  /              → Application info & version
GET  /health        → Health check for monitoring
```

### Document Management (Sprint 1)
```
POST   /documents/upload         → Upload PDF with validation
GET    /documents                → List all documents
GET    /documents/stats          → System-wide statistics
DELETE /documents/{id}           → Delete document and files
POST   /documents/reindex/{id}   → Reindex document
```

### Search (Sprint 2 + Sprint 3 enhancements)
```
POST /search                     → Semantic search with score_threshold
```

### RAG (Sprint 2 base + Sprint 3 new)
```
POST /rag/query                  → RAG Q&A with score_threshold + timing + caching
POST /rag/chat        [NEW]      → Multi-turn conversation with history
POST /rag/summarize   [NEW]      → Document summarization
POST /rag/stream      [NEW]      → Streaming RAG response (SSE)
```

**Total: 12 endpoints** (6 Sprint 1 + 2 Sprint 2 + 4 Sprint 3 — with 2 Sprint 2 endpoints enhanced)

---

## ⚙️ Configuration Reference (After Sprint 3)

```yaml
rag:
  retriever:
    k: 5                    # Top K chunks to retrieve
    score_threshold: 0.3    # Minimum similarity score
  ranker:
    strategy: "score_based" # score_based | recency_bias | diversity_aware
  generator:
    model: "mistral"        # Ollama model for generation
    temperature: 0.7        # LLM creativity (0.0-1.0)
    max_tokens: 500         # Max output tokens
    timeout_seconds: 120    # Graceful timeout for LLM calls
    system_prompt: "..."    # Configurable system prompt
  cache:
    enabled: true           # Enable/disable response caching
    max_entries: 100        # Max cached responses (LRU eviction)
    ttl_seconds: 3600       # Cache entry lifetime (1 hour)
```

---

## 📁 File Structure (After Sprint 3)

```
app/rag/
├── __init__.py              ← Updated exports
├── cache.py                 ← NEW — Response cache (LRU + TTL)
├── generator.py             ← ENHANCED — Templates, chat, summary, streaming, timeout
├── pipeline.py              ← ENHANCED — Ranking, caching, chat(), summarize(), timing
├── prompt_templates.py      ← NEW — QA, Summary, Chat templates
├── ranker.py                ← NEW — Score/recency/diversity ranking strategies
└── retriever.py             ← ENHANCED — Metadata enrichment

app/api/
├── deps.py                  ← ENHANCED — Ranker + cache singletons
├── rag.py                   ← ENHANCED — chat, summarize, stream endpoints
└── search.py                ← ENHANCED — score_threshold support

app/models/
└── schemas.py               ← ENHANCED — 6 new models, enhanced SearchRequest/Response

tests/unit/
├── test_ranker.py           ← NEW — 11 tests
├── test_prompt_templates.py ← NEW — 8 tests
├── test_response_cache.py   ← NEW — 12 tests
└── test_rag_pipeline.py     ← UPDATED — 3 tests (query, chat, summarize)

tests/integration/
└── test_rag_chat_api.py     ← NEW — 9 tests
```

---

## 🔄 Request Flow (After Sprint 3)

```
Client Request
    ↓
FastAPI Router (/rag/query, /rag/chat, /rag/summarize, /rag/stream)
    ↓
RAGPipeline
    ├── [1] Check ResponseCache (hit? → return cached)
    ├── [2] Retriever → Embed query → ChromaDB similarity search → Filter by threshold
    ├── [3] ResultRanker → Re-rank by strategy (score/recency/diversity)
    ├── [4] Generator → Build prompt (QA/Chat/Summary template) → Ollama LLM → Response
    ├── [5] Format sources (document_id, filename, page, score, text)
    └── [6] Store in ResponseCache → Return result with timing breakdown
```

---

## 🧪 Test Coverage

### Unit Tests (Sprint 3 additions)

| File | Test Cases | Coverage Area |
|------|-----------|---------------|
| `test_ranker.py` | 11 | All 3 ranking strategies + edge cases |
| `test_prompt_templates.py` | 8 | QA/summary/chat templates + custom + errors |
| `test_response_cache.py` | 12 | Set/get, TTL, eviction, disabled, stats |
| `test_rag_pipeline.py` | 3 | query(), chat(), summarize() |

### Integration Tests (Sprint 3 additions)

| File | Test Cases | Coverage Area |
|------|-----------|---------------|
| `test_rag_chat_api.py` | 9 | /rag/chat, /rag/summarize, /rag/query enhancements |

**Sprint 3 Total: ~43 new/updated test cases**

---

## ✅ Sprint 3 Deliverables Checklist

- [x] Result re-ranking with 3 strategies
- [x] Prompt template system (QA, Summary, Chat)
- [x] Response caching with LRU + TTL
- [x] `POST /rag/chat` — Multi-turn conversations
- [x] `POST /rag/summarize` — Document summarization
- [x] `POST /rag/stream` — Streaming responses (SSE)
- [x] Graceful LLM timeout handling (`asyncio.wait_for`)
- [x] `score_threshold` support on search + RAG endpoints
- [x] Timing breakdown in responses (retrieval + generation + total)
- [x] Cache hit/miss flag in responses
- [x] Configurable system prompt
- [x] 7 new config properties
- [x] 6 new Pydantic models
- [x] 43+ new/updated test cases
- [x] Enhanced startup logging

---

**Sprint 3 Status**: ✅ Code Generation Complete  
**Next**: Sprint 4 — Document Management & Full Test Suite  
**Ready for**: Testing & verification (`pytest tests/ -v`)
