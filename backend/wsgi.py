# wsgi.py - For Gunicorn with Uvicorn workers
from app.main import app

# ASGI application for Gunicorn + Uvicorn workers
# Usage: gunicorn wsgi:application -k uvicorn.workers.UvicornWorker
application = app
