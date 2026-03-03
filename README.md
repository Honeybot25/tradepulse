# TradePulse

Real-time strategy health monitoring for retail traders. Aggregates signals from TradingView webhooks into a unified health dashboard.

## Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Next.js + Tailwind
- **Webhooks**: TradingView webhook ingestion
- **Alerts**: Discord/Slack webhooks

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## MVP Scope (2-3 days)

1. TradingView webhook ingestion → FastAPI endpoint
2. Strategy health cards → SQLite/Postgres store, REST API
3. Dashboard UI → Next.js page
4. Discord alerts → Webhook on yellow/red status
