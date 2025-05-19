
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor,create_structured_chat_agent
from src.googleapis.gmail_service import smtp_gmail
from src.core.base import ChatEngine
from src.llm.model import UserMemory
from src.config.settings import BASE_PROMPT
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool
from pydantic import BaseModel, Field


chat = ChatEngine('qwen-qwq-32b')


class RagSchema(BaseModel):
    message: str = Field(..., description="Users message")

rag_retrieval_tool = Tool(
    name = "RAGtool",
    func=chat.process_message,
    args_schema=RagSchema,
    description="""
    Tool that can be used for retrieve the relevent docs
    for the context and answer the user queries
    """
)

## MAIL TOOL DEFINITION
class EmailInput(BaseModel):
    user_message: str = Field(..., description="Message to be sent including email and the username and query")

# Tool for sending support queries to dev team
support_query_tool = StructuredTool.from_function(
    name="ContactQueryMailer",
    func=smtp_gmail,
    args_schema = EmailInput,
    description="""
Use this tool to send a support query to the dev team 
Before use this tool ensure there is 
username
phone number
email
message 
presented 
else ask from user dont ! execute the tool
"""
)


# Register the tools
tools = [
support_query_tool,rag_retrieval_tool
]


# Global Memory Pool Access
memory = UserMemory()

from langchain_core.prompts import SystemMessagePromptTemplate

from langsmith import Client
client = Client(api_key='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')
prompt = client.pull_prompt("hwchase17/structured-chat-agent", include_model=True)
# Inject custom base prompt
context_message = SystemMessagePromptTemplate.from_template(
    BASE_PROMPT
)
prompt.messages.insert(0,context_message)



## CHAT AGENT IMPLEMENTATION
def chat_agent(user_id: str, user_input: str):

    chat_history = memory.get_user_memory(user_id=user_id)

    mem = ConversationBufferMemory(
        chat_memory=chat_history,
        memory_key="chat_history",
        return_messages=True
    )

    # define agent
    agent = create_structured_chat_agent(
        llm= chat.llm,
        prompt=prompt,
        tools= tools,
        stop_sequence= True
    )

    # define agent executor
    executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        memory = mem,
        verbose = True,
        tools=tools,
        handle_parsing_errors=True
    )

    result = executor.invoke({
        'input':user_input
    })

    return result





