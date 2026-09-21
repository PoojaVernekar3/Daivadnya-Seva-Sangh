import cv2
import numpy as np
from PIL import Image

cover = cv2.imread('scripts/cover_300dpi.png')
# Let's inspect where in cover the text or logo is
# Let's search with user's uploaded logo at multiple scales
user = cv2.imread('assets/logo_uploaded.png')
user_gray = cv2.cvtColor(user, cv2.COLOR_BGR2GRAY)
cover_gray = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)

res = cv2.matchTemplate(cover_gray, cv2.resize(user_gray, (300, 330)), cv2.TM_CCOEFF_NORMED)
min_v, max_v, min_l, max_l = cv2.minMaxLoc(res)
print(f"Match 2x: max_v={max_v:.3f} at {max_l}")

# If match is good (> 0.7), let's crop high-res 400x400
if max_v > 0.6:
    x, y = max_l
    crop_hq = cover[y:y+330, x:x+300]
    cv2.imwrite('assets/logo_hq.png', crop_hq)
    print("Saved assets/logo_hq.png")
