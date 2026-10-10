"""Page de Chat avec le Marcel — Yello."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="8. Marcel — Yello", page_icon="💬", layout="wide")

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    login_res = api_service.login("demo", "demo123")
    st.session_state["user"] = login_res.get("user", {})

user = st.session_state["user"]

st.title("💬 Marcel")
st.caption("🛡️ Réponses officielles basées sur les guides certifiés Yello (Bourse, PEA, Budget, Prêts & Aides d'État).")

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {
            "role": "assistant",
            "content": "Bonjour ! Je suis votre Marcel, votre assistant financier intelligent. Je réponds à toutes vos questions bancaires et réglementaires à partir de nos guides certifiés. Comment puis-je vous aider ?",
            "confidence": 1.0,
            "sources": []
        }
    ]

# Frame d'historique
for msg in st.session_state["chat_messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and msg.get("confidence") is not None:
            c_score = msg["confidence"]
            st.caption(f"🟢 **Certitude documentaire : {int(c_score * 100)}%**")

            sources = msg.get("sources", [])
            if sources:
                with st.expander("📚 Sources officielles citées"):
                    for s in sources:
                        st.markdown(f"**Guide :** `{s.get('document_title', 'Guide Officiel')}`")
                        st.markdown(f"> *« {s.get('snippet', '')} »*")

# Zone de saisie
prompt = st.chat_input("Posez votre question (ex: Quels sont les avantages du PEA après 5 ans ? Comment financer son permis à 1€ ?)")

if prompt:
    st.session_state["chat_messages"].append({"role": "user", "content": prompt})

    with st.spinner("Recherche dans les guides certifiés Yello..."):
        resp = api_service.send_chat_message(
            user_id=user.get("id", 1),
            message=prompt,
            track=user.get("current_track", "courant")
        )

    st.session_state["chat_messages"].append({
        "role": "assistant",
        "content": resp.get("content", ""),
        "confidence": resp.get("confidence_score", 0.95),
        "sources": resp.get("sources", [])
    })
    st.rerun()
