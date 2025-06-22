from fastapi import APIRouter, FastAPI, Path, status, HTTPException, Request

from src.contexts.note import Ports
from src.domain import service
from src.domain.requests import NoteRequest


router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/", status_code=status.HTTP_200_OK)
async def get_notes():
    ports = Ports()
    notes = service.get_all_notes(ports)
    return notes

@router.get("/{note_id}", status_code=status.HTTP_200_OK)
async def get_note(note_id: str = Path(..., description="The ID of the note to retrieve")):
    ports = Ports()
    note = service.get_note(ports, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    return note

@router.post("/notes", status_code=status.HTTP_201_CREATED)
async def create_note(note_request: NoteRequest):
    ports = Ports()
    note_data = note_request.model_dump()
    note = service.create_note(ports, note_data)
    return note

@router.put("/notes/{note_id}", status_code=status.HTTP_200_OK)
async def update_note(note_id: str, note_request: NoteRequest):
    ports = Ports()
    note_data = note_request.model_dump(update={"id": note_id})
    note = service.update_note(ports, note_data)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    return note