"""
Professional Face Data Collection System
Captures high-quality face images for training with proper validation
Usage: python collect_training_data.py
"""
import cv2
import os
import json
from pathlib import Path
from datetime import datetime
import numpy as np


class DataCollector:
    def __init__(self, dataset_dir='photos'):
        self.dataset_dir = dataset_dir
        self.students_file = 'students_data.json'
        self.students = self.load_students()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.min_faces_required = 20
        self.max_face_area_variance = 0.3
        
        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)
            print(f"✅ Created '{self.dataset_dir}' directory")

    def load_students(self):
        """Load existing students data"""
        if os.path.exists(self.students_file):
            try:
                with open(self.students_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_students(self):
        """Save students data"""
        with open(self.students_file, 'w') as f:
            json.dump(self.students, f, indent=4)

    def get_existing_students(self):
        """Display existing students"""
        if not self.students:
            print("\n📋 No students registered yet.\n")
            return None
        
        print("\n" + "=" * 60)
        print("📋 EXISTING STUDENTS")
        print("=" * 60)
        for idx, (sid, data) in enumerate(self.students.items(), 1):
            count = len([f for f in os.listdir(self.dataset_dir) 
                        if f.startswith(f"{sid}_")])
            status = "✅ Complete" if count >= self.min_faces_required else f"⏳ {count}/{self.min_faces_required}"
            print(f"{idx}. ID: {sid:3} | Name: {data['name']:20} | Images: {status}")
        print("=" * 60)

    def register_new_student(self):
        """Register new student"""
        print("\n" + "=" * 60)
        print("📝 REGISTER NEW STUDENT")
        print("=" * 60)
        
        while True:
            student_id = input("\nEnter Student ID (numeric, unique): ").strip()
            if not student_id.isdigit():
                print("❌ Student ID must be numeric!")
                continue
            if student_id in self.students:
                print("❌ Student ID already exists!")
                continue
            break
        
        student_name = input("Enter Student Name (First Last): ").strip()
        if not student_name or len(student_name.split()) < 1:
            print("❌ Please enter a valid name!")
            return None
        
        self.students[student_id] = {
            'name': student_name,
            'registered_date': datetime.now().isoformat()
        }
        self.save_students()
        print(f"\n✅ Student '{student_name}' (ID: {student_id}) registered!")
        
        return student_id

    def collect_faces(self, student_id, student_name):
        """Collect face images for a student"""
        print("\n" + "=" * 70)
        print(f"📸 CAPTURING FACES FOR: {student_name} (ID: {student_id})")
        print("=" * 70)
        
        # Open camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ ERROR: Camera not accessible!")
            return False
        
        # Optimize camera settings
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        
        print("\n📋 INSTRUCTIONS:")
        print("   • Face the camera directly")
        print("   • Keep good lighting")
        print("   • Press 's' to capture image")
        print("   • Press 'q' to finish")
        print(f"   • Target: {self.min_faces_required} images")
        print("   • Press 'r' to reset current batch\n")
        
        count = 0
        face_sizes = []
        current_batch = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error reading camera frame!")
                break
            
            # Mirror for selfie-view
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.05, minNeighbors=4, minSize=(100, 100)
            )
            
            # Draw UI
            frame_display = frame.copy()
            
            # Status bar
            cv2.rectangle(frame_display, (0, 0), (640, 50), (20, 20, 20), -1)
            status_text = f"Captured: {count}/{self.min_faces_required}"
            cv2.putText(frame_display, status_text, (10, 35),
                       cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            
            # Draw detected faces
            if len(faces) > 0:
                largest_face = max(faces, key=lambda f: f[2] * f[3])
                x, y, w, h = largest_face
                
                # Quality indicator
                face_area = w * h
                if face_sizes:
                    avg_area = np.mean(face_sizes)
                    variance = abs(face_area - avg_area) / avg_area
                    color = (0, 255, 0) if variance < self.max_face_area_variance else (0, 165, 255)
                    cv2.putText(frame_display, f"Variance: {variance:.2f}", (10, 70),
                               cv2.FONT_HERSHEY_DUPLEX, 0.6, color, 1)
                
                # Draw rectangle
                cv2.rectangle(frame_display, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame_display, f"ID: {student_id} | {student_name}",
                           (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
            
            # Instructions
            instructions = "Press 's' to capture | 'q' to finish | 'r' to reset"
            cv2.putText(frame_display, instructions, (10, 460),
                       cv2.FONT_HERSHEY_DUPLEX, 0.5, (200, 200, 200), 1)
            
            cv2.imshow(f'Face Capture - {student_name}', frame_display)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s') and len(faces) > 0:
                # Capture largest face
                x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
                face_roi = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face_roi, (200, 200))
                
                # Save image
                filename = f"{self.dataset_dir}/{student_id}_{student_name}_{count:02d}.jpg"
                cv2.imwrite(filename, face_resized)
                
                current_batch.append(filename)
                face_sizes.append(w * h)
                count += 1
                
                print(f"✅ Captured {count}/{self.min_faces_required}: {filename}")
                
                if count >= self.min_faces_required:
                    print(f"\n🎉 Completed! Captured {count} images for {student_name}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return True
            
            elif key == ord('q'):
                if count > 0:
                    print(f"\n⏹️  Stopped. Captured {count} images.")
                    cap.release()
                    cv2.destroyAllWindows()
                    return count >= self.min_faces_required
                else:
                    print("\n❌ No images captured. Exiting.")
                    cap.release()
                    cv2.destroyAllWindows()
                    return False
            
            elif key == ord('r'):
                # Reset current batch
                print("\n🔄 Resetting batch...")
                for f in current_batch:
                    if os.path.exists(f):
                        os.remove(f)
                count = 0
                face_sizes = []
                current_batch = []
        
        cap.release()
        cv2.destroyAllWindows()
        return count >= self.min_faces_required

    def run(self):
        """Main collection workflow"""
        print("\n" + "=" * 70)
        print("🎓 AI SMART ATTENDANCE - DATA COLLECTION SYSTEM")
        print("=" * 70)
        
        while True:
            self.get_existing_students()
            
            print("\n📌 OPTIONS:")
            print("1. Register & capture new student")
            print("2. Capture more images for existing student")
            print("3. Delete student data")
            print("4. Exit\n")
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == '1':
                student_id = self.register_new_student()
                if student_id:
                    if self.collect_faces(student_id, self.students[student_id]['name']):
                        print("✅ Student data collection completed!")
                    else:
                        print("⚠️  Minimum images not reached. Try again.")
            
            elif choice == '2':
                if not self.students:
                    print("❌ No students to add images to!")
                    continue
                
                sid = input("\nEnter Student ID: ").strip()
                if sid not in self.students:
                    print("❌ Student not found!")
                    continue
                
                self.collect_faces(sid, self.students[sid]['name'])
            
            elif choice == '3':
                if not self.students:
                    print("❌ No students to delete!")
                    continue
                
                sid = input("\nEnter Student ID to delete: ").strip()
                if sid not in self.students:
                    print("❌ Student not found!")
                    continue
                
                name = self.students[sid]['name']
                confirm = input(f"Delete all data for {name}? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    del self.students[sid]
                    for f in os.listdir(self.dataset_dir):
                        if f.startswith(f"{sid}_"):
                            os.remove(os.path.join(self.dataset_dir, f))
                    self.save_students()
                    print(f"✅ Deleted all data for {name}")
            
            elif choice == '4':
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid option!")


if __name__ == "__main__":
    collector = DataCollector()
    collector.run()
