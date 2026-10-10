"""Moteur de Gamification : Missions, XP, Niveaux et Badges."""

from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models.user import UserModel
from models.mission import MissionModel, UserMissionModel, UserBadgeModel, MissionOut, BadgeOut


DEFAULT_MISSIONS = [
    # Parcours Courant
    {"track": "courant", "title": "Paramètre ton alerte solde bas", "description": "Configure une notification push si ton compte passe sous 50 €.", "xp": 50, "badge": "Sentinelle du Solde"},
    {"track": "courant", "title": "Catégorise tes dépenses du mois", "description": "Vérifie la répartition de tes achats dans le graphique de budget.", "xp": 40, "badge": None},
    {"track": "courant", "title": "Commande ta carte ou teste le sans contact", "description": "Effectue un premier paiement sécurisé par mobile ou carte.", "xp": 50, "badge": "Paiement Express"},
    
    # Parcours PEA
    {"track": "pea", "title": "Découvre les 5 ans du PEA", "description": "Comprends pourquoi les gains sont exonérés d'impôt sur le revenu après 5 ans.", "xp": 60, "badge": "Épargnant Sage"},
    {"track": "pea", "title": "Investis tes 100 premiers euros", "description": "Place tes premiers 100 € sur un ETF mondial diversifié éligible.", "xp": 100, "badge": "Explorateur Bourse"},
    {"track": "pea", "title": "Évalue ton profil de risque", "description": "Réponds aux 3 questions pour définir ton horizon d'investissement.", "xp": 50, "badge": None},
    
    # Parcours Projets & Aides
    {"track": "projets", "title": "Simule tes droits APL", "description": "Vérifie en 2 minutes le montant d'aide au logement auquel tu as droit.", "xp": 60, "badge": "Chasseur d'Aides"},
    {"track": "projets", "title": "Estime ton budget d'installation", "description": "Calcule la caution, le premier loyer et l'assurance habitation.", "xp": 50, "badge": None},
    {"track": "projets", "title": "Active la garantie Visale", "description": "Obtiens ta caution locative gratuite garantie par l'État.", "xp": 70, "badge": "Clés en Main"},
]


class GamificationService:
    """Gère l'attribution des points d'XP, la complétion des missions et les badges."""

    def initialize_default_missions(self, db: Session):
        """Initialise le catalogue de missions dans la base si vide."""
        if db.query(MissionModel).count() == 0:
            for m in DEFAULT_MISSIONS:
                db_m = MissionModel(
                    track=m["track"],
                    title=m["title"],
                    description=m["description"],
                    xp_reward=m["xp"],
                    badge_reward=m["badge"],
                    is_challenge=False
                )
                db.add(db_m)
            db.commit()

    def get_user_progress(self, db: Session, user_id: int) -> Dict[str, Any]:
        self.initialize_default_missions(db)
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return {"error": "Utilisateur introuvable"}

        # Récupérer les missions du parcours de l'utilisateur
        track_missions = db.query(MissionModel).filter(MissionModel.track == user.current_track).all()
        
        # Récupérer les statuts complétés
        user_missions = {um.mission_id: um.status for um in db.query(UserMissionModel).filter(UserMissionModel.user_id == user_id).all()}

        missions_out = []
        for m in track_missions:
            status = user_missions.get(m.id, "available")
            missions_out.append({
                "id": m.id,
                "track": m.track,
                "title": m.title,
                "description": m.description,
                "xp_reward": m.xp_reward,
                "badge_reward": m.badge_reward,
                "is_challenge": m.is_challenge,
                "status": status
            })

        # Récupérer les badges acquis
        badges = db.query(UserBadgeModel).filter(UserBadgeModel.user_id == user_id).all()

        return {
            "user_id": user.id,
            "xp_points": user.xp_points,
            "level": max(1, user.xp_points // 100),
            "current_track": user.current_track,
            "badges": [{"id": b.id, "badge_name": b.badge_name, "badge_icon": b.badge_icon, "description": b.description, "unlocked_at": b.unlocked_at} for b in badges],
            "active_missions": missions_out,
            "completed_missions_count": sum(1 for m in missions_out if m["status"] == "completed")
        }

    def complete_mission(self, db: Session, user_id: int, mission_id: int) -> Dict[str, Any]:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        mission = db.query(MissionModel).filter(MissionModel.id == mission_id).first()
        if not user or not mission:
            return {"error": "Mission ou utilisateur introuvable"}

        um = db.query(UserMissionModel).filter(
            UserMissionModel.user_id == user_id,
            UserMissionModel.mission_id == mission_id
        ).first()

        if not um:
            um = UserMissionModel(user_id=user_id, mission_id=mission_id, status="completed", completed_at=datetime.utcnow())
            db.add(um)
        else:
            um.status = "completed"
            um.completed_at = datetime.utcnow()

        # Gain d'XP
        user.xp_points += mission.xp_reward
        user.level = max(1, user.xp_points // 100)

        # Déblocage de badge éventuel
        badge_awarded = None
        if mission.badge_reward:
            existing_badge = db.query(UserBadgeModel).filter(
                UserBadgeModel.user_id == user_id,
                UserBadgeModel.badge_name == mission.badge_reward
            ).first()
            if not existing_badge:
                new_badge = UserBadgeModel(
                    user_id=user_id,
                    badge_name=mission.badge_reward,
                    badge_icon="🏅",
                    description=f"Récompense pour la mission : {mission.title}"
                )
                db.add(new_badge)
                badge_awarded = mission.badge_reward

        db.commit()
        return {
            "success": True,
            "xp_gained": mission.xp_reward,
            "total_xp": user.xp_points,
            "level": user.level,
            "badge_unlocked": badge_awarded
        }


gamification_service_instance = GamificationService()
