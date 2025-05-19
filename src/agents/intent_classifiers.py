"""
This module provides basic intent classification tasks
"""
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import messages_to_dict
from src.core.chat import ChatEngine
from src.config.settings import BASE_PROMPT_INTENT
import json
from dataclasses import asdict

chat = ChatEngine()

async def classify_intent(history: InMemoryChatMessageHistory, text: str):
    """
    Method that classifies the intent of the text based on the query
    Args:
        history: InMemoryChatMessageHistory (memory object)
        text: str (text to classify the indent)
    Returns:
        str: The classified intent (agent, greetings, or chat)
    """
    chat_history = json.dumps(
        messages_to_dict(
            await history.aget_messages()
        )
    )
    
    # Make the classification prompt
    prompt = PromptTemplate.from_template(
        """system: {system_prompt}
            past_history: {past_history}
            query: {user_query}
        """
    )

    # Limit chat history to recent messages
    if len(chat_history) > 3:
        chat_history = chat_history[len(chat_history)-3:]
    
    # Check for email-related keywords to help with classification
    email_keywords = ["contact", "support", "email", "query", "team", "request", 
                     "feature", "bug", "issue", "problem", "help me with", 
                     "report", "feedback", "contact", "message", "send"]
    
    has_email_keywords = any(keyword in text.lower() for keyword in email_keywords)
    
    # Add additional context for the intent classifier if email keywords are detected
    if has_email_keywords:
        user_query = f"{text} [Contains email-related keywords, consider 'agent' intent]"
    else:
        user_query = text
    
    # Get intent classification from LLM
    intent = await chat.basic_completion(
        prompt.format(
            system_prompt=BASE_PROMPT_INTENT,
            user_query=user_query,
            past_history=chat_history
        )
    )
    
    return intent.strip()




