from agents.base_agent import BaseAgent
from models.context_object import StartupContextObject


class ConsultantAgent(BaseAgent):
    agent_name = "consultant_agent"
    search_index = "funding_patterns"
    system_prompt_file = "consultant.txt"

    def build_query(self, context: StartupContextObject) -> str:
        i = context.idea_intake
        return f"{i.industry} market size competitors {i.geography} {i.target_customer} startup"

    def build_filters(self, context: StartupContextObject) -> dict | None:
        return None

    def structure_output(self, llm_response: dict, docs: list, grounding: dict) -> dict:
        return {
            "market_size_verified": llm_response.get("market_size_verified", "Insufficient data"),
            "market_size_source": llm_response.get("market_size_source", ""),
            "tam": llm_response.get("tam", ""),
            "sam": llm_response.get("sam", ""),
            "som": llm_response.get("som", ""),
            "top_competitors": llm_response.get("top_competitors", []),
            "strategic_gap": llm_response.get("strategic_gap", ""),
            "strategy_score": llm_response.get("strategy_score", 5),
            "summary": llm_response.get("summary", ""),
            "raw_output": llm_response.get("raw_text", ""),
        }
