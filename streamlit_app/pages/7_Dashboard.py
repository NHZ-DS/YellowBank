"""Tableau de bord global — progression, badges et prochaines étapes."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Tableau de bord — Yello", page_icon="📊", layout="wide")
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
# Données du joueur (lues depuis la session et l'utilisateur)
# ---------------------------------------------------------------------------
name = (user.get("full_name") or user.get("name")
        or " ".join(x for x in (user.get("first_name"), user.get("last_name")) if x)
        or user.get("username") or "Aventurier")
login = user.get("username", "")
initials = "".join(w[0] for w in name.split()[:2]).upper() or "Y"

xp = int(user.get("xp_points", 0) or 0)
XP_PAR_NIVEAU = 400
level = xp // XP_PAR_NIVEAU + 1
xp_in = xp % XP_PAR_NIVEAU
xp_pct = round(xp_in / XP_PAR_NIVEAU * 100)
RANGS = ["Apprenti", "Explorateur", "Stratège", "Gestionnaire", "Expert", "Yello Master"]
rang = RANGS[min(level - 1, len(RANGS) - 1)]

courant = int(ss.get("courant_etape", user.get("courant_level", 0)) or 0)            # 0..2
pea = int(ss.get("pea_niveau", user.get("pea_level", 0)) or 0)                       # 0..6
projet_cards = list(ss.get("projet_collected", user.get("projet_collected", [])) or [])  # 0..4 cartes
projet_bilan = bool(ss.get("projet_bilan", user.get("projet_bilan", False)))
earned = set(user.get("badges", []) or [])

# ---------------------------------------------------------------------------
# Catalogue des badges (mêmes noms, icônes et couleurs que dans les parcours)
# ---------------------------------------------------------------------------
CATALOGUE = [
    ("Épargner & budget", [
        ("Bouclier anti-imprévu", "shield", "#3B82F6", "#1D4ED8"),
        ("Maître du budget", "pie_chart", "#22C55E", "#15803D"),
        ("Gardien de l'épargne", "savings", "#FFC83D", "#14213D"),
    ]),
    ("Investir & PEA", [
        ("Premiers pas en Bourse", "explore", "#22C55E", "#15803D"),
        ("Stratège diversifié", "lightbulb", "#3B82F6", "#1D4ED8"),
        ("Investisseur régulier", "account_balance_wallet", "#8B5CF6", "#6D28D9"),
        ("Trader virtuel", "monitoring", "#F59E0B", "#B45309"),
        ("Détenteur de PEA", "account_balance", "#F97316", "#C2410C"),
        ("Yello Master", "workspace_premium", "#FFC83D", "#14213D"),
        ("Profil investisseur", "query_stats", "#1F2BE0", "#14213D"),
    ]),
    ("Projets & aides", [
        ("Étudiant financé", "school", "#8B5CF6", "#6D28D9"),
        ("Pilote malin", "directions_car", "#3B82F6", "#1D4ED8"),
        ("Chasseur de primes", "redeem", "#F97316", "#C2410C"),
        ("Globe-trotter", "flight_takeoff", "#14B8A6", "#0F766E"),
        ("Expert des aides", "verified", "#FFC83D", "#14213D"),
    ]),
]
known = {b[0] for _, group in CATALOGUE for b in group}
autres = sorted(earned - known)          # badges venus du backend (anciens noms, etc.)
if autres:
    CATALOGUE.append(("Autres distinctions", [(b, "military_tech", "#1F2BE0", "#14213D") for b in autres]))
total_badges = sum(len(g) for _, g in CATALOGUE)
nb_earned = sum(1 for _, g in CATALOGUE for b in g if b[0] in earned)

PARCOURS = [
    {"name": "Épargner & budget", "sub": "Matelas de sécurité et règle 50/30/20", "icon": "shield", "c1": "#3B82F6", "c2": "#1D4ED8",
     "done": courant + (1 if courant >= 2 else 0), "total": 3, "page": "pages/4_ParcoursCourant.py",
     "next": ["Le test de résistance", "Le quiz 50/30/20"][min(courant, 1)] if courant < 2 else None},
    {"name": "Investir & PEA", "sub": "6 niveaux pour apprendre à investir", "icon": "monitoring", "c1": "#22C55E", "c2": "#15803D",
     "done": pea, "total": 6, "page": "pages/5_ParcoursPEA.py",
     "next": f"Niveau {pea + 1} du PEA" if pea < 6 else None},
    {"name": "Projets & aides", "sub": "Prêts, permis, primes et voyages", "icon": "school", "c1": "#8B5CF6", "c2": "#6D28D9",
     "done": len(projet_cards) + (1 if projet_bilan else 0), "total": 5, "page": "pages/6_ParcoursProjet.py",
     "next": (f"Carte d'aide {len(projet_cards) + 1} sur 4" if len(projet_cards) < 4 else "Valider ton bilan d'aides") if not projet_bilan else None},
]
parcours_finis = sum(1 for p in PARCOURS if p["done"] >= p["total"])

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
NAVY, BLUE, GOLD, SOFT, MUTE = "#14213D", "#1F2BE0", "#FFC83D", "#EEF1F8", "#5B6785"
CSS = f"""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL@24,500,1" rel="stylesheet">
<style>
.stApp{{background:#E6EBF5!important;}}
.block-container,[data-testid="stMainBlockContainer"]{{max-width:100%!important;width:100%!important;padding:1.6rem 3rem 3rem!important;}}
[data-testid="stMain"] p,[data-testid="stMain"] div,[data-testid="stMain"] button,[data-testid="stMain"] label{{font-family:'Plus Jakarta Sans',sans-serif;}}
.ms{{font-family:'Material Symbols Rounded'!important;font-weight:normal;font-style:normal;line-height:1;display:inline-block;
  -webkit-font-feature-settings:'liga';font-feature-settings:'liga';font-variation-settings:'FILL' 1;}}

/* Bandeau profil */
.hero{{margin-top:14px;display:flex;align-items:center;gap:28px;flex-wrap:wrap;background:linear-gradient(135deg,#1A2B5C,#101B3A);border-radius:30px;padding:30px 34px;
  box-shadow:0 14px 34px rgba(20,33,61,.25);position:relative;overflow:hidden;}}
.hero:after{{content:"";position:absolute;right:-80px;top:-80px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(255,200,61,.22),transparent 65%);}}
.avatar{{width:96px;height:96px;border-radius:50%;background:linear-gradient(160deg,{GOLD},#F59E0B);display:flex;align-items:center;justify-content:center;
  font-size:34px;font-weight:800;color:{NAVY};box-shadow:0 0 0 6px rgba(255,200,61,.25);flex-shrink:0;}}
.hello{{flex:1;min-width:280px;z-index:1;}}
.hello .k{{color:{GOLD};font-size:13px;font-weight:800;letter-spacing:2px;text-transform:uppercase;}}
.hello h1{{color:#fff;font-size:34px;font-weight:800;margin:4px 0 2px;letter-spacing:-.5px;}}
.hello .id{{color:#93A3C8;font-size:14.5px;}}
.hello .id b{{color:#C9D1F5;}}
.lvl{{z-index:1;min-width:320px;flex:1;max-width:460px;}}
.lvl .row{{display:flex;justify-content:space-between;align-items:baseline;color:#fff;margin-bottom:10px;}}
.lvl .row b{{font-size:22px;}}
.lvl .row span{{color:#93A3C8;font-weight:700;font-size:14px;}}
.bar{{height:16px;border-radius:99px;background:rgba(255,255,255,.12);overflow:hidden;}}
.bar i{{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#22C55E,{GOLD});box-shadow:0 0 14px rgba(255,200,61,.6);}}
.lvl small{{display:block;color:#93A3C8;font-size:13px;margin-top:8px;font-weight:600;}}

/* Chiffres clés */
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:22px 0 6px;}}
.kpi{{background:#fff;border-radius:22px;padding:20px 22px;display:flex;align-items:center;gap:16px;box-shadow:0 8px 22px rgba(20,33,61,.07);}}
.kpi .ic{{width:54px;height:54px;border-radius:16px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
.kpi .ic .ms{{font-size:30px;color:#fff;}}
.kpi b{{display:block;font-size:28px;font-weight:800;color:{NAVY};line-height:1.05;}}
.kpi span{{display:block;line-height:1.3;color:{MUTE};font-size:14px;font-weight:600;}}

.sec{{display:flex;justify-content:space-between;align-items:baseline;margin:34px 0 14px;}}
.sec .t{{font-size:24px;font-weight:800;color:{NAVY};margin:0;}}
.sec span{{color:{MUTE};font-weight:700;font-size:14.5px;}}

/* Cartes parcours */
[class*="st-key-pc_"]{{background:#fff!important;border-radius:24px!important;padding:22px!important;box-shadow:0 8px 22px rgba(20,33,61,.07);border:1.5px solid #E3E8F3!important;}}
.pc-top{{display:flex;gap:14px;align-items:center;}}
.pc-top .ic{{width:56px;height:56px;border-radius:18px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
.pc-top .ic .ms{{font-size:30px;color:#fff;}}
.pc-top b{{display:block;font-size:19px;color:{NAVY};}}
.pc-top span{{color:{MUTE};font-size:13.5px;}}
.pc-bar{{height:12px;border-radius:99px;background:{SOFT};overflow:hidden;margin:18px 0 8px;}}
.pc-bar i{{display:block;height:100%;border-radius:99px;}}
.pc-meta{{display:flex;justify-content:space-between;font-size:13.5px;font-weight:700;color:{MUTE};}}
.pc-meta b{{color:{NAVY};}}
.pc-next{{margin-top:12px;font-size:14px;color:{NAVY};background:{SOFT};border-radius:12px;padding:9px 12px;}}
.pc-next.ok{{background:#DCFCE7;color:#166534;font-weight:700;}}
[class*="st-key-pc_"] .stButton button,[class*="st-key-sg_"] .stButton button{{width:100%;min-height:48px!important;border-radius:99px!important;border:none!important;
  background:{NAVY}!important;box-shadow:0 5px 0 #0A1226!important;transition:transform .1s;}}
[class*="st-key-pc_"] .stButton button p,[class*="st-key-sg_"] .stButton button p{{color:#fff!important;font-weight:800!important;font-size:15px!important;}}
[class*="st-key-pc_"] .stButton button:active,[class*="st-key-sg_"] .stButton button:active{{transform:translateY(4px);box-shadow:0 1px 0 #0A1226!important;}}

/* Galerie de badges */
.gal{{background:#fff;border-radius:26px;padding:24px 26px;box-shadow:0 8px 22px rgba(20,33,61,.07);}}
.grp{{margin-bottom:18px;}}
.grp:last-child{{margin-bottom:0;}}
.grp h3{{font-size:14px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:{MUTE};margin:0 0 12px;}}
.row-b{{display:flex;flex-wrap:wrap;gap:18px;}}
.it{{width:118px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px;}}
.it p{{margin:0;font-size:13px;font-weight:700;color:{NAVY};line-height:1.25;}}
.it.off p{{color:#9AA5BD;}}
.bdg{{position:relative;width:var(--s);height:calc(var(--s) * 1.12);transition:transform .15s;}}
.it:hover .bdg{{transform:translateY(-4px) scale(1.04);}}
.bdg .hex{{position:absolute;clip-path:polygon(50% 0,94% 24%,94% 76%,50% 100%,6% 76%,6% 24%);}}
.bdg .o{{inset:0;background:linear-gradient(180deg,#FFE9A8 0%,#F2B623 55%,#C98A00 100%);}}
.bdg .i{{inset:7%;background:linear-gradient(160deg,var(--c1),var(--c2));display:flex;align-items:center;justify-content:center;}}
.bdg .i:after{{content:"";position:absolute;left:0;right:0;top:0;height:46%;background:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,0));}}
.bdg .i .ms{{color:#fff;font-size:calc(var(--s) * .44);filter:drop-shadow(0 3px 2px rgba(0,0,0,.25));z-index:1;}}
.bdg.off .o{{background:linear-gradient(180deg,#DDE2EC,#BAC2D3);}}
.bdg.off .i{{background:linear-gradient(160deg,#EEF1F7,#D5DBE7);}}
.bdg.off .i .ms{{color:#AEB6C8;filter:none;}}

/* Suggestions */
[class*="st-key-sg_"]{{border-radius:24px!important;padding:22px!important;}}
.st-key-sg_0{{background:linear-gradient(135deg,{NAVY},#26365F)!important;}}
.st-key-sg_1{{background:linear-gradient(135deg,{BLUE},#4F46E5)!important;}}
.sg .k{{font-size:12.5px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:{GOLD};}}
.sg h4{{color:#fff;font-size:21px;font-weight:800;margin:6px 0 6px;}}
.sg p{{color:#C9D1F5;font-size:14.5px;margin:0 0 14px;line-height:1.45;}}
.sg .ms{{font-size:40px;color:{GOLD};float:right;}}
[class*="st-key-sg_"] .stButton button{{background:{GOLD}!important;box-shadow:0 5px 0 #B86E00!important;}}
[class*="st-key-sg_"] .stButton button p{{color:{NAVY}!important;}}
@media (max-width:1000px){{.kpis{{grid-template-columns:repeat(2,1fr);}}}}
</style>
"""
st.markdown("\n".join(l for l in CSS.splitlines() if l.strip()), unsafe_allow_html=True)


def html(s: str) -> None:
    st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


def badge(icon: str, c1: str, c2: str, size: int, on: bool) -> str:
    return (f'<div class="bdg {"" if on else "off"}" style="--s:{size}px;--c1:{c1};--c2:{c2}">'
            f'<div class="hex o"></div><div class="hex i"><span class="ms">{icon if on else "lock"}</span></div></div>')


# ---------------------------------------------------------------------------
# 1. Bandeau profil
# ---------------------------------------------------------------------------
html(f"""<div class="hero">
<div class="avatar">{initials}</div>
<div class="hello"><div class="k">Tableau de bord</div><h1>Bonjour {name.split()[0]} !</h1>
<div class="id">{name}{f' · identifiant <b>{login}</b>' if login else ''}</div></div>
<div class="lvl"><div class="row"><b>Niveau {level} · {rang}</b><span>{xp_in} / {XP_PAR_NIVEAU} XP</span></div>
<div class="bar"><i style="width:{max(xp_pct, 3)}%"></i></div>
<small>Encore {XP_PAR_NIVEAU - xp_in} XP pour atteindre le niveau {level + 1}</small></div>
</div>""")

# ---------------------------------------------------------------------------
# 2. Chiffres clés
# ---------------------------------------------------------------------------
kpis = [
    ("bolt", "#F59E0B", f"{xp:,}".replace(",", " "), "XP au total"),
    ("military_tech", BLUE, f"{nb_earned} / {total_badges}", "badges obtenus"),
    ("flag", "#22C55E", f"{parcours_finis} / 3", "parcours terminés"),
    ("monitoring", "#8B5CF6", f"{pea} / 6", "niveaux PEA validés"),
]
html('<div class="kpis">' + "".join(
    f'<div class="kpi"><div class="ic" style="background:{c}"><span class="ms">{ic}</span></div><div><b>{v}</b><span>{l}</span></div></div>'
    for ic, c, v, l in kpis) + "</div>")

# ---------------------------------------------------------------------------
# 3. Progression par parcours
# ---------------------------------------------------------------------------
html('<div class="sec"><div class="t">Tes parcours</div><span>Reprends là où tu t\'es arrêté</span></div>')
cols = st.columns(3, gap="medium")
for i, (p, col) in enumerate(zip(PARCOURS, cols)):
    pct = round(min(p["done"], p["total"]) / p["total"] * 100)
    with col:
        with st.container(key=f"pc_{i}"):
            nxt = (f'<div class="pc-next"><b>Prochaine étape :</b> {p["next"]}</div>' if p["next"]
                   else '<div class="pc-next ok">Parcours terminé, bravo !</div>')
            html(f"""<div class="pc-top"><div class="ic" style="background:linear-gradient(160deg,{p["c1"]},{p["c2"]})"><span class="ms">{p["icon"]}</span></div>
<div><b>{p["name"]}</b><span>{p["sub"]}</span></div></div>
<div class="pc-bar"><i style="width:{max(pct, 2)}%;background:linear-gradient(90deg,{p["c1"]},{p["c2"]})"></i></div>
<div class="pc-meta"><span><b>{min(p["done"], p["total"])}</b> / {p["total"]} étapes</span><span>{pct} %</span></div>{nxt}""")
            label = "Revoir le parcours" if not p["next"] else ("Commencer" if p["done"] == 0 else "Continuer")
            if st.button(label, key=f"go_{i}", icon=":material/play_arrow:", use_container_width=True):
                st.switch_page(p["page"])

# ---------------------------------------------------------------------------
# 4. Galerie des badges
# ---------------------------------------------------------------------------
html(f'<div class="sec"><div class="t">Ta collection de badges</div><span>{nb_earned} sur {total_badges} débloqués</span></div>')
groups = ""
for title, items in CATALOGUE:
    its = "".join(
        f'<div class="it {"" if b in earned else "off"}">{badge(ic, c1, c2, 76, b in earned)}<p>{b}</p></div>'
        for b, ic, c1, c2 in items)
    groups += f'<div class="grp"><h3>{title}</h3><div class="row-b">{its}</div></div>'
html(f'<div class="gal">{groups}</div>')

# ---------------------------------------------------------------------------
# 5. Prochaine étape
# ---------------------------------------------------------------------------
html('<div class="sec"><div class="t">Ta prochaine étape</div><span>Suggestions personnalisées</span></div>')
todo = next((p for p in PARCOURS if p["next"]), None)
if todo:
    s1 = ("rocket_launch", "Recommandé pour toi", todo["next"],
          f"Continue le parcours « {todo['name']} » pour gagner de l'XP et ton prochain badge.", "Y aller", todo["page"])
elif pea >= 6:
    s1 = ("query_stats", "Débloqué", "Ton profil investisseur",
          "Tu as validé les 6 niveaux : découvre les entreprises qui collent à tes centres d'intérêt.",
          "Voir mon profil", "pages/9_ProfilInvestisseur.py")
else:
    s1 = ("emoji_events", "Bravo", "Tous les parcours sont terminés", "Rejoue les défis pour réviser.", "Revoir le plateau", "pages/3_Parcours.py")
s2 = ("forum", "Conseiller IA", "Pose ta question à Marcel",
      "Des réponses fiables, basées sur nos guides officiels, avec un score de confiance.", "Ouvrir le chat", "pages/8_Chat.py")

c1, c2 = st.columns(2, gap="medium")
for i, (col, (ic, k, h, d, btn, page)) in enumerate(zip((c1, c2), (s1, s2))):
    with col:
        with st.container(key=f"sg_{i}"):
            html(f'<div class="sg"><span class="ms">{ic}</span><div class="k">{k}</div><h4>{h}</h4><p>{d}</p></div>')
            if st.button(btn, key=f"sg_btn_{i}", icon=":material/arrow_forward:", use_container_width=True):
                st.switch_page(page)
