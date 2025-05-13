"""FAISS vector database integration for document storage and retrieval."""
import os
from typing import Dict, List, Optional, Any
import faiss
from langchain.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain.embeddings import HuggingFaceEmbeddings
from src.config.settings import EMBEDDING_MODEL,EMBEDDING_DIMENSION
import logging
from langchain.docstore import InMemoryDocstore
import json
logger = logging.getLogger('vector_db')


def create_vector_store(docstore: InMemoryDocstore):
    """
    Create a vector store.
    """
    try:
        # Get the actual embedding dimension from the model
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}
        )
        # Create a test embedding to get actual dimension
        test_embedding = embeddings.embed_query("test")
        actual_dimension = len(test_embedding)
        
        index = faiss.IndexFlatL2(actual_dimension)
        logger.info(f"Vector store created with index: {index}")
        return FAISS(
            embedding_function=embeddings,
            index=index,
            index_to_docstore_id={},
            docstore=docstore
        )
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        raise e


def add_documents(vector_store: FAISS, documents: List[Document]):
    """
    Add documents to the vector store.
    """
    try:
        vector_store.add_documents(documents)
        logger.info(f"Documents added to vector store: {len(documents)}")
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise e

def query_vector_store(vector_store: FAISS, query: str, k: int = 5):
    """
    Query the vector store for the most relevant documents.
    """
    try:
        # Use a larger fetch_k to ensure we retrieve enough candidates
        # This helps avoid "document not found" errors by casting a wider net
        fetch_k = max(k * 2, 20)  # At least 2x the requested k, minimum 20
        results = vector_store.similarity_search_with_score(query, k=k, fetch_k=fetch_k)
        logger.info(f"Documents retrieved from vector store: {len(results)}")
        return results
    except Exception as e:
        # Log the full error details to help debug document not found issues
        logger.error(f"Error querying vector store: {str(e)}")
        # Re-raise the exception to handle it at a higher level
        raise e


def save_vector_store(vector_store: FAISS, path: str):
    """
    Save the vector store to a file.
    """
    try:
        vector_store.save_local(path)
        logger.info(f"Vector store saved to {path}")
    except Exception as e:
        logger.error(f"Error saving vector store: {e}")
        raise e


def load_vector_store(path: str, docstore_path: str = None):
    """
    Load the FAISS vector store from disk.

    This loads both the FAISS index and the associated docstore, allowing document retrieval
    after similarity search. If a docstore_path is provided, it will load the docstore from that path
    and explicitly set it in the vector store.
    """
    try:
        logger.info(f"Loading vector store from {path}")

        # Check if path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Vector store path {path} does not exist")

        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}
        )

        # Load vector store with error handling
        try:
            vector_store = FAISS.load_local(
                folder_path=path,
                embeddings=embeddings
            )
        except Exception as load_error:
            logger.error(f"Failed to load vector store: {load_error}")
            raise load_error

        # Validate vector store components
        if not vector_store.index:
            raise ValueError("FAISS index is missing from loaded vector store")
        
        if not hasattr(vector_store, 'docstore') or not vector_store.docstore:
            raise ValueError("Doc store is missing from loaded vector store")

        if not hasattr(vector_store, 'index_to_docstore_id'):
            raise ValueError("index_to_docstore_id mapping is missing from vector store")

        # If docstore path is provided, reload the docstore and set it explicitly
        if docstore_path and os.path.exists(docstore_path):
            logger.info(f"Loading docstore from {docstore_path} and connecting it to vector store")
            vector_store.docstore = load_docstore(docstore_path)

        logger.info("Successfully loaded and validated vector store")
        return vector_store

    except Exception as e:
        logger.error(f"Error loading vector store: {e}")
        raise e



def persist_docstore(docstore: InMemoryDocstore, path: str):
    """
    Persist the docstore to a file.
    """
    try:
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(docstore.docstore, f,indent=4)
        logger.info(f"Docstore saved to {path}")
    except Exception as e:
        logger.error(f"Error persisting docstore: {e}")
        raise e


def load_docstore(path: str):
    """
    Load the docstore from a file.
    
    Properly converts strings to Document objects for compatibility with vector store.
    """
    try:
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            return InMemoryDocstore({})
            
        with open(path, "r") as f:
            docstore_dict = json.load(f)
            
        # Convert string values to Document objects
        document_dict = {}
        for doc_id, content in docstore_dict.items():
            if isinstance(content, str):
                document_dict[doc_id] = Document(page_content=content, metadata={"id": doc_id})
            else:
                document_dict[doc_id] = content
                
        logger.info(f"Loaded docstore from {path} with {len(document_dict)} documents")
        return InMemoryDocstore(document_dict)
    except Exception as e:
        logger.error(f"Error loading docstore: {e}")
        raise e
