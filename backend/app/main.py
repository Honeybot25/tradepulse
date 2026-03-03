from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import webhooks, strategies, alerts, health

app = FastAPI(title="TradePulse", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(strategies.router, prefix="/api/v1/strategies", tags=["strategies"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])

@app.get("/")
def root():
    return {"message": "TradePulse API", "version": "0.1.0"}
