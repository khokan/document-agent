"""
🔌 FastAPI RAG routes for question answering, chat, and summarization.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from app.models.schemas import (
    SearchRequest,
    SearchResponse,
    ChatRequest,
    ChatResponse,
    SummarizeRequest,
    SummarizeResponse,
    ErrorResponse,
)
from app.api.deps import get_rag_pipeline, get_retriever_service
from app.rag.pipeline import RAGPipeline
from app.rag.retriever import Retriever
from app.services.conversation_service import ConversationService
from app.utils.logger import logger
from app.models.database import get_db
from sqlalchemy.orm import Session

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
    Supports metadata filtering and score threshold.
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
            top_k=request.top_k,
            score_threshold=request.score_threshold
        )

        return SearchResponse(**result)

    except Exception as e:
        logger.error(f"[API] Error during RAG query execution: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"RAG query failed: {str(e)}"
        )


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def chat_rag(
    request: ChatRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
    db: Session = Depends(get_db),
):
    """
    Multi-turn conversation with RAG context.

    Accepts conversation history and generates a context-aware response
    using retrieved document chunks and previous messages.
    Optionally persists messages to database if conversation_id is provided.
    """
    try:
        logger.info(f"[API] RAG chat message: '{request.message}' (history={len(request.history)} msgs)")

        service = ConversationService(db)

        # Resolve conversation: create new if no conversation_id
        conversation_id = request.conversation_id
        if conversation_id:
            conv = service.get_conversation(conversation_id)
            if not conv:
                conv = service.create_conversation()
                conversation_id = conv.id
            history = service.get_history_for_llm(conversation_id)
        else:
            conv = service.create_conversation()
            conversation_id = conv.id
            history = None

        # If no DB history, fall back to request history
        if not history and request.history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.history
            ]

        # Convert filters to dict
        filters_dict = None
        if request.filters:
            filters_dict = request.filters.model_dump(exclude_none=True)

        # Run chat pipeline
        result = await pipeline.chat(
            question=request.message,
            history=history,
            filters=filters_dict,
            top_k=request.top_k,
            score_threshold=request.score_threshold
        )

        # Persist messages
        service.add_message(conversation_id, "user", request.message)
        service.add_message(
            conversation_id,
            "assistant",
            result.get("answer", ""),
            sources=result.get("sources"),
        )

        return ChatResponse(
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
            query=result.get("query", request.message),
            conversation_id=conversation_id,
            response_time_ms=result.get("response_time_ms", 0.0),
            retrieval_time_ms=result.get("retrieval_time_ms", 0.0),
            generation_time_ms=result.get("generation_time_ms", 0.0),
        )

    except Exception as e:
        logger.error(f"[API] Error during RAG chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"RAG chat failed: {str(e)}"
        )


@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def summarize_document(
    request: SummarizeRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
):
    """
    Generate a summary of a specific indexed document.

    Retrieves all chunks for the given document and generates a
    comprehensive summary using the LLM.
    """
    try:
        logger.info(f"[API] Summarize document: '{request.document_id}'")

        # Convert filters to dict
        filters_dict = None
        if request.filters:
            filters_dict = request.filters.model_dump(exclude_none=True)

        # Run summarization
        result = await pipeline.summarize(
            document_id=request.document_id,
            filters=filters_dict,
            top_k=request.max_chunks
        )

        return SummarizeResponse(**result)

    except Exception as e:
        logger.error(f"[API] Error during document summarization: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )


@router.post(
    "/stream",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def stream_rag_response(
    request: SearchRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
    retriever: Retriever = Depends(get_retriever_service)
):
    """
    Stream a RAG response using Server-Sent Events (SSE).

    Retrieves relevant context and streams the LLM response token by token.
    """
    try:
        logger.info(f"[API] RAG stream query: '{request.question}'")

        # Convert filters to dict
        filters_dict = None
        if request.filters:
            filters_dict = request.filters.model_dump(exclude_none=True)

        # Retrieve context chunks
        context_chunks = await retriever.retrieve(
            query=request.question,
            top_k=request.top_k,
            filters=filters_dict,
            score_threshold=request.score_threshold
        )

        # Rank chunks
        ranked_chunks = pipeline.ranker.rank(context_chunks)

        # Create streaming generator
        async def event_generator():
            async for token in pipeline.generator.generate_streaming_response(
                request.question, ranked_chunks
            ):
                yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    except Exception as e:
        logger.error(f"[API] Error during RAG streaming: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"RAG streaming failed: {str(e)}"
        )
