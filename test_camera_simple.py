"""
Simple Camera Test - Just show camera feed
Run this to test if camera is working
"""
import cv2

print("\n📷 Simple Camera Test")
print("=" * 50)
print("Attempting to open camera...")

# Try camera index 0
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: Could not open camera!")
    print("\nSolutions:")
    print("1. Check if camera is connected")
    print("2. Close other apps using camera (Zoom, Skype, Teams)")
    print("3. Try: python check_camera.py (to diagnose)")
    print("4. Restart computer")
    exit(1)

print("✅ Camera opened successfully!")
print("\nInstructions:")
print("  • 'q' to quit")
print("  • 's' to save a frame")
print("\nStarting camera feed...")

frame_count = 0
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("❌ Could not read frame from camera")
        break
    
    frame_count += 1
    
    # Flip for selfie view
    frame = cv2.flip(frame, 1)
    
    # Show info
    cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Press 'q' to quit | 's' to save", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imshow('Camera Test', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("\n✅ Closing camera...")
        break
    elif key == ord('s'):
        filename = f"camera_test_{frame_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"✅ Saved: {filename}")

cap.release()
cv2.destroyAllWindows()

print("✅ Camera test complete!")
