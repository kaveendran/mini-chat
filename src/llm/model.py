"""Language model integration for generating responses."""




from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.language_models import chat_models

class UserMemory:
    """Handles interactions with language models."""
    
    def __init__(self):
        """Initialize the LLM handler with settings from config."""
        # global memory for store the customers
        self.global_memory = {}

    # get user specific memory object
    def get_user_memory(self,user_id):
        if user_id not in self.global_memory:
            self.global_memory[user_id] = InMemoryChatMessageHistory()
        return self.global_memory[user_id]





