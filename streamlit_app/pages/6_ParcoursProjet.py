"""Parcours 3 : Projets & aides financières — cartes d'aides à collectionner."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Parcours 3 — Projets & aides", page_icon="🎓", layout="wide")
ss = st.session_state

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in ss or not ss["user"]:
    ss["user"] = api_service.login("demo", "demo123").get("user", {})
user = ss["user"]

PHOTO = "https://images.unsplash.com/photo-{}?w=900&q=75&auto=format&fit=crop"

# ---------------------------------------------------------------------------
# Les aides à collectionner (+ la récompense finale)
# ---------------------------------------------------------------------------
STEPS = {
    1: {"name": "Prêt étudiant", "title": "Garanti par l'État", "icon": "school", "c1": "#8B5CF6", "c2": "#6D28D9",
        "photo": "1623461487986-9400110de28e", "tag": "Sans caution parentale",
        "badge": "Étudiant financé", "xp": 40,
        "objectif": "Emprunter pour tes études sans caution personnelle ni garant familial.",
        "how": [("verified_user", "C'est l'État (via Bpifrance) qui se porte garant à la place de tes parents."),
                ("payments", "Jusqu'à 20 000 €, sans condition de ressources, dans les banques partenaires."),
                ("person", "Pour les étudiants de moins de 28 ans.")],
        "q": "Pour ce prêt, as-tu besoin d'un parent qui se porte garant ?",
        "opts": ["Oui, c'est obligatoire", "Non, c'est l'État qui garantit le prêt", "Seulement si tu as plus de 25 ans"], "ok": 1},
    2: {"name": "Permis à 1 €/jour", "title": "Prêt à taux zéro", "icon": "directions_car", "c1": "#3B82F6", "c2": "#1D4ED8",
        "photo": "1498887960847-2a5e46312788", "tag": "0 % d'intérêt",
        "badge": "Pilote malin", "xp": 40,
        "objectif": "Financer ton permis B sans payer d'intérêts.",
        "how": [("account_balance", "L'État prend en charge les intérêts : tu ne rembourses que la somme empruntée."),
                ("calendar_month", "Environ 30 € par mois, soit à peu près 1 € par jour."),
                ("person", "Pour les jeunes de 15 à 25 ans, via une auto-école partenaire.")],
        "q": "Qui paie les intérêts du prêt « Permis à 1 € par jour » ?",
        "opts": ["Toi, chaque mois", "L'État", "L'auto-école"], "ok": 1},
    3: {"name": "Prime de bienvenue", "title": "Et mobilité bancaire", "icon": "redeem", "c1": "#F97316", "c2": "#C2410C",
        "photo": "1633158829875-e5316a358c6f", "tag": "Jusqu'à 150 € offerts",
        "badge": "Chasseur de primes", "xp": 40,
        "objectif": "Profiter de l'offre Yello à l'ouverture et changer de banque sans effort.",
        "how": [("card_giftcard", "Une prime à l'ouverture de ton compte Yello, selon les conditions de l'offre."),
                ("sync_alt", "Avec la mobilité bancaire, ta nouvelle banque transfère tes virements et prélèvements."),
                ("money_off", "Ce service de transfert est gratuit.")],
        "q": "En changeant de banque, qui s'occupe de transférer tes prélèvements ?",
        "opts": ["Toi, un par un", "Ta nouvelle banque, gratuitement", "Ton employeur"], "ok": 1},
    4: {"name": "Frais à l'étranger", "title": "Stages et séjours", "icon": "flight_takeoff", "c1": "#14B8A6", "c2": "#0F766E",
        "photo": "1502301197179-65228ab57f78", "tag": "0 € de commission",
        "badge": "Globe-trotter", "xp": 40,
        "objectif": "Payer et retirer à l'étranger sans te faire grignoter par les frais.",
        "how": [("euro", "Dans la zone euro, payer en euros ne doit pas coûter plus cher qu'en France."),
                ("currency_exchange", "Hors zone euro, les banques facturent souvent une commission de change."),
                ("credit_card", "Avec Yello : 0 € de commission sur tes paiements et retraits à l'étranger.")],
        "q": "Payer en euros en Espagne avec ta carte, ça coûte…",
        "opts": ["Plus cher qu'en France", "Pareil qu'en France", "Toujours 3 % de frais"], "ok": 1},
    5: {"name": "Bilan d'aides", "title": "Parcours terminé", "icon": "workspace_premium", "c1": "#FFC83D", "c2": "#14213D",
        "photo": "1632650312771-52c324fb4d83", "tag": "Badge final",
        "badge": "Expert des aides", "xp": 100,
        "objectif": "Tu connais les aides et avantages qui peuvent financer tes projets."},
}
AIDS = [1, 2, 3, 4]

ss.setdefault("projet_collected", list(user.get("projet_collected", [])))
ss.setdefault("projet_bilan", bool(user.get("projet_bilan", False)))
ss.setdefault("projet_sel", next((n for n in AIDS if n not in ss.projet_collected), 5))
collected = ss.projet_collected


def state_of(n: int) -> str:
    if n == 5:
        return "done" if ss.projet_bilan else ("open" if len(collected) == len(AIDS) else "locked")
    return "done" if n in collected else "open"


NAVY, BLUE, GOLD, SOFT, MUTE = "#14213D", "#1F2BE0", "#FFC83D", "#EEF1F8", "#5B6785"
track_pct = max(0, len(collected) + (1 if ss.projet_bilan else 0) - 1) / 4 * 100
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
.st-key-map:before{{content:"";position:absolute;left:10%;right:10%;top:88px;height:10px;border-radius:99px;background:rgba(255,255,255,.12);}}
.st-key-map:after{{content:"";position:absolute;left:10%;top:88px;height:10px;border-radius:99px;width:calc(80% * {track_pct / 100:.3f});
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
.bdg.open{{}}
.bdg.current{{animation:float 2.6s ease-in-out infinite;filter:drop-shadow(0 0 18px rgba(255,200,61,.75));}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
.chip-now{{font-size:11px;font-weight:800;letter-spacing:1px;background:{GOLD};color:{NAVY};padding:3px 9px;border-radius:99px;margin-top:-4px;}}

/* Fiche */
.card{{background:#fff;border-radius:28px;padding:28px;box-shadow:0 10px 26px rgba(20,33,61,.08);border:1.5px solid #E3E8F3;}}
.photo{{width:calc(100% + 56px);margin:-28px -28px 0;height:190px;background-size:cover;background-position:center;border-radius:28px 28px 0 0;position:relative;}}
.photo:after{{content:"";position:absolute;inset:0;border-radius:28px 28px 0 0;background:linear-gradient(180deg,rgba(20,33,61,0) 40%,rgba(20,33,61,.55));}}
.hero .bdg{{margin-top:-70px;z-index:2;}}
.how{{display:grid;gap:10px;margin-bottom:20px;}}
.how div{{display:flex;gap:12px;align-items:flex-start;background:{SOFT};border-radius:16px;padding:13px 15px;color:{NAVY};font-size:15px;line-height:1.45;}}
.how .ms{{color:{BLUE};font-size:24px;}}
.tagline{{display:inline-block;margin-top:10px;background:#FFF3C4;color:#8A5A00;font-weight:800;font-size:13.5px;padding:5px 12px;border-radius:99px;}}
.recap{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:14px;}}
.recap div{{background:{SOFT};border-radius:16px;padding:14px;display:flex;gap:10px;align-items:center;font-weight:700;color:{NAVY};font-size:15px;}}
.recap .ms{{color:#22C55E;font-size:26px;}}
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


def give(n: int) -> None:
    S = STEPS[n]
    user["xp_points"] = int(user.get("xp_points", 0) or 0) + S["xp"]
    badges = list(user.get("badges", []))
    if S["badge"] not in badges:
        badges.append(S["badge"])
    user["badges"] = badges


# ---------------------------------------------------------------------------
# Fenêtre « badge débloqué »
# ---------------------------------------------------------------------------
def _unlock_body(n: int) -> None:
    S = STEPS[n]
    sub = "Parcours Projets &amp; aides terminé !" if n == 5 else f"Carte « {S['name']} » ajoutée à ta collection"
    html(f"""<div class="unlock"><div class="rays"></div><div class="pop">{badge(n, 140, "current")}</div>
