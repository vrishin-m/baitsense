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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent
SAVE_FOLDER = BASE_DIR / "thumbnails"
SAVE_FOLDER.mkdir(exist_ok=True)

class YTData(BaseModel):
    title: str
    thumbnail_url: str


@app.post("/process_youtube")
async def handle_youtube_request(data: YTData):
    try:
        
        video_id = data.thumbnail_url.split('/vi/')[1].split('/')[0]
        filepath = SAVE_FOLDER / f"{video_id}.jpg"
        
        response = requests.get(data.thumbnail_url)
        with open(filepath, "wb") as f:
            f.write(response.content)

    
        result_text, final_score = processing.clickbait_or_not(f"{filepath}", data.title)

        return {
            "status": "success",
            "summary": f"Result: {result_text}.   Final Score: {final_score}"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "summary": str(e)}


    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)