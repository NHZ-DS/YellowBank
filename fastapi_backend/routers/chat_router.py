"""Routeur de messagerie conversationnelle et RAG."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from utils import get_db
from models.message import ChatMessageRequest, ChatMessageResponse
from services.chat_service.orchestrator import chat_orchestrator_instance

router = APIRouter(prefix="/chat", tags=["Chat & Multi-Agents"])


@router.post("/message", response_model=ChatMessageResponse)
def send_message(req: ChatMessageRequest, db: Session = Depends(get_db)):
    """Reçoit un message utilisateur, le dispatche vers le bon agent et retourne la réponse."""
    return chat_orchestrator_instance.route_and_respond(
        db=db,
        user_id=req.user_id,
        query=req.message,
        track=req.track or "courant",
        conversation_id=req.conversation_id
    )


@router.get("/market-briefing/{sector}")
def get_market_briefing(sector: str = "tech"):
    """Génère un point de veille de marché factuel avec indicateur d'ambiance et sources."""
    from services.chat_service.agents.market_agent import market_agent_instance
    return market_agent_instance.get_briefing(sector)

