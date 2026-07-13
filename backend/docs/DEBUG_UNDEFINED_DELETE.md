# Fix: DELETE /documents/undefined 404 Errors

## Problem
Frontend is sending `DELETE /documents/undefined` requests, resulting in 404 errors.

```
DELETE /documents/undefined HTTP/1.1" 404 Not Found
```

This indicates the `document_id` is `undefined` instead of a valid ID.

## Root Causes

1. **Frontend Bug**: JavaScript not properly extracting document ID from UI element
2. **Missing Validation**: Backend not validating document ID format
3. **Silent Failures**: Frontend catching errors but not logging them

## Solution Implemented

### 1. Enhanced Delete Endpoint Validation (`routes.py`)

Added comprehensive validation:

```python
# Validate document_id
if not document_id or document_id == "undefined" or document_id.strip() == "":
    logger.warning(f"[WARN] Invalid document_id provided: '{document_id}'")
    raise HTTPException(
        status_code=400, 
        detail=f"Invalid document ID: '{document_id}'. Document ID cannot be empty or undefined."
    )
```

Now returns **400 Bad Request** with clear error message instead of 404.

### 2. Enhanced Logging

Added debug logging to list endpoint to show all document IDs:

```python
doc_ids = list(DOCUMENTS_STORE.keys())
logger.info(f"[INFO] Listed {len(documents)} documents: {doc_ids}")
```

This helps identify available document IDs for debugging.

### 3. File Hash Cleanup

Delete endpoint now also removes the file hash mapping:

```python
file_hash = doc_info.get("file_hash")
if file_hash and file_hash in FILE_HASH_MAP:
    del FILE_HASH_MAP[file_hash]
```

## How to Debug

### Check Server Logs

```
[INFO] Listed 2 documents: ['Report2024', 'AnnualReport']
[WARN] Invalid document_id provided: 'undefined'
```

This shows what document IDs are available.

### Test Delete Endpoint

```bash
# Wrong - will get 400 error
curl -X DELETE http://localhost:8000/documents/undefined

# Correct - use actual document ID from list
curl -X DELETE http://localhost:8000/documents/Report2024
```

### Check Frontend

Look for:
1. How the delete button captures document ID
2. Make sure it's getting `data-id` or similar attribute correctly
3. Check browser console for JavaScript errors

Example fix for frontend:

```javascript
// WRONG
const docId = document.getElementById('doc-id').value; // Could be undefined

// RIGHT
const docId = event.target.closest('[data-id]')?.dataset.id;
if (!docId) {
    console.error('Document ID not found');
    return;
}
```

### Verify Document IDs

```bash
# Get list of documents
curl http://localhost:8000/documents

# Response will show:
{
  "documents": [
    {
      "document_id": "Report2024",
      "filename": "Report2024.pdf",
      ...
    }
  ]
}
```

## Better Error Responses

### Before Fix
```
DELETE /documents/undefined → 404 Not Found
```

### After Fix
```
DELETE /documents/undefined → 400 Bad Request
{
  "detail": "Invalid document ID: 'undefined'. Document ID cannot be empty or undefined."
}
```

## Files Modified

1. **`routes.py`**
   - Enhanced delete endpoint validation
   - Added document ID list to logging
   - Added file hash cleanup

## Testing Checklist

- [ ] List documents shows all document IDs
- [ ] Delete with valid ID succeeds (204 No Content)
- [ ] Delete with `undefined` returns 400 Bad Request with clear message
- [ ] Delete with non-existent ID returns 404 Not Found
- [ ] Delete with empty string returns 400 Bad Request
- [ ] Frontend correctly captures and sends document IDs
- [ ] File and file_hash are properly cleaned up

## Production Recommendations

1. **Frontend**: Validate document ID exists before sending request
2. **Frontend**: Show error message from server if delete fails
3. **Frontend**: Log failed requests for debugging
4. **Backend**: Monitor 400 errors for patterns (indicates frontend bugs)
5. **Database**: Consider persisting document list to database instead of in-memory store
