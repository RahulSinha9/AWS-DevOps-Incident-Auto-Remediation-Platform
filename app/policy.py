from dataclasses import dataclass
from .config import settings
from .models import Analysis

@dataclass(frozen=True)
class Policy:
    action: str
    risk: str
    auto_execute: bool
    max_tasks: int | None = None

POLICIES = {
    "restart_service": Policy("restart_service", "low", True),
    "scale_service": Policy("scale_service", "medium", True, settings.max_scale_tasks),
    "rollback_deployment": Policy("rollback_deployment", "high", False),
    "modify_network": Policy("modify_network", "high", False),
    "modify_iam": Policy("modify_iam", "critical", False),
    "delete_resource": Policy("delete_resource", "critical", False),
    "observe": Policy("observe", "low", False),
}

def authorize(analysis: Analysis) -> Policy:
    return POLICIES.get(analysis.action, POLICIES["observe"])
