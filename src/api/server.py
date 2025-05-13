from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import modules from other parts of the application
from app.core.chat import ChatEngine
from app.llm.model import LLMHandler
from app.vectordb.faiss_db import VectorStore
from app.agents.simple_agent import SimpleAgent

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
    actions_taken: list = []
    
# Initialize components
llm_handler = LLMHandler()
vector_store = VectorStore()
chat_engine = ChatEngine(llm_handler, vector_store)
agent = SimpleAgent(llm_handler)

# Define routes
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get context from vector store through chat engine
        relevant_docs = vector_store.search(request.message)
        context = ""
        if relevant_docs:
            context = chat_engine._format_context(relevant_docs)
        
        # Process with agent if requested
        actions_taken = []
        if request.use_agent:
            agent_result = agent.process_message(request.message, context)
            if agent_result["response"]:
                return ChatResponse(
                    response=agent_result["response"],
                    actions_taken=[a["action"] for a in agent_result["actions_taken"]]
                )
        
        # Use standard chat engine if no agent or agent didn't handle
        response = chat_engine.process_message(
            message=request.message,
            user_id=request.user_id
        )
        return ChatResponse(response=response, actions_taken=actions_taken)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add configuration from config directory
# This demonstrates how to access config modules
@app.on_event("startup")
async def startup_event():
    # Method 1: Direct import from config
    from config import settings
    print(f"Loaded configuration from config module") 