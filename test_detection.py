import cv2
import os

print("Face Detection Test")
print("="*50)

# Check if OpenCV is working
print(f"OpenCV version: {cv2.__version__}")

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print("Face detector loaded successfully")

# Ask for image path
print("\nPlease provide the full path to a photo with a face")
print("Example: C:\\Users\\User\\Pictures\\my_photo.jpg")
image_path = input("Photo path: ").strip().strip('"')

# Check if file exists
if not os.path.exists(image_path):
    print(f"File not found: {image_path}")
    exit()

# Read and process image
img = cv2.imread(image_path)
if img is None:
    print("Could not read image")
    exit()

print(f"Image size: {img.shape[1]} x {img.shape[0]} pixels")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))

if len(faces) == 0:
    print("\n❌ NO FACE DETECTED!")
    print("\nTry:")
    print("1. Use a clear front-facing photo")
    print("2. Ensure good lighting")
    print("3. Face should be visible and looking at camera")
    print("4. Photo should be from shoulders up")
else:
    print(f"\n✓ Success! Detected {len(faces)} face(s)")
    
    # Save each face
    for i, (x, y, w, h) in enumerate(faces):
        face = img[y:y+h, x:x+w]
        face_filename = f"dataset/face_{i}.jpg"
        cv2.imwrite(face_filename, face)
        print(f"  Saved face {i+1} to {face_filename}")
    
    print("\n✓ You can now use these faces for recognition")

print("\n" + "="*50)
