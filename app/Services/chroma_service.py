# app/Services/chroma_service.py

import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


CHROMA_DIR      = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "..", "embedding", "chroma_db")
COLLECTION_NAME = "job_description"


class ChromaService:

    def __init__(self):
        embedding_fn = OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )

        client = chromadb.PersistentClient(path=CHROMA_DIR)

        self.collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn
        )

    def query(self, question: str, n_results: int = 3) :
        """
        Return the most relevant chunks for a given question.
        Used by InfoAdvisor for dynamic retrieval.
        """
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        chunks = results.get("documents", [[]])[0]
        return "\n\n".join(chunks)

    def get_full_document(self) :
        """
        Return all chunks from the collection as a single string.
        Used by ExitAdvisor and SchedulingAdvisor to understand
        the full job description.
        """
        results = self.collection.get()
        chunks  = results.get("documents", [])
        return "\n\n".join(chunks)
