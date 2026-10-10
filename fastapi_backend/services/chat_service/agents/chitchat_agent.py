"""Agent Chitchat pour les échanges conversationnels, l'accueil et la motivation."""

from typing import Dict, Any
from services.chat_service.llm_service import llm_service_instance
from models.message import ActionSuggestion


class ChitchatAgent:
    """Gère l'accueil chaleureux, les félicitations et les questions sur le jeu Archipel."""

    def process(self, query: str, track: str = "courant") -> Dict[str, Any]:
        system_prompt = (
            "Tu es le compagnon de bord virtuel sur l'île d'Archipel (YellowBank). "
            "Ton ton est dynamique, encourageant, moderne et bienveillant, parfaitement adapté à un jeune adulte. "
            "Tu expliques que l'application permet de naviguer à travers 3 grands parcours : "
            "1. Le Parcours Courant (gérer son argent au quotidien), "
            "2. Le Parcours PEA (investir en bourse progressivement), "
            "3. Le Parcours Projets & Aides (trouver des aides comme l'APL ou financer ses projets). "
            "Tu encourages l'utilisateur à relever des défis pour débloquer des badges ! "
            "Reste court et enthousiaste (1 à 2 courts paragraphes maximum)."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        answer_text = llm_service_instance.generate_response(messages)

        return {
            "content": answer_text,
            "confidence_score": 0.95,
            "sources": [],
            "suggested_actions": [
                ActionSuggestion(action_type="VIEW_MISSIONS", label="🏆 Voir mes missions de l'île")
            ],
            "risk_level": "faible"
        }


chitchat_agent_instance = ChitchatAgent()
