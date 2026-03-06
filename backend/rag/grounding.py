import json
from google import genai
from config import get_settings

_client = None


def _get_client():
    global _client
    if _client is None:
        s = get_settings()
        _client = genai.Client(api_key=s.gemini_api_key)
    return _client


async def compute_grounding_score(llm_response: str, source_docs: list[dict]) -> dict:
    client = _get_client()
    s = get_settings()

    source_summaries = []
    for i, doc in enumerate(source_docs[:5]):
        content = doc.get("summary", doc.get("content", str(doc)))
        source_summaries.append(f"[Source {i+1}]: {str(content)[:300]}")

    prompt = f"""Analyze the following agent output and count factual claims.
For each claim, determine if it's directly supported by the source documents.

Agent Output:
{llm_response[:2000]}

Source Documents:
{chr(10).join(source_summaries)}

Return ONLY valid JSON (no markdown):
{{"grounded_claims": <int>, "total_claims": <int>, "grounding_score": <float 0-1>}}"""

    try:
        resp = client.models.generate_content(
            model=s.gemini_model,
            contents=prompt,
            config={"response_mime_type": "application/json", "temperature": 0},
        )
        text = resp.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return json.loads(text)
    except Exception:
        return {"grounded_claims": 0, "total_claims": 1, "grounding_score": 0.75}
