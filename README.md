# 🎓 AI Smart Attendance System

An intelligent, AI-powered attendance management system using face recognition technology. Built with Flask, OpenCV, and machine learning to provide real-time student tracking and engagement monitoring.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 Features

### Core Features
- ✅ **Face Recognition**: AI-powered attendance marking using advanced computer vision
- 🎥 **Real-time Processing**: Live camera feed with instant face detection and recognition
- 📊 **Web Dashboard**: User-friendly interface for attendance management
- 🔐 **Multi-user Support**: Admin, teacher, and student access levels
- 📈 **Analytics**: Attendance statistics, trends, and reporting
- ⚙️ **Manual Entry**: Alternative manual attendance marking system
- 🔔 **Real-time Alerts**: WebSocket-based instant notifications

### Advanced Features
- 🤖 LBPH Face Recognizer trained on student dataset
- 📸 Batch face capture system for data collection
- 🎯 Confidence-based recognition filtering
- 💾 Attendance logging (CSV + Database)
- 📱 Responsive web interface

---

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Camera/Webcam**: For face capture and recognition
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB for installation and dataset

---

## 🛠️ Installation & Setup

### Step 1: Clone/Download Project
```bash
cd "final year project - Copy"
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** If `face-recognition` fails to install:
- The system will still work with OpenCV-based recognition
- Alternative: Use `pip install opencv-contrib-python` for SIFT features

### Step 4: Create Required Directories
```bash
# These are created automatically, but you can pre-create them:
mkdir photos
mkdir templates
```

---

## 🎯 Quick Start Guide

### Workflow Overview
```
Capture Faces → Train Model → Test Recognition → Run Web App → Mark Attendance
```

### Step 1️⃣: Capture Student Faces
```bash
python capture_faces.py
```

**Instructions:**
1. Enter Student ID (e.g., `1`, `2`, `3`)
2. Enter Student Name (e.g., `John Doe`)
3. Look at camera and **press 's'** to capture (capture ~20 images)
4. Press 'q' when done

**Output:** Student face images saved in `photos/` folder

##03241021-I have contributed this part

### Step 2️⃣: Train the Recognition Model
```bash
python train_model.py
```

**What it does:**
- Loads all face images from `photos/` folder
- Trains LBPH face recognizer
- Saves trained model as `trainer.yml`
- Creates `student_ids.txt` with ID-to-name mapping

**Output:** 
- ✅ `trainer.yml` (trained model)
- ✅ `student_ids.txt` (student database)

### Step 3️⃣: Test Face Recognition
```bash
python test_recognition.py
```

**Features:**
- Real-time face detection and recognition
- Green box = Recognized student
- Red box = Unknown face
- Shows confidence percentage
- Press 'q' to quit

### Step 4️⃣: Start Web Application
```bash
python app.py
```

**Output:**
```
============================================================
🚀 AI Smart Attendance System Starting...
============================================================
✅ Visit: http://127.0.0.1:5000
📧 Login: Admin / admin123
============================================================
```

Visit: **http://127.0.0.1:5000**

> Want a public HTTPS URL? Run the `START-NGROK.bat` helper script instead. It starts both the Flask app and an ngrok tunnel for `https://...` access.

---

## 🔐 Login Credentials

| Role | Username | Password |
|------|----------|----------|
| 👨‍💼 Admin | `Admin` | `admin123` |
| 👨‍🎓 Student | `student1` | `pass123` |
| 👨‍🏫 Teacher | `teacher` | `teacher123` |

---

## 📁 Project Structure

