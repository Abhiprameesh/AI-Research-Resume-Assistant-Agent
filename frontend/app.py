import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Agentic AI Career Assistant",
    layout="centered"
)

st.title("Agentic AI Career Assistant")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload resume
uploaded_file = st.file_uploader(
    "Upload PDF (Resume or Research Paper)",
    type=["pdf"]
)

# Display previous chat messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Chat input
user_input = st.chat_input(
    "Ask something..."
)

if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Show user message
    with st.chat_message("user"):

        st.markdown(user_input)

    payload = {
        "message": user_input
    }

    # Save uploaded resume
    if uploaded_file is not None:

        save_path = os.path.abspath(
            "../backend/uploaded_resume.pdf"
        )

        with open(save_path, "wb") as f:

            f.write(uploaded_file.getbuffer())

        payload["resume_path"] = save_path

    # Send request to backend
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json=payload
    )

    data = response.json()

    agent_response = data["response"]

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": agent_response
        }
    )

    # Show assistant message
    with st.chat_message("assistant"):

        st.markdown(agent_response)