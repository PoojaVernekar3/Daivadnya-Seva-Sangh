import pymupdf
import os
from PIL import Image
import io

doc = pymupdf.open(r'c:\xampp\htdocs\Haval ad\assets\Aahawal Full PS.pdf')
new_doc = pymupdf.open()

print("Optimizing PDF for GitHub 100MB limit (testing first 10 pages)...")
for i in range(10):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes("jpeg", jpg_quality=88)
    rect = page.rect
    new_page = new_doc.new_page(width=rect.width, height=rect.height)
    new_page.insert_image(rect, stream=img_bytes)

new_doc.save('scripts/test_10p.pdf', garbage=4, deflate=True)
sz = os.path.getsize('scripts/test_10p.pdf')
print(f"10 pages = {sz} bytes ({sz/1024/1024:.2f} MB)")
est_196 = (sz / 10) * 196
print(f"Estimated 196 pages = {est_196/1024/1024:.2f} MB")
