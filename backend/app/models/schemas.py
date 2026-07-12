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
    score_threshold: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Minimum similarity score threshold"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Why did revenue increase?",
                "filters": {"company": "ABC", "year": 2024},
                "top_k": 5,
                "score_threshold": 0.3,
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
    response_time_ms: float = Field(default=0.0, description="Total response time in milliseconds")
    retrieval_time_ms: float = Field(default=0.0, description="Retrieval phase time in milliseconds")
    generation_time_ms: float = Field(default=0.0, description="Generation phase time in milliseconds")
    cached: bool = Field(default=False, description="Whether the response was served from cache")

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
                "retrieval_time_ms": 341.2,
                "generation_time_ms": 2000.3,
                "cached": False,
            }
        }


# --- Sprint 3: Chat Models ---


class ChatMessage(BaseModel):
    """Single message in a conversation."""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content", min_length=1)

    class Config:
        json_schema_extra = {
            "example": {"role": "user", "content": "What was last year's revenue?"}
        }


class ChatRequest(BaseModel):
    """Multi-turn chat request schema."""

    message: str = Field(..., description="Current user message", min_length=1, max_length=2000)
    history: List[ChatMessage] = Field(
        default=[], description="Previous conversation messages"
    )
    filters: Optional[SearchFilters] = Field(None, description="Metadata filters")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of context chunks to retrieve")
    score_threshold: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Minimum similarity score threshold"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "How does that compare to the previous year?",
                "history": [
                    {"role": "user", "content": "What was last year's revenue?"},
                    {"role": "assistant", "content": "Last year's revenue was $10M."},
                ],
                "filters": {"company": "ABC"},
                "top_k": 5,
            }
        }


class ChatResponse(BaseModel):
    """Multi-turn chat response schema."""

    answer: str = Field(..., description="LLM-generated answer")
    sources: List[SearchResultSource] = Field(default=[], description="Source citations")
    query: str = Field(..., description="Current user message")
    response_time_ms: float = Field(default=0.0, description="Total response time")
    retrieval_time_ms: float = Field(default=0.0, description="Retrieval time")
    generation_time_ms: float = Field(default=0.0, description="Generation time")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Compared to the previous year, revenue grew by 15%...",
                "sources": [
                    {
                        "document_id": "abc_2024",
                        "filename": "AnnualReport2024.pdf",
                        "page": 12,
                        "score": 0.91,
                        "text": "Year-over-year revenue growth...",
                    }
                ],
                "query": "How does that compare to the previous year?",
                "response_time_ms": 1850.0,
                "retrieval_time_ms": 250.0,
                "generation_time_ms": 1600.0,
            }
        }


# --- Sprint 3: Summarization Models ---


class SummarizeRequest(BaseModel):
    """Document summarization request schema."""

    document_id: str = Field(..., description="ID of the document to summarize")
    filters: Optional[SearchFilters] = Field(None, description="Additional metadata filters")
    max_chunks: int = Field(default=20, ge=1, le=50, description="Maximum chunks to include in context")

    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "acme_2024_abc123",
                "max_chunks": 20,
            }
        }


class SummarizeResponse(BaseModel):
    """Document summarization response schema."""

    summary: str = Field(..., description="Generated summary text")
    document_id: str = Field(..., description="Summarized document ID")
    chunks_used: int = Field(default=0, description="Number of chunks used for summary")
    response_time_ms: float = Field(default=0.0, description="Total response time")
    retrieval_time_ms: float = Field(default=0.0, description="Retrieval time")
    generation_time_ms: float = Field(default=0.0, description="Generation time")

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "The annual report highlights key growth areas...",
                "document_id": "acme_2024_abc123",
                "chunks_used": 15,
                "response_time_ms": 3500.0,
                "retrieval_time_ms": 200.0,
                "generation_time_ms": 3300.0,
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
