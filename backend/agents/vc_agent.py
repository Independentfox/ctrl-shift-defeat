from agents.base_agent import BaseAgent
from models.context_object import StartupContextObject


class VCAgent(BaseAgent):
    agent_name = "vc_agent"
    search_index = "yc_companies"
    system_prompt_file = "vc.txt"

    def build_query(self, context: StartupContextObject) -> str:
        i = context.idea_intake
        return f"{i.industry} {i.b2b_or_b2c} {i.stage} startup {i.geography} {i.raw_idea[:100]}"

    def build_filters(self, context: StartupContextObject) -> dict | None:
        return None

    def structure_output(self, llm_response: dict, docs: list, grounding: dict) -> dict:
        return {
            "fundability_score": llm_response.get("fundability_score", 5),
            "comparable_companies_analyzed": llm_response.get("comparable_companies_analyzed", len(docs)),
            "positive_signals": llm_response.get("positive_signals", []),
            "red_flags": llm_response.get("red_flags", []),
            "recommended_funding_path": llm_response.get("recommended_funding_path", ""),
            "funded_at_this_stage": llm_response.get("funded_at_this_stage", 0),
            "not_funded_count": llm_response.get("not_funded_count", 0),
            "summary": llm_response.get("summary", ""),
            "raw_output": llm_response.get("raw_text", ""),
        }
