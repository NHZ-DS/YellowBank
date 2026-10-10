"""Questionnaire d'Entrée & Calibrage du Parcours — Yellow."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Questionnaire d'Entrée — Yellow", page_icon="📋", layout="wide")

with open("static/css/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "user" not in st.session_state:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title("📋 Questionnaire de Calibrage")
st.write("3 questions simples pour définir le parcours qui répond à votre priorité actuelle. Vous pourrez en changer à tout moment.")

st.divider()

with st.form("onboarding_form"):
    st.subheader("1. Quel est votre objectif prioritaire ?")
    objectif = st.radio(
        "Sélectionnez votre axe principal :",
        [
            ("gerer_budget", "🛡️ Épargner & Maîtriser mon budget au quotidien"),
            ("bourse_investir", "📈 Investir & Découvrir la bourse progressivement"),
            ("financer_projet", "🎓 Financer un projet (logement, études, aides & permis)")
        ],
        format_func=lambda x: x[1]
    )

    st.subheader("2. Votre degré d'aisance avec les concepts financiers")
    niveau = st.select_slider(
        "Niveau d'expérience :",
        options=["Débutant (je pars de zéro)", "Intermédiaire (j'ai déjà une épargne)", "Avancé (je connais les supports)"],
        value="Intermédiaire (j'ai déjà une épargne)"
    )

    st.subheader("3. Votre horizon de temps")
    horizon = st.radio(
        "Pour vos projets, sur quelle durée vous projetez-vous ?",
        [
            ("court_terme", "Court terme (moins d'un an, besoin de liquidités)"),
            ("moyen_terme", "Moyen terme (1 à 5 ans, préparer un apport ou projet)"),
            ("long_terme", "Long terme (plus de 5 ans, constitution de patrimoine)")
        ],
        format_func=lambda x: x[1]
    )

    submit_btn = st.form_submit_button("Valider mon Profil & Obtenir mon Parcours", type="primary", use_container_width=True)

if submit_btn:
    # Correspondance technique
    obj_key = objectif[0]
    lvl_key = "debutant" if "Débutant" in niveau else ("avance" if "Avancé" in niveau else "intermediaire")
    hor_key = horizon[0]

    with st.spinner("Analyse de votre profil en cours..."):
        res = api_service.submit_questionnaire(
            user_id=user.get("id", 1),
            objective=obj_key,
            knowledge_level=lvl_key,
            time_horizon=hor_key
        )

    # Mise à jour session
    user["current_track"] = res.get("recommended_track", "courant")
    user["xp_points"] = user.get("xp_points", 120) + res.get("xp_awarded", 100)
    st.session_state["user"] = user

    st.success(f"🎯 **Parcours Recommandé : {res.get('track_title')}**")
    st.info(f"💡 {res.get('track_description')}")
    st.write(f"🏅 Premier jalon débloqué : **{res.get('badge_unlocked')}** (+100 XP)")

    c_go1, c_go2 = st.columns(2)
    with c_go1:
        st.page_link("Dashboard.py", label="Accéder au Tableau de Bord", icon="📊")
    with c_go2:
        st.page_link("Chat.py", label="Poser une question au Marcel", icon="💬")
