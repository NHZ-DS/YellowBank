"""Page de Sélection de Parcours — Yello."""

import streamlit as st
import streamlit.components.v1 as components
import os
from services.api_service import api_service

st.set_page_config(page_title="3. Le Plateau — Yello", page_icon="🧭", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

st.title("🧭 Le Plateau d'Évolution")
st.write("Retrouvez l'intégralité de vos parcours financiers sur le plateau interactif ci-dessous.")

# Boutons invisibles pour la navigation depuis le Javascript
st.button("HIDDEN_GO_BUDGET", key="hidden_go_budget", on_click=lambda: st.switch_page("pages/4_ParcoursCourant.py"))
st.button("HIDDEN_GO_PEA", key="hidden_go_pea", on_click=lambda: st.switch_page("pages/5_ParcoursPEA.py"))
st.button("HIDDEN_GO_PROJETS", key="hidden_go_projets", on_click=lambda: st.switch_page("pages/6_ParcoursProjet.py"))

st.markdown("""<style>
button:contains('HIDDEN_GO_') { display: none !important; }
div:has(button[kind="secondary"]):has(div:contains("HIDDEN_GO_")) { display: none !important; }
</style>""", unsafe_allow_html=True)

# On lit le fichier HTML interactif que nous avons généré et on l'intègre dans Streamlit
html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "plateau_interactif.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as html_file:
        source_code = html_file.read()
        
        # Injection de l'état Python dans le Javascript du plateau
        user_state = st.session_state.get("user", {})
        pea_level = user_state.get("pea_level", 0)
        budget_level = user_state.get("budget_level", 0)
        projets_level = user_state.get("projets_level", 0)
        
        # On remplace l'état initial par les niveaux sauvegardés (index 1: Budget, 10: Investir, 11: Projets)
        done_array_str = f"done: [0,{budget_level},0,0,0,0,0,0,0,0,{pea_level},{projets_level},0,0,0,0]"
        source_code = source_code.replace("done: Array(16).fill(0)", done_array_str)
        
        components.html(source_code, height=1300, scrolling=True)
else:
    st.error(f"Le fichier du plateau interactif est introuvable au chemin : {html_path}")

