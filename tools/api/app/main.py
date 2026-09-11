from pathlib import Path
import json

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Noir DevOps Incident Intelligence Tools",
    description=(
        "Read-only investigation tools for the Noir AI-Powered "
        "DevOps & Incident Intelligence Platform."
    ),
    version="1.0.0",
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = PROJECT_ROOT / "data"


def load_json(path: Path) -> dict:
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Evidence file not found: {path.name}",
        )

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON evidence file: {path.name}",
        ) from exc


@app.get(
    "/incidents/{incident_id}",
    summary="Get incident details",
)
def get_incident(incident_id: str):
    path = DATA_ROOT / "incidents" / incident_id / "incident.json"
    return load_json(path)


@app.get(
    "/repository/releases/{version}",
    summary="Get repository and release evidence",
)
def get_release_evidence(version: str):
    path = (
        DATA_ROOT
        / "repositories"
        / "noir-operations"
        / "release-v2.8.4.json"
    )

    evidence = load_json(path)

    if evidence.get("current_version") != version:
        raise HTTPException(
            status_code=404,
            detail=f"No repository evidence found for release {version}.",
        )

    return evidence


@app.get(
    "/observability/{incident_id}",
    summary="Get observability evidence for an incident",
)
def get_observability(incident_id: str):
    path = DATA_ROOT / "logs" / incident_id / "observability.json"
    return load_json(path)


@app.get(
    "/knowledge/historical-incidents",
    summary="Get historical incident evidence",
)
def get_historical_incidents():
    path = DATA_ROOT / "knowledge" / "historical-incidents.json"
    return load_json(path)


@app.get(
    "/knowledge/database-troubleshooting",
    summary="Get database troubleshooting guidance",
)
def get_database_troubleshooting():
    path = DATA_ROOT / "knowledge" / "database-troubleshooting.md"

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="Database troubleshooting runbook not found.",
        )

    return {
        "title": "Database Connection Troubleshooting Runbook",
        "content": path.read_text(encoding="utf-8"),
    }


@app.get(
    "/health",
    summary="Check tool service health",
)
def health():
    return {
        "status": "healthy",
        "service": "noir-devops-incident-intelligence-tools",
    }