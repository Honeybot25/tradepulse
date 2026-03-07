"""
TradePulse FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database setup - make completely optional
import os
db_available = False
try:
    from app.database import create_tables
    # Ensure /tmp exists for Render
    if os.environ.get("RENDER"):
        os.makedirs("/tmp", exist_ok=True)
    create_tables()
    db_available = True
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"⚠️  Database initialization skipped: {e}")
    # Continue without database - use in-memory store
    db_available = False

from app.routers import strategies, webhooks, health

app = FastAPI(
    title="TradePulse API",
    description="AI Strategy Health Dashboard for Retail Traders",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://frontend-three-livid-43.vercel.app",
        "https://frontend-mt7n2i25f-honeys-projects-26bedb83.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(strategies.router)
app.include_router(webhooks.router)
app.include_router(health.router)


@app.get("/")
def root():
    return {
        "message": "TradePulse API",
        "version": "0.1.0",
        "docs": "/docs"
    }
