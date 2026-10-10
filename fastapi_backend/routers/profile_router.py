"""Routeur de Gestion de Profil et Conformité RGPD."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from utils import get_db
from models.user import UserOut, UserUpdate
from services.profile_service import profile_service_instance
from services.compliance_service import compliance_service_instance

router = APIRouter(prefix="/profile", tags=["Profil & Espace Client"])


class ConsentUpdate(BaseModel):
    user_id: int
    advisor_share_consent: bool


@router.get("/{user_id}", response_model=UserOut)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Retourne les informations du profil utilisateur."""
    user = profile_service_instance.get_profile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user_profile(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    """Met à jour les informations du profil utilisateur."""
    user = profile_service_instance.update_profile(db, user_id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    return user


@router.post("/consent")
def update_advisor_consent(consent_in: ConsentUpdate, db: Session = Depends(get_db)):
    """Met à jour le consentement RGPD pour le partage avec le conseiller."""
    return compliance_service_instance.update_consent(db, consent_in.user_id, consent_in.advisor_share_consent)


@router.get("/advisor-report/{user_id}")
def get_advisor_report(user_id: int, db: Session = Depends(get_db)):
    """Génère le compte-rendu pour le conseiller humain si le client a donné son accord."""
    return compliance_service_instance.generate_advisor_report(db, user_id)
