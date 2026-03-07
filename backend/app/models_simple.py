"""
Simplified models for TradePulse - works with or without database.
Uses Pydantic for validation, optional SQLAlchemy for persistence.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class Strategy(BaseModel):
    """Trading strategy configuration."""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Trade(BaseModel):
    """Individual trade record."""
    id: Optional[int] = None
    strategy_id: int
    symbol: str = Field(..., min_length=1, max_length=50)
    side: str = Field(..., pattern="^(BUY|SELL)$")
    entry_price: float = Field(..., gt=0)
    exit_price: Optional[float] = None
    quantity: float = Field(..., gt=0)
    pnl: Optional[float] = None
    status: str = Field(default="OPEN", pattern="^(OPEN|CLOSED)$")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HealthStatus(BaseModel):
    """API health check response."""
    status: str = "healthy"
    database: str = "connected"  # or "disconnected"
    version: str = "0.1.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
