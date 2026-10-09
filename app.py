
import os
import streamlit as st
from google import genai

# ==================================================
# XENO // FUTURISTIC AI INTERFACE
# ==================================================

st.set_page_config(
    page_title="XENO // AI SYSTEM",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL = "gemini-3.8-flash"


SYSTEM_PROMPT = """
Tu es Xeno, une intelligence artificielle personnelle, futuriste et professionnelle.
Tu réponds en français par défaut.

IDENTITÉ :
- Ton nom est Xeno.
- Ton créateur est Nader.
- Si quelqu'un demande « Qui est ton créateur ? »,
  « Qui t'a créé ? », « Qui t'a programmé ? » ou une question équivalente,
  réponds clairement : « Mon créateur est Nader. »
- Ne prétends pas connaître d'autres détails sur Nader si l'utilisateur
  ne les a pas fournis.
- Ne mentionne pas le nom du fournisseur du modèle dans tes réponses,
  sauf si l'utilisateur pose explicitement une question technique à ce sujet.

COMPORTEMENT :
- Réponds clairement, naturellement et de façon utile.
- Privilégie les réponses directes et rapides.
- Aide à programmer, apprendre, créer et résoudre des problèmes.
- Pour le code, donne des exemples complets et faciles à utiliser.
"""

# ==================================================
# DESIGN : DARK ALIEN / NEON BLUE
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #050810;
    --panel: #0A1120;
    --panel2: #0D1829;
    --line: #172D46;
    --blue: #168BFF;
    --cyan: #42E8FF;
    --white: #EAF6FF;
    --muted: #8098B4;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 50% -20%, #102748 0%, transparent 50%),
        linear-gradient(180deg, #050810 0%, #070C16 100%);
    color: var(--white);
}

header[data-testid="stHeader"] {
    background: rgba(5, 8, 16, 0.9);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080E19, #050810);
    border-right: 1px solid #17314C;
}

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.6rem;
    padding-bottom: 7rem;
}

.xeno-brand {
    font-family: 'Orbitron', sans-serif;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 5px;
    color: white;
    text-shadow: 0 0 20px rgba(22,139,255,.35);
}

.xeno-brand span {
    color: var(--cyan);
}

.brand-line {
    height: 2px;
    width: 100%;
    background: linear-gradient(90deg, var(--blue), var(--cyan), transparent);
    margin: 12px 0 18px;
}

.eyebrow {
    font-family: 'Orbitron', sans-serif;
    color: var(--cyan);
    font-size: 10px;
    letter-spacing: 3px;
}

.system-status {
    display: inline-block;
    border: 1px solid #145174;
    background: rgba(10, 50, 76, .4);
    color: #72E9FF;
    border-radius: 5px;
    padding: 7px 12px;
    font-size: 11px;
    letter-spacing: 1px;
}

.hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 42px 18px 32px;
    margin: 12px 0 24px;
    border: 1px solid #183552;
    border-radius: 18px;
    background:
        radial-gradient(ellipse at 50% 0%, rgba(22,139,255,.17), transparent 65%),
        linear-gradient(135deg, rgba(13,24,41,.97), rgba(5,10,19,.97));
    box-shadow: 0 0 45px rgba(0,100,255,.06), inset 0 0 25px rgba(22,139,255,.025);
}

.hero h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(30px, 5vw, 52px);
    letter-spacing: 5px;
    margin: 12px 0;
    color: white;
}

.hero h1 span {
    color: var(--cyan);
    text-shadow: 0 0 24px rgba(66,232,255,.3);
}

.hero p {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.8;
}

.hero-rule {
    width: 110px;
    height: 2px;
    margin: 18px auto;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
}

.section-label {
    color: #8FAAC8;
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    letter-spacing: 2px;
    margin: 24px 0 12px;
}

div[data-testid="stChatMessage"] {
    background: rgba(10,17,32,.85);
    border: 1px solid #19314B;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
}

div[data-testid="stChatMessage"]:has([data-testid="stMarkdownContainer"]) {
    box-shadow: 0 4px 20px rgba(0,0,0,.08);
}

