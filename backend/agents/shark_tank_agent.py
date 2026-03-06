from agents.base_agent import BaseAgent
from models.context_object import StartupContextObject


class SharkTankAgent(BaseAgent):
    agent_name = "shark_tank_agent"
    search_index = "combined_outcomes"
    system_prompt_file = "shark_tank.txt"

    def build_query(self, context: StartupContextObject) -> str:
        i = context.idea_intake
        return f"{i.industry} {i.b2b_or_b2c} startup pitch outcome {i.target_customer} {i.raw_idea[:100]}"

    def build_filters(self, context: StartupContextObject) -> dict | None:
        return {"source_type": "pitch_outcome"}

    def structure_output(self, llm_response: dict, docs: list, grounding: dict) -> dict:
        return {
            "similar_pitches_found": llm_response.get("similar_pitches_found", len(docs)),
            "funded_count": llm_response.get("funded_count", 0),
            "rejected_count": llm_response.get("rejected_count", 0),
            "common_rejection_reasons": llm_response.get("common_rejection_reasons", []),
            "common_funded_signals": llm_response.get("common_funded_signals", []),
            "your_gaps": llm_response.get("your_gaps", []),
            "score": llm_response.get("score", 5),
            "summary": llm_response.get("summary", ""),
            "raw_output": llm_response.get("raw_text", ""),
        }
