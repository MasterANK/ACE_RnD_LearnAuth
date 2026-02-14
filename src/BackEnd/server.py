from fastapi import FastAPI
from pydantic import BaseModel
from gemini_processing import (
    get_transcript_with_pytube,
    analyze_transcript_with_gemini
)

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.post("/analyze")
def analyze_video(data: VideoRequest):
    try:
        transcript = get_transcript_with_pytube(data.url)
        result = analyze_transcript_with_gemini(transcript)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
