"""Tableau de bord de suivi avec les 2 actions de démonstration interactives."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Dashboard & Missions — Yellow", page_icon="📊", layout="wide")

with open("static/css/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "user" not in st.session_state:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]
user_id = user.get("id", 1)

st.title("📊 Tableau de Bord & Jalons de Progression")
st.write(f"Client : **{user.get('full_name', 'Alexandre Dupont')}** | Parcours actif : **{user.get('current_track', 'courant').upper()}**")

# Barre de niveau
lvl = user.get("level", 1)
xp = user.get("xp_points", 120)
st.progress(min(1.0, (xp % 100) / 100.0), text=f"Niveau {lvl} — {xp} points d'expérience")

st.divider()

# =========================================================================
# LES 2 ACTIONS DE DÉMONSTRATION INTERACTIVES
# =========================================================================
st.subheader("🎯 Deux Démonstrations Clés du Dispositif")

tab_demo1, tab_demo2, tab_jalons = st.tabs([
    "🛡️ Action 1 : Test de Résistance (Épargne & Sérénité)",
    "📈 Action 2 : Radar de Veille Marché IA (Investir)",
    "🏅 Mes Jalons & Certifications"
])

# -------------------------------------------------------------------------
# DÉMO 1 : TEST DE RÉSISTANCE (PARCOURS ÉPARGNER)
# -------------------------------------------------------------------------
with tab_demo1:
    st.markdown("""
    ### 🛡️ Mission Simulation : Le Test de Résistance
    **Objectif :** Mesurer concrètement comment votre épargne absorbe un choc financier imprévu, sans jargon ni panique.
    """)

    col_sim1, col_sim2 = st.columns([1, 1])

    with col_sim1:
        st.write("##### 1. Vos paramètres financiers")
        depenses = st.slider("Dépenses incompressibles mensuelles (loyer, courses, charges)", 400, 2500, int(user.get("monthly_expenses", 700)), step=50, format="%d €")
        epargne = st.slider("Épargne de sécurité actuelle", 0, 10000, int(user.get("savings_balance", 3500)), step=100, format="%d €")
        imprevu_type = st.selectbox(
            "Scénario d'imprévu à tester :",
            [
                "Fin de contrat / Période de transition (2 mois sans salaire)",
                "Panne de voiture ou équipement indispensable (850 €)",
                "Dépense de santé ou imprévu familial (400 €)"
            ]
        )

    with col_sim2:
        st.write("##### 2. Diagnostic & Mesure de Sérénité")
        
        # Calcul du matelas
        mois_serenite = round(epargne / depenses, 1) if depenses > 0 else 0
        
        if "Fin de contrat" in imprevu_type:
            cout_imprevu = depenses * 2
            reste_epargne = max(0, epargne - cout_imprevu)
            mois_apres = round(reste_epargne / depenses, 1) if depenses > 0 else 0
        elif "850" in imprevu_type:
            cout_imprevu = 850
            reste_epargne = max(0, epargne - cout_imprevu)
            mois_apres = round(reste_epargne / depenses, 1) if depenses > 0 else 0
        else:
            cout_imprevu = 400
            reste_epargne = max(0, epargne - cout_imprevu)
            mois_apres = round(reste_epargne / depenses, 1) if depenses > 0 else 0

        # Indicateur sobre
        st.metric("Indicateur actuel", f"{mois_serenite} mois de sérénité")
        st.metric("Après absorption du choc", f"{mois_apres} mois restants", delta=f"-{cout_imprevu} € absorbés")

        if mois_serenite >= 3.0:
            st.success("✅ **Excellente résilience :** Vous disposez d'un fonds complet (≥ 3 mois). Vous pouvez envisager d'investir l'excédent.")
        elif mois_serenite >= 1.0:
            st.warning("⚠️ **Palier intermédiaire :** Votre matelas absorbe le premier choc, mais il est recommandé de reconstituer 2 mois de sécurité supplémentaires.")
        else:
            st.error("🚨 **Zone de vigilance :** Moins d'un mois de dépenses de côté. Priorité absolue : constituer 500 € à 1 000 € d'épargne d'urgence.")

        if st.button("Valider cette simulation & Débloquer le Jalon", type="primary", use_container_width=True):
            user["xp_points"] = user.get("xp_points", 120) + 60
            st.session_state["user"] = user
            st.balloons()
            st.success("Jalon validé : **'Matelas de Sécurité Testé'** (+60 XP attribués)")

# -------------------------------------------------------------------------
# DÉMO 2 : RADAR DE VEILLE MARCHÉ IA (PARCOURS INVESTIR)
# -------------------------------------------------------------------------
with tab_demo2:
    st.markdown("""
    ### 📈 L'Agent IA de Veille Marché : Information sans Incitation
    **Principe MiFID II :** L'agent informe sur l'état factuel du marché, explique la volatilité et cite ses sources. **Il ne donne aucun conseil d'achat ou de vente.**
    """)

    c_sec, c_vide = st.columns([2, 1])
    with c_sec:
        selected_sector = st.selectbox(
            "Sélectionnez le secteur sous surveillance :",
            [
                ("tech", "🇪🇺 Technologies Européennes (Euro Stoxx Tech)"),
                ("energie", "⚡ Énergies Renouvelables (S&P Global Clean Energy)"),
                ("immobilier", "🏢 Immobilier & SCPI (FTSE EPRA Nareit)")
            ],
            format_func=lambda x: x[1]
        )

    # Récupération du briefing de l'agent
    briefing = api_service.get_market_briefing(selected_sector[0])

    # Affichage du cadre d'information de marché
    st.markdown(f"""
    <div class="market-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h4 style="margin:0; color:#E5A910;">{briefing['sector']}</h4>
            <span style="font-size:16px;">{briefing['ambiance']}</span>
        </div>
        <p style="color:#94A3B8; font-size:13px; margin-top:4px;">Indice de référence : <b>{briefing['benchmark_index']}</b> | Variation 30 jours : <b>{briefing['monthly_variation']}</b></p>
        <p style="color:#F8FAFC; font-size:14px; line-height:1.6; margin-top:12px;">{briefing['analysis']}</p>
        <p style="color:#94A3B8; font-size:12px;"><b>Événement sous-jacent :</b> {briefing['key_event']}</p>
        <p style="color:#94A3B8; font-size:12px;"><b>Sources officielles citées :</b> {', '.join(briefing['sources'])}</p>
        <div class="legal-disclaimer">
            ⚖️ <b>Garde-fou réglementaire :</b> {briefing['disclaimer']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.write("##### ⏳ Bac à sable : 'La Machine à Remonter le Temps'")
    st.write("Voyez comment un portefeuille fictif de 1 000 € investi sur un ETF diversifié traverse une crise sans paniquer :")

    c_temps1, c_temps2, c_temps3 = st.columns(3)
    with c_temps1:
        st.metric("Janvier 2020 (Départ)", "1 000 €", "Point d'entrée")
    with c_temps2:
        st.metric("Mars 2020 (Choc Covid)", "750 €", "-25% (Forte turbulence)", delta_color="inverse")
    with c_temps3:
        st.metric("Mars 2021 (+1 an)", "1 150 €", "+15% (Discipline conservée)")

    st.info("💡 **Règle d'or de l'investisseur :** La volatilité est normale sur les marchés actions. Vendre pendant la baisse matérialise la perte. Conserver son plan régulier permet de capter le rebond.")

# -------------------------------------------------------------------------
# TAB 3 : JALONS ET CERTIFICATIONS SOBRES
# -------------------------------------------------------------------------
with tab_jalons:
    st.subheader("🏅 Vos Jalons Validés")
    st.write("Des jalons sobres, sans mascottes, marquant chaque étape clé de votre maturité financière.")

    c_b1, c_b2, c_b3 = st.columns(3)
    with c_b1:
        st.markdown("""
        <div class="mission-card mission-completed">
            <h4>🧭 Vision Claire</h4>
            <p style="font-size:13px; color:#94A3B8;">30 jours de dépenses analysés et catégorisés avec succès.</p>
            <span style="color:#10B981; font-weight:600; font-size:12px;">✓ Jalon acquis</span>
        </div>
        """, unsafe_allow_html=True)
    with c_b2:
        st.markdown("""
        <div class="mission-card mission-completed">
            <h4>🛡️ Matelas 1 Mois</h4>
            <p style="font-size:13px; color:#94A3B8;">Premier palier d'épargne de sécurité atteint et testé.</p>
            <span style="color:#10B981; font-weight:600; font-size:12px;">✓ Jalon acquis</span>
        </div>
        """, unsafe_allow_html=True)
    with c_b3:
        st.markdown("""
        <div class="mission-card">
            <h4>📈 Épargnant Averti</h4>
            <p style="font-size:13px; color:#94A3B8;">Compréhension des 5 ans du PEA et de l'inflation.</p>
            <span style="color:#E5A910; font-weight:600; font-size:12px;">En cours</span>
        </div>
        """, unsafe_allow_html=True)
