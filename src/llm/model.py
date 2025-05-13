"""Language model integration for generating responses."""
import os
from typing import Dict, List, Optional
from openai import OpenAI
from config import settings

class LLMHandler:
    """Handles interactions with language models."""
    
    def __init__(self):
        """Initialize the LLM handler with settings from config."""
        # Access settings from config module
        self.settings = settings.settings
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.settings["llm"]["api_key"])
        self.model = self.settings["llm"]["model"]
        self.temperature = self.settings["llm"]["temperature"]
        self.max_tokens = self.settings["llm"]["max_tokens"]
        
    def generate_response(self, message: str, context: str = "", user_id: str = "default_user") -> str:
        """Generate a response using the LLM.
        
        Args:
            message: The user's message
            context: Optional context information
            user_id: The user identifier for conversation tracking
            
        Returns:
            The LLM's response
        """
        # Construct the prompt with context if available
        prompt = self._construct_prompt(message, context)
        
        try:
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                user=user_id
            )
            
            # Extract and return the response text
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Handle errors gracefully
            print(f"Error generating LLM response: {e}")
            return "I'm sorry, I encountered an error processing your request."
    
    def _construct_prompt(self, message: str, context: str = "") -> str:
        """Construct the prompt for the LLM.
        
        Args:
            message: The user's message
            context: Optional context information
            
        Returns:
            The constructed prompt
        """
        if context:
            return f"{context}\n\nUser question: {message}\n\nResponse:"
        else:
            return f"User question: {message}\n\nResponse:" 