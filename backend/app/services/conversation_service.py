"""
Conversation service for chat persistence.
"""

import json
import uuid
from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.database import Conversation, ChatMessageModel


class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def list_conversations(self, limit: int = 50, offset: int = 0) -> Tuple[List[Conversation], int]:
        total = self.db.query(func.count(Conversation.id)).scalar()
        conversations = (
            self.db.query(Conversation)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return conversations, total

    def create_conversation(self, title: str = "New Chat") -> Conversation:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def update_conversation(self, conversation_id: str, title: str) -> Optional[Conversation]:
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None
        conversation.title = title
        conversation.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: str) -> bool:
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return False
        self.db.delete(conversation)
        self.db.commit()
        return True

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        sources: Optional[list] = None,
    ) -> ChatMessageModel:
        sources_json = json.dumps(sources) if sources else None
        message = ChatMessageModel(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            sources_json=sources_json,
            created_at=datetime.utcnow(),
        )
        self.db.add(message)

        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages(
        self, conversation_id: str, limit: int = 100, offset: int = 0
    ) -> Tuple[List[ChatMessageModel], int]:
        total = (
            self.db.query(func.count(ChatMessageModel.id))
            .filter(ChatMessageModel.conversation_id == conversation_id)
            .scalar()
        )
        messages = (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.conversation_id == conversation_id)
            .order_by(ChatMessageModel.created_at)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return messages, total

    def get_history_for_llm(self, conversation_id: str) -> List[dict]:
        messages, _ = self.get_messages(conversation_id)
        return [{"role": m.role, "content": m.content} for m in messages]
