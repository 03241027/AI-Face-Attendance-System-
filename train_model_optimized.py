"""
Train Face Recognition Model - OPTIMIZED VERSION
With better parameters and diagnostic output
Usage: python train_model_optimized.py
"""
import argparse
import cv2
import numpy as np
import os
from pathlib import Path
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='photos', help='path to the photos dataset')
parser.add_argument('--scale', type=float, default=1.1, help='Haar Cascade scaleFactor (1.05-1.4, lower=more detection)')
parser.add_argument('--neighbors', type=int, default=4, help='Haar Cascade minNeighbors (3-7, lower=more detection)')
args = parser.parse_args()


def train_face_model_optimized():
    """Train face recognition model from images with optimizations"""
    dataset_path = args.dataset
    
    print("\n" + "=" * 70)
    print("🤖 FACE RECOGNITION MODEL TRAINING - OPTIMIZED")
    print("=" * 70)
    print(f"\n⚙️  Parameters:")
    print(f"   • scaleFactor: {args.scale} (lower = more lenient detection)")
    print(f"   • minNeighbors: {args.neighbors} (lower = more lenient detection)")
    
    # Check if photos directory exists
    if not os.path.exists(dataset_path):
        print(f"\n❌ ERROR: '{dataset_path}' folder not found!")
        print("\n📝 Steps:")
        print("   1. Run 'python capture_faces.py' to capture student faces")
        print("   2. Then run this script again")
        return False
    
    # Initialize face detector and recognizer
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    faces = []
    ids = []
    student_names = {}
    student_image_count = defaultdict(int)
    
    print(f"\n📂 Loading images from '{dataset_path}'...")
    
    # Load all images from photos directory
    image_count = 0
    failed_files = []
    
    for filename in os.listdir(dataset_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(dataset_path, filename)
            
            try:
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    failed_files.append((filename, "Cannot read image"))
                    continue
                
                # Extract student ID and name from filename
                # Expected format: ID_StudentName_count.jpg
                parts = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')

                if len(parts) >= 2:
                    try:
                        student_id = int(parts[0])
                        student_name = parts[1]

                        img = cv2.resize(img, (200, 200))
                        img = cv2.equalizeHist(img)
                        
                        # Store mapping of ID to name
                        if student_id not in student_names:
                            student_names[student_id] = student_name
                        
                        faces.append(img)
                        ids.append(student_id)
                        student_image_count[student_id] += 1
                        image_count += 1
                        
                        if image_count % 10 == 0:
                            print(f"  ✅ Loaded {image_count} images...")
                    except (ValueError, IndexError):
                        failed_files.append((filename, "Invalid filename format (ID_Name_*.jpg)"))
                        continue
                else:
                    failed_files.append((filename, "Invalid filename format"))
                    continue
                    
            except Exception as e:
                failed_files.append((filename, str(e)))
                continue
    
    print(f"\n📊 Dataset Summary:")
    print(f"   • Total images loaded: {image_count}")
    print(f"   • Unique students: {len(student_names)}")
    
    if student_names:
        print(f"\n   Images per student:")
        for sid in sorted(student_names.keys()):
            count = student_image_count[sid]
            min_recommended = 10
            if count >= min_recommended:
                status = "✅ Excellent"
            elif count >= 5:
                status = "⚠️  OK"
            else:
                status = "❌ Too few"
            print(f"      {status} | ID {sid}: {count} images")
    
    if failed_files:
        print(f"\n⚠️  Issues found with {len(failed_files)} files:")
        for fname, msg in failed_files[:10]:
            print(f"      {fname}: {msg}")
        if len(failed_files) > 10:
            print(f"      ... and {len(failed_files)-10} more")
    
    # Train the model if we have images
    if len(faces) > 0:
        print(f"\n🔄 Training model on {len(faces)} images...")
        try:
            recognizer.train(faces, np.array(ids))
            recognizer.write('trainer.yml')
            
            # Save student names mapping
            with open('student_ids.txt', 'w') as f:
                for student_id, name in sorted(student_names.items()):
                    f.write(f"{student_id}:{name}\n")
            
            print("✅ SUCCESS! Model training complete!")
            print("   📁 Saved: trainer.yml")
            print("   📁 Saved: student_ids.txt")
            print(f"\n📝 Next step: Run 'python validate_model.py' to check accuracy")
            
            # Provide recommendations
            print(f"\n💡 Recommendations:")
            min_images = min(student_image_count.values()) if student_image_count else 0
            if min_images < 10:
                print(f"   ⚠️  Some students have only {min_images} images")
                print(f"      Capture 10-20+ images per student for better accuracy")
            
            print(f"\n🧪 To test the model:")
            print(f"   • Run: python test_recognition.py")
            print(f"   • If detection is poor, try:")
            print(f"      python train_model_optimized.py --scale 1.05 --neighbors 3")
            
            return True
        except Exception as e:
            print(f"❌ Error during training: {e}")
            return False
    else:
        print("\n❌ ERROR: No face images found in 'photos' folder!")
        print("\n📝 Steps to fix:")
        print("   1. Run 'python capture_faces.py' to capture student faces")
        print("   2. Make sure images are saved in the 'photos' folder")
        print("   3. Run this script again")
        return False

def main():
    """Main function"""
    try:
        success = train_face_model_optimized()
        if success:
            print("\n" + "=" * 70)
            print("✅ Model trained successfully!")
            print("=" * 70)
        else:
            print("\n" + "=" * 70)
            print("❌ Model training failed!")
            print("=" * 70)
    except KeyboardInterrupt:
        print("\n\n⏸️  Training interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
