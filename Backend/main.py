"""
main.py
───────
Entry point for the YatraSetu backend. Run with:
    uvicorn main:app --reload

STAGE 1 SCOPE: only the catalog router is included. Later stages will
add routes.identity, routes.requests, routes.safety, etc. here, one
`app.include_router(...)` line each — nothing else in this file should
need to change when that happens.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import catalog

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


@app.get("/", tags=["health"])
def health_check():
    """Simple endpoint to confirm the server is running."""
    return {"status": "ok", "service": "YatraSetu API", "stage": 1}
