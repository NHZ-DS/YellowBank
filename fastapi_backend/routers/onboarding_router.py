"""Routeur pour le Questionnaire d'Entrée et l'attribution de parcours."""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from utils import get_db
from services.onboarding_service import onboarding_service_instance

router = APIRouter(prefix="/onboarding", tags=["Onboarding & Questionnaire"])


class QuestionnaireSubmission(BaseModel):
    user_id: int
    objective: str  # 'gerer_budget', 'bourse_investir', 'financer_projet'
    knowledge_level: str  # 'debutant', 'intermediaire', 'avance'
    time_horizon: str  # 'court_terme', 'moyen_terme', 'long_terme'


@router.post("/submit")
def submit_questionnaire(submission: QuestionnaireSubmission, db: Session = Depends(get_db)):
    """Soumet le questionnaire d'entrée et calcule le parcours recommandé."""
    answers = {
        "objective": submission.objective,
        "knowledge_level": submission.knowledge_level,
        "time_horizon": submission.time_horizon
    }
    result = onboarding_service_instance.process_questionnaire(db, submission.user_id, answers)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
