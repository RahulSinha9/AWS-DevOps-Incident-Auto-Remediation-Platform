from .config import settings
from .models import Analysis, RemediationResult
from .policy import authorize

def execute_remediation(analysis: Analysis) -> RemediationResult:
    policy = authorize(analysis)
    if not policy.auto_execute:
        return RemediationResult(incident_id=analysis.incident_id, action=analysis.action, executed=False, dry_run=settings.dry_run, message=f"Approval required for risk={policy.risk}")
    if settings.dry_run:
        return RemediationResult(incident_id=analysis.incident_id, action=analysis.action, executed=False, dry_run=True, message="Dry-run enabled; remediation was simulated.")
    return RemediationResult(incident_id=analysis.incident_id, action=analysis.action, executed=False, dry_run=False, message="AWS executor hook is ready for integration.")
