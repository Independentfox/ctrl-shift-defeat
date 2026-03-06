import json
from pathlib import Path
from google import genai
from config import get_settings

_client = None


def _get_client():
    global _client
    if _client is None:
        s = get_settings()
        _client = genai.Client(api_key=s.gemini_api_key)
    return _client


class Synthesizer:
    def __init__(self):
        prompt_path = Path(__file__).parent.parent / "prompts" / "synthesizer.txt"
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

    async def synthesize(self, ideation_outputs: dict) -> dict:
        s = get_settings()
        client = _get_client()

        agent_summaries = {}
        for name in ["shark_tank_agent", "vc_agent", "consultant_agent", "worst_case_customer_agent"]:
            output = ideation_outputs.get(name, {})
            if output.get("status") == "completed":
                agent_summaries[name] = {
                    k: v for k, v in output.items()
                    if k not in ("raw_output", "source_documents")
                }

        full_prompt = f"{self.system_prompt}\n\nAgent Outputs:\n{json.dumps(agent_summaries, indent=2)}"

        resp = client.models.generate_content(
            model=s.gemini_model,
            contents=full_prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
                "max_output_tokens": 1000,
            },
        )

        text = resp.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        result = json.loads(text)
        return {
            "overall_viability_score": result.get("overall_viability_score", 5),
            "top_strengths": result.get("top_strengths", []),
            "top_risks": result.get("top_risks", []),
            "proceed_to_execution": result.get("proceed_to_execution", False),
            "recommendation": result.get("recommendation", ""),
        }
