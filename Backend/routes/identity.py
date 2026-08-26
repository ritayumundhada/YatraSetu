"""
routes/identity.py
───────────────────
Stage 2, Step 1 — Tourist Identity.

This is the backend-generated replacement for the frontend's static
Digital ID card ("Arjun Sharma" / "FV-2026-07421"). There is no login
here — an identity is created on demand and its id is then held by the
frontend (e.g. in the existing `S` state object) for the rest of the
session. See models.TouristIdentity for the reasoning.

STAGE 2 STEP 1 SCOPE: create identity, fetch identity, update emergency
contact. No join requests, SOS, incidents, geofencing, or auth here.
"""

import random
import string

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api", tags=["identity"])


def _generate_digital_id_code(db: Session) -> str:
    """
    Builds a display-friendly id code like "YS-2026-84213" and makes
    sure it isn't already in use. Collisions are extremely unlikely
    with 5 random digits, but we check anyway rather than assume.
    """
    for _ in range(10):  # a handful of attempts is more than enough
        candidate = "YS-2026-" + "".join(random.choices(string.digits, k=5))
        already_used = (
            db.query(models.TouristIdentity)
            .filter(models.TouristIdentity.digital_id_code == candidate)
            .first()
        )
        if not already_used:
            return candidate

    # Extremely unlikely fallback if every attempt collided.
    raise HTTPException(status_code=500, detail="Could not generate a unique digital ID. Please try again.")


@router.post("/identity", response_model=schemas.IdentityOut)
def create_identity(payload: schemas.IdentityCreate, db: Session = Depends(get_db)):
    """
    Creates a new tourist identity. Called by the frontend the first
    time one is needed (e.g. Finder submit or first Join click) — not
    behind any login screen.
    """
    digital_id_code = _generate_digital_id_code(db)

    identity = models.TouristIdentity(
        display_name=payload.display_name,
        digital_id_code=digital_id_code,
        interests=payload.interests,
    )
    db.add(identity)
    db.commit()
    db.refresh(identity)  # loads server-generated fields like id and created_at
    return identity


@router.get("/identity/{identity_id}", response_model=schemas.IdentityOut)
def get_identity(identity_id: int, db: Session = Depends(get_db)):
    """Fetches a single identity by id, e.g. to redraw the Digital ID card."""
    identity = db.query(models.TouristIdentity).filter(models.TouristIdentity.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=404, detail=f"No tourist identity found with id {identity_id}")
    return identity


@router.patch("/identity/{identity_id}/emergency-contact", response_model=schemas.IdentityOut)
def update_emergency_contact(
    identity_id: int,
    payload: schemas.EmergencyContactUpdate,
    db: Session = Depends(get_db),
):
    """Saves/updates the emergency contact for an existing identity."""
    identity = db.query(models.TouristIdentity).filter(models.TouristIdentity.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=404, detail=f"No tourist identity found with id {identity_id}")

    identity.emergency_contact_name = payload.name
    identity.emergency_contact_phone = payload.phone

    db.commit()
    db.refresh(identity)
    return identity


from fastapi import HTTPException

# This route checks if a Digital ID exists in the database
# This route checks if a Digital ID exists in the database
@router.get("/identity/login/{digital_id}")
def login_with_id(digital_id: str, db: Session = Depends(get_db)):
    print(f"\n--- LOGIN ATTEMPT RECEIVED ---")
    print(f"Looking for ID: '{digital_id}'")
    
    # We use .contains() instead of == to ignore accidental database spaces
    user = db.query(models.TouristIdentity).filter(models.TouristIdentity.digital_id_code.contains(digital_id)).first()
    
    if not user:
        print("FAILED: Route worked, but User not found in database.")
        raise HTTPException(status_code=404, detail="Digital ID not found. Please register first.")
    
    print(f"SUCCESS: Found user {user.display_name}")
    return {
        "message": "Login successful",
        "digital_id_code": user.digital_id_code,
        "display_name": user.display_name,
        "tourist_id": user.id
    }