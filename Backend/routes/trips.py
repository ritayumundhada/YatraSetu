from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from database import get_db
import models

router = APIRouter(tags=["trips"])

# Sample bookings that link directly to your seeded hosts and experiences!
SAMPLE_TRIPS = [
    {
        "id": "t1",
        "experience_id": "exp6",
        "title": "Umngot river mornings in Shnongpdeng",
        "city": "Shnongpdeng, Meghalaya",
        "host": "Banri Nongrum",
        "date": "2026-11-08",
        "guests": 2,
        "status": "confirmed",
        "price": 2100
    },
    {
        "id": "t2",
        "experience_id": "exp4",
        "title": "Kerala sadya: 28 dishes, one banana leaf",
        "city": "Thrissur, Kerala",
        "host": "The Nair family",
        "date": "2026-12-01",
        "guests": 4,
        "status": "pending",
        "price": 2800
    },
    {
        "id": "t3",
        "experience_id": "exp5",
        "title": "Chandni Chowk street food crawl",
        "city": "Delhi",
        "host": "Vikram Malhotra",
        "date": "2026-09-19",
        "guests": 2,
        "status": "completed",
        "price": 1200
    }
]

@router.get("/trips")
def get_trips():
    return SAMPLE_TRIPS

@router.delete("/trips/{trip_id}")
def cancel_trip(trip_id: str):
    return {"ok": True, "cancelled_id": trip_id}

@router.get("/destinations")
def list_destinations(q: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """
    Pulls directly from the seeded 'experiences' table in PostgreSQL.
    Dynamically maps all 7 seeded experiences into the browse destinations format.
    """
    query = db.query(models.Experience)
    
    if q:
        search = f"%{q.lower()}%"
        query = query.filter(
            or_(
                models.Experience.title.ilike(search),
                models.Experience.city.ilike(search),
                models.Experience.location.ilike(search),
                models.Experience.description.ilike(search)
            )
        )
    
    experiences = query.all()
    
    destinations = []
    for exp in experiences:
        # Extract state/region from location string (e.g. "Dadar, Mumbai" -> "Mumbai")
        location_parts = [p.strip() for p in exp.location.split(",")]
        state_or_region = location_parts[-1] if location_parts else exp.city
        
        tag_line = exp.tags[0] if (exp.tags and len(exp.tags) > 0) else exp.title
        if len(exp.tags) > 1:
            tag_line += f", {exp.tags[1]}"

        destinations.append({
            "id": exp.id,
            "name": exp.city,
            "state": state_or_region,
            "title": exp.title,
            "experiences": 1,
            "tag": tag_line,
            "price_label": exp.price_label,
            "rating": exp.rating,
            "image": exp.image
        })
        
    return destinations