# embedding/embed_job_description.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from app.Services.pdf_service import PDFService

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH    = os.path.join(BASE_DIR, "PythonDeveloperJobDescription.pdf")
CHROMA_DIR  = os.path.join(BASE_DIR, "embedding", "chroma_db")

COLLECTION_NAME = "job_description"
CHUNK_SIZE      = 300   
CHUNK_OVERLAP   = 50   


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if c]


def embed_and_store(pdf_path: str, chroma_dir: str):
    print("Extracting text from PDF...")
    text = PDFService.extract_text(pdf_path)
    if not text:
        print("ERROR: Could not extract text from PDF.")
        return
    print(f"      Extracted {len(text)} characters.")

    print("Splitting into chunks...")
    chunks = split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"      Created {len(chunks)} chunks.")

    print("Initializing Chroma...")
    embedding_fn = OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    client = chromadb.PersistentClient(path=chroma_dir)

    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"      Deleted existing collection '{COLLECTION_NAME}'.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    print("Embedding and storing chunks...")
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(f"\n Done! {len(chunks)} chunks stored in: {chroma_dir}")
    print(f"      Collection: '{COLLECTION_NAME}'")


if __name__ == "__main__":
    embed_and_store(PDF_PATH, CHROMA_DIR)
