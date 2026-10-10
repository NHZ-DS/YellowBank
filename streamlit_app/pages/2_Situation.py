"""Page de Situation Actuelle & Visualisation — Yello."""

import streamlit as st
import pandas as pd
from services.api_service import api_service

st.set_page_config(page_title="2. Situation Actuelle — Yello", page_icon="⭐", layout="wide")

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]
profil = st.session_state.get("profil", {})

age = profil.get("age", "Non renseigné")
statut = profil.get("statut", "Non renseigné")
details = profil.get("details", {})
objectif = profil.get("objectif", "Non défini")
interets = profil.get("interets", [])

# ==========================================
# STYLES CSS SANS LIGNES VIDES
# ==========================================
st.markdown("""
<style>
.stApp { background-color: #F8FAFC; }
.page-title { font-size: 32px; font-weight: 900; color: #0F172A; text-align: center; margin-bottom: 10px; }
.page-subtitle { font-size: 16px; color: #64748B; text-align: center; margin-bottom: 40px; }
div[data-testid="column"] { background: white; border-radius: 24px; padding: 20px; box-shadow: 0 10px 20px rgba(15,23,42,0.05); border: 1px solid #E2E8F0; transition: transform 0.3s; }
div[data-testid="column"]:hover { transform: translateY(-5px); border-color: #3B82F6; box-shadow: 0 15px 30px rgba(59,130,246,0.15); }
.recap-label { font-size: 13px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;}
.recap-val { font-size: 18px; font-weight: 900; color: #0F172A; }
.recap-icon { font-size: 30px; margin-bottom: 10px; }
.action-btn-container { text-align: center; margin-top: 40px; margin-bottom: 40px; }
.arcade-btn { display: inline-block; background: linear-gradient(180deg, #3B82F6 0%, #2563EB 100%); color: white !important; font-size: 20px; font-weight: 900; text-transform: uppercase; text-decoration: none; padding: 18px 50px; border-radius: 40px; border: none; box-shadow: 0 6px 0 #1D4ED8, 0 15px 20px rgba(37,99,235,0.3); transition: all 0.1s; animation: pulse-blue 2s infinite; }
.arcade-btn:active { transform: translateY(6px); box-shadow: 0 0px 0 #1D4ED8; }
@keyframes pulse-blue { 0% { box-shadow: 0 6px 0 #1D4ED8, 0 0 0 0 rgba(59,130,246,0.7); } 70% { box-shadow: 0 6px 0 #1D4ED8, 0 0 0 15px rgba(59,130,246,0); } 100% { box-shadow: 0 6px 0 #1D4ED8, 0 0 0 0 rgba(59,130,246,0); } }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">Diagnostic Visuel de ta Situation</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Voici la synthèse de ton profil et des recommandations adaptées.</div>', unsafe_allow_html=True)

# ------------------------------------------
# 1. RÉCAPITULATIF DU PROFIL
# ------------------------------------------
st.markdown("### 📋 Ton Profil Yello")
c1, c2, c3 = st.columns(3)

with c1:
    details_str = "<br>".join([f"<span style='font-size:13px; color:#64748B;'>{k.capitalize()}: {v}</span>" for k,v in details.items() if v])
    st.markdown(f"""
    <div class="recap-icon">👤</div>
    <div class="recap-label">Âge & Statut</div>
    <div class="recap-val">{age} <br><span style="color:#3B82F6;">{statut}</span><br>{details_str}</div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="recap-icon">🎯</div>
    <div class="recap-label">Objectif Principal</div>
    <div class="recap-val">{objectif}</div>
    """, unsafe_allow_html=True)

with c3:
    interets_str = ", ".join(interets).capitalize() if interets else "Non définis"
    st.markdown(f"""
    <div class="recap-icon">⭐</div>
    <div class="recap-label">Centres d'intérêt</div>
    <div class="recap-val" style="font-size:15px;">{interets_str}</div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ------------------------------------------
# 2. AVATAR & JAUGES ADAPTÉS
# ------------------------------------------
st.markdown("### 🛡️ Ta Santé Financière")
col_av1, col_av2, col_av3 = st.columns(3)

# Logique conditionnelle pour les alertes/conseils selon le statut
matelas_actuel = user.get("savings_balance", 3500.0)
depenses = user.get("monthly_expenses", 700.0)
months_serenity = round(matelas_actuel / depenses, 1) if depenses > 0 else 0

with col_av1:
    st.markdown("""
    <div style="text-align:center;">
        <div style="font-size:45px;">👤</div>
        <h3 style="margin:4px 0; color:#E5A910; font-size: 20px;">Aventurier Sérénité</h3>
        <p style="font-size:14px; color:#64748B;">Statut : <b>Épargnant Actif</b></p>
    </div>
    """, unsafe_allow_html=True)

with col_av2:
    st.markdown(f"""
    <div style="text-align:center;">
        <div style="font-size:45px;">🛡️</div>
        <h3 style="margin:4px 0; color:#10B981; font-size: 20px;">{months_serenity} Mois de Sécurité</h3>
        <p style="font-size:14px; color:#64748B;">Matelas d'urgence : <b>{matelas_actuel:,.0f} €</b></p>
    </div>
    """, unsafe_allow_html=True)

with col_av3:
    st.markdown(f"""
    <div style="text-align:center;">
        <div style="font-size:45px;">🏆</div>
        <h3 style="margin:4px 0; color:#3B82F6; font-size: 20px;">Niveau {user.get('level', 1)}</h3>
        <p style="font-size:14px; color:#64748B;">Prochain badge : <b>Matelas 1 Mois</b></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Message ciblé selon le profil
if statut == "Étudiant·e":
    st.info("🎓 **Astuce Yello :** En tant qu'étudiant, pensez à vérifier vos droits aux APL et à la bourse du CROUS. Vous pouvez utiliser ces aides pour financer votre quotidien ou commencer à épargner !")
elif statut == "Salarié·e":
    st.success("💼 **Astuce Yello :** Votre statut de salarié vous permet d'envisager des stratégies d'investissement (PEA) de manière régulière. L'automatisation est votre meilleure alliée !")
elif statut in ["Alternant·e", "Indépendant·e"]:
    st.warning("⚖️ **Astuce Yello :** Votre revenu peut fluctuer ou être en transition. Visez un matelas de sécurité plus robuste (3 à 6 mois) avant de vous lancer dans de gros investissements.")
elif statut == "En recherche":
    st.error("🔍 **Astuce Yello :** L'objectif actuel est de sécuriser le budget court terme et d'optimiser les aides (France Travail, Action Logement). Gardez vos liquidités disponibles.")

# ------------------------------------------
# 3. GRAPHIQUE ÉVOLUTION
# ------------------------------------------
st.markdown("### 📈 Évolution de ton Patrimoine")

months = [f"Mois {i}" for i in range(1, 13)]
courant = [800, 950, 1100, 1050, 1200, 1350, 1250, 1400, 1380, 1500, 1420, user.get("balance", 1450.80)]
epargne = [1000, 1200, 1500, 1800, 2000, 2300, 2600, 2900, 3100, 3300, 3400, user.get("savings_balance", 3500.00)]

df_chart = pd.DataFrame({
    "Compte Courant (€)": courant,
    "Épargne de Sécurité (€)": epargne
}, index=months)

st.line_chart(df_chart, height=320)

# ------------------------------------------
# 4. BOUTON CONTINUER
# ------------------------------------------
st.markdown("""
<div class="action-btn-container">
    <a href="Parcours" target="_self" class="arcade-btn">Accéder au Grand Plateau ▶</a>
</div>
""", unsafe_allow_html=True)
