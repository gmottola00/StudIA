from typing import List, Optional, Dict, Any
from supabase import Client
from app.models.course import Course

class CourseManager:
    def __init__(self, supabase: Client, table_name: str = "materia"):
        self.supabase = supabase
        self.table = table_name

    def insert(self, user_id: str, name: str, description: Optional[str] = None) -> Course:
        """Creates a new Course record."""
        payload = {
            "user_id": user_id,
            "name": name,
            "description": description
        }
        result = (
            self.supabase
            .table(self.table)
            .insert(payload)
            .select("*")
            .single()
            .execute()
        )
        data = result.data
        return Course(**data)

    def get(self, course_id: str) -> Optional[Course]:
        """Retrieves a Course by ID."""
        result = (
            self.supabase
            .table(self.table)
            .select("*")
            .eq("id", course_id)
            .single()
            .execute()
        )
        data = result.data
        return Course(**data) if data else None

    def get_all(self, user_id: str) -> List[Course]:
        """Retrieves all Courses for a given user."""
        result = (
            self.supabase
            .table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return [Course(**item) for item in result.data]

    def update(self, course_id: str, changes: Dict[str, Any]) -> Optional[Course]:
        """Updates an existing Course record."""
        result = (
            self.supabase
            .table(self.table)
            .update(changes)
            .eq("id", course_id)
            .select("*")
            .single()
            .execute()
        )
        data = result.data
        return Course(**data) if data else None

    def delete(self, course_id: str) -> bool:
        """Deletes a Course by ID."""
        result = (
            self.supabase
            .table(self.table)
            .delete()
            .eq("id", course_id)
            .execute()
        )
        return (result.count or 0) > 0
