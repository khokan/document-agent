# Fix: get_system_stats() Returns 0 but Search Shows 2 Documents

## Problem

- `GET /documents/stats` returns `total_documents: 0`
- But search queries find 2 documents in the database
- This indicates a **mismatch between in-memory tracking and persistent storage**

## Root Cause

The `DOCUMENTS_STORE` is an **in-memory Python dictionary** that:
- Gets populated when documents are uploaded
- Gets cleared when the app restarts
- Only tracks documents uploaded in **current session**

Meanwhile, ChromaDB **persistent vector store** contains:
- All chunks ever indexed (survives app restarts)
- Orphaned chunks from deleted documents
- Documents from previous app sessions

## Example Scenario

```
Session 1:
- Upload "Report.pdf" → DOCUMENTS_STORE = ["Report"], Vector DB = ["Report"] ✓

App Restart

Session 2:
- Fresh start → DOCUMENTS_STORE = {}, Vector DB = ["Report"] from session 1 ✗
- get_system_stats() returns 0 docs (only looks at DOCUMENTS_STORE)
- Search finds "Report" (queries Vector DB)
- Mismatch!
```

## Solution Implemented

### 1. Enhanced `get_system_stats()` Endpoint

Now **compares** tracked vs actual state and **warns about mismatches**:

```python
# Count from both sources
total_docs = len(DOCUMENTS_STORE)  # Tracked in memory
actual_docs_in_db = len(vector_doc_ids)  # Actual in vector store

# Log if there's a mismatch
if total_docs != actual_docs_in_db:
    logger.warning(
        f"[WARN] Document store mismatch detected:\n"
        f"  Tracked: {total_docs} docs\n"
        f"  Vector DB: {actual_docs_in_db} docs"
    )
```

**Server logs will now show:**
```
[WARN] Document store mismatch detected:
  Tracked: 0 docs, 0 chunks
  Vector DB: 2 docs, 45 chunks
```

### 2. New Health Check Endpoint

**Endpoint:** `GET /documents/health`

**Returns detailed diagnostic info:**
```json
{
  "status": "inconsistent",
  "tracked_documents": 0,
  "tracked_chunks": 0,
  "vector_db_documents": 2,
  "vector_db_chunks": 45,
  "orphaned_documents": ["Report2024", "AnnualReport"],
  "missing_documents": [],
  "is_consistent": false,
  "needs_cleanup": true,
  "tracked_doc_ids": [],
  "vector_doc_ids": ["Report2024", "AnnualReport"]
}
```

## How to Diagnose the Issue

### Step 1: Check Health Status

```bash
curl http://localhost:8000/documents/health
```

Look for:
- `"is_consistent": false` - indicates mismatch
- `"orphaned_documents"` - documents in DB but not tracked
- `"needs_cleanup": true` - should run cleanup

### Step 2: Check Stats

```bash
curl http://localhost:8000/documents/stats
```

Will now log warnings if mismatch detected:
```
[WARN] Document store mismatch detected:
  Tracked: 0 docs, 0 chunks
  Vector DB: 2 docs, 45 chunks
```

### Step 3: List Documents

```bash
curl http://localhost:8000/documents
```

If this returns empty list but health shows 2 docs in DB, you have orphaned chunks.

### Step 4: Cleanup Orphaned Documents

```bash
curl -X POST http://localhost:8000/documents/cleanup
```

Response:
```json
{
  "status": "success",
  "message": "Cleaned up 2 orphaned document(s)",
  "orphaned_documents": ["Report2024", "AnnualReport"]
}
```

### Step 5: Verify Consistency

```bash
curl http://localhost:8000/documents/health
```

Should now show:
```json
{
  "status": "healthy",
  "is_consistent": true,
  "needs_cleanup": false
}
```

## Why This Happens

| Scenario | Cause | Fix |
|----------|-------|-----|
| App restart | DOCUMENTS_STORE cleared | Sync on startup (already implemented) |
| Manual deletion | Chunks removed, store cleared | Auto-sync on startup |
| App crash | In-memory state lost | Auto-sync on startup |
| Bug in deletion | Chunks remain in DB | Run cleanup endpoint |
| Multiple app instances | Different DOCUMENTS_STORE copies | Use database instead of in-memory |

## Root Issue: In-Memory Store Problem

The real problem is using an **in-memory Python dictionary** for `DOCUMENTS_STORE`.

**Current Architecture:**
```
Python App Instance A
├── DOCUMENTS_STORE (RAM) 
└── ChromaDB (Disk) 

Restart App

Python App Instance B
├── DOCUMENTS_STORE = {} (empty!)
└── ChromaDB (Disk - still has old data)
```

**Better Architecture:**
```
PostgreSQL Database
├── Documents table
├── Chunks metadata
└── File mappings

Python App (any instance)
├── Load from database on startup
├── Query database for stats
└── ChromaDB (Disk - for embeddings)
```

## Files Modified

1. **`routes.py`**
   - Enhanced `get_system_stats()` to warn about mismatches
   - Added `GET /documents/health` diagnostic endpoint

## Prevention for the Future

To prevent this permanently, the backend should use a persistent database:

**Priority 1 (Quick):** Use SQLite instead of in-memory dict
```python
# Instead of: DOCUMENTS_STORE = {}
# Use: database.query("SELECT * FROM documents")
```

**Priority 2 (Better):** Use PostgreSQL for production
```python
# Persistent across app restarts and instances
# Supports concurrent access
# Better for scaling
```

## Testing Checklist

- [ ] `GET /documents/stats` shows correct counts
- [ ] `GET /documents/health` shows consistency status
- [ ] Mismatch warnings appear in logs
- [ ] `POST /documents/cleanup` removes orphaned docs
- [ ] After cleanup, health check shows `is_consistent: true`
- [ ] Search results match document count
- [ ] List endpoint shows same count as stats

## Quick Fixes You Can Run Now

### 1. Check Current State
```bash
curl http://localhost:8000/documents/health
```

### 2. If Inconsistent
```bash
curl -X POST http://localhost:8000/documents/cleanup
```

### 3. Verify Fixed
```bash
curl http://localhost:8000/documents/health
```

### 4. Restart App to Verify Persistence
```bash
# Stop and start the backend server
# Then check health again
curl http://localhost:8000/documents/health
```

## Long-Term Solution

For production, migrate from `DOCUMENTS_STORE = {}` to a proper database like PostgreSQL:

1. Create `documents` table with columns:
   - `id` (primary key)
   - `filename`
   - `upload_date`
   - `status`
   - `chunk_count`
   - `file_path`
   - `file_hash`

2. On startup: Query database instead of relying on in-memory dict

3. On upload: Insert into database

4. On delete: Remove from database

5. Stats endpoint: Query database, not in-memory dict

This will ensure stats are **always accurate** regardless of restarts.
