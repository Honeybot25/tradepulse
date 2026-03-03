from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Signal, Strategy, HealthSnapshot, get_engine, get_db, init_db

router = APIRouter()
engine = get_engine()
init_db(engine)

class TradingViewSignal(BaseModel):
    """Expected TradingView webhook payload"""
    strategy: str  # Strategy name/identifier
    symbol: str
    action: str  # buy, sell
    price: float
    volume: Optional[float] = None
    timestamp: Optional[str] = None  # ISO format
    metadata: Optional[Dict[str, Any]] = {}

def update_strategy_health(db: Session, strategy_id: int):
    """Recalculate health metrics after new signal"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        return
    
    signals = db.query(Signal).filter(
        Signal.strategy_id == strategy_id,
        Signal.filled == True
    ).order_by(Signal.timestamp.desc()).all()
    
    total = len(signals)
    wins = sum(1 for s in signals if s.pnl and s.pnl > 0)
    losses = sum(1 for s in signals if s.pnl and s.pnl < 0)
    
    win_rate = wins / total if total > 0 else 0.0
    
    # Calculate consecutive losses
    consecutive_losses = 0
    for s in signals:
        if s.pnl and s.pnl < 0:
            consecutive_losses += 1
        else:
            break
    
    # Calculate drawdown
    peak = 0
    current_drawdown = 0
    running_pnl = 0
    for s in reversed(signals):
        if s.pnl:
            running_pnl += s.pnl
            peak = max(peak, running_pnl)
            current_drawdown = peak - running_pnl if peak > 0 else 0
    
    # Health score calculation
    health_score = 100.0
    health_status = "green"
    
    if win_rate < strategy.min_win_rate:
        health_score -= (strategy.min_win_rate - win_rate) * 100
    if consecutive_losses >= strategy.max_consecutive_losses:
        health_score -= 20
        health_status = "red"
    elif consecutive_losses >= strategy.max_consecutive_losses // 2:
        health_score -= 10
        health_status = "yellow"
    
    health_score = max(0, min(100, health_score))
    if health_score < 50:
        health_status = "red"
    elif health_score < 75:
        health_status = "yellow"
    
    # Update strategy
    strategy.health_score = health_score
    strategy.updated_at = datetime.utcnow()
    
    # Create snapshot
    snapshot = HealthSnapshot(
        strategy_id=strategy_id,
        total_signals=total,
        win_count=wins,
        loss_count=losses,
        win_rate=win_rate,
        current_drawdown_pct=current_drawdown,
        consecutive_losses=consecutive_losses,
        health_score=health_score,
        health_status=health_status
    )
    db.add(snapshot)
    db.commit()
    
    return snapshot

@router.post("/tradingview")
async def receive_tradingview_signal(
    signal: TradingViewSignal,
    background_tasks: BackgroundTasks,
    db: Session = Depends(lambda: next(get_db(engine)))
):
    """Receive signal from TradingView webhook"""
    
    # Find or create strategy
    strategy = db.query(Strategy).filter(Strategy.name == signal.strategy).first()
    if not strategy:
        strategy = Strategy(name=signal.strategy, type="custom")
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
    
    # Create signal record
    new_signal = Signal(
        strategy_id=strategy.id,
        symbol=signal.symbol,
        action=signal.action,
        price=signal.price,
        volume=signal.volume,
        metadata=signal.metadata
    )
    
    if signal.timestamp:
        try:
            new_signal.timestamp = datetime.fromisoformat(signal.timestamp.replace('Z', '+00:00'))
        except:
            pass
    
    db.add(new_signal)
    db.commit()
    
    # Update health in background
    background_tasks.add_task(update_strategy_health, db, strategy.id)
    
    return {
        "status": "received",
        "signal_id": new_signal.id,
        "strategy_id": strategy.id
    }

@router.post("/{strategy_id}/fill")
async def mark_signal_filled(
    strategy_id: int,
    signal_id: int,
    filled_price: float,
    pnl: Optional[float] = None,
    db: Session = Depends(lambda: next(get_db(engine)))
):
    """Mark a signal as filled (manual or broker API callback)"""
    signal = db.query(Signal).filter(
        Signal.id == signal_id,
        Signal.strategy_id == strategy_id
    ).first()
    
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    
    signal.filled = True
    signal.filled_price = filled_price
    signal.pnl = pnl
    
    db.commit()
    
    # Recalculate health
    update_strategy_health(db, strategy_id)
    
    return {"status": "filled", "signal_id": signal_id}
