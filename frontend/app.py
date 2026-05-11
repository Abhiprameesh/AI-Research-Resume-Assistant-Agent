import streamlit as st
import requests
import os

st.title("Agentic AI Career Assistant")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

user_input = st.text_input("Ask something:")

if st.button("Send"):

    payload = {
        "message": user_input
    }

    # Save uploaded file
    if uploaded_file is not None:

        save_path = os.path.abspath(
    "../backend/uploaded_resume.pdf"
)
        

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        payload["resume_path"] = save_path

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json=payload
    )

    data = response.json()

    st.write("Agent:", data["response"])