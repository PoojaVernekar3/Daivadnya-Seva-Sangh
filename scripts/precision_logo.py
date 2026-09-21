import cv2
import numpy as np

cover = cv2.imread('scripts/cover_300dpi.png')
abs_cX, abs_cY = 358, 350
r = 250 # The actual emblem radius is ~220-250 pixels, not 369

# Pad cover by 100 pixels with reflection or black border just in case
padded = cv2.copyMakeBorder(cover, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[0, 0, 0])
p_cX, p_cY = abs_cX + 100, abs_cY + 100

box = padded[p_cY - r : p_cY + r, p_cX - r : p_cX + r]
print("Box shape:", box.shape)

rgba = cv2.cvtColor(box, cv2.COLOR_BGR2BGRA)
bh, bw = rgba.shape[:2]

Y, X = np.ogrid[:bh, :bw]
dist = np.sqrt((X - bw/2)**2 + (Y - bh/2)**2)

feather_w = 6.0
alpha = np.clip((r - dist) / feather_w, 0, 1)

brightness = np.mean(box, axis=2)
outer_mask = dist > (0.75 * r)
dark_fade = np.clip((brightness - 25) / 40.0, 0, 1)

combined_alpha = alpha.copy()
combined_alpha[outer_mask] = np.minimum(combined_alpha[outer_mask], dark_fade[outer_mask])
rgba[:, :, 3] = (combined_alpha * 255).astype(np.uint8)

cv2.imwrite('assets/logo_clean_hq.png', rgba)
print("Saved assets/logo_clean_hq.png successfully! Shape:", rgba.shape)
