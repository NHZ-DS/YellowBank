"""Page de Situation Actuelle & Visualisation — Yellow."""

import streamlit as st
import pandas as pd
from services.api_service import api_service

st.set_page_config(page_title="2. Situation Actuelle — Yellow", page_icon="⭐", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title(" Diagnostic Visuel de votre Situation Actuelle")
st.write("Retrouvez ici la synthèse visuelle de vos finances et les résultats de votre questionnaire.")

st.divider()

# Récapitulatif des réponses du questionnaire
st.subheader("📋 Récapitulatif de votre Profil")
col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.info(f" **Tranche d'âge :**\n{user.get('age_group', '22-25 ans (Jeune actif)')}")

with col_r2:
    track_name = user.get('current_track', 'courant').upper()
    st.success(f" **Parcours Choisi :**\n{track_name}")

with col_r3:
    st.warning(f" **Niveau & XP :**\nNiveau {user.get('level', 1)} ({user.get('xp_points', 120)} XP)")

st.divider()

# Avatar & Gauges de Santé Financière
st.subheader(" Votre Avatar Financier & Jauge de Sérénité")
col_av1, col_av2, col_av3 = st.columns(3)

with col_av1:
    st.markdown("""
    <div class="market-box" style="text-align:center;">
        <div style="font-size:45px;">👤</div>
        <h3 style="margin:4px 0; color:#E5A910;">Aventurier Sérénité</h3>
        <p style="font-size:13px; color:#94A3B8;">Statut : <b>Épargnant Actif</b></p>
    </div>
    """, unsafe_allow_html=True)

with col_av2:
    months_serenity = round(user.get("savings_balance", 3500.0) / user.get("monthly_expenses", 700.0), 1)
    st.markdown(f"""
    <div class="market-box" style="text-align:center;">
        <div style="font-size:45px;">🛡️</div>
        <h3 style="margin:4px 0; color:#10B981;">{months_serenity} Mois de Sécurité</h3>
        <p style="font-size:13px; color:#94A3B8;">Matelas d'urgence : <b>{user.get('savings_balance', 3500):,.2f} €</b></p>
    </div>
    """, unsafe_allow_html=True)

with col_av3:
    st.markdown("""
    <div class="market-box" style="text-align:center;">
        <div style="font-size:45px;">🏆</div>
        <h3 style="margin:4px 0; color:#3B82F6;">Niveau 1</h3>
        <p style="font-size:13px; color:#94A3B8;">Prochain badge : <b>Matelas 1 Mois</b></p>
    </div>
    """, unsafe_allow_html=True)

# Barre de progression globale
st.write("##### Progression du niveau :")
st.progress(min(1.0, (user.get("xp_points", 120) % 100) / 100.0), text=f"{user.get('xp_points', 120)} XP acquis sur ce palier")

st.divider()

# Graphe interactif d'évolution du compte et de l'épargne
st.subheader(" Graphique d'Évolution de votre Patrimoine (12 derniers mois)")

months = [f"Mois {i}" for i in range(1, 13)]
courant = [800, 950, 1100, 1050, 1200, 1350, 1250, 1400, 1380, 1500, 1420, user.get("balance", 1450.80)]
epargne = [1000, 1200, 1500, 1800, 2000, 2300, 2600, 2900, 3100, 3300, 3400, user.get("savings_balance", 3500.00)]

df_chart = pd.DataFrame({
    "Compte Courant (€)": courant,
    "Épargne de Sécurité (€)": epargne
}, index=months)

st.line_chart(df_chart, height=320)

st.info(" **Analyse Visuelle :** Votre épargne progresse de façon régulière. Vous disposez d'un matelas suffisant pour envisager le parcours d'investissement.")

st.divider()

# Bouton d'action vers la sélection des parcours
c_btn = st.columns([1, 2, 1])
with c_btn[1]:
    st.page_link("pages/3_Parcours.py", label="Choisir mon Parcours & Commencer les Jeux", icon="🧭")
