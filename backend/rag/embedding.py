from google import genai
from config import get_settings

_client = None


def _get_client():
    global _client
    if _client is None:
        s = get_settings()
        _client = genai.Client(api_key=s.gemini_api_key)
    return _client


async def get_embedding(text: str) -> list[float]:
    client = _get_client()
    s = get_settings()
    result = client.models.embed_content(
        model=s.gemini_embedding_model,
        contents=text[:2000],
    )
    return result.embeddings[0].values
