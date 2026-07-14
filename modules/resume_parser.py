import pytesseract
from pdf2image import convert_from_path


# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# Poppler location
POPPLER_PATH = (
    r"C:\Users\sharath V\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
)



def extract_resume_text(pdf_path):

    pages = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )


    text = ""


    for page in pages:

        page_text = pytesseract.image_to_string(
            page
        )

        text += page_text


    return text