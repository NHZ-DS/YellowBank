"""Page de Situation Actuelle & Visualisation — Yello."""

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from services.api_service import api_service

st.set_page_config(page_title="2. Situation Actuelle — Yello", page_icon="⭐", layout="wide")
ss = st.session_state

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in ss or not ss["user"]:
    ss["user"] = api_service.login("demo", "demo123").get("user", {})
user = ss["user"]
profil = ss.get("profil") or user.get("profil")

# ---------------------------------------------------------------------------
# Animations (LottieFiles, licence Lottie Simple License)
# ---------------------------------------------------------------------------
LOTTIE = {
    "avatar": "https://assets-v2.lottiefiles.com/a/72d1e8f4-1169-11ee-be4e-f75a6faac104/hnGhUFQXuS.lottie",
    "shield": "https://assets-v2.lottiefiles.com/a/51c344b6-f028-11ee-9c09-9f8a57ff8feb/fPmaIOZRFh.lottie",
    "vault": "https://assets-v2.lottiefiles.com/a/626ab95c-a532-11ee-9805-7764209008a3/TprQJ3VDwf.lottie",
    "star": "https://assets-v2.lottiefiles.com/a/2ac71f3a-1163-11ee-8932-a35df5ec6a4f/Xm2P1aETRE.lottie",
    "growth": "https://assets-v2.lottiefiles.com/a/a29f68b0-63bf-11ee-8655-b302196e7a77/WoXvLOaPsg.lottie",
}
LOTTIE_JS = '<script src="https://unpkg.com/@lottiefiles/dotlottie-wc@latest/dist/dotlottie-wc.js" type="module"></script>'

NAVY, BLUE, GOLD, SOFT, MUTE, GREEN = "#14213D", "#1F2BE0", "#FFB800", "#EEF1F8", "#5B6785", "#16A34A"
FONT = "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap"

# ---------------------------------------------------------------------------
# Libellés lisibles (plus de codes bruts à l'écran)
# ---------------------------------------------------------------------------
OBJECTIF_LABEL = {"courant": "Épargner (sécuriser le budget)", "pea": "Investir (PEA)", "projets": "Financer un projet"}
INTERET_LABEL = {"budget": "Budget", "projet": "Projet", "bourse": "Bourse", "aides": "Aides"}
AIDE_LABEL = {"bourse": "Bourse d'études", "job": "Job étudiant", "apl": "APL",
              "are": "Indemnisé·e", "formation": "Recherche formation"}

# ---------------------------------------------------------------------------
# Données financières
# Branche ici ton vrai appel API s'il existe ; sinon une estimation à partir du profil.
# ---------------------------------------------------------------------------
def get_finances(p: dict) -> dict:
    """Estimation à partir des réponses. À remplacer par ton appel API quand il existe
    (ex. api_service.get_situation(user["id"]))."""
    details = p.get("details", {})
    statut = p.get("statut")
    aides = details.get("aides", [])
    revenu = details.get("revenu", "")
    logement = details.get("logement", "")

    # Revenu mensuel
    if statut == "Étudiant·e":
        rev_val = 450 + 250 * ("bourse" in aides) + 200 * ("apl" in aides) + 450 * ("job" in aides)
    elif statut == "En recherche d'emploi":
        rev_val = 1000 if "are" in aides else 550
    else:
        rev_val = 1500
        if "< 800" in revenu: rev_val = 600
        elif "1 500 – 2 500" in revenu: rev_val = 2000
        elif "> 2 500" in revenu: rev_val = 3000

    # Dépenses selon le logement
    dep_val = rev_val * 0.7
    if logement in ("Chez mes parents", "Logement étudiant"): dep_val = rev_val * 0.4
    elif logement == "Locataire": dep_val = rev_val * 0.8

    epargne_mensuelle = max(30, (rev_val - dep_val) * 0.5)
    matelas = user.get("savings_balance", rev_val * 2)
    mois_secu = round(matelas / max(1, dep_val), 1)

    # Projection sur 12 mois
    serie = [{"mois": m + 1,
              "Compte courant": round((rev_val - dep_val) * (1 + 0.05 * m)),
              "Épargne & invest.": round(matelas + epargne_mensuelle * m)} for m in range(12)]
    return {"revenu": rev_val, "depenses": round(dep_val), "epargne_mensuelle": round(epargne_mensuelle),
            "matelas": round(matelas), "mois_secu": mois_secu, "serie": serie, "estimation": True}


