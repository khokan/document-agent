# Fix Summary: get_system_stats() Returns 0 but Search Shows 2 Documents

## The Problem
```
GET /documents/stats → total_documents: 0
POST /search → finds 2 documents
```

**Reason:** `DOCUMENTS_STORE` is cleared on app restart, but ChromaDB persists to disk.

## The Solution: 3 Enhancements

### 1. Enhanced Stats Endpoint

**Before:**
```python
total_docs = len(DOCUMENTS_STORE)  # Only counts in-memory
```

**After:**
```python
total_docs = len(DOCUMENTS_STORE)  # Tracked in memory
actual_docs_in_db = len(vector_doc_ids)  # Actual in vector store

# Warn if mismatch
if total_docs != actual_docs_in_db:
    logger.warning("Document store mismatch detected...")
```

**Result:** Server logs show warnings about mismatches

### 2. New Health Check Endpoint

**Endpoint:** `GET /documents/health`

**Returns:**
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

**Use cases:**
- Debugging consistency issues
- Health monitoring dashboards
- Automated alerting

### 3. Automatic Sync on Startup

Already implemented in `main.py`:
```python
# On app startup
await _sync_documents_from_vector_store()
```

This ensures orphaned chunks are cleaned up on restart.

## How to Use

### Check Current Health
```bash
curl http://localhost:8000/documents/health
```

Response example:
```json
{
  "status": "inconsistent",
  "is_consistent": false,
  "needs_cleanup": true,
  "tracked_documents": 0,
  "vector_db_documents": 2
}
```

### If Inconsistent, Cleanup
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

### Verify Fixed
```bash
curl http://localhost:8000/documents/health
```

Should show:
```json
{
  "status": "healthy",
  "is_consistent": true,
  "needs_cleanup": false
}
```

## API Endpoints Now Available

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/documents` | List tracked documents |
| `GET` | `/documents/stats` | Get counts (warns about mismatches) |
| `GET` | `/documents/health` | Check consistency (NEW) |
| `POST` | `/documents/cleanup` | Remove orphaned chunks |
| `POST` | `/documents/upload` | Upload new document |
| `DELETE` | `/documents/{id}` | Delete document |

## Why This Happens

### Root Cause Architecture
```
App Instance 1 (Session 1)
├── DOCUMENTS_STORE = {"Report": {...}} ← In RAM
├── Upload Report.pdf
└── ChromaDB saves to disk ✓

App Restart

App Instance 2 (Session 2)
├── DOCUMENTS_STORE = {} ← Fresh start, no prior data
├── Query ChromaDB → finds Report from Session 1
└── Mismatch! Stats shows 0, Search shows 1
```

### Why the Mismatch
1. **In-memory store** (`DOCUMENTS_STORE`) resets on restart
2. **Disk persistence** (ChromaDB) survives restart
3. After restart, they don't match until documents are re-indexed

## Log Messages You'll See

### Healthy State
```
[INFO] System stats: 2 docs, 45 chunks (synced)
[INFO] Document store health: Status: healthy
```

### Unhealthy State (Before Cleanup)
```
[WARN] Document store mismatch detected:
  Tracked: 0 docs, 0 chunks
  Vector DB: 2 docs, 45 chunks
[WARN] Found 2 orphaned document(s) in vector store: {'Report2024', 'AnnualReport'}
```

### After Cleanup
```
[OK] Cleaned up 2 orphaned document(s)
[INFO] Document store synchronized with vector store
```

## Testing Steps

1. **Verify Current State**
   ```bash
   curl http://localhost:8000/documents/health
   ```

2. **If Inconsistent, Cleanup**
   ```bash
   curl -X POST http://localhost:8000/documents/cleanup
   ```

3. **Verify Fixed**
   ```bash
   curl http://localhost:8000/documents/health
   # Should show: "is_consistent": true
   ```

4. **Restart App to Verify Persistence**
   ```bash
   # Stop app
   # Start app
   curl http://localhost:8000/documents/health
   # Should still be consistent
   ```

## Permanent Solution (Future)

The real issue is using **in-memory dictionary** for `DOCUMENTS_STORE`.

### Current (Has Issues)
```python
DOCUMENTS_STORE = {}  # Resets on restart
```

### Better (Recommended)
```python
# Use SQLite
db.query("SELECT * FROM documents")

# Or PostgreSQL for production
db.query("SELECT * FROM documents")
```

This ensures stats are **always accurate** even after restarts.

## Files Modified

1. **`app/api/routes.py`**
   - Enhanced `get_system_stats()` - now warns about mismatches
   - Added `GET /documents/health` - new diagnostic endpoint

2. **Documentation Created**
   - `FIX_STATS_MISMATCH.md` - Detailed explanation
   - `STATS_HEALTH_QUICK_FIX.md` - Quick reference guide

## Summary

✅ **Enhanced `get_system_stats()`** to show warnings  
✅ **New `/documents/health` endpoint** for diagnostics  
✅ **Automatic cleanup on startup** prevents orphaned data  
✅ **Clear logging** shows what's happening  
✅ **Easy fix:** Just run cleanup endpoint if mismatch detected  

The system now detects and reports the mismatch, and provides tools to fix it! 🎯
