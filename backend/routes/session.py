from fastapi import APIRouter, HTTPException
from models.api_models import CreateSessionRequest, CreateSessionResponse, SessionStatusResponse
from models.context_object import StartupContextObject, IdeaIntake
from storage import cosmos_client

router = APIRouter(prefix="/api/session", tags=["session"])


@router.post("/create", response_model=CreateSessionResponse)
async def create_session(req: CreateSessionRequest):
    intake = IdeaIntake(
        raw_idea=req.raw_idea,
        industry=req.industry,
        stage=req.stage,
        team_size=req.team_size,
        geography=req.geography,
        budget_range=req.budget_range,
        target_customer=req.target_customer,
        b2b_or_b2c=req.b2b_or_b2c,
        has_cofounder=req.has_cofounder,
    )
    ctx = StartupContextObject(idea_intake=intake)
    await cosmos_client.save_session(ctx)
    return CreateSessionResponse(session_id=ctx.session_id)


@router.get("/{session_id}/output")
async def get_output(session_id: str):
    ctx = await cosmos_client.get_session(session_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Session not found")
    return ctx.model_dump()


@router.get("/{session_id}/status", response_model=SessionStatusResponse)
async def get_status(session_id: str):
    ctx = await cosmos_client.get_session(session_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Session not found")

    agent_statuses = {}
    for name in ["shark_tank_agent", "vc_agent", "consultant_agent", "worst_case_customer_agent"]:
        output = ctx.ideation_outputs.get(name, {})
        agent_statuses[name] = output.get("status", "pending")

    # Determine current stage
    if ctx.operation_outputs.get("status") == "completed":
        stage = "operation"
    elif ctx.execution_outputs.get("pitch_deck", {}).get("status") == "completed":
        stage = "execution"
    elif ctx.ideation_outputs.get("synthesis"):
        stage = "ideation"
    else:
        stage = "intake"

    all_done = all(s == "completed" for s in agent_statuses.values())
    return SessionStatusResponse(
        session_id=session_id,
        stage=stage,
        agent_statuses=agent_statuses,
        status="completed" if all_done else "running",
    )
