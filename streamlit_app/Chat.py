"""Chat avec Marcel, le conseiller IA de Yello."""

import streamlit as st
from services.api_service import api_service

st.set_page_config(page_title="Marcel — Yello", page_icon="💬", layout="wide")
ss = st.session_state

try:
    with open("static/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

if "user" not in ss or not ss["user"]:
    ss["user"] = api_service.login("demo", "demo123").get("user", {})
user = ss["user"]

WELCOME = ("Bonjour ! Je suis Marcel, ton conseiller financier. Je réponds à tes questions sur le budget, "
           "l'épargne, la Bourse, le PEA et les aides, à partir des guides officiels Yello.")
SUGGESTIONS = [
    ("account_balance", "Quels sont les avantages du PEA après 5 ans ?"),
    ("directions_car", "Comment financer mon permis à 1 € par jour ?"),
    ("savings", "Combien garder de côté pour mon matelas de sécurité ?"),
    ("pie_chart", "C'est quoi la règle 50/30/20 ?"),
]
AGENTS = {"rag": "Expert documentaire", "faq": "Réponse rapide", "chitchat": "Discussion", "market": "Marchés"}

ss.setdefault("chat_history", [{"role": "assistant", "content": WELCOME, "confidence": None}])


# ---------------------------------------------------------------------------
# Appel au backend (FastAPI → orchestrateur → agents)
# ---------------------------------------------------------------------------
def ask_marcel(question: str) -> dict:
    uid = user.get("id", 1)
    for name in ("chat", "ask", "send_chat_message", "send_message", "ask_question", "query"):
        fn = getattr(api_service, name, None)
        if not callable(fn):
            continue
        for kwargs in ({"user_id": uid, "message": question}, {"user_id": uid, "question": question},
                       {"message": question}, {"question": question}):
            try:
                res = fn(**kwargs)
                break
            except TypeError:
                continue
        else:
            try:
                res = fn(question)
            except Exception as e:
                return {"answer": f"Je n'arrive pas à joindre le serveur ({e}).", "confidence": None}
        if isinstance(res, str):
            return {"answer": res, "confidence": None}
        res = res or {}
        conf = res.get("confidence", res.get("score", res.get("confidence_score")))
        if isinstance(conf, (int, float)) and conf <= 1:
            conf = conf * 100
        
        raw_agent = res.get("sender_agent") or res.get("agent") or res.get("agent_used", "")
        agent_clean = str(raw_agent).replace("_agent", "").lower()
        
        sources_clean = []
        for s in res.get("sources", []):
            if isinstance(s, dict):
                sources_clean.append({
                    "title": s.get("title") or s.get("document_title") or s.get("source") or "Guide officiel",
                    "snippet": s.get("snippet", "")
                })
            else:
                sources_clean.append({"title": str(s)})

        return {
            "answer": res.get("answer") or res.get("content") or res.get("response") or res.get("message") or "…",
            "confidence": round(conf) if isinstance(conf, (int, float)) else None,
            "agent": agent_clean,
            "sources": sources_clean
        }
    return {"answer": "Le service de chat n'est pas encore branché dans api_service.py.", "confidence": None}


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
NAVY, BLUE, GOLD, SOFT, MUTE = "#14213D", "#1F2BE0", "#FFC83D", "#EEF1F8", "#5B6785"
CSS = f"""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL@24,500,1" rel="stylesheet">
<style>
.stApp{{background:#E6EBF5!important;}}
.block-container,[data-testid="stMainBlockContainer"]{{max-width:980px!important;padding:1.6rem 2rem 7rem!important;}}
[data-testid="stMain"] p,[data-testid="stMain"] div,[data-testid="stMain"] button,[data-testid="stMain"] textarea{{font-family:'Plus Jakarta Sans',sans-serif;}}
.ms{{font-family:'Material Symbols Rounded'!important;font-weight:normal;font-style:normal;line-height:1;display:inline-block;
  -webkit-font-feature-settings:'liga';font-feature-settings:'liga';font-variation-settings:'FILL' 1;}}

/* En-tête */
.head{{display:flex;align-items:center;gap:20px;background:linear-gradient(135deg,#1A2B5C,#101B3A);border-radius:28px;padding:22px 26px;margin-top:10px;
  box-shadow:0 14px 34px rgba(20,33,61,.22);flex-wrap:wrap;}}
.av{{width:68px;height:68px;border-radius:22px;background:linear-gradient(160deg,{GOLD},#F59E0B);display:flex;align-items:center;justify-content:center;position:relative;flex-shrink:0;}}
.av .ms{{font-size:40px;color:{NAVY};}}
.av:after{{content:"";position:absolute;right:-3px;bottom:-3px;width:18px;height:18px;border-radius:50%;background:#22C55E;border:3px solid #101B3A;}}
.head h1{{color:#fff;font-size:28px;font-weight:800;margin:0;line-height:1.1;}}
.head .st{{color:#93A3C8;font-size:14px;font-weight:600;margin-top:4px;}}
.head .st b{{color:#7CF0A9;}}
.pills{{display:flex;gap:8px;flex-wrap:wrap;margin-left:auto;}}
.pill{{display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.1);color:#fff;font-size:13px;font-weight:700;padding:7px 12px;border-radius:99px;}}
.pill .ms{{font-size:18px;color:{GOLD};}}

/* Suggestions */
.sug-t{{font-size:14px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:{MUTE};margin:26px 0 10px;}}
[class*="st-key-sug_"] button{{width:100%;min-height:64px!important;justify-content:flex-start!important;text-align:left!important;background:#fff!important;
  border:2px solid #DCE2EF!important;border-radius:18px!important;box-shadow:0 6px 16px rgba(20,33,61,.05)!important;transition:all .12s;padding:10px 16px!important;}}
[class*="st-key-sug_"] button:hover{{border-color:{BLUE}!important;transform:translateY(-2px);}}
[class*="st-key-sug_"] button p{{color:{NAVY}!important;font-weight:700!important;font-size:15px!important;text-align:left!important;}}
[class*="st-key-sug_"] button [data-testid="stIconMaterial"]{{color:{BLUE}!important;font-size:24px!important;}}

/* Messages */
[data-testid="stChatMessage"]{{background:transparent!important;padding:4px 0!important;gap:12px!important;align-items:flex-start!important;justify-content:flex-start!important;}}
[data-testid="stChatMessageContent"],[data-testid="stChatMessageContent"] *{{margin-left:0!important;margin-right:0!important;}}
[data-testid="stChatMessageContent"] [data-testid="stVerticalBlock"]{{gap:0!important;}}
[data-testid="stChatMessageContent"] [data-testid="stMarkdownContainer"],[data-testid="stChatMessageContent"] [data-testid="stMarkdown"],[data-testid="stChatMessageContent"] [data-testid="stElementContainer"]{{margin-bottom:0!important;margin-top:0!important;height:auto!important;}}
[data-testid="stChatMessageContent"] p{{margin-bottom:0!important;}}
[data-testid="stChatMessageContent"] [data-testid="stElementContainer"]:has(.meta:empty){{display:none;}}
[data-testid="stChatMessageAvatarCustom"]{{border-radius:14px!important;width:42px!important;height:42px!important;min-width:42px;}}
[class*="st-key-msg_bot"] [data-testid="stChatMessageAvatarCustom"]{{background:linear-gradient(160deg,{GOLD},#F59E0B)!important;color:{NAVY}!important;}}
[class*="st-key-msg_user"] [data-testid="stChatMessageAvatarCustom"]{{background:{BLUE}!important;color:#fff!important;}}
[data-testid="stChatMessageContent"]{{flex:0 1 auto!important;width:auto!important;max-width:720px;border-radius:6px 22px 22px 22px;padding:12px 18px!important;
  background:#fff;box-shadow:0 6px 16px rgba(20,33,61,.06);}}
[data-testid="stChatMessageContent"] p{{color:{NAVY};font-size:15.5px;line-height:1.6;margin:0;}}
[class*="st-key-msg_user"] [data-testid="stChatMessage"]{{flex-direction:row-reverse;}}
[class*="st-key-msg_user"] [data-testid="stChatMessageContent"]{{background:{NAVY};border-radius:22px 6px 22px 22px;}}
[class*="st-key-msg_user"] [data-testid="stChatMessageContent"] p{{color:#fff;}}
.head{{margin-bottom:18px;}}
.meta{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;}}
.tag{{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;font-weight:700;padding:4px 10px;border-radius:99px;background:{SOFT};color:{NAVY};}}
.tag .ms{{font-size:16px;}}
.tag.hi{{background:#DCFCE7;color:#166534;}}
.tag.mid{{background:#FFF3C4;color:#8A5A00;}}
.tag.lo{{background:#FDE2E2;color:#991B1B;}}

/* Zone de saisie */
[data-testid="stBottom"] > div{{background:#E6EBF5!important;}}
[data-testid="stChatInput"]{{border-radius:22px!important;border:2px solid #DCE2EF!important;background:#fff!important;box-shadow:0 10px 26px rgba(20,33,61,.1);}}
[data-testid="stChatInput"]:focus-within{{border-color:{BLUE}!important;}}
[data-testid="stChatInputSubmitButton"]{{background:{NAVY}!important;border-radius:14px!important;color:#fff!important;}}
.legal{{text-align:center;color:{MUTE};font-size:12.5px;margin-top:14px;}}
</style>
"""
st.markdown("\n".join(l for l in CSS.splitlines() if l.strip()), unsafe_allow_html=True)


def html(s: str) -> None:
    st.markdown("\n".join(l.strip() for l in s.splitlines() if l.strip()), unsafe_allow_html=True)


def meta(msg: dict) -> str:
    out = []
    conf = msg.get("confidence")
    if isinstance(conf, (int, float)):
        cls = "hi" if conf >= 80 else ("mid" if conf >= 50 else "lo")
        out.append(f'<span class="tag {cls}"><span class="ms">verified</span>Confiance {conf} %</span>')
    agent = AGENTS.get(msg.get("agent", ""))
    if agent:
        out.append(f'<span class="tag"><span class="ms">hub</span>{agent}</span>')
    for s in msg.get("sources", [])[:3]:
        label = s.get("title") or s.get("source") if isinstance(s, dict) else str(s)
        out.append(f'<span class="tag"><span class="ms">description</span>{label}</span>')
    return f'<div class="meta">{"".join(out)}</div>' if out else ""


AVATARS = {"assistant": ":material/smart_toy:", "user": ":material/person:"}

# ---------------------------------------------------------------------------
# En-tête
# ---------------------------------------------------------------------------
html(f"""<div class="head"><div class="av"><span class="ms">smart_toy</span></div>
<div><h1>Marcel</h1><div class="st"><b>● En ligne</b> · ton conseiller financier Yello</div></div>
<div class="pills"><span class="pill"><span class="ms">menu_book</span>Guides officiels</span>
<span class="pill"><span class="ms">lock</span>IA 100 % locale</span></div></div>""")

# ---------------------------------------------------------------------------
# Conversation
# ---------------------------------------------------------------------------
def bubble(i: int, role: str):
    """Message encadré d'un conteneur nommé : permet de styler différemment Marcel et l'utilisateur."""
    box = st.container(key=f"msg_{'user' if role == 'user' else 'bot'}_{i}")
    return box.chat_message(role, avatar=AVATARS[role])


for i, msg in enumerate(ss.chat_history):
    with bubble(i, msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            html(meta(msg))

pending = None
if len(ss.chat_history) == 1:
    html('<div class="sug-t">Tu peux commencer par</div>')
    cols = st.columns(2)
    for i, (ic, q) in enumerate(SUGGESTIONS):
        with cols[i % 2]:
            with st.container(key=f"sug_{i}"):
                if st.button(q, key=f"sug_btn_{i}", icon=f":material/{ic}:", use_container_width=True):
                    pending = q

typed = st.chat_input("Pose ta question à Marcel…")
question = typed or pending
if question:
    ss.chat_history.append({"role": "user", "content": question})
    with bubble(len(ss.chat_history) - 1, "user"):
        st.markdown(question)
    with bubble(len(ss.chat_history), "assistant"):
        with st.spinner("Marcel cherche dans les guides…"):
            res = ask_marcel(question)
        st.markdown(res["answer"])
        html(meta(res))
    ss.chat_history.append({"role": "assistant", "content": res["answer"], **{k: v for k, v in res.items() if k != "answer"}})
    if pending:
        st.rerun()

html('<p class="legal">Marcel donne une information générale, pas un conseil personnalisé en investissement.</p>')
