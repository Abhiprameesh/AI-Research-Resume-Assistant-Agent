import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Agentic AI Career Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS for better UI
st.markdown("""
<style>
    .stChatInputContainer {
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 Document Upload")
    
    doc_type = st.radio(
        "Select Document Type",
        ["Resume", "Research Paper"],
        help="Select 'Resume' to get personalized career advice. Select 'Research Paper' to query its contents."
    )
    
    uploaded_file = st.file_uploader(
        f"Upload your {doc_type} (PDF)",
        type=["pdf"]
    )
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN AREA ---
st.title("✨ Agentic AI Career Assistant")
st.markdown("Your personal AI agent for career growth, resume building, and research analysis.")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask something...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "message": user_input,
        "doc_type": doc_type
    }

    # Save uploaded document
    if uploaded_file is not None:
        save_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "backend", "uploaded_resume.pdf")
        )

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        payload["resume_path"] = save_path

    # Send request to backend with a spinner
    with st.spinner("Agent is thinking..."):
        try:
            response = requests.post("http://127.0.0.1:8000/chat", json=payload)
            data = response.json()
            agent_response = data.get("response", "No response from agent.")
        except Exception as e:
            agent_response = f"Error connecting to backend: {str(e)}"

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": agent_response})

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(agent_response)