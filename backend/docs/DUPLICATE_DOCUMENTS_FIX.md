# Fix: Recent Documents Showing 1 Document but Search Showing Data from 2 Documents

## Problem
- Document list endpoint shows only 1 document
- Search results contain data from 2 documents
- This occurs after app restarts or crashes
- Root cause: In-memory `DOCUMENTS_STORE` gets reset, but chunks remain in persistent ChromaDB vector store

## Solution: 3-Component Fix

### 1. **Vector Store Enhancement** (`chromadb_service.py`)
Added new method to retrieve all document IDs currently stored in the vector database:

```python
async def get_all_document_ids(self) -> List[str]:
    """Get all unique document IDs currently stored in the vector database."""
```

This allows us to compare what's in memory vs. what's persisted.

### 2. **Startup Synchronization** (`main.py`)
Added automatic sync on app startup:

```python
# In lifespan startup
from app.api.routes import _sync_documents_from_vector_store
await _sync_documents_from_vector_store()
```

When the app starts, it:
- Gets all document IDs from the vector store
- Compares with tracked documents in `DOCUMENTS_STORE`
- Deletes orphaned chunks that don't belong to any tracked document

### 3. **Helper Functions & Cleanup Endpoint** (`routes.py`)

#### Helper Functions:
```python
async def _cleanup_orphaned_chunks():
    """Remove orphaned chunks from vector store"""
    
async def _sync_documents_from_vector_store():
    """Sync DOCUMENTS_STORE with actual vector store data"""
```

#### New Endpoint:
```
POST /documents/cleanup
```

Manually trigger cleanup of orphaned documents at any time.

## How It Works

### Scenario 1: App Restart After Incomplete Deletion
1. Document "Report.pdf" is deleted via API
2. Chunks removed from ChromaDB ✓
3. Document removed from `DOCUMENTS_STORE` ✓
4. App crashes before shutdown
5. App restarts → `_sync_documents_from_vector_store()` runs
6. Compares vector store with DOCUMENTS_STORE
7. Finds no orphaned chunks ✓
8. Search works correctly with no duplicates

### Scenario 2: Manual Vector Store Corruption
1. Vector store has chunks from "Report.pdf" with document_id "report_abc123"
2. `DOCUMENTS_STORE` doesn't track this document
3. User calls `POST /documents/cleanup`
4. System detects orphaned document_id "report_abc123"
5. All chunks for "report_abc123" are deleted
6. Search results now only show tracked documents

## Files Modified

1. **`chromadb_service.py`**
   - Added `get_all_document_ids()` method

2. **`main.py`**
   - Added sync call in lifespan startup

3. **`routes.py`**
   - Added `_cleanup_orphaned_chunks()` function
   - Added `_sync_documents_from_vector_store()` function
   - Added `POST /documents/cleanup` endpoint

## Testing

```bash
# 1. Upload a document
curl -X POST http://localhost:8000/documents/upload -F "file=@document.pdf"

# 2. Verify it appears in list
curl http://localhost:8000/documents

# 3. Search for content
curl -X POST http://localhost:8000/search -J "{\"question\": \"search query\"}"

# 4. Manually cleanup (if needed)
curl -X POST http://localhost:8000/documents/cleanup

# 5. Verify consistency
curl http://localhost:8000/documents/stats
```

## Benefits

✅ **Automatic Recovery** - Sync on startup prevents orphaned chunks  
✅ **Consistency** - Document list always matches search results  
✅ **Manual Control** - Cleanup endpoint for emergency situations  
✅ **Logging** - Clear logs show what was cleaned up  
✅ **No Data Loss** - Only removes truly orphaned chunks  

## Related Fixes

This fix works in conjunction with the previous duplicate document fixes:
- Layer 1: Upload-level deduplication (file hash tracking)
- Layer 2: Retriever-level deduplication (content deduplication)
- Layer 3: Persistence sync (this fix - orphaned chunk cleanup)
