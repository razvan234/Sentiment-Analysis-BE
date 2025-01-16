from typing import Optional, List, Dict

from pydantic import BaseModel


class VideoURL(BaseModel):
    url: str


class Comment(BaseModel):
    text_display: str
    text_original: Optional[str] = None
    sentiment: Optional[str] = None


class VideoOutput(BaseModel):
    comments: List[Comment]
    sentiment_summary: Dict
    overall_summary: str

