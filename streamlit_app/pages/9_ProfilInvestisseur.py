"""Profil investisseur — débloqué quand les 6 niveaux du parcours Investir sont validés."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="9. Profil investisseur — Yello", page_icon="📈", layout="wide")
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
# Déblocage : 6 niveaux du parcours Investir.
# Dans 5_ParcoursPEA.py, quand un niveau est validé :  st.session_state["pea_niveau"] = n
# (ou user["pea_level"] = n si ton backend le renvoie). ?demo=1 dans l'URL débloque pour tester.
# ---------------------------------------------------------------------------
NIVEAUX_REQUIS = 6
niveau_pea = max(int(ss.get("pea_niveau", 0) or 0), int(user.get("pea_level", 0) or 0))
debloque = niveau_pea >= NIVEAUX_REQUIS or st.query_params.get("demo") == "1"

# ---------------------------------------------------------------------------
# Données
# ---------------------------------------------------------------------------
RISQUES = ["Prudent", "Équilibré", "Dynamique"]
RISQUE_INFO = {
    "Prudent": "Tu veux surtout limiter les baisses, quitte à gagner moins.",
    "Équilibré": "Tu acceptes des hauts et des bas pour viser une croissance régulière.",
    "Dynamique": "Tu acceptes de fortes variations pour viser plus de croissance sur le long terme.",
}
# Exemple pédagogique de répartition : part fonds diversifié (ETF) / part actions choisies
REPARTITION = {"Prudent": (70, 30), "Équilibré": (50, 50), "Dynamique": (30, 70)}

SECTEURS = {
    "eco":   {"label": "Écologie",   "icon": "eco",               "style": "y"},
    "tech":  {"label": "Tech",       "icon": "memory",            "style": "b"},
    "indus": {"label": "Industrie",  "icon": "factory",           "style": "n"},
    "sante": {"label": "Santé",      "icon": "medical_services",  "style": "y"},
    "immo":  {"label": "Immobilier", "icon": "apartment",         "style": "b"},
    "sport": {"label": "Sport",      "icon": "sports_soccer",     "style": "n"},
}

# Entreprises FICTIVES pour la démonstration : nom, activité, siège, bourse, éligible PEA
CARTES = {
    "eco": [
        ("Aeolis Énergie", "Construit et exploite des parcs éoliens terrestres.", "Nantes", "Euronext Paris", True),
        ("Solvia Group", "Fabrique des panneaux solaires et des batteries de stockage.", "Montpellier", "Euronext Paris", True),
        ("Hydrane", "Produit de l'électricité grâce aux barrages et gère des réseaux.", "Grenoble", "Euronext Paris", True),
    ],
    "tech": [
        ("Nuvora", "Développe des logiciels de cybersécurité pour les entreprises.", "Rennes", "Euronext Paris", True),
        ("Pixalis", "Conçoit des puces électroniques pour les objets connectés.", "Grenoble", "Euronext Paris", True),
        ("Datacime", "Héberge les données et les applications des PME dans le cloud.", "Lille", "Euronext Paris", True),
    ],
    "indus": [
        ("Ferralis", "Fabrique des pièces de précision pour l'aéronautique.", "Toulouse", "Euronext Paris", True),
        ("Rotec Industries", "Conçoit des robots pour automatiser les usines.", "Lyon", "Euronext Paris", True),
        ("Vitralis", "Produit du verre et des matériaux isolants pour les bâtiments.", "Reims", "Euronext Paris", True),
    ],
    "sante": [
        ("Medivia", "Fabrique des médicaments génériques.", "Lyon", "Euronext Paris", True),
        ("Optalis", "Conçoit des verres de lunettes et des lentilles.", "Paris", "Euronext Paris", True),
        ("Genexa", "Développe des tests pour diagnostiquer les maladies.", "Strasbourg", "Euronext Paris", True),
    ],
    "immo": [
        ("Pierravenir", "Possède et loue des bureaux à Paris et à Lyon.", "Paris", "Euronext Paris", False),
        ("Résidia", "Possède et gère des résidences étudiantes.", "Bordeaux", "Euronext Paris", False),
        ("Commerco", "Possède et gère des centres commerciaux.", "Marseille", "Euronext Paris", False),
    ],
    "sport": [
        ("Stridea", "Crée des chaussures et des vêtements de running.", "Annecy", "Euronext Paris", True),
        ("Alpyn Loisirs", "Exploite des stations de ski et des parcs de loisirs.", "Chambéry", "Euronext Paris", True),
        ("Arena+", "Gère un réseau de salles de sport.", "Nice", "Euronext Paris", True),
    ],
}

# Données financières FICTIVES : performance 1 an (%), croissance des ventes (%), marge nette (%),
# endettement (dette nette / fonds propres, %), rendement du dividende (%)
FIN = {
    "Aeolis Énergie": (1.8, 6.5, 9.0, 85, 2.1), "Solvia Group": (-3.1, 12.0, 2.5, 120, 0.0), "Hydrane": (-5.0, 1.5, 11.0, 70, 4.2),
    "Nuvora": (14.2, 18.0, 15.0, 20, 0.0), "Pixalis": (-8.4, -2.0, 6.0, 45, 0.8), "Datacime": (6.7, 9.5, 7.5, 60, 1.2),
    "Ferralis": (9.3, 7.0, 8.0, 55, 2.0), "Rotec Industries": (3.1, 4.0, 10.5, 35, 1.5), "Vitralis": (-1.2, 0.5, 6.5, 90, 3.0),
    "Medivia": (4.5, 3.5, 12.0, 40, 2.8), "Optalis": (7.8, 6.0, 14.0, 30, 1.9), "Genexa": (-6.3, -4.0, 1.5, 65, 0.0),
    "Pierravenir": (-2.4, 1.0, 22.0, 95, 5.1), "Résidia": (3.6, 5.5, 18.0, 80, 4.4), "Commerco": (-4.1, -1.5, 15.0, 110, 6.0),
    "Stridea": (11.5, 10.0, 8.5, 25, 1.0), "Alpyn Loisirs": (-0.8, 2.0, 7.0, 75, 2.5), "Arena+": (5.2, 14.0, 3.5, 100, 0.0),
}


def serie(nom: str, perf: float, n: int = 52) -> list:
    """Courbe hebdomadaire fictive sur 1 an qui finit exactement à +perf %."""
    import random
    rng = random.Random(nom)
    walk = [0.0]
    for _ in range(n - 1):
        walk.append(walk[-1] + rng.gauss(0, 1.6))
    return [100 * (1 + perf / 100 * i / (n - 1)) + (w - walk[-1] * i / (n - 1)) for i, w in enumerate(walk)]


def sparkline(nom: str, perf: float, h: int = 70, dark: bool = False) -> str:
    pts = serie(nom, perf)
    lo, hi = min(pts), max(pts)
    xs = [i * 300 / (len(pts) - 1) for i in range(len(pts))]
    ys = [h - 6 - (p - lo) / (hi - lo or 1) * (h - 12) for p in pts]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    col = ("#4ADE80" if dark else "#16A34A") if perf >= 0 else ("#F87171" if dark else "#DC2626")
    return (f'<svg viewBox="0 0 300 {h}" preserveAspectRatio="none" style="width:100%;height:{h}px;display:block">'
            f'<polygon points="0,{h} {line} 300,{h}" fill="{col}" opacity=".18"/>'
            f'<polyline points="{line}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>')


def sante(nom: str) -> dict:
    perf, ca, marge, dette, div = FIN[nom]
    def feu(v, bon, moyen, inverse=False):
        if inverse:
            return "g" if v <= bon else ("y" if v <= moyen else "r")
        return "g" if v >= bon else ("y" if v >= moyen else "r")
    ind = [
        ("Croissance des ventes", f"{ca:+.1f} %", feu(ca, 5, 0),
         "Ses ventes augmentent nettement." if ca >= 5 else ("Ses ventes progressent peu." if ca >= 0 else "Ses ventes reculent.")),
        ("Rentabilité (marge nette)", f"{marge:.1f} %", feu(marge, 10, 3),
         f"Sur 100 € de ventes, il lui reste {marge:.0f} € de bénéfice."),
        ("Endettement", f"{dette} %", feu(dette, 50, 100, inverse=True),
         "Peu endettée." if dette <= 50 else ("Endettement modéré." if dette <= 100 else "Très endettée : à surveiller.")),
    ]
    verts = sum(1 for i in ind if i[2] == "g")
    rouges = sum(1 for i in ind if i[2] == "r")
    verdict = ("Solide", "g") if verts >= 2 and rouges == 0 else (("Fragile", "r") if rouges >= 2 or verts == 0 else ("Correcte", "y"))
    return {"perf": perf, "div": div, "ind": ind, "verdict": verdict}


for k, v in {"inv_step": "profil", "inv_risque": None, "inv_secteurs": [], "inv_montant": 50,
             "inv_pack": None, "inv_idx": 0, "inv_kept": [], "inv_vus": []}.items():
    ss.setdefault(k, v)

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
NAVY, BLUE, YEL, SOFT, MUTE, LILAC = "#14213D", "#1F2BE0", "#FFC83D", "#EEF1F8", "#5B6785", "#E4E2FB"
CSS = f"""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL@24,500,1" rel="stylesheet">
<style>
.stApp{{background:#E6EBF5!important;}}
.block-container,[data-testid="stMainBlockContainer"]{{max-width:100%!important;width:100%!important;padding:2rem 3rem 3rem!important;}}
.st-key-inv,.st-key-inv p,.st-key-inv div,.st-key-inv label,.st-key-inv button{{font-family:'Plus Jakarta Sans',sans-serif;}}
.ms{{font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;display:inline-block;-webkit-font-feature-settings:'liga';font-feature-settings:'liga';}}
.st-key-inv{{max-width:1000px;margin:0 auto;background:#fff!important;border-radius:28px!important;padding:32px 40px 30px!important;box-shadow:0 10px 30px rgba(20,33,61,.08);border:1.5px solid #E3E8F3!important;}}
.st-key-inv .deck{{max-width:700px;margin-left:auto;margin-right:auto;}}
.st-key-inv [class*="st-key-panel"]{{background:transparent!important;padding:0!important;}}
.st-key-inv .st-key-panel_lock{{max-width:640px;margin:0 auto;}}
.steps{{display:flex;gap:8px;flex-wrap:wrap;}}
.steps span{{display:flex;align-items:center;gap:8px;background:#fff;color:{MUTE};font-weight:700;font-size:14px;padding:7px 14px 7px 8px;border-radius:99px;box-shadow:0 4px 12px rgba(20,33,61,.06);}}
.steps span i{{font-style:normal;width:24px;height:24px;border-radius:50%;background:{SOFT};display:flex;align-items:center;justify-content:center;font-size:12.5px;}}
.steps span.on{{background:{NAVY};color:#fff;}}
.steps span.on i{{background:{YEL};color:{NAVY};}}
.steps span.ok i{{background:#22C55E;color:#fff;}}
.alloc{{display:flex;height:18px;border-radius:99px;overflow:hidden;margin:10px 0 8px;}}
.alloc div{{height:100%;}}
.legend{{display:flex;gap:16px;flex-wrap:wrap;font-size:13.5px;font-weight:700;color:{NAVY};}}
.legend i{{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;}}
.big-amount{{font-size:40px;font-weight:800;color:{NAVY};line-height:1;}}
.big-amount small{{font-size:16px;color:{MUTE};font-weight:700;}}
.st-key-inv .st-key-card_actions{{max-width:700px;margin:0 auto;}}
.i-top{{display:flex;justify-content:space-between;align-items:center;}}
.i-brand{{font-weight:800;color:{NAVY};font-size:14px;letter-spacing:3px;}}
.i-brand b{{color:{YEL};}}
.i-step{{font-size:12.5px;font-weight:700;color:{MUTE};background:{SOFT};padding:4px 12px;border-radius:99px;}}
.i-top{{margin-bottom:4px;}}
.i-title{{font-size:30px;font-weight:800;color:{NAVY};margin:14px 0 4px;line-height:1.15;}}
.i-h{{font-size:17px;font-weight:800;color:{NAVY};margin:20px 0 10px;}}
.i-hint{{font-size:13.5px;color:{MUTE};margin:6px 2px 0;}}
.guide{{background:{LILAC};border-radius:18px;padding:14px 16px;margin:12px 0 6px;}}
.guide b{{color:{BLUE};font-size:14px;}}
.guide p{{margin:4px 0 0;color:{NAVY};font-size:15px;line-height:1.45;}}
.warn{{display:flex;gap:10px;align-items:center;background:#FFF3C4;border-radius:16px;padding:12px 14px;color:{NAVY};font-size:14px;font-weight:600;margin-top:14px;}}
.locked{{text-align:center;padding:10px 0;}}
.locked .ms{{font-size:64px;color:{NAVY};}}
.bar{{height:12px;background:{SOFT};border-radius:99px;overflow:hidden;margin:14px 0 6px;}}
.bar i{{display:block;height:100%;background:{YEL};border-radius:99px;}}

/* Pilules (risque, secteurs) */
.st-key-inv [class*="st-key-pills_"] [data-testid="stHorizontalBlock"]{{gap:10px!important;}}
.st-key-inv [class*="st-key-pills_"] [data-testid="stElementContainer"],.st-key-inv [class*="st-key-pills_"] .stButton{{width:100%!important;}}
.st-key-inv [class*="st-key-pills_"] button{{width:100%!important;min-height:50px!important;border-radius:99px!important;border:2px solid {NAVY}!important;background:#fff!important;box-shadow:none!important;}}
.st-key-inv [class*="st-key-pills_"] button p{{color:{NAVY}!important;font-size:15.5px!important;font-weight:700!important;}}
.st-key-inv [class*="st-key-pills_"] button:hover{{background:{SOFT}!important;}}
.st-key-inv [class*="st-key-pills_"] button[kind="primary"],.st-key-inv [class*="st-key-pills_"] button[data-testid="stBaseButton-primary"]{{background:{NAVY}!important;}}
.st-key-inv [class*="st-key-pills_"] button[kind="primary"] p,.st-key-inv [class*="st-key-pills_"] button[data-testid="stBaseButton-primary"] p{{color:#fff!important;}}
.st-key-inv .st-key-pills_risque{{background:{SOFT};border-radius:99px;padding:6px!important;}}
.st-key-inv .st-key-pills_risque button{{border-color:transparent!important;background:transparent!important;}}
.st-key-inv .st-key-pills_risque button[kind="primary"],.st-key-inv .st-key-pills_risque button[data-testid="stBaseButton-primary"]{{background:{NAVY}!important;}}

/* Montant */
.st-key-inv .st-key-montant{{background:{SOFT};border-radius:99px;padding:6px!important;}}
.st-key-inv .st-key-montant [data-testid="stHorizontalBlock"]{{align-items:center!important;}}
.st-key-inv .st-key-montant button{{width:52px!important;height:52px!important;min-height:52px!important;border-radius:50%!important;background:{LILAC}!important;border:none!important;}}
.st-key-inv .st-key-montant button p{{color:{NAVY}!important;font-size:24px!important;font-weight:800!important;}}
.amount{{text-align:center;font-size:21px;font-weight:800;color:{NAVY};}}

/* Case de compréhension du risque */
.st-key-inv .st-key-ack{{background:#FFF3C4;border-radius:18px;padding:12px 14px!important;margin-top:14px;}}
.st-key-inv .st-key-ack label p{{font-size:14.5px!important;font-weight:600;color:{NAVY}!important;}}
.st-key-inv .st-key-ack label > div:not([data-testid]):first-of-type{{width:26px!important;height:26px!important;min-width:26px;border-radius:7px!important;border:2px solid {NAVY}!important;background-color:#fff!important;}}
.st-key-inv .st-key-ack label:has(input:checked) > div:not([data-testid]):first-of-type{{background-color:{NAVY}!important;}}

/* Boutons d'action */
.st-key-inv [class*="st-key-act_"] [data-testid="stElementContainer"],.st-key-inv [class*="st-key-act_"] .stButton{{width:100%!important;}}
.st-key-inv [class*="st-key-act_"] button{{width:100%!important;min-height:58px!important;border-radius:99px!important;border:none!important;box-shadow:0 6px 0 rgba(0,0,0,.18)!important;transition:transform .1s;}}
.st-key-inv [class*="st-key-act_"] button:active{{transform:translateY(5px);box-shadow:0 1px 0 rgba(0,0,0,.18)!important;}}
.st-key-inv [class*="st-key-act_"] button p{{font-size:17px!important;font-weight:800!important;}}
.st-key-inv [class*="st-key-act_y"] button{{background:{YEL}!important;}}
.st-key-inv [class*="st-key-act_y"] button p{{color:{NAVY}!important;}}
.st-key-inv [class*="st-key-act_n"] button{{background:{NAVY}!important;}}
.st-key-inv [class*="st-key-act_n"] button p{{color:#fff!important;}}
.st-key-inv [class*="st-key-act_w"] button{{background:#fff!important;border:2px solid {NAVY}!important;box-shadow:none!important;}}
.st-key-inv [class*="st-key-act_w"] button p{{color:{NAVY}!important;}}
.st-key-inv [class*="st-key-act_"] button:disabled{{opacity:.45;}}

/* Paquets de cartes */
.st-key-inv [class*="st-key-pack_"] [data-testid="stElementContainer"],.st-key-inv [class*="st-key-pack_"] .stButton{{width:100%!important;}}
.st-key-inv [class*="st-key-pack_"] button{{width:100%!important;height:190px!important;border-radius:20px!important;border:none!important;
  display:flex!important;flex-direction:column!important;gap:10px;box-shadow:0 10px 0 rgba(0,0,0,.15)!important;transition:transform .15s;
  background-size:100% 18px,100% 18px!important;background-repeat:no-repeat!important;background-position:top,bottom!important;}}
.st-key-inv [class*="st-key-pack_"] button > div,.st-key-inv [class*="st-key-pack_"] button > div > span{{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:12px!important;width:100%;}}
.st-key-inv [class*="st-key-pack_"] button p{{text-align:center!important;}}
.st-key-inv [class*="st-key-pack_"] button span:has(> [data-testid="stIconMaterial"]){{display:flex!important;height:auto!important;flex-shrink:0;margin:0!important;}}
.st-key-inv [class*="st-key-pack_"] button [data-testid="stIconMaterial"]{{width:60px!important;height:60px!important;min-width:60px;min-height:60px;line-height:60px!important;flex-shrink:0;}}
.st-key-inv [class*="st-key-pack_"] button:hover{{transform:translateY(-4px) rotate(-1.5deg);}}
.st-key-inv [class*="st-key-pack_"] button p{{font-size:21px!important;font-weight:800!important;line-height:1.25!important;white-space:pre-line;}}
.st-key-inv [class*="st-key-pack_"] button [data-testid="stIconMaterial"],.st-key-inv [class*="st-key-pack_"] button span[translate="no"]{{font-size:34px!important;width:58px;height:58px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;}}
.st-key-inv [class*="st-key-pack_y"] button{{background-color:{YEL}!important;border:4px solid {NAVY}!important;
  background-image:repeating-linear-gradient(90deg,{NAVY} 0 6px,transparent 6px 11px),repeating-linear-gradient(90deg,{NAVY} 0 6px,transparent 6px 11px)!important;}}
.st-key-inv [class*="st-key-pack_y"] button p{{color:{NAVY}!important;}}
.st-key-inv [class*="st-key-pack_y"] button [data-testid="stIconMaterial"],.st-key-inv [class*="st-key-pack_y"] button span[translate="no"]{{background:{NAVY};color:{YEL}!important;}}
.st-key-inv [class*="st-key-pack_b"] button{{background-color:{BLUE}!important;border:4px solid {NAVY}!important;
  background-image:repeating-linear-gradient(90deg,{NAVY} 0 6px,transparent 6px 11px),repeating-linear-gradient(90deg,{NAVY} 0 6px,transparent 6px 11px)!important;}}
.st-key-inv [class*="st-key-pack_b"] button p{{color:#fff!important;}}
.st-key-inv [class*="st-key-pack_b"] button [data-testid="stIconMaterial"],.st-key-inv [class*="st-key-pack_b"] button span[translate="no"]{{background:#fff;color:{BLUE}!important;}}
.st-key-inv [class*="st-key-pack_n"] button{{background-color:{NAVY}!important;border:4px solid {NAVY}!important;
  background-image:repeating-linear-gradient(90deg,{YEL} 0 6px,transparent 6px 11px),repeating-linear-gradient(90deg,{YEL} 0 6px,transparent 6px 11px)!important;}}
.st-key-inv [class*="st-key-pack_n"] button p{{color:{YEL}!important;}}
.st-key-inv [class*="st-key-pack_n"] button [data-testid="stIconMaterial"],.st-key-inv [class*="st-key-pack_n"] button span[translate="no"]{{background:{YEL};color:{NAVY}!important;}}
.st-key-inv [class*="st-key-pack_"][class*="_done"] button{{opacity:.55;}}

/* Carte entreprise */
.deck{{position:relative;margin:18px 8px 6px;}}
.deck:before,.deck:after{{content:"";position:absolute;inset:0;border-radius:22px;border:3px solid {NAVY};background:{BLUE};}}
.deck:before{{transform:rotate(4deg) translate(10px,4px);}}
.deck:after{{transform:rotate(2deg) translate(5px,2px);background:{LILAC};}}
.co{{position:relative;z-index:1;background:#fff;border:3px solid {NAVY};border-radius:22px;overflow:hidden;animation:pop .25s ease-out;}}
@keyframes pop{{from{{transform:scale(.96);opacity:.4}}to{{transform:none;opacity:1}}}}
.co-head{{background:{YEL};display:flex;justify-content:space-between;padding:10px 16px;font-weight:800;color:{NAVY};font-size:13.5px;}}
.co-chart{{background:{NAVY};padding:14px 16px 10px;}}
.co-perf{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;}}
.co-perf span{{color:#93A3C8;font-size:12.5px;font-weight:700;text-transform:uppercase;letter-spacing:1px;}}
.co-perf b{{font-size:24px;font-weight:800;}}
.up{{color:#16A34A!important;font-weight:800;}} .co-perf b.up{{color:#4ADE80!important;}}
.down{{color:#DC2626!important;font-weight:800;}} .co-perf b.down{{color:#F87171!important;}}
.health{{background:{SOFT};border-radius:16px;padding:12px 14px;margin:4px 0 10px;}}
.health-h{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;font-weight:800;color:{NAVY};font-size:14.5px;}}
.verdict{{font-size:12.5px;padding:3px 10px;border-radius:99px;}}
.verdict.g{{background:#DCFCE7;color:#166534;}} .verdict.y{{background:#FFF3C4;color:#8A5A00;}} .verdict.r{{background:#FDE2E2;color:#991B1B;}}
.ind{{display:flex;gap:10px;align-items:center;padding:7px 0;border-top:1px solid #DCE2EF;}}
.ind:first-of-type{{border-top:none;}}
.ind div{{flex:1;}}
.ind b{{display:block;font-size:13.5px;color:{NAVY};}}
.ind span{{font-size:12.5px;color:{MUTE};}}
.ind em{{font-style:normal;font-weight:800;color:{NAVY};font-size:14px;}}
.dot{{width:12px;height:12px;border-radius:50%;flex-shrink:0;}}
.dot.g{{background:#22C55E;}} .dot.y{{background:#F59E0B;}} .dot.r{{background:#EF4444;}}
.mini{{width:90px;margin:0 12px;}}
.co-art{{background:{NAVY};height:150px;display:flex;align-items:center;justify-content:center;}}
.co-art .ms{{font-size:76px;color:{YEL};}}
.co-body{{padding:16px 18px 8px;}}
.co-name{{font-size:26px;font-weight:800;color:{NAVY};}}
.co-desc{{font-size:15px;color:{MUTE};margin:4px 0 10px;line-height:1.45;}}
.co-row{{display:flex;justify-content:space-between;border-top:1px solid #E3E8F3;padding:9px 0;font-size:14.5px;color:{MUTE};}}
.co-row b{{color:{NAVY};}}
.co-row b.no{{color:#C62828;}}
.co-count{{font-size:13px;color:{MUTE};font-weight:700;}}

/* Récap */
.pick{{display:flex;justify-content:space-between;align-items:center;background:{SOFT};border-radius:16px;padding:12px 14px;margin:8px 0;}}
.pick b{{color:{NAVY};font-size:15.5px;}}
.pick span{{font-size:13px;color:{MUTE};font-weight:600;}}
.pick em{{font-style:normal;font-weight:800;color:{NAVY};}}
.tag{{display:inline-block;font-size:12px;font-weight:700;padding:3px 9px;border-radius:99px;background:#DCFCE7;color:#166534;}}
.tag.no{{background:#FDE2E2;color:#991B1B;}}
.reward{{display:flex;gap:12px;align-items:center;background:{NAVY};color:#fff;border-radius:20px;padding:14px 16px;margin-top:14px;}}
.reward .ms{{font-size:36px;color:{YEL};}}
.reward b{{color:{YEL};}}
.foot{{text-align:center;color:{MUTE};font-size:12.5px;margin-top:18px;}}
</style>
"""
st.markdown("\n".join(l for l in CSS.splitlines() if l.strip()), unsafe_allow_html=True)


def html(s: str) -> None:
    st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


STEP_NAMES = ["Mon profil", "Mes paquets", "Ma sélection"]


def header(title: str, step: str) -> None:
    current = {"1 / 3": 1, "2 / 3": 2, "3 / 3": 3}.get(step, 2 if step.startswith("Carte") else 0)
    chips = "".join(
        f'<span class="{"on" if i == current else ("ok" if i < current else "")}"><i>{"✓" if i < current else i}</i>{n}</span>'
        for i, n in enumerate(STEP_NAMES, 1))
    html(f'<div class="i-top"><span class="i-brand"><b>●</b> YELLO · PROFIL INVESTISSEUR</span><div class="steps">{chips}</div></div>'
         f'<div class="i-title">{title}</div>')


def guide(text: str) -> None:
    html(f'<div class="guide"><b>Guide IA</b><p>{text}</p></div>')


def action(label: str, key: str, style: str = "n", disabled: bool = False) -> bool:
    with st.container(key=f"act_{style}_{key}"):
        return st.button(label, key=key, disabled=disabled, use_container_width=True)


def go(step: str, **kw) -> None:
    ss.inv_step = step
    for k, v in kw.items():
        ss[k] = v
    st.rerun()


# ---------------------------------------------------------------------------
# Écrans
# ---------------------------------------------------------------------------
def ecran_verrouille() -> None:
    with st.container(key="panel_lock"):
        header("Profil investisseur", "Verrouillé")
        pct = round(niveau_pea / NIVEAUX_REQUIS * 100)
        html(f"""<div class="locked"><span class="ms">lock</span>
<p class="i-hint" style="font-size:15.5px">Termine les <b>{NIVEAUX_REQUIS} niveaux</b> du parcours Investir pour débloquer ton profil investisseur et tes paquets de cartes.</p>
<div class="bar"><i style="width:{max(pct, 3)}%"></i></div>
<p class="i-hint"><b>{niveau_pea} / {NIVEAUX_REQUIS}</b> niveaux validés</p></div>""")
        if action("Continuer le parcours Investir", "back_pea"):
            st.switch_page("pages/5_ParcoursPEA.py")


def ecran_profil() -> None:
    header("Mon profil investisseur", "1 / 3")

    html('<div class="i-h">Quel risque acceptes-tu ?</div>')
    with st.container(key="pills_risque"):
        cols = st.columns(3)
        for col, r in zip(cols, RISQUES):
            if col.button(r, key=f"risk_{r}", type="primary" if ss.inv_risque == r else "secondary", use_container_width=True):
                ss.inv_risque = r
                st.rerun()
    if ss.inv_risque:
        html(f'<p class="i-hint">{RISQUE_INFO[ss.inv_risque]}</p>')

    html('<div class="i-h">Ce qui t\'intéresse</div>')
    with st.container(key="pills_secteurs"):
        keys = list(SECTEURS)
        for i in range(0, len(keys), 3):
            cols = st.columns(3)
            for col, k in zip(cols, keys[i:i + 3]):
                on = k in ss.inv_secteurs
                label = ("✓ " if on else "") + SECTEURS[k]["label"]
                if col.button(label, key=f"sec_{k}", type="primary" if on else "secondary", use_container_width=True):
                    ss.inv_secteurs = [x for x in ss.inv_secteurs if x != k] if on else ss.inv_secteurs + [k]
                    st.rerun()

    html('<div class="i-h">Combien par mois ?</div>')
    with st.container(key="montant"):
        c1, c2, c3 = st.columns([1, 6, 1])
        if c1.button("−", key="moins"):
            ss.inv_montant = max(10, ss.inv_montant - 10)
            st.rerun()
        c2.markdown(f'<div class="amount">{ss.inv_montant} € par mois</div>', unsafe_allow_html=True)
        if c3.button("+", key="plus"):
            ss.inv_montant = min(1000, ss.inv_montant + 10)
            st.rerun()

    with st.container(key="ack"):
        ack = st.checkbox("⚠️ J'ai compris que je peux perdre une partie ou la totalité de mes placements.", key="inv_ack")

    pret = bool(ss.inv_risque and ss.inv_secteurs and ack)
    if action("Voir mes propositions", "voir", "y", disabled=not pret):
        go("paquets")
    if not pret:
        html('<p class="i-hint" style="text-align:center">Choisis un niveau de risque, au moins un secteur et coche la case.</p>')


def ecran_paquets() -> None:
    header("Tes paquets de cartes", "2 / 3")
    noms = [SECTEURS[k]["label"].lower() for k in ss.inv_secteurs]
    liste = ", ".join(noms[:-1]) + " et " + noms[-1] if len(noms) > 1 else noms[0]
    guide(f"{liste.capitalize()} : j'ai préparé un paquet pour chacun.")

    keys = ss.inv_secteurs
    n = 3 if len(keys) >= 3 else 2
    for i in range(0, len(keys), n):
        cols = st.columns(n)
        for col, k in zip(cols, keys[i:i + n]):
            s = SECTEURS[k]
            done = k in ss.inv_vus
            with col:
                with st.container(key=f"pack_{s['style']}_{k}{'_done' if done else ''}"):
                    sous = "✓ Ouvert" if done else f"{len(CARTES[k])} cartes"
                    if st.button(f"{s['label']}\n{sous}", key=f"open_{k}", icon=f":material/{s['icon']}:", use_container_width=True):
                        go("cartes", inv_pack=k, inv_idx=0)
    html('<p class="i-hint" style="text-align:center;margin-top:14px">Clique sur un paquet pour l\'ouvrir</p>')

    c1, c2 = st.columns(2)
    with c1:
        if action("Modifier", "edit", "w"):
            go("profil")
    with c2:
        if action("Ma sélection", "recap", "n", disabled=not ss.inv_vus):
            go("recap")


def ecran_cartes() -> None:
    k = ss.inv_pack
    s, cartes = SECTEURS[k], CARTES[k]
    idx = ss.inv_idx
    if idx >= len(cartes):
        if k not in ss.inv_vus:
            ss.inv_vus = ss.inv_vus + [k]
        go("paquets")

    nom, desc, siege, bourse, pea = cartes[idx]
    header(f"Paquet {s['label']}", f"Carte {idx + 1} sur {len(cartes)}")
    sa = sante(nom)
    v = sa["verdict"][0]
    conseil = {"Solide": "ses indicateurs sont plutôt rassurants",
               "Correcte": "certains indicateurs sont bons, d'autres à surveiller",
               "Fragile": "plusieurs indicateurs sont dans le rouge : prudence"}[v]
    intro = f"Trois entreprises du secteur, pour ton profil {ss.inv_risque.lower()}. " if idx == 0 else ""
    guide(f"{intro}Pour <b>{nom}</b>, {conseil}. Un bon résultat passé ne garantit pas l'avenir.")

    pea_txt = '<b>Éligible</b>' if pea else '<b class="no">Non éligible</b>'
    perf = sa["perf"]
    perf_cls = "up" if perf >= 0 else "down"
    rows = "".join(f'<div class="ind"><i class="dot {c}"></i><div><b>{t}</b><span>{e}</span></div><em>{val}</em></div>'
                   for t, val, c, e in sa["ind"])
    div_txt = f"{sa['div']:.1f} % par an" if sa["div"] > 0 else "Aucun (elle réinvestit ses bénéfices)"
    html(f"""<div class="deck"><div class="co">
<div class="co-head"><span>{s['label']}</span><span>Action cotée</span></div>
<div class="co-chart"><div class="co-perf"><span>Cours sur 1 an</span><b class="{perf_cls}">{perf:+.1f} %</b></div>{sparkline(nom, perf, 110, dark=True)}</div>
<div class="co-body">
<div class="co-name">{nom}</div>
<div class="co-desc">{desc}</div>
<div class="health"><div class="health-h"><span>Santé financière</span><span class="verdict {sa['verdict'][1]}">{v}</span></div>{rows}</div>
<div class="co-row"><span>Dividende</span><b>{div_txt}</b></div>
<div class="co-row"><span>Siège · Bourse</span><b>{siege} · {bourse}</b></div>
<div class="co-row"><span>PEA</span>{pea_txt}</div>
</div></div></div>""")
    if not pea:
        html('<p class="i-hint" style="text-align:center">Foncière cotée (SIIC) : non éligible au PEA, mais accessible avec un compte-titres.</p>')
    with st.container(key="card_actions"):
        html('<div class="warn">⚠️ Une action peut perdre de la valeur.</div>')
        c1, c2 = st.columns(2)
        with c1:
            if action("Passer", "pass", "w"):
                go("cartes", inv_idx=idx + 1)
        with c2:
            if action("Garder", "keep", "n"):
                kept = [c for c in ss.inv_kept if c[0] != nom] + [(nom, k, pea)]
                go("cartes", inv_idx=idx + 1, inv_kept=kept)


def ecran_recap() -> None:
    header("Ta sélection", "3 / 3")
    kept = ss.inv_kept
    etf_pct, act_pct = REPARTITION[ss.inv_risque]
    m = ss.inv_montant
    m_etf, m_act = round(m * etf_pct / 100), m - round(m * etf_pct / 100)

    if not kept:
        guide("Tu n'as gardé aucune entreprise pour l'instant. Un fonds diversifié (ETF monde éligible au PEA) est souvent un bon point de départ.")
    else:
        guide(f"Profil <b>{ss.inv_risque.lower()}</b> avec {m} € par mois. Voici un exemple de répartition pour t'entraîner, pas un conseil.")

    html(f"""<div class="alloc"><div style="width:{etf_pct}%;background:{BLUE}"></div><div style="width:{act_pct}%;background:{YEL}"></div></div>
<div class="legend" style="margin-bottom:12px"><span><i style="background:{BLUE}"></i>Fonds diversifié {etf_pct} %</span><span><i style="background:{YEL}"></i>Actions choisies {act_pct} %</span></div>""")
    html(f'<div class="pick"><div><b>Fonds diversifié (ETF monde)</b><br><span>Base de ton portefeuille · {etf_pct} %</span></div><em>{m_etf} €</em></div>')
    if kept:
        part = round(m_act / len(kept), 1)
        for nom, kk, pea in kept:
            tag = '<span class="tag">PEA</span>' if pea else '<span class="tag no">Compte-titres</span>'
            sa = sante(nom)
            html(f'<div class="pick"><div style="flex:1"><b>{nom}</b> {tag}<br><span>{SECTEURS[kk]["label"]} · santé {sa["verdict"][0].lower()} · '
                 f'<span class="{"up" if sa["perf"] >= 0 else "down"}">{sa["perf"]:+.1f} % sur 1 an</span></span></div>'
                 f'<div class="mini" style="width:160px">{sparkline(nom, sa["perf"], 40)}</div><em>{part:g} €</em></div>')

    if not ss.get("inv_badge"):
        user["xp_points"] = int(user.get("xp_points", 0) or 0) + 100
        badges = list(user.get("badges", []))
        if "Profil investisseur" not in badges:
            badges.append("Profil investisseur")
        user["badges"] = badges
        ss["inv_badge"] = True
    profil = {"risque": ss.inv_risque, "secteurs": ss.inv_secteurs, "montant_mensuel": m,
              "selection": [{"nom": n_, "secteur": k_, "pea": p_} for n_, k_, p_ in kept],
              "repartition": {"etf": etf_pct, "actions": act_pct}}
    ss["profil_investisseur"] = profil
    user["profil_investisseur"] = profil
    ss["user"] = user

    html('<div class="reward"><span class="ms">military_tech</span><div>Badge <b>Profil investisseur</b> débloqué · <b>+100 XP</b></div></div>')
    c1, c2 = st.columns(2)
    with c1:
        if action("Revoir mes paquets", "again", "w"):
            go("paquets")
    with c2:
        if action("Mon tableau de bord", "dash", "y"):
            st.switch_page("pages/7_Dashboard.py")


# ---------------------------------------------------------------------------
with st.container(key="inv"):
    if not debloque:
        ecran_verrouille()
    else:
        {"profil": ecran_profil, "paquets": ecran_paquets, "cartes": ecran_cartes, "recap": ecran_recap}[ss.inv_step]()
    html('<div class="foot">Entreprises et données fictives, pour la démonstration. Information générale, pas un conseil en investissement.</div>')
