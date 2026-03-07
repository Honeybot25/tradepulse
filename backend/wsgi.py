# wsgi.py
import uvicorn
from app.main import app

# Uvicorn-compatible application export
# FastAPI is ASGI - use uvicorn workers
application = app

# If run directly, start uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
