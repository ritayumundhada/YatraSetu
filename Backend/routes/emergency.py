from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models

router = APIRouter(prefix="/emergency", tags=["emergency"])

class ContactCreate(BaseModel):
    name: str
    phone: str
    relation: Optional[str] = ""
    tourist_id: Optional[int] = 1

class SOSAlert(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None
    note: Optional[str] = ""
    tourist_id: Optional[int] = None

@router.get("/contacts")
def list_contacts(tourist_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.EmergencyContact)
    if tourist_id:
        query = query.filter(models.EmergencyContact.tourist_id == tourist_id)
    contacts = query.all()
    
    return [
        {
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "relation": c.relation,
            "primary": c.primary
        }
        for c in contacts
    ]

@router.post("/contacts")
def add_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    t_id = payload.tourist_id if payload.tourist_id else 1
    
    existing_count = db.query(models.EmergencyContact).filter(models.EmergencyContact.tourist_id == t_id).count()
    is_primary = True if existing_count == 0 else False

    # 1. Save to the emergency contacts list table
    new_contact = models.EmergencyContact(
        tourist_id=t_id,
        name=payload.name,
        phone=payload.phone,
        relation=payload.relation,
        primary=is_primary
    )
    db.add(new_contact)

    # 2. SYNC: Automatically update the main user profile card table
    tourist = db.query(models.TouristIdentity).filter(models.TouristIdentity.id == t_id).first()
    if tourist:
        tourist.emergency_contact_name = payload.name
        tourist.emergency_contact_phone = payload.phone

    db.commit()
    db.refresh(new_contact)
    
    return {"ok": True, "id": new_contact.id}

@router.delete("/contacts/{contact_id}")
def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.EmergencyContact).filter(models.EmergencyContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"ok": True}

@router.post("/sos")
def send_sos(alert: SOSAlert, db: Session = Depends(get_db)):
    lat_lng_str = f"{alert.lat}, {alert.lng}" if alert.lat and alert.lng else "19.0760, 72.8777"
    t_id = alert.tourist_id if alert.tourist_id else 1

    new_incident = models.Incident(
        tourist_id=t_id,
        incident_type="SOS Emergency",
        description=alert.note if alert.note else "Emergency SOS triggered from Emergency page.",
        location_lat_lng=lat_lng_str,
        ai_severity="HIGH",
        status="OPEN"
    )
    
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return {"ok": True, "incident_id": new_incident.id}

@router.post("/location")
def share_location(payload: dict):
    return {"ok": True}