import json
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from models.api_models import RunStageRequest, RunStageResponse
from orchestrator import planner
from storage import cosmos_client

router = APIRouter(prefix="/api/stage", tags=["stage"])


@router.post("/run", response_model=RunStageResponse)
async def run_stage(req: RunStageRequest, background_tasks: BackgroundTasks):
    ctx = await cosmos_client.get_session(req.session_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Session not found")

    if req.stage == "ideation":
        background_tasks.add_task(planner.run_ideation, ctx)
    elif req.stage == "execution":
        background_tasks.add_task(planner.run_execution, ctx)
    elif req.stage == "operation":
        background_tasks.add_task(planner.run_operation, ctx)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid stage: {req.stage}")

    return RunStageResponse(session_id=req.session_id, stage=req.stage, status="running")


@router.get("/stream/{session_id}")
async def stream_ideation(session_id: str):
    ctx = await cosmos_client.get_session(session_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Session not found")

    async def event_generator():
        async for agent_name, result in planner.run_ideation_streaming(ctx):
            data = json.dumps({"agent": agent_name, "result": result})
            yield f"data: {data}\n\n"
        yield "data: {\"done\": true}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
