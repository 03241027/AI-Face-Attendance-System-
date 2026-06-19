@echo off
REM AI Smart Attendance System - Windows Startup Script
REM This script activates the virtual environment and starts the Flask application

echo.
echo ============================================================
echo  AI Smart Attendance System - Startup Script
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup first:
    echo   1. python -m venv .venv
    echo   2. .venv\Scripts\activate
    echo   3. pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
if not exist ".venv\Lib\site-packages\flask" (
    echo Installing dependencies...
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Run the application
echo.
echo ============================================================
echo  Starting Flask Application...
echo ============================================================
echo.
echo 🚀 AI Smart Attendance System is starting...
echo.
echo ✅ Access the application at: http://127.0.0.1:5000
echo 📧 Login: Admin / admin123
echo.
echo 💡 To expose the app publicly over HTTPS with ngrok, run START-NGROK.bat instead.
echo.
echo ⏹️  Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

REM Start the Flask app
python app.py

REM Exit script
exit /b 0
