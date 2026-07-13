#!/usr/bin/env python3
"""
Test script to verify document operations and API endpoints
"""

import httpx
import asyncio
import json
from pathlib import Path


class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def close(self):
        await self.client.aclose()
    
    async def list_documents(self):
        """List all documents"""
        print("\n" + "=" * 60)
        print("GET /documents")
        print("=" * 60)
        
        try:
            response = await self.client.get(f"{self.base_url}/documents")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Total documents: {data['total_count']}")
                print(f"Total chunks: {data['total_chunks']}")
                
                if data['documents']:
                    print("\nDocuments:")
                    for doc in data['documents']:
                        print(f"  • ID: {doc['document_id']}")
                        print(f"    Filename: {doc['filename']}")
                        print(f"    Chunks: {doc['chunk_count']}")
                else:
                    print("No documents found!")
                
                return data['documents']
            else:
                print(f"Error: {response.text}")
                return []
        except Exception as e:
            print(f"ERROR: {e}")
            return []
    
    async def get_stats(self):
        """Get system statistics"""
        print("\n" + "=" * 60)
        print("GET /documents/stats")
        print("=" * 60)
        
        try:
            response = await self.client.get(f"{self.base_url}/documents/stats")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Total documents: {data['total_documents']}")
                print(f"Total chunks: {data['total_chunks']}")
                print(f"Total size: {data['total_size_mb']} MB")
                print(f"Collection: {data['collection_name']}")
                print(f"Embedding dimension: {data['embedding_dimension']}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    async def cleanup_orphaned(self):
        """Cleanup orphaned documents"""
        print("\n" + "=" * 60)
        print("POST /documents/cleanup")
        print("=" * 60)
        
        try:
            response = await self.client.post(f"{self.base_url}/documents/cleanup")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Status: {data['status']}")
                print(f"Message: {data['message']}")
                if data['orphaned_documents']:
                    print(f"Orphaned documents removed: {data['orphaned_documents']}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    async def delete_document(self, document_id: str):
        """Delete a document"""
        print("\n" + "=" * 60)
        print(f"DELETE /documents/{document_id}")
        print("=" * 60)
        
        try:
            response = await self.client.delete(f"{self.base_url}/documents/{document_id}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 204:
                print("✓ Document deleted successfully")
            elif response.status_code == 400:
                print(f"✗ Bad request: {response.json()['detail']}")
            elif response.status_code == 404:
                print(f"✗ Not found: {response.json()['detail']}")
            else:
                print(f"✗ Error: {response.text}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    async def test_invalid_delete(self):
        """Test delete with invalid IDs"""
        print("\n" + "=" * 60)
        print("TESTING INVALID DELETE REQUESTS")
        print("=" * 60)
        
        invalid_ids = ["undefined", "", "nonexistent", "   "]
        
        for invalid_id in invalid_ids:
            print(f"\nTesting: '{invalid_id}'")
            await self.delete_document(invalid_id)


async def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 18 + "DOCUMENT API TESTER" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    
    tester = APITester()
    
    try:
        # Check connectivity
        print("\nChecking server connectivity...")
        try:
            response = await tester.client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✓ Server is running")
            else:
                print("✗ Server responded but health check failed")
                return
        except Exception as e:
            print(f"✗ Cannot connect to server: {e}")
            print("  Make sure the server is running on http://localhost:8000")
            return
        
        # Run tests
        documents = await tester.list_documents()
        await tester.get_stats()
        await tester.cleanup_orphaned()
        
        # Test invalid deletes
        await tester.test_invalid_delete()
        
        # Test valid delete if documents exist
        if documents:
            print("\n" + "=" * 60)
            print("TESTING VALID DELETE")
            print("=" * 60)
            first_doc_id = documents[0]['document_id']
            print(f"\nAttempting to delete: {first_doc_id}")
            await tester.delete_document(first_doc_id)
            
            # Verify deletion
            print("\nVerifying deletion...")
            docs_after = await tester.list_documents()
            remaining_ids = [d['document_id'] for d in docs_after]
            if first_doc_id not in remaining_ids:
                print(f"✓ Document '{first_doc_id}' was successfully deleted")
            else:
                print(f"✗ Document '{first_doc_id}' still exists!")
    
    finally:
        await tester.close()


if __name__ == "__main__":
    asyncio.run(main())
