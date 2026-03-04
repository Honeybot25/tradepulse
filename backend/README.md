# TradePulse Backend

## Quick Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/honeyrose/tradepulse)

Or manually:
1. Go to https://dashboard.render.com
2. Click "New Web Service"
3. Connect this repo
4. Use settings below

## Render Settings

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment:** Python 3.11

## Environment Variables

None required for MVP (SQLite database).

## API Endpoints

- `GET /api/v1/health` - Health check
- `GET /api/v1/strategies` - List strategies
- `POST /api/v1/webhooks/tradingview?token={TOKEN}` - Signal ingestion
