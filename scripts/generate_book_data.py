import json

# Define the Mandal config
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

# Categorize and title specific landmark pages
page_metadata = {
    1: {"title": "मुखपृष्ठ / Front Cover (४७ वा अहवाल)", "cat": "Cover", "section": "Cover"},
    2: {"title": "Mysore Jewellery House & S.V. Farms", "cat": "Jewellery", "section": "Advertisers"},
    3: {"title": "Anvekar Gold Loan (अणवेकर गोल्ड)", "cat": "Banking & Finance", "section": "Advertisers"},
    4: {"title": "Paramapujya Shri Shri Swamiji Blessings (ಆಶೀರ್ವಾದ)", "cat": "Devotional", "section": "Devotional"},
    5: {"title": "Vinayak Hanmanth Kudtarkar (Gold Wholesalers)", "cat": "Jewellery", "section": "Advertisers"},
    6: {"title": "Vadiraja Tirtha & Lord Hayagriva's Direct Offering", "cat": "Editorial", "section": "Editorial"},
    7: {"title": "R.K. & R.K. Anavekar Jewellers, Shahapur", "cat": "Jewellery", "section": "Advertisers"},
    8: {"title": "Laxmi Gold - Gold Chains & Ornaments", "cat": "Jewellery", "section": "Advertisers"},
    9: {"title": "Shree Balaji Tar Pasta, Vadgaon", "cat": "Jewellery", "section": "Advertisers"},
    10: {"title": "Shri Mahalaxmi Divine Reading / Kolvekar", "cat": "Patrons", "section": "Advertisers"},
    11: {"title": "President's Address - Sri Manoj Deepak Kolvekar", "cat": "Editorial", "section": "Editorial"},
    12: {"title": "Secretary's Address - Sri Sudhir Surendra Vernekar", "cat": "Editorial", "section": "Editorial"},
    13: {"title": "Shree Ganesh Utsav Programs 2026 (Schedule Day 1-7, English)", "cat": "Programme", "section": "Schedule"},
    14: {"title": "Shree Ganesh Utsav Programs 2026 (Schedule Day 8-12, English)", "cat": "Programme", "section": "Schedule"},
    15: {"title": "श्री गणेश उत्सव कार्यक्रम २०२६ (वेळापत्रक दिवस १ ते ७, मराठी)", "cat": "Programme", "section": "Schedule"},
    16: {"title": "श्री गणेश उत्सव कार्यक्रम २०२६ (वेळापत्रक दिवस ८ ते १२, मराठी)", "cat": "Programme", "section": "Schedule"},
    17: {"title": "ಶ್ರೀ ಗಣೇಶ ಉತ್ಸವ ಕಾರ್ಯಕ್ರಮಗಳು 2026 (ದಿನ 1 - 7, ಕನ್ನಡ)", "cat": "Programme", "section": "Schedule"},
    18: {"title": "ಶ್ರೀ ಗಣೇಶ ಉತ್ಸವ ಕಾರ್ಯಕ್ರಮಗಳು 2026 (ದಿನ 8 - 12, ಕನ್ನಡ)", "cat": "Programme", "section": "Schedule"},
    19: {"title": "Prize Distribution Programme - Daivadnya Seva Sangh (English)", "cat": "Hawal Report", "section": "Community Welfare"},
    20: {"title": "बक्षीस वितरण कार्यक्रम - दैवज्ञ सेवा संघ (मराठी)", "cat": "Hawal Report", "section": "Community Welfare"},
    21: {"title": "ಬಹುಮಾನ ವಿತರಣಾ ಕಾರ್ಯಕ್ರಮ - ದೈವಜ್ಞ ಸೇವಾ ಸಂಘ (ಕನ್ನಡ)", "cat": "Hawal Report", "section": "Community Welfare"},
    22: {"title": "Motichand Jewels - Wholesaler of Gold Jewellery", "cat": "Jewellery", "section": "Advertisers"},
    23: {"title": "Anvekar Jewellers / Community Sponsors", "cat": "Jewellery", "section": "Advertisers"},
    24: {"title": "Community Welfare & Sponsors", "cat": "Patrons", "section": "Advertisers"},
    25: {"title": "Managing Committee 2026-2028 (कार्यकारी समिती)", "cat": "Committee", "section": "Committee"},
    26: {"title": "Utsav 2025 Photos: Stambha Pooja & Murthi Agaman", "cat": "Gallery", "section": "Photo Gallery"},
    27: {"title": "Utsav 2025 Photos: Mahapooja & Devotees", "cat": "Gallery", "section": "Photo Gallery"},
    28: {"title": "Utsav 2025 Photos: Ganesh Murti & Dhol Group", "cat": "Gallery", "section": "Photo Gallery"},
    29: {"title": "Utsav 2025 Photos: Recipe, Rangoli & Drawing Competitions", "cat": "Gallery", "section": "Photo Gallery"},
    30: {"title": "Utsav 2025 Photos: Mehandi, Fancy Dress & Dance Show", "cat": "Gallery", "section": "Photo Gallery"},
    31: {"title": "Utsav 2025 Photos: Natak by ISKCON & Bhajan Competition", "cat": "Gallery", "section": "Photo Gallery"},
    32: {"title": "Utsav 2025 Photos: Medical Camp (Vernekar Hospital)", "cat": "Gallery", "section": "Photo Gallery"},
    33: {"title": "Utsav 2025 Photos: Shree Ganesh Utsav Lilav (Auction)", "cat": "Gallery", "section": "Photo Gallery"},
    34: {"title": "Utsav 2025 Photos: Murti Visarjan Miravnuk (Immersion)", "cat": "Gallery", "section": "Photo Gallery"},
    35: {"title": "Daivadnya Brahman Mangal Karyalaya, Shahapur", "cat": "Community Hall", "section": "Community Hall"},
    36: {"title": "Daivadnya Mahila Mandal Belagavi - Office Bearers", "cat": "Committee", "section": "Committee"},
    191: {"title": "Special Community Sponsors & Benefactors", "cat": "Patrons", "section": "Advertisers"},
    192: {"title": "Shree Ganesh Gold & Silver Works", "cat": "Jewellery", "section": "Advertisers"},
    193: {"title": "Omkrown PharmaChem Pvt Ltd (Late Shri Ramakant K. Anavekar)", "cat": "Industries", "section": "Advertisers"},
    194: {"title": "Shri Ganesh Gold - Trilling & Machine Chains, Balaji Shinde", "cat": "Jewellery", "section": "Advertisers"},
    195: {"title": "Shri Munishwar Motors - Royal Enfield (Lingaraj Jagajampi)", "cat": "Automobile", "section": "Advertisers"},
    196: {"title": "अंतिम मुखपृष्ठ / Back Cover: भगवान श्री गणेश संपूर्ण माहिती", "cat": "Cover", "section": "Back Cover"}
}

