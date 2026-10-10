"""Accueil de l'application Yellow (YellowBank) — Expérience Financière Ludique & Interactive."""

import streamlit as st
from services.api_service import api_service

# Configuration de la page
st.set_page_config(
    page_title="Yellow — Accueil Ludique",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# Session state initialization
if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

# En-tête Hero
st.markdown("""
<div class="archipel-hero">
    <div class="archipel-title">Bienvenue sur Yellow — Your Financial Adventure</div>
    <div class="archipel-subtitle">La première application bancaire ludique qui transforme la gestion d'argent en un jeu de stratégie et d'apprentissage sans pression.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🧭 Pourquoi choisir Yellow ?")
st.write("Finis les formulaires administratifs austères ! Yellow vous accompagne de manière **ludique, visuelle et gratifiante** pour maîtriser votre budget et faire vos premiers pas en bourse.")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="mission-card">
        <h3 style="margin-top:0; color:white;"> 1. Calibrage sur Mesure</h3>
        <p style="font-size:14px; color:#94A3B8;">Répondez à un court questionnaire pour définir votre tranche d'âge, vos centres d'intérêt et votre profil de risque.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="mission-card">
        <h3 style="margin-top:0; color:white;"> 2. Situation Visuelle</h3>
        <p style="font-size:14px; color:#94A3B8;">Visualisez votre jauge de sérénité, votre avatar progressif et l'évolution de votre patrimoine sur graphique.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="mission-card">
        <h3 style="margin-top:0; color:white;"> 3. Missions & Badges</h3>
        <p style="font-size:14px; color:#94A3B8;">Réalisez des mini-jeux à chaque étape de votre parcours pour gagner des points d'expérience (XP) et des badges.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Bouton Suivant vers le Questionnaire
col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    st.write("#### Prêt(e) à commencer votre aventure ?")
    st.page_link("pages/1_Questionnaire.py", label="Lancer le Questionnaire d'Orientation", icon="")
