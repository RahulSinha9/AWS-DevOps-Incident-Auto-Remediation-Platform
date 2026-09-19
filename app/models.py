from enum import Enum
from pydantic import BaseModel, Field
from typing import Any

class Severity(str, Enum):
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"
    critical = "CRITICAL"

class Incident(BaseModel):
    incident_id: str
    service: str
    source: str
    symptom: str
    evidence: dict[str, Any] = Field(default_factory=dict)

class Analysis(BaseModel):
    incident_id: str
    severity: Severity
    title: str
    likely_cause: str
    confidence: int = Field(ge=0, le=100)
    recommended_action: str
    evidence: list[str] = Field(default_factory=list)
    action: str
    requires_approval: bool

class RemediationResult(BaseModel):
    incident_id: str
    action: str
    executed: bool
    dry_run: bool
    message: str
