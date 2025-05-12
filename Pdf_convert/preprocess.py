import re

def preprocess_text(text):
    """Cleans and formats extracted text."""
    if not text:
        return "No text found in PDF."

    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove special characters (optional)
    text = re.sub(r'[^a-zA-Z0-9,.!? ]', '', text)

    return text
