from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class IdeaIntake(BaseModel):
    raw_idea: str
    industry: str
    stage: str = "Idea"
    team_size: int = 1
    geography: str = "India - Tier 2"
    budget_range: str = "< 5L"
    target_customer: str = ""
    b2b_or_b2c: str = "B2C"
    has_cofounder: bool = False


class OverrideEntry(BaseModel):
    version: int
    field_changed: str
    old_value: Any
    new_value: Any
    agents_rerun: List[str] = []
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class AgentOutput(BaseModel):
    status: str = "pending"
    grounding_score: float = 0.0
    source_documents: List[str] = []
    raw_output: str = ""
    data: Dict[str, Any] = {}


class SynthesisOutput(BaseModel):
    overall_viability_score: float = 0.0
    top_risks: List[str] = []
    top_strengths: List[str] = []
    proceed_to_execution: bool = False


class PitchDeckOutput(BaseModel):
    status: str = "pending"
    file_url: str = ""
    slides_generated: int = 0
    evidence_citations: int = 0
    grounding_score: float = 0.0


class FinancialModelOutput(BaseModel):
    status: str = "pending"
    file_url: str = ""
    data: Dict[str, Any] = {}
    grounding_score: float = 0.0


class OperationOutput(BaseModel):
    status: str = "pending"
    funding_path: str = ""
    roadmap: List[Dict[str, Any]] = []
    grounding_score: float = 0.0


class StartupContextObject(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: int = 1
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    idea_intake: IdeaIntake

    user_overrides: Dict[str, Any] = Field(default_factory=lambda: {"override_history": []})

    ideation_outputs: Dict[str, Any] = Field(default_factory=dict)
    execution_outputs: Dict[str, Any] = Field(default_factory=dict)
    operation_outputs: Dict[str, Any] = Field(default_factory=dict)

    def bump_version(self):
        self.version += 1
        self.last_updated = datetime.utcnow().isoformat()
