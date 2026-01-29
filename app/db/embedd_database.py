import json
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.db.config import CONFIG
from app.db.chroma import initialize_vector_store, index_documents


def load_attack_patterns(file_path: str) -> List[Document]:
    """Load JSON data and convert to LangChain Document objects."""
    with open(file_path, "r") as f:
        data = json.load(f)

    return [
        Document(
            page_content=entry["description"],
            metadata={
                "id": entry["id"],
                "name": entry["name"],
                "platforms": ", ".join(entry.get("platforms", [])),
            },
        )
        for entry in data
    ]


def get_text_chunks(documents: List[Document]) -> List[Document]:
    """Split documents into smaller, manageable chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CONFIG["chunk_size"],
        chunk_overlap=CONFIG["chunk_overlap"],
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documents)


def get_embedding_model(task_type: str = "retrieval_document"):
    """Initialize the Google Generative AI embedding model."""
    return GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=CONFIG["google_api_key"],
        task_type=task_type,
    )


def run_indexing_pipeline(file_path: str):
    """The main orchestration function."""
    # Prepare Data
    raw_docs = load_attack_patterns(file_path)
    chunks = get_text_chunks(raw_docs)

    # Setup Tools
    embeddings = get_embedding_model()
    vector_store = initialize_vector_store(embeddings)

    # Execute
    index_documents(vector_store, chunks)
    print("Done!")


if __name__ == "__main__":
    run_indexing_pipeline("./attack-patterns.json")
