import os
import shutil

def add_new_students():
    print("=" * 60)
    print("📸 ADD NEW STUDENTS (25 to 47)")
    print("=" * 60)
    
    # Get source folder
    source = input("Enter folder path with new student photos: ").strip()
    
    if not os.path.exists(source):
        print(f"❌ Folder not found: {source}")
        return
    
    # Get all folders or files
    print("\nHow are your photos organized?")
    print("1. Each student has a folder")
    print("2. All photos in one folder")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '1':
        # Each student in separate folder
        folders = [f for f in os.listdir(source) if os.path.isdir(os.path.join(source, f))]
        
        for folder in folders:
            print(f"\n📁 Processing: {folder}")
            student_id = input(f"Enter Student ID for {folder}: ").strip()
            student_name = input(f"Enter Student Name for ID {student_id}: ").strip()
            
            folder_path = os.path.join(source, folder)
            photos = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
            
            for i, photo in enumerate(photos, start=1):
                src = os.path.join(folder_path, photo)
                dst = os.path.join('photos', f"{student_id}_{student_name}_{i}.jpg")
                shutil.copy2(src, dst)
                print(f"  ✅ Added: {student_name} - Photo {i}")
    
    else:
        # All photos in one folder
        student_id = input("Enter Starting Student ID (e.g., 26): ").strip()
        student_name = input("Enter Student Name: ").strip()
        
        photos = [f for f in os.listdir(source) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        for i, photo in enumerate(photos, start=1):
            src = os.path.join(source, photo)
            dst = os.path.join('photos', f"{student_id}_{student_name}_{i}.jpg")
            shutil.copy2(src, dst)
            print(f"✅ Added: {student_name} - Photo {i}")
    
    print("\n✅ All new students added!")
    print("Run 'python train_model.py' to train the model")

if __name__ == "__main__":
    add_new_students()