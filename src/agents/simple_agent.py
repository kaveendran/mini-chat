from langchain.agents import initialize_agent, AgentType, Tool
from src.core.chat import ChatEngine
from src.googleapis.gmail_service import smtp_gmail
from src.config.settings import BASE_PROMPT
from src.googleapis.gmail_service import smtp_gmail
from langchain.agents import Tool
from langchain_core.messages import messages_to_dict
import json
from langchain.tools import Tool

smtp_mail_tool = [
    Tool(
        name="EmailSender",
        func=smtp_gmail,
        description="""
        Use this tool ONLY after you've collected all of the following:
        - user_name
        - user_email
        - user_message

        You must collect this details from the user query other wise ask it from the user
        Validate the email and be casual, friendly, and warm ❤️.
        And remember you are the chat bot called ava working for tech company called cogniforge ai
        if there is no relevent details found ask it from user
        Input must be a dictionary like:
        {
            "user_name": "...",
            "user_email": "...",
            "user_message": "...",
            "send_user_confirmation": true (optional)
        }
        """
    )
]

chat = ChatEngine('qwen-qwq-32b')


async def mail_agent(user_id: str,user_input: str) -> dict:
    """
    Run the mail agent with the given user input message.
    Returns the agent's response string (chatbot output).
    """
    # Initialize the agent once
    agent = initialize_agent(
        tools=smtp_mail_tool,
        llm=chat.llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )
    memory = chat.memory.get_user_memory(user_id=user_id)
    chat_history = json.dumps(
        messages_to_dict(
            await memory.aget_messages()
        )
    )

    if len(chat_history) > 3:
        chat_history = chat_history[len(chat_history)-3:]

    try:
        print(chat_history)
        response = await agent.ainvoke({"input": user_input})
        print(response)
        return response
    except Exception as e:
        print(e)
        return f"Oops, something went wrong while processing your request: {e}"
