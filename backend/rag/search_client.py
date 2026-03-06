from azure.search.documents import SearchClient as AzureSearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from rag.embedding import get_embedding
from config import get_settings


class SearchClient:
    def __init__(self, index_name: str):
        s = get_settings()
        self.client = AzureSearchClient(
            endpoint=s.azure_search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(s.azure_search_api_key),
        )
        self.index_name = index_name

    async def hybrid_search(
        self, query: str, top_k: int = 10, filters: dict | None = None
    ) -> list[dict]:
        embedding = await get_embedding(query)
        vector_query = VectorizedQuery(
            vector=embedding,
            k_nearest_neighbors=top_k,
            fields="embedding",
        )

        filter_str = self._build_odata_filter(filters) if filters else None

        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            filter=filter_str,
            top=top_k,
        )

        docs = []
        for r in results:
            doc = dict(r)
            doc["_score"] = r.get("@search.score", 0)
            docs.append(doc)
        return docs

    @staticmethod
    def _build_odata_filter(filters: dict) -> str:
        clauses = []
        for field, value in filters.items():
            if value is not None:
                clauses.append(f"{field} eq '{value}'")
        return " and ".join(clauses) if clauses else None
