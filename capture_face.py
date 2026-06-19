import cv2

print("Webcam Face Capture")
print("="*50)

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot access webcam")
    exit()

print("Press SPACE to take photo, ESC to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture")
        break
    
    # Show frame
    cv2.imshow('Face Capture', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == 32:  # SPACE
        # Save photo
        cv2.imwrite('test_face.jpg', frame)
        print("Photo saved as test_face.jpg")
        
        # Detect face
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        
        if len(faces) > 0:
            print(f"✓ Face detected! Saved {len(faces)} face(s)")
            # Save face region
            x, y, w, h = faces[0]
            face = frame[y:y+h, x:x+w]
            cv2.imwrite('dataset/registered_face.jpg', face)
            print("✓ Face registered in dataset folder")
        else:
            print("❌ No face detected in the photo")
        break

cap.release()
cv2.destroyAllWindows()
