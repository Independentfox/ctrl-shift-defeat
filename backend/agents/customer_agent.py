from agents.base_agent import BaseAgent
from models.context_object import StartupContextObject


class CustomerAgent(BaseAgent):
    agent_name = "worst_case_customer_agent"
    search_index = "combined_outcomes"
    system_prompt_file = "customer.txt"

    def build_query(self, context: StartupContextObject) -> str:
        i = context.idea_intake
        return f"{i.industry} {i.b2b_or_b2c} startup failure customer objections {i.target_customer}"

    def build_filters(self, context: StartupContextObject) -> dict | None:
        return {"source_type": "failure_postmortem"}

    def structure_output(self, llm_response: dict, docs: list, grounding: dict) -> dict:
        return {
            "customer_archetypes_analyzed": llm_response.get("customer_archetypes_analyzed", 0),
            "objections_by_persona": llm_response.get("objections_by_persona", {}),
            "failure_patterns_found": llm_response.get("failure_patterns_found", []),
            "friction_score": llm_response.get("friction_score", 5),
            "summary": llm_response.get("summary", ""),
            "raw_output": llm_response.get("raw_text", ""),
        }
