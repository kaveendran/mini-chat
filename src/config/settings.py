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

BASE_PROMPT =""" HELLO """