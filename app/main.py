from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from .api import router

app = FastAPI(title="AWS DevOps Incident & Auto-Remediation Platform", version="0.1.0")
INCIDENTS = Counter("incidents_analyzed_total", "Total incidents analyzed")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
