"""Page de Dashboard Global & Progression — Yello."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="7. Dashboard Global — Yello", page_icon="📊", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title("📊 Tableau de Bord Global & Badges")
st.write(f"Client : **{user.get('full_name', 'Alexandre Dupont')}** | Identifiant : `{user.get('username', 'demo')}`")

st.divider()

# Barre de niveau globale
lvl = user.get("level", 1)
xp = user.get("xp_points", 120)
st.progress(min(1.0, (xp % 100) / 100.0), text=f"Niveau {lvl} — Total XP : {xp} points")

st.divider()

# Récapitulatif des badges débloqués
st.subheader("🏆 Galerie des Badges & Certifications Acquis")

c_b1, c_b2, c_b3, c_b4 = st.columns(4)

with c_b1:
    st.markdown("""
    <div class="mission-card mission-completed">
        <h4 style="margin-top:0; color:white;">🛡️ Matelas 1 Mois</h4>
        <p style="font-size:12px; color:#94A3B8;">Épargne de précaution testée et validée.</p>
        <span style="color:#10B981; font-weight:600; font-size:12px;">✓ Badge Acquis</span>
    </div>
    """, unsafe_allow_html=True)

with c_b2:
    st.markdown("""
    <div class="mission-card mission-completed">
        <h4 style="margin-top:0; color:white;">🧭 Premiers Pas Bourse</h4>
        <p style="font-size:12px; color:#94A3B8;">Niveau 1 PEA complété.</p>
        <span style="color:#10B981; font-weight:600; font-size:12px;">✓ Badge Acquis</span>
    </div>
    """, unsafe_allow_html=True)

with c_b3:
    has_sangfroid = xp >= 200
    st.markdown(f"""
    <div class="mission-card {'mission-completed' if has_sangfroid else ''}">
        <h4 style="margin-top:0; color:white;">🏆 Sang-froid Financier</h4>
        <p style="font-size:12px; color:#94A3B8;">Bac à sable 10 000 € virtuels.</p>
        <span style="color:{'#10B981' if has_sangfroid else '#E5A910'}; font-weight:600; font-size:12px;">{'✓ Badge Acquis' if has_sangfroid else 'En cours'}</span>
    </div>
    """, unsafe_allow_html=True)

with c_b4:
    has_master = xp >= 400
    st.markdown(f"""
    <div class="mission-card {'mission-completed' if has_master else ''}">
        <h4 style="margin-top:0; color:white;">👑 Yello Master</h4>
        <p style="font-size:12px; color:#94A3B8;">Certification ultime d'autonomie.</p>
        <span style="color:{'#10B981' if has_master else '#64748B'}; font-weight:600; font-size:12px;">{'✓ Badge Acquis' if has_master else 'À venir'}</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Suggestions d'actions pour la prochaine étape
st.subheader("💡 Suggestions pour votre Prochaine Étape")

col_s1, col_s2 = st.columns(2)

with col_s1:
    st.info("📈 **Découvrir le Niveau 2 du PEA**")
    st.write("Comprenez les avantages de la fiscalité 5 ans et la différence entre actions et ETF.")
    st.page_link("pages/5_ParcoursPEA.py", label="Accéder au Parcours PEA ➡️", icon="📈")

with col_s2:
    st.success("💬 **Poser vos questions à l'Agent IA**")
    st.write("Obtenez des réponses certifiées basées sur nos guides officiels.")
    st.page_link("pages/8_Chat.py", label="Ouvrir le Chat Marcel ➡️", icon="💬")
