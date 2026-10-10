"""Service de Conformité RGPD et Synthèse pour le Conseiller Bancaire Humain."""

from typing import Dict, Any
from sqlalchemy.orm import Session
from models.user import UserModel
from models.conversation import ConversationModel, MessageRecordModel
from utils import calculate_debt_ratio


class ComplianceService:
    """Gère le consentement de partage RGPD et la production du compte-rendu conseiller."""

    def update_consent(self, db: Session, user_id: int, consent: bool) -> Dict[str, Any]:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return {"error": "Utilisateur introuvable"}

        user.advisor_share_consent = consent
        db.commit()
        return {
            "user_id": user.id,
            "advisor_share_consent": user.advisor_share_consent,
            "message": "Consentement de partage mis à jour avec succès."
        }

    def generate_advisor_report(self, db: Session, user_id: int) -> Dict[str, Any]:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return {"error": "Utilisateur introuvable"}

        if not user.advisor_share_consent:
            return {
                "authorized": False,
                "message": (
                    "Ce client n'a pas autorisé le partage de ses interactions avec son conseiller. "
                    "Conformément au RGPD, aucune donnée de conversation n'est accessible."
                )
            }

        # Calcul financier de synthèse
        debt_ratio = calculate_debt_ratio(user.monthly_income, user.monthly_expenses)

        # Récupération des dernières questions posées
        recent_conversations = db.query(ConversationModel).filter(ConversationModel.user_id == user_id).order_by(ConversationModel.updated_at.desc()).limit(3).all()
        topics_explored = [c.title for c in recent_conversations]

        report = {
            "authorized": True,
            "client_name": user.full_name or user.username,
            "client_email": user.email,
            "current_track": user.current_track.upper(),
            "financial_summary": {
                "monthly_income": f"{user.monthly_income:,.2f} €",
                "monthly_expenses": f"{user.monthly_expenses:,.2f} €",
                "debt_ratio": f"{debt_ratio} %",
                "current_balance": f"{user.balance:,.2f} €",
                "savings_balance": f"{user.savings_balance:,.2f} €",
            },
            "topics_discussed_with_ai": topics_explored if topics_explored else ["Prise en main générale de l'application"],
            "suggested_advisor_actions": self._suggest_human_advisor_actions(user.current_track, debt_ratio)
        }
        return report

    def _suggest_human_advisor_actions(self, track: str, debt_ratio: float) -> list:
        actions = []
        if track == "pea":
            actions.append("Proposer un point pédagogique sur la répartition d'actifs et les ETF indiciels.")
        elif track == "projets":
            actions.append("Vérifier si le client a besoin d'une attestation de caution pour son logement.")
        else:
            if debt_ratio > 30:
                actions.append("Proposer une révision des prélèvements récurrents ou des options de mensualisation.")
            else:
                actions.append("Sensibiliser à la mise en place d'une épargne programmée vers un livret rémunéré.")
        return actions


compliance_service_instance = ComplianceService()
