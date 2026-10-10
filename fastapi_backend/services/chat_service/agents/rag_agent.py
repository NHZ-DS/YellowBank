"""Agent RAG (Retrieval-Augmented Generation) pour les réponses bancaires certifiées."""

from typing import Dict, Any, List
from data.knowledge_base import knowledge_base_instance
from services.chat_service.llm_service import llm_service_instance
from models.message import SourceCitation, ActionSuggestion


class RAGAgent:
    """Agent expert qui recherche dans la base documentaire et répond avec citations et confiance."""

    def process(self, query: str, track: str = "courant") -> Dict[str, Any]:
        # 1. Recherche des fragments documentaires pertinents
        search_results = knowledge_base_instance.search(query, top_k=2)
        
        # 2. Calcul du score de confiance
        if search_results and search_results[0]["score"] >= 0.5:
            confidence_score = search_results[0]["score"]
        else:
            confidence_score = 0.55  # Score bas si peu de certitude documentaire

        # 3. Préparation du contexte documentaire pour le LLM
        context_text = "\n\n".join([f"Source: {res['document_title']}\n{res['full_text']}" for res in search_results])

        system_prompt = (
            "Tu es le Conseiller Bancaire IA officiel d'Archipel (YellowBank). "
            "RÈGLES IMPÉRATIVES DE SÉCURITÉ ET DÉONTOLOGIE :\n"
            "1. Réponds de façon précise, pédagogique et bienveillante en t'appuyant STRICTEMENT sur le contexte documentaire ci-dessous.\n"
            "2. 'L'agent conseille, le client décide' : Ne valide jamais d'opération à la place du client. Propose-lui la démarche à suivre.\n"
            "3. Si la question concerne la bourse ou le PEA, rappelle brièvement le risque de perte en capital.\n"
            "4. Sois concis (2 à 3 paragraphes maximum).\n\n"
            f"CONTEXTE DOCUMENTAIRE OFFICIEL :\n{context_text}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        # 4. Génération de la réponse via OpenAI
        answer_text = llm_service_instance.generate_response(messages)

        # 5. Construction des citations
        citations = [
            SourceCitation(
                document_title=res["document_title"],
                snippet=res["snippet"],
                relevance_score=res["score"]
            )
            for res in search_results
        ]

        # 6. Suggestions d'actions adaptées
        suggested_actions = []
        q_lower = query.lower()
        if "pea" in q_lower or "invest" in q_lower or "bourse" in q_lower:
            suggested_actions.append(ActionSuggestion(action_type="OPEN_PEA", label="🚀 Ouvrir mon PEA en 3 clics"))
        elif "alerte" in q_lower or "solde" in q_lower:
            suggested_actions.append(ActionSuggestion(action_type="SET_ALERT", label="🔔 Configurer mon alerte solde bas"))
        elif "apl" in q_lower or "logement" in q_lower:
            suggested_actions.append(ActionSuggestion(action_type="ESTIMATE_APL", label="🏠 Simuler mes droits APL"))

        return {
            "content": answer_text,
            "confidence_score": confidence_score,
            "sources": citations,
            "suggested_actions": suggested_actions,
            "risk_level": "moyen" if "pea" in q_lower else "faible"
        }


rag_agent_instance = RAGAgent()
