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



