# from langchain.agents import initialize_agent, AgentType, Tool
# from langchain_core.messages import messages_to_dict, BaseMessage, HumanMessage, AIMessage
# from langchain.tools import Tool
# import json
# from langchain.agents import AgentExecutor, create_react_agent,create_vectorstore_router_agent,create_structured_chat_agent
#
# from src.core.chat import ChatEngine
# from src.googleapis.gmail_service import smtp_gmail
#
#
# from pydantic import BaseModel, Field
#
# class EmailInput(BaseModel):
#     user_name: str = Field(..., description="User's full name")
#     user_email: str = Field(..., description="User's email address")
#     user_message: str = Field(..., description="Message to be sent")
# # chain tool
#
# qa_chain_tool = Tool(
#
# )
#
# # Tool for sending support queries to dev team
# support_query_tool = Tool(
#     name="SupportQueryEmailer",
#     func=smtp_gmail,
#     args_schema = EmailInput,
#     description="""
# Use this tool to send a support query to the dev team and optionally send a confirmation to the user.
#
# **Before using this tool, you MUST ensure you have the following information. If any of it is missing, ask the user for it:**
# - user_name: The name of the user.
# - user_email: The email address of the user (validate the format!).
# - user_message: The user's support query.
#
# Validate the email format and be casual, friendly, and warm ❤️.
# You are Ava, a chatbot working for Cogniforge AI.
#
# if not relevent information found ask from user dont try to execute the tool
#
# """
# )
#
#
#
# # Initialize ChatEngine
# chat = ChatEngine('qwen-qwq-32b')
#
# async def email_agent(user_id: str, user_input: str, request_type: str = "support") -> dict:
#     """
#     Run the email agent with the given user input message.
#
#     Args:
#         user_id: The unique identifier for the user
#         user_input: The user's message
#         request_type: Either "support" (for user support queries) or "dev" (for dev team requests)
#
#     Returns:
#         The agent's response dictionary
#     """
#     # Choose the appropriate tool based on request type
#     if request_type.lower() == "dev":
#         tools = [support_query_tool]
#     else:  # default to support
#         tools = [support_query_tool]
#
#     # Initialize the agent
#     agent = (
#         tools=tools,
#         llm=chat.llm,
#         prompt='based on the query execute tool else prompt the user'
#     )
#
#     react_agent_executor = AgentExecutor.from_agent_and_tools(
#         agent=agent, tools=tools, verbose=True, handle_parsing_errors=True,memory =
#     )
#
#     # Get user chat history
#     memory = chat.memory.get_user_memory(user_id=user_id)
#     chat_history_objects = await memory.aget_messages()
#
#     # Limit chat history to recent messages
#     chat_history = chat_history_objects[-3:] if len(chat_history_objects) > 3 else chat_history_objects
#
#     try:
#         print(f"Processing {request_type} email request from user {user_id}")
#         response = await react_agent_executor.ainvoke({
#             "input": user_input,
#             "chat_history": chat_history
#         })
#         print(f"Email agent response: {response}")
#         return response
#     except Exception as e:
#         error_msg = f"Error processing email request: {str(e)}"
#         print(error_msg)
#         return {"output": error_msg}