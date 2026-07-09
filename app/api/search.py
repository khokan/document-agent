"""
🔌 FastAPI search routes for semantic document search.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.schemas import SearchRequest, SearchResultSource, ErrorResponse
from app.api.deps import get_retriever_service
from app.rag.retriever import Retriever
from app.utils.logger import logger

router = APIRouter(prefix="/search", tags=["Search"])


@router.post(
    "",
    response_model=List[SearchResultSource],
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def semantic_search(
    request: SearchRequest,
    retriever: Retriever = Depends(get_retriever_service)
):
    """
    Perform semantic search on indexed document chunks.

    Returns:
        List of matching sources with relevance scores
    """
    try:
        logger.info(f"[API] Semantic search query: '{request.question}'")
        
        # Extract filters as dict
        filters_dict = None
        if request.filters:
            filters_dict = request.filters.model_dump(exclude_none=True)

        # Retrieve documents
        matches = await retriever.retrieve(
            query=request.question,
            top_k=request.top_k,
            filters=filters_dict
        )

        # Format output matching SearchResultSource schema
        results = []
        for match in matches:
            metadata = match["metadata"]
            results.append(
                SearchResultSource(
                    document_id=metadata.get("document_id", "unknown"),
                    filename=metadata.get("original_filename", metadata.get("filename", "unknown")),
                    page=metadata.get("page_number", 1),
                    score=match["score"],
                    text=match["text"]
                )
            )

        return results

    except Exception as e:
        logger.error(f"[API] Error during semantic search: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {str(e)}"
        )
