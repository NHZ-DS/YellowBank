"""Accueil de l'application Yello — Expérience Arcade & Gamifiée avec Animations Lottie."""

import streamlit as st
import streamlit.components.v1 as components
from services.api_service import api_service

# Configuration de la page
st.set_page_config(
    page_title="Yello — Jouer",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fonction d'affichage des animations Lottie
def lottie(url: str, height: int = 160):
    components.html(f"""
    <script src="https://unpkg.com/@lottiefiles/dotlottie-wc@latest/dist/dotlottie-wc.js" type="module"></script>
    <div style="display:flex;justify-content:center;align-items:center;height:{height}px;">
        <dotlottie-wc src="{url}" autoplay loop style="width:100%;height:100%;"></dotlottie-wc>
    </div>
    """, height=height + 15)

# Style CSS personnalisé
try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# Initialisation des variables session (HUD)
if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]
username = user.get("full_name", "Alexandre").split(" ")[0]

# Variables de jeu
xp = st.session_state.get("xp", user.get("xp_points", 120))
level = st.session_state.get("level", user.get("level", 1))
coins = st.session_state.get("coins", 450)

# ==========================================
# STYLES CSS SPÉCIFIQUES ARCADE
# ==========================================
st.markdown("""
<style>
/* HUD EN HAUT */
.arcade-hud {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.8);
    backdrop-filter: blur(10px);
    border-bottom: 2px solid #E5A910;
    padding: 10px 20px;
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(229, 169, 16, 0.2);
}
.hud-logo { font-size: 24px; font-weight: 900; color: #E5A910; text-transform: uppercase; letter-spacing: 2px; }
.hud-stats { display: flex; gap: 20px; align-items: center; }
.hud-level { font-weight: 800; color: white; background: #2563EB; padding: 4px 12px; border-radius: 20px; font-size: 14px; }
.hud-xp-bar { width: 120px; height: 10px; background: #334155; border-radius: 10px; overflow: hidden; border: 1px solid #475569; }
.hud-xp-fill { width: 60%; height: 100%; background: linear-gradient(90deg, #10B981, #34D399); }
.hud-coins { font-weight: 800; color: #FBBF24; display: flex; align-items: center; gap: 6px; font-size: 16px; }

/* BANNIÈRE D'ACCUEIL */
.banner-container {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    margin-bottom: 50px;
}
.banner-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    margin-bottom: 5px;
    text-shadow: 0 4px 10px rgba(0,0,0,0.5);
    line-height: 1.2;
}
.banner-slogan {
    font-size: 24px;
    font-weight: 800;
    color: #E5A910;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
    margin-top: 10px;
}
.banner-text {
    font-size: 16px;
    color: #94A3B8;
    line-height: 1.6;
}

/* SECTION TITRE POURQUOI CHOISIR */
.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #1E293B;
    margin-bottom: 10px;
}
.section-subtitle {
    color: #64748B;
    font-size: 16px;
    margin-bottom: 30px;
}

/* CARTES NATIVES STREAMLIT CUSTOM */
div[data-testid="column"] {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    border: 1px solid #E2E8F0;
    transition: transform 0.3s, box-shadow 0.3s;
}
div[data-testid="column"]:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(229,169,16,0.15);
    border-color: #E5A910;
}
.card-number {
    font-size: 18px;
    font-weight: 900;
    color: #E5A910;
    margin-bottom: -15px;
}
.card-title {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
    margin-top: 10px;
    margin-bottom: 10px;
}
.card-desc {
    font-size: 14px;
    color: #64748B;
}

/* BOUTON JOUER ARCADE */
.arcade-btn-container { text-align: center; margin-top: 40px; margin-bottom: 60px; }
.cta-text { font-size: 24px; font-weight: 900; color: #1E293B; margin-bottom: 20px; text-transform: uppercase;}
.arcade-btn {
    display: inline-block;
    background: linear-gradient(180deg, #E5A910 0%, #B4840A 100%);
    color: white !important;
    font-size: 24px;
    font-weight: 900;
    text-transform: uppercase;
    text-decoration: none;
    padding: 20px 60px;
    border-radius: 50px;
    border: none;
    box-shadow: 0 8px 0 #8A6405, 0 15px 20px rgba(0,0,0,0.4);
    transition: all 0.1s;
    animation: pulse 2s infinite;
    cursor: pointer;
}
.arcade-btn:active {
    transform: translateY(8px);
    box-shadow: 0 0px 0 #8A6405, 0 5px 10px rgba(0,0,0,0.4);
}
@keyframes pulse {
    0% { box-shadow: 0 8px 0 #8A6405, 0 0 0 0 rgba(229,169,16,0.7); }
    70% { box-shadow: 0 8px 0 #8A6405, 0 0 0 20px rgba(229,169,16,0); }
    100% { box-shadow: 0 8px 0 #8A6405, 0 0 0 0 rgba(229,169,16,0); }
}

@media (prefers-color-scheme: dark) {
    .section-title, .cta-text { color: white; }
    div[data-testid="column"] { background: #1E293B; border-color: #334155; }
    .card-title { color: white; }
    .card-desc, .section-subtitle { color: #94A3B8; }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. HUD EN HAUT
# ==========================================
st.markdown(f"""
<div class="arcade-hud">
    <div class="hud-logo">YELLO</div>
    <div class="hud-stats">
        <div class="hud-level">LVL {level}</div>
        <div class="hud-xp-bar"><div class="hud-xp-fill"></div></div>
        <div class="hud-coins">
            🪙 {coins}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. BANNIÈRE D'ACCUEIL AVEC LOTTIE
# ==========================================
st.markdown('<div class="banner-container">', unsafe_allow_html=True)
col_b1, col_b2 = st.columns([2, 1])

with col_b1:
    st.markdown(f"""
    <div class="banner-title">Salut {username} ! Bienvenue sur Yello</div>
    <div class="banner-slogan">Your Financial Adventure</div>
    <div class="banner-text">La première application bancaire ludique qui transforme la gestion d'argent en un jeu de stratégie et d'apprentissage sans pression.</div>
    """, unsafe_allow_html=True)

with col_b2:
    lottie("https://assets-v2.lottiefiles.com/a/dc03a102-7fd4-11ef-823f-4b77d70ae382/537QUUlhlg.lottie", 220)

st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 3. POURQUOI CHOISIR YELLO ? (CARTES + LOTTIE)
# ==========================================
st.markdown("""
<div class="section-title">Pourquoi choisir Yello ?</div>
<div class="section-subtitle">Finis les formulaires administratifs austères ! Yello vous accompagne de manière ludique, visuelle et gratifiante pour maîtriser votre budget et faire vos premiers pas en bourse.</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    lottie("https://assets-v2.lottiefiles.com/a/94e496be-1167-11ee-8394-235eccc39aff/sDUS5XtwWU.lottie", 180)
    st.markdown("""
    <div class="card-number">01</div>
    <div class="card-title">Calibrage sur Mesure</div>
    <div class="card-desc">Répondez à un court questionnaire pour définir votre tranche d'âge, vos centres d'intérêt et votre profil de risque.</div>
    """, unsafe_allow_html=True)

with col2:
    lottie("https://assets-v2.lottiefiles.com/a/a29f68b0-63bf-11ee-8655-b302196e7a77/WoXvLOaPsg.lottie", 180)
    st.markdown("""
    <div class="card-number">02</div>
    <div class="card-title">Situation Visuelle</div>
    <div class="card-desc">Visualisez votre jauge de sérénité, votre avatar progressif et l'évolution de votre patrimoine sur un magnifique plateau.</div>
    """, unsafe_allow_html=True)

with col3:
    lottie("https://assets-v2.lottiefiles.com/a/a5841fa0-117e-11ee-baae-5bb1ce7e6584/G96ILI4Xy6.lottie", 180)
    st.markdown("""
    <div class="card-number">03</div>
    <div class="card-title">Missions & Badges</div>
    <div class="card-desc">Réalisez des mini-jeux à chaque étape de votre parcours pour gagner des points d'expérience (XP) et débloquer des récompenses.</div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. APPEL À L'ACTION & BOUTON JOUER (LOTTIE FUSÉE)
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)

col_f1, col_f2 = st.columns([1, 1])

with col_f1:
    lottie("https://assets-v2.lottiefiles.com/a/7c03fa1e-117a-11ee-9f0a-8f62cd81c7a3/uU7kl3MLw8.lottie", 250)

with col_f2:
    st.markdown("""
    <div class="arcade-btn-container" style="text-align: left; padding-top: 50px;">
        <div class="cta-text">Prêt·e à commencer ton aventure ?</div>
        <a href="Questionnaire" target="_self" class="arcade-btn">▶ JOUER</a>
    </div>
    """, unsafe_allow_html=True)