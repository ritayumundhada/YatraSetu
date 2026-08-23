"""
models.py
─────────
SQLAlchemy models = Python classes that map 1:1 to PostgreSQL tables.

STAGE 1 SCOPE: only the catalog tables (Experience, Festival, Circle,
Review). Identity, SOS, incident reports, geofencing, etc. are NOT
defined here yet — they'll be added in later stages as their own
routes/models, without needing to touch these tables.

Beginner note on JSONB columns: several fields on the original frontend
(gallery images, itinerary steps, tags, etc.) are simple lists of
strings. Rather than creating a separate table + foreign key for each
one (e.g. a "tags" table), we store them as a single JSONB column.
This matches the "avoid unnecessary complexity" instruction — these
lists are always read/written as a whole, never queried row-by-row.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from database import Base


class Experience(Base):
    """
    A bookable home-hosted experience (e.g. "Tea-slope mornings above
    Munnar"). Host details are stored directly on this table (not a
    separate `hosts` table) because in the current data every host is
    tied to exactly one experience — a join would add complexity with
    no benefit today. This can be split out later if a host ever hosts
    multiple experiences.
    """
    __tablename__ = "experiences"

    # Using the original string ids (e.g. "exp1") as the primary key,
    # so the existing frontend's openExp(id) calls keep working unchanged.
    id = Column(String, primary_key=True)

    title = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)  # e.g. "Chinnakanal, Idukki, Kerala"
    interests = Column(JSONB, nullable=False, default=list)  # e.g. ["community", "food"]
    price_label = Column(String, nullable=False)  # e.g. "₹1,900 / person" — display string as-is
    rating = Column(Float, nullable=False, default=0)
    review_count = Column(Integer, nullable=False, default=0)

    image = Column(String, nullable=False)          # primary image filename/key
    gallery = Column(JSONB, nullable=False, default=list)  # list of image filenames/keys

    date_label = Column(String)      # e.g. "September – March · 6:00 AM"
    people_label = Column(String)    # e.g. "2–6 guests"
    duration_label = Column(String)  # e.g. "Half day"

    tags = Column(JSONB, nullable=False, default=list)
    description = Column(Text, nullable=False)
    plan = Column(JSONB, nullable=False, default=list)      # itinerary steps, ordered list of strings
    included = Column(JSONB, nullable=False, default=list)  # what's included, list of strings
    bring = Column(JSONB, nullable=False, default=list)     # what to bring, list of strings

    # Host details (embedded — see class docstring)
    host_name = Column(String, nullable=False)
    host_since = Column(String)   # e.g. "2022" — kept as a display string, not a real year type
    host_langs = Column(String)   # e.g. "Malayalam, Tamil, English"
    host_bio = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship("Review", back_populates="experience", cascade="all, delete-orphan")


class Review(Base):
    """A guest review left on a specific experience."""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    experience_id = Column(String, ForeignKey("experiences.id"), nullable=False, index=True)

    reviewer_name = Column(String, nullable=False)
    reviewer_city = Column(String)
    stars = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    experience = relationship("Experience", back_populates="reviews")


class Festival(Base):
    """
    A festival/cultural window (e.g. "Hornbill Festival"). Some festival
    tiles in the current frontend just open an existing Experience's
    detail modal instead of a festival-specific one — that's what
    `linked_experience_id` represents.
    """
    __tablename__ = "festivals"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String, nullable=False)
    date_label = Column(String, nullable=False)   # e.g. "1 – 10 December"
    region = Column(String)                        # e.g. "Kisama, Kohima, Nagaland"
    seats = Column(Integer, nullable=False, default=0)
    image = Column(String, nullable=False)
    is_big_tile = Column(Boolean, nullable=False, default=False)

    who = Column(String)          # e.g. "Hosted by an Angami family in Kohima"
    description = Column(Text)
    about = Column(JSONB, nullable=False, default=list)  # list of bullet strings

    # If set, clicking this festival tile opens this Experience's detail
    # modal instead of a standalone festival modal (matches current frontend).
    linked_experience_id = Column(String, ForeignKey("experiences.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Circle(Base):
    """A community interest group (e.g. "Festival Seekers")."""
    __tablename__ = "circles"

    id = Column(Integer, primary_key=True, autoincrement=True)

    display_code = Column(String)  # original "01".."04" label shown in the UI icon
    name = Column(String, nullable=False)
    member_count = Column(Integer, nullable=False, default=0)
    host_name = Column(String)
    description = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
