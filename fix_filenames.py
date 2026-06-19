"""
Fix Invalid Filenames - Rename to Correct Format
Convert: Mahara.jpeg → 26_Mahara_1.jpeg
"""
import os
from collections import defaultdict

print("\n" + "=" * 70)
print("🔧 FIXING INVALID FILENAME FORMAT")
print("=" * 70)

dataset_path = 'photos'

# Find all files with invalid format
invalid_files = []
valid_files = []
student_ids_used = set()

print("\n📂 Scanning photos folder...")

for filename in os.listdir(dataset_path):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        # Check if filename has proper format: ID_Name_Number
        name_without_ext = filename.rsplit('.', 1)[0]
        parts = name_without_ext.split('_')
        
        # Valid format: ID_Name_Number (at least 3 parts, first is digit)
        is_valid = len(parts) >= 2 and parts[0].isdigit()
        
        if is_valid:
            valid_files.append(filename)
            student_ids_used.add(int(parts[0]))
        else:
            invalid_files.append(filename)

print(f"✅ Valid files: {len(valid_files)}")
print(f"⚠️  Invalid files: {len(invalid_files)}")

if invalid_files:
    print(f"\n❌ Invalid filenames found:")
    for f in invalid_files[:10]:
        print(f"   • {f}")
    if len(invalid_files) > 10:
        print(f"   ... and {len(invalid_files) - 10} more")

if not invalid_files:
    print("\n✅ All filenames are valid! No fixes needed.")
    exit(0)

# Assign new IDs to invalid files
print(f"\n🔍 Assigning new Student IDs...")

# Get next available ID
next_id = max(student_ids_used) + 1 if student_ids_used else 1

# Group invalid files by student name
invalid_by_name = defaultdict(list)
for filename in invalid_files:
    name_without_ext = filename.rsplit('.', 1)[0]
    invalid_by_name[name_without_ext].append(filename)

print(f"\n📝 Renaming scheme:")
print(f"   Students already have IDs: 1-{max(student_ids_used) if student_ids_used else 0}")
print(f"   New students will get IDs: {next_id}+")

# Rename files
rename_map = {}
for student_name, files in sorted(invalid_by_name.items()):
    print(f"\n   Student: {student_name}")
    print(f"   New ID: {next_id}")
    print(f"   Files to rename: {len(files)}")
    
    for idx, filename in enumerate(files, 1):
        ext = filename.rsplit('.', 1)[1]
        new_filename = f"{next_id}_{student_name}_{idx}.{ext}"
        old_path = os.path.join(dataset_path, filename)
        new_path = os.path.join(dataset_path, new_filename)
        
        rename_map[filename] = new_filename
        print(f"      {filename} → {new_filename}")
    
    next_id += 1

# Ask for confirmation
print("\n" + "=" * 70)
print("🔄 READY TO RENAME FILES")
print("=" * 70)
print(f"\nWill rename {len(invalid_files)} files to correct format")
print("\nThese students will be assigned NEW IDs:")
for name in sorted(invalid_by_name.keys()):
    print(f"  • {name}")

response = input("\n⚠️  Proceed with renaming? (yes/no): ").strip().lower()

if response != 'yes':
    print("❌ Cancelled. No files renamed.")
    exit(0)

# Perform renaming
print("\n🔄 Renaming files...")
renamed_count = 0
failed_count = 0

for old_name, new_name in rename_map.items():
    old_path = os.path.join(dataset_path, old_name)
    new_path = os.path.join(dataset_path, new_name)
    
    try:
        if os.path.exists(new_path):
            print(f"⚠️  {new_name} already exists, skipping")
            continue
        
        os.rename(old_path, new_path)
        print(f"✅ {old_name} → {new_name}")
        renamed_count += 1
    except Exception as e:
        print(f"❌ Error renaming {old_name}: {e}")
        failed_count += 1

print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"✅ Successfully renamed: {renamed_count} files")
print(f"❌ Failed to rename: {failed_count} files")

if failed_count == 0:
    print("\n✅ All files renamed successfully!")
    print("\nNow retrain your model:")
    print("  python train_model.py")
    print("OR")
    print("  python validate_model.py")
