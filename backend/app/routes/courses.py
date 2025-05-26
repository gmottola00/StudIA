from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel

from app.dependencies import get_supabase_service
from app.models.course import Course

router = APIRouter(prefix="/courses", tags=["courses"])

class CourseCreate(BaseModel):
    user_id: str
    name: str
    description: Optional[str] = None

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, supabase=Depends(get_supabase_service)):
    return supabase.courses.insert(
        user_id=payload.user_id,
        name=payload.name,
        description=payload.description
    )

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: str, supabase=Depends(get_supabase_service)):
    course = supabase.courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/", response_model=List[Course])
def list_courses(user_id: str, supabase=Depends(get_supabase_service)):
    return supabase.courses.get_all(user_id)

@router.patch("/{course_id}", response_model=Course)
def update_course(course_id: str, payload: CourseUpdate, supabase=Depends(get_supabase_service)):
    updated = supabase.courses.update(course_id, payload.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found or no changes applied")
    return updated

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: str, supabase=Depends(get_supabase_service)):
    success = supabase.courses.delete(course_id)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")
