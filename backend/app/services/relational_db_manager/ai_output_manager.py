# ai_output_manager.py

from typing import List, Optional, Dict, Any
from datetime import datetime
from supabase import Client
from pydantic import BaseModel


class AIOutput(BaseModel):
    id: Optional[str]
    document_id: str
    type: str        # 'summary', 'quiz', 'flashcard', 'mindmap', 'audio'
    format: str      # 'text', 'json', 'url', 'mp3', 'base64'
    content: str
    created_at: Optional[datetime]


class AIOutputManager:
    def __init__(self, supabase: Client, table_name: str = "ai_outputs"):
        self.supabase = supabase
        self.table = table_name

    def insert(
        self,
        document_id: str,
        type: str,
        format: str,
        content: str
    ) -> AIOutput:
        """Crea un nuovo record AIOutput."""
        payload = {
            "document_id": document_id,
            "type": type,
            "format": format,
            "content": content
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
        return AIOutput(**data)

    def get_by_id(self, output_id: str) -> Optional[AIOutput]:
        """Recupera un AIOutput per ID."""
        result = (
            self.supabase
            .table(self.table)
            .select("*")
            .eq("id", output_id)
            .single()
            .execute()
        )
        data = result.data
        return AIOutput(**data) if data else None

    def get_by_document(self, document_id: str) -> List[AIOutput]:
        """Recupera tutti gli AIOutput di un documento specifico."""
        result = (
            self.supabase
            .table(self.table)
            .select("*")
            .eq("document_id", document_id)
            .order("created_at", desc=True)
            .execute()
        )
        return [AIOutput(**row) for row in result.data]

    def update(self, output_id: str, changes: Dict[str, Any]) -> Optional[AIOutput]:
        """Aggiorna i campi di un AIOutput esistente."""
        result = (
            self.supabase
            .table(self.table)
            .update(changes)
            .eq("id", output_id)
            .select("*")
            .single()
            .execute()
        )
        data = result.data
        return AIOutput(**data) if data else None

    def delete(self, output_id: str) -> bool:
        """Elimina un AIOutput per ID."""
        result = (
            self.supabase
            .table(self.table)
            .delete()
            .eq("id", output_id)
            .execute()
        )
        # Supabase ritorna count di righe eliminate in result.count
        return (result.count or 0) > 0

    def get_all(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[AIOutput]:
        """Recupera ai più 'limit' AIOutput, con pagination."""
        result = (
            self.supabase
            .table(self.table)
            .select("*")
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return [AIOutput(**row) for row in result.data]
