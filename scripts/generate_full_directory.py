import json
import re

with open("data/ocr_index.json", "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

print(f"Loaded {len(ocr_data)} pages from OCR index.")

mandal_config = """/**
 * Official Book & Website Data for
 * Daivadnya Seva Sangh, Shree Ganesh Utsav Mandal, Shahapur - Belgaum
 * 47th Ahawal 2026-27 (४७ वा वार्षिक अहवाल २०२६-२७)
 */

const MANDAL_CONFIG = {
  officialName: "Daivadnya Seva Sangh, Shree Ganesh Utsav Mandal, Shahapur - Belgaum",
  marathiName: "दैवज्ञ सेवा संघ, श्री गणेश उत्सव मंडळ, शहापूर-बेळगांव",
  shortName: "DSS Shree Ganesh Utsav Mandal",
  city: "Shahapur, Belagavi",
  state: "Karnataka",
  pincode: "590003",
  celebrationYear: "47th Ahawal 2026-27 (४७ वा अहवाल २०२६-२७)",
  festivalDates: "14th Sept 2026 to 27th Sept 2026",
  editionText: "वार्षिक अहवाल स्मरणिका व जाहिरात पुस्तिका (Digital Hawal Souvenir)",
  browserTitle: "Daivadnya Seva Sangh, Shree Ganesh Utsav Mandal, Shahapur - Belgaum | 47th Ahawal 2026-27",
  shareTitle: "Daivadnya Seva Sangh, Shree Ganesh Utsav Mandal, Shahapur - Belgaum – 47th Ahawal Book",
  shareDescription: "Explore the official 196-page 47th Ahawal (२०२६-२७) Souvenir Book of Daivadnya Seva Sangh, Shree Ganesh Utsav Mandal, Shahapur-Belgaum.",
  pdfPath: "assets/Aahawal Full PS.pdf",
  pdfDownloadName: "Daivadnya_Seva_Sangh_Shahapur_47th_Ahawal_2026-27.pdf",
  totalPages: 196,
  leadership: {
    president: "Sri Manoj Deepak Kolvekar (President, Shree Ganesh Utsav Mandal)",
    secretary: "Sri Sudhir Surendra Vernekar (Secretary, Shree Ganesh Utsav Mandal)",
    sanghPresident: "Sri Dayanand Ganapati Netalkar (President, Daivadnya Seva Sangh)",
    sanghSecretary: "Sri Manjunath Shankar Shet (Secretary, Daivadnya Seva Sangh)",
    sanghTreasurer: "Sri Bhushan Prakash Revankar (Treasurer, Daivadnya Seva Sangh)"
  },
  contactEmail: "info@daivadnyasevasangh.org",
  contactPhone: "+91 831 356 6962",
  address: "Daivadnya Mangala Karyalaya, Mahatma Phule Road, Shahapur, Belagavi - 590003"
};
"""

curated_titles = {
    1: {"name": "दैवज्ञ सेवा संघ, श्री गणेश उत्सव मंडळ (Front Cover)", "marathi": "४७ वा अहवाल २०२६-२७ मुखपृष्ठ", "cat": "Patrons & Blessings"},
    2: {"name": "Mysore Jewellery House & S.V. Farms", "marathi": "मैसूर ज्वेलरी हाऊस व एस.व्ही. फार्म्स", "cat": "Jewellery & Gold", "prop": "Surendra V. Vernekar & Sudhir S. Vernekar", "loc": "1202, Saraf Galli, Shahapur, Belagavi", "phone": "9845563059"},
    3: {"name": "Anvekar Gold (अणवेकर गोल्ड)", "marathi": "सोने तारण सुलभ कर्ज (Gold Loan)", "cat": "Banking & Gold Loan", "prop": "Anvekar Gold Finance", "loc": "Shahapur, Belagavi", "phone": "8884388863"},
    4: {"name": "Paramapujya Shri Shri Swamiji Blessings", "marathi": "परमपूज्य श्री श्री स्वामीजी आशीर्वाद", "cat": "Patrons & Blessings", "prop": "Shri Shri Sachidanand Gyaneshwar Bharati Maha Swamiji", "loc": "Swamiji Peetha"},
    5: {"name": "Vinayak Hanmanth Kudtarkar Wholesalers", "marathi": "विनायक हनुमंत कुडतरकर (Gold Wholesaler)", "cat": "Jewellery & Gold", "prop": "Vinayak H. Kudtarkar", "loc": "H. No. 358, Om Nagar, Belagavi", "phone": "9945423885"},
    6: {"name": "Vadiraja Tirtha & Lord Hayagriva", "marathi": "श्री वादिराज तीर्थ व हयग्रीव महात्म्य", "cat": "Patrons & Blessings"},
    7: {"name": "R.K. & R.K. Anavekar Jewellers", "marathi": "आर.के. अँड आर.के. अणवेकर ज्वेलर्स", "cat": "Jewellery & Gold", "prop": "Anavekar Jewellers", "loc": "Kalyani, K.R. Street, Bharat Nagar, Shahapur", "phone": "9900092711"},
    8: {"name": "Laxmi Gold (Ashok & Aniket Vernekar)", "marathi": "लक्ष्मी गोल्ड - सोन्याचे दागिने व चेन्स", "cat": "Jewellery & Gold", "prop": "Ashok Vernekar & Aniket Vernekar", "loc": "Navdurga Tower, Dane Galli, Shahapur", "phone": "9845439427"},
    9: {"name": "Shree Balaji Tar Pasta", "marathi": "श्री बालाजी तार पास्ता (वडगाव)", "cat": "Jewellery & Gold", "prop": "Dinesh Vaishnav & Anil Vaishnav", "loc": "H.No. 553/1, Datta Galli, Vadgaon, Belagavi", "phone": "9686199765"},
    10: {"name": "Shri Mahalaxmi Divine Reading / Kolvekar", "marathi": "श्री महालक्ष्मी डिव्हाईन रीडिंग (टॅरो कार्ड)", "cat": "Patrons & Blessings", "prop": "Veena Manoj Kolvekar & Deepak Kolvekar", "loc": "Jed Galli, Shahapur / Tilakwadi", "phone": "9035594395"},
    11: {"name": "President Address - Sri Manoj Deepak Kolvekar", "marathi": "अध्यक्षांचे मनोगत - श्री मनोज दीपक कोलवेकर", "cat": "Patrons & Blessings"},
    12: {"name": "Secretary Address - Sri Sudhir Surendra Vernekar", "marathi": "सचिवांचे मनोगत - श्री सुधीर सुरेंद्र वेर्णेकर", "cat": "Patrons & Blessings"},
    13: {"name": "Shree Ganesh Utsav Programs 2026 (Schedule Day 1-7)", "marathi": "श्री गणेश उत्सव कार्यक्रम २०२६ (इंग्रजी १-७)", "cat": "Patrons & Blessings"},
    14: {"name": "Shree Ganesh Utsav Programs 2026 (Schedule Day 8-12)", "marathi": "श्री गणेश उत्सव कार्यक्रम २०२६ (इंग्रजी ८-१२)", "cat": "Patrons & Blessings"},
    15: {"name": "श्री गणेश उत्सव कार्यक्रम २०२६ (मराठी दिवस १-७)", "marathi": "श्री गणेश उत्सव कार्यक्रम २०२६ (मराठी १-७)", "cat": "Patrons & Blessings"},
    16: {"name": "श्री गणेश उत्सव कार्यक्रम २०२६ (मराठी दिवस ८-१२)", "marathi": "श्री गणेश उत्सव कार्यक्रम २०२६ (मराठी ८-१२)", "cat": "Patrons & Blessings"},
    17: {"name": "ಶ್ರೀ ಗಣೇಶ ಉತ್ಸವ ಕಾರ್ಯಕ್ರಮಗಳು 2026 (ಕನ್ನಡ ದಿನ 1-7)", "marathi": "श्री गणेश उत्सव कार्यक्रम २०२६ (कन्नड १-७)", "cat": "Patrons & Blessings"},
    18: {"name": "ಶ್ರೀ ಗಣೇಶ ಉತ್ಸವ ಕಾರ್ಯಕ್ರಮಗಳು 2026 (ಕನ್ನಡ ದಿನ 8-12)", "marathi": "श्री गणेश उत्सव कार्यक्रम २०२६ (कन्नड ८-१२)", "cat": "Patrons & Blessings"},
    19: {"name": "Prize Distribution Programme - Daivadnya Seva Sangh", "marathi": "बक्षीस वितरण कार्यक्रम (English)", "cat": "Community Halls"},
    20: {"name": "बक्षीस वितरण कार्यक्रम - दैवज्ञ सेवा संघ", "marathi": "बक्षीस वितरण कार्यक्रम (मराठी)", "cat": "Community Halls"},
    21: {"name": "ಬಹುಮಾನ ವಿತರಣಾ ಕಾರ್ಯಕ್ರಮ - ದೈವಜ್ಞ ಸೇವಾ ಸಂಘ", "marathi": "बक्षीस वितरण कार्यक्रम (कन्नड)", "cat": "Community Halls"},
    22: {"name": "Motichand Jewels (Nagendra M. Pauskar)", "marathi": "मोतीचंद ज्युवेल्स (नागेंद्र एम. पावसकर)", "cat": "Jewellery & Gold", "prop": "Nagendra M. Pauskar", "loc": "Manorath Apt, Adarsh Nagar, Belagavi", "phone": "9480988593"},
    25: {"name": "Managing Committee 2026-2028 (कार्यकारी समिती)", "marathi": "दैवज्ञ सेवा संघ कार्यकारी समिती २०२६-२०२८", "cat": "Patrons & Blessings"},
    26: {"name": "Utsav 2025 Photos: Stambha Pooja & Murthi Agaman", "marathi": "उत्सव २०२५ छायाचित्रे: स्तंभ पूजा व मूर्ती आगमन", "cat": "Patrons & Blessings"},
    27: {"name": "Utsav 2025 Photos: Mahapooja & Devotees", "marathi": "उत्सव २०२५ छायाचित्रे: महापूजा", "cat": "Patrons & Blessings"},
    28: {"name": "Utsav 2025 Photos: Ganesh Murti & Dhol Group", "marathi": "उत्सव २०२५ छायाचित्रे: श्री गणेश मूर्ती व ढोल पथक", "cat": "Patrons & Blessings"},
    29: {"name": "Utsav 2025 Photos: Recipe, Rangoli & Drawing Competitions", "marathi": "उत्सव २०२५ स्पर्धा: पाककला, रांगोळी व चित्रकला", "cat": "Patrons & Blessings"},
    30: {"name": "Utsav 2025 Photos: Mehandi, Fancy Dress & Dance Show", "marathi": "उत्सव २०२५ स्पर्धा: मेहंदी, फॅन्सी ड्रेस व नृत्य", "cat": "Patrons & Blessings"},
    31: {"name": "Utsav 2025 Photos: Natak by ISKCON & Bhajan Competition", "marathi": "उत्सव २०२५: इस्कॉन नाटक व भजन स्पर्धा", "cat": "Patrons & Blessings"},
    32: {"name": "Utsav 2025 Photos: Medical Camp (Vernekar Hospital)", "marathi": "उत्सव २०२५: मोफत आरोग्य शिबीर", "cat": "Patrons & Blessings"},
    33: {"name": "Utsav 2025 Photos: Shree Ganesh Utsav Lilav (Auction)", "marathi": "उत्सव २०२५: लिलाव कार्यक्रम", "cat": "Patrons & Blessings"},
    34: {"name": "Utsav 2025 Photos: Murti Visarjan Miravnuk (Immersion)", "marathi": "उत्सव २०२५: विसर्जन मिरवणूक", "cat": "Patrons & Blessings"},
    35: {"name": "Daivadnya Brahman Mangal Karyalaya, Shahapur", "marathi": "दैवज्ञ ब्राह्मण मंगल कार्यालय, शहापूर", "cat": "Community Halls", "prop": "Manager Satish", "loc": "Mahatma Phule Road, Shahapur, Belagavi", "phone": "7892793120"},
    36: {"name": "Daivadnya Mahila Mandal, Belagavi", "marathi": "दैवज्ञ महिला मंडळ, बेळगाव (पदाधिकारी)", "cat": "Patrons & Blessings"},
    117: {"name": "Shri Chowdeshwari Jewellery Works", "marathi": "श्री चौडेश्वरी ज्वेलरी वर्क्स (मंजुनाथ वेर्णेकर)", "cat": "Jewellery & Gold", "prop": "Manjunath M. Vernekar & Ganesh R. Kurdekar", "loc": "Shanta Tower, Bhoj Galli, Shahapur, Belagavi", "phone": "9945905841"},
    193: {"name": "Omkrown PharmaChem Pvt Ltd", "marathi": "ओमक्राऊन फार्माकेम प्रा. लि. (अणवेकर)", "cat": "Pharma & Industry", "prop": "Late Shri Ramakant K. Anavekar", "loc": "Kalyani, K.R. Street, Shahapur / Macche", "phone": "9448482711"},
    194: {"name": "Shri Ganesh Gold (Balaji Shinde)", "marathi": "श्री गणेश गोल्ड - चेन स्पेशालिस्ट (बाळाजी शिंदे)", "cat": "Jewellery & Gold", "prop": "Balaji Shinde", "loc": "Bhoj Galli, Shahapur, Belagavi - 590003", "phone": "7406515823"},
    195: {"name": "Shri Munishwar Motors - Royal Enfield", "marathi": "श्री मुनीश्वर मोटर्स - रॉयल एनफील्ड (लिंगराज जगजंपी)", "cat": "Automobile", "prop": "Shri Lingaraj Jagajampi", "loc": "Opp. Kavookatta, GOAVES, Belagavi", "phone": "8105282000"},
    196: {"name": "भगवान श्री गणेश संपूर्ण माहिती (Back Cover)", "marathi": "भगवान श्री गणेश संपूर्ण माहिती (Back Cover)", "cat": "Cover"}
}

def clean_text_words(text):
    return re.sub(r'[^A-Za-z0-9\u0900-\u097F\u0C80-\u0CFF\s]', ' ', text)

directory_list = []
pages_list = []

for entry in ocr_data:
    pnum = entry["pageNumber"]
    lines = entry.get("lines", [])
    raw_text = entry.get("rawText", "")
    
    # Check if curated
    if pnum in curated_titles:
        c = curated_titles[pnum]
        name = c["name"]
        marathi_name = c.get("marathi", name)
        category = c.get("cat", "Jewellery & Gold")
        proprietor = c.get("prop", "")
        location = c.get("loc", entry.get("location", "Shahapur / Belagavi"))
        phone = c.get("phone", entry.get("phone", ""))
    else:
        # Extract title from prominent lines
        title_candidates = []
        for line in lines[:8]:
            l = line.strip()
            if re.match(r'^(with|best|compliments|wishes|from|॥|\|\||shree\s+ganeshaya|om\s+gam|prop|cell|mob|ph|phone|contact|date|page|day|\d+)', l, re.I):
                continue
            if len(l) < 3 or re.match(r'^[0-9\s,\.\-/:;]+$', l):
                continue
            if re.match(r'^(saraf|galli|shahapur|belgaum|belagavi)', l, re.I):
                continue
            title_candidates.append(l)
            if len(title_candidates) >= 2:
                break
                
        if title_candidates:
            name = " ".join(title_candidates)
        else:
            name = f"Souvenir Sponsor Page {pnum}"
            
        marathi_name = name
        category = entry.get("category", "Jewellery & Gold")
        if category == "General":
            category = "Jewellery & Gold"
            
        prop_candidates = []
        for line in lines:
            if any(s in line for s in ["Vernekar", "Revankar", "Pauskar", "Anavekar", "Netalkar", "Raikar", "Shet", "Shinde", "Vaishnav", "Kurdekar", "Kudtarkar", "Bhat", "Kolvekar", "Patil"]):
                prop_candidates.append(line)
            elif re.search(r'\b(prop|owner|partner|director|er\.|ar\.|shri|smt)\b', line, re.I):
                prop_candidates.append(line)
                
        proprietor = prop_candidates[0] if prop_candidates else ""
        location = entry.get("location", "Shahapur / Belagavi")
        if len(location) < 5 or "page" in location.lower():
            location = "Shahapur / Belagavi"
        phone = entry.get("phone", "")
        
    specialty_lines = [l for l in lines if any(w in l.lower() for w in ["manufactur", "special", "dealer", "wholesal", "pure", "gold", "silver", "hallmark", "chain", "ornament", "916"])]
    tagline = specialty_lines[0] if specialty_lines else f"Official Sponsor - 47th Ahawal 2026-27 (Page {pnum})"
    
    # Build clean tags array
    search_tags = [name, marathi_name, category, proprietor, location, phone, f"Page {pnum}", f"p{pnum}"]
    for line in lines:
        if len(line) >= 3:
            search_tags.append(line)
            
    # Flipbook page object
    pages_list.append({
        "id": pnum,
        "pageNumber": pnum,
        "title": name,
        "category": category,
        "image": f"assets/pages/page_{pnum:03d}.jpg",
        "thumbnail": f"assets/thumbnails/thumb_{pnum:03d}.jpg"
    })
    
    # Directory card object
    directory_list.append({
        "id": f"adv-p{pnum}",
        "name": name,
        "marathiName": marathi_name,
        "category": category,
        "pageNumber": pnum,
        "proprietor": proprietor,
        "location": location,
        "address": location,
        "phone": phone,
        "contact": phone,
        "tagline": tagline,
        "badge": f"Page {pnum}",
        "thumbnail": f"assets/thumbnails/thumb_{pnum:03d}.jpg",
        "image": f"assets/pages/page_{pnum:03d}.jpg",
        "rawText": raw_text,
        "tags": search_tags
    })

output_js = mandal_config + "\n\nconst BOOK_PAGES = " + json.dumps(pages_list, indent=2, ensure_ascii=False) + ";\n\nconst ADVERTISERS_DATA = " + json.dumps(directory_list, indent=2, ensure_ascii=False) + ";\n\nconst ADVERTISERS_DIRECTORY = ADVERTISERS_DATA;\n"

with open("js/book-data.js", "w", encoding="utf-8") as f:
    f.write(output_js)

print("Regenerated js/book-data.js successfully with all 196 pages and rich OCR searchable directory!")
