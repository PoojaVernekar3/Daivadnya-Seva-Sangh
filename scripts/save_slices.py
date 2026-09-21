import cv2
import json

cover = cv2.imread('scripts/cover_300dpi.png')
h, w = cover.shape[:2]

# Let's crop slices of the top 1000px:
# Slices: (0 to 600, 0 to 800), (0 to 600, 700 to 1500), (0 to 600, 1400 to 2200)
cv2.imwrite('scripts/slice_top_left.png', cover[0:700, 0:800])
cv2.imwrite('scripts/slice_top_center.png', cover[0:700, 700:1500])
cv2.imwrite('scripts/slice_top_right.png', cover[0:700, 1400:2200])

# Middle slices (700 to 1600):
cv2.imwrite('scripts/slice_mid_left.png', cover[700:1600, 0:800])
cv2.imwrite('scripts/slice_mid_center.png', cover[700:1600, 700:1500])
cv2.imwrite('scripts/slice_mid_right.png', cover[700:1600, 1400:2200])

# Bottom slices (2000 to 2954):
cv2.imwrite('scripts/slice_bot_left.png', cover[2000:, 0:800])
cv2.imwrite('scripts/slice_bot_center.png', cover[2000:, 700:1500])
cv2.imwrite('scripts/slice_bot_right.png', cover[2000:, 1400:2200])

print("Saved all 9 slices!")
