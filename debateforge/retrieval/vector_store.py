class VectorStore:
    def __init__(self):
        self.documents = {}

    def add(self, doc_id: str, text: str, metadata: dict = {}):
        self.documents[doc_id] = {"text": text, "metadata": metadata}

    def search(self, query: str, top_k: int = 3) -> list[str]:
        return [doc["text"] for doc in list(self.documents.values())[:top_k]]