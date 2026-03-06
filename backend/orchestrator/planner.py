import asyncio
from models.context_object import StartupContextObject
from agents.shark_tank_agent import SharkTankAgent
from agents.vc_agent import VCAgent
from agents.consultant_agent import ConsultantAgent
from agents.customer_agent import CustomerAgent
from agents.synthesizer import Synthesizer
from storage import cosmos_client


IDEATION_AGENTS = [
    ("shark_tank_agent", SharkTankAgent),
    ("vc_agent", VCAgent),
    ("consultant_agent", ConsultantAgent),
    ("worst_case_customer_agent", CustomerAgent),
]


async def run_ideation(context: StartupContextObject) -> StartupContextObject:
    agents = [(name, cls()) for name, cls in IDEATION_AGENTS]

    results = await asyncio.gather(
        *[agent.execute(context) for _, agent in agents],
        return_exceptions=True,
    )

    for i, (name, _) in enumerate(agents):
        result = results[i]
        if isinstance(result, Exception):
            context.ideation_outputs[name] = {
                "status": "error",
                "error": str(result),
                "grounding_score": 0,
            }
        else:
            context.ideation_outputs[name] = result

    # Synthesize
    synthesis = await Synthesizer().synthesize(context.ideation_outputs)
    context.ideation_outputs["synthesis"] = synthesis

    context.bump_version()
    await cosmos_client.save_session(context)
    return context


async def run_ideation_streaming(context: StartupContextObject):
    """Yields agent results as they complete (for SSE)."""
    agents = [(name, cls()) for name, cls in IDEATION_AGENTS]
    tasks = {
        asyncio.create_task(agent.execute(context)): name
        for name, agent in agents
    }

    for coro in asyncio.as_completed(tasks.keys()):
        task = None
        for t in tasks:
            if t is coro or (hasattr(coro, 'cr_frame') and t is coro):
                task = t
                break

        try:
            result = await coro
            # Find which agent this was
            for t, name in tasks.items():
                if t.done() and not hasattr(t, '_yielded'):
                    context.ideation_outputs[name] = result
                    t._yielded = True
                    yield name, result
                    break
        except Exception as e:
            for t, name in tasks.items():
                if t.done() and not hasattr(t, '_yielded'):
                    error_result = {"status": "error", "error": str(e), "grounding_score": 0}
                    context.ideation_outputs[name] = error_result
                    t._yielded = True
                    yield name, error_result
                    break

    synthesis = await Synthesizer().synthesize(context.ideation_outputs)
    context.ideation_outputs["synthesis"] = synthesis
    context.bump_version()
    await cosmos_client.save_session(context)
    yield "synthesis", synthesis


async def run_execution(context: StartupContextObject) -> StartupContextObject:
    from agents.pitch_deck_agent import PitchDeckAgent
    from agents.financial_model_agent import FinancialModelAgent

    pitch_result = await PitchDeckAgent().execute(context)
    context.execution_outputs["pitch_deck"] = pitch_result

    financial_result = await FinancialModelAgent().execute(context)
    context.execution_outputs["financial_model"] = financial_result

    context.bump_version()
    await cosmos_client.save_session(context)
    return context


async def run_operation(context: StartupContextObject) -> StartupContextObject:
    from agents.operations_agent import OperationsAgent

    roadmap = await OperationsAgent().execute(context)
    context.operation_outputs = roadmap

    context.bump_version()
    await cosmos_client.save_session(context)
    return context
