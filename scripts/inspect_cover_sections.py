import cv2
import matplotlib.pyplot as plt

cover = cv2.imread('scripts/cover_300dpi.png')
h, w = cover.shape[:2]
print(f"Cover 300DPI size: {w}x{h}")

# The user uploaded: media_1789977153880.png
# Let's see: on cover, what is at the top, center, bottom?
# Let's save 4 quadrants or sections:
cv2.imwrite('scripts/cover_top.png', cover[0:int(h*0.35), :])
cv2.imwrite('scripts/cover_mid.png', cover[int(h*0.35):int(h*0.7), :])
cv2.imwrite('scripts/cover_bottom.png', cover[int(h*0.7):, :])
print("Saved cover sections")
