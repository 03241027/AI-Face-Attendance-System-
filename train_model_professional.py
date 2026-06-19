"""
Professional Face Recognition Model Training
Optimized training with validation and quality checks
Usage: python train_model_professional.py
"""
import cv2
import numpy as np
import os
import json
from pathlib import Path
from collections import defaultdict
import pickle


class ModelTrainer:
    def __init__(self, dataset_dir='photos', model_file='trainer.yml', 
                 mapping_file='id_name_mapping.pkl'):
        self.dataset_dir = dataset_dir
        self.model_file = model_file
        self.mapping_file = mapping_file
        self.students_file = 'students_data.json'
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.min_images_per_student = 15

    def load_students_data(self):
        """Load registered students"""
        if os.path.exists(self.students_file):
            try:
                with open(self.students_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def validate_dataset(self):
        """Validate dataset integrity"""
        print("\n" + "=" * 70)
        print("🔍 VALIDATING DATASET")
        print("=" * 70)
        
        if not os.path.exists(self.dataset_dir):
            print(f"❌ ERROR: '{self.dataset_dir}' directory not found!")
            return False
        
        images = [f for f in os.listdir(self.dataset_dir) 
                 if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not images:
            print(f"❌ No images found in '{self.dataset_dir}'!")
            print("\n📝 Please run: python collect_training_data.py")
            return False
        
        # Parse and validate filenames
        student_counts = defaultdict(int)
        invalid_files = []
        
        for img in images:
            parts = img.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')
            if len(parts) >= 2:
                try:
                    student_id = int(parts[0])
                    student_counts[student_id] += 1
                except ValueError:
                    invalid_files.append(img)
            else:
                invalid_files.append(img)
        
        print(f"\n📊 Found {len(images)} images")
        print(f"\n👥 Students: {len(student_counts)}")
        
        insufficient_students = []
        for sid, count in sorted(student_counts.items()):
            status = "✅" if count >= self.min_images_per_student else "⚠️"
            print(f"   {status} ID {sid}: {count} images", end="")
            if count < self.min_images_per_student:
                print(f" (need {self.min_images_per_student - count} more)")
                insufficient_students.append(sid)
            else:
                print()
        
        if invalid_files:
            print(f"\n⚠️  Invalid filenames: {len(invalid_files)}")
            for f in invalid_files[:5]:
                print(f"   - {f}")
        
        if len(student_counts) < 2:
            print("\n❌ ERROR: Need at least 2 students to train!")
            return False
        
        if insufficient_students:
            print(f"\n⚠️  WARNING: {len(insufficient_students)} student(s) have insufficient images")
            proceed = input("   Continue anyway? (yes/no): ").strip().lower()
            return proceed == 'yes'
        
        print("\n✅ Dataset validation passed!")
        return True

    def load_training_data(self):
        """Load and preprocess training images"""
        print("\n" + "=" * 70)
        print("📂 LOADING TRAINING DATA")
        print("=" * 70)
        
        faces = []
        ids = []
        id_name_mapping = {}
        students_data = self.load_students_data()
        
        images = [f for f in os.listdir(self.dataset_dir) 
                 if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"\n📦 Processing {len(images)} images...\n")
        
        failed_count = 0
        for idx, filename in enumerate(images, 1):
            path = os.path.join(self.dataset_dir, filename)
            
            try:
                # Parse filename
                parts = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')
                student_id = int(parts[0])
                student_name = parts[1] if len(parts) > 1 else f"Student_{student_id}"
                
                # Read image
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    failed_count += 1
                    continue
                
                # Ensure correct size
                if img.shape != (200, 200):
                    img = cv2.resize(img, (200, 200))
                
                # Enhance image
                img = cv2.equalizeHist(img)
                
                # Apply CLAHE for better feature extraction
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                img = clahe.apply(img)
                
                # Store data
                faces.append(img)
                ids.append(student_id)
                id_name_mapping[student_id] = student_name
                
                if idx % 20 == 0:
                    print(f"   ✅ Processed {idx}/{len(images)} images")
            
            except Exception as e:
                failed_count += 1
                continue
        
        print(f"   ✅ Processed all {len(images)} images")
        
        if failed_count > 0:
            print(f"   ⚠️  Failed to process {failed_count} images")
        
        if len(faces) < 30:
            print("\n❌ ERROR: Not enough valid training images!")
            return None, None, None
        
        print(f"\n📊 Training data summary:")
        print(f"   • Total faces: {len(faces)}")
        print(f"   • Unique students: {len(set(ids))}")
        print(f"   • ID-Name mapping: {len(id_name_mapping)} entries")
        
        return faces, ids, id_name_mapping

    def train_model(self, faces, ids):
        """Train LBPH face recognizer"""
        print("\n" + "=" * 70)
        print("🤖 TRAINING FACE RECOGNIZER")
        print("=" * 70)
        
        print("\n⚙️  Initializing LBPH Face Recognizer...")
        
        recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=1,
            neighbors=8,
            grid_x=8,
            grid_y=8
        )
        
        print("📚 Training model... (this may take a minute)")
        recognizer.train(faces, np.array(ids))
        
        print("✅ Training completed successfully!")
        return recognizer

    def validate_model(self, recognizer, faces, ids, id_name_mapping):
        """Validate trained model on random samples"""
        print("\n" + "=" * 70)
        print("✔️  VALIDATING MODEL")
        print("=" * 70)
        
        if len(faces) < 10:
            print("⚠️  Not enough images for validation")
            return
        
        # Test on random samples
        num_tests = min(10, len(faces) // 3)
        correct = 0
        
        print(f"\nTesting on {num_tests} random samples...\n")
        
        np.random.seed(42)
        test_indices = np.random.choice(len(faces), num_tests, replace=False)
        
        for test_idx in test_indices:
            test_face = faces[test_idx]
            expected_id = ids[test_idx]
            
            predicted_id, confidence = recognizer.predict(test_face)
            
            expected_name = id_name_mapping.get(expected_id, f"Student_{expected_id}")
            predicted_name = id_name_mapping.get(predicted_id, f"Student_{predicted_id}")
            
            is_correct = predicted_id == expected_id
            status = "✅" if is_correct else "❌"
            
            print(f"{status} Expected: {expected_name} | Predicted: {predicted_name} | "
                  f"Confidence: {confidence:.2f}")
            
            if is_correct:
                correct += 1
        
        accuracy = (correct / num_tests) * 100
        print(f"\n📊 Validation Accuracy: {accuracy:.1f}% ({correct}/{num_tests})")
        
        if accuracy < 70:
            print("⚠️  WARNING: Low validation accuracy. Consider collecting more diverse images.")
        else:
            print("✅ Model validation passed!")

    def save_model(self, recognizer, id_name_mapping):
        """Save trained model"""
        print("\n" + "=" * 70)
        print("💾 SAVING MODEL")
        print("=" * 70)
        
        recognizer.write(self.model_file)
        print(f"✅ Model saved: {self.model_file}")
        
        with open(self.mapping_file, 'wb') as f:
            pickle.dump(id_name_mapping, f)
        print(f"✅ ID-Name mapping saved: {self.mapping_file}")
        
        # Also save as student_ids.txt for legacy compatibility
        with open('student_ids.txt', 'w') as f:
            for student_id, name in sorted(id_name_mapping.items()):
                f.write(f"{student_id}:{name}\n")
        print("✅ Legacy format saved: student_ids.txt")

    def run(self):
        """Main training workflow"""
        print("\n" + "=" * 70)
        print("🎓 AI SMART ATTENDANCE - MODEL TRAINING")
        print("=" * 70)
        print("\nThis script will:")
        print("   1. Validate your dataset")
        print("   2. Load and preprocess images")
        print("   3. Train LBPH face recognizer")
        print("   4. Validate model accuracy")
        print("   5. Save the trained model")
        
        # Step 1: Validate
        if not self.validate_dataset():
            print("\n❌ Dataset validation failed!")
            return False
        
        # Step 2: Load data
        faces, ids, id_name_mapping = self.load_training_data()
        if faces is None:
            print("\n❌ Failed to load training data!")
            return False
        
        # Step 3: Train
        recognizer = self.train_model(faces, ids)
        
        # Step 4: Validate
        self.validate_model(recognizer, faces, ids, id_name_mapping)
        
        # Step 5: Save
        self.save_model(recognizer, id_name_mapping)
        
        print("\n" + "=" * 70)
        print("🎉 MODEL TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\n✅ Your trained model is ready to use!")
        print("   Next: Run the Flask app to test face recognition")
        print(f"   Command: python app.py\n")
        
        return True


if __name__ == "__main__":
    trainer = ModelTrainer()
    success = trainer.run()
    exit(0 if success else 1)
