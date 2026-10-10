"""Schémas des Messages et Citations RAG."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SourceCitation(BaseModel):
    """Citation d'une source documentaire issue du RAG."""
    document_title: str
    snippet: str
    relevance_score: float  # entre 0.0 et 1.0


class ActionSuggestion(BaseModel):
    """Suggestion d'action que l'utilisateur peut choisir de valider."""
    action_type: str  # ex: 'OPEN_PEA', 'SET_ALERT', 'START_MISSION'
    label: str
    payload: Dict[str, Any] = Field(default_factory=dict)


class ChatMessageRequest(BaseModel):
    """Requête envoyée par le frontend Streamlit."""
    user_id: int
    message: str
    track: Optional[str] = "courant"  # Contexte du parcours en cours
    conversation_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Réponse structurée retournée par le backend FastAPI."""
    conversation_id: int
    sender_agent: str  # 'rag_agent', 'faq_agent', 'chitchat_agent'
    content: str
    confidence_score: float  # Score de confiance (ex: 0.94)
    sources: List[SourceCitation] = Field(default_factory=list)
    suggested_actions: List[ActionSuggestion] = Field(default_factory=list)
    risk_level: str = "faible"  # 'faible', 'moyen', 'eleve'
    timestamp: datetime = Field(default_factory=datetime.utcnow)
