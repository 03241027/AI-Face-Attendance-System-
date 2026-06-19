import cv2

print("Testing Webcam...")
print("Press 'q' to quit")

# Try to open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open webcam!")
    print("Check:")
    print("  - Webcam is connected")
    print("  - Webcam drivers are installed")
    print("  - No other app is using the webcam")
    exit()

print("✓ Webcam opened successfully")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("❌ Failed to capture frame")
        break
    
    # Show the frame
    cv2.imshow('Webcam Test', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Webcam test completed")
