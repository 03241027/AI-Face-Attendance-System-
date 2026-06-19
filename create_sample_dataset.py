"""
Sample Student Registration & Auto-Generate Test Dataset
This script creates sample students for quick testing and development
Usage: python create_sample_dataset.py
"""
import os
import json
import cv2
import numpy as np
from datetime import datetime


def create_sample_students():
    """Create sample students data"""
    students_data = {
        "1": {
            "name": "John Smith",
            "registered_date": datetime.now().isoformat()
        },
        "2": {
            "name": "Sarah Johnson",
            "registered_date": datetime.now().isoformat()
        },
        "3": {
            "name": "Michael Chen",
            "registered_date": datetime.now().isoformat()
        },
        "4": {
            "name": "Emily Davis",
            "registered_date": datetime.now().isoformat()
        },
        "5": {
            "name": "James Wilson",
            "registered_date": datetime.now().isoformat()
        }
    }
    
    # Save students data
    with open('students_data.json', 'w') as f:
        json.dump(students_data, f, indent=4)
    
    return students_data


def generate_synthetic_faces(students_data, photos_per_student=25):
    """Generate synthetic face images for testing"""
    
    os.makedirs('photos', exist_ok=True)
    
    print("\n" + "=" * 70)
    print("🤖 GENERATING SYNTHETIC FACE DATASET")
    print("=" * 70)
    print(f"\nGenerating {photos_per_student} images for each student...\n")
    
    total_generated = 0
    
    for student_id, student_data in students_data.items():
        print(f"👤 {student_data['name']} (ID: {student_id})")
        
        for count in range(photos_per_student):
            # Create a synthetic face image (200x200 grayscale)
            # In real scenario, this would be from camera capture
            
            # Generate a unique face pattern for each student
            # This simulates variations in the same person
            seed = int(student_id) * 1000 + count
            np.random.seed(seed)
            
            # Create base face image
            face = np.ones((200, 200), dtype=np.uint8) * 128
            
            # Add student-specific features (static)
            # These represent facial features
            face[50:80, 70:100] = np.random.randint(200, 255, (30, 30))   # Forehead
            face[80:130, 60:140] = np.random.randint(180, 230, (50, 80))  # Face region
            face[90:110, 70:90] = np.random.randint(100, 150, (20, 20))   # Eyes (left)
            face[90:110, 110:130] = np.random.randint(100, 150, (20, 20)) # Eyes (right)
            face[130:150, 80:120] = np.random.randint(140, 180, (20, 40)) # Mouth
            
            # Add variation (tilt, expression, lighting)
            variation = np.random.randint(-20, 20, (200, 200))
            face = np.clip(face.astype(np.int16) + variation, 0, 255).astype(np.uint8)
            
            # Apply some blur to simulate real camera
            face = cv2.GaussianBlur(face, (3, 3), 0)
            
            # Add some noise
            noise = np.random.normal(0, 5, face.shape)
            face = np.clip(face.astype(np.float32) + noise, 0, 255).astype(np.uint8)
            
            # Save image
            filename = f"photos/{student_id}_{student_data['name'].replace(' ', '_')}_{count:02d}.jpg"
            cv2.imwrite(filename, face)
            
            total_generated += 1
            if (count + 1) % 10 == 0:
                print(f"   ✅ Generated {count + 1}/{photos_per_student} images", end="\r")
        
        print(f"   ✅ Generated {photos_per_student}/{photos_per_student} images")
    
    print(f"\n✅ Total images generated: {total_generated}")
    print(f"📂 Saved to: photos/")
    
    return total_generated


def main():
    print("\n" + "=" * 70)
    print("🎓 SAMPLE DATASET GENERATOR")
    print("=" * 70)
    print("\nThis script will:")
    print("   1. Register 5 sample students")
    print("   2. Generate synthetic face images (for testing)")
    print("   3. Prepare dataset for training\n")
    
    # Create students
    students_data = create_sample_students()
    print(f"\n✅ Registered {len(students_data)} students in students_data.json")
    
    # Generate synthetic faces
    total = generate_synthetic_faces(students_data, photos_per_student=25)
    
    print("\n" + "=" * 70)
    print("✅ SAMPLE DATASET READY!")
    print("=" * 70)
    print("\n🎯 Next Steps:")
    print("   1. Run: python train_model_professional.py")
    print("   2. Then: python app.py")
    print("   3. Open: http://127.0.0.1:5000")
    print("   4. Go to: Face Recognition tab to test\n")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
