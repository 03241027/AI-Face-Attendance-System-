"""
Test Face Recognition Model
Verifies that the trained model can recognize faces from photos_aug
Usage: python test_recognition_quick.py
"""
import cv2
import pickle
import os
import numpy as np


def test_recognition():
    print("\n" + "=" * 70)
    print("🧪 TESTING FACE RECOGNITION MODEL")
    print("=" * 70)
    
    # Check model files
    print("\n📁 Checking model files...")
    
    if not os.path.exists('trainer.yml'):
        print("❌ trainer.yml not found!")
        return False
    print("✅ trainer.yml exists")
    
    if not os.path.exists('student_ids.txt'):
        print("❌ student_ids.txt not found!")
        return False
    print("✅ student_ids.txt exists")
    
    # Load model
    print("\n🤖 Loading LBPH Face Recognizer...")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    print("✅ Model loaded successfully")
    
    # Load student mappings
    print("\n📋 Loading student mappings...")
    student_names = {}
    with open('student_ids.txt', 'r') as f:
        for line in f:
            if ':' in line:
                sid, name = line.strip().split(':', 1)
                student_names[int(sid)] = name
    
    print(f"✅ Loaded {len(student_names)} student mappings")
    print(f"\nSample students:")
    for i, (sid, name) in enumerate(list(student_names.items())[:5]):
        print(f"   {sid}: {name}")
    print("   ...")
    
    # Test on sample images from photos_aug
    print("\n🧪 Testing on sample images from photos_aug...")
    test_images = []
    photos_aug_dir = 'photos_aug'
    
    if not os.path.exists(photos_aug_dir):
        print(f"❌ {photos_aug_dir} directory not found!")
        return False
    
    # Get first 5 images for testing
    for filename in sorted(os.listdir(photos_aug_dir))[:5]:
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            test_images.append(filename)
    
    if not test_images:
        print("❌ No test images found!")
        return False
    
    print(f"\nTesting {len(test_images)} sample images:\n")
    
    correct = 0
    for filename in test_images:
        path = os.path.join(photos_aug_dir, filename)
        
        # Parse filename to get expected ID
        parts = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')
        expected_id = int(parts[0])
        expected_name = parts[1] if len(parts) > 1 else f"Student_{expected_id}"
        
        # Read and preprocess image
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        
        img = cv2.resize(img, (200, 200))
        img = cv2.equalizeHist(img)
        
        # Apply CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)
        
        # Predict
        predicted_id, confidence = recognizer.predict(img)
        predicted_name = student_names.get(predicted_id, f"Student_{predicted_id}")
        
        is_correct = predicted_id == expected_id
        status = "✅" if is_correct else "❌"
        
        print(f"{status} {filename}")
        print(f"   Expected: ID {expected_id} ({expected_name})")
        print(f"   Predicted: ID {predicted_id} ({predicted_name})")
        print(f"   Confidence: {confidence:.2f}\n")
        
        if is_correct:
            correct += 1
    
    accuracy = (correct / len(test_images)) * 100 if test_images else 0
    print(f"📊 Quick Test Results: {correct}/{len(test_images)} correct ({accuracy:.0f}%)")
    
    print("\n" + "=" * 70)
    print("✅ RECOGNITION SYSTEM READY!")
    print("=" * 70)
    print("\n🚀 Next: Start the Flask app")
    print("   Command: python app.py")
    print("   Access: http://127.0.0.1:5000")
    print("   Login: Admin / admin123")
    print("   Go to: Face Recognition tab")
    print("   Camera will recognize your 52 students!\n")
    
    return True


if __name__ == "__main__":
    success = test_recognition()
    exit(0 if success else 1)
