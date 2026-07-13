# Quick Reference: Document Store Mismatch

## The Issue
```
Stats: 0 documents
Search: Finds 2 documents
Mismatch!
```

## Why
- In-memory `DOCUMENTS_STORE = {}` gets cleared on app restart
- ChromaDB persists documents to disk
- After restart, they don't match

## Quick Diagnosis

### Check if Consistent
```bash
curl http://localhost:8000/documents/health
```

Look for:
- `"is_consistent": true` ✓ or `false` ✗

### If Inconsistent, Cleanup
```bash
curl -X POST http://localhost:8000/documents/cleanup
```

Then verify:
```bash
curl http://localhost:8000/documents/health
```

## Better Endpoints Now Available

| Endpoint | Returns | Use Case |
|----------|---------|----------|
| `GET /documents/stats` | Count & size | Dashboard display |
| `GET /documents/health` | Full diagnostics | Debugging mismatches |
| `POST /documents/cleanup` | Cleanup status | Remove orphaned chunks |

## What Each Endpoint Shows

### `/documents/stats` (existing)
- `total_documents`: Count from tracked store
- `total_chunks`: Count from tracked store
- ⚠️ Now logs warning if doesn't match vector DB

### `/documents/health` (new)
Shows both sources:
```json
{
  "tracked_documents": 0,
  "vector_db_documents": 2,
  "orphaned_documents": ["doc1", "doc2"],
  "is_consistent": false,
  "needs_cleanup": true
}
```

## Quick Fix Steps

1. **Check health:**
   ```bash
   curl http://localhost:8000/documents/health
   ```

2. **If inconsistent, cleanup:**
   ```bash
   curl -X POST http://localhost:8000/documents/cleanup
   ```

3. **Verify fixed:**
   ```bash
   curl http://localhost:8000/documents/health
   # Should show "is_consistent": true
   ```

4. **Restart app to verify persistence:**
   ```bash
   # Restart backend
   curl http://localhost:8000/documents/health
   # Should still be consistent
   ```

## Log Messages

### Healthy
```
[INFO] System stats: 2 docs, 45 chunks (synced)
[HEALTHY] Document store health: ...
```

### Unhealthy
```
[WARN] Document store mismatch detected:
  Tracked: 0 docs, 0 chunks
  Vector DB: 2 docs, 45 chunks
[INCONSISTENT] Document store health: ...
```

## Files Modified

- `routes.py`: Enhanced `get_system_stats()` + new `health` endpoint

## Next Steps

To truly fix this permanently, migrate from in-memory dict to database:
- SQLite (quick, file-based)
- PostgreSQL (production-ready)

See `FIX_STATS_MISMATCH.md` for details.
