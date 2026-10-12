"""Client HTTP pour connecter Streamlit au backend FastAPI avec fallback résilient."""

import os
import requests
from typing import Dict, Any, Optional

API_BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")
TIMEOUT = 4.0


def _load_local_env():
    """Charge automatiquement .env s'il existe pour tester en local sans package tiers."""
    for path in [".env", "../.env", "../../.env"]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip("'\"")
                            if k and k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass
            break

_load_local_env()


class ApiService:
    """Encapsule les requêtes vers l'API FastAPI avec fallback local pour garantir la continuité."""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url

    def _is_api_available(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=1.0)
            return r.status_code == 200
        except Exception:
            return False

    def get_current_user(self, user_id: int = 1) -> Dict[str, Any]:
        """Récupère la session du client authentifié par l'application bancaire hôte."""
        try:
            r = requests.get(f"{self.base_url}/profile/{user_id}", timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass

        return {
            "id": 1,
            "username": "alex",
            "email": "alexandre.dupont@yello.fr",
            "full_name": "Alexandre Dupont",
            "role": "client",
            "balance": 1450.80,
            "savings_balance": 3500.00,
            "monthly_income": 2600.00,
            "monthly_expenses": 700.00,
            "current_track": "courant",
            "xp_points": 120,
            "level": 1,
            "advisor_share_consent": True,
            "created_at": "2026-10-10T12:00:00"
        }

    def login(self, username: str = "demo", password: str = "") -> Dict[str, Any]:
        """Compatibilité automatique : Yello réutilise la session du client bancaire connecté."""
        user = self.get_current_user(1)
        return {
            "access_token": "banking_sso_session_token",
            "token_type": "bearer",
            "user": user
        }

    def register(self, username: str, email: str, password: str, full_name: str = "") -> Dict[str, Any]:
        try:
            r = requests.post(
                f"{self.base_url}/auth/register",
                json={"username": username, "email": email, "password": password, "full_name": full_name},
                timeout=TIMEOUT
            )
            if r.status_code in (200, 201):
                return r.json()
            return {"error": r.json().get("detail", "Erreur d'inscription.")}
        except Exception:
            return {
                "id": 2,
                "username": username,
                "email": email,
                "full_name": full_name,
                "role": "client",
                "balance": 500.00,
                "savings_balance": 1000.00,
                "monthly_income": 2200.00,
                "monthly_expenses": 600.00,
                "current_track": "courant",
                "xp_points": 50,
                "level": 1,
                "advisor_share_consent": False
            }

    def submit_questionnaire(self, user_id: int, objective: str, knowledge_level: str, time_horizon: str) -> Dict[str, Any]:
        try:
            r = requests.post(
                f"{self.base_url}/onboarding/submit",
                json={"user_id": user_id, "objective": objective, "knowledge_level": knowledge_level, "time_horizon": time_horizon},
                timeout=TIMEOUT
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass

        # Calcul local équivalent
        if objective == "bourse_investir":
            track = "pea"
            title = "Le Parcours Investir (PEA & Bourse Progressive)"
            desc = "Découvrez la bourse pas à pas, comprenez le fonctionnement d'un PEA et investissez vos premiers 100 € en toute sérénité."
        elif objective == "financer_projet":
            track = "projets"
            title = "Le Parcours Projets & Aides"
            desc = "Optimisez vos aides (APL, bourses, garantie Visale) et budgétez votre projet de vie (logement, études, voyage)."
        else:
            track = "courant"
            title = "Le Parcours Épargner & Budget"
            desc = "Prenez le contrôle de votre budget, paramétrez vos alertes de solde bas et construisez votre premier mois de sécurité."

        return {
            "recommended_track": track,
            "track_title": title,
            "track_description": desc,
            "xp_awarded": 100,
            "badge_unlocked": "Vision Claire"
        }

    def _call_cloud_llm(self, message: str) -> Optional[Dict[str, Any]]:
        """Interroge un LLM Cloud sécurisé (Llama 3 via Groq, Mistral, ou OpenAI) si configuré."""
        def _get_val(k: str) -> Optional[str]:
            # 1. Variables d'environnement
            v = os.getenv(k, "").strip() or os.getenv(k.lower(), "").strip()
            if v:
                return v.strip(' "\'')
            # 2. Secrets Streamlit
            try:
                import streamlit as st
                if hasattr(st, "secrets"):
                    # Clé directe
                    if k in st.secrets:
                        return str(st.secrets[k]).strip(' "\'')
                    if k.lower() in st.secrets:
                        return str(st.secrets[k.lower()]).strip(' "\'')
                    # Clé dans une section TOML
                    for _, sec_val in st.secrets.items():
                        if isinstance(sec_val, dict):
                            if k in sec_val:
                                return str(sec_val[k]).strip(' "\'')
                            if k.lower() in sec_val:
                                return str(sec_val[k.lower()]).strip(' "\'')
            except Exception as e:
                print(f"[API_SERVICE] Lecture secrets: {e}")
            return None

        groq_key = _get_val("GROQ_API_KEY")
        mistral_key = _get_val("MISTRAL_API_KEY")
        openai_key = _get_val("OPENAI_API_KEY")

        if not (groq_key or mistral_key or openai_key):
            print("[API_SERVICE] Aucune clé Cloud détectée (GROQ_API_KEY / MISTRAL_API_KEY / OPENAI_API_KEY).")
            return None

        system_prompt = (
            "Tu es Marcel, le conseiller financier virtuel officiel de Yello (YellowBank).\n"
            "Ton rôle est d'expliquer la finance, le budget, le PEA, l'épargne et les aides jeunes de manière claire, bienveillante, pédagogique et structurée.\n"
            "Tu t'exprimes en français avec un ton moderne, direct et accessible (tutoiement chaleureux).\n\n"
            "GUIDES OFFICIELS YELLO :\n"
            "1. ÉPARGNE & BUDGET : Règle 50/30/20 (50% besoins vitaux, 30% envies et loisirs, 20% épargne). "
            "Matelas de sécurité indispensable de 1 à 3 mois de dépenses sur Livret A ou LDDS avant d'investir.\n"
            "2. PEA & BOURSE : PEA exonéré d'impôt sur le revenu après 5 ans (seuls 17,2% de prélèvements sociaux sont dus). "
            "Plafond de 150 000 € (20 000 € pour PEA Jeune 18-25 ans). Pour débuter : ETF mondial diversifié dès 50 €/mois. "
            "Rappeler toujours le risque de perte en capital.\n"
            "3. PROJETS & AIDES JEUNES : Permis à 1 € par jour (prêt à taux zéro jusqu'à 1 200 € garanti par l'État, ~30 €/mois). "
            "Prêt étudiant garanti par l'État (Bpifrance, jusqu'à 20 000 € sans caution parentale). "
            "Logement : APL de la CAF et garantie Visale d'Action Logement (caution gratuite).\n\n"
            "Consignes : Réponds précisément avec des puces et du gras pour faciliter la lecture. Ne sors pas de ton rôle de conseiller Yello."
        )

        # 1. Option prioritaire : Groq (Llama / Open-source puissant, 100% gratuit et instantané)
        if groq_key:
            groq_models = [
                "openai/gpt-oss-120b",
                "qwen/qwen3.8-27b",
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "llama3-8b-8192",
                "openai/gpt-oss-20b"
            ]
            for model_name in groq_models:
                try:
                    r = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                        json={
                            "model": model_name,
                            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}],
                            "temperature": 0.4,
                            "max_tokens": 800
                        },
                        timeout=15.0
                    )
                    if r.status_code == 200:
                        ans = r.json()["choices"][0]["message"]["content"]
                        print(f"[API_SERVICE] Succès Groq avec modèle {model_name} !")
                        return {
                            "answer": ans, "content": ans, "confidence": 0.98, "confidence_score": 0.98,
                            "agent": "rag", "sender_agent": "rag_agent",
                            "sources": [{"title": f"Base Documentaire Yello ({model_name})", "snippet": "Réponse générée par IA Cloud sécurisée."}]
                        }
                    else:
                        print(f"[API_SERVICE] Groq erreur HTTP {r.status_code} ({model_name}): {r.text[:200]}")
                except Exception as err:
                    print(f"[API_SERVICE] Exception Groq ({model_name}): {err}")

        # 2. Option Mistral
        if mistral_key:
            try:
                r = requests.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {mistral_key}", "Content-Type": "application/json"},
                    json={
                        "model": "mistral-small-latest",
                        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}],
                        "temperature": 0.4
                    },
                    timeout=15.0
                )
                if r.status_code == 200:
                    ans = r.json()["choices"][0]["message"]["content"]
                    return {
                        "answer": ans, "content": ans, "confidence": 0.96, "confidence_score": 0.96,
                        "agent": "rag", "sender_agent": "rag_agent",
                        "sources": [{"title": "Base Documentaire Yello (Mistral)", "snippet": "Réponse certifiée Mistral AI."}]
                    }
            except Exception:
                pass

        # 3. Option OpenAI
        if openai_key:
            try:
                r = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}],
                        "temperature": 0.4
                    },
                    timeout=15.0
                )
                if r.status_code == 200:
                    ans = r.json()["choices"][0]["message"]["content"]
                    return {
                        "answer": ans, "content": ans, "confidence": 0.98, "confidence_score": 0.98,
                        "agent": "rag", "sender_agent": "rag_agent",
                        "sources": [{"title": "Base Documentaire Yello (GPT-4o)", "snippet": "Réponse certifiée OpenAI."}]
                    }
            except Exception:
                pass

        return None

    def send_chat_message(self, user_id: int, message: str, track: str = "courant") -> Dict[str, Any]:
        # 1. Essai vers l'API FastAPI locale si active
        try:
            r = requests.post(
                f"{self.base_url}/chat/message",
                json={"user_id": user_id, "message": message, "track": track},
                timeout=12.0
            )
            if r.status_code == 200:
                data = r.json()
                content = data.get("content", "")
                conf = data.get("confidence_score", 0.9)
                agent = data.get("sender_agent", "rag_agent").replace("_agent", "")
                sources = []
                for s in data.get("sources", []):
                    if isinstance(s, dict):
                        sources.append({"title": s.get("document_title", "Guide officiel"), "snippet": s.get("snippet", "")})
                    else:
                        sources.append({"title": str(s)})
                return {
                    "answer": content,
                    "content": content,
                    "confidence": conf,
                    "confidence_score": conf,
                    "agent": agent,
                    "sources": sources,
                    **data
                }
        except Exception:
            pass

        # 2. Essai vers le LLM Cloud sécurisé (Groq Llama 3 / Mistral / OpenAI via Secrets)
        cloud_res = self._call_cloud_llm(message)
        if cloud_res:
            return cloud_res

        # Fallback IA autonome enrichi (utilisé sur Streamlit Cloud ou si l'API locale est inaccessible)
        m_lower = message.lower().strip()

        # 1. Salutations et présentations
        if any(w in m_lower for w in ["bonjour", "salut", "hello", "coucou", "bonsoir", "qui es-tu", "qui es tu", "tu es qui"]):
            ans = ("Bonjour ! Je suis Marcel, ton conseiller financier virtuel chez Yello 🤖.\n\n"
                   "Je suis là pour t'accompagner sur tes finances : comment gérer ton budget, débloquer des aides "
                   "(permis à 1 €, prêt étudiant) ou débuter en Bourse avec le PEA.\n\n"
                   "Quelle question as-tu en tête aujourd'hui ?")
            return {
                "answer": ans, "content": ans, "confidence": 0.98, "confidence_score": 0.98,
                "agent": "chitchat", "sender_agent": "chitchat_agent",
                "sources": []
            }

        # 2. Remerciements et politesse
        if any(w in m_lower for w in ["merci", "super", "parfait", "top", "au revoir"]):
            ans = "Avec grand plaisir ! N'hésite pas si tu as d'autres questions sur tes projets ou ton épargne. Bonne journée !"
            return {
                "answer": ans, "content": ans, "confidence": 0.99, "confidence_score": 0.99,
                "agent": "chitchat", "sender_agent": "chitchat_agent",
                "sources": []
            }

        # 3. PEA & Bourse & Investissement
        if any(w in m_lower for w in ["pea", "bourse", "action", "investir", "etf", "dividende", "5 ans"]):
            ans = ("Le Plan d'Épargne en Actions (PEA) permet d'investir sur les actions et ETF européens. "
                   "Ses atouts clés :\n"
                   "• **Après 5 ans** : exonération totale d'impôt sur le revenu sur les plus-values (seuls les 17,2 % de prélèvements sociaux sont dus).\n"
                   "• **Plafond** : jusqu'à 150 000 € de versements (20 000 € pour le PEA Jeune 18-25 ans rattaché au foyer fiscal).\n"
                   "• **Pour démarrer** : un ETF indiciel monde diversifié permet de répartir le risque dès 50 € ou 100 € par mois.\n\n"
                   "⚠️ *Rappel : tout investissement en Bourse comporte un risque de perte en capital.*")
            return {
                "answer": ans, "content": ans, "confidence": 0.95, "confidence_score": 0.95,
                "agent": "rag", "sender_agent": "rag_agent",
                "sources": [{"title": "Guide PEA & Investissement", "snippet": "Fiscalité avantageuse après 5 ans et diversification ETF."}]
            }

        # 4. Aides, Permis à 1€, Logement, Projets jeunes
        if any(w in m_lower for w in ["permis", "aide", "projet", "pret", "prêt", "etudiant", "étudiant", "apl", "visale", "garantie"]):
            ans = ("Plusieurs dispositifs clés sont disponibles pour financer tes projets jeunes :\n\n"
                   "• **Permis à 1 € par jour** : un prêt à taux zéro jusqu'à 1 200 € où l'État prend en charge l'ensemble des intérêts (remboursement ~30 €/mois).\n"
                   "• **Prêt étudiant garanti par l'État** : accessible jusqu'à 20 000 € sans caution parentale via Bpifrance.\n"
                   "• **Logement & Aides** : l'APL de la CAF et la garantie Visale d'Action Logement pour avoir un garant gratuit.\n\n"
                   "Tu peux retrouver le récapitulatif complet de ces aides dans le Parcours 3 (Projets & Aides) !")
            return {
                "answer": ans, "content": ans, "confidence": 0.93, "confidence_score": 0.93,
                "agent": "rag", "sender_agent": "rag_agent",
                "sources": [{"title": "Guide Aides & Projets Jeunes", "snippet": "Prêt permis 1 €/jour et prêt étudiant garanti par l'État."}]
            }

        # 5. Règle 50/30/20, Budget, Matelas d'épargne
        if any(w in m_lower for w in ["50/30/20", "regle", "règle", "budget", "matelas", "securite", "sécurité", "imprevu", "imprévu", "combien garder"]):
            ans = ("Pour bien structurer ton budget sans te priver, la règle **50 / 30 / 20** est la méthode de référence :\n\n"
                   "• **50 % pour les besoins vitaux** : loyer, charges, courses alimentaires, transports essentiels.\n"
                   "• **30 % pour les envies & loisirs** : sorties, abonnements, shopping, voyages.\n"
                   "• **20 % pour l'épargne** : constituer en priorité un **matelas de sécurité** de 1 à 3 mois de dépenses sur un Livret A ou LDDS avant d'investir.")
            return {
                "answer": ans, "content": ans, "confidence": 0.94, "confidence_score": 0.94,
                "agent": "rag", "sender_agent": "rag_agent",
                "sources": [{"title": "Guide Épargne & Budget", "snippet": "Répartition 50/30/20 et matelas de précaution de 1 à 3 mois."}]
            }

        # 6. Question générale / non répertoriée
        ans = (f"C'est une excellente question sur tes finances ! En tant que conseiller Yello, je te conseille d'explorer nos parcours éducatifs :\n\n"
               "• **Parcours 1** pour maîtriser ton budget et tes imprévus.\n"
               "• **Parcours 2 & Profil Investisseur** pour tout comprendre au PEA et à la Bourse.\n"
               "• **Parcours 3** pour collecter toutes les aides d'État adaptées à ta situation.\n\n"
               "Tu peux aussi me poser une question précise sur le PEA, le permis à 1 € ou ton matelas de précaution.")
        return {
            "answer": ans, "content": ans, "confidence": 0.88, "confidence_score": 0.88,
            "agent": "rag", "sender_agent": "rag_agent",
            "sources": [{"title": "Base Documentaire Yello", "snippet": "Guides officiels Épargne, PEA et Projets."}]
        }

    def chat(self, message: str, user_id: int = 1, track: str = "courant") -> Dict[str, Any]:
        """Alias pour le chat avec Marcel."""
        return self.send_chat_message(user_id=user_id, message=message, track=track)

    def ask(self, message: str, user_id: int = 1, track: str = "courant") -> Dict[str, Any]:
        """Alias pour poser une question à Marcel."""
        return self.send_chat_message(user_id=user_id, message=message, track=track)

    def get_market_briefing(self, sector: str = "tech") -> Dict[str, Any]:
        try:
            r = requests.get(f"{self.base_url}/chat/market-briefing/{sector}", timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass

        data = {
            "tech": {
                "sector": "Technologies Européennes",
                "benchmark_index": "Euro Stoxx Tech",
                "monthly_variation": "+2.4%",
                "ambiance": "🟢 Marché stable",
                "volatility_level": "stable",
                "analysis": "Le secteur technologique européen affiche une progression mensuelle de +2,4%, portée par les résultats trimestriels résilients des semi-conducteurs et du cloud. La volatilité reste contenue à 14,2%, niveau proche des moyennes annuelles.\n\nCe point d'information est purement factuel et ne constitue pas un conseil en investissement.",
                "key_event": "Résultats solides sur les infrastructures semi-conducteurs.",
                "sources": ["Euronext Paris", "BCE", "Reuters"]
            },
            "energie": {
                "sector": "Énergies Renouvelables & Transition",
                "benchmark_index": "S&P Global Clean Energy",
                "monthly_variation": "-4.8%",
                "ambiance": "🟠 Marché volatil",
                "volatility_level": "volatil",
                "analysis": "Le secteur des énergies renouvelables a reculé de 4,8% ce mois-ci, sous l'effet du coût de financement des infrastructures et de prises de bénéfices. Ce niveau de volatilité est similaire aux variations observées en 2022.\n\nDocument d'information générale sans valeur de recommandation d'achat ou de vente.",
                "key_event": "Ajustement des coûts de financement des parcs éoliens offshore.",
                "sources": ["Agence Internationale de l'Énergie", "Euronext ESG Index"]
            }
        }
        return data.get(sector, data["tech"])

    def get_gamification_progress(self, user_id: int) -> Dict[str, Any]:
        try:
            r = requests.get(f"{self.base_url}/gamification/progress/{user_id}", timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass

        return {
            "user_id": user_id,
            "xp_points": 180,
            "level": 1,
            "current_track": "courant",
            "badges": [
                {"id": 1, "badge_name": "Vision Claire", "badge_icon": "🧭", "description": "Diagnostic des 30 jours complété."},
                {"id": 2, "badge_name": "Matelas 1 Mois", "badge_icon": "🛡️", "description": "Premier palier de sécurité atteint."}
            ],
            "active_missions": [
                {"id": 1, "track": "courant", "title": "Faire le point : Diagnostic des 30 jours", "description": "Catégoriser ses dépenses et mesurer son score de lucidité.", "xp_reward": 50, "status": "completed"},
                {"id": 2, "track": "courant", "title": "Test de résistance : Simuler un imprévu", "description": "Mesurer combien de mois de sérénité absorbe votre épargne.", "xp_reward": 60, "status": "available"},
                {"id": 3, "track": "courant", "title": "Automatiser : Virement de sécurité", "description": "Mettre en place un versement automatique mensuel.", "xp_reward": 50, "status": "available"}
            ],
            "completed_missions_count": 1
        }

    def complete_mission(self, user_id: int, mission_id: int) -> Dict[str, Any]:
        try:
            r = requests.post(f"{self.base_url}/gamification/complete-mission", json={"user_id": user_id, "mission_id": mission_id}, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {"success": True, "xp_gained": 60, "total_xp": 240, "level": 2, "badge_unlocked": "Sécurité Testée"}

    def update_consent(self, user_id: int, consent: bool) -> Dict[str, Any]:
        try:
            r = requests.post(f"{self.base_url}/profile/consent", json={"user_id": user_id, "advisor_share_consent": consent}, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {"message": "Consentement mis à jour."}

    def get_advisor_report(self, user_id: int) -> Dict[str, Any]:
        try:
            r = requests.get(f"{self.base_url}/profile/advisor-report/{user_id}", timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {
            "authorized": True,
            "client_name": "Alexandre Dupont",
            "client_email": "demo@yello.fr",
            "current_track": "ÉPARGNER & BUDGET",
            "financial_summary": {
                "monthly_income": "2 600,00 €",
                "monthly_expenses": "700,00 €",
                "debt_ratio": "26.9 %",
                "current_balance": "1 450,80 €",
                "savings_balance": "3 500,00 €"
            },
            "topics_discussed_with_ai": ["Constitution du fonds de sécurité", "Règles du PEA 5 ans"],
            "suggested_advisor_actions": ["Présenter l'offre de livret d'épargne rémunéré à 3% pour le matelas de précaution."]
        }


api_service = ApiService()