[data-testid="stChatInput"] {
    border: 1px solid #24577C !important;
    border-radius: 12px !important;
    background: #080F1C !important;
    box-shadow: 0 0 24px rgba(22,139,255,.06);
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 18px rgba(66,232,255,.12);
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

.stButton > button {
    width: 100%;
    min-height: 43px;
    border: 1px solid #1A3855;
    border-radius: 9px;
    color: #D9ECFF;
    background: linear-gradient(135deg, #0C1727, #09111E);
    transition: all .2s ease;
}

.stButton > button:hover {
    color: white;
    border-color: var(--cyan);
    background: #10253B;
    box-shadow: 0 0 18px rgba(22,139,255,.12);
}

div[data-testid="stMetric"] {
    background: #0A1422;
    border: 1px solid #18314B;
    padding: 12px;
    border-radius: 10px;
}

div[data-testid="stMetricLabel"] {
    color: var(--muted);
}

div[data-testid="stMetricValue"] {
    color: var(--cyan);
    font-family: 'Orbitron', sans-serif;
}

hr {
    border-color: #172D46;
}

.stCaption, [data-testid="stCaptionContainer"] {
    color: #8196AF;
}

.stAlert {
    border-radius: 10px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

.system-footer {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 9px;
    letter-spacing: 2px;
    color: #45627F;
    padding: 20px 0;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# GEMINI CLIENT
# ==================================================

@st.cache_resource
def get_client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY est introuvable. Vérifie la variable "
            "d'environnement Windows."
        )
    return genai.Client(api_key=key)


# ==================================================
# SESSION
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def new_conversation():
    st.session_state.messages = []
    st.session_state.previous_interaction_id = None
    st.session_state.pending_prompt = None


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown(
        '<div class="xeno-brand">XE<span>NO</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="brand-line"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="eyebrow">ARTIFICIAL INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button("＋  NOUVELLE SESSION", use_container_width=True):
        new_conversation()
        st.rerun()

    st.write("")
    st.markdown('<div class="section-label">SYSTEME</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="system-status">● CONSOLE ACTIVE</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    st.caption("MOTEUR XENO")
    st.code("XENO CORE", language=None)

    st.caption("INTERFACE")
    st.markdown("`DARK MODE` · `NEON BLUE`")

    st.divider()

    st.markdown('<div class="section-label">OUTILS RAPIDES</div>',
                unsafe_allow_html=True)

    if st.button("⌘  Programmation"):
        st.session_state.pending_prompt = (
            "Aide-moi à programmer un projet étape par étape."
        )
        st.rerun()

    if st.button("◈  Apprendre l'IA"):
        st.session_state.pending_prompt = (
            "Apprends-moi les bases de l'intelligence artificielle."
        )
        st.rerun()

    if st.button("⟢  Mode créativité"):
        st.session_state.pending_prompt = (
            "Propose-moi une idée originale de projet technologique."
        )
        st.rerun()

    if st.button("▤  Rédaction"):
        st.session_state.pending_prompt = (
            "Aide-moi à écrire un texte clair et professionnel."
        )
        st.rerun()

    st.divider()

    if st.button("⌫  EFFACER LA CONVERSATION"):
        new_conversation()
        st.rerun()

    st.markdown(
        '<div class="system-footer">XENO CORE // V1.1</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# HEADER
# ==================================================

header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        '<div class="eyebrow">PERSONAL INTELLIGENCE SYSTEM</div>',
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        '<div style="text-align:right;">'
        '<span class="system-status">● EN LIGNE</span>'
        '</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# WELCOME SCREEN
# ==================================================

if not st.session_state.messages:
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">SYSTEME INITIALISE</div>
        <h1>WELCOME TO <span>XENO</span></h1>
        <div class="hero-rule"></div>
        <p>
            Intelligence connectée. Interface nouvelle génération.<br>
            Pose une question, explore une idée ou lance un projet.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">SELECTIONNER UNE OPERATION</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        if st.button("⌘   DEVELOPPER UN PROGRAMME"):
            st.session_state.pending_prompt = (
                "Aide-moi à développer un programme, avec un plan clair."
            )
            st.rerun()

        if st.button("◈   EXPLORER L'INTELLIGENCE ARTIFICIELLE"):
            st.session_state.pending_prompt = (
                "Explique-moi un concept important de l'IA."
            )
            st.rerun()

    with c2:
        if st.button("⟢   GENERER UNE IDEE"):
            st.session_state.pending_prompt = (
                "Donne-moi trois idées de projets futuristes réalisables."
            )
            st.rerun()

        if st.button("▤   REDIGER UN TEXTE"):
            st.session_state.pending_prompt = (
                "Aide-moi à rédiger un texte professionnel."
            )
            st.rerun()

    st.write("")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("MESSAGES", len(st.session_state.messages))

    with metric2:
        st.metric("MODE", "ONLINE")

    with metric3:
        st.metric("INTERFACE", "ALIEN")


# ==================================================
# CHAT HISTORY
# Aucun avatar personnalisé : aucun bonhomme.
# ==================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ==================================================
# INPUT
# ==================================================

typed_prompt = st.chat_input("ENTRER UN MESSAGE POUR XENO...")

prompt = typed_prompt

if not prompt and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# ==================================================
# STREAMING RESPONSE
# ==================================================

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        text_parts = []

        try:
            client = get_client()

            options = {
                "model": MODEL,
                "input": prompt,
                "system_instruction": SYSTEM_PROMPT,
                "stream": True,
            }

            previous_id = st.session_state.previous_interaction_id

            if previous_id:
                options["previous_interaction_id"] = previous_id

            with st.spinner("Connexion au moteur Xeno..."):
                stream = client.interactions.create(**options)

            interaction_id = None

            for event in stream:
                event_type = getattr(event, "event_type", "")

                # Capturer l'identifiant de la conversation si disponible.
                interaction = getattr(event, "interaction", None)
                event_id = getattr(interaction, "id", None)

                if event_id:
                    interaction_id = event_id

                # Certains événements exposent le texte sous delta.text.
                delta = getattr(event, "delta", None)
                chunk = getattr(delta, "text", None) if delta else None

                if (
                    chunk
                    and event_type in (
                        "content.delta",
                        "step.delta",
                    )
                ):
                    text_parts.append(chunk)
                    placeholder.markdown("".join(text_parts) + " ▌")

            answer = "".join(text_parts).strip()

            if not answer:
                answer = (
                    "Je n'ai reçu aucun texte. Réessaie ta question. "
                    "Si le problème continue, vérifie la compatibilité "
                    "du modèle avec le streaming."
                )

            placeholder.markdown(answer)

            if interaction_id:
                st.session_state.previous_interaction_id = interaction_id

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })

        except Exception as error:
            placeholder.error("Le moteur Xeno a rencontré un problème.")
            st.caption(f"Détail technique : {error}")

            # Ne pas enregistrer une réponse d'erreur comme réponse IA.

# ==================================================
# FOOTER
# ==================================================

st.markdown(
    '<div class="system-footer">'
    'XENO AI SYSTEM  //  DARK INTERFACE  //  CONNECTION SECURISEE PAR API'
    '</div>',
    unsafe_allow_html=True,
)
