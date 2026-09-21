import os
import pymupdf

# Let's inspect some pages around 17-35, 180-196 to see committee lists, accounts, etc.
doc = pymupdf.open("assets/Aahawal Full PS.pdf")

pages_to_check = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 180, 185, 190, 191, 192, 193, 194, 195]

for pno in pages_to_check:
    pix = doc[pno].get_pixmap(dpi=50)
    pix.save(f"assets/thumbnails/temp_{pno+1:03d}.jpg")

print("Rendered check pages.")
