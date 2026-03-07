from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import List
import enum

Base = declarative_base()

# Strategy status enum
class StrategyStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"

# Health status enum  
class HealthStatus(str, enum.Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"

class Strategy(Base):
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    type = Column(String(50), default="custom")
    status = Column(String(20), default=StrategyStatus.ACTIVE.value)
    health_status = Column(String(20), default=HealthStatus.GREEN.value)
    webhook_token = Column(String(255), unique=True, nullable=True)
    max_drawdown_threshold = Column(Float, default=10.0)
    max_consecutive_losses_threshold = Column(Integer, default=5)
    discord_webhook_url = Column(String(500), nullable=True)
    win_rate = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    consecutive_losses = Column(Integer, default=0)
    alert_enabled = Column(String(10), default="true")
    last_signal_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trades: List["Trade"] = relationship("Trade", back_populates="strategy")
    signals: List["Signal"] = relationship("Signal", back_populates="strategy")
    health_snapshots: List["HealthSnapshot"] = relationship("HealthSnapshot", back_populates="strategy")

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    symbol = Column(String(50), nullable=False)
    side = Column(String(10), nullable=False)  # BUY or SELL
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    quantity = Column(Float, nullable=False)
    pnl = Column(Float, nullable=True)
    status = Column(String(20), nullable=False)  # OPEN or CLOSED
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    strategy: "Strategy" = relationship("Strategy", back_populates="trades")


class Signal(Base):
    """Trading signals from webhooks."""
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    symbol = Column(String(50), nullable=False)
    action = Column(String(10), nullable=False)  # buy or sell
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    strategy: "Strategy" = relationship("Strategy", back_populates="signals")


class HealthSnapshot(Base):
    """Health metric snapshots over time."""
    __tablename__ = "health_snapshots"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    health_status = Column(String(20), nullable=False)
    win_rate = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    consecutive_losses = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    strategy: "Strategy" = relationship("Strategy", back_populates="health_snapshots")
