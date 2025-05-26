from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel

from app.dependencies import get_supabase_service
from app.models.ai_output import AIOutput

router = APIRouter(prefix="/ai-outputs", tags=["ai_outputs"])

class AIOutputCreate(BaseModel):
    document_id: str
    type: str
    format: str
    content: str

@router.post("/", response_model=AIOutput, status_code=201)
def create_output(payload: AIOutputCreate, supabase=Depends(get_supabase_service)):
    return supabase.ai_outputs.insert(
        document_id=payload.document_id,
        type=payload.type,
        format=payload.format,
        content=payload.content
    )

@router.get("/{output_id}", response_model=AIOutput)
def get_output(output_id: str, supabase=Depends(get_supabase_service)):
    output = supabase.ai_outputs.get_by_id(output_id)
    if not output:
        raise HTTPException(status_code=404, detail="AI output not found")
    return output

@router.get("/by-document/{document_id}", response_model=List[AIOutput])
def list_outputs(document_id: str, supabase=Depends(get_supabase_service)):
    return supabase.ai_outputs.get_by_document(document_id)
