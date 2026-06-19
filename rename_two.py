import os

os.chdir('photos')  # Go to photos folder

try:
    os.rename('Mahara.jpeg', '3_Mahara_1.jpg')
    print('✅ Renamed: Mahara.jpeg → 3_Mahara_1.jpg')
except FileNotFoundError:
    print('❌ Mahara.jpeg not found')

try:
    os.rename('Sajitha.jpeg', '25_Sajeetha_1.jpg')
    print('✅ Renamed: Sajitha.jpeg → 25_Sajeetha_1.jpg')
except FileNotFoundError:
    print('❌ Sajitha.jpeg not found')

print('\n✅ Done!')