"""Parcours 1 : Épargner & Budget — Archipel."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Parcours 1 : Épargner & Budget — Archipel", page_icon="🛡️", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title("🛡️ Parcours 1 : Épargner & Budget")
st.write("Réalisez les étapes ci-dessous sous forme de mini-jeux pour débloquer vos badges.")

st.divider()

# Liste des étapes du jeu
tab_e1, tab_e2 = st.tabs(["🕹️ Étape 1 : Le Test de Résistance", "🧩 Étape 2 : Le Quizz Budgétaire 50/30/20"])

with tab_e1:
    st.markdown("### 🕹️ Étape 1 : Simuler la Résistance à un Imprévu")
    st.write("Ajustez vos curseurs pour mesurer combien de mois de sérénité résistent à un choc financier :")

    depenses = st.slider("Dépenses mensuelles incompressibles (€)", 400, 2000, int(user.get("monthly_expenses", 700)))
    epargne = st.slider("Épargne de sécurité actuelle (€)", 0, 5000, int(user.get("savings_balance", 3500)))

    type_imprevu = st.selectbox(
        "Choisissez un scénario d'imprévu à tester :",
        ["Panne de voiture / Ordinateur (600 €)", "Réparation d'urgence (900 €)", "Période de transition (2 mois de dépenses)"]
    )

    cout = 600 if "600" in type_imprevu else (900 if "900" in type_imprevu else depenses * 2)
    reste = max(0, epargne - cout)
    mois_r = round(reste / depenses, 1) if depenses > 0 else 0

    st.metric("Matelas de sécurité restant", f"{mois_r} mois restants", delta=f"-{cout} € absorbés")

    if st.button("🏆 Valider l'Étape 1 & Obtenir le Badge", type="primary"):
        user["xp_points"] = user.get("xp_points", 120) + 60
        user["budget_level"] = max(user.get("budget_level", 0), 1)
        st.session_state["user"] = user
        st.balloons()
        st.success("🎉 **Badge Débloqué : Matelas de Sécurité Testé !** (+60 XP attribués)")

with tab_e2:
    st.markdown("### 🧩 Étape 2 : La Règle Budgétaire 50/30/20")
    st.write("Testez vos connaissances en gestion de budget :")

    q1 = st.radio(
        "Dans la règle 50/30/20, à quoi correspondent les 20% ?",
        ["Les dépenses de loisirs et sorties", "L'épargne et les investissements", "Le loyer et les factures"],
        index=0
    )

    if st.button("Valider ma réponse au Quizz", type="primary"):
        if "épargne" in q1.lower():
            user["xp_points"] = user.get("xp_points", 120) + 50
            user["budget_level"] = max(user.get("budget_level", 0), 2)
            st.session_state["user"] = user
            st.balloons()
            st.success("🎉 **Excellente réponse !** Badge Débloqué : 🧭 **Gestionnaire Prudent** (+50 XP)")
        else:
            st.error("Essayez encore ! Les 20% sont réservés à la constitution de l'épargne.")

st.divider()

col_nav = st.columns([1, 2, 1])
with col_nav[1]:
    st.page_link("pages/7_Dashboard.py", label="Retour au Dashboard & Mes Badges 📊", icon="📊")
