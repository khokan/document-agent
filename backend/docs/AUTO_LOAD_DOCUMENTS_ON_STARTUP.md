# Fix: Auto-Load Documents from Vector Store on Startup

## Problem

When the app restarts:
- `DOCUMENTS_STORE` (in-memory) is empty
- ChromaDB (persistent) still has all the documents
- Result: Stats shows 0 docs but search finds documents

## Solution

On app startup, automatically:
1. **Scan vector store** for all documents
2. **Load metadata** into `DOCUMENTS_STORE`
3. **Restore in-memory cache** from persistent storage
4. **Clean up orphaned** chunks

## How It Works

### Before (Old Behavior)
```
App Restart
    ↓
DOCUMENTS_STORE = {} (empty)
    ↓
Vector Store has 2 docs (from previous session)
    ↓
Stats: 0 docs
Search: Finds 2 docs
    ↓
MISMATCH ✗
```

### After (New Behavior)
```
App Startup
    ↓
_sync_documents_from_vector_store() runs
    ↓
Query vector store: Found 2 documents
    ↓
Get metadata for each document
    ↓
Load into DOCUMENTS_STORE
    ↓
DOCUMENTS_STORE = {"doc1": {...}, "doc2": {...}}
    ↓
Stats: 2 docs
Search: Finds 2 docs
    ↓
CONSISTENT ✓
```

## Implementation Details

### 1. New Vector Store Method

**Added to `chromadb_service.py`:**

```python
async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
    """
    Get aggregated metadata for a specific document.
    
    Retrieves all chunks for the document and returns:
    - filename
    - original_filename
    - chunk_count
    - page_count
    - status
    """
```

This method:
- Queries all chunks for a document
- Counts unique pages
- Aggregates metadata from chunks
- Returns document-level information

### 2. Enhanced Sync Function

**Updated in `routes.py`:**

```python
async def _sync_documents_from_vector_store():
    # 1. Get all document IDs from vector store
    vector_doc_ids = await vector_service.get_all_document_ids()
    
    # 2. For each document, load metadata
    for doc_id in vector_doc_ids:
        metadata = await vector_service.get_document_metadata(doc_id)
        DOCUMENTS_STORE[doc_id] = {
            "document_id": doc_id,
            "filename": metadata.get("filename"),
            "chunk_count": metadata.get("chunk_count"),
            ...
        }
    
    # 3. Cleanup orphaned chunks
    await _cleanup_orphaned_chunks()
```

### 3. Automatic Trigger on Startup

**In `main.py` lifespan:**
```python
await _sync_documents_from_vector_store()
```

Runs during app startup before any requests are handled.

## Log Output on Startup

### Healthy System
```
[INFO] Starting document store sync from vector store...
[INFO] Found 2 document(s) in vector store
[DEBUG] Loaded document: Report2024 (45 chunks)
[DEBUG] Loaded document: AnnualReport (32 chunks)
[OK] Loaded 2 document(s) into memory
[OK] No orphaned documents found in vector store
[OK] Document store synchronized with vector store
```

### System with Orphaned Data
```
[INFO] Starting document store sync from vector store...
[INFO] Found 3 document(s) in vector store
[DEBUG] Loaded document: Report2024 (45 chunks)
[DEBUG] Loaded document: AnnualReport (32 chunks)
[OK] Loaded 2 document(s) into memory
[WARN] Found 1 orphaned document(s) in vector store: {'OldReport'}
[INFO] Deleting orphaned chunks for document: OldReport
[OK] Cleaned up 1 orphaned document(s)
[OK] Document store synchronized with vector store
```

## Behavior After Startup

After sync completes:

| Scenario | Before | After |
|----------|--------|-------|
| Stats endpoint | Returns 0 docs (wrong) | Returns 2 docs (correct) |
| Health check | Shows inconsistent | Shows healthy |
| List documents | Empty | Shows all 2 documents |
| Search | Finds orphaned docs | Only finds tracked docs |

## Testing

### Test 1: Fresh Start with Existing Data
```bash
# 1. Ensure app is stopped
# 2. Upload 2 documents (if not already there)
# 3. Stop app
# 4. Start app

# 5. Check logs - should see:
# [OK] Loaded 2 document(s) into memory

# 6. Verify
curl http://localhost:8000/documents
# Should list 2 documents (instead of 0)

curl http://localhost:8000/documents/stats
# Should show 2 documents
```

### Test 2: Orphaned Chunks Cleanup
```bash
# 1. Upload document "Report.pdf"
# 2. Delete via API
# 3. Manually add chunks back to ChromaDB (simulating DB corruption)
# 4. Restart app

# 5. Check logs - should see:
# [WARN] Found 1 orphaned document(s)
# [OK] Cleaned up 1 orphaned document(s)

# 6. Verify cleanup
curl http://localhost:8000/documents/health
# Should show is_consistent: true
```

### Test 3: Multiple Restarts
```bash
# 1. Upload 2 documents
# 2. Restart app → Should load 2 docs
# 3. Check stats → Should show 2 docs
# 4. Restart app → Should still show 2 docs
# 5. Add 3rd document
# 6. Restart app → Should now show 3 docs
```

## Benefits

✅ **No More Mismatches** - DOCUMENTS_STORE always reflects actual data  
✅ **Automatic Recovery** - No need for manual cleanup  
✅ **Transparent** - Clear logs show what's happening  
✅ **Persistent** - Survives app restarts  
✅ **Clean Start** - Orphaned chunks removed automatically  

## Files Modified

1. **`app/vector_store/chromadb_service.py`**
   - Added `get_document_metadata()` method
   - Aggregates metadata from chunks

2. **`app/api/routes.py`**
   - Enhanced `_sync_documents_from_vector_store()` function
   - Now loads documents from vector store into memory

## Architecture Before vs After

### Before
```
┌─────────────────────────────────────┐
│ App Start (main.py)                 │
│  ↓                                  │
│  _sync_documents_from_vector_store() │
│   - Only cleanup orphaned chunks    │
│   - DOCUMENTS_STORE stays empty     │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ DOCUMENTS_STORE: {}                 │
│ Vector Store: [doc1, doc2]          │
│                                     │
│ MISMATCH ✗                          │
└─────────────────────────────────────┘
```

### After
```
┌─────────────────────────────────────────────────────┐
│ App Start (main.py)                                 │
│  ↓                                                  │
│  _sync_documents_from_vector_store()                │
│   1. Get all document IDs from vector store        │
│   2. Load metadata for each document               │
│   3. Populate DOCUMENTS_STORE                       │
│   4. Cleanup orphaned chunks                        │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ DOCUMENTS_STORE: {                                  │
│   "doc1": {filename, chunks: 45, ...},             │
│   "doc2": {filename, chunks: 32, ...}              │
│ }                                                   │
│ Vector Store: [doc1, doc2]                          │
│                                                     │
│ CONSISTENT ✓                                        │
└─────────────────────────────────────────────────────┘
```

## Performance Considerations

- **Startup time**: Adds slight delay proportional to number of documents
- **Memory usage**: All documents loaded into memory (same as if uploaded during session)
- **Network**: Only local ChromaDB queries, no external calls
- **Optimization**: Uses batch operations and efficient metadata aggregation

## Future Improvements

1. **Persistent Storage**: Replace `DOCUMENTS_STORE = {}` with database
2. **Partial Sync**: Only load changed documents
3. **Background Sync**: Periodic sync during operation
4. **Distributed Cache**: For multi-instance deployments
