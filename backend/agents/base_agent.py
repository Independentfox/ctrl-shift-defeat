import json
from abc import ABC, abstractmethod
from pathlib import Path
from google import genai
from rag.search_client import SearchClient
from rag.grounding import compute_grounding_score
from models.context_object import StartupContextObject
from config import get_settings

_llm_client = None


def _get_llm():
    global _llm_client
    if _llm_client is None:
        s = get_settings()
        _llm_client = genai.Client(api_key=s.gemini_api_key)
    return _llm_client


class BaseAgent(ABC):
    agent_name: str = "base"
    search_index: str = ""
    system_prompt_file: str = ""

    def __init__(self):
        self.search_client = SearchClient(self.search_index) if self.search_index else None
        self.system_prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        if not self.system_prompt_file:
            return ""
        path = Path(__file__).parent.parent / "prompts" / self.system_prompt_file
        return path.read_text(encoding="utf-8")

    async def execute(self, context: StartupContextObject) -> dict:
        query = self.build_query(context)

        docs = []
        if self.search_client:
            filters = self.build_filters(context)
            docs = await self.search_client.hybrid_search(query, top_k=10, filters=filters)
            docs = [d for d in docs if d.get("_score", 0) > 0.5][:5]

        llm_response = await self._reason(context, docs)

        grounding = await compute_grounding_score(
            llm_response.get("raw_text", json.dumps(llm_response)), docs
        )

        output = self.structure_output(llm_response, docs, grounding)
        output["status"] = "completed"
        output["grounding_score"] = grounding.get("grounding_score", 0.75)
        output["source_documents"] = [
            d.get("id", d.get("pitch_id", d.get("company_id", f"doc_{i}")))
            for i, d in enumerate(docs)
        ]
        return output

    async def _reason(self, context: StartupContextObject, docs: list[dict]) -> dict:
        s = get_settings()
        client = _get_llm()

        evidence = "\n\n".join(
            f"[Source {i+1}: {d.get('id', 'unknown')}]\n{self._doc_summary(d)}"
            for i, d in enumerate(docs)
        )

        user_msg = f"""Startup Context:
{context.idea_intake.model_dump_json(indent=2)}

Retrieved Evidence ({len(docs)} documents):
{evidence if evidence else "No relevant documents found. Use your best judgment but note low grounding."}

Analyze this startup idea based on the evidence above. Return structured JSON as specified."""

        full_prompt = f"{self.system_prompt}\n\n{user_msg}"

        resp = client.models.generate_content(
            model=s.gemini_model,
            contents=full_prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.3,
                "max_output_tokens": 2000,
            },
        )

        text = resp.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        result = json.loads(text)
        result["raw_text"] = resp.text
        return result

    @staticmethod
    def _doc_summary(doc: dict) -> str:
        skip = {"embedding", "_score", "@search.score"}
        parts = []
        for k, v in doc.items():
            if k not in skip and v:
                parts.append(f"{k}: {v}")
        return "\n".join(parts[:10])

    @abstractmethod
    def build_query(self, context: StartupContextObject) -> str: ...

    def build_filters(self, context: StartupContextObject) -> dict | None:
        return None

    @abstractmethod
    def structure_output(self, llm_response: dict, docs: list, grounding: dict) -> dict: ...
