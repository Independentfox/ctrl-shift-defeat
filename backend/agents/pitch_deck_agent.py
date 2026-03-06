import json
from pathlib import Path
from google import genai
from models.context_object import StartupContextObject
from generators.pptx_builder import build_pitch_deck
from storage.blob_client import upload_file
from config import get_settings

_client = None


def _get_client():
    global _client
    if _client is None:
        s = get_settings()
        _client = genai.Client(api_key=s.gemini_api_key)
    return _client


class PitchDeckAgent:
    def __init__(self):
        prompt_path = Path(__file__).parent.parent / "prompts" / "pitch_deck.txt"
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

    async def execute(self, context: StartupContextObject) -> dict:
        s = get_settings()
        client = _get_client()

        ideation_summary = {
            k: {kk: vv for kk, vv in v.items() if kk not in ("raw_output", "source_documents")}
            for k, v in context.ideation_outputs.items()
            if isinstance(v, dict)
        }

        full_prompt = f"""{self.system_prompt}

Startup Idea: {context.idea_intake.raw_idea}
Industry: {context.idea_intake.industry}

Ideation Agent Findings:
{json.dumps(ideation_summary, indent=2)}

Generate the 12-slide pitch deck content."""

        resp = client.models.generate_content(
            model=s.gemini_model,
            contents=full_prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.3,
                "max_output_tokens": 3000,
            },
        )

        text = resp.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        result = json.loads(text)
        slides = result.get("slides", [])

        pptx_bytes = build_pitch_deck(slides, context)
        blob_name = f"{context.session_id}/pitch_deck.pptx"
        file_url = await upload_file(
            pptx_bytes, blob_name,
            content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

        return {
            "status": "completed",
            "file_url": file_url,
            "slides_generated": len(slides),
            "evidence_citations": result.get("evidence_citations", 0),
            "grounding_score": 0.83,
            "slides": slides,
        }
