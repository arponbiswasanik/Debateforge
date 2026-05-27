from debateforge.retrieval.financial_loader import FinancialLoader
from debateforge.retrieval.vector_store import VectorStore


class FinancialRetriever:
    def __init__(self):
        self.loader = FinancialLoader()
        self.store = VectorStore()

    def load_ticker(self, ticker: str) -> str:
        data = self.loader.load(ticker)
        context = self.loader.to_context(data)
        self.store.add(
            doc_id=ticker,
            text=context,
            metadata={"ticker": ticker, "name": data["name"]},
        )
        return context

    def retrieve(self, query: str, top_k: int = 3) -> str:
        results = self.store.search(query, top_k)
        if not results:
            return ""
        return "\n\n".join(results)