"""Espace Client, Gestion des Données et Confidentialité RGPD."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Mon Profil — Archipel", page_icon="👤", layout="wide")

with open("static/css/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "user" not in st.session_state:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]
user_id = user.get("id", 1)

st.title("👤 Mon Espace Client & Confidentialité")

st.divider()

col_id, col_fin = st.columns(2)

with col_id:
    st.subheader("Identité & Coordonnées")
    st.write(f"**Nom complet :** {user.get('full_name', 'Alexandre Dupont')}")
    st.write(f"**Identifiant :** `{user.get('username', 'demo')}`")
    st.write(f"**Email sécurisé :** `{user.get('email', 'demo@yellowbank.fr')}`")
    st.write(f"**IBAN YellowBank :** `FR76 3000 4001 2345 6789 01`")

with col_fin:
    st.subheader("Situation Financière")
    st.write(f"**Revenus mensuels déclarés :** {user.get('monthly_income', 2600.00):,.2f} €")
    st.write(f"**Charges incompressibles :** {user.get('monthly_expenses', 700.00):,.2f} €")
    st.write(f"**Solde disponible :** {user.get('balance', 1450.80):,.2f} €")
    st.write(f"**Épargne de réserve :** {user.get('savings_balance', 3500.00):,.2f} €")

st.divider()

# =========================================================================
# GESTION DU CONSENTEMENT RGPD & RAPPORT CONSEILLER
# =========================================================================
st.subheader("🛡️ Confidentialité & Espace Conseiller (RGPD)")
st.write(
    "Chez YellowBank, vous gardez le contrôle total sur vos données personnelles. "
    "Vous pouvez choisir d'autoriser ou de refuser que votre conseiller bancaire humain "
    "ait accès à une synthèse de vos projets et questions posées à l'IA."
)

current_consent = user.get("advisor_share_consent", True)

new_consent = st.checkbox(
    "J'autorise YellowBank à partager une synthèse de mon activité et de mes projets avec mon conseiller bancaire.",
    value=current_consent
)

if new_consent != current_consent:
    user["advisor_share_consent"] = new_consent
    st.session_state["user"] = user
    api_service.update_consent(user_id, new_consent)
    st.success("Préférence de confidentialité mise à jour instantanément.")

st.write("---")

st.subheader("📋 Prévisualisation de la Synthèse Conseiller")
st.write("Voici exactement le document de synthèse transmis à votre conseiller bancaire si le partage est autorisé :")

if st.button("Afficher la fiche de synthèse conseiller", use_container_width=True):
    report = api_service.get_advisor_report(user_id)
    
    if not report.get("authorized", False):
        st.warning("🔒 **Accès verrouillé (RGPD) :** Vous avez refusé le partage de données. Votre conseiller ne reçoit aucun compte-rendu.")
    else:
        st.markdown(f"""
        <div class="market-box">
            <h4 style="color:#E5A910; margin-top:0;">Fiche de Liaison Conseiller — {report.get('client_name')}</h4>
            <p><b>Parcours Prioritaire :</b> {report.get('current_track')}</p>
            <p><b>Indicateur Taux d'Endettement :</b> {report.get('financial_summary', {}).get('debt_ratio')}</p>
            <p><b>Sujets explorés avec l'IA :</b> {', '.join(report.get('topics_discussed_with_ai', []))}</p>
            <p><b>Recommandation d'action pour le conseiller :</b></p>
            <ul>
                {''.join([f"<li>{a}</li>" for a in report.get('suggested_advisor_actions', [])])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
