import cv2
import numpy as np

img = cv2.imread('scripts/slice_top_left.png')
print("Loaded slice_top_left.png:", img.shape)

# Let's find contours of circular objects or yellow brush
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (10, 80, 80), (30, 255, 255))

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("Found contours:", len(contours))

# Find largest contour
if contours:
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    print(f"Largest contour box: x={x}, y={y}, w={w}, h={h}")
    crop = img[y:y+h, x:x+w]
    cv2.imwrite('scripts/contour_crop.png', crop)
