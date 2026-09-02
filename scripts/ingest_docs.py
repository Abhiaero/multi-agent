import os
import argparse
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.rag import rag_manager

def ingest_directory(directory_path: str):
    """
    Loads text files from a directory, chunks them, and ingests them into ChromaDB.
    """
    print(f"Loading documents from {directory_path}...")
    
    # Load documents
    loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("No .txt documents found in the directory.")
        return

    print(f"Loaded {len(documents)} documents. Splitting text...")
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    
    print(f"Split into {len(chunks)} chunks. Ingesting into vector store...")
    
    # Ingest into Chroma
    rag_manager.ingest_documents(chunks)
    print("Ingestion complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into the RAG vector store.")
    parser.add_argument(
        "--dir", 
        type=str, 
        required=True, 
        help="Path to the directory containing .txt files."
    )
    args = parser.parse_args()
    
    if not os.path.exists(args.dir):
        print(f"Error: Directory '{args.dir}' does not exist.")
    else:
        ingest_directory(args.dir)