<h3>{S["badge"]}</h3><p>{sub}</p><div class="gain">+{S["xp"]} XP</div></div>""")
    with st.container(key="dialog_btn"):
        if st.button("Continuer", key="close_dialog", use_container_width=True):
            ss.pop("projet_unlocked", None)
            st.rerun()


show_unlock = st.dialog("Badge débloqué !")(_unlock_body) if hasattr(st, "dialog") else _unlock_body
if ss.get("projet_unlocked"):
    show_unlock(ss["projet_unlocked"])

# ---------------------------------------------------------------------------
# En-tête
# ---------------------------------------------------------------------------
nb_badges = len(collected) + (1 if ss.projet_bilan else 0)
html(f"""<div class="p-head"><div>
<div class="p-kick">Parcours 3</div><div class="p-title">Projets &amp; aides financières</div>
<p class="p-sub">Collectionne les 4 cartes d'aides pour financer tes projets, puis valide ton bilan.</p></div>
<div class="hud">
<div><span class="ms" style="color:{BLUE}">style</span><span><b>{len(collected)} / 4</b><small>cartes</small></span></div>
<div><span class="ms" style="color:#F59E0B">bolt</span><span><b>{int(user.get("xp_points", 0) or 0)}</b><small>XP</small></span></div>
</div></div>""")

# ---------------------------------------------------------------------------
# Carte de progression
# ---------------------------------------------------------------------------
with st.container(key="map"):
    cols = st.columns(5)
    for n, col in zip(STEPS, cols):
        stt = state_of(n)
        shown = "current" if (ss.projet_sel == n and stt == "open") else stt
        with col:
            lvl = "Récompense" if n == 5 else f"Carte {n}"
            html(f'<div class="node {shown}">{badge(n, 86, shown)}<div class="lvl">{lvl}</div></div>')
            if st.button(STEPS[n]["name"], key=f"step_{n}", disabled=stt == "locked",
                         type="primary" if ss.projet_sel == n else "secondary"):
                ss.projet_sel = n
                st.rerun()

st.write("")

# ---------------------------------------------------------------------------
# Fiche + mission
# ---------------------------------------------------------------------------
sel = ss.projet_sel
S = STEPS[sel]
stt = state_of(sel)
status_txt = {"done": "✓ Carte collectionnée" if sel != 5 else "✓ Bilan validé",
              "open": "À débloquer", "locked": "Verrouillé"}[stt]
status_cls = {"done": "done", "open": "current", "locked": "locked"}[stt]

left, right = st.columns([1, 1.7], gap="medium")
with left:
    html(f"""<div class="card hero" style="--glow:{S["c1"]}26">
