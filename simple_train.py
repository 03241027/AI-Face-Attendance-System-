import cv2
import os
import pickle
import numpy as np

print("="*50)
print("Simple Training (OpenCV LBPH)")
print("="*50)

# Check dataset
if not os.path.exists("dataset"):
    print("❌ No dataset folder")
    exit()

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Get images
images = []
labels = []
label_names = {}
current_id = 0

print("Loading images...")
for filename in os.listdir("dataset"):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        name = os.path.splitext(filename)[0]
        path = os.path.join("dataset", filename)
        
        # Assign label
        if name not in label_names.values():
            label_names[current_id] = name
            label_id = current_id
            current_id += 1
        else:
            for k, v in label_names.items():
                if v == name:
                    label_id = k
                    break
        
        # Load and process image
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect face
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
        
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            images.append(face)
            labels.append(label_id)
            print(f"  ✓ Processed: {name}")

# Train model
if len(images) > 0:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(images, np.array(labels))
    recognizer.save("face_model.yml")
    
    with open("labels.pkl", "wb") as f:
        pickle.dump(label_names, f)
    
    print(f"\n✓ Training complete!")
    print(f"  Faces trained: {len(images)}")
    print(f"  People: {', '.join(label_names.values())}")
else:
    print("❌ No faces detected for training")
