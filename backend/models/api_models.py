from pydantic import BaseModel
from typing import Optional, Dict, Any


class CreateSessionRequest(BaseModel):
    raw_idea: str
    industry: str
    stage: str = "Idea"
    team_size: int = 1
    geography: str = "India - Tier 2"
    budget_range: str = "< 5L"
    target_customer: str = ""
    b2b_or_b2c: str = "B2C"
    has_cofounder: bool = False


class CreateSessionResponse(BaseModel):
    session_id: str
    status: str = "created"


class RunStageRequest(BaseModel):
    session_id: str
    stage: str  # "ideation" | "execution" | "operation"


class RunStageResponse(BaseModel):
    session_id: str
    stage: str
    status: str = "running"


class RerunAgentRequest(BaseModel):
    session_id: str
    agent_name: str
    overrides: Dict[str, Any] = {}


class SessionStatusResponse(BaseModel):
    session_id: str
    stage: str
    agent_statuses: Dict[str, str] = {}
    status: str = "pending"


class DownloadResponse(BaseModel):
    download_url: str
    file_type: str
