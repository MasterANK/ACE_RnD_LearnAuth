import os
import requests
import pandas as pd
from gemini_processing import (
    get_transcript_with_pytube,
    analyze_transcript_with_gemini
)
from dotenv import load_dotenv

# -----------------------------
# 🔐 Load API Keys
# -----------------------------
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


# -----------------------------
# 🎥 YouTube Search Function
# -----------------------------
def search_youtube(topic, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": topic,
        "type": "video",
        "videoCaption": "closedCaption",
        "videoDuration": "medium",
        "order": "relevance",
        "relevanceLanguage": "en",
        "safeSearch": "moderate",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        raise Exception(data["error"]["message"])

    videos = []

    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]

        videos.append({
            "title": title,
            "channel": channel,
            "link": f"https://www.youtube.com/watch?v={video_id}"
        })

    return videos


# -----------------------------
# 🏆 Recommendation Engine
# -----------------------------
def recommend_videos(topic, max_results=12, limit=5):

    videos = search_youtube(topic, max_results=max_results)

    results = []

    for video in videos:
        if len(results) >= limit:
            break

        try:
            transcript = get_transcript_with_pytube(
                video["link"],
                languages=['en', 'hi']
            )

            rating = analyze_transcript_with_gemini(transcript)

            results.append({
                "Video Title": video["title"],
                "Channel": video["channel"],
                "Link": video["link"],
                **rating
            })

        except Exception:
            continue

    if not results:
        return None

    df = pd.DataFrame(results)

    # Equal weight scoring
    df["personal_score"] = (
        df["clarity"] +
        df["concept_depth"] +
        df["engagement"] +
        (10 - df["promotion"])
    )

    ranked = df.sort_values("personal_score", ascending=False).reset_index(drop=True)

    ranked.insert(0, "Rank", ranked.index + 1)

    return ranked


# -----------------------------
# 📥 CSV Export Utility
# -----------------------------
def export_to_csv(ranked_df, topic):
    export_df = ranked_df[[
        "Rank",
        "Video Title",
        "Channel",
        "Link",
        "clarity",
        "concept_depth",
        "engagement",
        "promotion",
        "personal_score"
    ]].rename(columns={
        "personal_score": "Personal Score",
        "concept_depth": "Concept Depth"
    })

    return export_df.to_csv(index=False).encode("utf-8")
