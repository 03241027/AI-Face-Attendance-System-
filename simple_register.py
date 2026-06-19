import cv2
import os
import numpy as np

print("="*50)
print("Simple Face Registration (OpenCV Only)")
print("="*50)

# Create dataset folder
if not os.path.exists("dataset"):
    os.makedirs("dataset")
    print("✓ Created 'dataset' folder")

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open webcam!")
    exit()

print("\n📸 Webcam ready")
print("Press 's' to save face, 'q' to quit\n")

face_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.putText(frame, f"Faces: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Press 's' to save, 'q' to quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow('Register Face', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s') and len(faces) > 0:
        name = input("\nEnter name: ")
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            filename = f"dataset/{name}.jpg"
            cv2.imwrite(filename, face)
            print(f"✓ Saved: {filename}")
            face_count += 1

cap.release()
cv2.destroyAllWindows()
print(f"\n✓ Saved {face_count} face(s)")
