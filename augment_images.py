"""
Simple augmentation script to expand the `photos/` dataset from single images.
Saves augmented grayscale images back into `photos/` with suffix `_augN`.
Usage: python augment_images.py --count 15
"""
import cv2
import os
import argparse
import random
import shutil
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--count', type=int, default=15, help='augmentations per image')
parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--output', type=str, default='photos_aug', help='output folder for augmented images')
args = parser.parse_args()

random.seed(args.seed)
np.random.seed(args.seed)

SRC_DIR = 'photos'
OUT_DIR = args.output

if not os.path.isdir(SRC_DIR):
    raise SystemExit(f"Photos directory '{SRC_DIR}' not found")

os.makedirs(OUT_DIR, exist_ok=True)

files = [f for f in os.listdir(SRC_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
print(f'Found {len(files)} images; creating up to {args.count} augmentations each in {OUT_DIR}')

def random_transform(img):
    # img: grayscale numpy array
    h, w = img.shape[:2]
    out = img.copy()

    # Random flip
    if random.random() < 0.5:
        out = cv2.flip(out, 1)

    # Rotation
    angle = random.uniform(-15, 15)
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
    out = cv2.warpAffine(out, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

    # Random scale and crop
    if random.random() < 0.5:
        scale = random.uniform(0.9, 1.1)
        nw, nh = int(w*scale), int(h*scale)
        out = cv2.resize(out, (nw, nh))
        # center-crop or pad
        if nw > w:
            sx = (nw - w)//2
            out = out[sx:sx+w, sx:sx+w]
        else:
            pad_w = (w - nw)//2
            pad_h = (h - nh)//2
            out = cv2.copyMakeBorder(out, pad_h, h-nh-pad_h, pad_w, w-nw-pad_w, cv2.BORDER_REPLICATE)

    # Brightness / contrast
    if random.random() < 0.8:
        alpha = random.uniform(0.8, 1.2)  # contrast
        beta = random.uniform(-20, 20)    # brightness
        out = cv2.convertScaleAbs(out, alpha=alpha, beta=beta)

    # Gaussian blur
    if random.random() < 0.2:
        k = random.choice([3,5])
        out = cv2.GaussianBlur(out, (k,k), 0)

    # Add small noise
    if random.random() < 0.3:
        noise = np.random.normal(0, 5, out.shape).astype(np.int16)
        out = np.clip(out.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Equalize
    out = cv2.equalizeHist(out)
    out = cv2.resize(out, (200,200))
    return out

created = 0
for fname in files:
    base, ext = os.path.splitext(fname)
    # Use only original files, not previously generated augmentations
    if '_aug' in base:
        continue
    src_path = os.path.join(SRC_DIR, fname)
    img = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('skip', fname)
        continue

    shutil.copy2(src_path, os.path.join(OUT_DIR, fname))
    for i in range(args.count):
        out = random_transform(img)
        out_name = f"{base}_aug{i+1}{ext}"
        out_path = os.path.join(OUT_DIR, out_name)
        if os.path.exists(out_path):
            continue
        cv2.imwrite(out_path, out)
        created += 1
    print(f'Augmented {fname} -> {args.count} images')

print(f'Total augmented images created: {created}')
