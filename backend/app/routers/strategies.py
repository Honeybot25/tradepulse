from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models import Strategy, HealthSnapshot, get_engine, get_db

router = APIRouter()
engine = get_engine()

class StrategyCreate(BaseModel):
    name: str
    type: str = "custom"
    max_drawdown_pct: float = 5.0
    min_win_rate: float = 0.5
    max_consecutive_losses: int = 3
    alert_webhook_url: Optional[str] = None

class StrategyResponse(BaseModel):
    id: int
    name: str
    type: str
    status: str
    health_score: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class HealthSnapshotResponse(BaseModel):
    id: int
    timestamp: datetime
    total_signals: int
    win_count: int
    loss_count: int
    win_rate: float
    avg_pnl: float
    current_drawdown_pct: float
    consecutive_losses: int
    health_score: float
    health_status: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[StrategyResponse])
def list_strategies(db: Session = Depends(lambda: next(get_db(engine)))):
    """List all strategies with current health"""
    return db.query(Strategy).order_by(Strategy.updated_at.desc()).all()

@router.post("/", response_model=StrategyResponse)
def create_strategy(strategy: StrategyCreate, db: Session = Depends(lambda: next(get_db(engine)))):
    """Create a new strategy"""
    db_strategy = Strategy(**strategy.model_dump())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@router.get("/{strategy_id}", response_model=StrategyResponse)
def get_strategy(strategy_id: int, db: Session = Depends(lambda: next(get_db(engine)))):
    """Get a specific strategy"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@router.get("/{strategy_id}/health", response_model=List[HealthSnapshotResponse])
def get_strategy_health_history(
    strategy_id: int,
    limit: int = 100,
    db: Session = Depends(lambda: next(get_db(engine)))
):
    """Get health history for a strategy"""
    snapshots = db.query(HealthSnapshot).filter(
        HealthSnapshot.strategy_id == strategy_id
    ).order_by(HealthSnapshot.timestamp.desc()).limit(limit).all()
    return snapshots

@router.get("/{strategy_id}/current-health")
def get_current_health(strategy_id: int, db: Session = Depends(lambda: next(get_db(engine)))):
    """Get most recent health snapshot"""
    snapshot = db.query(HealthSnapshot).filter(
        HealthSnapshot.strategy_id == strategy_id
    ).order_by(HealthSnapshot.timestamp.desc()).first()
    
    if not snapshot:
        raise HTTPException(status_code=404, detail="No health data found")
    
    return {
        "strategy_id": strategy_id,
        "health_score": snapshot.health_score,
        "health_status": snapshot.health_status,
        "win_rate": snapshot.win_rate,
        "current_drawdown_pct": snapshot.current_drawdown_pct,
        "consecutive_losses": snapshot.consecutive_losses,
        "total_signals": snapshot.total_signals,
        "timestamp": snapshot.timestamp
    }
