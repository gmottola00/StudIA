from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel

from app.dependencies import get_supabase_service
from app.models.activity_log import ActivityLog

router = APIRouter(prefix="/activity-logs", tags=["activity_logs"])

class ActivityLogCreate(BaseModel):
    user_id: str
    action: str
    metadata: dict = {}

@router.post("/", response_model=ActivityLog, status_code=201)
def create_log(payload: ActivityLogCreate, supabase=Depends(get_supabase_service)):
    return supabase.activity_logs.insert(
        user_id=payload.user_id,
        action=payload.action,
        metadata=payload.metadata
    )

@router.get("/{log_id}", response_model=ActivityLog)
def get_log(log_id: str, supabase=Depends(get_supabase_service)):
    log = supabase.activity_logs.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return log

@router.get("/by-user/{user_id}", response_model=List[ActivityLog])
def list_logs(user_id: str, supabase=Depends(get_supabase_service)):
    return supabase.activity_logs.get_by_user(user_id)
