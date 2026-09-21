from PIL import Image, ImageDraw
import numpy as np

# Load user original image
user_img = Image.open('assets/logo_uploaded.png').convert('RGBA')
w, h = user_img.size

# The medallion center is at cx=74, cy=92, with radius around 68
cx, cy = 74, 92
r = 68

# Create a clean circular cut centered on the medallion
# Feather radius: 2 pixels
mask = Image.new('L', (w, h), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)

# Crop to the medallion square
crop_box = (cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2)
# Make transparent outside circle
clean_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
clean_img.paste(user_img, (0, 0), mask=mask)
circular_logo = clean_img.crop(crop_box)
circular_logo.save('assets/logo_circle.png')
print("Saved assets/logo_circle.png:", circular_logo.size)

# Also let's keep the user's full uploaded image centered
# By padding top/left so cx and cy are right at the center:
target_cx = max(cx, w - cx)
target_cy = max(cy, h - cy)
side = max(target_cx, target_cy) * 2

centered_full = Image.new('RGBA', (side, side), (0, 0, 0, 0))
centered_full.paste(user_img, (side // 2 - cx, side // 2 - cy))
centered_full.save('assets/logo_centered.png')
print("Saved assets/logo_centered.png:", centered_full.size)

# Also copy circular_logo to assets/logo.png as default
circular_logo.save('assets/logo.png')
print("Saved assets/logo.png successfully!")
