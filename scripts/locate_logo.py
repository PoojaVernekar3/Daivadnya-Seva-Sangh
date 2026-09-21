import cv2
import numpy as np
from PIL import Image

# Read cover and user logo
cover = cv2.imread('scripts/cover_300dpi.png')
user_img = cv2.imread(r'C:\Users\pooja\.gemini\antigravity-ide\brain\44e24a14-13ce-4428-91ad-5135c9fec645\.user_uploaded\media_1789977153880.png')

print("Cover shape:", cover.shape)
print("User img shape:", user_img.shape)

# Let's see where the logo is located on the cover.
# Let's save a resized version or find match
h_user, w_user = user_img.shape[:2]
# Template matching with multi-scale
gray_cover = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
gray_user = cv2.cvtColor(user_img, cv2.COLOR_BGR2GRAY)

best_val = -1
best_loc = None
best_scale = 1.0

for scale in np.linspace(2.0, 7.0, 30):
    resized_user = cv2.resize(gray_user, (int(w_user * scale), int(h_user * scale)))
    if resized_user.shape[0] > gray_cover.shape[0] or resized_user.shape[1] > gray_cover.shape[1]:
        continue
    res = cv2.matchTemplate(gray_cover, resized_user, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > best_val:
        best_val = max_val
        best_loc = max_loc
        best_scale = scale

print(f"Best match: score={best_val:.3f}, loc={best_loc}, scale={best_scale:.2f}")

if best_loc:
    x, y = best_loc
    w = int(w_user * best_scale)
    h = int(h_user * best_scale)
    cropped = cover[y:y+h, x:x+w]
    cv2.imwrite('assets/logo_raw_crop.png', cropped)
    print(f"Cropped raw logo: {w}x{h} saved to assets/logo_raw_crop.png")
