import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from app.core.config import settings

class RAGManager:
    def __init__(self):
        # Switched to Gemini Embeddings to avoid PyTorch Out-of-Memory (OOM) on free tiers (512MB RAM limit)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=settings.gemini_api_key
        )
        self.persist_directory = settings.chroma_db_dir
        self._init_db()

    def _init_db(self):
        os.makedirs(self.persist_directory, exist_ok=True)
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def ingest_documents(self, documents: list[Document]):
        """
        Ingests LangChain Document objects into ChromaDB.
        """
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()

    def retrieve(self, query: str, k: int = 3) -> list[Document]:
        """
        Retrieves top k most relevant documents.
        """
        return self.vectorstore.similarity_search(query, k=k)

    def get_retriever(self):
        """
        Returns a LangChain retriever object.
        """
        return self.vectorstore.as_retriever()

# Singleton instance
rag_manager = RAGManager()
