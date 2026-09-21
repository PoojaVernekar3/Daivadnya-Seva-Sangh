import pymupdf
import cv2
import numpy as np

# Open PDF
doc = pymupdf.open(r'c:\xampp\htdocs\Haval ad\assets\Aahawal Full PS.pdf')
user = cv2.imread('assets/logo_uploaded.png')
user_gray = cv2.resize(cv2.cvtColor(user, cv2.COLOR_BGR2GRAY), (100, 110))

print(f"Total pages: {len(doc)}")

# Check first 15 pages and last 5 pages
pages_to_check = list(range(0, 15)) + list(range(len(doc)-5, len(doc)))

best_match = (0, -1, None)

for p_num in range(len(doc)):
    # Render at 100 dpi
    page = doc[p_num]
    pix = page.get_pixmap(dpi=100)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Template match
    res = cv2.matchTemplate(gray, user_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > best_match[1]:
        best_match = (p_num, max_val, max_loc)
        print(f"New best match: Page {p_num + 1} (0-idx {p_num}) with score {max_val:.3f} at {max_loc}")

print(f"\nFinal Best match: Page {best_match[0] + 1} with score {best_match[1]:.3f}")
