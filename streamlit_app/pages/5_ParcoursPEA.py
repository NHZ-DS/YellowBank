"""Parcours 2 : PEA & Investissement (6 Niveaux) — Yellow."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Parcours 2 : Investir & PEA — Yellow", page_icon="📈", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title("📈 Parcours 2 : Investir & Découvrir le PEA")
st.write("Progression en 6 niveaux pédagogiques sans incitation au risque.")

st.divider()

# Onglets des 6 Niveaux
t1, t2, t3, t4, t5, t6 = st.tabs([
    "🟢 Niv. 1 : Explorateur",
    "🔵 Niv. 2 : Stratège",
    "🟣 Niv. 3 : Gestionnaire",
    "🟡 Niv. 4 : Virtuel 10k€",
    "🟠 Niv. 5 : Ouverture PEA",
    "👑 Niv. 6 : Yellow Master"
])

with t1:
    st.markdown("### 🟢 Niveau 1 — L'Explorateur : Découvrir l'investissement")
    st.write("**Objectif :** Démystifier les marchés financiers et comprendre les mécanismes fondamentaux via de courtes leçons (2 à 3 min).")
    st.info("🎖️ **Badge à débloquer :** `Premiers pas en Bourse`")
    if st.button("🎮 Valider le Niveau 1", key="btn_n1", type="primary"):
        user["xp_points"] = user.get("xp_points", 120) + 50
        user["pea_level"] = max(user.get("pea_level", 0), 1)
        st.session_state["user"] = user
        st.balloons()
        st.success("🎉 **Badge Débloqué : Premiers pas en Bourse !** (+50 XP)")

with t2:
    st.markdown("### 🔵 Niveau 2 — Le Stratège : Comprendre avant d'agir")
    st.write("**Objectif :** Découvrir le PEA, la fiscalité avantageuse après 5 ans, la différence entre une action et un ETF, et l'importance de la diversification.")
    st.write("• Qu'est-ce qu'un PEA ?\n• Pourquoi son cadre fiscal est-il intéressant à long terme ?\n• Action vs ETF & Diversification.")
    if st.button("🎮 Valider le Niveau 2", key="btn_n2", type="primary"):
        user["xp_points"] = user.get("xp_points", 120) + 60
        user["pea_level"] = max(user.get("pea_level", 0), 2)
        st.session_state["user"] = user
        st.balloons()
        st.success("🎉 **Badge Débloqué : Investisseur Éclairé !** (+60 XP)")

with t3:
    st.markdown("### 🟣 Niveau 3 — Le Gestionnaire : Se préparer financièrement")
    st.write("**Objectif :** Diagnostiquer sa situation personnelle (budget, capacité d'épargne, matelas de précaution).")
    st.write("Conformément aux préconisations AMF, préserver son épargne de sécurité est récompensé au même titre que l'investissement.")
    if st.button("🎮 Valider le Niveau 3", key="btn_n3", type="primary"):
        user["xp_points"] = user.get("xp_points", 120) + 60
        user["pea_level"] = max(user.get("pea_level", 0), 3)
        st.session_state["user"] = user
        st.balloons()
        st.success("🎉 **Badge Débloqué : Investisseur Éclairé !** (+60 XP)")

with t4:
    st.markdown("### 🟡 Niveau 4 — L'Investisseur Virtuel : Apprendre sans risque réel")
    st.write("**Objectif :** Manipuler un portefeuille fictif de 10 000 € virtuels.")

    alloc = st.slider("% d'ETF Monde diversifié (Actions)", 0, 100, 70)
    st.metric("Valeur simulée à 1 an", f"{10000 + alloc * 15:,.2f} €", delta=f"+{alloc * 15} € (Simulé)")

    if st.button("🎮 Valider le Niveau 4", key="btn_n4", type="primary"):
        user["xp_points"] = user.get("xp_points", 120) + 100
        user["pea_level"] = max(user.get("pea_level", 0), 4)
        st.session_state["user"] = user
        st.balloons()
        st.success("🎉 **Badge Débloqué : Sang-froid Financier !** (+100 XP)")

with t5:
    st.markdown("### 🟠 Niveau 5 — L'Investisseur Autonome : Comprendre l'ouverture du PEA")
    st.write("**Objectif :** Validation des prérequis d'ouverture du PEA (éligibilité, documents, frais, questionnaire MiFID II).")
    st.caption("Plafond classique : 150 000 € | Plafond PEA Jeune : 20 000 €.")
    if st.button("🎮 Valider le Niveau 5", key="btn_n5", type="primary"):
        user["xp_points"] = user.get("xp_points", 120) + 80
        user["pea_level"] = max(user.get("pea_level", 0), 5)
        st.session_state["user"] = user
        st.balloons()
        st.success("🎉 **Badge Débloqué : Mon premier PEA !** (+80 XP)")

with t6:
    st.markdown("### 👑 Niveau 6 — Le Maître de l'Indépendance")
    st.write("**Objectif :** Bilans récurrents, maintien de l'épargne de sécurité et autonomie dans la durée.")
    if st.button("👑 Débloquer le Badge Ultime", key="btn_n6", type="primary"):
        user["xp_points"] = user.get("xp_points", 120) + 150
        user["pea_level"] = max(user.get("pea_level", 0), 6)
        st.session_state["user"] = user
        st.balloons()
        st.success("👑 **BADGE ULTIME DÉBLOQUÉ : YELLOW MASTER !** (+150 XP)")

st.divider()

col_nav = st.columns([1, 2, 1])
with col_nav[1]:
    st.page_link("pages/7_Dashboard.py", label="Retour au Dashboard & Mes Badges 📊", icon="📊")
