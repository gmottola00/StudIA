from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ActivityLog(BaseModel):
    id: Optional[str]
    user_id: str
    action: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