def compute(f: dict) -> dict:
    mois = f["mois_secu"]
    score = min(100, int(f["matelas"] / max(1, f["depenses"] * 3) * 100))   # 100 % = 3 mois de matelas

    rang = "Apprenti prudent"
    if mois >= 1: rang = "Aventurier sérénité"
    if mois >= 3: rang = "Gardien du trésor"

    if mois < 1:   badge, cible = "Matelas 1 mois", 1
    elif mois < 3: badge, cible = "Matelas 3 mois", 3
    elif mois < 6: badge, cible = "Matelas 6 mois", 6
    else:          badge, cible = "Investisseur en herbe", 6
    return {"mois": mois, "score": score, "rang": rang, "badge": badge, "cible": cible,
            "niveau": user.get("level", 1), "xp": user.get("xp_points", 0)}


def tips(p: dict) -> list[tuple[str, str]]:
    """Tes astuces, affichées en cartes (jusqu'à 3, selon la situation ET l'objectif)."""
    d, statut, obj = p.get("details", {}), p.get("statut"), p.get("objectif")
    out = []
    if statut == "Étudiant·e":
        out.append(("Astuce étudiant", "As-tu vérifié ton éligibilité aux bourses du CROUS ou aux APL pour ton logement ? Chaque aide compte pour construire ton épargne."))
    elif statut == "Alternant·e":
        out.append(("Astuce alternant", "Pense à l'aide au permis pour les apprentis majeurs et à l'aide Mobili-Jeune pour alléger ton loyer."))
    elif statut == "Salarié·e" and d.get("logement") == "Locataire":
        out.append(("Astuce salarié locataire", "Connais-tu la prime d'activité ? Et pour un futur déménagement, la garantie Visale peut faire office de garant gratuit."))
    elif statut == "En recherche d'emploi":
        out.append(("Astuce transition", "Sécurise tes liquidités et fais valoir tes droits (France Travail, APL) en attendant le retour à l'emploi."))
    if obj == "pea":
        out.append(("Astuce investisseur", "La règle d'or du PEA : l'horizon de 5 ans pour l'avantage fiscal sur les plus-values. Prends date dès aujourd'hui !"))
    elif obj == "projets":
        out.append(("Astuce projet", "Permis, études, logement : beaucoup d'aides se cumulent. Ton parcours Projet te les fait découvrir une par une."))
    out.append(("Astuce Yello", "Continue de mettre de côté régulièrement pour consolider ton matelas de sécurité."))
    return out[:3]


# ---------------------------------------------------------------------------
# Composants visuels
# ---------------------------------------------------------------------------
def card_component(html: str, height: int) -> None:
    components.html(f"""
<link href="{FONT}" rel="stylesheet">{LOTTIE_JS}
<style>
*{{box-sizing:border-box;margin:0;font-family:'Plus Jakarta Sans',sans-serif;}}
body{{background:transparent;padding:4px 4px 14px;}}
.card{{background:#fff;border-radius:26px;padding:22px;height:{height - 22}px;box-shadow:0 8px 24px rgba(20,33,61,.08);border:1.5px solid #E3E8F3;
display:flex;flex-direction:column;align-items:center;text-align:center;}}
.lbl{{font-size:12px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:{MUTE};}}
.big{{font-size:30px;font-weight:800;color:{NAVY};line-height:1.1;margin:6px 0 2px;}}
.sub{{font-size:13.5px;color:{MUTE};font-weight:500;}}
.bar{{width:100%;height:10px;background:{SOFT};border-radius:99px;overflow:hidden;margin:12px 0 6px;}}
.bar i{{display:block;height:100%;border-radius:99px;}}
.chip{{background:#fff;border:1.5px solid #D9DFEE;color:{NAVY};font-weight:700;font-size:13px;padding:6px 12px;border-radius:99px;}}
.chip.k{{background:{NAVY};border-color:{NAVY};color:#fff;}}
.chip.b{{background:{BLUE};border-color:{BLUE};color:#fff;}}
.chip span{{color:{MUTE};font-weight:600;margin-right:5px;}}
.chip.k span,.chip.b span{{color:#C9D1F5;}}
</style>{html}""", height=height)


