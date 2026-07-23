from app.services.pdf_parser_service import extract_text_from_pdf

def process_document(file_path: str):
    pages= extract_text_from_pdf(file_path)

    return {
        "total_page": len(pages),
        "pages": pages 
    }