"""Agent IA de Veille Marché : Information factuelle, analyse de volatilité et indicateur d'ambiance."""

from typing import Dict, Any, List
from services.chat_service.llm_service import llm_service_instance

MARKET_DATA = {
    "tech": {
        "sector_name": "Technologies Européennes",
        "benchmark_index": "Euro Stoxx Tech",
        "monthly_variation": "+2.4%",
        "volatility_status": "🟢 Marché stable",
        "volatility_level": "stable",
        "volatility_explanation": "Volatilité modérée (14,2%), dans la moyenne historique des 12 derniers mois.",
        "key_event": "Publication des résultats trimestriels des semi-conducteurs et résilience de la demande en infrastructures cloud.",
        "sources": ["Euronext Paris", "BCE (Bulletin économique)", "Reuters Finance"]
    },
    "energie": {
        "sector_name": "Énergies Renouvelables & Transition",
        "benchmark_index": "S&P Global Clean Energy",
        "monthly_variation": "-4.8%",
        "volatility_status": "🟠 Marché volatil",
        "volatility_level": "volatil",
        "volatility_explanation": "Volatilité accrue liée aux variations des taux d'intérêt et au coût des financements d'infrastructures.",
        "key_event": "Ajustement des valorisations sur les parcs éoliens offshore et consolidation des acteurs du solaire européen.",
        "sources": ["Agence Internationale de l'Énergie (AIE)", "Euronext ESG Index", "Financial Times"]
    },
    "immobilier": {
        "sector_name": "Immobilier Européen & SCPI",
        "benchmark_index": "FTSE EPRA Nareit Europe",
        "monthly_variation": "+0.8%",
        "volatility_status": "🟢 Marché stable",
        "volatility_level": "stable",
        "volatility_explanation": "Stabilisation progressive des valeurs d'expertise après la fin du cycle de hausse des taux directeurs.",
        "key_event": "Reprise progressive des volumes de transactions sur le résidentiel et logistique prime.",
        "sources": ["Banque de France", "Notaires de France", "IEIF"]
    }
}


class MarketAgent:
    """Produit un point de veille de marché factuel sans incitation ni conseil d'achat."""

    def get_briefing(self, sector_key: str = "tech") -> Dict[str, Any]:
        data = MARKET_DATA.get(sector_key, MARKET_DATA["tech"])

        system_prompt = (
            "Tu es l'analyste de veille financière d'Archipel (YellowBank). "
            "RÈGLES DÉONTOLOGIQUES ET RÉGLEMENTAIRES STRICTES (MIFID II) :\n"
            "1. Ton rôle est EXCLUSIVEMENT d'informer et d'expliquer les faits de marché avec un ton adulte, neutre et professionnel.\n"
            "2. INTERDICTION ABSOLUE : N'utilise jamais de phrases incitatives comme 'c'est le moment d'acheter', 'ne ratez pas cette occasion', ou de prévisions de cours.\n"
            "3. Rédige un point de situation en 2 courts paragraphes : résume la variation et l'événement clé avec pédagogie.\n"
            "4. Termine obligatoirement par la mention réglementaire : 'Document d'information générale sans valeur de conseil personnalisé. Tout investissement comporte un risque de perte en capital.'\n"
        )

        user_content = (
            f"Secteur : {data['sector_name']}\n"
            f"Indice : {data['benchmark_index']}\n"
            f"Variation mensuelle : {data['monthly_variation']}\n"
            f"Ambiance : {data['volatility_status']}\n"
            f"Contexte : {data['key_event']}"
        )

        analysis_text = llm_service_instance.generate_response([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ], temperature=0.2)

        return {
            "sector": data["sector_name"],
            "benchmark_index": data["benchmark_index"],
            "monthly_variation": data["monthly_variation"],
            "ambiance": data["volatility_status"],
            "volatility_level": data["volatility_level"],
            "analysis": analysis_text,
            "key_event": data["key_event"],
            "sources": data["sources"],
            "disclaimer": "Information générale et factuelle (MiFID II). Ne constitue pas un conseil en investissement."
        }


market_agent_instance = MarketAgent()
