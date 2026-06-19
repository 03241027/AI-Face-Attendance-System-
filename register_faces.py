import cv2
import face_recognition
import pickle
import os
import numpy as np

print("="*50)
print("Face Registration System")
print("="*50)

# Create dataset folder if it doesn't exist
if not os.path.exists("dataset"):
    os.makedirs("dataset")
    print("✓ Created 'dataset' folder")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open webcam!")
    print("Please check:")
    print("  - Webcam is connected")
    print("  - Webcam drivers are installed")
    print("  - No other app is using the webcam")
    exit()

print("\n📸 Webcam opened successfully")
print("\nInstructions:")
print("1. Look at the camera")
print("2. Make sure your face is in the green box")
print("3. Press 's' to save your face")
print("4. Press 'q' to quit")
print("\n" + "="*50)

face_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break
    
    # Convert to RGB for face_recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    
    # Draw rectangles around faces
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, "Face Detected", (left, top-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Show status
    status = f"Faces detected: {len(face_locations)}"
    cv2.putText(frame, status, (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Press 's' to save, 'q' to quit", (10, 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Display
    cv2.imshow('Register Face', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s') and len(face_locations) > 0:
        # Save the face
        name = input("\nEnter person's name: ")
        
        for (top, right, bottom, left) in face_locations:
            face = frame[top:bottom, left:right]
            filename = f"dataset/{name}.jpg"
            cv2.imwrite(filename, face)
            print(f"✓ Face saved as {filename}")
            face_count += 1

cap.release()
cv2.destroyAllWindows()

print(f"\n✓ Registration complete! Saved {face_count} face(s)")
