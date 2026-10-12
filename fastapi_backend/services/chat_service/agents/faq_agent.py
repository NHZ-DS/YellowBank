"""Agent FAQ pour les réponses instantanées aux questions récurrentes sans coût de tokens."""

from typing import Dict, Any, Optional
from models.message import ActionSuggestion


FAQ_DATABASE = {
    "rib": {
        "keywords": ["rib", "iban", "coordonnees bancaires"],
        "answer": (
            "Vous pouvez télécharger votre Relevé d'Identité Bancaire (RIB) au format PDF directement "
            "depuis votre espace dans l'onglet Profil > 'Télécharger mon RIB', ou copier votre IBAN en 1 clic."
        ),
        "action": ActionSuggestion(action_type="GET_RIB", label="📥 Télécharger mon RIB")
    },
    "decouvert": {
        "keywords": ["decouvert", "agios", "autorise"],
        "answer": (
            "L'autorisation de découvert par défaut chez Yello est de 500 € au taux de 7,50 % par an. "
            "Vous pouvez demander l'augmentation de votre découvert autorisé dans Profil > Paramètres du compte."
        ),
        "action": ActionSuggestion(action_type="OVERDRAFT", label="⚙️ Gérer mon découvert")
    }
}


class FAQAgent:
    """Agent FAQ spécialisé dans la détection des questions courantes."""

    def can_handle(self, query: str) -> bool:
        q_lower = query.lower()
        for item in FAQ_DATABASE.values():
            if any(k in q_lower for k in item["keywords"]):
                return True
        return False

    def process(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()
        for item in FAQ_DATABASE.values():
            if any(k in q_lower for k in item["keywords"]):
                return {
                    "content": item["answer"],
                    "confidence_score": 1.0,  # 100% de certitude
                    "sources": [],
                    "suggested_actions": [item["action"]] if item.get("action") else [],
                    "risk_level": "faible"
                }
        
        return {
            "content": "Je n'ai pas trouvé de réponse directe dans la FAQ.",
            "confidence_score": 0.0,
            "sources": [],
            "suggested_actions": [],
            "risk_level": "faible"
        }


faq_agent_instance = FAQAgent()
