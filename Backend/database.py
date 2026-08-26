"""
database.py
────────────
Sets up the connection to PostgreSQL using SQLAlchemy.

Beginner note: SQLAlchemy talks to Postgres through an "Engine". A
"Session" is a temporary workspace you use to read/write rows during
one request, and "Base" is the parent class every table model (in
models.py) inherits from so SQLAlchemy knows about it.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load variables from a local .env file (if present) into the environment.
# In production you'd set these as real environment variables instead.
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy .env.example to .env and fill in "
        "your PostgreSQL connection details."
    )

# The engine manages the actual connections to PostgreSQL.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory that creates new DB sessions when called.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the class every SQLAlchemy model in models.py will inherit from.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session to a route,
    and guarantees it gets closed afterwards (even if an error happens).

    Usage in a route:
        @router.get("/something")
        def handler(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
