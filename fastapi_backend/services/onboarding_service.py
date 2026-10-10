"""Service de traitement du Questionnaire d'Entrée et d'orientation de parcours."""

from typing import Dict, Any
from sqlalchemy.orm import Session
from models.user import UserModel
from models.mission import UserBadgeModel, MissionModel, UserMissionModel


class OnboardingService:
    """Analyse les réponses du questionnaire et oriente l'utilisateur vers son parcours."""

    def process_questionnaire(self, db: Session, user_id: int, answers: Dict[str, Any]) -> Dict[str, Any]:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return {"error": "Utilisateur introuvable"}

        objective = answers.get("objective", "gerer_budget")
        knowledge_level = answers.get("knowledge_level", "debutant")
        time_horizon = answers.get("time_horizon", "court_terme")

        # Règle d'attribution du parcours type
        if objective == "bourse_investir" or (objective != "financer_projet" and knowledge_level in ("intermediaire", "avance") and time_horizon == "long_terme"):
            recommended_track = "pea"
            track_title = "Le Parcours PEA (Investissement & Bourse Progressive)"
            track_desc = "Découvrez la bourse pas à pas, comprenez le fonctionnement d'un PEA et investissez vos premiers 100 € en toute sérénité."
        elif objective == "financer_projet":
            recommended_track = "projets"
            track_title = "Le Parcours Projets & Aides"
            track_desc = "Optimisez vos aides (APL, bourses, garantie Visale) et budgétez votre projet de vie (logement, études, voyage)."
        else:
            recommended_track = "courant"
            track_title = "Le Parcours Courant (Gestion au Quotidien)"
            track_desc = "Prenez le contrôle de votre budget, paramétrez vos alertes de solde bas et catégorisez vos dépenses facilement."

        # Mise à jour du parcours de l'utilisateur et gain d'XP
        user.current_track = recommended_track
        user.xp_points += 100
        user.level = 1

        # Attribution automatique du premier badge "Bienvenue à bord"
        existing_badge = db.query(UserBadgeModel).filter(
            UserBadgeModel.user_id == user_id,
            UserBadgeModel.badge_name == "Bienvenue à bord"
        ).first()
        
        if not existing_badge:
            welcome_badge = UserBadgeModel(
                user_id=user_id,
                badge_name="Bienvenue à bord",
                badge_icon="🏝️",
                description="A complété son questionnaire d'entrée et rejoint l'île d'Yellow."
            )
            db.add(welcome_badge)

        db.commit()
        db.refresh(user)

        return {
            "recommended_track": recommended_track,
            "track_title": track_title,
            "track_description": track_desc,
            "xp_awarded": 100,
            "badge_unlocked": "Bienvenue à bord"
        }


onboarding_service_instance = OnboardingService()
