"""
Validate face recognition model accuracy.
This script trains and validates the LBPH model using a hold-out test split.
Usage: python validate_model.py
"""
import cv2
import numpy as np
import os
import random
from collections import defaultdict

DATASET_PATH = 'photos'
TEST_RATIO = 0.25
RANDOM_SEED = 42
MIN_IMAGES_PER_STUDENT = 4


def load_dataset(dataset_path):
    faces = []
    ids = []
    student_names = {}

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset folder '{dataset_path}' not found.")

    for filename in sorted(os.listdir(dataset_path)):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        path = os.path.join(dataset_path, filename)
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"⚠️  Could not read image: {filename}")
            continue

        name_part = filename.rsplit('.', 1)[0]
        parts = name_part.split('_')
        if len(parts) < 2:
            print(f"⚠️  Invalid filename format: {filename}")
            continue

        try:
            student_id = int(parts[0])
        except ValueError:
            print(f"⚠️  Invalid student ID in filename: {filename}")
            continue

        student_name = parts[1]
        faces.append(image)
        ids.append(student_id)
        student_names[student_id] = student_name

    return faces, ids, student_names


def stratified_split(ids, test_ratio, seed):
    random.seed(seed)
    indexes_by_id = defaultdict(list)
    for idx, sid in enumerate(ids):
        indexes_by_id[sid].append(idx)

    train_indexes = []
    test_indexes = []

    for sid, indexes in indexes_by_id.items():
        random.shuffle(indexes)
        n_test = max(1, int(len(indexes) * test_ratio))
        if len(indexes) - n_test < 1:
            n_test = 1
        test_indexes.extend(indexes[:n_test])
        train_indexes.extend(indexes[n_test:])

    random.shuffle(train_indexes)
    random.shuffle(test_indexes)
    return train_indexes, test_indexes


def evaluate_model(recognizer, faces, ids, test_indexes):
    correct = 0
    total = len(test_indexes)
    per_id_correct = defaultdict(int)
    per_id_total = defaultdict(int)

    for idx in test_indexes:
        face = faces[idx]
        expected_id = ids[idx]
        predicted_id, confidence = recognizer.predict(face)
        per_id_total[expected_id] += 1

        # LBPH returns lower confidence for better matches
        correct_match = predicted_id == expected_id
        if correct_match:
            correct += 1
            per_id_correct[expected_id] += 1

    accuracy = correct / total * 100 if total > 0 else 0.0
    return accuracy, correct, total, per_id_correct, per_id_total


def train_and_validate(faces, ids, train_indexes, test_indexes):
    if len(train_indexes) == 0 or len(test_indexes) == 0:
        raise ValueError('Training and test sets must both contain at least one image.')

    train_faces = [faces[i] for i in train_indexes]
    train_ids = np.array([ids[i] for i in train_indexes], dtype=np.int32)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(train_faces, train_ids)

    accuracy, correct, total, per_id_correct, per_id_total = evaluate_model(
        recognizer, faces, ids, test_indexes
    )

    return recognizer, accuracy, correct, total, per_id_correct, per_id_total


def main():
    print('\n' + '=' * 60)
    print('📊 FACE RECOGNITION VALIDATION')
    print('=' * 60)

    faces, ids, student_names = load_dataset(DATASET_PATH)
    if len(faces) == 0:
        print('❌ No images found for validation.')
        return

    print(f'✅ Loaded {len(faces)} images for {len(student_names)} students.')

    counts_by_id = defaultdict(int)
    for sid in ids:
        counts_by_id[sid] += 1

    for sid, count in counts_by_id.items():
        if count < MIN_IMAGES_PER_STUDENT:
            print(f'⚠️  Student ID {sid} has only {count} images. Add more images for better accuracy.')

    train_indexes, test_indexes = stratified_split(ids, TEST_RATIO, RANDOM_SEED)
    print(f'✅ Train images: {len(train_indexes)}')
    print(f'✅ Test images: {len(test_indexes)}')

    recognizer, accuracy, correct, total, per_id_correct, per_id_total = train_and_validate(
        faces, ids, train_indexes, test_indexes
    )

    print('\n📈 Validation results:')
    print(f'   • Correct predictions: {correct}/{total}')
    print(f'   • Accuracy: {accuracy:.2f}%')

    print('\n🔍 Per-student results:')
    for sid in sorted(per_id_total):
        student_name = student_names.get(sid, 'Unknown')
        correct_count = per_id_correct.get(sid, 0)
        total_count = per_id_total[sid]
        print(f'   • {sid} ({student_name}): {correct_count}/{total_count} = {correct_count/total_count*100:.1f}%')

    if accuracy >= 90.0:
        print('\n🎉 Great! Your model reached 90% or higher accuracy.')
    else:
        print('\n⚠️  Accuracy is below 90%. Add more images and improve lighting/pose variety to improve it.')

    recognizer.write('trainer.yml')
    print('\n✅ Updated model saved to trainer.yml')

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'\n❌ Error: {exc}')
