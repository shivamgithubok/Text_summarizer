import streamlit as st
from Pdf_convert.pdf_utils import extract_text_from_pdf
from Pdf_convert.preprocess import preprocess_text
from src.textSummarizer.pipeline.prediction import PredictionPipeline
from Pdf_convert.text_to_speech import text_to_speech
from bs4 import BeautifulSoup
import requests
import os

st.title("Text Summarizer App")

# Upload PDF
st.header("1. Upload a PDF File")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file:
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    pdf_text = extract_text_from_pdf(temp_path)
    os.remove(temp_path)

    if pdf_text:
        st.subheader("Extracted Text")
        st.text_area("PDF Text", pdf_text, height=200)

        processed_text = preprocess_text(pdf_text)
        st.subheader("Processed Text")
        st.text_area("Processed", processed_text, height=150)

        # Predict Summary
        if st.button("Summarize Text"):
            predictor = PredictionPipeline()
            summary = predictor.predict(processed_text)
            st.subheader("Summary")
            st.write(summary)

            # Text to Speech
            if st.button("Convert to Speech"):
                audio_file = text_to_speech(summary, "speech.mp3")
                audio_bytes = open("speech.mp3", "rb").read()
                st.audio(audio_bytes, format="audio/mp3")

    else:
        st.error("Could not extract text from PDF.")

# Scrape Website
st.header("2. Scrape Website Content")
url = st.text_input("Enter a URL to scrape:")
if st.button("Scrape"):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        scraped_text = " ".join([p.get_text() for p in paragraphs[:5]])
        st.text_area("Scraped Text", scraped_text, height=200)
    except Exception as e:
        st.error(f"Web Scraping Error: {str(e)}")
