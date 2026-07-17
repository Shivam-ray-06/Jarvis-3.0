import chromadb
import hashlib
from typing import List

class MemoryManager:
    """Manages long-term memory for Jarvis using ChromaDB."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="jarvis_memory")

    def store(self, user_input: str, assistant_response: str):
        """Stores an interaction in the vector database."""
        doc = f"User: {user_input}\nJarvis: {assistant_response}"
        # Create a deterministic ID based on content
        doc_id = hashlib.sha256(doc.encode('utf-8')).hexdigest()
        
        # Add to collection (chromadb automatically generates embeddings if none provided)
        self.collection.add(
            documents=[doc],
            ids=[doc_id]
        )

    def retrieve(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieves relevant past interactions based on a query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        if results and results.get('documents') and len(results['documents']) > 0:
            return results['documents'][0]
        return []
