import cv2
import numpy as np

crop = cv2.imread('scripts/contour_crop.png')
print("Contour crop shape:", crop.shape)

# Let's inspect center and circle fit
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
# Save contour crop
cv2.imwrite('assets/logo_clean_highres.png', crop)
print("Saved assets/logo_clean_highres.png!")
