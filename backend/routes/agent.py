from fastapi import APIRouter, HTTPException
from models.api_models import RerunAgentRequest
from orchestrator.rerun import rerun_agent

router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/rerun")
async def rerun(req: RerunAgentRequest):
    try:
        ctx = await rerun_agent(req.session_id, req.agent_name, req.overrides)
        return ctx.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
