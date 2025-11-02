"""
Pydantic models for Diary entries
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class EntryCreate(BaseModel):
    """Model for creating a new entry"""
    title: str = "Untitled"
    text: Optional[str] = None
    audio_path: Optional[str] = None
    image_path: Optional[str] = None
    tags: List[str] = []
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class EntryResponse(BaseModel):
    """Model for entry response"""
    id: str
    title: str
    text: Optional[str] = None
    audio_path: Optional[str] = None
    image_path: Optional[str] = None
    tags: List[str] = []
    timestamp: str
    similarity_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class SearchQuery(BaseModel):
    """Model for search queries"""
    text: str
    limit: Optional[int] = Field(default=10, ge=1, le=100)


class QuestionQuery(BaseModel):
    """Model for question-answering queries"""
    text: str
    include_media: bool = True




