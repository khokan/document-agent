"""
Database models and session management for chat persistence.
"""

import os
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    DateTime,
    Integer,
    Index,
    ForeignKey,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
)

from app.utils.config import config

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False, default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    messages = relationship(
        "ChatMessageModel",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ChatMessageModel.created_at",
    )

    __table_args__ = (
        Index("ix_conversations_updated_at", "updated_at"),
    )


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True)
    conversation_id = Column(
        String(36),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    sources_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")

    __table_args__ = (
        Index("ix_chat_messages_conversation_id", "conversation_id"),
    )


class DocumentRecord(Base):
    """Durable source-of-truth for uploaded PDFs and their indexing state."""

    __tablename__ = "documents"

    document_id = Column(String(255), primary_key=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_hash = Column(String(64), nullable=False, unique=True)
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(32), nullable=False, default="indexed")
    page_count = Column(Integer, nullable=False, default=0)
    chunk_count = Column(Integer, nullable=False, default=0)
    embedding_fingerprint = Column(String(64), nullable=True)

    __table_args__ = (Index("ix_documents_file_hash", "file_hash"),)


# Ensure database directory exists before creating engine
_db_url = config.database_url
if "sqlite" in _db_url:
    _db_path = _db_url.split("sqlite:///")[-1]
    _db_dir = os.path.dirname(_db_path)
    if _db_dir:
        os.makedirs(_db_dir, exist_ok=True)

engine = create_engine(
    config.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in config.database_url else {},
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
