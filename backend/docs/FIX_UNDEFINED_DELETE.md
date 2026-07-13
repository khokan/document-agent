# DELETE /documents/undefined 404 Error - Complete Fix & Debugging Guide

## Problem Summary

Frontend is sending `DELETE /documents/undefined` requests:
```
DELETE /documents/undefined HTTP/1.1" 404 Not Found
DELETE /documents/undefined HTTP/1.1" 404 Not Found
```

This indicates the document ID is `undefined` instead of a valid ID string.

## Root Cause Analysis

### Why This Happens

1. **Frontend JavaScript Bug**: Document ID not properly extracted from DOM
   - Missing element attribute
   - Wrong selector used
   - Element not found
   - Variable assignment failed

2. **Missing Backend Validation**: Server was returning 404 instead of 400
   - Didn't distinguish between "not found" and "invalid"
   - No helpful error message for debugging

3. **Silent Failures**: No logging to indicate the issue

## Solution Implemented

### 1. Enhanced Delete Endpoint (routes.py)

**Before:**
```python
if document_id not in DOCUMENTS_STORE:
    raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")
```

**After:**
```python
# Validate document_id
if not document_id or document_id == "undefined" or document_id.strip() == "":
    logger.warning(f"[WARN] Invalid document_id provided: '{document_id}'")
    raise HTTPException(
        status_code=400, 
        detail=f"Invalid document ID: '{document_id}'. Document ID cannot be empty or undefined."
    )

if document_id not in DOCUMENTS_STORE:
    logger.warning(f"[WARN] Attempt to delete non-existent document: {document_id}")
    raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")
```

**Benefits:**
- Returns **400 Bad Request** for invalid IDs
- Returns **404 Not Found** for valid but missing IDs
- Clear error messages for debugging
- Proper warning logs

### 2. Enhanced Logging (routes.py)

**Before:**
```python
logger.info(f"[INFO] Listed {len(documents)} documents")
```

**After:**
```python
doc_ids = list(DOCUMENTS_STORE.keys())
logger.info(f"[INFO] Listed {len(documents)} documents: {doc_ids}")
```

**Benefits:**
- Shows available document IDs in logs
- Easy to verify frontend has correct IDs

### 3. File Hash Cleanup

Added cleanup of file hash mappings during deletion:
```python
file_hash = doc_info.get("file_hash")
if file_hash and file_hash in FILE_HASH_MAP:
    del FILE_HASH_MAP[file_hash]
```

### 4. Debug Endpoints

No changes to endpoints, but added better error responses.

## Error Response Examples

### Invalid Document ID (400 Bad Request)

**Request:**
```bash
curl -X DELETE http://localhost:8000/documents/undefined
```

**Response:**
```json
{
  "detail": "Invalid document ID: 'undefined'. Document ID cannot be empty or undefined."
}
```

### Non-Existent Document (404 Not Found)

**Request:**
```bash
curl -X DELETE http://localhost:8000/documents/nonexistent-id
```

**Response:**
```json
{
  "detail": "Document not found: nonexistent-id"
}
```

### Successful Delete (204 No Content)

**Request:**
```bash
curl -X DELETE http://localhost:8000/documents/Report2024
```

**Response:** (empty, 204 status)

## Debugging Steps

### Step 1: Check Available Document IDs

```bash
curl http://localhost:8000/documents
```

Look for the document IDs in the response:
```json
{
  "documents": [
    {
      "document_id": "Report2024",
      "filename": "Report2024.pdf",
      ...
    },
    {
      "document_id": "AnnualReport",
      "filename": "AnnualReport.pdf",
      ...
    }
  ]
}
```

### Step 2: Check Server Logs

Look for this log entry when listing documents:
```
[INFO] Listed 2 documents: ['Report2024', 'AnnualReport']
```

This shows what IDs are available.

### Step 3: Test Delete with Valid ID

```bash
curl -X DELETE http://localhost:8000/documents/Report2024
```

Should return 204 (empty response).

### Step 4: Run Debug Script

```bash
python debug_documents.py
```

Output will show:
- Documents in store
- Documents in vector store
- Orphaned documents
- Recent errors

### Step 5: Run API Test Script

```bash
python test_api.py
```

Tests all document operations and validates responses.

## Frontend Debugging

### Common Issues

**1. Missing data attribute:**
```html
<!-- WRONG -->
<button onclick="deleteDoc()">Delete</button>
<script>
  function deleteDoc() {
    const id = document.getElementById('nonexistent'); // Returns null
    fetch(`/documents/${id}`); // Sends undefined
  }
</script>

<!-- RIGHT -->
<button onclick="deleteDoc(this)" data-id="Report2024">Delete</button>
<script>
  function deleteDoc(button) {
    const id = button.dataset.id;
    if (!id) {
      console.error('Document ID not found');
      return;
    }
    fetch(`/documents/${id}`, { method: 'DELETE' });
  }
</script>
```

**2. Wrong selector:**
```javascript
// WRONG
const id = document.querySelector('[data-doc-id]').value; // Might be wrong element

// RIGHT
const id = event.target.closest('[data-id]')?.dataset.id;
if (!id) throw new Error('Document ID not found');
```

**3. Not validating before request:**
```javascript
// WRONG
const id = getData();
fetch(`/documents/${id}`, { method: 'DELETE' }); // id could be undefined

// RIGHT
const id = getData();
if (!id || id === 'undefined') {
  console.error('Invalid document ID:', id);
  alert('Cannot delete: Document ID is invalid');
  return;
}
fetch(`/documents/${id}`, { method: 'DELETE' });
```

### Browser Developer Tools

1. Open **Network** tab
2. Look for DELETE requests
3. Check the URL - does it say `/documents/undefined`?
4. If yes, check the frontend code that makes the request
5. Add `console.log()` to debug the ID value

## Provided Tools

### 1. `debug_documents.py`

Comprehensive debug report showing:
- Documents in store
- Documents in vector store  
- Orphaned documents
- Recent logs
- Recommendations

**Run:**
```bash
python debug_documents.py
```

### 2. `test_api.py`

API endpoint tester that:
- Lists documents
- Gets statistics
- Tests invalid deletes
- Tests valid deletes
- Verifies cleanup

**Run:**
```bash
python test_api.py
```

## Testing Checklist

- [ ] Server logs show correct document IDs when listing
- [ ] Delete with valid ID returns 204
- [ ] Delete with "undefined" returns 400 with message
- [ ] Delete with empty string returns 400 with message
- [ ] Delete with non-existent ID returns 404
- [ ] Frontend correctly captures document ID
- [ ] Frontend sends correct ID in DELETE request
- [ ] Browser console shows no JavaScript errors
- [ ] File hashes are cleaned up on deletion
- [ ] Orphaned documents can be cleaned up

## Production Checklist

- [ ] Enable detailed request logging in production
- [ ] Monitor 400 errors - indicates frontend bugs
- [ ] Set up alerts for multiple undefined deletions
- [ ] Document the API error responses
- [ ] Add request validation tests to CI/CD
- [ ] Consider using UUID validation instead of string comparison
- [ ] Migrate from in-memory store to database

## Files Modified

1. **`app/api/routes.py`**
   - Enhanced delete validation
   - Better error messages
   - File hash cleanup
   - Enhanced logging

2. **Created:**
   - `debug_documents.py` - Debug utility
   - `test_api.py` - API test utility

## Next Steps

1. Run `debug_documents.py` to identify current state
2. Run `test_api.py` to test all endpoints
3. Check frontend code for document ID extraction
4. Fix frontend bug if found
5. Verify no more `undefined` errors in logs
