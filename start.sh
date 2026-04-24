#!/bin/bash

echo ""
echo "================================================"
echo "  HeadphoneAI - RAG + MCP + LLM Demo"
echo "================================================"
echo ""

# ── Check Python ──────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 is not installed."
    echo ""
    echo "  Mac:   brew install python  (or download from python.org)"
    echo "  Linux: sudo apt install python3 python3-pip"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

PYTHON=$(command -v python3)
echo "[1/3] Python found: $($PYTHON --version)"
echo ""

# ── Install dependencies ──────────────────────────
echo "[2/3] Installing dependencies (first run may take ~1 min)..."
$PYTHON -m pip install -r requirements.txt --quiet --disable-pip-version-check

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to install dependencies."
    echo "Try running manually: pip3 install -r requirements.txt"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "      Dependencies ready."
echo ""

# ── Open browser after delay ──────────────────────
echo "[3/3] Starting server..."
echo ""
echo "------------------------------------------------"
echo "  App will open at: http://localhost:8000"
echo "  Press Ctrl+C to stop."
echo "------------------------------------------------"
echo ""

# Open browser after 3s in background
(sleep 3 && open "http://localhost:8000" 2>/dev/null || xdg-open "http://localhost:8000" 2>/dev/null) &

# ── Start server ──────────────────────────────────
$PYTHON -m uvicorn main:app --host 0.0.0.0 --port 8000
