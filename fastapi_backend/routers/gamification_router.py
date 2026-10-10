"""Routeur de Gamification (Missions, XP, Badges)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from utils import get_db
from models.mission import GamificationProfileOut
from services.gamification_service import gamification_service_instance

router = APIRouter(prefix="/gamification", tags=["Gamification & Badges"])


class CompleteMissionRequest(BaseModel):
    user_id: int
    mission_id: int


@router.get("/progress/{user_id}", response_model=GamificationProfileOut)
def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    """Récupère la progression, le niveau, les badges et les missions de l'utilisateur."""
    result = gamification_service_instance.get_user_progress(db, user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/complete-mission")
def complete_mission(req: CompleteMissionRequest, db: Session = Depends(get_db)):
    """Valide la réalisation d'une mission et attribue XP et éventuel badge."""
    result = gamification_service_instance.complete_mission(db, req.user_id, req.mission_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
