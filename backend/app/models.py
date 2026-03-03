from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Strategy(Base):
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # momentum, mean_reversion, range_breakout, custom
    status = Column(String, default="active")  # active, paused, error
    health_score = Column(Float, default=100.0)  # 0-100
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Health thresholds
    max_drawdown_pct = Column(Float, default=5.0)
    min_win_rate = Column(Float, default=0.5)
    max_consecutive_losses = Column(Integer, default=3)
    
    # Alert config
    alert_webhook_url = Column(String)
    
    # Relationships
    signals = relationship("Signal", back_populates="strategy", cascade="all, delete-orphan")
    health_snapshots = relationship("HealthSnapshot", back_populates="strategy", cascade="all, delete-orphan")

class Signal(Base):
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    symbol = Column(String, index=True)
    action = Column(String)  # buy, sell
    timestamp = Column(DateTime, default=datetime.utcnow)
    price = Column(Float)
    volume = Column(Float)
    metadata = Column(JSON)  # Store extra TradingView payload fields
    
    # Filled by user or broker API later
    filled = Column(Boolean, default=False)
    filled_price = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    
    strategy = relationship("Strategy", back_populates="signals")

class HealthSnapshot(Base):
    __tablename__ = "health_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Metrics
    total_signals = Column(Integer, default=0)
    win_count = Column(Integer, default=0)
    loss_count = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    avg_pnl = Column(Float, default=0.0)
    current_drawdown_pct = Column(Float, default=0.0)
    consecutive_losses = Column(Integer, default=0)
    
    # Calculated health
    health_score = Column(Float, default=100.0)
    health_status = Column(String, default="green")  # green, yellow, red
    
    strategy = relationship("Strategy", back_populates="health_snapshots")

# Database setup
def get_engine(db_url="sqlite:///./tradepulse.db"):
    return create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})

def init_db(engine):
    Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def get_db(engine):
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()
