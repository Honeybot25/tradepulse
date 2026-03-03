"""
SQLAlchemy models for TradePulse.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


class StrategyStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"


class HealthStatus(str, enum.Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class Strategy(Base):
    """Trading strategy configuration and state."""
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, default="custom")  # momentum, mean_reversion, etc.
    status = Column(String, default=StrategyStatus.ACTIVE)
    health_status = Column(String, default=HealthStatus.GREEN)
    
    # Webhook integration
    webhook_token = Column(String, unique=True, index=True)
    
    # Health metrics (cached for quick dashboard access)
    win_rate = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    consecutive_losses = Column(Integer, default=0)
    
    # Thresholds
    max_drawdown_threshold = Column(Float, default=10.0)  # Alert at 10% drawdown
    max_consecutive_losses_threshold = Column(Integer, default=5)  # Alert at 5 losses
    
    # Alert configuration
    discord_webhook_url = Column(String, nullable=True)
    alert_enabled = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_signal_at = Column(DateTime, nullable=True)
    
    # Relationships
    signals = relationship("Signal", back_populates="strategy", cascade="all, delete-orphan")
    health_snapshots = relationship("HealthSnapshot", back_populates="strategy", cascade="all, delete-orphan")


class Signal(Base):
    """Individual trading signal from TradingView."""
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    
    symbol = Column(String, index=True, nullable=False)
    action = Column(String, nullable=False)  # buy or sell
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Optional: filled status for paper trading
    filled = Column(Boolean, default=False)
    exit_price = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    
    strategy = relationship("Strategy", back_populates="signals")


class HealthSnapshot(Base):
    """Time-series health data for charting and alerts."""
    __tablename__ = "health_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    
    health_status = Column(String, nullable=False)
    win_rate = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    consecutive_losses = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    strategy = relationship("Strategy", back_populates="health_snapshots")
