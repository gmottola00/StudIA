from typing import List, Optional, Dict, Any
from supabase import Client
from app.models.activity_log import ActivityLog

class ActivityLogManager:
    def __init__(self, supabase: Client, table_name: str = "activity_log"):
        self.supabase = supabase
        self.table = table_name

    def insert(self, user_id: str, action: str, metadata: Optional[Dict[str, Any]] = None) -> ActivityLog:
        """Crea un nuovo log attività."""
        payload = {
            "user_id": user_id,
            "action": action,
            "metadata": metadata or {}
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
        return ActivityLog(**data)

    def get_by_id(self, log_id: str) -> Optional[ActivityLog]:
        """Recupera un log attività per ID."""
        result = (
            self.supabase
            .table(self.table)
            .select("*")
            .eq("id", log_id)
            .single()
            .execute()
        )
        data = result.data
        return ActivityLog(**data) if data else None

    def get_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> List[ActivityLog]:
        """Recupera tutti i log di un utente specifico."""
        result = (
            self.supabase
            .table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return [ActivityLog(**item) for item in result.data]

    def delete(self, log_id: str) -> bool:
        """Elimina un log attività per ID."""
        result = (
            self.supabase
            .table(self.table)
            .delete()
            .eq("id", log_id)
            .execute()
        )
        return (result.count or 0) > 0

    def get_all(self, limit: int = 100, offset: int = 0) -> List[ActivityLog]:
        """Recupera tutti i log con pagination."""
        result = (
            self.supabase
            .table(self.table)
            .select("*")
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return [ActivityLog(**item) for item in result.data]
