"""Page de Questionnaire d'Orientation — Yello."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="1. Questionnaire — Yello", page_icon="📋", layout="wide")
ss = st.session_state

# Style global de l'app (chargé AVANT le style de la page pour que celui-ci ait le dernier mot)
try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# Connexion si personne n'est connecté
if "user" not in ss or not ss["user"]:
    login_res = api_service.login("alex", "alex123")
    ss["user"] = login_res.get("user", {})
user = ss["user"]

# ---------------------------------------------------------------------------
# Contenu du questionnaire
# ---------------------------------------------------------------------------
AGES = ["18-21 ans", "22-25 ans", "26-30 ans", "+30 ans"]

STATUTS = ["Étudiant·e", "Alternant·e", "Salarié·e", "Indépendant·e", "En recherche d'emploi", "Autre"]

# Questions complémentaires selon la situation
CONTRATS = ["CDI", "CDD", "Intérim", "Fonctionnaire"]
REVENUS = ["< 800 €", "800 – 1 500 €", "1 500 – 2 500 €", "> 2 500 €"]
LOGEMENTS = ["Chez mes parents", "Locataire", "Logement étudiant", "Propriétaire"]
AIDES_ETUDIANT = {
    "bourse": "Je touche une bourse",
    "job": "J'ai un job étudiant",
    "apl": "Je touche les APL",
}
AIDES_RECHERCHE = {
    "are": "Je suis indemnisé·e par France Travail",
    "formation": "Je cherche une formation",
}

INTERESTS = {
    "budget": "Budget et épargne d'urgence",
    "projet": "Financement de projet",
    "bourse": "Bourse, PEA et investissement",
    "aides": "Primes et aides d'État",
}
OBJECTIVES = {
    "courant": "**Épargner** : sécuriser mon budget",
    "pea": "**Investir** : découvrir le PEA",
    "projets": "**Financer un projet** : mes aides",
}

for k in ("q_age", "q_statut", "q_contrat", "q_revenu", "q_logement"):
    ss.setdefault(k, None)

# ---------------------------------------------------------------------------
# Style
# Les sélecteurs [class*="st-key-…"] ciblent uniquement les blocs de cette page.
# ---------------------------------------------------------------------------
NAVY, BLUE, SOFT, SOFT2, MUTE = "#14213D", "#1F2BE0", "#EEF1F8", "#E2E7F6", "#5B6785"

CSS = f"""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
.stApp{{background:#E6EBF5!important;}}
.st-key-quiz,.st-key-quiz p,.st-key-quiz div,.st-key-quiz span,.st-key-quiz label,.st-key-quiz button{{font-family:'Plus Jakarta Sans',sans-serif;}}
.block-container{{padding-top:2rem!important;}}
header[data-testid="stHeader"]{{background:transparent!important;}}

/* Les éléments prennent toute la largeur dans nos blocs */
.st-key-quiz [class*="st-key-pill_"] [data-testid="stElementContainer"],.st-key-quiz [class*="st-key-pill_"] .element-container,.st-key-quiz [class*="st-key-pill_"] .stButton,
.st-key-quiz [class*="st-key-check_"] [data-testid="stElementContainer"],.st-key-quiz [class*="st-key-check_"] .element-container,.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"],
.st-key-quiz .st-key-objective [data-testid="stElementContainer"],.st-key-quiz .st-key-objective .element-container,.st-key-quiz .st-key-objective [data-testid="stRadio"],
.st-key-quiz .st-key-objective div[role="radiogroup"],.st-key-quiz .st-key-submit [data-testid="stElementContainer"],.st-key-quiz .st-key-submit .element-container,.st-key-quiz .st-key-submit .stButton{{width:100%!important;}}

/* Carte principale */
.st-key-quiz{{background:white!important;border:1px solid #E2E8F0!important;border-radius:24px!important;padding:40px!important;box-shadow:0 10px 20px rgba(15,23,42,0.05);}}
.q-top{{display:flex;justify-content:space-between;align-items:center;}}
.q-brand{{font-weight:800;color:{NAVY};font-size:15px;letter-spacing:3px;}}
.q-brand b{{color:#FFC83D;}}
.q-step{{font-size:13px;font-weight:700;color:{MUTE};background:{SOFT};padding:4px 12px;border-radius:99px;}}
.q-title{{font-size:30px;font-weight:800;color:{NAVY};margin:14px 0 4px;line-height:1.1;}}
.q-sub{{color:{MUTE};font-size:15px;margin:0;}}
.q-h{{display:flex;justify-content:space-between;align-items:baseline;margin:24px 0 10px;}}
.q-h span:first-child{{font-size:19px;font-weight:800;color:{NAVY};}}
.q-h span:last-child{{font-size:14px;color:{MUTE};font-weight:600;}}
.q-hint{{text-align:center;font-size:13px;color:{MUTE};margin:4px 0 0;min-height:18px;}}

/* Pilules (âge, situation, contrat, revenus…) : blanches, bleues une fois choisies */
.st-key-quiz [class*="st-key-pill_"] [data-testid="stHorizontalBlock"]{{gap:12px!important;}}
.st-key-quiz [class*="st-key-pill_"] button{{width:100%!important;min-height:52px!important;border-radius:99px!important;
border:2px solid {NAVY}!important;background:#FFFFFF!important;color:{NAVY}!important;box-shadow:none!important;transition:transform .1s,background .15s;}}
.st-key-quiz [class*="st-key-pill_"] button p{{color:{NAVY}!important;font-size:16px!important;font-weight:600!important;}}
.st-key-quiz [class*="st-key-pill_"] button:hover{{background:{SOFT}!important;transform:translateY(-1px);}}
.st-key-quiz [class*="st-key-pill_"] button[kind="primary"],.st-key-quiz [class*="st-key-pill_"] button[data-testid="stBaseButton-primary"]{{
background:{BLUE}!important;border-color:{BLUE}!important;box-shadow:0 6px 14px rgba(31,43,224,.3)!important;}}
.st-key-quiz [class*="st-key-pill_"] button[kind="primary"] p,.st-key-quiz [class*="st-key-pill_"] button[data-testid="stBaseButton-primary"] p{{color:#FFFFFF!important;}}

/* Bloc de questions complémentaires */
.st-key-quiz .st-key-follow{{background:#FFFFFF!important;border:2px dashed #C9D1E8!important;border-radius:22px!important;padding:6px 18px 18px!important;
margin-top:14px;animation:slidein .35s ease-out;}}
.st-key-quiz .st-key-follow .q-h{{margin-top:14px;}}
.st-key-quiz .st-key-follow .q-h span:first-child{{font-size:16px;}}
.st-key-quiz .st-key-follow [class*="st-key-pill_"] button{{min-height:44px!important;}}
.st-key-quiz .st-key-follow [class*="st-key-pill_"] button p{{font-size:14.5px!important;}}
@keyframes slidein{{from{{opacity:0;transform:translateY(-8px)}}to{{opacity:1;transform:none}}}}

/* Cases à cocher en lignes */
.st-key-quiz [class*="st-key-check_"]{{gap:10px!important;}}
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"]{{margin:0!important;}}
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label{{display:flex!important;align-items:center;width:100%!important;background:{SOFT};border:2px solid transparent;
border-radius:16px;padding:14px 16px;cursor:pointer;transition:all .12s;}}
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label:hover{{border-color:#C9D1E8;}}
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label:has(input:checked){{background:{SOFT2};}}
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label p{{font-size:16px!important;font-weight:600;color:{NAVY}!important;}}
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label:has(input:checked) p{{font-weight:800;}}
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label > div:not([data-testid]):first-of-type,
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label > span:first-child:not(:has(input)){{width:24px!important;height:24px!important;min-width:24px;border-radius:7px!important;
border:2px solid {NAVY}!important;background-color:#FFFFFF!important;margin-right:4px;}}
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label:has(input:checked) > div:not([data-testid]):first-of-type,
.st-key-quiz [class*="st-key-check_"] [data-testid="stCheckbox"] label:has(input:checked) > span:first-child:not(:has(input)){{background-color:{NAVY}!important;border-color:{NAVY}!important;}}

/* Objectif : lignes avec bouton radio, rien de coché au départ */
.st-key-quiz .st-key-objective div[role="radiogroup"]{{gap:10px!important;flex-direction:column!important;}}
.st-key-quiz .st-key-objective div[role="radiogroup"] > div{{width:100%!important;}}
.st-key-quiz .st-key-objective div[role="radiogroup"] label{{display:flex!important;align-items:center;width:100%!important;background:{SOFT};border:2px solid transparent;
border-radius:16px;padding:14px 16px!important;margin:0!important;cursor:pointer;transition:all .12s;}}
.st-key-quiz .st-key-objective div[role="radiogroup"] label:hover{{border-color:#C9D1E8;}}
.st-key-quiz .st-key-objective div[role="radiogroup"] label:has(input:checked){{background:{SOFT2};}}
.st-key-quiz .st-key-objective div[role="radiogroup"] label p{{font-size:16px!important;color:{NAVY}!important;}}
.st-key-quiz .st-key-objective [data-testid="stRadioOption"] > div > div:first-child,
.st-key-quiz .st-key-objective div[role="radiogroup"] label:not([data-testid]) > div:first-child{{width:24px!important;height:24px!important;min-width:24px;border:2px solid {NAVY}!important;background-color:#FFFFFF!important;margin-right:4px;}}
.st-key-quiz .st-key-objective [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child,
.st-key-quiz .st-key-objective div[role="radiogroup"] label:not([data-testid]):has(input:checked) > div:first-child{{border:7px solid {BLUE}!important;background-color:#FFFFFF!important;}}
.st-key-quiz .st-key-objective [data-testid="stRadioOption"] > div > div:first-child > div{{display:none!important;}}

/* Bouton de validation */
.st-key-quiz .st-key-submit{{margin-top:26px;}}
.st-key-quiz .st-key-submit button{{width:100%!important;min-height:62px!important;border-radius:99px!important;background:{NAVY}!important;border:none!important;
box-shadow:0 8px 0 #0A1226!important;transition:transform .1s;}}
.st-key-quiz .st-key-submit button p{{color:#FFFFFF!important;font-size:19px!important;font-weight:700!important;}}
.st-key-quiz .st-key-submit button:hover{{transform:translateY(-2px);}}
.st-key-quiz .st-key-submit button:active{{transform:translateY(6px);box-shadow:0 2px 0 #0A1226!important;}}
.q-error{{color:#C62828;font-weight:600;font-size:14px;text-align:center;margin-top:12px;}}
</style>
"""
st.markdown("\n".join(l for l in CSS.splitlines() if l.strip()), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Composants
# ---------------------------------------------------------------------------
def heading(title: str, right: str = "") -> None:
    st.markdown(f'<div class="q-h"><span>{title}</span><span>{right}</span></div>', unsafe_allow_html=True)


def pills(name: str, options: list[str], state_key: str, per_row: int = 2) -> None:
    """Groupe de boutons pilules à choix unique. Rien n'est sélectionné au départ."""
    with st.container(key=f"pill_{name}"):
        for i in range(0, len(options), per_row):
            row = options[i:i + per_row]
            cols = st.columns(per_row)
            for col, opt in zip(cols, row):
                selected = ss[state_key] == opt
                if col.button(opt, key=f"{name}_{opt}", type="primary" if selected else "secondary",
                              use_container_width=True):
                    ss[state_key] = None if selected else opt   # re-cliquer désélectionne
                    st.rerun()


def checks(name: str, options: dict[str, str]) -> list[str]:
    with st.container(key=f"check_{name}"):
        return [k for k, label in options.items() if st.checkbox(label, key=f"{name}_{k}")]


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
with st.container(key="quiz"):
    st.markdown(
        '<div class="q-top"><span class="q-brand"><b>●</b> YELLO</span></div>'
        '<div class="q-title">Ton profil de joueur</div>'
        '<p class="q-sub">Tes choix débloquent tes jeux et tes badges.</p>',
        unsafe_allow_html=True,
    )

    # 1. Âge
    heading("1. Ta tranche d'âge")
    pills("age", AGES, "q_age")

    # 2. Situation + questions complémentaires
    heading("2. Ta situation")
    pills("statut", STATUTS, "q_statut")

    statut = ss.q_statut
    details: dict = {}
    if statut:
        with st.container(key="follow"):
            if statut == "Étudiant·e":
                heading("Tu es plutôt…", "Plusieurs choix")
                details["aides"] = checks("etu", AIDES_ETUDIANT)
                heading("Ton logement")
                pills("logement", LOGEMENTS, "q_logement")

            elif statut in ("Alternant·e", "Salarié·e", "Indépendant·e"):
                if statut == "Salarié·e":
                    heading("Ton contrat")
                    pills("contrat", CONTRATS, "q_contrat")
                heading("Ton revenu net mensuel")
                pills("revenu", REVENUS, "q_revenu")
                heading("Ton logement")
                pills("logement", LOGEMENTS, "q_logement")

            elif statut == "En recherche d'emploi":
                heading("Ta situation actuelle", "Plusieurs choix")
                details["aides"] = checks("rech", AIDES_RECHERCHE)
                heading("Ton logement")
                pills("logement", LOGEMENTS, "q_logement")

            else:
                heading("Ton revenu net mensuel")
                pills("revenu", REVENUS, "q_revenu")

        details.update({k: ss[f"q_{k}"] for k in ("contrat", "revenu", "logement") if ss[f"q_{k}"]})

    # 3. Centres d'intérêt
    heading("3. Tes centres d'intérêt", "Plusieurs choix")
    chosen = checks("int", INTERESTS)

    # 4. Objectif
    heading("4. Ton objectif du moment")
    with st.container(key="objective"):
        objective = st.radio("Objectif", list(OBJECTIVES), format_func=OBJECTIVES.get, index=None,
                             key="q_objective", label_visibility="collapsed")

    # Validation
    with st.container(key="submit"):
        clicked = st.button("Valider et voir mon profil", key="submit_btn", use_container_width=True)

    if clicked:
        missing = None
        if not ss.q_age:
            missing = "Choisis ta tranche d'âge."
        elif not statut:
            missing = "Indique ta situation."
        elif statut == "Salarié·e" and not ss.q_contrat:
            missing = "Indique ton type de contrat."
        elif not chosen:
            missing = "Sélectionne au moins un centre d'intérêt."
        elif not objective:
            missing = "Choisis ton objectif du moment."

        if missing:
            st.markdown(f'<div class="q-error">{missing}</div>', unsafe_allow_html=True)
        else:
            profil = {
                "age": ss.q_age,
                "statut": statut,
                "details": details,          # aides, contrat, revenu, logement
                "interets": chosen,          # ["budget", "projet", "bourse", "aides"]
                "objectif": objective,       # "courant" | "pea" | "projets"
            }
            ss["profil"] = profil

            # Mise à jour de l'utilisateur (mêmes clés qu'avant + les nouvelles infos)
            user["age_group"] = ss.q_age
            user["current_track"] = objective
            user["statut"] = statut
            user["profil"] = profil
            ss["user"] = user

            try:
                api_service.submit_questionnaire(
                    user_id=user.get("id", 1),
                    objective=objective,
                    knowledge_level="intermediaire",
                    time_horizon="moyen_terme",
                )
            except Exception as e:
                st.warning(f"Réponses gardées sur cette session, mais l'envoi au serveur a échoué : {e}")

            ss["questionnaire_done"] = True
            st.switch_page("pages/2_Situation.py")