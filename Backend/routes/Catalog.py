"""
routes/catalog.py
──────────────────
Read-only endpoints that serve the experience/festival/circle catalog.
These replace the hardcoded `experiences`, `festivals`, and `circles`
JS arrays in the frontend — the frontend will fetch this data instead
of reading it from a local const.

STAGE 1 SCOPE: GET endpoints only. Nothing here writes to the database.
"""

from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api", tags=["catalog"])


@router.get("/experiences", response_model=List[schemas.ExperienceListOut])
def list_experiences(
    city: Optional[str] = Query(None, description="Filter by city, case-insensitive partial match"),
    interest: Optional[str] = Query(None, description="Filter by a single interest, e.g. 'food'"),
    db: Session = Depends(get_db),
):
    """
    List experiences for the homepage cards and the Trip Finder.
    Both filters are optional and can be combined.
    """
    query = db.query(models.Experience)

    if city:
        # Match against either the city field or the fuller location string,
        # same behaviour as the frontend's current client-side filter.
        like = f"%{city}%"
        query = query.filter(
            or_(models.Experience.city.ilike(like), models.Experience.location.ilike(like))
        )

    if interest:
        # interests is a JSONB list column — the `?` "contains" style filter
        # is fine to add later, but for Stage 1 (MVP) we fetch and filter in
        # Python to keep the DB query simple and portable while data volume
        # is tiny (a handful of rows).
        experiences = query.all()
        experiences = [e for e in experiences if interest.lower() in [i.lower() for i in e.interests]]
        return experiences

    return query.all()


@router.get("/experiences/{experience_id}", response_model=schemas.ExperienceDetailOut)
def get_experience(experience_id: str, db: Session = Depends(get_db)):
    """Full detail for the experience modal, including its reviews."""
    experience = (
        db.query(models.Experience)
        .options(joinedload(models.Experience.reviews))
        .filter(models.Experience.id == experience_id)
        .first()
    )
    if not experience:
        raise HTTPException(status_code=404, detail=f"No experience found with id '{experience_id}'")
    return experience


@router.get("/festivals", response_model=List[schemas.FestivalOut])
def list_festivals(db: Session = Depends(get_db)):
    """List festival/cultural-window tiles for the festival grid."""
    return db.query(models.Festival).all()


@router.get("/circles", response_model=List[schemas.CircleOut])
def list_circles(db: Session = Depends(get_db)):
    """List community circles."""
    return db.query(models.Circle).all()
