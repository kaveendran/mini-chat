from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from pyexpat.errors import messages

from src.config.settings import BASE_PROMPT, VECTOR_DB_PATH, DOCSTORE_PATH
from src.llm.model import UserMemory
from src.vectordb.faiss_db import load_vector_store
from langchain_groq import ChatGroq
import dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()

class ChatEngine:
    """
    Chat Engine using conversational chain,
    user-specific memory store, and Groq Chat as the LLM.
    """

    def __init__(self,model_name='llama-3.1-8b-instant'):
        self.llm = ChatGroq(
            temperature=0.4,
            model_name= model_name,
            verbose=True,
            max_tokens=1000,

        )
        self.vector_store = load_vector_store(VECTOR_DB_PATH, DOCSTORE_PATH)


        # Prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", BASE_PROMPT),
            ("human", "Context:\n{context}\n\nUser: {input}")
        ])

        # Build core chain
        self.chain = self.prompt | self.llm | StrOutputParser()


    def process_message(self, message: str):
        # Async document retrieval
        retriever = self.vector_store.as_retriever(k=3)
        rel_docs = retriever.invoke(message)
        print(len(rel_docs))
        context = self._format_context(rel_docs)

        # Run chain with memory
        return  self.chain.invoke(
            {"input": message, "context": context}
        )

    def _format_context(self, documents: list) -> str:
        if not documents:
            return "No relevant context found."
        return "\n".join([f"{i+1}. {doc.page_content}" for i, doc in enumerate(documents)])


    async def basic_completion(self,text_input:str):
        response = await self.llm.ainvoke(text_input)
        return response.content


# Optional: test the LLM directly
if __name__ == "__main__":
    ce = ChatEngine()
    op = ce.process_message()

    print(op)