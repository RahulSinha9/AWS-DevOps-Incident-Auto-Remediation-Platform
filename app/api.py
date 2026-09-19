from fastapi import APIRouter
from .analyzer import analyze_incident
from .models import Incident
from .remediation import execute_remediation

router = APIRouter(prefix="/api/v1", tags=["incidents"])

@router.post("/incidents/analyze")
def analyze(payload: Incident):
    analysis = analyze_incident(payload)
    remediation = execute_remediation(analysis)
    return {"analysis": analysis, "remediation": remediation}
