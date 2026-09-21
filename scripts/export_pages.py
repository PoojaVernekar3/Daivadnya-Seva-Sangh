import os
import sys
import time
import pymupdf

pdf_path = os.path.join("assets", "Aahawal Full PS.pdf")
pages_dir = os.path.join("assets", "pages")
thumbs_dir = os.path.join("assets", "thumbnails")

os.makedirs(pages_dir, exist_ok=True)
os.makedirs(thumbs_dir, exist_ok=True)

if not os.path.exists(pdf_path):
    print(f"Error: PDF not found at {pdf_path}")
    sys.exit(1)

doc = pymupdf.open(pdf_path)
total_pages = len(doc)
print(f"Starting export of {total_pages} pages from '{pdf_path}'...")

t0 = time.time()

# Page render settings
# DPI 120 gives ~880x1180 which is razor-sharp for screen reading
# DPI 28 gives ~200x270 for fast thumbnail grid
page_dpi = 120
thumb_dpi = 28

for idx in range(total_pages):
    page_num = idx + 1
    page = doc[idx]
    
    page_img_path = os.path.join(pages_dir, f"page_{page_num:03d}.jpg")
    thumb_img_path = os.path.join(thumbs_dir, f"thumb_{page_num:03d}.jpg")
    
    # Render main page if not exists
    if not os.path.exists(page_img_path):
        pix = page.get_pixmap(dpi=page_dpi)
        # Ensure RGB (convert if CMYK or with alpha)
        if pix.alpha or pix.colorspace.name != "DeviceRGB":
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        pix.save(page_img_path, jpg_quality=85)
    
    # Render thumbnail if not exists
    if not os.path.exists(thumb_img_path):
        thumb_pix = page.get_pixmap(dpi=thumb_dpi)
        if thumb_pix.alpha or thumb_pix.colorspace.name != "DeviceRGB":
            thumb_pix = pymupdf.Pixmap(pymupdf.csRGB, thumb_pix)
        thumb_pix.save(thumb_img_path, jpg_quality=75)
    
    if page_num % 20 == 0 or page_num == total_pages:
        elapsed = time.time() - t0
        rate = page_num / elapsed if elapsed > 0 else 0
        print(f"Processed {page_num}/{total_pages} pages ({page_num*100//total_pages}%) - {rate:.1f} pages/sec")

total_time = time.time() - t0
print(f"Successfully exported {total_pages} pages and thumbnails in {total_time:.1f} seconds!")
