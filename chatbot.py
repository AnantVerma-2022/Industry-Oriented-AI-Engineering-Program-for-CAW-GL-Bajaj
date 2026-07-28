import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. "
    "Use previous conversation whenever relevant."
)

model_name = "llama-3.1-8b-instant"

model = ChatGroq(
    model=model_name,
    temperature=0.7
)

parser = StrOutputParser()

chain = model | parser

def chat_with_groq(user_input: str, chat_history: list) -> str:
    
    """
    history = [
        {"role": "user", "content": "..."}
        {"role": "assistant", "content": "..."}
        ]
    """
    
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
            
    messages.append(HumanMessage(content=user_input))
    
    response = chain.invoke(messages)
    
    return response