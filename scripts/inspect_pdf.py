import pymupdf

doc = pymupdf.open('assets/Aahawal Full PS.pdf')
print(f"Total pages: {len(doc)}")

for i in range(min(10, len(doc))):
    page = doc[i]
    images = page.get_images()
    if images:
        xref = images[0][0]
        info = doc.extract_image(xref)
        print(f"Page {i+1}: ext={info['ext']}, w={info['width']}, h={info['height']}, size_kb={len(info['image']) // 1024}")
    else:
        print(f"Page {i+1}: no images, rect={page.rect}")
