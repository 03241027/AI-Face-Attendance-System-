"""
AI Smart Attendance System - Flask Application Entry Point
This is the main entry point for running the web application.
"""
from project import app, socketio

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI Smart Attendance System Starting...")
    print("=" * 60)
    print("✅ Visit: http://127.0.0.1:5000")
    print("📧 Login: Admin / admin123")
    print("=" * 60)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
