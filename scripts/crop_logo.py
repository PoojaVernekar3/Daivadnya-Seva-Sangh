import pymupdf
from PIL import Image
import numpy as np

# Load user's uploaded logo to see its features
user_img = Image.open(r'C:\Users\pooja\.gemini\antigravity-ide\brain\44e24a14-13ce-4428-91ad-5135c9fec645\.user_uploaded\media_1789977153880.png')
print('User logo size:', user_img.size)

# Let's inspect page 0 (cover) rendered at 300 DPI or higher to locate this exact circular logo
doc = pymupdf.open(r'c:\xampp\htdocs\Haval ad\assets\Aahawal Full PS.pdf')
page0 = doc[0]
pix = page0.get_pixmap(dpi=300)
pix.save('scripts/cover_300dpi.png')
print('Rendered cover 300dpi:', pix.width, pix.height)
