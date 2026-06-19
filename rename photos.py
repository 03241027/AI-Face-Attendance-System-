"""
Rename photos to correct format for training
Run: python rename_photos.py
"""
import os
import re

def rename_photos():
    """Rename all photos to ID_Name_Number.jpg format"""
    
    photos_dir = "photos"
    
    if not os.path.exists(photos_dir):
        print(f"❌ '{photos_dir}' folder not found!")
        return
    
    # Get all image files
    files = [f for f in os.listdir(photos_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print("No images found in photos folder!")
        return
    
    print("=" * 60)
    print("📸 PHOTO RENAMING TOOL")
    print("=" * 60)
    print(f"\nFound {len(files)} images\n")
    
    # Ask for mapping
    print("Please enter Student ID for each name:")
    print("(Enter 'skip' to skip a file, 'quit' to stop)\n")
    
    renamed_count = 0
    student_counter = {}
    
    for old_name in sorted(files):
        # Extract name from filename
        # Remove extensions and numbers
        base_name = re.sub(r'[\d\s_]+', ' ', old_name.split('.')[0]).strip()
        base_name = re.sub(r'\s+', ' ', base_name)
        
        print(f"\nCurrent file: {old_name}")
        print(f"Detected name: {base_name}")
        
        # Ask for student ID
        student_id = input(f"Enter Student ID for '{base_name}' (or 'skip', 'quit'): ").strip()
        
        if student_id.lower() == 'quit':
            break
        elif student_id.lower() == 'skip':
            print(f"⏭️  Skipped: {old_name}")
            continue
        
        # Track count for this student
        if student_id not in student_counter:
            student_counter[student_id] = 1
        else:
            student_counter[student_id] += 1
        
        # Create new filename
        number = student_counter[student_id]
        new_name = f"{student_id}_{base_name}_{number}.jpg"
        old_path = os.path.join(photos_dir, old_name)
        new_path = os.path.join(photos_dir, new_name)
        
        # Rename file
        os.rename(old_path, new_path)
        print(f"✅ Renamed to: {new_name}")
        renamed_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Summary:")
    print(f"   • Files renamed: {renamed_count}")
    print(f"   • Students processed: {len(student_counter)}")
    for sid, count in student_counter.items():
        print(f"     - Student {sid}: {count} images")
    print("=" * 60)
    
    if renamed_count > 0:
        print("\n✅ Ready to train! Run: python train_model.py")

if __name__ == "__main__":
    rename_photos()
    
    
    
    