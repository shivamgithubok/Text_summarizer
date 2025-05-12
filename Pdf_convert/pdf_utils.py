import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using PyMuPDF; falls back to OCR if needed."""
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])

        if text.strip():  # If text extraction works
            return text.strip()

        # If no text found, try OCR on images
        images = convert_from_bytes(open(pdf_path, "rb").read())
        ocr_text = "\n".join(pytesseract.image_to_string(img) for img in images)

        return ocr_text.strip() if ocr_text.strip() else None
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
