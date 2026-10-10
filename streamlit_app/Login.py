"""Écran de Connexion et d'Inscription — Yellow."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Connexion — Yellow", page_icon="🔐", layout="centered")

with open("static/css/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🔐 Accès à votre Espace Yellow")
st.caption("Banque digitale YellowBank — Environnement sécurisé.")

tab_login, tab_register = st.tabs(["Connexion", "Créer un compte"])

with tab_login:
    with st.form("login_form"):
        username = st.text_input("Identifiant ou Email", value="demo")
        password = st.text_input("Mot de passe", type="password", value="demo123")
        btn_submit = st.form_submit_button("Se connecter", type="primary", use_container_width=True)

    if btn_submit:
        res = api_service.login(username, password)
        if "error" in res:
            st.error(res["error"])
        else:
            st.session_state["user"] = res["user"]
            st.session_state["token"] = res.get("access_token", "")
            st.success(f"Bienvenue, {res['user'].get('full_name', username)} !")
            st.page_link("Home.py", label="Accéder à l'Accueil", icon="🏠")

    st.write("---")
    st.info("💡 **Compte de démonstration pré-configuré :** Identifiant `demo` / Mot de passe `demo123`")

with tab_register:
    with st.form("reg_form"):
        reg_username = st.text_input("Identifiant souhaité")
        reg_fullname = st.text_input("Prénom et Nom")
        reg_email = st.text_input("Adresse email")
        reg_password = st.text_input("Mot de passe", type="password")
        btn_reg = st.form_submit_button("Créer mon compte", use_container_width=True)

    if btn_reg:
        if not reg_username or not reg_password or not reg_email:
            st.warning("Veuillez remplir tous les champs obligatoires.")
        else:
            res_reg = api_service.register(reg_username, reg_email, reg_password, reg_fullname)
            if "error" in res_reg:
                st.error(res_reg["error"])
            else:
                st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
