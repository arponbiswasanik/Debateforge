import chromadb
from sentence_transformers import SentenceTransformer
from debateforge.config.settings import settings


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory
        )
        self.collection = self.client.get_or_create_collection("financial_data")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def add(self, doc_id: str, text: str, metadata: dict = {}):
        embedding = self.embedder.encode(text).tolist()
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
        )

    def search(self, query: str, top_k: int = 3) -> list[str]:
        embedding = self.embedder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )
        return results["documents"][0] if results["documents"] else []