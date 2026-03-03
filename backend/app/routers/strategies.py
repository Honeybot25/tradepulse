"""
Strategy management endpoints.
"""
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import Strategy, StrategyStatus, HealthStatus

router = APIRouter(prefix="/api/v1/strategies", tags=["strategies"])


class StrategyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = "custom"
    max_drawdown_threshold: float = Field(default=10.0, ge=0, le=100)
    max_consecutive_losses_threshold: int = Field(default=5, ge=1, le=20)
    discord_webhook_url: str = None


class StrategyResponse(BaseModel):
    id: int
    name: str
    type: str
    status: str
    health_status: str
    webhook_token: str
    win_rate: float
    max_drawdown: float
    consecutive_losses: int
    created_at: datetime
    updated_at: datetime
    last_signal_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


@router.post("", response_model=StrategyResponse)
def create_strategy(
    data: StrategyCreate,
    db: Session = Depends(get_db)
):
    """Create a new trading strategy with webhook endpoint."""
    
    # Generate unique webhook token
    webhook_token = secrets.token_urlsafe(32)
    
    strategy = Strategy(
        name=data.name,
        type=data.type,
        webhook_token=webhook_token,
        max_drawdown_threshold=data.max_drawdown_threshold,
        max_consecutive_losses_threshold=data.max_consecutive_losses_threshold,
        discord_webhook_url=data.discord_webhook_url,
        status=StrategyStatus.ACTIVE,
        health_status=HealthStatus.GREEN,
    )
    
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    
    return strategy


@router.get("", response_model=List[StrategyResponse])
def list_strategies(
    status: str = None,
    db: Session = Depends(get_db)
):
    """List all strategies with optional filtering."""
    query = db.query(Strategy)
    
    if status:
        query = query.filter(Strategy.status == status)
    
    return query.order_by(Strategy.updated_at.desc()).all()


@router.get("/{strategy_id}", response_model=StrategyResponse)
def get_strategy(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific strategy by ID."""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    return strategy


@router.patch("/{strategy_id}")
def update_strategy(
    strategy_id: int,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Update strategy status (pause/resume)."""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    if status:
        strategy.status = status
        strategy.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(strategy)
    
    return {"status": "updated", "strategy": strategy.name}


@router.delete("/{strategy_id}")
def delete_strategy(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Delete a strategy and all its data."""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    name = strategy.name
    db.delete(strategy)
    db.commit()
    
    return {"status": "deleted", "strategy": name}
