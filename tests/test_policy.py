from app.models import Analysis, Severity
from app.policy import authorize

def test_dangerous_action_requires_approval():
    analysis = Analysis(incident_id="INC-3", severity=Severity.critical, title="network change", likely_cause="unknown", confidence=95, recommended_action="modify network", evidence=[], action="modify_network", requires_approval=True)
    policy = authorize(analysis)
    assert policy.auto_execute is False
    assert policy.risk == "high"
