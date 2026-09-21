import cv2
import numpy as np
from PIL import Image

crop = cv2.imread('scripts/contour_crop.png')
h, w = crop.shape[:2]
print(f"Crop: {w}x{h}")

# The contour crop has the orange brush circle with white Marathi calligraphy and Ganesha motif.
# Outside the circle is the black background of the cover page.
# Let's create an alpha channel where:
# - The inside of the circular brush is 100% opaque.
# - The outer dark background outside the brush circle is completely transparent (alpha = 0).
# Let's find the circle center (cx, cy) and radius (r):

# Distance transform from dark background or center of mass of orange circle
hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (8, 60, 60), (35, 255, 255))

M = cv2.moments(mask)
cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])
print(f"Exact center: ({cx}, {cy})")

# Let's find radius:
y_idxs, x_idxs = np.where(mask > 0)
dists = np.sqrt((x_idxs - cx)**2 + (y_idxs - cy)**2)
r = int(np.percentile(dists, 99.5))
print(f"Radius: {r}")

# Let's pad crop if needed to make cx, cy exactly the image center:
size = max(cx, cy, w - cx, h - cy) + 10
canvas = np.zeros((size * 2, size * 2, 4), dtype=np.uint8)

# Center the crop
dx = size - cx
dy = size - cy
# Paste crop into canvas
for y in range(h):
    for x in range(w):
        canvas[y + dy, x + dx, :3] = crop[y, x]

# Create circular mask centered at (size, size) with radius r
Y, X = np.ogrid[:size*2, :size*2]
dist_from_c = np.sqrt((X - size)**2 + (Y - size)**2)

# Inside r-3: alpha 255, between r-3 and r+1: smooth feather, outside r+1: alpha 0
alpha = np.clip((r + 1 - dist_from_c) / 3.0, 0, 1)

# Also check for dark pixels in the outer ring (r*0.8 to r) so that any dark background doesn't get preserved
brightness = np.mean(canvas[:, :, :3], axis=2)
outer_zone = dist_from_c > (r * 0.85)
dark_pixels = outer_zone & (brightness < 40)
alpha[dark_pixels] = 0

canvas[:, :, 3] = (alpha * 255).astype(np.uint8)

# Crop to tight bounding box around the circle
side = r + 4
final_logo = canvas[size - side : size + side, size - side : size + side]

cv2.imwrite('assets/logo_pristine.png', final_logo)
print(f"Saved assets/logo_pristine.png shape={final_logo.shape}")

# Resize to standard sizes: 512x512, 256x256, 128x128
im_pristine = Image.fromarray(cv2.cvtColor(final_logo, cv2.COLOR_BGRA2RGBA))
im_512 = im_pristine.resize((512, 512), Image.Resampling.LANCZOS)
im_512.save('assets/logo.png')
print("Saved assets/logo.png at 512x512 crisp resolution!")
