"""
Pytest configuration and fixtures for the test suite.

Provides:
- Test client fixture
- Sample PDF fixtures
- Mock fixtures for services
- Database cleanup
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Fixture for FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def temp_dir():
    """Fixture for temporary directory."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    
    # Cleanup
    import shutil
    if Path(temp_path).exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def sample_pdf_content():
    """Fixture for minimal valid PDF content."""
    return b"""%PDF-1.4
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
(Sample Test Document) Tj
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


@pytest.fixture
def invalid_pdf_content():
    """Fixture for invalid PDF content (corrupted)."""
    return b"INVALID_PDF_CONTENT_NOT_A_REAL_PDF"


@pytest.fixture
def mock_vector_service():
    """Fixture for mocked vector service."""
    service = AsyncMock()
    service.add_chunks = AsyncMock(return_value=True)
    service.delete_document_chunks = AsyncMock(return_value=True)
    service.search = AsyncMock(return_value=[])
    return service


@pytest.fixture
def mock_embedding_service():
    """Fixture for mocked embedding service."""
    service = AsyncMock()
    service.get_embeddings = AsyncMock(return_value=[[0.1, 0.2, 0.3]])
    return service


@pytest.fixture
def mock_config():
    """Fixture for mocked configuration."""
    config = MagicMock()
    config.app_name = "PDF Knowledge Assistant"
    config.app_version = "1.0.0"
    config.upload_dir = "/tmp/uploads"
    config.temp_dir = "/tmp/temp"
    config.embedding_dimension = 768
    config.chroma_collection_name = "company_documents"
    config.max_file_size_mb = 100
    config.max_filename_length = 255
    return config


@pytest.fixture(autouse=True)
def cleanup_documents_store():
    """Fixture to cleanup documents store before and after each test."""
    from app.api.routes import DOCUMENTS_STORE
    DOCUMENTS_STORE.clear()
    yield
    DOCUMENTS_STORE.clear()


@pytest.fixture
def sample_document_store():
    """Fixture for sample data in documents store."""
    from app.api.routes import DOCUMENTS_STORE
    from datetime import datetime
    
    DOCUMENTS_STORE.clear()
    DOCUMENTS_STORE["doc1"] = {
        "document_id": "doc1",
        "filename": "Annual_Report_2024.pdf",
        "upload_date": datetime.utcnow(),
        "status": "indexed",
        "page_count": 50,
        "chunk_count": 150,
        "file_path": "/tmp/uploads/doc1.pdf",
        "page_texts": {i: f"Page {i} content" for i in range(1, 51)}
    }
    DOCUMENTS_STORE["doc2"] = {
        "document_id": "doc2",
        "filename": "Quarterly_Report_Q1.pdf",
        "upload_date": datetime.utcnow(),
        "status": "indexed",
        "page_count": 25,
        "chunk_count": 75,
        "file_path": "/tmp/uploads/doc2.pdf",
        "page_texts": {i: f"Page {i} content" for i in range(1, 26)}
    }
    
    yield DOCUMENTS_STORE
    
    DOCUMENTS_STORE.clear()


# Configure pytest
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "error_handling: mark test as testing error handling"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
