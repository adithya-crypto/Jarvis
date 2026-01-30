#!/bin/bash
# Quick start script for JARVIS

echo "Starting J.A.R.V.I.S..."
echo ""

cd "$(dirname "$0")"

# Check for --gui flag
if [ "$1" == "--gui" ]; then
    python jarvis_app.py --gui
else
    python jarvis_app.py
fi
