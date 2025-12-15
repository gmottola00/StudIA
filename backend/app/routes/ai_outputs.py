from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel

from app.dependencies import get_supabase_service
from app.models.ai_output import AIOutput
from app.services.generative.rag import generate_rag_content

router = APIRouter(prefix="/ai-outputs", tags=["ai_outputs"])

class AIOutputCreate(BaseModel):
    document_id: str
    type: str
    format: str
    content: str

class AIContentGenerateRequest(BaseModel):
    document_id: str
    query: str

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

@router.post("/generate", response_model=AIOutput, status_code=201)
def generate_ai_content(payload: AIContentGenerateRequest, supabase=Depends(get_supabase_service)):
    # Retrieve the document from the database
    document = supabase.documents.get_by_id(payload.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Generate content using the RAG pipeline
    generated_content = generate_rag_content(document.content, payload.query)

    # Store the generated content in the database
    ai_output = supabase.ai_outputs.insert(
        document_id=payload.document_id,
        type="generated",
        format="text",
        content=generated_content
    )

    return ai_output
