import pytesseract
from pdf2image import convert_from_path
import fitz
import os


def extract_resume_text(pdf_path):

    text = ""


    # First try normal PDF text extraction
    try:

        doc = fitz.open(pdf_path)

        for page in doc:

            page_text = page.get_text()

            text += page_text


        doc.close()


        # If text exists, return it
        if text.strip():

            return text


    except Exception:

        pass



    # If PDF is scanned, use OCR

    try:

        pages = convert_from_path(
            pdf_path
        )


        for page in pages:

            page_text = pytesseract.image_to_string(
                page
            )

            text += page_text



    except Exception as e:

        return f"OCR Error: {e}"



    return text