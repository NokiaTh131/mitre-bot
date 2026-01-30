from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain.tools import tool
from pydantic import BaseModel, Field
from app.db.config import CONFIG
from app.db.chroma import initialize_vector_store

class RetrievalAttackPatternsSchema(BaseModel):
    """Schema for retrieval of attack patterns."""
    query: str = Field(description="The query string to search for relevant attack patterns.")
    
class AttackPatternsTool:
    def __init__(self) -> None:
        pass
    def get_vector_store(self):
        """Reconnect to the existing persisted ChromaDB."""
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=CONFIG["google_api_key"],
            task_type="retrieval_query",
        )

        return initialize_vector_store(embeddings)


    def query_attack_patterns(self,query: str) -> List[Document]:
        """Search for the top 'k' most similar attack patterns."""
        vector_store = self.get_vector_store()

        results = vector_store.similarity_search(query, k=5)
        return results


    @tool(response_format="content_and_artifact")
    def retrieve_context(self, query: str):
        """Retrieve information to help answer a query."""
        try:
            retrieved_docs = self.query_attack_patterns(query)
            serialized = "\n\n".join(
                (
                    f"ID: {doc.metadata.get('id')}\nNAME: {doc.metadata.get('name')}\nPLATFORMS: {doc.metadata.get('platforms')}\nContent: {doc.page_content.replace('\n', ' ')}"
                )
                for doc in retrieved_docs
            )
            return serialized, retrieved_docs
        except Exception as e:
            return {"error": f"Could not retrieve attack patterns: {str(e)}"}
