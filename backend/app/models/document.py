from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Document(BaseModel):
    id: Optional[str]
    user_id: str
    original_filename: str
    file_url: str
    parsed_text: Optional[str] = None
    created_at: Optional[datetime] = None
