"""Module for create the text embeddings"""
import sys
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config.settings import EMBEDDING_MODEL
from typing import List
import logging
logger = logging.getLogger('embeddings')

# Load the HuggingFaceEmbeddings model
hf = HuggingFaceEmbeddings(
        model_name = EMBEDDING_MODEL,
        model_kwargs = {"device": "cpu"}
    )


def create_embeddings(texts: List[str]):
    """
    Create embeddings for a list of texts or text using the 
    HuggingFaceEmbeddings model.
    Args:
        texts: List[str] or str
    Returns:
        embeddings: List[float]
    Raises:
        Exception: If an error occurs during embedding creation.
    """
    try:
        if isinstance(texts, list):
            embeddings = hf.embed_documents(texts)
        else:
            embeddings = hf.embed_query(texts)
        return embeddings
    except Exception as e:
        logger.error(f"Error creating embeddings: {e}")
        raise e



if __name__ == "__main__":
    texts = ["Hello, world!", "This is a test."]
    embeddings = create_embeddings(texts)
    print(embeddings)

