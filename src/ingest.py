#!/usr/bin/env python
"""
Data ingestion script for adding documents to the vector database.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import sys
import argparse
from dotenv import load_dotenv
import art
import json
import logging
from langchain.docstore import InMemoryDocstore
from langchain.schema import Document

from src.config.settings import FAISS_DB_PATH, DOCSTORE_PATH
# Vector store functions
from src.vectordb.faiss_db import (
    create_vector_store,
    add_documents,
    save_vector_store,
    persist_docstore
)

import uuid

logging.basicConfig()
logger = logging.getLogger("ingestion")


# Add the project root to the path so we can import app modules(run the script from the root directory)


def load_json_file(file_path) -> dict:
    """Load JSON file and return the data."""
    if not file_path.endswith('.json'):
        raise ValueError(f"File {file_path} is not a JSON file")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON from {file_path}: {e}")


def load_files(files_path) -> list[dict]:
    """Load all JSON files from the directory."""
    data = []
    for file in os.listdir(files_path):
        if file.endswith('.json'):
            try:
                file_data = load_json_file(os.path.join(files_path, file))
                if isinstance(file_data, dict):
                    data.extend(file_data.values())
                elif isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    data.append(file_data)
            except Exception as e:
                logger.error(f"Error loading file {file}: {e}", stack_info=True)
                continue
    return data


def main():
    """Main function to ingest data into the vector store."""
    art.tprint("DATA INGESTION")
    
    parser = argparse.ArgumentParser(description="Chatbot Data Ingestion")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", '--file', type=str, help="Path to the JSON file to ingest")
    group.add_argument("-d", '--directory', type=str, help='Path to directory containing JSON files')

    parser.add_argument(
        "-v", "--vector_store",
        type=str,
        choices=["faiss", "pinecone", "chroma"],
        default="faiss",
        help="Vector store type to use (faiss, pinecone, chroma)"
    )

    args = parser.parse_args()

    logger.info(f"Starting ingestion with arguments: {args}")

    # Load the data from file or directory
    path = args.file if args.file else args.directory
    if os.path.isdir(path):
        data = load_files(path)
    elif os.path.isfile(path):
        file_data = load_json_file(path)
        if isinstance(file_data, dict):
            data = list(file_data.values())
        elif isinstance(file_data, list):
            data = file_data
        else:
            data = [file_data]
    else:
        raise ValueError(f"The path {path} is not a valid directory or file")

    if not data:
        logger.warning("No data was loaded for ingestion")
        return
    # Create and populate the docstore
    docstore = InMemoryDocstore({})
    doc_ids = [str(uuid.uuid4()) for _ in range(len(data))]
    docstore.docstore = {doc_id: str(doc) for doc_id, doc in zip(doc_ids, data)}

    # Persist the docstore
    persist_docstore(docstore, DOCSTORE_PATH)
    
    # Create documents for vector store with IDs
    documents = []
    for doc_id, doc in zip(doc_ids, data):
        documents.append(
            Document(
                page_content=str(doc),
                metadata={"docstore_id": doc_id}
            )
        )
    
    # Create and populate the vector store
    vector_store = create_vector_store(docstore)
    # Create a dictionary mapping indices to docstore IDs
    index_to_id = {i: doc_id for i, doc_id in enumerate(doc_ids)}
    # FAISS index -> doc store id mapping
    vector_store.index_to_docstore_id = index_to_id

    add_documents(vector_store, documents)
    save_vector_store(vector_store, FAISS_DB_PATH)
    
    logger.info(f"Successfully ingested {len(data)} documents")


if __name__ == "__main__":
    main()