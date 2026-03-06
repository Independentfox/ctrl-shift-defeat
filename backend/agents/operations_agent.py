import json
from pathlib import Path
from google import genai
from models.context_object import StartupContextObject
from config import get_settings

_client = None


def _get_client():
    global _client
    if _client is None:
        s = get_settings()
        _client = genai.Client(api_key=s.gemini_api_key)
    return _client


class OperationsAgent:
    def __init__(self):
        prompt_path = Path(__file__).parent.parent / "prompts" / "operations.txt"
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

    async def execute(self, context: StartupContextObject) -> dict:
        s = get_settings()
        client = _get_client()

        financial_data = context.execution_outputs.get("financial_model", {}).get("data", {})
        vc_data = context.ideation_outputs.get("vc_agent", {})

        full_prompt = f"""{self.system_prompt}

Startup: {context.idea_intake.raw_idea}
Industry: {context.idea_intake.industry}
Budget: {context.idea_intake.budget_range}
Has Co-founder: {context.idea_intake.has_cofounder}
Team Size: {context.idea_intake.team_size}

Financial Model:
{json.dumps(financial_data, indent=2)}

VC Agent Recommended Funding Path: {vc_data.get('recommended_funding_path', 'Not available')}

Generate the operations roadmap."""

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
        return {
            "status": "completed",
            "funding_path": result.get("funding_path", ""),
            "financial_reality": result.get("financial_reality", {}),
            "roadmap": result.get("roadmap", []),
            "grounding_score": result.get("grounding_score", 0.8),
            "raw_output": result.get("raw_text", ""),
        }
