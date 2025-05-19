from src.vectordb.faiss_db import load_docstore,load_vector_store,query_vector_store
from src.config.settings import DOCSTORE_PATH,VECTOR_DB_PATH
from src.core.chat import ChatEngine
# try:
#     vec_store = load_vector_store(VECTOR_DB_PATH, docstore_path=DOCSTORE_PATH)
#     data = query_vector_store(vec_store,"who is the ceo of cogniforgeai")
#     print(data)
# except ValueError as e:
#     print(f"Error querying vector store: {e}")
#     data = None

import uvicorn
from src.agents.chat_agent import chat_agent
import asyncio
if __name__ == "__main__":

    while True:
        id = "hello"
        inpu =  input("QUERY :")
        out = chat_agent(id,inpu)
        print(out)
    # from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
    # Create a LANGSMITH_API_KEY in Settings > API Keys
    # from langsmith import Client
    #
    # client = Client(api_key='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')
    # prompt = client.pull_prompt("hwchase17/structured-chat-agent", include_model=False)

    print(len(prompt.to_dict()))