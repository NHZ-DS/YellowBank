"""Orchestrateur central du système Multi-Agents de chat."""

import re
from typing import Dict, Any
from sqlalchemy.orm import Session

from services.chat_service.agents.faq_agent import faq_agent_instance
from services.chat_service.agents.rag_agent import rag_agent_instance
from services.chat_service.agents.chitchat_agent import chitchat_agent_instance
from models.conversation import ConversationModel, MessageRecordModel


GREETING_PATTERNS = [
    r"\b(bonjour|salut|coucou|hello|bonsoir|hey)\b",
    r"\b(qui es[- ]tu|c[' ]est quoi archipel|comment ca va|merci)\b"
]


class ChatOrchestrator:
    """Analyse l'intention du message et délègue au bon agent conversationnel."""

    def route_and_respond(self, db: Session, user_id: int, query: str, track: str = "courant", conversation_id: int = None) -> Dict[str, Any]:
        # 1. Gestion ou création de la conversation
        if conversation_id:
            conv = db.query(ConversationModel).filter(ConversationModel.id == conversation_id, ConversationModel.user_id == user_id).first()
        else:
            conv = None

        if not conv:
            conv = ConversationModel(user_id=user_id, title=f"Échange : {query[:35]}...")
            db.add(conv)
            db.commit()
            db.refresh(conv)

        # Enregistrer le message de l'utilisateur
        user_msg = MessageRecordModel(
            conversation_id=conv.id,
            sender="user",
            content=query,
            agent="user",
            confidence_score=1.0
        )
        db.add(user_msg)
        db.commit()

        # 2. Qualification de l'intention et routage
        q_lower = query.lower().strip()

        # A. Vérifier la FAQ d'abord (réponse instantanée)
        if faq_agent_instance.can_handle(q_lower):
            agent_name = "faq_agent"
            result = faq_agent_instance.process(q_lower)

        # B. Vérifier si c'est du Chitchat / Salutation
        elif any(re.search(p, q_lower) for p in GREETING_PATTERNS) and len(query.split()) <= 6:
            agent_name = "chitchat_agent"
            result = chitchat_agent_instance.process(query, track=track)

        # C. Par défaut : Agent RAG avec recherche documentaire
        else:
            agent_name = "rag_agent"
            result = rag_agent_instance.process(query, track=track)

        # 3. Enregistrer la réponse de l'assistant dans la DB
        assistant_msg = MessageRecordModel(
            conversation_id=conv.id,
            sender="assistant",
            content=result["content"],
            agent=agent_name,
            confidence_score=result["confidence_score"]
        )
        db.add(assistant_msg)
        db.commit()

        # 4. Formater la réponse finale
        return {
            "conversation_id": conv.id,
            "sender_agent": agent_name,
            "content": result["content"],
            "confidence_score": result["confidence_score"],
            "sources": result.get("sources", []),
            "suggested_actions": result.get("suggested_actions", []),
            "risk_level": result.get("risk_level", "faible")
        }


chat_orchestrator_instance = ChatOrchestrator()
