"""
Test Face Recognition Model
This script tests the trained face recognizer with real-time camera feed
Usage: python test_recognition.py
"""
import cv2
import os

def load_student_names():
    """Load student ID to name mapping"""
    student_names = {}
    if os.path.exists('student_ids.txt'):
        try:
            with open('student_ids.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        sid, name = line.split(':', 1)
                        student_names[int(sid)] = name
        except Exception as e:
            print(f"⚠️  Could not load student names: {e}")
    return student_names

def test_face_recognition():
    """Main face recognition test function"""
    print("\n" + "=" * 60)
    print("👁️  FACE RECOGNITION TEST")
    print("=" * 60)
    
    # Check if model exists
    if not os.path.exists('trainer.yml'):
        print("\n❌ ERROR: trainer.yml not found!")
        print("\n📝 Steps to fix:")
        print("   1. Run 'python capture_faces.py' to capture student faces")
        print("   2. Run 'python train_model.py' to train the model")
        print("   3. Then run this script again")
        return
    
    print("\n✅ Model found: trainer.yml")
    
    # Load the trained model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Load student names
    student_names = load_student_names()
    print(f"✅ Loaded {len(student_names)} student profiles")
    
    # Start camera
    print("\n📷 Opening camera...")
    cap = cv2.VideoCapture(0)
    
    # Try DirectShow backend if default fails (Windows)
    if not cap.isOpened():
        print("⚠️  Default camera backend failed, trying DirectShow...")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow on Windows
    
    if not cap.isOpened():
        print("\n❌ ERROR: Could not open camera!")
        print("\n🔧 SOLUTIONS:")
        print("   1. Check if camera is connected")
        print("   2. Close apps using camera (Zoom, Teams, Discord, OBS)")
        print("   3. Update drivers (Device Manager → Imaging devices)")
        print("   4. Restart computer")
        print("\n📝 To diagnose, run:")
        print("   python check_camera.py")
        print("   python test_camera_simple.py")
        return
    
    print("\n📷 Starting camera feed...")
    print("📋 Instructions:")
    print("   • Press 'q' to quit")
    print("   • Press 'c' to capture attendance")
    print("   • Position your face in the frame\n")
    
    recognized_count = 0
    unknown_count = 0
    
    last_candidate_id = None
    consecutive_matches = 0
    required_matches = 3

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read from camera")
            break
        
        # Flip frame for selfie-view
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        
        # Process detected faces
        for (x, y, w, h) in faces:
            # Predict the face
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))
            face_roi = cv2.equalizeHist(face_roi)
            student_id, confidence = recognizer.predict(face_roi)
            
            # Calculate confidence percentage
            confidence_percent = max(0.0, min(100.0, 100.0 - confidence))
            
            # Determine if it's a recognized face (lower confidence = better match)
            is_confident = confidence < 35
            is_known = student_id in student_names
            
            if is_confident and is_known:
                if last_candidate_id == student_id:
                    consecutive_matches += 1
                else:
                    last_candidate_id = student_id
                    consecutive_matches = 1
                
                # Only accept after several stable frames
                if consecutive_matches >= required_matches:
                    label = f"{student_names[student_id]} (ID: {student_id})"
                    color = (0, 255, 0)  # Green for recognized
                    recognized_count += 1
                else:
                    label = f"Candidate: {student_names[student_id]} ({consecutive_matches}/{required_matches})"
                    color = (0, 255, 255)  # Yellow for pending
                label_confidence = f"Confidence: {confidence_percent:.1f}%"
            else:
                last_candidate_id = None
                consecutive_matches = 0
                label = "Unknown"
                label_confidence = f"Confidence: {confidence_percent:.1f}%"
                color = (0, 0, 255)  # Red for unknown
                unknown_count += 1
            
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Draw labels
            cv2.putText(frame, label, (x, y-30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, label_confidence, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        
        # Display instructions and status
        cv2.putText(frame, "Press 'q' to quit | 'c' to capture", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Recognized: {recognized_count} | Unknown: {unknown_count}", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('👁️  Face Recognition Test - Press q to quit', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n⏸️  Test stopped by user")
            break
        elif key == ord('c') and len(faces) > 0:
            # Capture current frame for manual attendance
            face_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if face_id in student_names:
                print(f"✅ Attendance marked for: {student_names[face_id]}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 60)
    print(f"📊 Test Complete!")
    print(f"   • Total recognized: {recognized_count}")
    print(f"   • Total unknown: {unknown_count}")
    print("=" * 60)

def main():
    """Main function"""
    try:
        test_face_recognition()
    except KeyboardInterrupt:
        print("\n\n⏸️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()