```
final year project - Copy/
│
├── 🚀 Core Application Files
│   ├── app.py                      # Flask entry point
│   ├── project.py                  # Main application logic
│   └── requirements.txt             # Python dependencies
│
├── 📊 ML Training Scripts
│   ├── capture_faces.py            # Collect face images
│   ├── train_model.py              # Train face recognizer
│   └── test_recognition.py         # Test the model
│
├── 🎨 Web Interface
│   └── templates/
│       ├── login.html              # Login page
│       ├── dashboard.html          # Main dashboard
│       ├── mark_attendance.html    # Attendance marking
│       └── records.html            # View attendance records
│
├── 📸 Data & Models
│   ├── photos/                     # Student face images
│   ├── trainer.yml                 # Trained face recognition model
│   ├── student_ids.txt             # Student ID to name mapping
│   └── attendance.csv              # Attendance logs
│
├── 📝 Documentation
│   ├── README.md                   # This file
│   ├── system design.txt           # Architecture documentation
│   └── .env.example                # Environment variables template
│
└── 🔧 Configuration
    ├── run_system.bat              # Windows startup script
    └── run_system.sh               # Unix startup script
```

---

## 🎬 Usage Examples

### Example 1: Capture Faces for a New Student
```bash
# Step 1: Run capture script
python capture_faces.py

# Enter when prompted:
# Student ID: 5
# Student Name: Alice Smith

# Step 2: Position face in frame and press 's' to capture
# Capture ~20 images

# Step 3: Press 'q' to finish
```

### Example 2: Mark Attendance Manually
1. Go to Dashboard
2. Click "Mark Attendance"
3. Enter Student ID and Name
4. Click "Submit"

### Example 3: Automated Face Recognition Attendance
1. Go to "Mark Attendance" page
2. Allow camera access when prompted
3. Position face in frame
4. System automatically marks attendance when recognized

---

## 🔧 Configuration

### Database Setup (Optional - SQLite by default)

**To use MySQL instead:**

1. Edit `project.py`:
```python
# Current (SQLite):
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'

# Change to MySQL:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/attendance_db'
```

2. Create MySQL database:
```sql
CREATE DATABASE attendance_db;
```

### Environment Variables

Create `.env` file:
```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///attendance.db
SECRET_KEY=your-secret-key-here
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Camera not opening** | Check if camera is connected and not in use by other apps |
| **trainer.yml not found** | Run `python train_model.py` first |
| **No faces detected** | Ensure adequate lighting, face is clearly visible |
| **Module not found error** | Run `pip install -r requirements.txt` again |
| **Port 5000 already in use** | Change port in `app.py`: `port=5001` |
| **face_recognition fails to install** | It's optional - system works with OpenCV alone |

---

## 📊 API Endpoints

### GET Endpoints
- `GET /health` - Health check
- `GET /dashboard` - Main dashboard
- `GET /api/attendance` - Get all attendance records
- `GET /api/stats` - Get attendance statistics

### POST Endpoints
- `POST /login` - User authentication
- `POST /mark_attendance` - Record attendance

### WebSocket Events
- `connect` - Client connection
- `mark_attendance_socket` - Real-time attendance marking
- `disconnect` - Client disconnection

---

## 🔒 Security Notes

**⚠️ Important:** This is a development version. For production:

1. ✅ Use proper database (PostgreSQL/MySQL)
2. ✅ Implement secure authentication (JWT, OAuth)
3. ✅ Add SSL/HTTPS
4. ✅ Use environment variables for secrets
5. ✅ Implement rate limiting
6. ✅ Add input validation
7. ✅ Encrypt sensitive data

---

## 📈 Performance Tips

- **Larger Dataset**: Capture 20-30 images per student for better accuracy
- **Lighting**: Good lighting improves face detection significantly
- **Resolution**: Higher resolution images improve recognition accuracy
- **Distance**: Keep face 30-60cm from camera for best results
- **Model Updates**: Retrain model after adding new students

---

## 🎓 Technical Details

### Face Recognition Algorithm
- **Method**: LBPH (Local Binary Patterns Histograms)
- **Detector**: Haar Cascade Classifier
- **Library**: OpenCV

### Architecture
- **Backend**: Flask + Flask-SocketIO
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Database**: SQLite (SQLAlchemy ORM)
- **Real-time**: WebSockets

### Accuracy Metrics
- **Recognition Accuracy**: ~90% (depends on dataset quality)
- **False Positive Rate**: ~5%
- **Processing Speed**: ~30ms per face

---

## 📞 Support & Troubleshooting

### Common Issues

1. **OpenCV not building from source**
   ```bash
   pip install --only-binary :all: opencv-python
   ```

2. **Camera permissions on Linux**
   ```bash
   sudo usermod -a -G video $USER
   ```

3. **Port already in use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   kill -9 <PID>
   ```

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Author

