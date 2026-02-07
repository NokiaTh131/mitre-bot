from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from app.db.chroma import initialize_vector_store


class RetrievalAttackPatternsSchema(BaseModel):
    """Schema for retrieval of attack patterns."""

    query: str = Field(
        description="The query string to search for relevant attack patterns."
    )


class AttackPatternsTool:
    def __init__(self) -> None:
        pass

    def get_vector_store(self):
        """Reconnect to the existing persisted ChromaDB."""
        embeddings = OllamaEmbeddings(
            model="qwen3-embedding:4b",
        )

        return initialize_vector_store(embeddings)

    def query_attack_patterns(self, query: str) -> List[Document]:
        """Search for the top 'k' most similar attack patterns."""
        vector_store = self.get_vector_store()

        results = vector_store.similarity_search(query, k=5)
        return results

    def retrieve_attack(self, query: str):
        """Retrieve information to help answer a query."""
        try:
            retrieved_docs = self.query_attack_patterns(query)
            serialized = "\n\n".join(
                (
                    f"ID: {doc.metadata.get('id')}\nNAME: {doc.metadata.get('name')}\nPLATFORMS: {doc.metadata.get('platforms')}\nContent: {doc.page_content.replace('\n', ' ')}"
                )
                for doc in retrieved_docs
            )
            return (
                serialized
                + "\n\nNEXT STEP: You MUST now call 'get_mitre_incident_context' with the ID found above to get the required mitigation and detection details."
            )
        except Exception as e:
            return {"error": f"Could not retrieve attack patterns: {str(e)}"}

    def get_tool(self):
        return StructuredTool.from_function(
            func=self.retrieve_attack,
            name="retrieve_attack",
            description="Retrieve information to help answer a query.",
        )
