from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import requests
from app.models import Strategy, get_engine, get_db

router = APIRouter()
engine = get_engine()

class AlertConfig(BaseModel):
    strategy_id: int
    webhook_url: str
    alert_on_status: List[str] = ["yellow", "red"]  # Trigger on these statuses

class DiscordWebhookPayload(BaseModel):
    content: str
    embeds: Optional[List[dict]] = None

def send_discord_alert(webhook_url: str, strategy_name: str, health_status: str, health_score: float, metrics: dict):
    """Send alert to Discord webhook"""
    color = 0x00ff00 if health_status == "green" else 0xffaa00 if health_status == "yellow" else 0xff0000
    
    embed = {
        "title": f"⚠️ Strategy Alert: {strategy_name}",
        "color": color,
        "fields": [
            {"name": "Status", "value": health_status.upper(), "inline": True},
            {"name": "Health Score", "value": f"{health_score:.1f}", "inline": True},
            {"name": "Win Rate", "value": f"{metrics.get('win_rate', 0):.1%}", "inline": True},
            {"name": "Drawdown", "value": f"{metrics.get('current_drawdown_pct', 0):.2f}%", "inline": True},
            {"name": "Consecutive Losses", "value": str(metrics.get('consecutive_losses', 0)), "inline": True},
        ],
        "timestamp": datetime.utcnow().isoformat()
    }
    
    payload = {
        "content": f"Strategy **{strategy_name}** health status changed to **{health_status.upper()}**",
        "embeds": [embed]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")
        return False

@router.post("/test")
def test_alert(config: AlertConfig):
    """Test alert webhook"""
    strategy = {"name": "Test Strategy", "id": config.strategy_id}
    
    for status in config.alert_on_status:
        success = send_discord_alert(
            webhook_url=config.webhook_url,
            strategy_name=strategy["name"],
            health_status=status,
            health_score=65.0 if status == "yellow" else 35.0,
            metrics={
                "win_rate": 0.45,
                "current_drawdown_pct": 3.5,
                "consecutive_losses": 2
            }
        )
    
    return {"status": "test alerts sent", "webhook_configured": success}
