from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel

from app.dependencies import get_supabase_service
from app.models.document import Document

router = APIRouter(prefix="/documents", tags=["documents"])

class DocumentCreate(BaseModel):
    user_id: str
    original_filename: str
    file_url: str
    parsed_text: Optional[str] = None

class DocumentUpdate(BaseModel):
    original_filename: Optional[str] = None
    file_url: Optional[str] = None
    parsed_text: Optional[str] = None

@router.post("/", response_model=Document, status_code=status.HTTP_201_CREATED)
def create_document(payload: DocumentCreate, supabase=Depends(get_supabase_service)):
    """
    Create a new document.
    """
    return supabase.documents.insert(
        user_id=payload.user_id,
        original_filename=payload.original_filename,
        file_url=payload.file_url,
        parsed_text=payload.parsed_text
    )

@router.get("/{document_id}", response_model=Document)
def get_document(document_id: str, supabase=Depends(get_supabase_service)):
    doc = supabase.documents.get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/", response_model=List[Document])
def list_documents(user_id: str, supabase=Depends(get_supabase_service)):
    """
    List all documents for a specific user.
    """
    return supabase.documents.get_all(user_id)

@router.patch("/{document_id}", response_model=Document)
def update_document(document_id: str, payload: DocumentUpdate, supabase=Depends(get_supabase_service)):
    updated = supabase.documents.update(document_id, payload.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Document not found or no changes applied")
    return updated

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, supabase=Depends(get_supabase_service)):
    success = supabase.documents.delete(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
