"""
Camera Diagnostics - Check why camera is not opening
"""
import cv2
import sys

print("\n" + "=" * 70)
print("📷 CAMERA DIAGNOSTIC TOOL")
print("=" * 70)

print("\n🔍 Checking camera access...")

# Test 1: Try camera index 0
print("\n1️⃣  Testing Camera Index 0...")
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("   ✅ Camera 0 is available!")
    ret, frame = cap.read()
    if ret:
        print(f"   ✅ Frame captured successfully")
        print(f"   📊 Resolution: {frame.shape[1]}x{frame.shape[0]}")
    else:
        print(f"   ⚠️  Camera opened but cannot read frames")
    cap.release()
else:
    print("   ❌ Camera 0 not available")

# Test 2: Try other camera indices
print("\n2️⃣  Checking other camera indices...")
for i in range(1, 5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"   ✅ Camera {i} is available!")
        cap.release()
    cap.release()

# Test 3: OpenCV version
print(f"\n3️⃣  OpenCV Version: {cv2.__version__}")

# Test 4: Check with different API backends
print("\n4️⃣  Trying different API backends...")
backends = [
    (cv2.CAP_ANY, "CAP_ANY"),
    (cv2.CAP_DSHOW, "CAP_DSHOW (DirectShow - Windows)"),
    (cv2.CAP_MSMF, "CAP_MSMF (MediaFoundation - Windows)"),
    (cv2.CAP_V4L2, "CAP_V4L2 (V4L2 - Linux)"),
]

for backend, name in backends:
    try:
        cap = cv2.VideoCapture(0, backend)
        if cap.isOpened():
            print(f"   ✅ {name}: WORKS")
            cap.release()
        else:
            print(f"   ❌ {name}: Not available")
    except Exception as e:
        print(f"   ❌ {name}: Error - {e}")

print("\n" + "=" * 70)
print("📝 SOLUTIONS:")
print("=" * 70)

print("\n❌ IF CAMERA NOT FOUND:")
print("   1. Check if camera is physically connected")
print("   2. Restart your computer")
print("   3. Update camera drivers")
print("   4. Check Device Manager (Windows):")
print("      • Start → Device Manager")
print("      • Look for camera under 'Imaging devices'")
print("      • If ❌ exclamation mark → driver issue")
print("   5. Test camera in other apps (Windows Camera, etc)")

print("\n❌ IF CAMERA IN USE BY ANOTHER APP:")
print("   1. Close: Zoom, Skype, Teams, OBS, etc")
print("   2. Kill camera processes:")
print("      • Open Task Manager")
print("      • Find camera-related processes")
print("      • End Task")

print("\n❌ IF PERMISSIONS ISSUE:")
print("   1. Run Python as Administrator")
print("   2. Or: Grant camera permissions to Python")

print("\n✅ IF CAMERA FOUND BUT NOT OPENING:")
print("   1. Update OpenCV: pip install --upgrade opencv-python")
print("   2. Try DShow backend (Windows):")
print("      cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)")

print("\n" + "=" * 70)