<div class="photo" style="background-image:url('{PHOTO.format(S["photo"])}'),linear-gradient(135deg,{S["c1"]},{S["c2"]})"></div>
{badge(sel, 120, "done" if stt == "done" else ("locked" if stt == "locked" else "open"))}
<div class="n">{"Récompense" if sel == 5 else f"Carte {sel}"}</div><h2>{S["name"]}</h2><div class="t">{S["title"]}</div>
<div class="tagline">{S["tag"]}</div>
<p>{S["objectif"]}</p>
<div class="rewards">
<div class="rw xp"><span class="ms">bolt</span>+{S["xp"]} XP</div>
<div class="rw"><span class="ms">military_tech</span>{S["badge"]}</div>
</div><div class="status {status_cls}">{status_txt}</div></div>""")

with right:
    with st.container(key="mission"):
        if sel == 5:
            if stt == "locked":
                html(f'<div class="locked-msg"><span class="ms">lock</span><p>Collectionne les 4 cartes d\'aides pour valider ton bilan ({len(collected)} / 4).</p></div>')
            else:
                html('<div class="m-h"><span class="ms">fact_check</span>Ton bilan d\'aides</div>'
                     '<p class="m-p">Voici les dispositifs que tu sais maintenant mobiliser pour tes projets.</p>')
                html('<div class="recap">' + "".join(
                    f'<div><span class="ms">check_circle</span>{STEPS[n]["name"]}</div>' for n in AIDS) + "</div>")
                if not ss.projet_bilan:
                    if st.button("Valider mon bilan d'aides et obtenir le badge", key="val_bilan",
                                 icon=":material/emoji_events:", use_container_width=True):
                        ss.projet_bilan = True
                        user["projet_bilan"] = True
                        give(5)
                        ss["user"] = user
                        ss["projet_unlocked"] = 5
                        st.rerun()
                else:
                    html('<div class="feedback ok"><b>Bilan validé !</b> Tu as terminé le parcours Projets &amp; aides.</div>')
        else:
            html('<div class="m-h"><span class="ms">lightbulb</span>Comment ça marche</div>')
            html('<div class="how">' + "".join(
                f'<div><span class="ms">{ic}</span><span>{t}</span></div>' for ic, t in S["how"]) + "</div>")
            html('<div class="m-h"><span class="ms">quiz</span>Pour débloquer la carte</div>')
            html(f'<div style="font-size:17px;font-weight:800;color:{NAVY};margin:4px 0 10px">{S["q"]}</div>')
            choice = st.radio("Réponse", range(len(S["opts"])), format_func=lambda i: S["opts"][i],
                              index=None, key=f"q_projet_{sel}", label_visibility="collapsed")
            label = "Rejouer" if stt == "done" else "Débloquer cette carte"
            if st.button(label, key=f"val_{sel}", disabled=choice is None, icon=":material/style:", use_container_width=True):
                if choice == S["ok"]:
                    if stt != "done":
                        ss.projet_collected = collected + [sel]
                        user["projet_collected"] = ss.projet_collected
                        give(sel)
                        ss["user"] = user
                        ss.projet_sel = next((n for n in AIDS if n not in ss.projet_collected), 5)
                        ss["projet_unlocked"] = sel
                        st.rerun()
                    html('<div class="feedback ok"><b>Bonne réponse !</b></div>')
                else:
                    html('<div class="feedback ko"><b>Pas tout à fait.</b> Relis « Comment ça marche » et retente ta chance.</div>')

st.write("")
st.page_link("pages/7_Dashboard.py", label="Retour au Dashboard & mes badges", icon=":material/dashboard:")
html('<p style="text-align:center;color:#5B6785;font-size:12.5px;margin-top:10px">Conditions des aides publiques susceptibles d\'évoluer : vérifie toujours sur les sites officiels.</p>')
