"""Page de Sélection de Parcours — Archipel."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="3. Sélection de Parcours — Archipel", page_icon=":material/explore:", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title(":material/explore: Choisissez votre Parcours d'Évolution")
st.write("Chaque parcours est découpé en étapes sous forme de mini-jeux. Choisissez votre priorité :")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="mission-card">
        <h3>:material/shield: Parcours 1 : Épargner & Budget</h3>
        <p style="font-size:14px; color:#94A3B8;">
            Faites le point sur vos dépenses, simulez des chocs d'imprévus et construisez votre matelas de sécurité.
        </p>
        <span class="badge-pill">Jalon : Matelas 1 mois</span>
    </div>
    """, unsafe_allow_html=True)
    st.write(" ")
    if st.button("Commencer le Parcours 1", icon=":material/rocket_launch:", key="start_p1", use_container_width=True, type="primary"):
        user["current_track"] = "courant"
        st.session_state["user"] = user
        st.switch_page("pages/4_ParcoursCourant.py")

with col2:
    st.markdown("""
    <div class="mission-card">
        <h3>:material/trending_up: Parcours 2 : Investir & PEA</h3>
        <p style="font-size:14px; color:#94A3B8;">
            Découvrez la bourse en 6 niveaux progressifs, testez 10 000 € virtuels et maîtrisez la fiscalité du PEA.
        </p>
        <span class="badge-pill">Jalon : Investisseur Éclairé</span>
    </div>
    """, unsafe_allow_html=True)
    st.write(" ")
    if st.button("Commencer le Parcours 2", icon=":material/rocket_launch:", key="start_p2", use_container_width=True, type="primary"):
        user["current_track"] = "pea"
        st.session_state["user"] = user
        st.switch_page("pages/5_ParcoursPEA.py")

with col3:
    st.markdown("""
    <div class="mission-card">
        <h3>:material/school: Parcours 3 : Projets & Aides</h3>
        <p style="font-size:14px; color:#94A3B8;">
            Mobilisez vos droits d'État (APL, Visale, Bourses), simulez le permis à 1€/jour et profitez des primes bancaires.
        </p>
        <span class="badge-pill">Jalon : Chasseur d'Aides</span>
    </div>
    """, unsafe_allow_html=True)
    st.write(" ")
    if st.button("Commencer le Parcours 3", icon=":material/rocket_launch:", key="start_p3", use_container_width=True, type="primary"):
        user["current_track"] = "projets"
        st.session_state["user"] = user
        st.switch_page("pages/6_ParcoursProjet.py")

st.divider()
st.page_link("pages/7_Dashboard.py", label="Voir mon Tableau de Bord global", icon=":material/dashboard:")
