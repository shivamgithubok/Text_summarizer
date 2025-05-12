from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from src.textsummarizer.pipeline.prediction import PredictionPipeline

app = FastAPI()

# Load Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict_route(request: TextRequest):
    try:
        obj = PredictionPipeline()
        result = obj.predict(request.text)
        return JSONResponse(content={"summary": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
