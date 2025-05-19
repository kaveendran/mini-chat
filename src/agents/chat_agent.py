
from langchain_core.messages import messages_to_dict, BaseMessage, HumanMessage, AIMessage
from langchain.tools import Tool,StructuredTool
from langchain.agents import AgentExecutor, create_react_agent,create_structured_chat_agent
from src.core.chat import ChatEngine
from src.googleapis.gmail_service import smtp_gmail
from src.core.base import ChatEngine
from pydantic import BaseModel, Field
from src.llm.model import UserMemory
from src.config.settings import BASE_PROMPT
## RAG TOOL DEFINITION
# basic convo chain with retrieval
from langchain.memory import ConversationBufferMemory

chat = ChatEngine('qwen-qwq-32b')



from langchain.agents import Tool
from pydantic import BaseModel, Field
from src.core.chat import ChatEngine

# Assuming you have initialized your ChatEngine instance elsewhere, e.g.,
# chat = ChatEngine()

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
    user_name: str = Field(..., description="User's full name")
    user_email: str = Field(..., description="User's email address")
    user_message: str = Field(..., description="Message to be sent")

# Tool for sending support queries to dev team
support_query_tool = StructuredTool.from_function(
    name="ContactQueryMailer",
    func=smtp_gmail,
    args_schema = EmailInput,
    description="""
Use this tool to send a support query to the dev team and optionally send a confirmation to the user.

**Before using this tool, you MUST ensure you have the following information. If any of it is missing, ask the user for it:**
- user_name: The name of the user.
- user_email: The email address of the user (validate the format!).
- user_message: The user's support query.

Validate the email format and be casual, friendly, and warm ❤️.
You are Ava, a chatbot working for Cogniforge AI.

if not relevent information found ask from user dont try to execute the tool

"""
)

tools = [
support_query_tool,rag_retrieval_tool
]
# Global Memory Pool Access
memory = UserMemory()



# settings.py
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# Create a LANGSMITH_API_KEY in Settings > API Keys
from langsmith import Client
client = Client(api_key='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')
prompt = client.pull_prompt("hwchase17/structured-chat-agent", include_model=True)

context_message = SystemMessagePromptTemplate.from_template(
    BASE_PROMPT
)

prompt.messages.insert(0,context_message)
def chat_agent(user_id: str, user_input: str):

    chat_history = memory.get_user_memory(user_id=user_id)
    mem = ConversationBufferMemory(chat_memory=chat_history, memory_key="chat_history", return_messages=True)

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

    result = executor.invoke({'input':user_input})
    return result





