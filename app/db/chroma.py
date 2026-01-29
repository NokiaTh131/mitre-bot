from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.db.config import CONFIG
import time

from typing import List


def initialize_vector_store(embeddings):
    """Create or load a ChromaDB instance."""
    return Chroma(
        collection_name=CONFIG["collection_name"],
        embedding_function=embeddings,
        persist_directory=CONFIG["chroma_path"],
    )


def index_documents(vector_store, chunks: List[Document]):
    """Add documents to vector store in batches to respect API limits."""
    batch_size = CONFIG["batch_size"]
    total_batches = (len(chunks) + batch_size - 1) // batch_size

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        try:
            vector_store.add_documents(documents=batch)
            print(f"Successfully indexed batch {i // batch_size + 1}/{total_batches}")
        except Exception as e:
            print(
                f"Rate limit hit or error at batch {i}. Sleeping for 30s... (Error: {e})"
            )
            time.sleep(60)
            vector_store.add_documents(documents=batch)  # Retry
