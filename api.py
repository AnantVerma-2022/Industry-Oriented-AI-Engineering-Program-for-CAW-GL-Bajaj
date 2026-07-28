from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chat_with_groq

app = FastAPI(title = 'LangChain Groq Chatbot API', description = 'API for interacting with the LangChain Groq Chatbot', version = '1.0.0')


class ChatRequest(BaseModel):
    message: str
    history: list = []
    
class ChatResponse(BaseModel):
    response: str
    

@app.post("/chat", response_model=ChatResponse)
def chatbot(request: ChatRequest):
    response = chat_with_groq(request.message, request.history)
    return {"response": response}
