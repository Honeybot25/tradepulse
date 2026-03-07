# Gunicorn configuration for FastAPI
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Worker processes - use Uvicorn workers for FastAPI
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"

# Logging
errorlog = "-"
accesslog = "-"
loglevel = "info"

# Process naming
proc_name = "tradepulse"

# Server mechanics
daemon = False
pidfile = None
