from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import uvicorn
# Import modules from other parts of the application
from src.core.chat import ChatEngine
from src.agents.intent_classifiers import classify_intent
from src.agents.simple_agent import mail_agent
from src.agents.email_agent import email_agent
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

        # Classify the intent
        intent = await classify_intent(memory, request.message)
        print(f"Classified intent: {intent}")

        # Handle support query and dev team requests
        if intent == 'agent':
            # Determine if this is a dev team request or a support query
            # Check if this is a dev request (feature request, technical issue, etc.)
            is_dev_request = "feature" in request.message.lower() or "improvement" in request.message.lower() or "bug" in request.message.lower()

            # Use the appropriate email agent based on request type
            request_type = "support"
            agent_response = await email_agent(
                user_id=request.user_id,
                user_input=request.message,
                request_type=request_type
            )

            if isinstance(agent_response, dict) and "output" in agent_response:
                return ChatResponse(response=agent_response["output"], actions_taken=[], user_id=request.user_id)
            else:
                return ChatResponse(response=str(agent_response), actions_taken=[], user_id=request.user_id)

        # Use standard chat engine if no agent or agent didn't handle
        response = await chat_engine.process_message(
            message=request.message,
            user_id=request.user_id
        )
        print(response)

        return ChatResponse(response=response, actions_taken=[], user_id=request.user_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# run_server.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.api.server:app", host="127.0.0.1", port=8888, reload=True)
