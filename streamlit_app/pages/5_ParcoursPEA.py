"""Parcours 2 : Investir & découvrir le PEA — carte de progression en 6 niveaux."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Parcours 2 — Investir", page_icon="📈", layout="wide")
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
# Les 6 niveaux
# ---------------------------------------------------------------------------
LEVELS = {
    1: {"name": "L'Explorateur", "title": "Découvrir l'investissement", "icon": "explore", "c1": "#22C55E", "c2": "#15803D",
        "badge": "Premiers pas en Bourse", "xp": 50,
        "objectif": "Démystifier les marchés financiers et comprendre les mécanismes de base.",
        "lessons": [("Une action", "C'est une petite part d'une entreprise. Si l'entreprise grandit, ta part peut prendre de la valeur."),
                    ("Une obligation", "C'est un prêt que tu fais à une entreprise ou à un État, contre des intérêts."),
                    ("Risque et rendement", "Plus on vise un gain élevé, plus le risque de perte est grand. Les deux vont ensemble.")],
        "q": "Acheter une action, c'est…",
        "opts": ["Prêter de l'argent à l'État", "Devenir copropriétaire d'une petite part d'une entreprise", "Ouvrir un livret d'épargne"],
        "ok": 1, "why": "Une action représente une part du capital d'une entreprise : tu en deviens un tout petit propriétaire."},
    2: {"name": "Le Stratège", "title": "Diversifier ses placements", "icon": "lightbulb", "c1": "#3B82F6", "c2": "#1D4ED8",
        "badge": "Stratège diversifié", "xp": 75,
        "objectif": "Comprendre pourquoi on répartit son argent entre beaucoup d'entreprises.",
        "lessons": [("Ne pas tout miser au même endroit", "Si une entreprise chute, les autres limitent la casse."),
                    ("L'ETF", "Un fonds qui suit un indice (ex. MSCI World) : des centaines d'entreprises en un seul achat."),
                    ("Le temps", "Sur une longue durée, les hauts et les bas ont tendance à se lisser.")],
        "q": "Un ETF, c'est…",
        "opts": ["Une seule action très risquée", "Un fonds qui réplique un indice composé de nombreuses entreprises", "Un compte épargne garanti"],
        "ok": 1, "why": "Un ETF suit un indice : en un achat, tu es exposé à beaucoup d'entreprises à la fois."},
    3: {"name": "Le Gestionnaire", "title": "Investir avec régularité", "icon": "account_balance_wallet", "c1": "#8B5CF6", "c2": "#6D28D9",
        "badge": "Investisseur régulier", "xp": 100,
        "objectif": "Mettre en place de bonnes habitudes : petites sommes, régulièrement, sans paniquer.",
        "lessons": [("L'investissement programmé", "Investir la même somme chaque mois, quel que soit le marché."),
                    ("Les frais", "Même 1 % de frais par an pèse lourd sur 20 ans. Compare toujours."),
                    ("Garder son calme", "Vendre dans la panique après une baisse, c'est transformer une perte temporaire en perte réelle.")],
        "q": "Investir 50 € chaque mois, quel que soit l'état du marché, s'appelle…",
        "opts": ["Le market timing", "L'investissement programmé", "La spéculation"],
        "ok": 1, "why": "C'est l'investissement programmé : il évite de devoir deviner le « bon moment »."},
    4: {"name": "Virtuel 10 k€", "title": "S'entraîner sans risque", "icon": "monitoring", "c1": "#F59E0B", "c2": "#B45309",
        "badge": "Trader virtuel", "xp": 125,
        "objectif": "Gérer un portefeuille fictif de 10 000 € pour vivre les variations sans rien perdre.",
        "lessons": [("10 000 € fictifs", "Tu composes ton portefeuille avec de l'argent virtuel."),
                    ("Observer", "Tu vois ton portefeuille monter et baisser, comme en vrai."),
                    ("Comparer", "Compare tes choix avec un simple ETF monde : c'est souvent instructif.")],
        "q": "Ton portefeuille virtuel baisse de 8 % en un mois. Le réflexe le plus raisonnable ?",
        "opts": ["Tout vendre immédiatement", "Garder le cap si ton horizon est long et ton portefeuille diversifié", "Emprunter pour racheter davantage"],
        "ok": 1, "why": "Les baisses font partie du jeu. Avec un horizon long et de la diversification, on évite de vendre dans la panique."},
    5: {"name": "Ouverture PEA", "title": "Comprendre le PEA", "icon": "account_balance", "c1": "#F97316", "c2": "#C2410C",
        "badge": "Détenteur de PEA", "xp": 150,
        "objectif": "Connaître les règles du Plan d'Épargne en Actions avant d'en ouvrir un.",
        "lessons": [("Le plafond", "Jusqu'à 150 000 € de versements sur un PEA classique, un seul PEA par personne."),
                    ("La règle des 5 ans", "Après 5 ans, les gains sont exonérés d'impôt sur le revenu (les prélèvements sociaux restent dus)."),
                    ("Retrait avant 5 ans", "En principe, un retrait avant 5 ans entraîne la clôture du plan, sauf cas particuliers.")],
        "q": "Quel est le principal avantage du PEA après 5 ans ?",
        "opts": ["Il n'y a plus aucun risque de perte", "Les gains sont exonérés d'impôt sur le revenu (hors prélèvements sociaux)", "Le rendement est garanti"],
        "ok": 1, "why": "Le PEA offre un avantage fiscal après 5 ans, mais le capital investi en actions reste exposé au risque."},
    6: {"name": "Yello Master", "title": "Maîtriser les bases", "icon": "workspace_premium", "c1": "#FFC83D", "c2": "#14213D",
        "badge": "Yello Master", "xp": 200,
        "objectif": "Valider tout ce que tu as appris et débloquer ton profil investisseur.",
        "lessons": [("Récapitulatif", "Actions, ETF, diversification, régularité, PEA : tu as toutes les bases."),
                    ("Ton profil", "Prudent, équilibré ou dynamique : il dépend de ton horizon et de ta tolérance au risque."),
                    ("Prochaine étape", "Ton profil investisseur te propose des entreprises qui collent à tes centres d'intérêt.")],
        "q": "Quelle affirmation est vraie ?",
        "opts": ["Une action peut perdre de la valeur", "Le PEA garantit le capital investi", "Diversifier augmente toujours le risque"],
        "ok": 0, "why": "Investir en actions comporte toujours un risque de perte, même dans un PEA."},
}
N = len(LEVELS)

ss.setdefault("pea_niveau", int(user.get("pea_level", 0) or 0))   # niveaux validés
ss.setdefault("pea_sel", min(ss.pea_niveau + 1, N))
done = ss.pea_niveau


def state_of(n: int) -> str:
    if n <= done:
        return "done"
    if n == done + 1:
        return "current"
    return "locked"


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
NAVY, BLUE, GOLD, SOFT, MUTE = "#14213D", "#1F2BE0", "#FFC83D", "#EEF1F8", "#5B6785"
track_pct = 0 if done == 0 else min(100, (done) / (N - 1) * 100)
CSS = f"""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL@24,500,1" rel="stylesheet">
<style>
.stApp{{background:#E6EBF5!important;}}
.block-container,[data-testid="stMainBlockContainer"]{{max-width:100%!important;width:100%!important;padding:1.6rem 3rem 3rem!important;}}
[data-testid="stMain"] p,[data-testid="stMain"] div,[data-testid="stMain"] button,[data-testid="stMain"] label{{font-family:'Plus Jakarta Sans',sans-serif;}}
.ms{{font-family:'Material Symbols Rounded'!important;font-weight:normal;font-style:normal;line-height:1;display:inline-block;
  -webkit-font-feature-settings:'liga';font-feature-settings:'liga';font-variation-settings:'FILL' 1;}}

/* En-tête */
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
.st-key-map:before{{content:"";position:absolute;left:8.3%;right:8.3%;top:88px;height:10px;border-radius:99px;background:rgba(255,255,255,.12);}}
.st-key-map:after{{content:"";position:absolute;left:8.3%;top:88px;height:10px;border-radius:99px;width:calc(83.4% * {track_pct / 100:.3f});
  background:linear-gradient(90deg,#22C55E,{GOLD});box-shadow:0 0 14px rgba(255,200,61,.6);}}
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

/* Fiche du niveau */
.card{{background:#fff;border-radius:28px;padding:28px;box-shadow:0 10px 26px rgba(20,33,61,.08);border:1.5px solid #E3E8F3;height:100%;}}
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

.m-h{{display:flex;align-items:center;gap:10px;font-size:20px;font-weight:800;color:{NAVY};margin:0 0 14px;}}
.m-h .ms{{color:{BLUE};font-size:26px;}}
.lessons{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:22px;}}
.lesson{{background:{SOFT};border-radius:18px;padding:16px;}}
.lesson .k{{width:30px;height:30px;border-radius:10px;background:{NAVY};color:{GOLD};font-weight:800;display:flex;align-items:center;justify-content:center;margin-bottom:10px;}}
.lesson b{{display:block;color:{NAVY};font-size:15.5px;margin-bottom:4px;}}
.lesson span{{color:{MUTE};font-size:14px;line-height:1.45;}}
.quiz-q{{font-size:17px;font-weight:800;color:{NAVY};margin:4px 0 10px;}}

/* Quiz */
.st-key-mission{{background:#fff!important;border-radius:28px!important;padding:28px!important;box-shadow:0 10px 26px rgba(20,33,61,.08);border:1.5px solid #E3E8F3!important;}}
.st-key-mission div[role="radiogroup"]{{gap:10px!important;flex-direction:column!important;}}
.st-key-mission div[role="radiogroup"] > div,.st-key-mission div[role="radiogroup"] label{{width:100%!important;}}
.st-key-mission div[role="radiogroup"] label{{background:#fff;border:2px solid #DCE2EF;border-radius:16px;padding:13px 16px!important;margin:0!important;cursor:pointer;transition:all .12s;}}
.st-key-mission div[role="radiogroup"] label:hover{{border-color:{BLUE};}}
.st-key-mission div[role="radiogroup"] label:has(input:checked){{background:#E4E2FB;border-color:{BLUE};}}
.st-key-mission div[role="radiogroup"] label p{{font-size:15.5px!important;color:{NAVY}!important;font-weight:600;}}
.st-key-mission .stButton button{{width:100%;min-height:58px!important;border-radius:99px!important;border:none!important;background:{NAVY}!important;
  box-shadow:0 7px 0 #0A1226!important;transition:transform .1s;margin-top:8px;}}
.st-key-mission .stButton button p{{color:#fff!important;font-size:17px!important;font-weight:800!important;}}
.st-key-mission .stButton button:active{{transform:translateY(6px);box-shadow:0 1px 0 #0A1226!important;}}
.st-key-mission .stButton button:disabled{{opacity:.45;}}
.st-key-cta .stButton button{{background:{GOLD}!important;box-shadow:0 7px 0 #B86E00!important;}}
.st-key-cta .stButton button p{{color:{NAVY}!important;}}
.st-key-mission [data-testid="stRadioOption"] > div > div:first-child{{border:2px solid #9AA5BD!important;background:#fff!important;width:20px!important;height:20px!important;}}
.st-key-mission [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child{{border:6px solid {BLUE}!important;}}
.st-key-mission [data-testid="stRadioOption"] > div > div:first-child > div{{display:none!important;}}
.st-key-mission_dialog .stButton button{{min-height:52px!important;border-radius:99px!important;background:{NAVY}!important;border:none!important;box-shadow:0 6px 0 #0A1226!important;}}
.st-key-mission_dialog .stButton button p{{color:#fff!important;font-weight:800!important;font-size:16px!important;}}
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
@media (max-width:900px){{.lessons{{grid-template-columns:1fr;}}.st-key-map:before,.st-key-map:after{{display:none;}}}}
</style>
"""
st.markdown("\n".join(l for l in CSS.splitlines() if l.strip()), unsafe_allow_html=True)


def html(s: str) -> None:
    st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


def badge(n: int, size: int, state: str) -> str:
    L = LEVELS[n]
    pin = {"done": '<div class="pin"><span class="ms">check</span></div>',
           "locked": '<div class="pin"><span class="ms">lock</span></div>'}.get(state, "")
    return (f'<div class="bdg {state}" style="--s:{size}px;--c1:{L["c1"]};--c2:{L["c2"]}">'
            f'<div class="hex o"></div><div class="hex i"><span class="ms">{L["icon"]}</span></div>{pin}</div>')


# ---------------------------------------------------------------------------
# Fenêtre « badge débloqué »
# ---------------------------------------------------------------------------
def _unlock_body(n: int) -> None:
    L = LEVELS[n]
    html(f"""<div class="unlock"><div class="rays"></div><div class="pop">{badge(n, 150, "current")}</div>
<h3>{L["badge"]}</h3><p>Niveau {n} · {L["name"]} validé</p><div class="gain">+{L["xp"]} XP</div></div>""")
    with st.container(key="mission_dialog"):
        if st.button("Continuer", key="close_dialog", use_container_width=True, type="primary"):
            ss.pop("pea_unlocked", None)
            st.rerun()


if hasattr(st, "dialog"):
    show_unlock = st.dialog("Badge débloqué !")(_unlock_body)
else:  # vieille version de Streamlit
    def show_unlock(n):
        _unlock_body(n)

if ss.get("pea_unlocked"):
    show_unlock(ss["pea_unlocked"])

# ---------------------------------------------------------------------------
# En-tête
# ---------------------------------------------------------------------------
xp_total = int(user.get("xp_points", 0) or 0)
html(f"""<div class="p-head"><div>
<div class="p-kick">Parcours 2</div><div class="p-title">Investir &amp; découvrir le PEA</div>
<p class="p-sub">6 niveaux pour apprendre à investir, sans jamais être poussé à prendre des risques.</p></div>
<div class="hud">
<div><span class="ms" style="color:{BLUE}">military_tech</span><span><b>{done} / {N}</b><small>badges</small></span></div>
<div><span class="ms" style="color:#F59E0B">bolt</span><span><b>{xp_total}</b><small>XP</small></span></div>
</div></div>""")

# ---------------------------------------------------------------------------
# Carte des niveaux
# ---------------------------------------------------------------------------
with st.container(key="map"):
    cols = st.columns(N)
    for n, col in zip(LEVELS, cols):
        stt = state_of(n)
        with col:
            now = '<div class="chip-now">EN COURS</div>' if stt == "current" else ""
            html(f'<div class="node {stt}">{badge(n, 92, stt)}{now}<div class="lvl">Niveau {n}</div></div>')
            if st.button(LEVELS[n]["name"], key=f"lvl_{n}", disabled=stt == "locked",
                         type="primary" if ss.pea_sel == n else "secondary"):
                ss.pea_sel = n
                st.rerun()

st.write("")

# ---------------------------------------------------------------------------
# Fiche du niveau sélectionné
# ---------------------------------------------------------------------------
sel = ss.pea_sel
L = LEVELS[sel]
stt = state_of(sel)
status_txt = {"done": "✓ Niveau validé", "current": "Mission en cours", "locked": "Verrouillé"}[stt]

left, right = st.columns([1, 1.7], gap="medium")
with left:
    html(f"""<div class="card hero" style="--glow:{L["c1"]}33">
{badge(sel, 150, "current" if stt == "current" else stt)}
<div class="n">Niveau {sel}</div><h2>{L["name"]}</h2><div class="t">{L["title"]}</div>
<p>{L["objectif"]}</p>
<div class="rewards">
<div class="rw xp"><span class="ms">bolt</span>+{L["xp"]} XP</div>
<div class="rw"><span class="ms">military_tech</span>{L["badge"]}</div>
</div><div class="status {stt}">{status_txt}</div></div>""")

with right:
    with st.container(key="mission"):
        if stt == "locked":
            html(f'<div class="locked-msg"><span class="ms">lock</span><p>Termine le niveau {done + 1} pour débloquer celui-ci.</p></div>')
        else:
            html('<div class="m-h"><span class="ms">school</span>Les leçons</div>')
            html('<div class="lessons">' + "".join(
                f'<div class="lesson"><div class="k">{i + 1}</div><b>{t}</b><span>{d}</span></div>'
                for i, (t, d) in enumerate(L["lessons"])) + "</div>")
            html('<div class="m-h"><span class="ms">quiz</span>Le défi</div>')
            html(f'<div class="quiz-q">{L["q"]}</div>')
            choice = st.radio("Réponse", range(len(L["opts"])), format_func=lambda i: L["opts"][i],
                              index=None, key=f"q_{sel}", label_visibility="collapsed")
            label = "Rejouer le défi" if stt == "done" else f"Valider le niveau {sel}"
            if st.button(label, key=f"validate_{sel}", disabled=choice is None,
                         icon=":material/sports_esports:", use_container_width=True):
                if choice == L["ok"]:
                    if stt == "current":
                        ss.pea_niveau = sel
                        user["pea_level"] = sel
                        user["xp_points"] = xp_total + L["xp"]
                        badges = list(user.get("badges", []))
                        if L["badge"] not in badges:
                            badges.append(L["badge"])
                        user["badges"] = badges
                        ss["user"] = user
                        ss.pea_sel = min(sel + 1, N)
                        ss["pea_unlocked"] = sel
                        st.rerun()
                    else:
                        html(f'<div class="feedback ok"><b>Bonne réponse !</b> {L["why"]}</div>')
                else:
                    html('<div class="feedback ko"><b>Pas tout à fait.</b> Relis les 3 leçons ci-dessus et retente ta chance.</div>')

            if done == N:
                with st.container(key="cta"):
                    if st.button("Débloquer mon profil investisseur", key="go_profil", icon=":material/rocket_launch:", use_container_width=True):
                        st.switch_page("pages/9_ProfilInvestisseur.py")

st.write("")
st.page_link("pages/7_Dashboard.py", label="Retour au Dashboard & mes badges", icon=":material/dashboard:")
html('<p style="text-align:center;color:#5B6785;font-size:12.5px;margin-top:10px">Contenu pédagogique, pas un conseil en investissement.</p>')
