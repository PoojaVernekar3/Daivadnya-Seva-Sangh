import pymupdf
import os
import sys

src_path = r'c:\xampp\htdocs\Haval ad\assets\Aahawal Full PS.pdf'
backup_path = r'c:\xampp\htdocs\Haval ad\assets\Aahawal_Full_PS_original_backup.pdf'
out_path = r'c:\xampp\htdocs\Haval ad\assets\Aahawal_Full_PS_optimized.pdf'

if not os.path.exists(backup_path):
    print("Creating backup of original PDF...")
    import shutil
    shutil.copy2(src_path, backup_path)

doc = pymupdf.open(backup_path)
new_doc = pymupdf.open()

total_pages = len(doc)
print(f"Compressing {total_pages} pages at 150 DPI JPEG 88...")

for i in range(total_pages):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes("jpeg", jpg_quality=88)
    rect = page.rect
    new_page = new_doc.new_page(width=rect.width, height=rect.height)
    new_page.insert_image(rect, stream=img_bytes)
    if (i + 1) % 25 == 0 or (i + 1) == total_pages:
        print(f"Processed {i + 1}/{total_pages} pages...")

print("Saving optimized PDF with deflate...")
new_doc.save(out_path, garbage=4, deflate=True)
doc.close()
new_doc.close()

sz_orig = os.path.getsize(backup_path)
sz_opt = os.path.getsize(out_path)
print(f"Original size:  {sz_orig:,} bytes ({sz_orig/1024/1024:.2f} MB)")
print(f"Optimized size: {sz_opt:,} bytes ({sz_opt/1024/1024:.2f} MB)")

# Replace original with optimized
import shutil
shutil.move(out_path, src_path)
print(f"Replaced {src_path} with optimized version!")
