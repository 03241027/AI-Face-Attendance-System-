import cv2
import os

print("Starting Face Recognition Test...")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

if not os.path.exists("trainer.yml"):
    print("ERROR: trainer.yml not found! Run python train_model.py first")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

student_names = {}
if os.path.exists("student_ids.txt"):
    with open("student_ids.txt", "r") as f:
        for line in f:
            if ":" in line:
                sid, name = line.strip().split(":", 1)
                student_names[int(sid)] = name
    print(f"Loaded {len(student_names)} students")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = face_cascade.detectMultiScale(gray, 1.05, 3, minSize=(60,60))
    
    for (x,y,w,h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (200,200))
        student_id, confidence = recognizer.predict(face_roi)
        
        if confidence < 60 and student_id in student_names:
            label = f"{student_names[student_id]}"
            color = (0,255,0)
        else:
            label = "Unknown"
            color = (0,0,255)
        
        cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
        cv2.putText(frame, label, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"Conf: {confidence:.0f}", (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    cv2.putText(frame, "Faces: " + str(len(faces)), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.imshow("Face Recognition", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
