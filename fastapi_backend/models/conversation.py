"""Modèles d'Historique de Conversation (SQLAlchemy & Pydantic)."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from pydantic import BaseModel

from utils import Base


class ConversationModel(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    title = Column(String(150), default="Échange avec Archipel")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MessageRecordModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True, nullable=False)
    sender = Column(String(20), nullable=False)  # 'user' ou 'assistant'
    content = Column(Text, nullable=False)
    agent = Column(String(50), default="rag_agent")
    confidence_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class MessageRecordOut(BaseModel):
    id: int
    sender: str
    content: str
    agent: str
    confidence_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationOut(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime
    messages: List[MessageRecordOut] = []

    class Config:
        from_attributes = True
