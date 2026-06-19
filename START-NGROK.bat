@echo off
REM AI Smart Attendance System - Windows Startup Script with ngrok

echo.
echo ============================================================
echo  AI Smart Attendance System - Startup Script with ngrok
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

REM Check if ngrok is available
where ngrok >nul 2>&1
if errorlevel 1 (
    echo ERROR: ngrok is not installed or not in PATH.
    echo.
    echo Install ngrok and make sure it is available from the command line.
    echo Example: https://ngrok.com/download
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo ============================================================
echo  Starting Flask Application and ngrok Tunnel...
echo ============================================================
echo.
echo 🚀 AI Smart Attendance System is starting...
echo.
echo ✅ Flask local app: http://127.0.0.1:5000

echo ✅ ngrok will expose an HTTPS public URL after launch
echo.
echo ⏹️  Press Ctrl+C in each window to stop the server and the tunnel
echo.
echo ============================================================
echo.

REM Start the Flask app in a new window
start "AI Attendance Server" cmd /k "cd /d %~dp0 && call .venv\Scripts\activate.bat && python app.py"

REM Start ngrok tunnel in this terminal so HTTPS appears here
echo Starting ngrok tunnel in the current window...
cd /d %~dp0
ngrok http 5000

echo.
echo If ngrok shows both URLs, use the HTTPS one above.
echo.
echo Press Ctrl+C to stop ngrok. Close the Flask server window separately when done.
exit /b 0
