"""Interface de Discussion avec le Conseiller IA Augmenté (RAG & FAQ)."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Conseiller IA — Archipel", page_icon="💬", layout="wide")

with open("static/css/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "user" not in st.session_state:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

# Historique des messages en session
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {
            "role": "assistant",
            "content": "Bonjour ! Je suis votre conseiller d'information financière Archipel. Je réponds à vos questions en m'appuyant strictement sur nos guides officiels et les règles bancaires. N'hésitez pas à me solliciter.",
            "confidence": 1.0,
            "sources": [],
            "actions": []
        }
    ]

st.title("💬 Conseiller d'Information Financière")
st.caption("🛡️ Déontologie : L'agent informe et vous guide en toute neutralité. Aucune opération bancaire n'est exécutée sans votre accord explicite.")

# Suggestions rapides
st.write("##### Questions fréquentes :")
s_col1, s_col2, s_col3 = st.columns(3)
with s_col1:
    if st.button("📈 Fiscalité du PEA après 5 ans ?", use_container_width=True):
        st.session_state["user_input_prompt"] = "Comment fonctionne la fiscalité du PEA après 5 ans ?"
with s_col2:
    if st.button("🔒 Vol de carte : faire opposition", use_container_width=True):
        st.session_state["user_input_prompt"] = "Comment faire opposition sur ma carte bancaire ?"
with s_col3:
    if st.button("🎁 Quelles sont les aides au permis ?", use_container_width=True):
        st.session_state["user_input_prompt"] = "Quelles sont les aides pour financer le permis de conduire ?"

st.divider()

# Affichage de l'historique
for msg in st.session_state["chat_messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        # Affichage du badge de confiance et des sources pour les réponses de l'assistant
        if msg["role"] == "assistant" and msg.get("confidence") is not None:
            c_score = msg["confidence"]
            if c_score >= 0.90:
                badge_color = "🟢"
                conf_text = "Très haute certitude"
            elif c_score >= 0.70:
                badge_color = "🟡"
                conf_text = "Certitude satisfaisante"
            else:
                badge_color = "🟠"
                conf_text = "Information indicative (validation conseiller conseillée)"

            st.caption(f"{badge_color} **Score de confiance RAG : {int(c_score * 100)}%** ({conf_text})")

            # Affichage des sources citées
            sources = msg.get("sources", [])
            if sources:
                with st.expander("📚 Consulter les sources documentaires certifiées"):
                    for s in sources:
                        st.markdown(f"**Document :** `{s.get('document_title', 'Guide Officiel')}`")
                        st.markdown(f"> *« {s.get('snippet', '')} »*")

            # Actions suggérées
            actions = msg.get("actions", [])
            if actions:
                st.write("**Action recommandée :**")
                for act in actions:
                    if st.button(act.get("label", "Action"), key=f"act_{act.get('label')}"):
                        st.success(f"Action '{act.get('label')}' prise en compte. Accédez à votre tableau de bord.")

# Zone de saisie utilisateur
prompt = st.chat_input("Posez votre question (ex: Quels sont les plafonds de carte ? Comment ouvrir un PEA ?)")

# Prise en compte si clic sur suggestion
if "user_input_prompt" in st.session_state and st.session_state["user_input_prompt"]:
    prompt = st.session_state.pop("user_input_prompt")

if prompt:
    # 1. Ajouter le message utilisateur
    st.session_state["chat_messages"].append({"role": "user", "content": prompt})

    # 2. Appel au backend RAG
    with st.spinner("Recherche dans la base de connaissances et formulation..."):
        resp = api_service.send_chat_message(
            user_id=user.get("id", 1),
            message=prompt,
            track=user.get("current_track", "courant")
        )

    # 3. Ajouter la réponse
    st.session_state["chat_messages"].append({
        "role": "assistant",
        "content": resp.get("content", ""),
        "confidence": resp.get("confidence_score", 0.90),
        "sources": resp.get("sources", []),
        "actions": resp.get("suggested_actions", [])
    })
    st.rerun()
