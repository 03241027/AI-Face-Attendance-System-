# 📖 Complete Setup Guide

## Quick Reference Commands

### Windows
```batch
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Capture faces
python capture_faces.py

# 4. Train model
python train_model.py

# 5. Test recognition
python test_recognition.py

# 6. Start application
python app.py
```

### macOS/Linux
```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Capture faces
python3 capture_faces.py

# 4. Train model
python3 train_model.py

# 5. Test recognition
python3 test_recognition.py

# 6. Start application
python3 app.py
```

---

## System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- 500MB disk space
- USB Camera/Webcam

### Recommended
- Python 3.10+
- 8GB RAM
- 2GB disk space
- HD Webcam (720p+)

---

## File Organization After Setup

```
final year project - Copy/
├── .venv/                          # Virtual environment (auto-created)
├── __pycache__/                    # Python cache (auto-created)
│
├── 📂 Main Application
│   ├── app.py ✅                   # Entry point
│   ├── project.py ✅               # Core logic
│   └── requirements.txt ✅         # Dependencies
│
├── 📂 Machine Learning
│   ├── capture_faces.py ✅         # Data collection
│   ├── train_model.py ✅           # Model training
│   ├── test_recognition.py ✅      # Model testing
│   ├── trainer.yml                 # Trained model (created after training)
│   └── student_ids.txt             # Student mapping (created after training)
│
├── 📂 Web Interface
│   └── templates/
│       ├── login.html
│       ├── dashboard.html
│       ├── mark_attendance.html
│       └── records.html
│
├── 📂 Data & Logs
│   ├── photos/                     # Student faces (captured images)
│   ├── attendance.csv              # Attendance logs
│   └── attendance.db               # SQLite database
│
└── 📂 Documentation
    ├── README.md ✅                # Main documentation
    ├── SETUP_GUIDE.md ✅           # This file
    └── system design.txt           # Architecture
```

---

## Step-by-Step Setup Instructions

### Phase 1: Environment Setup (5 minutes)

**Step 1a: Create Virtual Environment**
```bash
python -m venv .venv
```

**Step 1b: Activate Virtual Environment**

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

You should see `(.venv)` at the beginning of your terminal prompt.

**Step 1c: Update pip**
```bash
python -m pip install --upgrade pip
```

**Step 1d: Install Dependencies**
```bash
pip install -r requirements.txt
```

Expected output: `Successfully installed [packages...]`

### Phase 2: Data Collection (10-20 minutes)

**Step 2a: Create Photos Directory**
```bash
mkdir photos
```

**Step 2b: Capture Faces**
```bash
python capture_faces.py
```

Follow on-screen instructions:
- Enter student ID: `1`
- Enter name: `John Doe`
- Press 's' to capture faces
- Capture 15-20 images per student
- Press 'q' when done

**Step 2c: Repeat for Each Student**
- Student 2, 3, 4, etc.
- Aim for consistent lighting and angles

### Phase 3: Model Training (5-10 minutes)

**Step 3: Train the Model**
```bash
python train_model.py
```

Expected output:
```
============================================================
🤖 FACE RECOGNITION MODEL TRAINING
============================================================

📂 Loading images from 'photos'...
  ✅ 1. 1_John_Doe_0.jpg (ID: 1, Name: John Doe)
  ✅ 2. 1_John_Doe_1.jpg (ID: 1, Name: John Doe)
  ...
  
📊 Summary:
   • Total images loaded: 50
   • Unique students: 3

🔄 Training model on 50 images...
✅ SUCCESS! Model training complete!
   📁 Saved: trainer.yml
   📁 Saved: student_ids.txt
```

### Phase 4: Model Testing (5 minutes)

**Step 4: Test Face Recognition**
```bash
python test_recognition.py
```

- Position face in frame
- Look for green boxes (recognized) or red boxes (unknown)
- Press 'q' to exit

### Phase 5: Web Application (Ongoing)

**Step 5: Start the Application**
```bash
python app.py
```

Expected output:
```
============================================================
🚀 AI Smart Attendance System Starting...
============================================================
✅ Visit: http://127.0.0.1:5000
📧 Login: Admin / admin123
============================================================
 * Running on http://127.0.0.1:5000
```

**Access the application:**
1. Open web browser
2. Go to: http://127.0.0.1:5000
3. Login with: Admin / admin123
4. Start marking attendance!

---

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (no errors)
- [ ] `photos/` directory created
- [ ] Faces captured (check `photos/` folder)
- [ ] Model trained (`trainer.yml` exists)
- [ ] Student IDs saved (`student_ids.txt` exists)
- [ ] Model test successful (faces recognized)
- [ ] Web app starts without errors
- [ ] Can access http://127.0.0.1:5000
- [ ] Can login with credentials

---

## Running Commands for First-Time Users

### Complete Setup from Scratch

```bash
# Step 1: Navigate to project folder
cd "final year project - Copy"

# Step 2: Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Step 3: Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Ensure photos directory exists
mkdir photos

# Step 5: Capture student faces
python capture_faces.py

# Step 6: Train the model
python train_model.py

# Step 7: Test recognition
python test_recognition.py

# Step 8: Run the web application
python app.py
```

---

## Daily Usage

### To Start the System

```bash
# 1. Open terminal/command prompt
# 2. Navigate to project folder
cd "final year project - Copy"

# 3. Activate virtual environment
.venv\Scripts\activate

# 4. Start application
python app.py

# 5. Open browser and go to: http://127.0.0.1:5000
```

### To Add New Students

```bash
# 1. Make sure app is running
# 2. In new terminal window, activate venv
.venv\Scripts\activate

# 3. Capture new student faces
python capture_faces.py

# 4. Retrain the model
python train_model.py

# 5. Model is automatically updated in app
```

---

## Troubleshooting Quick Fixes

### Issue: "python: command not found"
**Solution:** Use `python3` instead of `python` on macOS/Linux

### Issue: "Module not found: flask"
**Solution:** Run `pip install -r requirements.txt` again

### Issue: Camera not opening
**Solution:** 
- Check camera is connected
- Close other apps using camera
- Try plugging into different USB port

### Issue: Port 5000 already in use
**Solution:** Edit `app.py` and change `port=5000` to `port=5001`

### Issue: "No module named cv2"
**Solution:** Run `pip install opencv-python --upgrade`

### Issue: "trainer.yml not found"
**Solution:** Make sure you ran `python train_model.py` first

---

## Performance Tuning

### For Better Face Recognition Accuracy:
1. Capture 20-30 images per student (not just 15)
2. Use consistent lighting
3. Include various angles and expressions
4. Retrain model after adding new students

### For Faster Performance:
1. Use a solid-state drive (SSD)
2. Close unnecessary background applications
3. Use a camera with at least 720p resolution

---

## Important Notes

⚠️ **Before Going Live:**
1. Backup your photos and attendance data
2. Test with all student photos
3. Verify all credentials work
4. Test on different computers/networks
5. Create database backups regularly

💡 **Best Practices:**
- Keep the system updated
- Regular backups of attendance data
- Periodic model retraining with new data
- Monitor system performance logs

---

## Getting Help

If you encounter issues:
1. Check the error message carefully
2. Search this guide for the error
3. Review the troubleshooting section
4. Check README.md for detailed info
5. Verify all dependencies are installed

---

**Last Updated:** May 2024
**Version:** 1.0
