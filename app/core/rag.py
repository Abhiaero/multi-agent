import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.documents import Document
from app.core.config import settings

class RAGManager:
    def __init__(self):
        # Switched to FastEmbed for extremely fast, lightweight local embeddings 
        # (Zero API limits, 100% free, and no PyTorch OOM errors)
        self.embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
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
