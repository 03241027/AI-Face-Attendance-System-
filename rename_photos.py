import os
import re

def rename_photos():
    photos_dir = "photos"
    
    if not os.path.exists(photos_dir):
        print(f"Error: '{photos_dir}' folder not found!")
        return
    
    files = [f for f in os.listdir(photos_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print("No images found in photos folder!")
        return
    
    print("=" * 60)
    print("PHOTO RENAMING TOOL")
    print("=" * 60)
    print(f"\nFound {len(files)} images\n")
    
    renamed_count = 0
    student_counter = {}
    
    for old_name in sorted(files):
        # Extract name from filename
        name_part = old_name.split('.')[0]
        # Keep only letters and spaces
        clean_name = ''.join(c for c in name_part if c.isalpha() or c == ' ')
        clean_name = ' '.join(clean_name.split())
        
        print(f"\nCurrent file: {old_name}")
        print(f"Detected name: {clean_name}")
        
        student_id = input(f"Enter Student ID for '{clean_name}' (or 'skip', 'quit'): ").strip()
        
        if student_id.lower() == 'quit':
            break
        elif student_id.lower() == 'skip':
            print(f"Skipped: {old_name}")
            continue
        
        if student_id not in student_counter:
            student_counter[student_id] = 1
        else:
            student_counter[student_id] += 1
        
        number = student_counter[student_id]
        new_name = f"{student_id}_{clean_name}_{number}.jpg"
        old_path = os.path.join(photos_dir, old_name)
        new_path = os.path.join(photos_dir, new_name)
        
        os.rename(old_path, new_path)
        print(f"Renamed to: {new_name}")
        renamed_count += 1
    
    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"   Files renamed: {renamed_count}")
    print(f"   Students processed: {len(student_counter)}")
    print("=" * 60)

if __name__ == "__main__":
    rename_photos()