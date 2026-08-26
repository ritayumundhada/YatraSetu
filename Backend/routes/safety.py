from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

# This creates the /api/incident endpoint
router = APIRouter(prefix="/api/incident", tags=["safety"])

@router.post("/", response_model=schemas.IncidentOut)
def report_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    # 1. Check if the tourist ID actually exists in the database
    tourist = db.query(models.TouristIdentity).filter(models.TouristIdentity.id == incident.tourist_id).first()
    if not tourist:
        raise HTTPException(status_code=404, detail="Tourist ID not found")
    
    # 2. Package the incoming SOS data into our database model
    new_incident = models.Incident(
        tourist_id=incident.tourist_id,
        incident_type=incident.incident_type,
        description=incident.description,
        location_lat_lng=incident.location_lat_lng
    )
    
    # 3. Save it securely to PostgreSQL
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    
    return new_incident