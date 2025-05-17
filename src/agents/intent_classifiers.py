"""
This module provides basic intent  classification tasks
"""
from langchain.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import messages_to_dict
from src.core.chat import ChatEngine
from src.config.settings import BASE_PROMPT_INTENT
import json
from dataclasses import asdict

chat = ChatEngine()

async def classify_intent(history:InMemoryChatMessageHistory,text:str):
    """
    Method that classify the intent of the text based on the query
    Args:
        history :InMemoryChatMessageHistory (memory Object)
        text:str (text to classify the indent)
    """
    chat_history = json.dumps(
        messages_to_dict(
            await history.aget_messages()
        )
    )
    # Make the classification prompt
    prompt = PromptTemplate.from_template(
        """system: {system_prompt}
            past_history : {past_history}
            query :{user_query}
        """
    )

    if len(chat_history) > 3:
        chat_history = chat_history[len(chat_history)-3:]


    return await chat.basic_completion(
        prompt.format(
            system_prompt = BASE_PROMPT_INTENT,
            user_query = text,
            past_history = chat_history
        )
    )




