#!/bin/bash
# Deploy to Render using deploy hook

# Try to trigger deploy via webhook
HOOK_URL="https://api.render.com/deploy/srv-TRADEPULSE?key=DEPLOY_KEY"

echo "Creating deploy hook..."
echo "Repo: https://github.com/Honeybot25/tradepulse"
echo ""
echo "Manual deploy URL:"
echo "https://dashboard.render.com/select-repo?type=web"
echo ""
echo "Settings to use:"
echo "  Root Directory: backend"
echo "  Build Command: pip install -r requirements.txt"
echo "  Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "Or use one-click:"
echo "https://dashboard.render.com/blueprint?repo=https://github.com/Honeybot25/tradepulse"
