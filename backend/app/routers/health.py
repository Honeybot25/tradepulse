"""
Health check endpoint.
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get("")
def health_check():
    """Check API health status."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
