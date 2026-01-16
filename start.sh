#!/bin/bash
echo "========================================"
echo "J-INVESTMENTS Fleet Management System"
echo
echo "========================================"
echo ""
echo "[1/3] Checking dependencies..."
pip install -r requirements.txt --quiet
echo "[2/3] Initializing database..."
echo "[3/3] Starting application..."
echo ""
echo "========================================"
echo "Application will open at:"
echo "http://localhost:8050"
echo ""
echo "Default Login:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""
python3 app.py