# Generate 196 pages
pages = []
for p in range(1, 197):
    meta = page_metadata.get(p)
    if meta:
        title = meta["title"]
        cat = meta["cat"]
        section = meta["section"]
    else:
        title = f"स्मरणिका पृष्ठ {p} / Souvenir Page {p}"
        cat = "Advertisers"
        section = "Souvenir Advertisements"
    
    pages.append({
        "id": p,
        "pageNumber": p,
        "title": title,
        "category": cat,
        "section": section,
        "image": f"assets/pages/page_{p:03d}.jpg",
        "thumbnail": f"assets/thumbnails/thumb_{p:03d}.jpg"
    })

# Curate prominent advertisers directory
advertisers_data = [
    {
        "id": "adv-1",
        "name": "Mysore Jewellery House & S.V. Farms",
        "category": "Jewellery",
        "pageNumber": 2,
        "tagline": "Stay Perfect Staycation & Fine Gold Ornaments",
        "address": "1202, Saraf Galli, Shahapur, Belagavi / Devgiri Kadoli",
        "contact": "+91 98455 63059 / 99009 69963",
        "proprietor": "Surendra V. Vernekar & Sudhir S. Vernekar",
        "badge": "Platinum Sponsor",
        "thumbnail": "assets/thumbnails/thumb_002.jpg"
    },
    {
        "id": "adv-2",
        "name": "Anvekar Gold (अणवेकर गोल्ड)",
        "category": "Banking",
        "pageNumber": 3,
        "tagline": "सोने तारण सुलभ कर्ज • फक्त ३ मिनिटात दर ग्राम ₹10,000/-",
        "address": "Shahapur, Belagavi",
        "contact": "+91 88843 88863 / 94487 96863",
        "proprietor": "Anvekar Gold Finance",
        "badge": "Gold Loan",
        "thumbnail": "assets/thumbnails/thumb_003.jpg"
    },
    {
        "id": "adv-3",
        "name": "Vinayak Hanmanth Kudtarkar",
        "category": "Jewellery",
        "pageNumber": 5,
        "tagline": "Manufacturers and Wholesalers of Gold Jewellery",
        "address": "H. No. 358, Plot No. 7/6, Om Nagar, Belagavi",
        "contact": "+91 99454 23885",
        "proprietor": "Vinayak H. Kudtarkar",
        "badge": "Gold Wholesaler",
        "thumbnail": "assets/thumbnails/thumb_005.jpg"
    },
    {
        "id": "adv-4",
        "name": "R.K. & R.K. Anavekar Jewellers",
        "category": "Jewellery",
        "pageNumber": 7,
        "tagline": "Crafted with Purity, Elegance and Traditional Excellence",
        "address": "Kalyani, K.R. Street, Bharat Nagar, Shahapur, Belgaum - 590003",
        "contact": "+91 99000 92711",
        "proprietor": "rkanavekar@gmail.com",
        "badge": "Premier Jeweller",
        "thumbnail": "assets/thumbnails/thumb_007.jpg"
    },
    {
        "id": "adv-5",
        "name": "Laxmi Gold (Ashok & Aniket Vernekar)",
        "category": "Jewellery",
        "pageNumber": 8,
        "tagline": "Dealers in All Types of Gold Chains & Ornaments (916, 84, 74 Melting)",
        "address": "Shop No. 19, Navdurga Tower, Dane Galli, Shahapur, Belagavi - 590003",
        "contact": "+91 98454 39427 / 97403 23327",
        "proprietor": "Ashok Vernekar & Aniket Vernekar",
        "badge": "Gold Chains & 916",
        "thumbnail": "assets/thumbnails/thumb_008.jpg"
    },
    {
        "id": "adv-6",
        "name": "Shree Balaji Tar Pasta",
        "category": "Jewellery",
        "pageNumber": 9,
        "tagline": "Specialist in Bazubandh Patti, Gop Chain, Net Chain, Bracelets, Barik Tar & Nalli Pasta",
        "address": "H.No. 553/1, Datta Galli, Vadgaon, Belagavi",
        "contact": "+91 96861 99765 / 80589 75638",
        "proprietor": "Dinesh Vaishnav & Anil Vaishnav",
        "badge": "Specialist Artisan",
        "thumbnail": "assets/thumbnails/thumb_009.jpg"
    },
    {
        "id": "adv-7",
        "name": "Shri Mahalaxmi & Divine Reading",
        "category": "Patrons",
        "pageNumber": 10,
        "tagline": "Certified Tarot Card Reader & Astrological Insights",
        "address": "H.No. 1781 Jed Galli, Shahapur / Mahalaxmi, Congress Road, Tilakwadi",
        "contact": "+91 90355 94395 / 99169 63786",
        "proprietor": "Veena Manoj Kolvekar & Deepak M. Kolvekar",
        "badge": "Divine Reading",
        "thumbnail": "assets/thumbnails/thumb_010.jpg"
    },
    {
        "id": "adv-8",
        "name": "Motichand Jewels",
        "category": "Jewellery",
        "pageNumber": 22,
        "tagline": "Manufacturer & Wholesaler of Gold Jewellery",
        "address": "Manorath Apt, #102, 5th Cross, Opp. IMER College, Adarsh Nagar, Belagavi",
        "contact": "+91 831 355 4418 / 94809 88593",
        "proprietor": "Nagendra M. Pauskar",
        "badge": "Gold Wholesaler",
        "thumbnail": "assets/thumbnails/thumb_022.jpg"
    },
    {
        "id": "adv-9",
        "name": "Daivadnya Brahman Mangal Karyalaya",
        "category": "Community",
        "pageNumber": 35,
        "tagline": "2 Spacious Halls with Sound System, CCTV & Space for 800 People",
        "address": "Mahatma Phule Road, Shahapur, Belagavi - 590003",
        "contact": "+91 78927 93120 / 0831-3566962",
        "proprietor": "Manager Satish",
        "badge": "Community Hall",
        "thumbnail": "assets/thumbnails/thumb_035.jpg"
    },
    {
        "id": "adv-10",
        "name": "Omkrown PharmaChem Pvt Ltd",
        "category": "Industries",
        "pageNumber": 193,
        "tagline": "Innovating Chemistry, Enriching Lives - Specialty Chemicals & Pharma",
        "address": "Kalyani, K.R. Street, Shahapur / 422/4 Goa Road, Macche, Belgaum",
        "contact": "+91 94484 82711 / info@omkrown.com",
        "proprietor": "Late Shri Ramakant K. Anavekar (Founder Chairman)",
        "badge": "Pharma & Chemical",
        "thumbnail": "assets/thumbnails/thumb_193.jpg"
    },
    {
        "id": "adv-11",
        "name": "Shri Ganesh Gold",
        "category": "Jewellery",
        "pageNumber": 194,
        "tagline": "Trilling Chain & Machine Chain, All Types of Ornaments Work",
        "address": "Bhoj Galli, Shahapur, Belagavi - 590003",
        "contact": "+91 74065 15823",
        "proprietor": "Balaji Shinde",
        "badge": "Chain Specialist",
        "thumbnail": "assets/thumbnails/thumb_194.jpg"
    },
    {
        "id": "adv-12",
        "name": "Shri Munishwar Motors (Royal Enfield)",
        "category": "Automobile",
        "pageNumber": 195,
        "tagline": "Authorized Royal Enfield Showroom & State-of-the-Art Service Center",
        "address": "Opp. Kavookatta and Fire Brigade, GOAVES, Belagavi",
        "contact": "+91 81052 82000 / 99643 22773",
        "proprietor": "Shri Lingaraj Jagajampi (Managing Director)",
        "badge": "Royal Enfield Belgaum",
        "thumbnail": "assets/thumbnails/thumb_195.jpg"
    }
]

# Standardize advertiser directory items
for item in advertisers_data:
    if "marathiName" not in item:
        item["marathiName"] = item["name"]
    item["location"] = item["address"]
    item["phone"] = item["contact"]
    item["tags"] = [item["name"], item["category"], item["address"], item["badge"], item["tagline"]]

output_js = mandal_config + "\n\nconst BOOK_PAGES = " + json.dumps(pages, indent=2, ensure_ascii=False) + ";\n\nconst ADVERTISERS_DATA = " + json.dumps(advertisers_data, indent=2, ensure_ascii=False) + ";\n\nconst ADVERTISERS_DIRECTORY = ADVERTISERS_DATA;\n"

with open("js/book-data.js", "w", encoding="utf-8") as f:
    f.write(output_js)

print("Generated js/book-data.js successfully with 196 pages and aligned advertiser directory!")
