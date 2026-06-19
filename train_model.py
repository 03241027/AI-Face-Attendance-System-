"""
Train Face Recognition Model
This script trains the LBPH face recognizer using images from the photos directory
Usage: python train_model.py
"""
import argparse
import cv2
import numpy as np
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='photos', help='path to the photos dataset')
args = parser.parse_args()


def train_face_model():
    """Train face recognition model from images"""
    dataset_path = args.dataset
    
    print("\n" + "=" * 60)
    print("🤖 FACE RECOGNITION MODEL TRAINING")
    print("=" * 60)
    
    # Check if photos directory exists
    if not os.path.exists(dataset_path):
        print(f"❌ ERROR: '{dataset_path}' folder not found!")
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
    
    print(f"\n📂 Loading images from '{dataset_path}'...")
    
    # Load all images from photos directory
    image_count = 0
    detection_count = 0
    failed_files = []
    format_errors = []
    from collections import defaultdict
    student_image_count = defaultdict(int)
    
    for filename in os.listdir(dataset_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(dataset_path, filename)
            
            try:
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    failed_files.append((filename, "Could not read image"))
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
                        print(f"  ✅ {image_count}. {filename} (ID: {student_id}, Name: {student_name})")
                    except (ValueError, IndexError) as e:
                        format_errors.append((filename, "Could not parse student ID"))
                        print(f"  ⚠️  Could not parse ID from: {filename}")
                        continue
                else:
                    format_errors.append((filename, "Invalid filename format"))
                    print(f"  ⚠️  Invalid filename format: {filename}")
                    continue
                    
            except Exception as e:
                failed_files.append((filename, str(e)))
                print(f"  ❌ Error processing {filename}: {e}")
                continue
    
    print(f"\n📊 Summary:")
    print(f"   • Total images loaded: {image_count}")
    print(f"   • Unique students: {len(student_names)}")
    if student_names:
        print(f"   • Images per student:")
        for sid in sorted(student_names.keys()):
            count = student_image_count[sid]
            status = "✅" if count >= 5 else "⚠️ " if count >= 3 else "❌"
            print(f"      {status} ID {sid}: {count} images")
    
    # Show errors if any
    if format_errors:
        print(f"\n⚠️  Filename format errors ({len(format_errors)} files):")
        for fname, msg in format_errors[:5]:
            print(f"      {fname}: {msg}")
        if len(format_errors) > 5:
            print(f"      ... and {len(format_errors)-5} more")
    
    if failed_files:
        print(f"\n⚠️  Failed to read ({len(failed_files)} files):")
        for fname, msg in failed_files[:5]:
            print(f"      {fname}: {msg}")
        if len(failed_files) > 5:
            print(f"      ... and {len(failed_files)-5} more")
    
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
            print("\n📝 Next step: Run 'python test_recognition.py' to test the model")
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
        success = train_face_model()
        if success:
            print("\n" + "=" * 60)
            print("✅ Model trained successfully!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ Model training failed!")
            print("=" * 60)
    except KeyboardInterrupt:
        print("\n\n⏸️  Training interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()