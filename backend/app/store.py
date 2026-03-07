"""
In-memory data store for TradePulse.
Falls back to this when database is unavailable.
"""
from typing import Dict, List, Optional
from datetime import datetime
from app.models_simple import Strategy, Trade

# In-memory storage
_strategies: Dict[int, Strategy] = {}
_trades: Dict[int, Trade] = {}
_next_strategy_id = 1
_next_trade_id = 1

def get_strategies() -> List[Strategy]:
    """Get all strategies."""
    return list(_strategies.values())

def get_strategy(strategy_id: int) -> Optional[Strategy]:
    """Get strategy by ID."""
    return _strategies.get(strategy_id)

def create_strategy(strategy: Strategy) -> Strategy:
    """Create a new strategy."""
    global _next_strategy_id
    strategy.id = _next_strategy_id
    strategy.created_at = datetime.utcnow()
    strategy.updated_at = datetime.utcnow()
    _strategies[_next_strategy_id] = strategy
    _next_strategy_id += 1
    return strategy

def update_strategy(strategy_id: int, updates: dict) -> Optional[Strategy]:
    """Update an existing strategy."""
    if strategy_id not in _strategies:
        return None
    strategy = _strategies[strategy_id]
    for key, value in updates.items():
        if hasattr(strategy, key):
            setattr(strategy, key, value)
    strategy.updated_at = datetime.utcnow()
    return strategy

def delete_strategy(strategy_id: int) -> bool:
    """Delete a strategy."""
    if strategy_id in _strategies:
        del _strategies[strategy_id]
        return True
    return False

def get_trades(strategy_id: Optional[int] = None) -> List[Trade]:
    """Get all trades, optionally filtered by strategy."""
    trades = list(_trades.values())
    if strategy_id:
        trades = [t for t in trades if t.strategy_id == strategy_id]
    return trades

def get_trade(trade_id: int) -> Optional[Trade]:
    """Get trade by ID."""
    return _trades.get(trade_id)

def create_trade(trade: Trade) -> Trade:
    """Create a new trade."""
    global _next_trade_id
    trade.id = _next_trade_id
    trade.timestamp = datetime.utcnow()
    _trades[_next_trade_id] = trade
    _next_trade_id += 1
    return trade

def update_trade(trade_id: int, updates: dict) -> Optional[Trade]:
    """Update an existing trade."""
    if trade_id not in _trades:
        return None
    trade = _trades[trade_id]
    for key, value in updates.items():
        if hasattr(trade, key):
            setattr(trade, key, value)
    return trade

def delete_trade(trade_id: int) -> bool:
    """Delete a trade."""
    if trade_id in _trades:
        del _trades[trade_id]
        return True
    return False

# Add some sample data
if not _strategies:
    create_strategy(Strategy(
        name="Momentum Strategy",
        description="Buy high, sell higher"
    ))
    create_strategy(Strategy(
        name="Mean Reversion",
        description="Buy dips, sell rips"
    ))
