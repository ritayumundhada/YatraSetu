"""
main.py
───────
Entry point for the YatraSetu backend. Run with:
    uvicorn main:app --reload

STAGE 2 STEP 1: the identity router is now included alongside catalog.
Later stages will add routes.requests, routes.safety, etc. here, one
`app.include_router(...)` line each — nothing else in this file should
need to change when that happens.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
# `models` must be imported (even though nothing below references it
# directly) BEFORE Base.metadata.create_all() runs. Importing the module
# is what registers every table class — including TouristIdentity — onto
# Base's metadata. Skip this import and create_all() would only know
# about whatever other file happened to import models.py first.
import models  # noqa: F401
from routes import catalog, identity, safety, trips, emergency, safety_host

load_dotenv()

# Creates any tables defined in models.py that don't already exist yet.
# Safe to call every startup — it never touches tables that already exist.
# (seed.py also calls this before inserting data, so this line matters
# most for a fresh database that hasn't been seeded at all.)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YatraSetu API",
    description="Backend for the YatraSetu smart tourist safety & assistance platform (SIH prototype).",
    version="0.1.0",
)

# CORS: lets the frontend (served from a different origin/port, or opened
# as a local file) call this API from the browser without being blocked.
cors_origins = os.getenv("CORS_ORIGINS", "*")
allow_origins = ["*"] if cors_origins.strip() == "*" else [o.strip() for o in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalog.router)
app.include_router(identity.router)
app.include_router(safety.router)
app.include_router(trips.router)
app.include_router(emergency.router)
app.include_router(safety_host.router)

@app.get("/", tags=["health"])
def health_check():
    """Simple endpoint to confirm the server is running."""
    return {"status": "ok", "service": "YatraSetu API", "stage": "2.1"}
