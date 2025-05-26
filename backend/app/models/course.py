from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Course(BaseModel):
    id: Optional[str]
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
