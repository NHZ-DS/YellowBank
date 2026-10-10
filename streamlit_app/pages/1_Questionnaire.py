"""Page de Questionnaire d'Orientation — Yellow."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="1. Questionnaire — Yellow", page_icon="📋", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title("📋 Questionnaire d'Orientation & Profiling")
st.write("Personnalisez votre expérience en 3 étapes rapides. Vos choix détermineront les jeux et badges débloquables.")

st.divider()

with st.form("funnel_quiz"):
    st.subheader("1. Quelle est votre tranche d'âge ?")
    age_group = st.radio(
        "Choisissez votre profil :",
        [
            "18 - 21 ans (Étudiant / Début de cursus)",
            "22 - 25 ans (Jeune diplômé / Premier emploi)",
            "26 - 30 ans (Jeune actif autonome)",
            "+30 ans (Actif expérimenté)"
        ],
        index=1
    )

    st.subheader("2. Quels sont vos centres d'intérêt prioritaires ? (Sélection multiple)")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        c_budget = st.checkbox("🛡️ Budget, épargne d'urgence et maîtrise des charges", value=True)
        c_pea = st.checkbox(" Bourse, PEA et investissement progressif", value=True)
    with col_i2:
        c_projets = st.checkbox(" Financement de projet (Permis 1€/jour, études, logement)", value=False)
        c_aides = st.checkbox(" Primes bancaires (bienvenue, mobilité) & Aides d'État", value=True)

    st.subheader("3. Quel est votre objectif principal du moment ?")
    objective = st.radio(
        "Sélectionnez votre parcours prioritaire :",
        [
            ("courant", "🛡️ ÉPARGNER : Maîtriser mon budget et sécuriser mon matelas de sécurité"),
            ("pea", " INVESTIR : Découvrir les 6 niveaux du PEA et la bourse sans risque"),
            ("projets", " FINANCER UN PROJET : Mobiliser mes aides, prêts à 0% et primes")
        ],
        format_func=lambda x: x[1]
    )

    submit = st.form_submit_button("Valider mes réponses & Découvrir ma situation", type="primary", use_container_width=True)

if submit:
    # Sauvegarde dans la session et appel API
    user["age_group"] = age_group
    user["current_track"] = objective[0]
    st.session_state["user"] = user

    res = api_service.submit_questionnaire(
        user_id=user.get("id", 1),
        objective=objective[0],
        knowledge_level="intermediaire",
        time_horizon="moyen_terme"
    )

    st.success(" Vos réponses ont été enregistrées avec succès !")
    st.page_link("pages/2_Situation.py", label="Accéder à ma Situation Visuelle", icon="")
