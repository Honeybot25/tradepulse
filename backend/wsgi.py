# wsgi.py
from app.main import app

# Gunicorn will look for 'application' variable
# FastAPI is ASGI, but we can expose it for gunicorn
application = app
