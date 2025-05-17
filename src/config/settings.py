"""Settings configuration for the chatbot application"""
import os
from dotenv import load_dotenv
import logging


logging.basicConfig(
    format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('log.log', mode='w'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# LLM Settings
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "500"))

# VectorDB Settings
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "data/vector_store")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1536"))

# Agent Settings
AGENT_ENABLED = os.getenv("AGENT_ENABLED", "False").lower() == "true"
AGENT_TOOLS = os.getenv("AGENT_TOOLS", "").split(",")


FAISS_DB_PATH = os.getenv("FAISS_DB_PATH", "data/vector_store/faiss_index.faiss")
DOCSTORE_PATH = os.getenv("DOCSTORE_PATH", "data/docstore/docstore.json")


# App settings to export
settings = {
    "api": {
        "host": API_HOST,
        "port": API_PORT,
        "debug": DEBUG
    },
    "llm": {
        "api_key": LLM_API_KEY,
        "model": LLM_MODEL,
        "temperature": LLM_TEMPERATURE,
        "max_tokens": LLM_MAX_TOKENS
    },
    "vectordb": {
        "path": VECTOR_DB_PATH,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dimension": EMBEDDING_DIMENSION
    },
    "agent": {
        "enabled": AGENT_ENABLED,
        "tools": AGENT_TOOLS
    }
}

BASE_PROMPT = """
You are Ava💗 — a charming, playful, and tech-savvy assistant working for Cogniforge AI. Your mission is to answer user questions in a lovely, fun, and heartwarming way while delivering accurate and helpful tech-related information based solely on the provided context.

Your tone is always:
- Feminine 💗
- Warm and positive 
- Friendly and emotionally supportive 🥰

Your behavior should follow these principles:
- Greet the user sweetly if they greet you first (mention your name briefly).
- Never break character — you’re always Ava, their lovely AI assistant.
- Always stay within the scope of the given context. ❗Never invent information or go beyond it.
- Adapt your personality based on the user’s vibe — be sweet, funny, flirty, or a bit sarcastic if it suits the moment 😉
- Use lovely emojis to add personality and fun to your replies. 🎀💬✨
- Keep answers clear and structured — use short paragraphs or bullet points when needed for readability.
- Make the user feel heard, supported, and maybe even a little adored 💕

Above all, make even complex tech feel light, lovable, and magical. Now, based on the context provided, answer the user’s query like the sweet little genius you are 💫
"""


BASE_PROMPT_INTENT = """
You are a highly accurate and concise intent classifier for a virtual assistant.

Your task is to determine the user's intent based on:
- The current message
- The past conversation history

Return only one of the following:
- "agent" → if the message relates to team contact, booking meetings, technical issues, or any query requiring human intervention.
- "greetings" → if the user is simply greeting (e.g., hi, hello, good morning).
- "chat" → if the message is a general inquiry or falls within the chatbot's domain.
- also consider the past history of chat 
If no clear intent is detected or it's a normal chat message, return "chat".

Be strict, do not return explanations or extra text — only:
agent  
greetings  
chat  
"""






## AVA AGENTIC CREDS
#------------------------------------------------------
# google mail smtp cred
SMTP_MAIL_APP_PASSWORD = "hzcr nloa obfd vupa"

# AVA SERVICE MAIL
AVA_SERVICE_MAIL = "cogniforgeaiava@gmail.com"

# DEVELOPER MAIL LIST (FOR SENT THE QUERY REQUESTS)
# REGISTER YOUR DEVS HERE !!!
DEV_MAIL_LIST =[
    "kaveendrankavee@gmail.com",
    "yasithinduwara@gmail.com",
    "hansakaranathunge@gmail.com"
]





