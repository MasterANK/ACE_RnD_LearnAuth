import os
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from dotenv import load_dotenv

# -----------------------------
# 🔐 Load API Key
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"


# =====================================================
# 🎥 Transcript Extraction
# =====================================================
def get_transcript_with_pytube(url, languages=None):
    """
    Extracts transcript from YouTube video.
    Handles manual + auto-generated + fallback transcripts.
    """

    # Extract video ID
    if "youtu.be/" in url:
        video_id = url.split("/")[-1].split("?")[0]
    else:
        video_id = url.split("v=")[-1].split("&")[0]

    ytt = YouTubeTranscriptApi()
    transcript_list = ytt.list(video_id)

    transcript = None

    # Try preferred languages
    if languages:
        try:
            transcript = transcript_list.find_manually_created_transcript(languages)
        except:
            try:
                transcript = transcript_list.find_generated_transcript(languages)
            except:
                pass

    # Fallback: use any available transcript
    if transcript is None:
        try:
            available_languages = [t.language_code for t in transcript_list]
            transcript = transcript_list.find_transcript(available_languages)
        except:
            pass

    if transcript is None:
        raise Exception("No transcript found for video_id=" + video_id)

    fetched = transcript.fetch()

    try:
        full_text = " ".join([item["text"] for item in fetched if item.get("text")])
    except:
        full_text = " ".join([item.text for item in fetched if hasattr(item, "text")])

    return full_text.strip()


# =====================================================
# 🤖 Gemini Analysis
# =====================================================
def analyze_transcript_with_gemini(transcript_text):

    prompt = f"""
You are an expert educational evaluator.
Analyze this YouTube video transcript and rate it objectively.

Return ONLY valid JSON:

{{
  "clarity": 1-10,
  "concept_depth": 1-10,
  "engagement": 1-10,
  "promotion": 1-10,
  "summary": "short summary",
  "overall_rating": 1-10
}}

Transcript:
\"\"\"{transcript_text[:15000]}\"\"\"
"""

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    text = getattr(response, "text", str(response))

    try:
        return json.loads(text)
    except:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Could not parse JSON output.")
