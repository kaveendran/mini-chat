from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import uvicorn
# Import modules from other parts of the application
from src.core.chat import ChatEngine
from src.agents.intent_classifiers import classify_intent
from src.agents.simple_agent import mail_agent
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
    user_id:str
    actions_taken: list = None


chat_engine = ChatEngine()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:

        ## memory that can be used by the indent_classifier
        memory = chat_engine.memory.get_user_memory(request.user_id)

        # # classify the indent
        indent = await classify_intent(memory,request.message)
        print(indent)

        if indent is 'agent':
            agent_out = mail_agent(
                user_id=request.user_id,
                user_input=request.message
            )
            request.message = request.message + "Agent output :" + agent_out



        # This memory also can be used by the agent also ??

        # Use standard chat engine if no agent or agent didn't handle
        response = await chat_engine.process_message(
            message=request.message,
            user_id=request.user_id
        )
        print(response)

        return ChatResponse(response=response, actions_taken=[],user_id=request.user_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# run_server.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.api.server:app", host="127.0.0.1", port=8888, reload=True)
