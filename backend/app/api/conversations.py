"""
Conversation management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import (
    ConversationCreateRequest,
    ConversationUpdateRequest,
    ConversationResponse,
    ConversationDetailResponse,
    ConversationListResponse,
    ChatMessageResponse,
    MessageListResponse,
    SearchResultSource,
)
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["Conversations"])


def _parse_sources(sources_json: str):
    if not sources_json:
        return None
    import json
    try:
        return [SearchResultSource(**s) for s in json.loads(sources_json)]
    except Exception:
        return None


def _conversation_to_response(conv, message_count=0):
    return ConversationResponse(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        message_count=message_count,
    )


def _message_to_response(msg):
    return ChatMessageResponse(
        id=msg.id,
        role=msg.role,
        content=msg.content,
        sources=_parse_sources(msg.sources_json),
        created_at=msg.created_at,
    )


@router.get(
    "",
    response_model=ConversationListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_conversations(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)
    conversations, total = service.list_conversations(limit=limit, offset=offset)
    return ConversationListResponse(
        conversations=[_conversation_to_response(c, len(c.messages)) for c in conversations],
        total=total,
    )


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)
    conv = service.create_conversation(title=request.title or "New Chat")
    return _conversation_to_response(conv, 0)


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailResponse,
    status_code=status.HTTP_200_OK,
)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)
    conv = service.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages, total = service.get_messages(conversation_id)
    return ConversationDetailResponse(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        message_count=total,
        messages=[_message_to_response(m) for m in messages],
    )


@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
    status_code=status.HTTP_200_OK,
)
async def update_conversation(
    conversation_id: str,
    request: ConversationUpdateRequest,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)
    conv = service.update_conversation(conversation_id, title=request.title)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return _conversation_to_response(conv, len(conv.messages))


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)
    deleted = service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")


@router.get(
    "/{conversation_id}/messages",
    response_model=MessageListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_messages(
    conversation_id: str,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)
    conv = service.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages, total = service.get_messages(conversation_id, limit=limit, offset=offset)
    return MessageListResponse(
        messages=[_message_to_response(m) for m in messages],
        total=total,
    )
