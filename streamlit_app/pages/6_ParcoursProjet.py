"""Parcours 3 : Projets & Aides — Yellow."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Parcours 3 : Projets & Aides — Yellow", page_icon="🎓", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title("🎓 Parcours 3 : Projets & Aides Financières")
st.write("Mobilisez vos droits publics et les avantages bancaires exclusifs YellowBank.")

st.divider()

st.subheader("🎁 Vos Avantages & Dispositifs à Débloquer")

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="mission-card">
        <h4 style="color: white;">🎓 Prêt Étudiant Garanti par l'État</h4>
        <p style="font-size:13px; color:#94A3B8;">Empruntez sans caution personnelle ni garant familial via la garantie d'État.</p>
        <span class="badge-pill">Taux préférentiel</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mission-card">
        <h4 style="color: white;">🚗 Prêt Permis de Conduire (1 € / jour)</h4>
        <p style="font-size:13px; color:#94A3B8;">Financez votre permis B avec prise en charge des intérêts par l'État.</p>
        <span class="badge-pill">0 % intérêt</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="mission-card">
        <h4 style="color: white;">🎁 Prime de Bienvenue & Mobilité</h4>
        <p style="font-size:13px; color:#94A3B8;">Jusqu'à 150 € offerts pour la première ouverture et le transfert automatique.</p>
        <span class="badge-pill">Prime cash</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mission-card">
        <h4 style="color: white;">✈️ Frais Réduits à l'Étranger</h4>
        <p style="font-size:13px; color:#94A3B8;">Paiements et retraits sans commission de change lors de vos stages et séjours.</p>
        <span class="badge-pill">0 € commission</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

if st.button("🏆 Valider mon Bilan d'Aides & Obtenir le Badge", type="primary", use_container_width=True):
    user["xp_points"] = user.get("xp_points", 120) + 100
    user["projets_level"] = max(user.get("projets_level", 0), 1)
    st.session_state["user"] = user
    st.balloons()
    st.success("🎉 **Badge Débloqué : Chasseur d'Aides !** (+100 XP attribués)")

st.divider()

col_nav = st.columns([1, 2, 1])
with col_nav[1]:
    st.page_link("pages/7_Dashboard.py", label="Retour au Dashboard & Mes Badges 📊", icon="📊")
