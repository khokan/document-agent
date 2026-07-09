"""
📋 Pydantic data models for API requests and responses.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    """Response schema for document upload."""

    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original file name")
    upload_date: datetime = Field(default_factory=datetime.utcnow, description="Upload timestamp")
    status: str = Field(default="indexed", description="Document status")
    chunk_count: int = Field(default=0, description="Number of chunks created")

    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "abc_2024",
                "filename": "AnnualReport2024.pdf",
                "upload_date": "2024-07-09T10:30:00",
                "status": "indexed",
                "chunk_count": 142,
            }
        }


class DocumentInfo(BaseModel):
    """Information about a stored document."""

    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original file name")
    upload_date: datetime = Field(..., description="Upload timestamp")
    status: str = Field(..., description="Document status")
    chunk_count: int = Field(default=0, description="Number of chunks")
    page_count: int = Field(default=0, description="Number of pages")


class SearchFilters(BaseModel):
    """Metadata filters for search."""

    company: Optional[str] = Field(None, description="Company name filter")
    year: Optional[int] = Field(None, description="Year filter")
    document: Optional[str] = Field(None, description="Document name filter")
    department: Optional[str] = Field(None, description="Department filter")
    report_type: Optional[str] = Field(None, description="Report type filter")

    class Config:
        json_schema_extra = {
            "example": {"company": "ABC", "year": 2024, "document": "AnnualReport2024.pdf"}
        }


class SearchRequest(BaseModel):
    """Search request schema."""

    question: str = Field(..., description="Search query / question", min_length=1, max_length=1000)
    filters: Optional[SearchFilters] = Field(None, description="Metadata filters")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Why did revenue increase?",
                "filters": {"company": "ABC", "year": 2024},
                "top_k": 5,
            }
        }


class SearchResultSource(BaseModel):
    """Source information for search result."""

    document_id: str = Field(..., description="Document identifier")
    filename: str = Field(..., description="Source document name")
    page: int = Field(..., description="Page number in document")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")
    text: str = Field(..., description="Chunk text")


class SearchResponse(BaseModel):
    """Search response schema."""

    answer: str = Field(..., description="LLM-generated answer")
    sources: List[SearchResultSource] = Field(default=[], description="Source citations")
    query: str = Field(..., description="Original query")
    response_time_ms: float = Field(default=0.0, description="Response time in milliseconds")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Revenue increased due to expanded market reach...",
                "sources": [
                    {
                        "document_id": "abc_2024",
                        "filename": "AnnualReport2024.pdf",
                        "page": 34,
                        "score": 0.95,
                        "text": "Revenue increased...",
                    }
                ],
                "query": "Why did revenue increase?",
                "response_time_ms": 2341.5,
            }
        }


class DocumentListResponse(BaseModel):
    """Response for listing documents."""

    documents: List[DocumentInfo] = Field(default=[], description="List of documents")
    total_count: int = Field(default=0, description="Total document count")
    total_chunks: int = Field(default=0, description="Total chunks across all documents")


class SystemStats(BaseModel):
    """System statistics."""

    total_documents: int = Field(default=0, description="Total indexed documents")
    total_chunks: int = Field(default=0, description="Total chunks")
    total_size_mb: float = Field(default=0.0, description="Total storage in MB")
    embedding_dimension: int = Field(default=768, description="Embedding dimension")
    collection_name: str = Field(default="company_documents", description="ChromaDB collection name")


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid PDF file",
                "details": "File is not a valid PDF (invalid magic bytes)",
                "status_code": 400,
            }
        }
