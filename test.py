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
