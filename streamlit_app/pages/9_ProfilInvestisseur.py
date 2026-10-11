"""Profil investisseur — débloqué quand les 6 niveaux du parcours Investir sont validés."""

import streamlit as st
import requests
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

# name, activité, siège, bourse, éligible PEA
CARTES = {
    "eco": [
        ("Schneider Electric", "Fabrique des équipements pour gérer l'électricité et économiser l'énergie.", "Rueil-Malmaison", "Paris", True),
        ("Veolia", "Gère l'eau, les déchets et l'énergie pour les villes et les industries.", "Aubervilliers", "Paris", True),
        ("Vestas", "Construit et installe des éoliennes partout dans le monde.", "Aarhus (Danemark)", "Copenhague", True),
    ],
    "tech": [
        ("Capgemini", "Aide les entreprises à se transformer grâce au numérique.", "Paris", "Paris", True),
        ("Dassault Systèmes", "Crée des logiciels 3D pour concevoir avions, voitures et objets.", "Vélizy-Villacoublay", "Paris", True),
        ("ASML", "Fabrique les machines qui gravent les puces électroniques.", "Veldhoven (Pays-Bas)", "Amsterdam", True),
    ],
    "indus": [
        ("Michelin", "Fabrique des pneus pour voitures, camions et avions.", "Clermont-Ferrand", "Paris", True),
        ("Airbus", "Conçoit et assemble des avions, des hélicoptères et des satellites.", "Blagnac (Toulouse)", "Paris", True),
        ("Saint-Gobain", "Produit des matériaux pour construire et rénover les bâtiments.", "Courbevoie", "Paris", True),
    ],
    "sante": [
        ("Sanofi", "Développe des médicaments et des vaccins.", "Paris", "Paris", True),
        ("EssilorLuxottica", "Fabrique des verres de lunettes et des montures.", "Charenton-le-Pont", "Paris", True),
        ("bioMérieux", "Conçoit des tests pour diagnostiquer les maladies.", "Marcy-l'Étoile", "Paris", True),
    ],
    "immo": [
        ("Gecina", "Possède et loue des bureaux et des logements, surtout à Paris.", "Paris", "Paris", False),
        ("Klépierre", "Possède et gère des centres commerciaux en Europe.", "Paris", "Paris", False),
        ("Covivio", "Possède des bureaux, des hôtels et des logements en Europe.", "Metz", "Paris", False),
    ],
    "sport": [
        ("Adidas", "Crée des chaussures, des vêtements et des équipements de sport.", "Herzogenaurach (Allemagne)", "Francfort", True),
        ("Puma", "Crée des chaussures et des tenues de sport.", "Herzogenaurach (Allemagne)", "Francfort", True),
        ("Compagnie des Alpes", "Exploite des stations de ski et des parcs de loisirs.", "Paris", "Paris", True),
    ],
}

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
.st-key-inv{{max-width:100%;margin:0 auto;background:#fff!important;border:1.5px solid #E3E8F3!important;border-radius:26px!important;padding:40px!important;box-shadow:0 8px 24px rgba(20,33,61,.08);}}
.i-top{{display:flex;justify-content:space-between;align-items:center;}}
.i-brand{{font-weight:800;color:{NAVY};font-size:14px;letter-spacing:3px;}}
.i-brand b{{color:{YEL};}}
.i-step{{font-size:12.5px;font-weight:700;color:{MUTE};background:{SOFT};padding:4px 12px;border-radius:99px;}}
.i-title{{font-size:27px;font-weight:800;color:{NAVY};margin:14px 0 4px;line-height:1.15;}}
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


def header(title: str, step: str) -> None:
    html(f'<div class="i-top"><span class="i-brand"><b>●</b> YELLO</span><span class="i-step">{step}</span></div>'
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
        for i in range(0, len(keys), 2):
            cols = st.columns(2)
            for col, k in zip(cols, keys[i:i + 2]):
                on = k in ss.inv_secteurs
                label = ("✓ " if on else "") + SECTEURS[k]["label"]
                if col.button(label, key=f"sec_{k}", type="primary" if on else "secondary", use_container_width=True):
                    ss.inv_secteurs = [s for s in ss.inv_secteurs if s != k] if on else ss.inv_secteurs + [k]
                    st.rerun()

    html('<div class="i-h">Combien par mois ?</div>')
    with st.container(key="montant"):
        c1, c2, c3 = st.columns([1, 3, 1])
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
        ss.pop("ollama_advice", None)
        go("paquets")
    if not pret:
        html('<p class="i-hint" style="text-align:center">Choisis un niveau de risque, au moins un secteur et coche la case.</p>')


def ecran_paquets() -> None:
    header("Tes paquets de cartes", "2 / 3")
    noms = [SECTEURS[k]["label"].lower() for k in ss.inv_secteurs]
    liste = ", ".join(noms[:-1]) + " et " + noms[-1] if len(noms) > 1 else noms[0]
    guide(f"{liste.capitalize()} : j'ai préparé un paquet pour chacun.")

    keys = ss.inv_secteurs
    for i in range(0, len(keys), 2):
        cols = st.columns(2)
        for col, k in zip(cols, keys[i:i + 2]):
            s = SECTEURS[k]
            done = k in ss.inv_vus
            with col:
                with st.container(key=f"pack_{s['style']}_{k}{'_done' if done else ''}"):
                    sous = "✓ Ouvert" if done else f"{len(CARTES[k])} cartes"
                    if st.button(f"{s['label']}\n{sous}", key=f"open_{k}", icon=f":material/{s['icon']}:", use_container_width=True):
                        go("cartes", inv_pack=k, inv_idx=0)
    html('<p class="i-hint" style="text-align:center;margin-top:14px">Touche un paquet pour l\'ouvrir</p>')

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
    if idx == 0:
        guide(f"Trois entreprises qui collent à ton profil {ss.inv_risque.lower()}. Garde celles qui te parlent.")
    else:
        guide("Celle-ci te parle ? Garde-la, sinon passe à la suivante.")

    pea_txt = '<b>Éligible</b>' if pea else '<b class="no">Non éligible</b>'
    html(f"""<div class="deck"><div class="co">
<div class="co-head"><span>{s['label']}</span><span>Action cotée</span></div>
<div class="co-art"><span class="ms">{s['icon']}</span></div>
<div class="co-body">
<div class="co-name">{nom}</div>
<div class="co-desc">{desc}</div>
<div class="co-row"><span>Siège</span><b>{siege}</b></div>
<div class="co-row"><span>Bourse</span><b>{bourse}</b></div>
<div class="co-row"><span>PEA</span>{pea_txt}</div>
</div></div></div>""")
    if not pea:
        html('<p class="i-hint">Foncière cotée (SIIC) : non éligible au PEA, mais accessible avec un compte-titres.</p>')
    html('<div class="warn">⚠️ Une action peut perdre de la valeur.</div>')

    c1, c2 = st.columns(2)
    with c1:
        if action("Passer", "pass", "w"):
            go("cartes", inv_idx=idx + 1)
    with c2:
        if action("Garder", "keep", "n"):
            ss.pop("ollama_advice", None)
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
        # Appel dynamique à Ollama !
        if "ollama_advice" not in ss:
            noms_entreprises = [n for n, k, p in kept]
            prompt = (f"Agis comme un éducateur financier bienveillant. L'utilisateur a un profil {ss.inv_risque.lower()} "
                      f"et investit {m}€ par mois. Il a choisi de mettre {etf_pct}% dans un ETF diversifié, et le reste "
                      f"dans : {', '.join(noms_entreprises)}. Rédige un court paragraphe (3-4 phrases max) très encourageant "
                      f"qui explique de manière éducative en quoi cette diversification est intéressante. "
                      f"Termine par un mot d'encouragement. Réponds directement, sans introduction.")
            
            with st.spinner("🤖 Génération de l'analyse IA (via Llama 3 local)..."):
                try:
                    r = requests.post("http://localhost:11434/api/generate", json={
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False
                    }, timeout=10)
                    if r.status_code == 200:
                        ss.ollama_advice = r.json().get("response", "").strip()
                    else:
                        ss.ollama_advice = f"Profil **{ss.inv_risque.lower()}** avec {m} € par mois. Voici un exemple de répartition."
                except Exception as e:
                    ss.ollama_advice = f"Profil **{ss.inv_risque.lower()}** avec {m} € par mois. (Ollama non disponible)"
        
        guide(ss.ollama_advice)

    html(f'<div class="pick"><div><b>Fonds diversifié (ETF monde)</b><br><span>Base de ton portefeuille · {etf_pct} %</span></div><em>{m_etf} €</em></div>')
    if kept:
        part = round(m_act / len(kept), 1)
        for nom, k, pea in kept:
            tag = '<span class="tag">PEA</span>' if pea else '<span class="tag no">Compte-titres</span>'
            html(f'<div class="pick"><div><b>{nom}</b> {tag}<br><span>{SECTEURS[k]["label"]}</span></div><em>{part:g} €</em></div>')
        html(f'<p class="i-hint">Part actions : {act_pct} % de ton montant mensuel, répartie entre tes {len(kept)} entreprise(s).</p>')

    # Récompense (une seule fois)
    if not ss.get("inv_badge"):
        user["xp_points"] = int(user.get("xp_points", 0) or 0) + 100
        badges = list(user.get("badges", []))
        if "Profil investisseur" not in badges:
            badges.append("Profil investisseur")
        user["badges"] = badges
        ss["inv_badge"] = True
    profil = {"risque": ss.inv_risque, "secteurs": ss.inv_secteurs, "montant_mensuel": m,
              "selection": [{"nom": n, "secteur": k, "pea": p} for n, k, p in kept],
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
    html('<div class="foot">Information générale, pas un conseil en investissement.</div>')
