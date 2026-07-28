import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.title("AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    history = st.session_state.messages

    payload = {
        "message": user_input,
        "history": history
    }

    response = requests.post(
        API_URL,
        json=payload
    )

    answer = response.json()["response"]

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)