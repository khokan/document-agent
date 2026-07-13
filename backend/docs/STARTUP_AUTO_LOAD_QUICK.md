# Auto-Load Documents on Startup - Summary

## The Change

When the app starts, it now automatically loads all documents from the persistent vector store into the in-memory `DOCUMENTS_STORE`.

## Before vs After

### Before
```
App Restart
  ↓
DOCUMENTS_STORE = {} (empty)
  ↓
Stats: 0 documents
Search: Finds 2 documents
  ↓
MISMATCH
```

### After
```
App Startup
  ↓
Scan vector store: Found 2 documents
  ↓
Load metadata into memory
  ↓
DOCUMENTS_STORE = {doc1, doc2}
  ↓
Stats: 2 documents
Search: Finds 2 documents
  ↓
CONSISTENT
```

## What Changed

### 1. New Method in ChromaDB Service
```python
async def get_document_metadata(document_id: str) -> Dict:
    # Returns aggregated metadata:
    # - filename
    # - chunk_count
    # - page_count
    # - status
```

### 2. Enhanced Sync on Startup
```python
async def _sync_documents_from_vector_store():
    # 1. Get all documents from vector store
    # 2. Load metadata for each into DOCUMENTS_STORE
    # 3. Clean up any orphaned chunks
```

## Startup Logs

### Normal
```
[INFO] Found 2 document(s) in vector store
[DEBUG] Loaded document: Report2024 (45 chunks)
[DEBUG] Loaded document: AnnualReport (32 chunks)
[OK] Loaded 2 document(s) into memory
[OK] No orphaned documents found
```

### With Cleanup
```
[INFO] Found 3 document(s) in vector store
[OK] Loaded 2 document(s) into memory
[WARN] Found 1 orphaned document(s): {'OldReport'}
[OK] Cleaned up 1 orphaned document(s)
```

## Verification

After app starts:
```bash
# Should show loaded documents
curl http://localhost:8000/documents
# ✓ Returns 2 documents

curl http://localhost:8000/documents/stats
# ✓ Shows 2 documents, 45 chunks

curl http://localhost:8000/documents/health
# ✓ Shows "is_consistent": true
```

## Benefits

✅ **No Manual Sync** - Automatic on startup  
✅ **Persistent Memory** - Survives restarts  
✅ **Always Consistent** - Matches vector store  
✅ **Self-Healing** - Cleans orphaned data  
✅ **Clear Logging** - Shows what's loading  

## Files Modified

1. `chromadb_service.py` - Added `get_document_metadata()` method
2. `routes.py` - Enhanced `_sync_documents_from_vector_store()` function

## No Breaking Changes

- Existing API endpoints work the same
- Just more efficient and consistent on startup
- No changes needed to frontend or other services
