"""
Capture Student Faces - Data Collection Script
This script collects face images for training the face recognition model
Usage: python capture_faces.py
"""
import cv2
import os
from pathlib import Path

def create_photos_directory():
    """Create photos directory if it doesn't exist"""
    if not os.path.exists('photos'):
        os.makedirs('photos')
        print("✅ Created 'photos' directory")

def capture_faces():
    """Main face capture function"""
    create_photos_directory()
    
    # Initialize face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Start camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera. Check if camera is connected.")
        return
    
    # Get student information
    print("\n" + "=" * 60)
    print("📸 FACE CAPTURE SYSTEM")
    print("=" * 60)
    student_id = input("Enter Student ID (e.g., 1, 2, 3): ").strip()
    student_name = input("Enter Student Name: ").strip()
    
    if not student_id or not student_name:
        print("❌ Student ID and name are required!")
        cap.release()
        cv2.destroyAllWindows()
        return
    
    print(f"\n👤 Capturing faces for: {student_name} (ID: {student_id})")
    print("📋 Instructions:")
    print("   • Look at the camera")
    print("   • Press 's' to capture face")
    print("   • Press 'q' to quit")
    print("   • Aim to capture 15-20 images\n")
    
    count = 0
    target_images = 20
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read from camera")
            break
        
        # Flip frame for selfie-view
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {student_id} | {student_name}", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display capture count and instructions
        cv2.putText(frame, f"Captured: {count}/{target_images}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "Press 's' to capture, 'q' to quit", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('📸 Capture Faces - Press s to save, q to quit', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s') and len(faces) > 0:
            # Save all detected faces in the frame
            saved_this_frame = 0
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                filename = f"photos/{student_id}_{student_name}_{count}.jpg"
                cv2.imwrite(filename, face)
                print(f"✅ Saved: {filename}")
                count += 1
                saved_this_frame += 1
                
                if count >= target_images:
                    print(f"\n✅ Target reached! Captured {count} images for {student_name}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return
            
            if saved_this_frame == 0:
                print("⚠️  No faces detected in frame")
        
        elif key == ord('q'):
            print(f"\n⏸️  Capture stopped. Total images saved: {count}")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if count < 10:
        print(f"\n⚠️  Warning: Captured only {count} images. At least 10-15 images recommended for better accuracy.")
    else:
        print(f"\n✅ Successfully captured {count} images for {student_name}")
        print("📝 Next step: Run 'python train_model.py' to train the recognition model")

if __name__ == "__main__":
    try:
        capture_faces()
    except KeyboardInterrupt:
        print("\n\n⏸️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
