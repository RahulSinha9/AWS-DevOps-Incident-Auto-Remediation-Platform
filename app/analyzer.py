from .models import Analysis, Incident, Severity

def analyze_incident(incident: Incident) -> Analysis:
    ev = incident.evidence
    action = "observe"
    approval = True
    severity = Severity.medium
    cause = "Insufficient evidence"
    confidence = 55
    evidence = []
    if incident.source == "ecs" and ev.get("target_health") == "unhealthy":
        severity = Severity.high
        action = "restart_service"
        approval = False
        cause = "ECS service health degradation correlated with load-balancer failures"
        confidence = 91
        evidence.extend([f"ALB 5xx rate: {ev.get('alb_5xx_rate', 'unknown')}", f"Unhealthy targets: {ev.get('unhealthy_targets', 'unknown')}", f"Deployment revision: {ev.get('deployment_revision', 'unknown')}"])
    elif incident.source == "ecs" and float(ev.get("cpu", 0)) >= 80:
        severity = Severity.medium
        action = "scale_service"
        approval = False
        cause = "Sustained ECS CPU saturation"
        confidence = 88
        evidence.append(f"CPU utilization: {ev.get('cpu')}%")
    elif incident.source == "rds" and float(ev.get("connections_pct", 0)) >= 85:
        severity = Severity.high
        action = "observe"
        approval = True
        cause = "RDS connection pressure may be exhausting the application connection pool"
        confidence = 84
        evidence.append(f"DB connection utilization: {ev.get('connections_pct')}%")
    else:
        evidence.append("No deterministic high-confidence rule matched.")
    return Analysis(incident_id=incident.incident_id, severity=severity, title=incident.symptom, likely_cause=cause, confidence=confidence, recommended_action=action, evidence=evidence, action=action, requires_approval=approval)
