from app.analyzer import analyze_incident
from app.models import Incident

def test_ecs_unhealthy():
    incident = Incident(incident_id="INC-1", service="checkout", source="ecs", symptom="unhealthy", evidence={"target_health":"unhealthy","alb_5xx_rate":"18%","unhealthy_targets":3})
    result = analyze_incident(incident)
    assert result.severity.value == "HIGH"
    assert result.action == "restart_service"
    assert result.confidence == 91

def test_cpu_rule():
    incident = Incident(incident_id="INC-2", service="api", source="ecs", symptom="high cpu", evidence={"cpu":92})
    assert analyze_incident(incident).action == "scale_service"
