from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_analyze_endpoint():
    payload = {"incident_id":"INC-4","service":"checkout","source":"ecs","symptom":"ECS unhealthy","evidence":{"target_health":"unhealthy","alb_5xx_rate":"20%","unhealthy_targets":4}}
    r = client.post("/api/v1/incidents/analyze", json=payload)
    assert r.status_code == 200
    assert r.json()["analysis"]["action"] == "restart_service"
