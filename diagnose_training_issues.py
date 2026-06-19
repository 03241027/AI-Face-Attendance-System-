"""
Comprehensive diagnostic tool for face training issues
Identifies why the model is not detecting/training well
"""
import cv2
import os
import numpy as np
from collections import defaultdict

print("\n" + "=" * 70)
print("🔍 FACE TRAINING DIAGNOSTIC REPORT")
print("=" * 70)

# ============================================================================
# 1. DATASET ANALYSIS
# ============================================================================
print("\n📊 1. DATASET ANALYSIS")
print("-" * 70)

dataset_path = 'photos'
if not os.path.exists(dataset_path):
    print(f"❌ ERROR: '{dataset_path}' folder not found!")
    exit(1)

photos = [f for f in os.listdir(dataset_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
print(f"✅ Total images found: {len(photos)}")

if len(photos) == 0:
    print("❌ NO IMAGES FOUND! Capture images first using 'python capture_faces.py'")
    exit(1)

# Analyze by student
student_counts = defaultdict(int)
filename_issues = []
bad_images = []

for filename in photos:
    parts = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')
    
    # Check filename format
    if len(parts) < 2:
        filename_issues.append((filename, "Invalid filename format (expected: ID_Name_*.jpg)"))
        continue
    
    try:
        student_id = int(parts[0])
        student_name = parts[1]
        student_counts[student_id] += 1
        
        # Check if image is readable
        path = os.path.join(dataset_path, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            bad_images.append((filename, "Cannot read image (corrupted?)"))
            continue
            
    except ValueError:
        filename_issues.append((filename, "Cannot parse student ID (must be a number)"))

print(f"\n📁 Students in dataset: {len(student_counts)}")
if student_counts:
    print("   Images per student:")
    for sid in sorted(student_counts.keys()):
        count = student_counts[sid]
        status = "✅" if count >= 5 else "⚠️ " if count >= 3 else "❌"
        print(f"      {status} ID {sid}: {count} images")

# ============================================================================
# 2. FILENAME ISSUES
# ============================================================================
if filename_issues:
    print(f"\n⚠️  2. FILENAME FORMAT ISSUES ({len(filename_issues)} images)")
    print("-" * 70)
    for fname, issue in filename_issues[:10]:
        print(f"   ❌ {fname}")
        print(f"      └─ {issue}")
    if len(filename_issues) > 10:
        print(f"   ... and {len(filename_issues) - 10} more")

# ============================================================================
# 3. IMAGE QUALITY ISSUES
# ============================================================================
if bad_images:
    print(f"\n⚠️  3. CORRUPTED/UNREADABLE IMAGES ({len(bad_images)} images)")
    print("-" * 70)
    for fname, issue in bad_images[:10]:
        print(f"   ❌ {fname}: {issue}")
    if len(bad_images) > 10:
        print(f"   ... and {len(bad_images) - 10} more")

# ============================================================================
# 4. FACE DETECTION TEST
# ============================================================================
print(f"\n👁️  4. FACE DETECTION TEST (Haar Cascade)")
print("-" * 70)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

test_sample = min(10, len([p for p in photos if p.endswith(('.jpg', '.jpeg', '.png'))]))
detected = 0
not_detected = []

print(f"Testing {test_sample} random images for face detection...")

for i, filename in enumerate(sorted(photos)[:test_sample]):
    path = os.path.join(dataset_path, filename)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        continue
    
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)
    
    if len(faces) > 0:
        detected += 1
        print(f"   ✅ {filename}: {len(faces)} face(s) detected")
    else:
        not_detected.append(filename)
        print(f"   ❌ {filename}: NO FACES DETECTED")

detection_rate = (detected / test_sample * 100) if test_sample > 0 else 0
print(f"\n   Detection rate: {detected}/{test_sample} ({detection_rate:.1f}%)")

# ============================================================================
# 5. TRAINER MODEL STATUS
# ============================================================================
print(f"\n🤖 5. TRAINED MODEL STATUS")
print("-" * 70)

if os.path.exists('trainer.yml'):
    size_mb = os.path.getsize('trainer.yml') / (1024 * 1024)
    print(f"✅ trainer.yml exists (Size: {size_mb:.2f} MB)")
    
    # Try to load and test the model
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer.yml')
        print(f"✅ Model loaded successfully")
        
        # Test with one image
        test_image = None
        for filename in photos:
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(dataset_path, filename)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    test_image = cv2.resize(img, (200, 200))
                    test_image = cv2.equalizeHist(test_image)
                    break
        
        if test_image is not None:
            student_id, confidence = recognizer.predict(test_image)
            print(f"✅ Model prediction works (ID: {student_id}, Confidence: {confidence:.2f})")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
else:
    print(f"❌ trainer.yml NOT FOUND - Run 'python train_model.py' to train the model")

# ============================================================================
# 6. RECOMMENDATIONS
# ============================================================================
print(f"\n💡 RECOMMENDATIONS TO FIX TRAINING/DETECTION ISSUES")
print("-" * 70)

issues_found = False

# Check minimum images
min_per_student = min(student_counts.values()) if student_counts else 0
if min_per_student < 5:
    print("❌ ISSUE: Not enough images per student")
    print("   FIX: Capture at least 10-20 images per student")
    print("        - Different angles, lighting, and expressions")
    print("        - Run: python capture_faces.py")
    issues_found = True

# Check detection rate
if detection_rate < 80:
    print("❌ ISSUE: Haar Cascade detector failing to detect faces")
    print("   CAUSES:")
    print("      • Poor lighting/shadows in photos")
    print("      • Faces too small or too large in frame")
    print("      • Faces at extreme angles")
    print("   FIXES:")
    print("      • Capture images in good, even lighting")
    print("      • Keep face centered in frame")
    print("      • Capture images from different angles")
    print("      • Try dlib instead: python train_dlib_model.py")
    issues_found = True

# Check filename issues
if filename_issues:
    print("❌ ISSUE: Some filenames have invalid format")
    print("   FIX: Rename images to format: ID_StudentName_number.jpg")
    issues_found = True

# Check corrupted images
if bad_images:
    print("❌ ISSUE: Some image files are corrupted")
    print("   FIX: Delete corrupted images and recapture")
    issues_found = True

if not issues_found:
    print("✅ No critical issues found!")
    print("   Try the following to improve recognition:")
    print("      • Add more images per student (20+ images)")
    print("      • Improve lighting and angle variety")
    print("      • Run: python validate_model.py (to check accuracy)")
    print("      • Run: python train_dlib_model.py (alternative algorithm)")

print("\n" + "=" * 70)
