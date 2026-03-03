"""
Notification services for alerts.
"""
import requests
from datetime import datetime
from app.models import Strategy


async def send_discord_alert(strategy: Strategy, status: str, consecutive_losses: int):
    """Send alert to Discord webhook when strategy health degrades."""
    
    if not strategy.discord_webhook_url:
        return
    
    # Color based on status
    colors = {
        "yellow": 16776960,  # Yellow
        "red": 16711680      # Red
    }
    
    emoji = "⚠️" if status == "yellow" else "🚨"
    title = f"{emoji} Strategy Alert: {strategy.name}"
    
    description = f"Your strategy **{strategy.name}** has degraded to **{status.upper()}** status."
    
    if status == "yellow":
        description += f"\n\n⚠️ Warning: {consecutive_losses} consecutive losses detected."
    elif status == "red":
        description += f"\n\n🚨 Critical: {consecutive_losses} consecutive losses - strategy may be burned out."
    
    embed = {
        "title": title,
        "description": description,
        "color": colors.get(status, 16711680),
        "fields": [
            {
                "name": "Win Rate",
                "value": f"{strategy.win_rate:.1f}%",
                "inline": True
            },
            {
                "name": "Max Drawdown",
                "value": f"{strategy.max_drawdown:.1f}%",
                "inline": True
            },
            {
                "name": "Consecutive Losses",
                "value": str(consecutive_losses),
                "inline": True
            }
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    payload = {
        "embeds": [embed]
    }
    
    try:
        response = requests.post(
            strategy.discord_webhook_url,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")
