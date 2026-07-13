#!/usr/bin/env python3
"""
Debug script to identify why DELETE requests have 'undefined' document_id
"""

import asyncio
import json
from pathlib import Path


async def check_documents_store():
    """Check what documents are actually stored in DOCUMENTS_STORE"""
    print("=" * 60)
    print("DOCUMENTS STORE CHECK")
    print("=" * 60)
    
    try:
        from app.api.routes import DOCUMENTS_STORE, FILE_HASH_MAP
        
        print(f"\nTotal documents in store: {len(DOCUMENTS_STORE)}")
        print(f"Total file hashes tracked: {len(FILE_HASH_MAP)}")
        
        if DOCUMENTS_STORE:
            print("\nDocuments:")
            for doc_id, doc_info in DOCUMENTS_STORE.items():
                print(f"  • {doc_id}")
                print(f"    - Filename: {doc_info.get('filename')}")
                print(f"    - Status: {doc_info.get('status')}")
                print(f"    - Chunks: {doc_info.get('chunk_count')}")
                print(f"    - File Hash: {doc_info.get('file_hash', 'N/A')}")
        else:
            print("\nNo documents in store!")
        
        print("\nFile Hash Map:")
        if FILE_HASH_MAP:
            for file_hash, doc_id in FILE_HASH_MAP.items():
                print(f"  • {file_hash[:16]}... → {doc_id}")
        else:
            print("  (empty)")
            
    except Exception as e:
        print(f"ERROR: {e}")


async def check_vector_store():
    """Check what documents are in the vector store"""
    print("\n" + "=" * 60)
    print("VECTOR STORE CHECK")
    print("=" * 60)
    
    try:
        from app.api.deps import vector_service
        
        # Get all document IDs from vector store
        doc_ids = await vector_service.get_all_document_ids()
        print(f"\nTotal unique document IDs in vector store: {len(doc_ids)}")
        
        if doc_ids:
            print("Document IDs:")
            for doc_id in sorted(doc_ids):
                print(f"  • {doc_id}")
        else:
            print("No documents in vector store!")
        
        # Get stats
        stats = await vector_service.get_stats()
        print(f"\nVector Store Stats:")
        print(f"  - Total chunks: {stats.get('count')}")
        print(f"  - Collection: {stats.get('collection_name')}")
        
    except Exception as e:
        print(f"ERROR: {e}")


async def check_orphaned_documents():
    """Check for orphaned documents in vector store"""
    print("\n" + "=" * 60)
    print("ORPHANED DOCUMENTS CHECK")
    print("=" * 60)
    
    try:
        from app.api.routes import DOCUMENTS_STORE
        from app.api.deps import vector_service
        
        vector_doc_ids = set(await vector_service.get_all_document_ids())
        tracked_doc_ids = set(DOCUMENTS_STORE.keys())
        
        orphaned = vector_doc_ids - tracked_doc_ids
        untracked = tracked_doc_ids - vector_doc_ids
        
        print(f"\nTracked documents: {tracked_doc_ids}")
        print(f"Vector store documents: {vector_doc_ids}")
        
        if orphaned:
            print(f"\n⚠️  ORPHANED DOCUMENTS (in vector store but not tracked):")
            for doc_id in sorted(orphaned):
                print(f"  • {doc_id}")
            print("\n  Run: POST /documents/cleanup")
        else:
            print("\n✓ No orphaned documents")
        
        if untracked:
            print(f"\n⚠️  UNTRACKED DOCUMENTS (tracked but not in vector store):")
            for doc_id in sorted(untracked):
                print(f"  • {doc_id}")
            print("\n  Documents may not have been indexed")
        else:
            print("✓ All tracked documents are in vector store")
            
    except Exception as e:
        print(f"ERROR: {e}")


async def check_recent_logs():
    """Check recent error logs"""
    print("\n" + "=" * 60)
    print("RECENT ERROR LOGS")
    print("=" * 60)
    
    try:
        log_file = Path("logs/app.log")
        if log_file.exists():
            lines = log_file.read_text().split('\n')
            
            # Get last 20 lines
            recent_lines = [l for l in lines if l.strip()][-20:]
            
            print("\nLast 20 log entries:")
            for line in recent_lines:
                if 'undefined' in line.lower() or 'delete' in line.lower() or 'error' in line.lower():
                    print(f"  ! {line[:100]}")
                else:
                    print(f"    {line[:100]}")
        else:
            print("Log file not found!")
            
    except Exception as e:
        print(f"ERROR: {e}")


async def main():
    """Run all checks"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 14 + "DOCUMENT STORE DEBUG REPORT" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    
    await check_documents_store()
    await check_vector_store()
    await check_orphaned_documents()
    await check_recent_logs()
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    print("""
1. Check that document IDs are being properly captured in frontend
2. Verify list endpoint returns correct document IDs
3. Test delete with a valid document_id from the list
4. Check browser console for JavaScript errors
5. Verify delete button has data-id or similar attribute
    """)


if __name__ == "__main__":
    asyncio.run(main())
