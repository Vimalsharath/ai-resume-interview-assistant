import fitz

def extract_text(pdf_path):

    print("Opening:", pdf_path)

    document = fitz.open(pdf_path)

    print("Number of pages:", len(document))

    text = ""

    for page in document:
        page_text = page.get_text()

        print("Characters on page:", len(page_text))

        text += page_text

    document.close()

    return text