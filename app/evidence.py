from typing import Any
import boto3

def collect_ecs_service(service_name: str, cluster: str, region: str) -> dict[str, Any]:
    client = boto3.client("ecs", region_name=region)
    svc = client.describe_services(cluster=cluster, services=[service_name])["services"][0]
    return {"service": svc["serviceName"], "running_count": svc.get("runningCount", 0), "desired_count": svc.get("desiredCount", 0), "deployments": len(svc.get("deployments", []))}
