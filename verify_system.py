"""
System Verification & Health Check
Validates that your system is ready for training and deployment
Usage: python verify_system.py
"""
import os
import sys
import cv2
import json
from pathlib import Path


class SystemVerifier:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []

    def print_header(self):
        """Print header"""
        print("\n" + "=" * 70)
        print("🔍 AI SMART ATTENDANCE - SYSTEM VERIFICATION")
        print("=" * 70 + "\n")

    def check_python_version(self):
        """Check Python version"""
        print("📦 Python Version...", end=" ")
        version = sys.version_info
        if version.major == 3 and version.minor >= 7:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
            self.checks_passed += 1
        else:
            print(f"❌ Python {version.major}.{version.minor} (need 3.7+)")
            self.checks_failed += 1

    def check_opencv(self):
        """Check OpenCV installation"""
        print("📷 OpenCV...", end=" ")
        try:
            version = cv2.__version__
            print(f"✅ OpenCV {version}")
            self.checks_passed += 1
            return True
        except Exception as e:
            print(f"❌ Not installed")
            self.checks_failed += 1
            return False

    def check_face_cascade(self):
        """Check face cascade classifier"""
        print("👤 Face Cascade Classifier...", end=" ")
        try:
            cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            if cascade.empty():
                print("❌ Could not load")
                self.checks_failed += 1
            else:
                print("✅ Available")
                self.checks_passed += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            self.checks_failed += 1

    def check_required_files(self):
        """Check required Python files"""
        print("📄 Required Files...", end=" ")
        required = [
            'app.py',
            'project.py',
            'templates/base.html',
            'templates/face_recognition.html',
            'static/css/style.css',
            'static/js/app.js'
        ]
        
        missing = [f for f in required if not os.path.exists(f)]
        
        if not missing:
            print(f"✅ All {len(required)} files present")
            self.checks_passed += 1
        else:
            print(f"⚠️  Missing: {', '.join(missing)}")
            self.warnings.append(f"Missing files: {missing}")
            self.checks_failed += 1

    def check_directories(self):
        """Check required directories"""
        print("📁 Directory Structure...", end=" ")
        required = ['templates', 'static', 'static/css', 'static/js']
        
        missing = [d for d in required if not os.path.isdir(d)]
        
        if not missing:
            print(f"✅ All directories exist")
            self.checks_passed += 1
        else:
            print(f"❌ Missing: {', '.join(missing)}")
            self.checks_failed += 1

    def check_camera(self):
        """Check camera availability"""
        print("🎥 Camera Access...", end=" ")
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                cap.release()
                print("✅ Camera available")
                self.checks_passed += 1
            else:
                print("⚠️  Camera not accessible")
                self.warnings.append("Camera not accessible. Check connections.")
                self.checks_failed += 1
        except Exception as e:
            print(f"⚠️  {str(e)[:30]}...")
            self.warnings.append(f"Camera error: {e}")

    def check_dataset(self):
        """Check if dataset exists"""
        print("📸 Training Dataset...", end=" ")
        if os.path.exists('photos'):
            image_count = len([f for f in os.listdir('photos') 
                             if f.endswith(('.jpg', '.jpeg', '.png'))])
            if image_count > 0:
                print(f"✅ {image_count} images found")
                self.checks_passed += 1
                
                # Check image distribution
                students = set()
                for f in os.listdir('photos'):
                    if f.endswith(('.jpg', '.jpeg', '.png')):
                        parts = f.split('_')
                        if len(parts) > 0:
                            try:
                                students.add(int(parts[0]))
                            except:
                                pass
                
                if len(students) < 2:
                    self.warnings.append(
                        f"Dataset has only {len(students)} student(s). "
                        "Recommend at least 2-3 for meaningful training."
                    )
            else:
                print("⚠️  No images yet")
                self.warnings.append("Run: python collect_training_data.py")
        else:
            print("⚠️  Not found (new installation)")
            self.warnings.append("Dataset not found. Run collection script first.")

    def check_trained_model(self):
        """Check if model is already trained"""
        print("🤖 Trained Model...", end=" ")
        if os.path.exists('trainer.yml'):
            print("✅ Model exists")
            self.checks_passed += 1
            
            # Check for mapping file
            if not os.path.exists('id_name_mapping.pkl'):
                self.warnings.append("Model exists but mapping file missing.")
        else:
            print("⚠️  Not trained yet")
            self.warnings.append("Run: python train_model_professional.py")

    def check_dependencies(self):
        """Check Python package dependencies"""
        print("📦 Dependencies...", end=" ")
        required_packages = {
            'flask': 'Flask',
            'flask_cors': 'flask-cors',
            'flask_socketio': 'flask-socketio',
            'cv2': 'opencv-python',
            'numpy': 'numpy',
            'PIL': 'Pillow'
        }
        
        missing = []
        for import_name, package_name in required_packages.items():
            try:
                __import__(import_name)
            except ImportError:
                missing.append(package_name)
        
        if not missing:
            print(f"✅ All packages installed")
            self.checks_passed += 1
        else:
            print(f"❌ Missing: {', '.join(missing)}")
            self.checks_failed += 1
            self.warnings.append(
                f"Install missing packages:\n"
                f"   pip install {' '.join(missing)}"
            )

    def check_student_data(self):
        """Check student registration data"""
        print("👥 Student Registry...", end=" ")
        if os.path.exists('students_data.json'):
            try:
                with open('students_data.json', 'r') as f:
                    data = json.load(f)
                    print(f"✅ {len(data)} students registered")
                    self.checks_passed += 1
            except:
                print("⚠️  File corrupted")
                self.checks_failed += 1
        else:
            print("⚠️  Not created yet")
            self.warnings.append("Student registry will be created on first registration.")

    def print_summary(self):
        """Print summary"""
        total = self.checks_passed + self.checks_failed
        
        print("\n" + "=" * 70)
        print("📊 VERIFICATION SUMMARY")
        print("=" * 70)
        
        print(f"\n✅ Checks Passed: {self.checks_passed}/{total}")
        print(f"❌ Checks Failed: {self.checks_failed}/{total}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings: ({len(self.warnings)})")
            for warning in self.warnings:
                lines = warning.split('\n')
                for i, line in enumerate(lines):
                    if i == 0:
                        print(f"   • {line}")
                    else:
                        print(f"     {line}")
        
        print("\n" + "=" * 70)
        
        if self.checks_failed == 0:
            print("🎉 SYSTEM READY!")
            print("\nNext Steps:")
            print("   1. Run: python collect_training_data.py")
            print("   2. Run: python train_model_professional.py")
            print("   3. Run: python app.py")
            return True
        else:
            print("⚠️  SYSTEM NOT READY")
            print("\nPlease fix the failed checks above before proceeding.")
            return False

    def run(self):
        """Run all checks"""
        self.print_header()
        
        # Core checks
        self.check_python_version()
        self.check_opencv()
        self.check_face_cascade()
        
        # System checks
        self.check_dependencies()
        self.check_directories()
        self.check_required_files()
        self.check_camera()
        
        # Data checks
        self.check_dataset()
        self.check_trained_model()
        self.check_student_data()
        
        # Summary
        return self.print_summary()


if __name__ == "__main__":
    verifier = SystemVerifier()
    success = verifier.run()
    sys.exit(0 if success else 1)
