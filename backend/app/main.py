"""
TradePulse FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables
from app.routers import strategies, webhooks, health

# Create database tables on startup
create_tables()

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
