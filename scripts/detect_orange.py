import cv2
import numpy as np

user = cv2.imread('assets/logo_uploaded.png')
user_hsv = cv2.cvtColor(user, cv2.COLOR_BGR2HSV)
# Average orange color in user logo:
print("User mean BGR:", cv2.mean(user))

slices = [
    'scripts/slice_top_left.png',
    'scripts/slice_top_center.png',
    'scripts/slice_top_right.png',
    'scripts/slice_mid_left.png',
    'scripts/slice_mid_center.png',
    'scripts/slice_mid_right.png',
    'scripts/slice_bot_left.png',
    'scripts/slice_bot_center.png',
    'scripts/slice_bot_right.png',
    'scripts/page_2_150dpi.png',
    'scripts/page_3_150dpi.png',
    'scripts/page_4_150dpi.png',
    'scripts/page_196_150dpi.png'
]

for s in slices:
    img = cv2.imread(s)
    if img is None:
        continue
    # Check for orange/gold pixels (H: 10-35, S: 100-255, V: 100-255)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (10, 100, 100), (30, 255, 255))
    count = cv2.countNonZero(mask)
    if count > 500:
        print(f"Slice {s}: {count} orange/gold pixels, shape={img.shape}")
