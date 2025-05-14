from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain
from src.config.settings import BASE_PROMPT,VECTOR_DB_PATH,DOCSTORE_PATH
from src.llm.model import UserMemory
from src.vectordb.faiss_db import load_vector_store
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv()


class ChatEngine:
    """"
    Chat Engine using conversational chain
    and user specific memory object store and the  groq chat as a llm
    """
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.4,
            model_name='lama-3.1-8b-instant',
            verbose= True
        )
        self.vector_store = load_vector_store(VECTOR_DB_PATH, DOCSTORE_PATH)
        self.memory = UserMemory()

        # Wrap BASE_PROMPT if it's a string into a valid chat prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(BASE_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("Context:\n{context}\n\nUser: {input}")
        ])

    async def process_message(self, message: str, user_id: str):
        user_specific_memory = self.memory.get_user_memory(user_id)

        # Async document retrieval
        retriever = self.vector_store.as_retriever()
        rel_docs = await retriever.ainvoke(message)
        context = self._format_context(rel_docs)

        # conversational chain
        chain = ConversationChain(
            prompt=self.prompt_template,
            llm=self.llm,
            memory=user_specific_memory,
            verbose=True
        )

        return await chain.ainvoke({"input": message, "context": context})

    def _format_context(self, documents: list) -> str:
        if not documents:
            return "No relevant context found."
        return "\n".join([f"{i+1}. {doc.page_content}" for i, doc in enumerate(documents)])


if __name__ == "__main__":
    chat = ChatEngine()
    chat.process_message("hello","123243")