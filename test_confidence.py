import cv2
import os

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

# Load student names
student_names = {}
with open('student_ids.txt', 'r') as f:
    for line in f:
        if ':' in line:
            sid, name = line.strip().split(':', 1)
            student_names[int(sid)] = name

print(f"Loaded {len(student_names)} students")
print("Confidence values: LOWER = better match (0-100)")
print("If confidence > 60, match is weak\n")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = face_cascade.detectMultiScale(gray, 1.05, 3, minSize=(50,50))
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (200, 200))
        face_roi = cv2.equalizeHist(face_roi)
        
        student_id, confidence = recognizer.predict(face_roi)
        confidence_percent = max(0, min(100, 100 - confidence))
        
        # Determine if match is good
        is_match = confidence < 60
        color = (0, 255, 0) if is_match else (0, 0, 255)
        
        if is_match and student_id in student_names:
            label = f"{student_names[student_id]} ({confidence:.1f})"
        else:
            label = f"Unknown (conf:{confidence:.1f})"
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv2.putText(frame, "Confidence: LOWER = BETTER match (0-100)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    cv2.putText(frame, "Press 'q' to quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    
    cv2.imshow('Confidence Test - Lower number = Better match', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()