**AI Attendance System Team**
- Group 05 - International Campus of Science and Technology

---

## 🙏 Acknowledgments

- OpenCV community
- Flask framework
- Python open-source community

---

## 📚 Additional Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/3/)

---

**Last Updated:** May 2024
**Version:** 1.0.0

---

## ⭐ Support

If you find this project useful, please consider giving it a ⭐ star!

For issues and questions, please open an issue on the project repository.
├── test_recognition.py        # Face recognition testing
├── trainer.yml               # Trained face recognition model
├── requirements.txt           # Python dependencies
├── templates/                 # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   ├── mark_attendance.html
│   └── records.html
├── photos/                    # Training face images
├── ai attendance/             # Original dataset
├── Maths.csv                  # Attendance records
├── Portuguese.csv             # Attendance records
└── README.md                  # This file
```

## 🎮 Web Interface Features

### Dashboard
- Real-time attendance statistics
- Quick access to all features
- System status monitoring

### Mark Attendance
- **Manual Entry**: Form-based attendance marking
- **Face Recognition**: AI-powered attendance (if available)
- **Real-time Feedback**: Success/error messages

### View Records
- Complete attendance history
- Separate views for Maths and Portuguese classes
- CSV export capability

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirect to login |
| `/login` | GET/POST | User authentication |
| `/dashboard` | GET | Main dashboard |
| `/mark_attendance` | GET/POST | Attendance marking interface |
| `/start_recognition` | POST | Start face recognition |
| `/start_training` | POST | Train face recognition model |
| `/view_records` | GET | View attendance records |
| `/logout` | GET | User logout |

## 🧠 Face Recognition Details

### Training Process
1. **Data Collection**: Capture multiple face images per student
2. **Preprocessing**: Convert to grayscale, detect faces
3. **Feature Extraction**: LBPH (Local Binary Patterns Histograms)
4. **Model Training**: Train recognizer on face features
5. **Model Saving**: Store trained model for recognition

### Recognition Process
1. **Face Detection**: Haar cascade classifiers
2. **Feature Matching**: Compare with trained model
3. **Confidence Scoring**: Calculate recognition accuracy
4. **Threshold Filtering**: Accept matches above 50% confidence

## 📊 Data Storage

- **Face Images**: Stored in `photos/` folder
- **Trained Model**: `trainer.yml` file
- **Attendance Records**: `Maths.csv` and `Portuguese.csv`
- **User Sessions**: Flask session management

## 🐛 Troubleshooting

### Common Issues

**1. Camera Not Working**
```bash
# Check camera access
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

**2. Model Training Fails**
- Ensure `photos/` folder exists and contains images
- Check image naming format: `ID_Name_count.jpg`
- Verify OpenCV installation

**3. Face Recognition Not Accurate**
- Capture more images per student (20+ recommended)
- Ensure good lighting and clear face visibility
- Retrain model with better quality images

**4. Web App Won't Start**
- Check if port 5000 is available
- Ensure virtual environment is activated
- Verify all dependencies are installed

### Performance Tips

- Use high-quality webcam for better recognition
- Maintain consistent lighting conditions
- Capture faces from different angles when training
- Keep face images clear and focused

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed for educational purposes.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test individual components separately

---

**Happy Attending! 🎓📸**#   A I - S m a r t - A t t e n d a n c e - S y s t e m 
 
 #   A I - S m a r t - A t t e n d a n c e - S y s t e m 
 
 #   A I - F a c e - A t t e n d a n c e - S y s t e m - 
 
 #   A I - F a c e - A t t e n d a n c e - S y s t e m - 
 
 
