import os
import cv2
import requests
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import processing
app = FastAPI()

# 1. ALLOW THE EXTENSION TO TALK TO PYTHON
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. SETUP DATA FOLDER
BASE_DIR = Path(__file__).resolve().parent
SAVE_FOLDER = BASE_DIR / "thumbnails"
SAVE_FOLDER.mkdir(exist_ok=True)

class YTData(BaseModel):
    title: str
    thumbnail_url: str

# 3. THE ENDPOINT
@app.post("/process_youtube")
async def handle_youtube_request(data: YTData):
    try:
        # Save the image
        video_id = data.thumbnail_url.split('/vi/')[1].split('/')[0]
        filepath = SAVE_FOLDER / f"{video_id}.jpg"
        
        response = requests.get(data.thumbnail_url)
        with open(filepath, "wb") as f:
            f.write(response.content)

        # --- TRIGGER YOUR AI LOGIC HERE ---
        # Note: I renamed this so it doesn't conflict with any imports
        result_text = run_ai_analysis(str(filepath), data.title)

        return {
            "status": "success",
            "summary": f"Video: {data.title}. Result: {result_text}"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "summary": str(e)}

def run_ai_analysis(image_path, title):
    return processing.clickbait_or_not(image_path, title)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)