def lottie(key: str, size: int) -> str:
    return f'<dotlottie-wc src="{LOTTIE[key]}" autoplay loop style="width:{size}px;height:{size}px"></dotlottie-wc>'


def ring(pct: int, color: str) -> str:
    r, c = 52, 2 * 3.1416 * 52
    return f"""<svg width="132" height="132" viewBox="0 0 132 132" style="margin:4px 0">
<circle cx="66" cy="66" r="{r}" fill="none" stroke="{SOFT}" stroke-width="13"/>
<circle cx="66" cy="66" r="{r}" fill="none" stroke="{color}" stroke-width="13" stroke-linecap="round"
stroke-dasharray="{c * pct / 100:.1f} {c:.1f}" transform="rotate(-90 66 66)"/>
<text x="66" y="62" text-anchor="middle" font-size="30" font-weight="800" fill="{NAVY}" font-family="Plus Jakarta Sans">{pct}</text>
<text x="66" y="84" text-anchor="middle" font-size="12" font-weight="600" fill="{MUTE}" font-family="Plus Jakarta Sans">/ 100</text></svg>"""


# ---------------------------------------------------------------------------
# Style de la page
# ---------------------------------------------------------------------------
CSS = f"""
<link href="{FONT}" rel="stylesheet">
<style>
.stApp{{background:#E6EBF5!important;}}
.block-container,[data-testid="stMainBlockContainer"]{{max-width:100%!important;width:100%!important;padding:2rem 3rem 3rem!important;}}
.st-key-page,.st-key-page p,.st-key-page div,.st-key-page span,.st-key-page h3{{font-family:'Plus Jakarta Sans',sans-serif;}}
.s-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;}}
.s-brand{{font-weight:800;color:{NAVY};font-size:15px;letter-spacing:3px;}}
.s-brand b{{color:{GOLD};}}
.s-step{{font-size:13px;font-weight:700;color:{MUTE};background:#fff;padding:5px 14px;border-radius:99px;}}
.s-title{{font-size:34px;font-weight:800;color:{NAVY};margin:0;line-height:1.1;}}
.s-sub{{color:{MUTE};font-size:15.5px;margin:6px 0 0;}}
.s-h{{font-size:20px;font-weight:800;color:{NAVY};margin:30px 0 12px;}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px;}}
.chip{{background:#fff;border:1.5px solid #D9DFEE;color:{NAVY};font-weight:700;font-size:14px;padding:7px 14px;border-radius:99px;}}
.chip.k{{background:{NAVY};border-color:{NAVY};color:#fff;}}
.chip.b{{background:{BLUE};border-color:{BLUE};color:#fff;}}
.chip span{{color:{MUTE};font-weight:600;margin-right:4px;}}
.chip.k span,.chip.b span{{color:#C9D1F5;}}
.tips{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;}}
.tip{{background:#fff;border-radius:20px;padding:18px 20px;border:1.5px solid #E3E8F3;border-top:5px solid {GOLD};}}
.tip h4{{margin:0 0 6px;font-size:16px;font-weight:800;color:{NAVY};}}
.tip p{{margin:0;font-size:14px;color:{MUTE};line-height:1.5;}}
.st-key-chart{{background:#fff!important;border-radius:26px!important;padding:18px 18px 6px!important;border:1.5px solid #E3E8F3!important;box-shadow:0 8px 24px rgba(20,33,61,.08);}}
.est{{font-size:12.5px;color:{MUTE};margin:8px 4px 0;}}
.st-key-cta{{display:flex!important;align-items:center!important;margin:30px 0 10px;}}
.st-key-cta .stButton,.st-key-cta [data-testid="stElementContainer"]{{width:auto!important;}}
.st-key-cta button{{min-height:60px!important;padding:0 44px!important;border-radius:99px!important;background:{NAVY}!important;border:none!important;
box-shadow:0 8px 0 #0A1226!important;transition:transform .1s;}}
.st-key-cta button p{{color:#fff!important;font-size:18px!important;font-weight:800!important;letter-spacing:.5px;}}
.st-key-cta button:hover{{transform:translateY(-2px);}}
.st-key-cta button:active{{transform:translateY(6px);box-shadow:0 2px 0 #0A1226!important;}}
</style>
"""
st.markdown("\n".join(l for l in CSS.splitlines() if l.strip()), unsafe_allow_html=True)


