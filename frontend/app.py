import streamlit as st
import requests

st.title("Agentic AI Career Assistant")

user_input = st.text_input("Ask something:")

if st.button("Send"):

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"message": user_input}
    )

    data = response.json()

    st.write("Agent:", data["response"])