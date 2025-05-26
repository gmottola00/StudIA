from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AIOutput(BaseModel):
    id: Optional[str]
    document_id: str
    type: str      # 'summary', 'quiz', 'flashcard', 'mindmap', 'audio'
    format: str    # 'text', 'json', 'url', 'mp3', 'base64'
    content: str
    created_at: Optional[datetime] = None
