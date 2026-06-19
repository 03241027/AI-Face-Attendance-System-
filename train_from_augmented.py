"""
Train Model from Existing Augmented Dataset (photos_aug)
Optimized for limited images per student with proper face preprocessing
Usage: python train_from_augmented.py
"""
import cv2
import numpy as np
import os
import pickle
import sys
from collections import defaultdict


class AugmentedDatasetTrainer:
    def __init__(self, dataset_dir='photos_aug', model_file='trainer.yml', 
                 mapping_file='id_name_mapping.pkl'):
        self.dataset_dir = dataset_dir
        self.model_file = model_file
        self.mapping_file = mapping_file
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def validate_dataset(self):
        """Validate dataset exists and has images"""
        print("\n" + "=" * 70)
        print("🔍 VALIDATING AUGMENTED DATASET")
        print("=" * 70)
        
        if not os.path.exists(self.dataset_dir):
            print(f"❌ ERROR: '{self.dataset_dir}' directory not found!")
            return False
        
        images = [f for f in os.listdir(self.dataset_dir) 
                 if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not images:
            print(f"❌ No images found in '{self.dataset_dir}'!")
            return False
        
        # Analyze dataset
        student_counts = defaultdict(int)
        invalid_files = []
        
        print(f"\n📊 Dataset Analysis:")
        print(f"   Total images: {len(images)}")
        
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
        
        print(f"   Total students: {len(student_counts)}")
        print(f"   Students with data: {len(student_counts)}")
        
        # Show distribution
        min_images = min(student_counts.values()) if student_counts else 0
        max_images = max(student_counts.values()) if student_counts else 0
        print(f"   Images per student: {min_images}-{max_images}")
        
        if invalid_files:
            print(f"\n⚠️  Invalid filenames: {len(invalid_files)}")
            print("   Expected format: ID_Name_number.jpg")
        
        if len(student_counts) < 2:
            print("\n❌ ERROR: Need at least 2 students!")
            return False
        
        print("\n✅ Dataset validation passed!")
        return True

    def extract_face_features(self, image, add_noise=False):
        """Extract and enhance face features for single-image datasets"""
        # Ensure correct size
        if image.shape != (200, 200):
            image = cv2.resize(image, (200, 200))
        
        # Histogram equalization
        enhanced = cv2.equalizeHist(image)
        
        # CLAHE for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(enhanced)
        
        # Apply bilateral filter to smooth while keeping edges
        enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        # Optional: Add slight noise variation for robustness
        if add_noise:
            noise = np.random.normal(0, 2, enhanced.shape)
            enhanced = np.clip(enhanced.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        
        return enhanced

    def augment_single_image(self, image):
        """Generate variations of a single image for better training"""
        variations = [image]
        
        # Slight rotations
        for angle in [-10, 10]:
            rows, cols = image.shape
            M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
            rotated = cv2.warpAffine(image, M, (cols, rows))
            variations.append(rotated)
        
        # Brightness adjustments
        for delta in [-30, 30]:
            bright = np.clip(image.astype(np.float32) + delta, 0, 255).astype(np.uint8)
            variations.append(bright)
        
        # Slight sharpening
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]]) / 2.0
        sharpened = cv2.filter2D(image, -1, kernel)
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        variations.append(sharpened)
        
        # Horizontal flip
        flipped = cv2.flip(image, 1)
        variations.append(flipped)
        
        return variations

    def load_training_data(self):
        """Load and augment training images"""
        print("\n" + "=" * 70)
        print("📂 LOADING AND AUGMENTING DATA")
        print("=" * 70)
        
        faces = []
        ids = []
        id_name_mapping = {}
        
        images = [f for f in os.listdir(self.dataset_dir) 
                 if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"\n📦 Processing {len(images)} images with augmentation...\n")
        
        failed_count = 0
        augmentation_count = 0
        
        for idx, filename in enumerate(images, 1):
            path = os.path.join(self.dataset_dir, filename)
            
            try:
                # Parse filename (ID_Name_number.jpg)
                parts = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')
                student_id = int(parts[0])
                student_name = parts[1] if len(parts) > 1 else f"Student_{student_id}"
                
                # Read image
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    failed_count += 1
                    print(f"  ❌ Failed to read: {filename}")
                    continue
                
                # Extract and enhance features
                enhanced = self.extract_face_features(img, add_noise=False)
                
                # Add original enhanced version
                faces.append(enhanced)
                ids.append(student_id)
                id_name_mapping[student_id] = student_name
                
                # Generate augmented variations
                variations = self.augment_single_image(enhanced)
                for var in variations[1:]:  # Skip first (original)
                    var_enhanced = self.extract_face_features(var, add_noise=False)
                    faces.append(var_enhanced)
                    ids.append(student_id)
                    augmentation_count += len(variations) - 1
                
                if idx % 10 == 0:
                    print(f"   ✅ Processed {idx}/{len(images)} images")
            
            except Exception as e:
                failed_count += 1
                print(f"  ❌ Error processing {filename}: {str(e)[:50]}")
                continue
        
        print(f"\n   ✅ Processed all {len(images)} images")
        
        if failed_count > 0:
            print(f"   ⚠️  Failed to process {failed_count} images")
        
        print(f"\n📊 Training Data Summary:")
        print(f"   • Original images: {len(images)}")
        print(f"   • Augmented variations: {augmentation_count}")
        print(f"   • Total training faces: {len(faces)}")
        print(f"   • Unique students: {len(set(ids))}")
        print(f"   • ID-Name mapping: {len(id_name_mapping)} entries")
        
        if len(faces) < 50:
            print("\n⚠️  WARNING: Limited training data. Accuracy may be lower.")
            print("   Consider collecting more images per student for better results.")
        
        return faces, ids, id_name_mapping

    def train_model(self, faces, ids):
        """Train LBPH face recognizer optimized for limited data"""
        print("\n" + "=" * 70)
        print("🤖 TRAINING FACE RECOGNIZER (OPTIMIZED FOR LIMITED DATA)")
        print("=" * 70)
        
        print("\n⚙️  Creating LBPH Face Recognizer...")
        print("   Parameters optimized for single-image datasets")
        
        # Adjusted parameters for better performance with limited data
        recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=2,           # Increased for more context
            neighbors=16,       # More neighbors for robustness
            grid_x=10,          # Finer grid for detailed features
            grid_y=10           # Finer grid for detailed features
        )
        
        print(f"\n📚 Training model with {len(faces)} face samples...")
        recognizer.train(faces, np.array(ids))
        
        print("✅ Training completed successfully!")
        return recognizer

    def validate_model(self, recognizer, faces, ids, id_name_mapping):
        """Validate trained model"""
        print("\n" + "=" * 70)
        print("✔️  VALIDATING MODEL")
        print("=" * 70)
        
        if len(faces) < 20:
            print("⚠️  Not enough data for comprehensive validation")
            print("   (Need at least 20 images)\n")
            return
        
        # Test on samples
        num_tests = min(15, len(faces) // 3)
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
            
            print(f"{status} Expected: {expected_name:20} | Predicted: {predicted_name:20} | "
                  f"Confidence: {confidence:.2f}")
            
            if is_correct:
                correct += 1
        
        accuracy = (correct / num_tests) * 100
        print(f"\n📊 Validation Accuracy: {accuracy:.1f}% ({correct}/{num_tests})")
        
        if accuracy < 60:
            print("⚠️  WARNING: Validation accuracy is low.")
            print("   The model may need more diverse training images.")
            print("   Consider collecting additional images from different angles/lighting.")
        elif accuracy < 80:
            print("⚠️  Accuracy could be improved with more training data.")
        else:
            print("✅ Model validation passed!")

    def save_model(self, recognizer, id_name_mapping):
        """Save trained model"""
        print("\n" + "=" * 70)
        print("💾 SAVING MODEL")
        print("=" * 70)
        
        recognizer.write(self.model_file)
        print(f"✅ Model saved: {self.model_file}")
        
        # Save mapping
        with open(self.mapping_file, 'wb') as f:
            pickle.dump(id_name_mapping, f)
        print(f"✅ ID-Name mapping saved: {self.mapping_file}")
        
        # Also save as student_ids.txt for compatibility
        with open('student_ids.txt', 'w') as f:
            for student_id, name in sorted(id_name_mapping.items()):
                f.write(f"{student_id}:{name}\n")
        print("✅ Legacy format saved: student_ids.txt")

    def run(self):
        """Main training workflow"""
        print("\n" + "=" * 70)
        print("🎓 TRAIN MODEL FROM AUGMENTED DATASET")
        print("=" * 70)
        print("\nThis script will:")
        print("   1. Load images from photos_aug/")
        print("   2. Enhance and augment each image")
        print("   3. Train LBPH face recognizer")
        print("   4. Validate model accuracy")
        print("   5. Save trained model")
        
        # Step 1: Validate
        if not self.validate_dataset():
            print("\n❌ Dataset validation failed!")
            return False
        
        # Step 2: Load and augment
        faces, ids, id_name_mapping = self.load_training_data()
        if faces is None or len(faces) == 0:
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
        print("\n✅ Your trained model is ready!")
        print("   Next: Run the Flask app to test face recognition")
        print("   Command: python app.py")
        print("   Access: http://127.0.0.1:5000")
        print("   Camera will recognize your students!\n")
        
        return True


if __name__ == "__main__":
    trainer = AugmentedDatasetTrainer()
    success = trainer.run()
    sys.exit(0 if success else 1)
