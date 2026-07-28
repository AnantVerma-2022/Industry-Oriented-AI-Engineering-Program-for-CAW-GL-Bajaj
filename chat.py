import os
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


st.title("Chatbot with LangChain and Groq")
st.caption("Ask anything and get responses from the chatbot.")

st.sidebar.title("Settings")
groq_api_key = st.sidebar.text_input("Enter your API key", type="password" )

model_name = st.sidebar.selectbox(
    "Model",
    [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b"
    ]
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
    
model = ChatGroq(
    model=model_name,
    api_key=groq_api_key,
    temperature=temperature)
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
        
    st.session_state.messages.append(
        {"role": "user", "content": user_input})
    
     # Convert Streamlit history to LangChain messages
    chat_history = [
        SystemMessage(content="You are a helpful AI assistant.")
    ]

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            chat_history.append(AIMessage(content=msg["content"]))

    
    response = model.invoke(chat_history)

    assistant_message = response.content

    with st.chat_message("assistant"):
        st.markdown(assistant_message)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_message
            }
        )
    
    
    
