from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import os
from bs4 import BeautifulSoup

# Import the required functions
from Pdf_convert.pdf_utils import extract_text_from_pdf
from Pdf_convert.preprocess import preprocess_text  # Ensure preprocess.py exists
from src.textSummarizer.pipeline.prediction import PredictionPipeline
from Pdf_convert.text_to_speech import text_to_speech

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        pdf_text = extract_text_from_pdf(temp_path)
        os.remove(temp_path)

        if not pdf_text:
            return JSONResponse(content={"error": "Not able to extract text from PDF"}, status_code=500)

        processed_text = preprocess_text(pdf_text)
        return JSONResponse(content={"text": processed_text})

    except Exception as e:
        return JSONResponse(content={"error": f"PDF Processing Error: {str(e)}"}, status_code=500)


@app.post("/predict")
async def predict_route(request: dict):
    try:
        text = request.get("text", "").strip()
        if not text:
            return JSONResponse(content={"error": "No input text provided"}, status_code=400)

        predictor = PredictionPipeline()
        summary = predictor.predict(text)

        if not summary:
            return JSONResponse(content={"error": "Summarization failed"}, status_code=500)

        return JSONResponse(content={"summary": summary})

    except Exception as e:
        return JSONResponse(content={"error": f"Internal Server Error: {str(e)}"}, status_code=500)


@app.post("/speak")
async def speak_text(request: dict):
    try:
        text = request.get("text", "").strip()
        if not text:
            return JSONResponse(content={"error": "No text provided"}, status_code=400)

        audio_file = text_to_speech(text, "speech.mp3")

        if not audio_file:
            return JSONResponse(content={"error": "Speech conversion failed"}, status_code=500)

        return FileResponse(audio_file, media_type="audio/mpeg", filename="speech.mp3")

    except Exception as e:
        return JSONResponse(content={"error": f"Internal Server Error: {str(e)}"}, status_code=500)


@app.post("/scrape")
async def scrape_website(request: Request):
    try:
        data = await request.json()
        url = data.get("url")

        if not url:
            return JSONResponse(content={"error": "No URL provided"}, status_code=400)

        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        scraped_text = " ".join([p.get_text() for p in paragraphs[:5]])  # Limit to 5 paragraphs

        return JSONResponse(content={"text": scraped_text})

    except Exception as e:
        return JSONResponse(content={"error": f"Web Scraping Error: {str(e)}"}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
