"""Parcours 1 : Épargner & Budget — carte de progression et mini-jeux."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Parcours 1 — Épargner", page_icon="🛡️", layout="wide")
ss = st.session_state

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in ss or not ss["user"]:
    ss["user"] = api_service.login("demo", "demo123").get("user", {})
user = ss["user"]

# ---------------------------------------------------------------------------
# Étapes du parcours (2 mini-jeux + la récompense finale)
# ---------------------------------------------------------------------------
STEPS = {
    1: {"name": "Test de résistance", "title": "Simuler un imprévu", "icon": "shield", "c1": "#3B82F6", "c2": "#1D4ED8",
        "badge": "Bouclier anti-imprévu", "xp": 50,
        "objectif": "Mesurer combien de mois ton épargne de sécurité tient face à un coup dur."},
    2: {"name": "Quiz 50/30/20", "title": "La règle budgétaire", "icon": "pie_chart", "c1": "#22C55E", "c2": "#15803D",
        "badge": "Maître du budget", "xp": 50,
        "objectif": "Comprendre comment répartir ses revenus entre besoins, envies et épargne."},
    3: {"name": "Gardien de l'épargne", "title": "Parcours terminé", "icon": "savings", "c1": "#FFC83D", "c2": "#14213D",
        "badge": "Gardien de l'épargne", "xp": 100,
        "objectif": "La récompense finale du parcours Épargner & Budget."},
}
N_GAMES = 2

SCENARIOS = {
    "Frais de santé imprévus (250 €)": lambda dep: 250,
    "Panne de voiture / ordinateur (600 €)": lambda dep: 600,
    "Déménagement imprévu (1 200 €)": lambda dep: 1200,
    "Perte d'emploi (3 mois sans revenu)": lambda dep: 3 * dep,
}

ss.setdefault("courant_etape", int(user.get("courant_level", 0) or 0))  # mini-jeux validés (0, 1 ou 2)
ss.setdefault("courant_sel", min(ss.courant_etape + 1, N_GAMES))
done = ss.courant_etape


def state_of(n: int) -> str:
    if n == 3:
        return "done" if done >= N_GAMES else "locked"
    if n <= done:
        return "done"
    if n == done + 1:
        return "current"
    return "locked"


# ---------------------------------------------------------------------------
# Style (identique au parcours Investir)
# ---------------------------------------------------------------------------
NAVY, BLUE, GOLD, SOFT, MUTE = "#14213D", "#1F2BE0", "#FFC83D", "#EEF1F8", "#5B6785"
track_pct = min(100, done / 2 * 100)
CSS = f"""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL@24,500,1" rel="stylesheet">
<style>
.stApp{{background:#E6EBF5!important;}}
.block-container,[data-testid="stMainBlockContainer"]{{max-width:100%!important;width:100%!important;padding:1.6rem 3rem 3rem!important;}}
[data-testid="stMain"] p,[data-testid="stMain"] div,[data-testid="stMain"] button,[data-testid="stMain"] label{{font-family:'Plus Jakarta Sans',sans-serif;}}
.ms{{font-family:'Material Symbols Rounded'!important;font-weight:normal;font-style:normal;line-height:1;display:inline-block;
  -webkit-font-feature-settings:'liga';font-feature-settings:'liga';font-variation-settings:'FILL' 1;}}

.p-head{{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;margin-bottom:18px;}}
.p-kick{{font-size:13px;font-weight:800;letter-spacing:2px;color:{BLUE};text-transform:uppercase;}}
.p-title{{font-size:36px;font-weight:800;color:{NAVY};margin:4px 0 2px;letter-spacing:-.5px;}}
.p-sub{{color:{MUTE};font-size:15.5px;margin:0;}}
.hud{{display:flex;gap:12px;flex-wrap:wrap;}}
.hud div{{background:#fff;border-radius:18px;padding:10px 18px;box-shadow:0 6px 18px rgba(20,33,61,.07);display:flex;align-items:center;gap:10px;}}
.hud .ms{{font-size:28px;}}
.hud b{{display:block;font-size:20px;color:{NAVY};line-height:1.1;}}
.hud small{{color:{MUTE};font-weight:600;font-size:12.5px;}}

/* Carte de progression */
.st-key-map{{position:relative;background:linear-gradient(135deg,#1A2B5C,#101B3A)!important;border-radius:30px!important;padding:26px 22px 18px!important;
  box-shadow:0 14px 34px rgba(20,33,61,.25);overflow:hidden;}}
.st-key-map:before{{content:"";position:absolute;left:16.7%;right:16.7%;top:88px;height:10px;border-radius:99px;background:rgba(255,255,255,.12);}}
.st-key-map:after{{content:"";position:absolute;left:16.7%;top:88px;height:10px;border-radius:99px;width:calc(66.6% * {track_pct / 100:.3f});
  background:linear-gradient(90deg,#3B82F6,{GOLD});box-shadow:0 0 14px rgba(255,200,61,.6);}}
.st-key-map [data-testid="stColumn"]{{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;}}
.node{{display:flex;flex-direction:column;align-items:center;gap:6px;}}
.node .lvl{{font-size:12px;font-weight:800;letter-spacing:1.5px;color:#93A3C8;text-transform:uppercase;margin-top:4px;}}
.node.current .lvl{{color:{GOLD};}}
.st-key-map .stButton,.st-key-map [data-testid="stElementContainer"]{{width:100%!important;display:flex;justify-content:center;}}
.st-key-map button{{background:transparent!important;border:none!important;box-shadow:none!important;padding:2px 8px!important;min-height:0!important;}}
.st-key-map button p{{color:#fff!important;font-weight:800!important;font-size:15px!important;}}
.st-key-map button:hover p{{color:{GOLD}!important;}}
.st-key-map button:disabled p{{color:#5F6E93!important;}}
.st-key-map button[kind="primary"] p,.st-key-map button[data-testid="stBaseButton-primary"] p{{color:{GOLD}!important;text-decoration:underline;text-underline-offset:5px;}}

/* Badge hexagonal */
.bdg{{position:relative;width:var(--s);height:calc(var(--s) * 1.12);}}
.bdg .hex{{position:absolute;clip-path:polygon(50% 0,94% 24%,94% 76%,50% 100%,6% 76%,6% 24%);}}
.bdg .o{{inset:0;background:linear-gradient(180deg,#FFE9A8 0%,#F2B623 55%,#C98A00 100%);}}
.bdg .i{{inset:7%;background:linear-gradient(160deg,var(--c1),var(--c2));display:flex;align-items:center;justify-content:center;}}
.bdg .i:after{{content:"";position:absolute;left:0;right:0;top:0;height:46%;background:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,0));}}
.bdg .i .ms{{color:#fff;font-size:calc(var(--s) * .44);filter:drop-shadow(0 3px 2px rgba(0,0,0,.25));z-index:1;}}
.bdg .pin{{position:absolute;right:-2px;bottom:6%;width:calc(var(--s) * .34);height:calc(var(--s) * .34);border-radius:50%;
  display:flex;align-items:center;justify-content:center;border:3px solid #101B3A;z-index:2;}}
.bdg .pin .ms{{font-size:calc(var(--s) * .2);color:#fff;}}
.bdg.done .pin{{background:#22C55E;}}
.bdg.locked .o{{background:linear-gradient(180deg,#8D97AF,#5F6A85);}}
.bdg.locked .i{{background:linear-gradient(160deg,#4A5577,#343E5C);}}
.bdg.locked .i .ms{{opacity:.35;}}
.bdg.locked .pin{{background:#5F6A85;}}
.bdg.current{{animation:float 2.6s ease-in-out infinite;filter:drop-shadow(0 0 18px rgba(255,200,61,.75));}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
.chip-now{{font-size:11px;font-weight:800;letter-spacing:1px;background:{GOLD};color:{NAVY};padding:3px 9px;border-radius:99px;margin-top:-4px;}}

/* Fiche */
.card{{background:#fff;border-radius:28px;padding:28px;box-shadow:0 10px 26px rgba(20,33,61,.08);border:1.5px solid #E3E8F3;}}
.hero{{display:flex;flex-direction:column;align-items:center;text-align:center;background:radial-gradient(circle at 50% 30%,var(--glow) 0%,#fff 62%);}}
.hero .n{{font-size:13px;font-weight:800;letter-spacing:2px;color:{MUTE};text-transform:uppercase;margin-top:14px;}}
.hero h2{{font-size:30px;font-weight:800;color:{NAVY};margin:4px 0 2px;}}
.hero .t{{font-size:17px;font-weight:700;color:{BLUE};}}
.hero p{{color:{MUTE};font-size:15px;line-height:1.5;margin:12px 0 0;}}
.rewards{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:18px;}}
.rw{{display:flex;align-items:center;gap:8px;background:{SOFT};border-radius:16px;padding:9px 14px;font-weight:800;color:{NAVY};font-size:14.5px;}}
.rw .ms{{font-size:22px;color:{BLUE};}}
.rw.xp .ms{{color:#F59E0B;}}
.status{{margin-top:16px;font-weight:800;font-size:14px;padding:7px 14px;border-radius:99px;}}
.status.done{{background:#DCFCE7;color:#166534;}}
.status.current{{background:#FFF3C4;color:#8A5A00;}}
.status.locked{{background:{SOFT};color:{MUTE};}}
.m-h{{display:flex;align-items:center;gap:10px;font-size:20px;font-weight:800;color:{NAVY};margin:0 0 6px;}}
.m-h .ms{{color:{BLUE};font-size:26px;}}
.m-p{{color:{MUTE};font-size:15px;margin:0 0 14px;}}

/* Mission */
.st-key-mission{{background:#fff!important;border-radius:28px!important;padding:28px!important;box-shadow:0 10px 26px rgba(20,33,61,.08);border:1.5px solid #E3E8F3!important;}}
.st-key-mission [data-testid="stSlider"] label p,.st-key-mission [data-testid="stSelectbox"] label p{{font-weight:800!important;color:{NAVY}!important;font-size:15px!important;}}
.st-key-mission [data-testid="stSlider"] [role="slider"]{{width:22px!important;height:22px!important;background:#fff!important;border:5px solid {BLUE}!important;box-shadow:0 2px 6px rgba(31,43,224,.35)!important;}}
.st-key-mission [data-testid="stSlider"] [data-testid="stSliderThumbValue"]{{color:{BLUE}!important;font-weight:800!important;}}
.st-key-mission [data-baseweb="slider"] > div > div > div:first-child{{background:{BLUE}!important;}}
.st-key-mission [data-testid="stSelectbox"] [data-baseweb="select"] > div{{border-radius:14px!important;background:{SOFT}!important;border-color:transparent!important;min-height:48px;}}
.st-key-mission div[role="radiogroup"]{{gap:10px!important;flex-direction:column!important;}}
.st-key-mission div[role="radiogroup"] > div,.st-key-mission div[role="radiogroup"] label{{width:100%!important;}}
.st-key-mission div[role="radiogroup"] label{{background:#fff;border:2px solid #DCE2EF;border-radius:16px;padding:13px 16px!important;margin:0!important;cursor:pointer;transition:all .12s;}}
.st-key-mission div[role="radiogroup"] label:hover{{border-color:{BLUE};}}
.st-key-mission div[role="radiogroup"] label:has(input:checked){{background:#E4E2FB;border-color:{BLUE};}}
.st-key-mission div[role="radiogroup"] label p{{font-size:15.5px!important;color:{NAVY}!important;font-weight:600;}}
.st-key-mission [data-testid="stRadioOption"] > div > div:first-child{{border:2px solid #9AA5BD!important;background:#fff!important;width:20px!important;height:20px!important;}}
.st-key-mission [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child{{border:6px solid {BLUE}!important;}}
.st-key-mission [data-testid="stRadioOption"] > div > div:first-child > div{{display:none!important;}}
.st-key-mission .stButton button{{width:100%;min-height:58px!important;border-radius:99px!important;border:none!important;background:{NAVY}!important;
  box-shadow:0 7px 0 #0A1226!important;transition:transform .1s;margin-top:8px;}}
.st-key-mission .stButton button p{{color:#fff!important;font-size:17px!important;font-weight:800!important;}}
.st-key-mission .stButton button:active{{transform:translateY(6px);box-shadow:0 1px 0 #0A1226!important;}}
.st-key-mission .stButton button:disabled{{opacity:.45;}}

/* Résultat du simulateur */
.res{{display:flex;gap:22px;align-items:center;flex-wrap:wrap;background:linear-gradient(135deg,{NAVY},#26365F);border-radius:22px;padding:20px 24px;margin:6px 0 4px;}}
.res .big{{font-size:44px;font-weight:800;color:{GOLD};line-height:1;}}
.res .lab{{color:#C9D1F5;font-weight:700;font-size:13.5px;margin-bottom:6px;}}
.res .cost{{display:inline-block;margin-top:8px;background:rgba(255,255,255,.12);color:#FFD6D6;font-weight:700;font-size:13px;padding:4px 10px;border-radius:99px;}}
.gauge{{flex:1;min-width:260px;}}
.cells{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;}}
.cells i{{height:26px;border-radius:8px;background:rgba(255,255,255,.12);}}
.cells i.on{{background:var(--g);box-shadow:0 0 10px var(--g);}}
.scale{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-top:6px;color:#93A3C8;font-size:12px;font-weight:700;text-align:center;}}
.verdict{{color:#fff;font-weight:700;font-size:14.5px;margin-top:10px;}}

/* Règle 50/30/20 (affichée après la réponse) */
.rule{{display:flex;height:54px;border-radius:16px;overflow:hidden;margin-top:14px;font-weight:800;color:#fff;font-size:14px;}}
.rule div{{display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.2;}}
.feedback{{border-radius:16px;padding:12px 16px;font-size:15px;margin-top:12px;}}
.feedback.ko{{background:#FDE2E2;color:#7F1D1D;}}
.feedback.ok{{background:#DCFCE7;color:#14532D;}}
.locked-msg{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;min-height:260px;color:{MUTE};}}
.locked-msg .ms{{font-size:56px;color:#AEB6C8;}}

/* Fenêtre badge débloqué */
.unlock{{display:flex;flex-direction:column;align-items:center;text-align:center;padding:6px 0 4px;position:relative;}}
.rays{{position:absolute;top:-10px;width:260px;height:260px;border-radius:50%;
  background:repeating-conic-gradient(rgba(255,200,61,.28) 0 12deg,transparent 12deg 30deg);animation:spin 9s linear infinite;
  -webkit-mask:radial-gradient(circle,#000 35%,transparent 70%);mask:radial-gradient(circle,#000 35%,transparent 70%);}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.pop{{animation:pop .8s cubic-bezier(.2,1.6,.4,1) both;margin-top:30px;position:relative;}}
@keyframes pop{{0%{{transform:scale(.2) rotate(-25deg);opacity:0}}100%{{transform:none;opacity:1}}}}
.unlock h3{{font-size:26px;font-weight:800;color:{NAVY};margin:22px 0 4px;}}
.unlock p{{color:{MUTE};margin:0;font-size:15px;}}
.unlock .gain{{margin-top:14px;font-weight:800;color:{NAVY};background:#FFF3C4;padding:8px 16px;border-radius:99px;}}
.st-key-dialog_btn .stButton button{{min-height:52px!important;border-radius:99px!important;background:{NAVY}!important;border:none!important;box-shadow:0 6px 0 #0A1226!important;}}
.st-key-dialog_btn .stButton button p{{color:#fff!important;font-weight:800!important;font-size:16px!important;}}
@media (max-width:900px){{.st-key-map:before,.st-key-map:after{{display:none;}}}}
</style>
"""
st.markdown("\n".join(l for l in CSS.splitlines() if l.strip()), unsafe_allow_html=True)


def html(s: str) -> None:
    st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


def badge(n: int, size: int, state: str) -> str:
    S = STEPS[n]
    pin = {"done": '<div class="pin"><span class="ms">check</span></div>',
           "locked": '<div class="pin"><span class="ms">lock</span></div>'}.get(state, "")
    return (f'<div class="bdg {state}" style="--s:{size}px;--c1:{S["c1"]};--c2:{S["c2"]}">'
            f'<div class="hex o"></div><div class="hex i"><span class="ms">{S["icon"]}</span></div>{pin}</div>')


# ---------------------------------------------------------------------------
# Validation + fenêtre « badge débloqué »
# ---------------------------------------------------------------------------
def give(n: int) -> None:
    S = STEPS[n]
    user["xp_points"] = int(user.get("xp_points", 0) or 0) + S["xp"]
    badges = list(user.get("badges", []))
    if S["badge"] not in badges:
        badges.append(S["badge"])
    user["badges"] = badges


def validate(n: int) -> None:
    if n != done + 1:
        return
    ss.courant_etape = n
    user["courant_level"] = n
    give(n)
    unlocked = [n]
    if n == N_GAMES:          # parcours terminé : récompense finale
        give(3)
        unlocked.append(3)
    ss["user"] = user
    ss.courant_sel = min(n + 1, N_GAMES)
    ss["courant_unlocked"] = unlocked
    st.rerun()


def _unlock_body(ns: list) -> None:
    for n in ns:
        S = STEPS[n]
        html(f"""<div class="unlock"><div class="rays"></div><div class="pop">{badge(n, 140, "current")}</div>
<h3>{S["badge"]}</h3><p>{"Parcours Épargner &amp; Budget terminé !" if n == 3 else S["name"] + " validé"}</p>
<div class="gain">+{S["xp"]} XP</div></div>""")
    with st.container(key="dialog_btn"):
        if st.button("Continuer", key="close_dialog", use_container_width=True):
            ss.pop("courant_unlocked", None)
            st.rerun()


show_unlock = st.dialog("Badge débloqué !")(_unlock_body) if hasattr(st, "dialog") else _unlock_body
if ss.get("courant_unlocked"):
    show_unlock(ss["courant_unlocked"])

# ---------------------------------------------------------------------------
# En-tête
# ---------------------------------------------------------------------------
nb_badges = done + (1 if done >= N_GAMES else 0)
html(f"""<div class="p-head"><div>
<div class="p-kick">Parcours 1</div><div class="p-title">Épargner &amp; maîtriser son budget</div>
<p class="p-sub">Deux mini-jeux pour construire ton matelas de sécurité et mieux répartir ton argent.</p></div>
<div class="hud">
<div><span class="ms" style="color:{BLUE}">military_tech</span><span><b>{nb_badges} / 3</b><small>badges</small></span></div>
<div><span class="ms" style="color:#F59E0B">bolt</span><span><b>{int(user.get("xp_points", 0) or 0)}</b><small>XP</small></span></div>
</div></div>""")

# ---------------------------------------------------------------------------
# Carte de progression
# ---------------------------------------------------------------------------
with st.container(key="map"):
    cols = st.columns(3)
    for n, col in zip(STEPS, cols):
        stt = state_of(n)
        with col:
            now = '<div class="chip-now">EN COURS</div>' if stt == "current" else ""
            lvl = "Récompense" if n == 3 else f"Étape {n}"
            html(f'<div class="node {stt}">{badge(n, 92, stt)}{now}<div class="lvl">{lvl}</div></div>')
            if st.button(STEPS[n]["name"], key=f"step_{n}", disabled=stt == "locked" or n == 3,
                         type="primary" if ss.courant_sel == n else "secondary"):
                ss.courant_sel = n
                st.rerun()

st.write("")

# ---------------------------------------------------------------------------
# Fiche + mission
# ---------------------------------------------------------------------------
sel = ss.courant_sel
S = STEPS[sel]
stt = state_of(sel)
status_txt = {"done": "✓ Étape validée", "current": "Mission en cours", "locked": "Verrouillé"}[stt]

left, right = st.columns([1, 1.7], gap="medium")
with left:
    html(f"""<div class="card hero" style="--glow:{S["c1"]}33">
{badge(sel, 150, stt)}
<div class="n">Étape {sel}</div><h2>{S["name"]}</h2><div class="t">{S["title"]}</div>
<p>{S["objectif"]}</p>
<div class="rewards">
<div class="rw xp"><span class="ms">bolt</span>+{S["xp"]} XP</div>
<div class="rw"><span class="ms">military_tech</span>{S["badge"]}</div>
</div><div class="status {stt}">{status_txt}</div></div>""")

with right:
    with st.container(key="mission"):
        if stt == "locked":
            html(f'<div class="locked-msg"><span class="ms">lock</span><p>Termine l\'étape {done + 1} pour débloquer celle-ci.</p></div>')

        # ---------------- Étape 1 : simulateur ----------------
        elif sel == 1:
            html('<div class="m-h"><span class="ms">sports_esports</span>Le simulateur</div>'
                 '<p class="m-p">Règle tes curseurs, choisis un coup dur et regarde combien de mois ton matelas tient.</p>')
            c1, c2 = st.columns(2)
            with c1:
                dep = st.slider("Dépenses mensuelles incompressibles (€)", 200, 2500, 700, 50, key="sim_dep")
            with c2:
                ep = st.slider("Épargne de sécurité actuelle (€)", 0, 15000, 3500, 100, key="sim_ep")
            scen = st.selectbox("Le coup dur à tester", list(SCENARIOS), index=1, key="sim_scen")
            cost = SCENARIOS[scen](dep)
            reste = ep - cost
            mois = max(reste, 0) / max(dep, 1)
            on = min(6, int(mois))
            if mois >= 3:
                g, verdict = "#22C55E", "Solide : ton matelas encaisse le choc et il te reste de la marge."
            elif mois >= 1:
                g, verdict = GOLD, "Ça passe, mais ton matelas devient fin. Vise au moins 3 mois de dépenses."
            else:
                g, verdict = "#EF4444", "Aïe : l'imprévu dépasse ton épargne. Priorité : reconstituer un matelas."
            cells = "".join(f'<i class="{"on" if k < on else ""}"></i>' for k in range(6))
            scale = "".join(f"<span>{k + 1} m</span>" for k in range(6))
            html(f"""<div class="res" style="--g:{g}">
<div><div class="lab">Matelas restant</div><div class="big">{mois:.1f} mois</div>
<div class="cost">−{cost:,.0f} € absorbés</div></div>
<div class="gauge"><div class="cells">{cells}</div><div class="scale">{scale}</div>
<div class="verdict">{verdict}</div></div></div>""".replace(",", " "))
            label = "Rejouer" if stt == "done" else "Valider l'étape 1 et obtenir le badge"
            if st.button(label, key="val_1", icon=":material/emoji_events:", use_container_width=True) and stt == "current":
                validate(1)

        # ---------------- Étape 2 : quiz ----------------
        elif sel == 2:
            html('<div class="m-h"><span class="ms">quiz</span>Le défi</div>'
                 '<p class="m-p">La règle 50/30/20 aide à répartir ses revenus en trois parts. Saurais-tu dire à quoi sert chacune ?</p>')
            html(f'<div style="font-size:17px;font-weight:800;color:{NAVY};margin:4px 0 10px">Dans la règle 50/30/20, à quoi correspondent les 20 % ?</div>')
            opts = ["Les dépenses de loisirs et sorties", "L'épargne et les investissements", "Le loyer et les factures"]
            choice = st.radio("Réponse", range(3), format_func=lambda i: opts[i], index=None, key="quiz_5030", label_visibility="collapsed")
            label = "Rejouer le défi" if stt == "done" else "Valider ma réponse"
            if st.button(label, key="val_2", disabled=choice is None, icon=":material/sports_esports:", use_container_width=True):
                if choice == 1:
                    if stt == "current":
                        validate(2)
                    html('<div class="feedback ok"><b>Bonne réponse !</b> Les 20 % vont à l\'épargne et aux investissements.</div>')
                else:
                    html('<div class="feedback ko"><b>Pas tout à fait.</b> Pense à la part qui sert à préparer l\'avenir, et retente ta chance.</div>')
            if stt == "done":
                html(f"""<div class="rule">
<div style="width:50%;background:{BLUE}">50 %<br>Besoins</div>
<div style="width:30%;background:#8B5CF6">30 %<br>Envies</div>
<div style="width:20%;background:#22C55E">20 %<br>Épargne</div></div>""")

st.write("")
st.page_link("pages/7_Dashboard.py", label="Retour au Dashboard & mes badges", icon=":material/dashboard:")
