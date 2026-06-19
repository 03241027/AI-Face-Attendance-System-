"""
AI Smart Attendance System - Main Application Logic
"""
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os
import cv2
import numpy as np
import base64
from datetime import datetime
import csv
import json
import pickle

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'attendance_system_secret_key_2024'
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# User credentials
users = {
    "Admin": "admin123",
    "student1": "pass123",
    "teacher": "teacher123"
}

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "✅ AI Attendance System Active", "version": "1.0"}), 200

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    
    message = None
    if request.args.get('registered') == '1':
        message = 'Registration successful. Please sign in.'
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not username or not password or not confirm_password:
            return render_template('register.html', error="Username, password, and confirmation are required.")
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")
        if username in users:
            return render_template('register.html', error="Username already exists.")

        users[username] = password
        return redirect(url_for('login', registered='1'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def load_stats():
    attendance_file = 'attendance.csv'
    stats = {
        'total_records': 0,
        'today_present': 0,
        'unique_students': 0
    }

    if os.path.exists(attendance_file):
        try:
            with open(attendance_file, 'r', newline='', encoding='utf-8') as f:
                records = list(csv.DictReader(f))
                stats['total_records'] = len(records)
                today = datetime.now().strftime('%Y-%m-%d')
                stats['today_present'] = len([r for r in records if r.get('Date') == today])
                stats['unique_students'] = len(set([r.get('Student ID') for r in records if r.get('Student ID')]))
        except Exception as e:
            print(f"Error loading stats: {e}")

    return stats

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    stats = load_stats()
    return render_template(
        'dashboard.html',
        user=session['user'],
        page_title='Dashboard',
        page_sub='Attendance summary and quick actions',
        active_page='dashboard',
        stats=stats
    )

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        student_id = request.form.get('student_id', '').strip()
        date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        time = request.form.get('time', datetime.now().strftime('%H:%M:%S'))
        
        if not student_name or not student_id:
            return jsonify({"error": "❌ Student name and ID are required"}), 400
        
        attendance_file = 'attendance.csv'
        try:
            if not os.path.exists(attendance_file):
                with open(attendance_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Student ID', 'Student Name', 'Date', 'Time', 'Status', 'Method'])
            
            with open(attendance_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([student_id, student_name, date, time, 'Present', 'Manual'])
            
            return jsonify({
                "success": True,
                "message": f"✅ Attendance marked for {student_name}"
            }), 200
        except Exception as e:
            return jsonify({"error": f"❌ Error: {str(e)}"}), 500
    
    return render_template(
        'mark_attendance.html',
        user=session['user'],
        page_title='Attendance',
        page_sub='Mark attendance manually or with camera support',
        active_page='mark_attendance'
    )

@app.route('/records')
def records():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    attendance_data = []
    attendance_file = 'attendance.csv'
    
    if os.path.exists(attendance_file):
        try:
            with open(attendance_file, 'r') as f:
                reader = csv.DictReader(f)
                attendance_data = list(reader)
        except Exception as e:
            print(f"Error reading attendance: {e}")
    
    return render_template(
        'records.html',
        user=session['user'],
        page_title='Attendance Records',
        page_sub='Search and export attendance history',
        active_page='records',
        attendance_records=attendance_data
    )

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    attendance_data = []
    attendance_file = 'attendance.csv'
    
    if os.path.exists(attendance_file):
        try:
            with open(attendance_file, 'r') as f:
                reader = csv.DictReader(f)
                attendance_data = list(reader)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify(attendance_data), 200

@app.route('/api/attendance/delete/<int:row_index>', methods=['DELETE'])
def delete_attendance_record(row_index):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    attendance_file = 'attendance.csv'
    if not os.path.exists(attendance_file):
        return jsonify({'error': 'No attendance data found.'}), 404

    try:
        with open(attendance_file, 'r', newline='', encoding='utf-8') as f:
            records = list(csv.DictReader(f))

        if row_index < 0 or row_index >= len(records):
            return jsonify({'error': 'Record index out of range.'}), 404

        deleted = records.pop(row_index)

        with open(attendance_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Student ID', 'Student Name', 'Date', 'Time', 'Status', 'Method'])
            writer.writeheader()
            writer.writerows(records)

        return jsonify({'success': True, 'deleted': deleted}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    stats = load_stats()
    return jsonify(stats), 200

# ============================================================================
# FACE RECOGNITION ROUTES - FIXED VERSION
# ============================================================================

@app.route('/face_recognition')
def face_recognition_page():
    """Face recognition page"""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'face_recognition.html',
        user=session['user'],
        page_title='Face Recognition',
        page_sub='Camera-based attendance capture',
        active_page='face_recognition'
    )

@app.route('/test_recognition')
def test_recognition_page():
    """Face recognition test page"""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template(
        'face_recognition.html',
        user=session['user'],
        page_title='Face Recognition',
        page_sub='Camera-based attendance capture',
        active_page='face_recognition'
    )

@app.route('/api/recognize', methods=['POST'])
def recognize_face_api():
    """API endpoint for face recognition - FIXED VERSION with higher threshold"""
    try:
        import pickle
        
        data = request.json
        image_data = data.get('image')
        
        # Decode base64 image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'recognized': False, 'error': 'Invalid image'}), 200
        
        # Load face detector
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Preprocess frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        # Detect faces with MORE SENSITIVE parameters
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.05,    # More sensitive
            minNeighbors=2,      # Very sensitive
            minSize=(50, 50),    # Smaller minimum face
            maxSize=(500, 500)
        )
        
        print(f"🔍 Faces detected: {len(faces)}")
        
        # Check if model exists
        if not os.path.exists('trainer.yml'):
            print("❌ Model not found!")
            return jsonify({'recognized': False, 'error': 'Model not trained'}), 200

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer.yml')
        
        # Load student names
        student_names = {}
        
        # Try pickle file first
        if os.path.exists('id_name_mapping.pkl'):
            try:
                with open('id_name_mapping.pkl', 'rb') as f:
                    student_names = pickle.load(f)
                    print(f"✅ Loaded {len(student_names)} students from pickle")
            except Exception as e:
                print(f"Error loading pickle: {e}")
        
        # Fallback to txt file
        if not student_names and os.path.exists('student_ids.txt'):
            with open('student_ids.txt', 'r') as f:
                for line in f:
                    if ':' in line:
                        try:
                            sid, name = line.strip().split(':', 1)
                            student_names[int(sid)] = name
                        except:
                            pass
            print(f"✅ Loaded {len(student_names)} students from txt")
        
        if len(faces) == 0:
            print("❌ No faces detected in image")
            return jsonify({'recognized': False, 'faces_detected': 0}), 200
        
        # Process the largest face
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        
        # Extract face region
        face_roi = gray[y:y+h, x:x+w]
        
        # Ensure proper size
        face_resized = cv2.resize(face_roi, (200, 200))
        
        # Apply CLAHE for better feature extraction
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        face_enhanced = clahe.apply(face_resized)
        
        # Predict
        student_id, confidence = recognizer.predict(face_enhanced)
        
        print(f"🎯 Predicted ID: {student_id}, Confidence: {confidence:.2f}")
        
        # CONFIDENCE THRESHOLD - HIGHER VALUE = MORE LENIENT
        # For LBPH, lower confidence = better match (0 is perfect)
        # Set to 120 to be very lenient (will match most faces)
        CONFIDENCE_THRESHOLD = 120  # ← CHANGE THIS VALUE TO ADJUST LENIENCY
        
        if confidence < CONFIDENCE_THRESHOLD and student_id in student_names:
            confidence_percent = max(0.0, min(100.0, 100.0 - (confidence / 100.0 * 100)))
            print(f"✅ RECOGNIZED: {student_names[student_id]} (Confidence: {confidence:.2f})")
            return jsonify({
                'recognized': True,
                'student_id': int(student_id),
                'student_name': student_names.get(student_id, f"Student_{student_id}"),
                'confidence': confidence_percent,
                'raw_confidence': float(confidence)
            }), 200
        else:
            print(f"❌ NOT RECOGNIZED - ID: {student_id}, Conf: {confidence}, Threshold: {CONFIDENCE_THRESHOLD}")
            if student_id in student_names:
                print(f"   Student exists but confidence too high: {confidence} > {CONFIDENCE_THRESHOLD}")
            return jsonify({
                'recognized': False,
                'confidence': max(0, min(100, 100 - confidence)),
                'raw_confidence': float(confidence),
                'faces_detected': len(faces)
            }), 200
            
    except Exception as e:
        print(f"❌ Recognition error: {str(e)}")
        return jsonify({'error': str(e), 'recognized': False}), 200

# ============================================================================
# ADDITIONAL PAGE ROUTES
# ============================================================================

@app.route('/students')
def students_page():
    """Students directory page"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    students = []
    if os.path.exists('student_ids.txt'):
        with open('student_ids.txt', 'r') as f:
            for line in f:
                if ':' in line:
                    sid, name = line.strip().split(':', 1)
                    students.append({
                        'id': sid,
                        'name': name,
                        'last_seen': 'Today',
                        'records': 0
                    })
    
    return render_template(
        'students.html',
        user=session['user'],
        active_page='students',
        students=students
    )

@app.route('/analytics')
def analytics_page():
    """Analytics dashboard page"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    stats = load_stats()
    return render_template(
        'analytics.html',
        user=session['user'],
        active_page='analytics',
        stats=stats
    )

@app.route('/alerts')
def alerts_page():
    """System alerts page"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template(
        'alerts.html',
        user=session['user'],
        active_page='alerts'
    )

@app.route('/settings')
def settings_page():
    """Settings page"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template(
        'settings.html',
        user=session['user'],
        active_page='settings'
    )

# ============================================================================
# SOCKET.IO EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    emit('response', {'data': '✅ Connected to server'})

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("=" * 60)
    print("🚀 AI Smart Attendance System Starting...")
    print("=" * 60)
    print("✅ Visit: http://127.0.0.1:5000")
    print("📧 Login: Admin / admin123")
    print("=" * 60)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)