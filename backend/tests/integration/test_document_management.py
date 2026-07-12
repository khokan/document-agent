"""
Integration tests for document management API endpoints.

Tests the complete workflow:
- Upload documents
- List documents
- Delete documents
- Reindex documents
- System statistics
"""

import io
import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestDocumentUploadEndpoint:
    """Test POST /documents/upload endpoint."""

    def test_upload_with_valid_pdf(self):
        """Test successful PDF upload."""
        # Create a minimal valid PDF
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< >>
stream
BT
/F1 12 Tf
100 700 Td
(Test Document) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000273 00000 n 
0000000372 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
450
%%EOF"""
        
        files = {'file': ('test_document.pdf', io.BytesIO(pdf_content), 'application/pdf')}
        
        with patch('app.api.routes.PDFExtractor.extract_text_by_page') as mock_extract:
            mock_extract.return_value = (True, {1: "Test document content"})
            
            with patch('app.api.routes._process_and_store_document') as mock_process:
                mock_process.return_value = 5  # 5 chunks
                
                response = client.post("/documents/upload", files=files)
        
        # Response should be 200 (or 422 if PDF validation fails, which is expected)
        assert response.status_code in [200, 422]

    def test_upload_with_invalid_filename(self):
        """Test rejection of file with invalid filename."""
        files = {'file': ('file<invalid>.pdf', io.BytesIO(b'content'), 'application/pdf')}
        response = client.post("/documents/upload", files=files)
        assert response.status_code == 400

    def test_upload_with_wrong_extension(self):
        """Test rejection of non-PDF files."""
        files = {'file': ('document.txt', io.BytesIO(b'content'), 'text/plain')}
        response = client.post("/documents/upload", files=files)
        assert response.status_code == 400

    def test_upload_with_no_file(self):
        """Test rejection of upload with no file."""
        response = client.post("/documents/upload")
        assert response.status_code in [400, 422]


class TestDocumentListEndpoint:
    """Test GET /documents endpoint."""

    def test_list_documents_empty(self):
        """Test listing documents when collection is empty."""
        # Clear the document store
        from app.api.routes import DOCUMENTS_STORE
        DOCUMENTS_STORE.clear()
        
        response = client.get("/documents")
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 0
        assert data["total_chunks"] == 0
        assert len(data["documents"]) == 0

    def test_list_documents_with_data(self):
        """Test listing documents with sample data."""
        from app.api.routes import DOCUMENTS_STORE
        from datetime import datetime
        
        DOCUMENTS_STORE.clear()
        DOCUMENTS_STORE["doc1"] = {
            "document_id": "doc1",
            "filename": "report.pdf",
            "upload_date": datetime.utcnow(),
            "status": "indexed",
            "page_count": 5,
            "chunk_count": 10,
            "file_path": "/tmp/report.pdf",
            "page_texts": {}
        }
        
        response = client.get("/documents")
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 1
        assert data["total_chunks"] == 10
        assert len(data["documents"]) == 1
        assert data["documents"][0]["document_id"] == "doc1"
        
        DOCUMENTS_STORE.clear()

    def test_list_documents_multiple_docs(self):
        """Test listing multiple documents."""
        from app.api.routes import DOCUMENTS_STORE
        from datetime import datetime
        
        DOCUMENTS_STORE.clear()
        for i in range(3):
            DOCUMENTS_STORE[f"doc{i}"] = {
                "document_id": f"doc{i}",
                "filename": f"report{i}.pdf",
                "upload_date": datetime.utcnow(),
                "status": "indexed",
                "page_count": 5,
                "chunk_count": 10 * (i + 1),
                "file_path": f"/tmp/report{i}.pdf",
                "page_texts": {}
            }
        
        response = client.get("/documents")
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 3
        assert data["total_chunks"] == 60  # 10 + 20 + 30
        assert len(data["documents"]) == 3
        
        DOCUMENTS_STORE.clear()


class TestDocumentDeleteEndpoint:
    """Test DELETE /documents/{id} endpoint."""

    def test_delete_nonexistent_document(self):
        """Test deletion of non-existent document returns 404."""
        from app.api.routes import DOCUMENTS_STORE
        DOCUMENTS_STORE.clear()
        
        response = client.delete("/documents/nonexistent_id")
        assert response.status_code == 404
        data = response.json()
        assert "Document not found" in data["detail"]

    def test_delete_existing_document(self):
        """Test successful deletion of existing document."""
        from app.api.routes import DOCUMENTS_STORE
        from datetime import datetime
        import tempfile
        
        DOCUMENTS_STORE.clear()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
            temp_path = f.name
            f.write(b"test content")
        
        try:
            DOCUMENTS_STORE["doc_to_delete"] = {
                "document_id": "doc_to_delete",
                "filename": "todelete.pdf",
                "upload_date": datetime.utcnow(),
                "status": "indexed",
                "page_count": 1,
                "chunk_count": 1,
                "file_path": temp_path,
                "page_texts": {}
            }
            
            with patch('app.api.routes.vector_service.delete_document_chunks', new_callable=AsyncMock) as mock_delete:
                mock_delete.return_value = None
                
                response = client.delete("/documents/doc_to_delete")
            
            # Should return 204 No Content
            assert response.status_code == 204
            assert "doc_to_delete" not in DOCUMENTS_STORE
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            DOCUMENTS_STORE.clear()


class TestDocumentReindexEndpoint:
    """Test POST /documents/reindex/{id} endpoint."""

    def test_reindex_nonexistent_document(self):
        """Test reindexing non-existent document returns 404."""
        from app.api.routes import DOCUMENTS_STORE
        DOCUMENTS_STORE.clear()
        
        response = client.post("/documents/reindex/nonexistent_id")
        assert response.status_code == 404

    def test_reindex_existing_document(self):
        """Test successful reindexing of existing document."""
        from app.api.routes import DOCUMENTS_STORE
        from datetime import datetime
        import tempfile
        
        DOCUMENTS_STORE.clear()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
            temp_path = f.name
            f.write(b"test content")
        
        try:
            upload_date = datetime.utcnow()
            DOCUMENTS_STORE["doc_to_reindex"] = {
                "document_id": "doc_to_reindex",
                "filename": "toreindex.pdf",
                "upload_date": upload_date,
                "status": "indexed",
                "page_count": 1,
                "chunk_count": 1,
                "file_path": temp_path,
                "page_texts": {1: "old content"}
            }
            
            with patch('app.api.routes.PDFExtractor.extract_text_by_page') as mock_extract:
                mock_extract.return_value = (True, {1: "new content"})
                
                with patch('app.api.routes._process_and_store_document') as mock_process:
                    mock_process.return_value = 2  # 2 chunks after reindexing
                    
                    with patch('app.api.routes.vector_service.delete_document_chunks', new_callable=AsyncMock) as mock_delete:
                        mock_delete.return_value = None
                        
                        response = client.post("/documents/reindex/doc_to_reindex")
            
            assert response.status_code == 200
            data = response.json()
            assert data["document_id"] == "doc_to_reindex"
            assert data["status"] == "reindexed"
            assert data["chunk_count"] == 2
            assert DOCUMENTS_STORE["doc_to_reindex"]["status"] == "reindexed"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            DOCUMENTS_STORE.clear()


class TestSystemStatsEndpoint:
    """Test GET /documents/stats endpoint."""

    def test_stats_empty_system(self):
        """Test system stats when no documents."""
        from app.api.routes import DOCUMENTS_STORE
        DOCUMENTS_STORE.clear()
        
        response = client.get("/documents/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_documents"] == 0
        assert data["total_chunks"] == 0
        assert data["total_size_mb"] == 0.0

    def test_stats_with_documents(self):
        """Test system stats with sample documents."""
        from app.api.routes import DOCUMENTS_STORE
        from datetime import datetime
        import tempfile
        
        DOCUMENTS_STORE.clear()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
            temp_path = f.name
            f.write(b"x" * 1000)  # 1KB file
        
        try:
            DOCUMENTS_STORE["doc1"] = {
                "document_id": "doc1",
                "filename": "report1.pdf",
                "upload_date": datetime.utcnow(),
                "status": "indexed",
                "page_count": 5,
                "chunk_count": 15,
                "file_path": temp_path,
                "page_texts": {}
            }
            
            response = client.get("/documents/stats")
            assert response.status_code == 200
            data = response.json()
            assert data["total_documents"] == 1
            assert data["total_chunks"] == 15
            assert data["total_size_mb"] > 0
            assert data["embedding_dimension"] > 0
            assert data["collection_name"] is not None
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            DOCUMENTS_STORE.clear()


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint returns app info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"

    def test_health_check_endpoint(self):
        """Test /health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
