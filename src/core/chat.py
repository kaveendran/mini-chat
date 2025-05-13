"""Core chat engine functionality"""
from app.llm.model import LLMHandler
from app.vectordb.faiss_db import VectorStore
from config import settings

class ChatEngine:
    """Chat engine that processes messages and generates responses."""
    
    def __init__(self, llm_handler: LLMHandler, vector_store: VectorStore):
        """Initialize the chat engine with LLM and vector store components.
        
        Args:
            llm_handler: The language model handler
            vector_store: The vector database for context retrieval
        """
        self.llm_handler = llm_handler
        self.vector_store = vector_store
        # Access settings from config module
        self.settings = settings.settings
        
    def process_message(self, message: str, user_id: str) -> str:
        """Process an incoming message and generate a response.
        
        Args:
            message: The user's message
            user_id: The user's identifier
            
        Returns:
            A response from the language model
        """
        # Retrieve relevant context from vector store
        relevant_docs = self.vector_store.search(message)
        
        # Combine message with context for LLM processing
        context = self._format_context(relevant_docs)
        
        # Generate response using LLM
        response = self.llm_handler.generate_response(message, context, user_id)
        
        return response
    
    def _format_context(self, documents: list) -> str:
        """Format documents into context string for the LLM.
        
        Args:
            documents: List of document objects from vector store
            
        Returns:
            Formatted context string
        """
        if not documents:
            return ""
        
        context = "Context information:\n"
        for i, doc in enumerate(documents):
            context += f"{i+1}. {doc.content}\n"
        
        return context 