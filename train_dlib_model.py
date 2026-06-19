"""
Train face embeddings using dlib / face_recognition.
This script creates 128-dimensional face encodings for each student and stores them for later recognition.
Usage: python train_dlib_model.py
"""
import glob
import json
import os
import pickle
import sys
from collections import defaultdict

import cv2
import numpy as np

try:
    import face_recognition
except ImportError as exc:
    raise ImportError(
        "face_recognition is required for dlib-based training. "
        "Install it with 'pip install face-recognition' after installing dlib."
    ) from exc

DATA_DIR = 'photos'
ENCODINGS_FILE = 'face_encodings.pkl'
LABELS_FILE = 'face_labels.json'
MIN_IMAGES_PER_STUDENT = 5
EVALUATION_TOLERANCE = 0.45


def parse_student_info(filename):
    name, _ = os.path.splitext(os.path.basename(filename))
    parts = name.split('_')
    if len(parts) < 2:
        return None, None

    try:
        student_id = int(parts[0])
    except ValueError:
        return None, None

    if len(parts) >= 3 and parts[-1].isdigit():
        student_name = '_'.join(parts[1:-1])
    else:
        student_name = '_'.join(parts[1:])

    return student_id, student_name


def load_images():
    encodings = []
    labels = []
    student_names = {}
    counts = defaultdict(int)

    pattern = os.path.join(DATA_DIR, '*.*')
    for path in sorted(glob.glob(pattern)):
        if not path.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        student_id, student_name = parse_student_info(path)
        if student_id is None or not student_name:
            print(f"⚠️  Skipping invalid filename: {path}")
            continue

        image = cv2.imread(path)
        if image is None:
            print(f"⚠️  Cannot read image: {path}")
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb, model='hog')
        if not face_locations:
            print(f"⚠️  No face found in image: {path}")
            continue

        face_encodings = face_recognition.face_encodings(rgb, face_locations)
        if not face_encodings:
            print(f"⚠️  Unable to encode face in image: {path}")
            continue

        encoding = face_encodings[0]
        encodings.append(encoding)
        labels.append(student_id)
        counts[student_id] += 1
        student_names[student_id] = student_name
        print(f"✅ Loaded {path} (ID={student_id}, Name={student_name})")

    return encodings, labels, student_names, counts


def evaluate_embeddings(encodings, labels):
    if len(encodings) < 2:
        return 0.0, 0, len(encodings)

    encodings_arr = np.vstack(encodings)
    labels_arr = np.array(labels, dtype=int)
    correct = 0

    for idx, encoding in enumerate(encodings_arr):
        distances = np.linalg.norm(encodings_arr - encoding, axis=1)
        distances[idx] = np.inf
        nearest = np.argmin(distances)
        predicted = labels_arr[nearest]
        if predicted == labels_arr[idx] and distances[nearest] < EVALUATION_TOLERANCE:
            correct += 1

    accuracy = correct / len(encodings_arr) * 100.0 if encodings_arr.size else 0.0
    return accuracy, correct, len(encodings_arr)


def main():
    print('\n' + '=' * 60)
    print('📘 DLIB FACE EMBEDDING TRAINING')
    print('=' * 60)

    if not os.path.isdir(DATA_DIR):
        raise FileNotFoundError(f"Dataset directory '{DATA_DIR}' not found.")

    encodings, labels, student_names, counts = load_images()

    if not encodings:
        print('❌ No valid face encodings were generated. Check your photo dataset.')
        sys.exit(1)

    print(f'\n✅ Encodings created: {len(encodings)} images from {len(student_names)} students.')
    for sid, count in sorted(counts.items()):
        note = ''
        if count < MIN_IMAGES_PER_STUDENT:
            note = ' ⚠️ Add more images for this student.'
        print(f'   • ID {sid}: {student_names[sid]} — {count} images{note}')

    print('\n🔎 Evaluating nearest-neighbor accuracy on the same dataset...')
    accuracy, correct, total = evaluate_embeddings(encodings, labels)
    print(f'   • Matched samples: {correct}/{total}')
    print(f'   • Approximate embedding accuracy: {accuracy:.2f}%')

    with open(ENCODINGS_FILE, 'wb') as f:
        pickle.dump({'encodings': encodings, 'labels': labels}, f)

    with open(LABELS_FILE, 'w', encoding='utf-8') as f:
        json.dump({str(k): v for k, v in student_names.items()}, f, indent=2)

    print(f'\n✅ Saved encodings to {ENCODINGS_FILE}')
    print(f'✅ Saved student mapping to {LABELS_FILE}')
    if accuracy < 80.0:
        print('⚠️  Accuracy is still low. Add more images, improve lighting, and capture varied poses.')
    else:
        print('🎉 Great! Embeddings appear reasonable for this dataset.')


if __name__ == '__main__':
    main()
