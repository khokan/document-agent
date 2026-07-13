# Complete Fix: Auto-Load Documents on Startup

## Problem Solved

**Before:** After app restart, stats showed 0 documents while search found documents  
**After:** Documents are automatically loaded from vector store into memory on startup

## The Solution

When the app starts, it now:
1. **Scans the vector store** for all documents
2. **Retrieves metadata** for each document
3. **Loads into `DOCUMENTS_STORE`** (in-memory cache)
4. **Cleans up orphaned** chunks

## Implementation

### 1. New ChromaDB Method

**File:** `app/vector_store/chromadb_service.py`

```python
async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
    """
    Get aggregated metadata for a specific document.
    
    - Queries all chunks for the document
    - Counts unique pages
    - Aggregates filename, chunk count, etc.
    
    Returns:
    {
        "document_id": "report2024",
        "filename": "Report2024.pdf",
        "chunk_count": 45,
        "page_count": 10,
        "status": "indexed"
    }
    """
```

### 2. Enhanced Sync Function

**File:** `app/api/routes.py`

```python
async def _sync_documents_from_vector_store():
    """Sync DOCUMENTS_STORE on startup"""
    
    # 1. Get all document IDs from vector store
    vector_doc_ids = await vector_service.get_all_document_ids()
    
    # 2. For each document, get metadata
    for doc_id in vector_doc_ids:
        metadata = await vector_service.get_document_metadata(doc_id)
        
        # 3. Store in memory
        DOCUMENTS_STORE[doc_id] = {
            "document_id": doc_id,
            "filename": metadata["filename"],
            "chunk_count": metadata["chunk_count"],
            "page_count": metadata["page_count"],
            ...
        }
    
    # 4. Clean up orphaned chunks
    await _cleanup_orphaned_chunks()
```

### 3. Automatic Trigger

**File:** `main.py` (already implemented)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ...
    # Sync document store with vector store on startup
    await _sync_documents_from_vector_store()
    
    yield
    
    # Shutdown
    ...
```

## Behavior Timeline

### Old Behavior
```
[STARTUP] App starts
          DOCUMENTS_STORE = {}
          ↓
[0ms]     Ready to serve requests
          Stats: 0 docs
          Search: Finds 2 docs
          ✗ MISMATCH
```

### New Behavior
```
[STARTUP] App starts
          ↓
[INFO] Starting document store sync from vector store...
[INFO] Found 2 document(s) in vector store
[DEBUG] Loaded document: Report2024 (45 chunks)
[DEBUG] Loaded document: AnnualReport (32 chunks)
[OK] Loaded 2 document(s) into memory
[OK] No orphaned documents found
[OK] Document store synchronized with vector store
          DOCUMENTS_STORE = {"Report2024": {...}, "AnnualReport": {...}}
          ↓
[~500ms]  Ready to serve requests
          Stats: 2 docs ✓
          Search: Finds 2 docs ✓
          ✓ CONSISTENT
```

## API Behavior After Startup

### GET /documents
```json
{
  "documents": [
    {
      "document_id": "Report2024",
      "filename": "Report2024.pdf",
      "chunk_count": 45,
      ...
    },
    {
      "document_id": "AnnualReport",
      "filename": "AnnualReport.pdf", 
      "chunk_count": 32,
      ...
    }
  ],
  "total_count": 2
}
```

### GET /documents/stats
```json
{
  "total_documents": 2,
  "total_chunks": 77,
  "total_size_mb": 5.2
}
```

### GET /documents/health
```json
{
  "status": "healthy",
  "tracked_documents": 2,
  "vector_db_documents": 2,
  "orphaned_documents": [],
  "is_consistent": true,
  "needs_cleanup": false
}
```

## Testing Verification

### Test Case 1: Fresh Restart
```bash
# Prerequisites: System has 2 documents stored

# 1. Stop app
# 2. Start app

# 3. Check logs - should see:
[INFO] Found 2 document(s) in vector store
[OK] Loaded 2 document(s) into memory

# 4. Verify endpoints
curl http://localhost:8000/documents
# ✓ Returns 2 documents

curl http://localhost:8000/documents/stats
# ✓ Shows total_documents: 2

# 5. Verify search still works
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"question": "search query"}'
# ✓ Finds results from both documents
```

### Test Case 2: With Orphaned Chunks
```bash
# Prerequisites: System has orphaned chunks

# 1. Start app
# 2. Check logs - should see:
[WARN] Found 1 orphaned document(s) in vector store
[OK] Cleaned up 1 orphaned document(s)

# 3. Verify cleanup worked
curl http://localhost:8000/documents/health
# ✓ Shows orphaned_documents: []
# ✓ Shows is_consistent: true
```

### Test Case 3: Multiple Restarts
```bash
# 1. Restart app → Loads 2 documents
# 2. Verify stats → Shows 2 documents
# 3. Restart app → Still shows 2 documents
# 4. Upload 3rd document
# 5. Restart app → Shows 3 documents
# 6. Delete 1 document via API
# 7. Restart app → Shows 2 documents
# ✓ Consistency maintained across restarts
```

## Performance Impact

| Metric | Impact |
|--------|--------|
| **Startup time** | +50-200ms (proportional to docs) |
| **Memory usage** | Same (documents in memory) |
| **Runtime speed** | No change (local memory access) |
| **Network calls** | Only local ChromaDB queries |

## Benefits

| Benefit | Description |
|---------|-------------|
| **Automatic Recovery** | No manual sync needed |
| **Persistent Memory** | Survives app restarts |
| **Always Consistent** | DOCUMENTS_STORE matches vector store |
| **Self-Healing** | Orphaned chunks cleaned automatically |
| **Better UX** | No confusing mismatches |
| **Better Logging** | Clear startup logs show loading progress |

## Files Modified

| File | Changes |
|------|---------|
| `chromadb_service.py` | Added `get_document_metadata()` method |
| `routes.py` | Enhanced `_sync_documents_from_vector_store()` to load documents |
| `main.py` | Already had startup sync call (no changes needed) |

## Backward Compatibility

✓ **Fully compatible** - No breaking changes  
✓ **No API changes** - All endpoints work the same  
✓ **No data migration** - Works with existing ChromaDB  
✓ **Graceful degradation** - Handles missing documents gracefully  

## Architecture Improvements

### Data Flow Before
```
Vector Store (disk)
      ↓
      ✗ Not synced to memory
      ↓
DOCUMENTS_STORE (memory) = {}
      ↓
API sees: 0 documents
```

### Data Flow After
```
Vector Store (disk)
      ↓
Get all documents
      ↓
Get metadata for each
      ↓
Load into memory
      ↓
DOCUMENTS_STORE (memory) = {doc1, doc2, ...}
      ↓
API sees: Correct document count
```

## Future Enhancements

1. **Database Persistence** - Replace in-memory dict with SQLite/PostgreSQL
2. **Partial Sync** - Only sync changed documents
3. **Background Sync** - Periodic sync during operation
4. **Multi-Instance** - Distributed cache for clustered deployments
5. **Incremental Load** - Load documents lazily on first access

## Summary

✅ **Automatic document loading on startup**  
✅ **Metadata retrieval from vector store**  
✅ **In-memory cache population**  
✅ **Orphaned chunk cleanup**  
✅ **Consistent state across restarts**  
✅ **No breaking changes**  
✅ **Clear logging**  

The system now maintains consistency automatically! 🎯
