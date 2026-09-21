import os
import re
import json
import time
from multiprocessing import Pool, cpu_count
from rapidocr_onnxruntime import RapidOCR

# Global engine per worker process
ocr_engine = None

def init_worker():
    global ocr_engine
    ocr_engine = RapidOCR()

def process_page(page_num):
    global ocr_engine
    img_path = os.path.join("assets", "pages", f"page_{page_num:03d}.jpg")
    thumb_path = os.path.join("assets", "thumbnails", f"thumb_{page_num:03d}.jpg")
    
    if not os.path.exists(img_path):
        return None
    
    try:
        results, _ = ocr_engine(img_path)
    except Exception as e:
        print(f"Error processing page {page_num}: {e}")
        return None
    
    lines = []
    if results:
        for box, text, score in results:
            t = text.strip()
            if t and score > 0.4:
                lines.append(t)
    
    raw_text = " ".join(lines)
    
    # Extract phone numbers
    phones = re.findall(r'(?:\+?91[\s-]?)?[6-9]\d{9}|\b\d{5}[-\s]?\d{5}\b|\b0831[-\s]?\d{6,7}\b', raw_text)
    clean_phones = list(dict.fromkeys([p.replace(" ", "").replace("-", "") for p in phones]))
    
    # Extract candidate title / brand (look at first 4 non-trivial lines)
    candidate_names = []
    for line in lines[:6]:
        if len(line) >= 3 and not re.match(r'^(page|\d+|श्री|with best|compliments|cell|mob|ph)', line, re.I):
            candidate_names.append(line)
    
    brand_name = candidate_names[0] if candidate_names else f"Page {page_num} Sponsor"
    
    # Determine category based on keywords
    text_lower = raw_text.lower()
    category = "General"
    if any(k in text_lower for k in ["gold", "jewel", "silver", "chain", "ornament", "दागिने", "सोने", "सोनार", "सराफ"]):
        category = "Jewellery & Gold"
    elif any(k in text_lower for k in ["loan", "finance", "तारण", "कर्ज", "बँक"]):
        category = "Banking & Gold Loan"
    elif any(k in text_lower for k in ["karyalaya", "hall", "मंगळ", "कार्यालय"]):
        category = "Community Halls"
    elif any(k in text_lower for k in ["pharma", "chem", "industry", "ltd", "works", "factory"]):
        category = "Pharma & Industry"
    elif any(k in text_lower for k in ["motor", "auto", "enfield", "bike", "car"]):
        category = "Automobile"
    elif any(k in text_lower for k in ["swamiji", "mahila", "committee", "schedule", "कार्यक्रम", "पूजा", "committee"]):
        category = "Patrons & Blessings"
    
    # Extract location snippet
    loc_match = re.search(r'([A-Za-z0-9\s,\.-]+(?:Shahapur|Belagavi|Belgaum|Vadgaon|Tilakwadi|Galli|Street|Road)[A-Za-z0-9\s,\.-]*)', raw_text, re.I)
    location = loc_match.group(1).strip()[:70] if loc_match else "Shahapur / Belagavi"
    
    return {
        "pageNumber": page_num,
        "name": brand_name,
        "category": category,
        "lines": lines,
        "rawText": raw_text,
        "phone": clean_phones[0] if clean_phones else "",
        "allPhones": clean_phones,
        "location": location,
        "thumbnail": thumb_path.replace("\\", "/"),
        "image": img_path.replace("\\", "/")
    }

def main():
    total_pages = 196
    num_workers = min(8, cpu_count())
    print(f"Starting OCR on {total_pages} pages using {num_workers} parallel workers...")
    
    t0 = time.time()
    page_numbers = list(range(1, total_pages + 1))
    
    with Pool(processes=num_workers, initializer=init_worker) as pool:
        results = pool.map(process_page, page_numbers)
    
    valid_results = [r for r in results if r is not None]
    
    os.makedirs("data", exist_ok=True)
    with open("data/ocr_index.json", "w", encoding="utf-8") as f:
        json.dump(valid_results, f, ensure_ascii=False, indent=2)
    
    elapsed = time.time() - t0
    print(f"Finished OCR on {len(valid_results)} pages in {elapsed:.1f}s ({len(valid_results)/elapsed:.2f} pages/sec)!")

if __name__ == "__main__":
    main()
