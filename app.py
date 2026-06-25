import streamlit as st
import os

from create_database1 import create_database
from rag import get_answer

st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------
# CUSTOM CSS
# -----------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #0F172A,
        #111827,
        #1E293B
    );
}

.block-container{
    padding-top: 1rem;
    max-width: 1200px;
}

/* HERO SECTION */

.hero{
    text-align:center;
    padding:30px;
    margin-bottom:25px;
}

.hero h1{
    font-size:4rem;
    font-weight:800;
    background: linear-gradient(
        90deg,
        #60A5FA,
        #A855F7,
        #EC4899
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p{
    font-size:1.2rem;
    color:#CBD5E1;
}

/* CARD */

.upload-card{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(15px);
    border:1px solid rgba(255,255,255,0.1);
    padding:25px;
    border-radius:25px;
    margin-bottom:25px;
}

/* CHAT */

.stChatMessage{
    border-radius:20px;
    padding:10px;
}

[data-testid="stChatMessageContent"]{
    border-radius:15px;
}

/* USER MESSAGE */

.stChatMessage[data-testid="chat-message-user"]{
    background:#1E293B;
    border:1px solid #334155;
}

/* BOT MESSAGE */

.stChatMessage[data-testid="chat-message-assistant"]{
    background:#111827;
    border:1px solid #374151;
}

/* BUTTON */

.stButton button{
    width:100%;
    border-radius:15px;
    height:50px;
    font-size:18px;
    font-weight:bold;
    background:linear-gradient(
        90deg,
        #3B82F6,
        #8B5CF6
    );
    color:white;
    border:none;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"]{
    background:rgba(255,255,255,0.03);
    padding:15px;
    border-radius:20px;
}

/* CHAT INPUT */

[data-testid="stChatInput"]{
    border-radius:20px;
}

.footer{
    text-align:center;
    color:#94A3B8;
    padding-top:20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# HERO
# -----------------------

st.markdown("""
<div class="hero">
    <h1>🤖 PDF AI Assistant</h1>
    <p>Upload any PDF and chat with your documents using Mistral AI</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# TWO COLUMN LAYOUT
# -----------------------

left,right = st.columns([1,2])

with left:

    st.markdown("""
    <div class="upload-card">
        <h3>📄 Upload Document</h3>
        <p>Supported Format: PDF</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_file:

        with open("temp.pdf","wb") as f:
            f.write(uploaded_file.getbuffer())

        if "db_created" not in st.session_state:

            with st.spinner("Creating AI Knowledge Base..."):

                create_database("temp.pdf")

            st.session_state.db_created = True

            st.success("✅ Document Ready")

with right:

    st.markdown("""
    <div class="upload-card">
        <h3>💬 AI Chat</h3>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input(
        "Ask something from your PDF..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = get_answer(question)

            st.write(answer)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

st.markdown("""
<div class="footer">
Built with ❤️ Streamlit • LangChain • Mistral AI • ChromaDB
</div>
""", unsafe_allow_html=True)