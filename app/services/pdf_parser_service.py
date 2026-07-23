import fitz
from typing import List, Dict 

def extract_text_from_pdf(file_path: str) -> List[Dict]:

    doc = fitz.open(file_path)
    
    pages = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        pages.append({
            "page_number": page_num + 1,
            "text": text.strip()
        })

    doc.close()

    return pages
