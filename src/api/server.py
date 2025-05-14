from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import modules from other parts of the application
from src.core.chat import ChatEngine


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Mini Chat",
    description="A minimalistic chatbot API with FAISS vector database",
    version="0.1.0"
)

# Define request/response models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    use_agent: bool = False

class ChatResponse(BaseModel):
    response: str
    actions_taken: list = None

chat_engine = ChatEngine()

# Define routes
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:

        # Use standard chat engine if no agent or agent didn't handle
        response = await chat_engine.process_message(
            message=request.message,
            user_id=request.user_id
        )
        return ChatResponse(response=response, actions_taken=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

