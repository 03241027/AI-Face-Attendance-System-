"""
Real-time face recognition using dlib embeddings.
Requires: face_recognition, dlib, opencv-python, numpy
Usage: python recognize_dlib.py
"""
import json
import os
import pickle

import cv2
import numpy as np

try:
    import face_recognition
except ImportError as exc:
    raise ImportError(
        "face_recognition is required for recognition. "
        "Install it with 'pip install face-recognition' after installing dlib."
    ) from exc

ENCODINGS_FILE = 'face_encodings.pkl'
LABELS_FILE = 'face_labels.json'
MATCH_THRESHOLD = 0.45


def load_models():
    if not os.path.exists(ENCODINGS_FILE) or not os.path.exists(LABELS_FILE):
        raise FileNotFoundError(
            'Required files not found. Run train_dlib_model.py first.'
        )

    with open(ENCODINGS_FILE, 'rb') as f:
        data = pickle.load(f)

    with open(LABELS_FILE, 'r', encoding='utf-8') as f:
        student_names = json.load(f)

    encodings = np.array(data['encodings'])
    labels = np.array(data['labels'], dtype=int)

    return encodings, labels, student_names


def get_name_for_label(label, student_names):
    return student_names.get(str(label), f'Unknown ({label})')


def main():
    print('\n' + '=' * 60)
    print('👁️  DLIB FACE RECOGNITION TEST')
    print('=' * 60)

    known_encodings, known_labels, student_names = load_models()
    print(f'✅ Loaded {len(known_encodings)} known face embeddings.')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError('Unable to open camera. Check your webcam settings.')

    print('\n📋 Press q to quit. Press c to capture a recognition frame.')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb, model='hog')
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_index = int(np.argmin(distances))
            best_distance = float(distances[best_index])
            student_id = int(known_labels[best_index])
            recognized = best_distance <= MATCH_THRESHOLD

            if recognized:
                label = get_name_for_label(student_id, student_names)
                color = (0, 255, 0)
            else:
                label = 'Unknown'
                color = (0, 0, 255)

            text = f'{label} ({best_distance:.2f})'
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow('DLIB Face Recognition', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