def html(block: str) -> None:
    st.markdown("\n".join(l.strip() for l in block.splitlines() if l.strip()), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
with st.container(key="page"):
    if not profil:
        html('<div class="s-title">Ton diagnostic t\'attend</div><p class="s-sub">Réponds d\'abord au questionnaire pour découvrir ta situation.</p>')
        with st.container(key="cta"):
            if st.button("Faire le questionnaire ▶", key="go_quiz"):
                st.switch_page("pages/1_Questionnaire.py")
        st.stop()

    fin = get_finances(profil)
    sc = compute(fin)
    name = user.get("username") or user.get("first_name") or "Aventurier"

    # En-tête
    html(f"""
<div class="s-head"><span class="s-brand"><b>●</b> YELLO</span><span class="s-step">Étape 2 / 3</span></div>
<div class="s-title">Diagnostic visuel de ta situation</div>
<p class="s-sub">Salut {name} ! Voici la synthèse de ton profil, de tes finances et de ton plan d'action.</p>
""")

    # Carte avatar + profil
    d = profil.get("details", {})
    chips = [f'<span class="chip k"><span>Âge</span>{profil.get("age", "—")}</span>',
             f'<span class="chip b"><span>Situation</span>{profil.get("statut", "—")}</span>',
             f'<span class="chip"><span>Objectif</span>{OBJECTIF_LABEL.get(profil.get("objectif"), "—")}</span>']
    for k, lab in (("contrat", "Contrat"), ("revenu", "Revenu"), ("logement", "Logement")):
        if d.get(k):
            chips.append(f'<span class="chip"><span>{lab}</span>{d[k]}</span>')
    chips += [f'<span class="chip">{AIDE_LABEL.get(a, a)}</span>' for a in d.get("aides", [])]
    interets = " · ".join(INTERET_LABEL.get(i, i) for i in profil.get("interets", []))

    xp_next = 100
    xp_pct = sc["xp"] % 100
    card_component(f"""
<div class="card" style="flex-direction:row;align-items:center;gap:24px;text-align:left;flex-wrap:wrap">
  <div style="width:150px;height:150px;border-radius:50%;background:radial-gradient(circle,#FFF4CC 0%,#FFFFFF 70%);display:flex;align-items:center;justify-content:center;flex-shrink:0">{lottie("avatar", 150)}</div>
  <div style="flex:1;min-width:260px">
    <div class="lbl">Ton rang</div>
    <div class="big" style="font-size:28px">{sc["rang"]}</div>
    <div class="sub">Niveau {sc["niveau"]} · {sc["xp"]} XP · {xp_pct} / 100 vers le niveau suivant</div>
    <div class="bar" style="max-width:420px"><i style="width:{max(xp_pct, 4)}%;background:linear-gradient(90deg,#FF9F1C,{GOLD})"></i></div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px">{"".join(chips)}</div>
    <div class="sub" style="margin-top:10px">Centres d'intérêt : <b style="color:{NAVY}">{interets or "—"}</b></div>
  </div>
</div>""", height=260)

    # Santé financière : 3 cartes
    html('<div class="s-h">Ta santé financière</div>')
    c1, c2, c3 = st.columns(3)
    score_color = GREEN if sc["score"] >= 70 else (GOLD if sc["score"] >= 35 else "#E5484D")
    with c1:
        card_component(f"""<div class="card">
<div class="lbl">Jauge de sérénité</div>{ring(sc["score"], score_color)}
<div class="sub">100 = 3 mois de dépenses mis de côté</div></div>""", height=300)
    with c2:
        mois_pct = min(100, round(sc["mois"] / 6 * 100))
        card_component(f"""<div class="card">
<div class="lbl">Matelas de sécurité</div>{lottie("shield", 96)}
<div class="big">{sc["mois"]:.1f} mois</div>
<div class="sub">{fin["matelas"]:,} € de côté · {fin["depenses"]:,} € de dépenses/mois</div>
<div class="bar"><i style="width:{max(mois_pct, 4)}%;background:{BLUE}"></i></div></div>""".replace(",", " "), height=300)
    with c3:
        badge_pct = min(100, round(sc["mois"] / sc["cible"] * 100))
        card_component(f"""<div class="card">
<div class="lbl">Prochain badge</div>{lottie("star", 96)}
<div class="big" style="font-size:24px">{sc["badge"]}</div>
<div class="sub">{"Débloqué ! Ton matelas est complet, place à l'investissement." if sc["mois"] >= 6 else f"Encore {sc['cible'] - sc['mois']:.1f} mois d'épargne pour le débloquer"}</div>
<div class="bar"><i style="width:{max(badge_pct, 4)}%;background:{GOLD}"></i></div></div>""", height=300)

    # Conseils
    t = tips(profil)
    if t:
        html('<div class="s-h">Les astuces de Yello pour toi</div>')
        html('<div class="tips">' + "".join(f'<div class="tip"><h4>{a}</h4><p>{b}</p></div>' for a, b in t) + "</div>")

    # Évolution du patrimoine
    html('<div class="s-h">Projection de ton patrimoine sur 12 mois</div>')
    df = pd.DataFrame(fin["serie"]).melt("mois", var_name="Compte", value_name="Montant")
    chart = (
        alt.Chart(df)
        .mark_area(line={"strokeWidth": 3}, opacity=0.18, interpolate="monotone")
        .encode(
            x=alt.X("mois:Q", title=None, scale=alt.Scale(domain=[1, 12], nice=False),
                    axis=alt.Axis(values=list(range(1, 13)), labelExpr="'M' + datum.value", grid=False)),
            y=alt.Y("Montant:Q", title=None, stack=None, axis=alt.Axis(format=",.0f", labelExpr="datum.label + ' €'", gridColor="#EEF1F8")),
            color=alt.Color("Compte:N", scale=alt.Scale(domain=["Compte courant", "Épargne & invest."], range=[NAVY, GOLD]),
                            legend=alt.Legend(orient="top", title=None, labelFontSize=13)),
            tooltip=[alt.Tooltip("Compte:N"), alt.Tooltip("mois:Q", title="Mois"), alt.Tooltip("Montant:Q", format=",.0f")],
        )
        .properties(height=300)
        .configure_view(strokeWidth=0)
        .configure_axis(labelFont="Plus Jakarta Sans", labelColor=MUTE, labelFontSize=12, domain=False, ticks=False)
        .configure_legend(labelFont="Plus Jakarta Sans", labelColor=NAVY, symbolType="circle")
    )
    with st.container(key="chart"):
        st.altair_chart(chart, use_container_width=True)
    if fin.get("estimation"):
        html('<p class="est">Estimations basées sur tes réponses au questionnaire (revenus, logement, aides).</p>')

    # Suite
    with st.container(key="cta"):
        if st.button("Accéder au grand plateau ▶", key="go_board"):
            st.switch_page("pages/3_Parcours.py")