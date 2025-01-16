from typing import Union
from utils.utils import extract_values, clean_text
import requests
from fastapi.middleware.cors import CORSMiddleware
from sentiment import sentiment_scores, sentiment_summary
from dotenv import load_dotenv
import os
from models.Video import Comment,  VideoOutput

from fastapi import FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY is not set in the .env file")

YOUTUBE_COMMENTS_URL = "https://www.googleapis.com/youtube/v3/commentThreads"


@app.post("/comments")
async def scrape_comments(video_id: str):
    params = {
        "part": "snippet",
        "videoId": extract_values(video_id),
        "key": YOUTUBE_API_KEY,
        "maxResults": 20
    }

    response = requests.get(YOUTUBE_COMMENTS_URL, params=params)

    if response.status_code != 200:
        return {"error": "Failed to fetch data from YouTube API"}

    data = response.json()

    comments = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
        comments.append(Comment(
            text_display=clean_text(snippet.get("textDisplay", "")),
            sentiment=sentiment_scores(snippet.get("textDisplay", ""))
        ))
    summary_data = sentiment_summary(comments)

    video_output = VideoOutput(
        comments=comments,
        sentiment_summary=summary_data['summary'],
        overall_summary=summary_data['overall_sentiment']
    )
    return video_output
