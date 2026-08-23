"""
schemas.py
──────────
Pydantic schemas define the *shape* of data going in/out of the API.
They're separate from models.py (the DB tables) on purpose: a schema
can hide or reshape fields before they reach the client, and validates
incoming data before it ever touches the database.

STAGE 1 SCOPE: read-only catalog schemas. No "create" schemas are
needed yet because Stage 1 has no write endpoints (join requests, host
applications, etc. come in a later stage).
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# ─────────────── Review ───────────────

class ReviewOut(BaseModel):
    # from_attributes=True lets Pydantic read data straight off a
    # SQLAlchemy model instance (e.g. review.text), not just off a dict.
    model_config = ConfigDict(from_attributes=True)

    id: int
    reviewer_name: str
    reviewer_city: Optional[str] = None
    stars: int
    text: str


# ─────────────── Experience ───────────────

class ExperienceListOut(BaseModel):
    """Lighter shape used for list views (homepage cards, finder results)."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    city: str
    location: str
    interests: List[str]
    price_label: str
    rating: float
    review_count: int
    image: str


class ExperienceDetailOut(BaseModel):
    """Full shape used for the experience detail modal, includes reviews."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    city: str
    location: str
    interests: List[str]
    price_label: str
    rating: float
    review_count: int

    image: str
    gallery: List[str]

    date_label: Optional[str] = None
    people_label: Optional[str] = None
    duration_label: Optional[str] = None

    tags: List[str]
    description: str
    plan: List[str]
    included: List[str]
    bring: List[str]

    host_name: str
    host_since: Optional[str] = None
    host_langs: Optional[str] = None
    host_bio: Optional[str] = None

    reviews: List[ReviewOut] = []


# ─────────────── Festival ───────────────

class FestivalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    date_label: str
    region: Optional[str] = None
    seats: int
    image: str
    is_big_tile: bool
    who: Optional[str] = None
    description: Optional[str] = None
    about: List[str]
    linked_experience_id: Optional[str] = None


# ─────────────── Circle ───────────────

class CircleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_code: Optional[str] = None
    name: str
    member_count: int
    host_name: Optional[str] = None
    description: Optional[str] = None
