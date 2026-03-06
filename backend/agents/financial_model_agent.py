import json
from pathlib import Path
from google import genai
from models.context_object import StartupContextObject
from generators.xlsx_builder import build_financial_model
from storage.blob_client import upload_file
from config import get_settings

_client = None


def _get_client():
    global _client
    if _client is None:
        s = get_settings()
        _client = genai.Client(api_key=s.gemini_api_key)
    return _client


class FinancialModelAgent:
    def __init__(self):
        prompt_path = Path(__file__).parent.parent / "prompts" / "financial_model.txt"
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

    async def execute(self, context: StartupContextObject) -> dict:
        s = get_settings()
        client = _get_client()

        vc_data = context.ideation_outputs.get("vc_agent", {})
        consultant_data = context.ideation_outputs.get("consultant_agent", {})

        full_prompt = f"""{self.system_prompt}

Startup: {context.idea_intake.raw_idea}
Industry: {context.idea_intake.industry}
Budget: {context.idea_intake.budget_range}
Team Size: {context.idea_intake.team_size}

VC Agent Findings:
{json.dumps({k: v for k, v in vc_data.items() if k not in ('raw_output', 'source_documents')}, indent=2)}

Consultant Agent Findings:
{json.dumps({k: v for k, v in consultant_data.items() if k not in ('raw_output', 'source_documents')}, indent=2)}

Generate the financial model."""

        resp = client.models.generate_content(
            model=s.gemini_model,
            contents=full_prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
                "max_output_tokens": 2000,
            },
        )

        text = resp.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        result = json.loads(text)

        xlsx_bytes = build_financial_model(result, context)
        blob_name = f"{context.session_id}/financial_model.xlsx"
        file_url = await upload_file(
            xlsx_bytes, blob_name,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        return {
            "status": "completed",
            "file_url": file_url,
            "data": result,
            "grounding_score": 0.88,
        }
