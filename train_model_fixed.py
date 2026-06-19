import face_recognition
import pickle
import os
import cv2

print("="*50)
print("Training Face Recognition Model")
print("="*50)

# Check if dataset exists
if not os.path.exists("dataset"):
    print("❌ No 'dataset' folder found!")
    print("Please run register_faces.py first")
    exit()

# Get all images from dataset
image_files = [f for f in os.listdir("dataset") if f.endswith(('.jpg', '.jpeg', '.png'))]

if len(image_files) == 0:
    print("❌ No images found in 'dataset' folder!")
    print("Please register faces first using register_faces.py")
    exit()

print(f"✓ Found {len(image_files)} face images")

known_encodings = []
known_names = []

for image_file in image_files:
    # Get name from filename (without extension)
    name = os.path.splitext(image_file)[0]
    image_path = os.path.join("dataset", image_file)
    
    print(f"Processing: {name}")
    
    # Load image
    image = face_recognition.load_image_file(image_path)
    
    # Get face encodings
    encodings = face_recognition.face_encodings(image)
    
    if len(encodings) > 0:
        known_encodings.append(encodings[0])
        known_names.append(name)
        print(f"  ✓ Face encoded successfully")
    else:
        print(f"  ❌ No face found in {image_file}")

# Save the encodings
if len(known_encodings) > 0:
    data = {
        "encodings": known_encodings,
        "names": known_names
    }
    
    with open("encodings.pkl", "wb") as f:
        pickle.dump(data, f)
    
    print("\n" + "="*50)
    print("✓ TRAINING COMPLETE!")
    print(f"  Total faces trained: {len(known_encodings)}")
    print(f"  Registered people: {', '.join(set(known_names))}")
    print(f"  Model saved to: encodings.pkl")
else:
    print("\n❌ Training failed! No faces were encoded.")

print("="*50)
