from typing import Optional, List
from supabase import Client
from models import Document

class DocumentManager:
    """
    DocumentManager gestisce le operazioni CRUD sulla tabella 'documents' in Supabase.
    """

    def __init__(self, client: Client):
        self.client = client
        self.table = self.client.table("documents")

    def insert(self, user_id: str, original_filename: str, file_url: str, parsed_text: Optional[str] = None) -> Document:
        """
        Inserisce un nuovo documento e restituisce il record creato come Document.
        """
        data = {
            "user_id": user_id,
            "original_filename": original_filename,
            "file_url": file_url,
            "parsed_text": parsed_text
        }
        response = self.table.insert(data).execute()
        record = response.data[0]
        return Document(**record)

    def get(self, doc_id: str) -> Optional[Document]:
        """
        Recupera un documento per ID, restituisce Document o None.
        """
        response = self.table.select("*").eq("id", doc_id).single().execute()
        if response.data:
            return Document(**response.data)
        return None

    def get_all(self, user_id: Optional[str] = None) -> List[Document]:
        """
        Recupera tutti i documenti, o quelli di uno specifico utente.
        """
        query = self.table.select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        response = query.execute()
        return [Document(**item) for item in response.data]

    def update(self, doc_id: str, new_data: dict) -> Optional[Document]:
        """
        Aggiorna i campi di un documento e restituisce il documento aggiornato.
        """
        response = self.table.update(new_data).eq("id", doc_id).execute()
        if response.data:
            return Document(**response.data[0])
        return None

    def delete(self, doc_id: str) -> bool:
        """
        Elimina un documento per ID. Restituisce True se eliminato con successo.
        """
        response = self.table.delete().eq("id", doc_id).execute()
        # Supabase restituisce un array vuoto se nessun record, altrimenti array di deleted
        return len(response.data) > 0
