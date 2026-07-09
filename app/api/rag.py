"""
🔌 FastAPI RAG routes for question answering over document chunks.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import SearchRequest, SearchResponse, ErrorResponse
from app.api.deps import get_rag_pipeline
from app.rag.pipeline import RAGPipeline
from app.utils.logger import logger

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post(
    "/query",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def query_rag(
    request: SearchRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
):
    """
    Perform Retrieval-Augmented Generation (RAG) query.

    Retrieves relevant document context and uses local LLM to generate an answer.
    """
    try:
        logger.info(f"[API] RAG query: '{request.question}'")

        # Convert filters to dict
        filters_dict = None
        if request.filters:
            filters_dict = request.filters.model_dump(exclude_none=True)

        # Run pipeline
        result = await pipeline.query(
            question=request.question,
            filters=filters_dict,
            top_k=request.top_k
        )

        return SearchResponse(**result)

    except Exception as e:
        logger.error(f"[API] Error during RAG query execution: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"RAG query failed: {str(e)}"
        )
