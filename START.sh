#!/bin/bash

# AI Smart Attendance System - Unix Startup Script
# This script activates the virtual environment and starts the Flask application

echo ""
echo "============================================================"
echo " AI Smart Attendance System - Startup Script"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo ""
    echo "Please run setup first:"
    echo "  1. python3 -m venv .venv"
    echo "  2. source .venv/bin/activate"
    echo "  3. pip install -r requirements.txt"
    echo ""
    exit 1
fi

# Check if Flask is installed
if [ ! -d ".venv/lib/python*/site-packages/flask" ]; then
    echo "Installing dependencies..."
    source .venv/bin/activate
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Run the application
echo ""
echo "============================================================"
echo " Starting Flask Application..."
echo "============================================================"
echo ""
echo "🚀 AI Smart Attendance System is starting..."
echo ""
echo "✅ Access the application at: http://127.0.0.1:5000"
echo "📧 Login: Admin / admin123"
echo ""
echo "⏹️  Press Ctrl+C to stop the server"
echo ""
echo "============================================================"
echo ""

# Start the Flask app
python3 app.py

exit 0
