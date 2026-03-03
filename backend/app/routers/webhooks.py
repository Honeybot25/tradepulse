"""
TradingView webhook ingestion endpoint.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.models import Strategy, Signal, HealthSnapshot
from app.services.notifications import send_discord_alert

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])


class TradingViewWebhook(BaseModel):
    """TradingView webhook payload format."""
    strategy: str
    symbol: str
    action: str  # "buy" or "sell"
    price: float
    time: Optional[str] = None


@router.post("/tradingview")
async def tradingview_webhook(
    payload: TradingViewWebhook,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Ingest signals from TradingView alerts.
    
    TradingView Alert Message Format:
    {
        "strategy": "{{strategy_title}}",
        "symbol": "{{ticker}}",
        "action": "buy",
        "price": "{{close}}",
        "time": "{{time}}"
    }
    """
    # Validate strategy by webhook token
    strategy = db.query(Strategy).filter(
        Strategy.webhook_token == token
    ).first()
    
    if not strategy:
        raise HTTPException(status_code=401, detail="Invalid webhook token")
    
    if strategy.status != "active":
        raise HTTPException(status_code=400, detail="Strategy is not active")
    
    # Create signal record
    signal = Signal(
        strategy_id=strategy.id,
        symbol=payload.symbol,
        action=payload.action.lower(),
        price=float(payload.price),
        timestamp=datetime.utcnow()
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    
    # Recalculate health metrics
    await recalculate_health(db, strategy)
    
    return {
        "status": "success",
        "signal_id": signal.id,
        "strategy": strategy.name
    }


async def recalculate_health(db: Session, strategy: Strategy):
    """Recalculate strategy health metrics after each signal."""
    
    # Get recent signals (last 100 for rolling window)
    signals = db.query(Signal).filter(
        Signal.strategy_id == strategy.id
    ).order_by(Signal.timestamp.desc()).limit(100).all()
    
    if len(signals) < 2:
        return
    
    # Calculate win rate and P&L (simplified - assumes 50% win for now)
    total_signals = len(signals)
    
    # Calculate consecutive losses (key burnout indicator)
    consecutive_losses = 0
    max_consecutive_losses = 0
    
    for s in signals:
        # For paper trading: alternate wins/losses for MVP
        # In production: compare entry/exit prices
        is_win = s.id % 2 == 0  # Simplified for MVP
        
        if not is_win:
            consecutive_losses += 1
            max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
        else:
            consecutive_losses = 0
    
    # Calculate drawdown (simplified)
    max_drawdown = min(max_consecutive_losses * 2.0, 50.0)  # 2% per loss, max 50%
    
    # Determine health status
    # Green: < 3 consecutive losses, < 10% drawdown
    # Yellow: 3-5 consecutive losses, 10-20% drawdown
    # Red: > 5 consecutive losses, > 20% drawdown
    
    if max_consecutive_losses >= 5 or max_drawdown > 20:
        new_status = "red"
    elif max_consecutive_losses >= 3 or max_drawdown > 10:
        new_status = "yellow"
    else:
        new_status = "green"
    
    # Update strategy
    old_status = strategy.health_status
    strategy.health_status = new_status
    strategy.win_rate = 50.0  # Simplified for MVP
    strategy.max_drawdown = max_drawdown
    strategy.consecutive_losses = max_consecutive_losses
    strategy.last_signal_at = datetime.utcnow()
    strategy.updated_at = datetime.utcnow()
    
    # Create health snapshot
    snapshot = HealthSnapshot(
        strategy_id=strategy.id,
        health_status=new_status,
        win_rate=strategy.win_rate,
        max_drawdown=max_drawdown,
        consecutive_losses=max_consecutive_losses
    )
    db.add(snapshot)
    db.commit()
    
    # Send alert if status degraded
    if new_status in ["yellow", "red"] and old_status == "green" and strategy.alert_enabled:
        await send_discord_alert(strategy, new_status, max_consecutive_losses)
