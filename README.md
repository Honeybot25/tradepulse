# TradePulse

Real-time strategy health monitoring for retail traders. Aggregates signals from TradingView webhooks into a unified health dashboard.

## Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite (Postgres for prod)
- **Frontend**: Next.js 14 + Tailwind CSS + Recharts
- **Webhooks**: TradingView webhook ingestion
- **Alerts**: Discord/Slack webhooks

## Quick Start

### Backend (Port 8000)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Port 3000)
```bash
cd frontend
npm install
npm run dev
```

### Test Commands
```bash
# Check API health
curl http://localhost:8000/

# Create a strategy
curl -X POST http://localhost:8000/api/v1/strategies/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Momentum Long", "type": "momentum"}'

# Simulate TradingView webhook
curl -X POST http://localhost:8000/api/v1/webhooks/tradingview \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "Momentum Long",
    "symbol": "AAPL",
    "action": "buy",
    "price": 185.50,
    "volume": 100
  }'
```

## MVP Scope (2-3 days)

1. ✅ **TradingView webhook ingestion** → FastAPI endpoint
2. ✅ **Strategy health cards** → SQLite store, REST API
3. ✅ **Dashboard UI** → Next.js page with real-time updates
4. **Discord alerts** → Webhook on yellow/red status (configured, needs integration)

## Next Steps

- [ ] TradingView webhook signature verification
- [ ] Health history charts on strategy detail page
- [ ] Automatic alert triggers
- [ ] Strategy creation form
- [ ] P&L tracking (manual fill or broker API)
