import os

import fitz
import pytesseract
from pdf2image import convert_from_path


def extract_resume_text(pdf_path):
    text = ""

    if not os.path.exists(pdf_path):
        return "Resume file was not found."

    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        if text.strip():
            return text.strip()
    except Exception:
        pass

    try:
        pages = convert_from_path(pdf_path)
        for page in pages:
            text += pytesseract.image_to_string(page)
        return text.strip()
    except Exception as exc:
        return f"OCR Error: {exc}"