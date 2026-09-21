import pymupdf
from PIL import Image

doc = pymupdf.open(r'c:\xampp\htdocs\Haval ad\assets\Aahawal Full PS.pdf')

for p_num in [0, 1, 2, 3, 91, 195]:
    page = doc[p_num]
    pix = page.get_pixmap(dpi=150)
    pix.save(f'scripts/page_{p_num+1}_150dpi.png')
    print(f"Saved page {p_num+1}")
