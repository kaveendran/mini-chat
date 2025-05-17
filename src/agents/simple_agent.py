from langchain.agents import initialize_agent, AgentType, Tool
from src.core.chat import ChatEngine
from src.googleapis.gmail_service import smtp_gmail
from src.config.settings import BASE_PROMPT
from src.googleapis.gmail_service import smtp_gmail
from langchain.agents import Tool

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

chat = ChatEngine()


def mail_agent(user_id: str,user_input: str) -> str:
    """
    Run the mail agent with the given user input message.
    Returns the agent's response string (chatbot output).
    """
    # Initialize the agent once
    agent = initialize_agent(
        tools=smtp_mail_tool,
        llm=chat.llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True,
    )
    agent.memory = chat.memory.get_user_memory(user_id=user_id)

    try:
        response = agent.run(user_input)
        return response
    except Exception as e:
        return f"Oops, something went wrong while processing your request: {e}"
