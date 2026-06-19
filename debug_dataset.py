import os
from collections import Counter

photos = [f for f in os.listdir('photos') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
print('photo count', len(photos))
counts = Counter(p.split('_')[0] for p in photos)
for sid, count in sorted(counts.items(), key=lambda x: int(x[0])):
    print(sid, count)
