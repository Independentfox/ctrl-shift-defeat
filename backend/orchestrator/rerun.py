from datetime import datetime
from models.context_object import StartupContextObject
from agents.shark_tank_agent import SharkTankAgent
from agents.vc_agent import VCAgent
from agents.consultant_agent import ConsultantAgent
from agents.customer_agent import CustomerAgent
from agents.synthesizer import Synthesizer
from storage import cosmos_client


AGENT_REGISTRY = {
    "shark_tank_agent": SharkTankAgent,
    "vc_agent": VCAgent,
    "consultant_agent": ConsultantAgent,
    "worst_case_customer_agent": CustomerAgent,
}

FIELD_TO_AGENT_MAP = {
    "industry": list(AGENT_REGISTRY.keys()),
    "target_customer": ["shark_tank_agent", "worst_case_customer_agent", "consultant_agent"],
    "b2b_or_b2c": list(AGENT_REGISTRY.keys()),
    "geography": ["vc_agent", "consultant_agent"],
    "has_cofounder": ["vc_agent"],
    "budget_range": ["consultant_agent"],
    "stage": ["vc_agent"],
    "team_size": ["vc_agent"],
}


async def rerun_agent(
    session_id: str, agent_name: str, overrides: dict
) -> StartupContextObject:
    ctx = await cosmos_client.get_session(session_id)
    if not ctx:
        raise ValueError(f"Session {session_id} not found")

    # Apply overrides
    for field, new_val in overrides.items():
        old_val = getattr(ctx.idea_intake, field, None)
        if old_val != new_val:
            setattr(ctx.idea_intake, field, new_val)
            ctx.user_overrides.setdefault("override_history", []).append({
                "version": ctx.version + 1,
                "field_changed": field,
                "old_value": old_val,
                "new_value": new_val,
                "agents_rerun": [agent_name],
                "timestamp": datetime.utcnow().isoformat(),
            })

    # Re-run agent
    if agent_name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent: {agent_name}")

    agent = AGENT_REGISTRY[agent_name]()
    result = await agent.execute(ctx)
    ctx.ideation_outputs[agent_name] = result

    # Recompute synthesis
    ctx.ideation_outputs["synthesis"] = await Synthesizer().synthesize(ctx.ideation_outputs)

    # Mark downstream as stale
    if ctx.execution_outputs.get("pitch_deck", {}).get("status") == "completed":
        ctx.execution_outputs["pitch_deck"]["status"] = "stale"
    if ctx.execution_outputs.get("financial_model", {}).get("status") == "completed":
        ctx.execution_outputs["financial_model"]["status"] = "stale"
    if ctx.operation_outputs.get("status") == "completed":
        ctx.operation_outputs["status"] = "stale"

    ctx.bump_version()
    await cosmos_client.save_session(ctx)
    return ctx
