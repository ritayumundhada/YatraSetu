from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models

router = APIRouter(tags=["host_safety"])

class ReportCreate(BaseModel):
    type: str
    location: str
    date: str
    severity: str
    note: str
    anonymous: Optional[bool] = False

class IncidentCreate(BaseModel):
    tourist_id: int
    incident_type: str
    description: str
    location_lat_lng: Optional[str] = "19.0760, 72.8777"

# --- HOST ENDPOINTS ---
@router.get("/host/requests")
def host_requests():
    return [
        {"id": "r1", "traveller": "Sarah Johnson", "from": "Manchester, UK", "match": 94, "guests": 2, "date": "2026-09-07", "status": "pending"},
        {"id": "r2", "traveller": "Kiran Bhat", "from": "Bengaluru, India", "match": 87, "guests": 1, "date": "2026-09-14", "status": "pending"}
    ]

@router.post("/host/requests/{req_id}")
def respond_host_request(req_id: str, payload: dict):
    return {"ok": True, "id": req_id, "accepted": payload.get("accepted", True)}

# --- SAFETY & INCIDENT ENDPOINTS ---
@router.get("/safety/reports")
def list_reports(db: Session = Depends(get_db)):
    return []

@router.post("/safety/reports")
def submit_report(payload: ReportCreate):
    return {"ok": True, "report_id": "rep_mock"}

@router.post("/safety/checkin")
def safety_checkin(payload: dict):
    return {"ok": True, "checked_in": True}

@router.post("/api/incident/")
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = models.Incident(
        tourist_id=payload.tourist_id,
        incident_type=payload.incident_type,
        description=payload.description,
        location_lat_lng=payload.location_lat_lng,
        ai_severity="HIGH",
        status="OPEN"
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return {"ok": True, "incident_id": incident.id}