import uuid
from fastapi import APIRouter, Path, status, HTTPException, Request

from src.contexts.note import PortsImpl
from src.domain import service
from src.domain.requests import NoteRequest, NoteUpdateRequest


router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/", status_code=status.HTTP_200_OK)
async def get_notes():
    ports = PortsImpl()
    notes = service.get_all_notes(ports)
    return notes


@router.get("/{note_id}", status_code=status.HTTP_200_OK)
async def get_note(note_id: str = Path(..., description="The ID of the note to retrieve")):
    ports = PortsImpl()
    note = service.get_note(ports, uuid.UUID(note_id))
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    return note


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_note(note_request: NoteRequest):
    ports = PortsImpl()
    note = service.create_note(ports, note_request)
    return note


@router.put("/{note_id}", status_code=status.HTTP_200_OK)
async def update_note(note_id: str, note_request: NoteUpdateRequest):
    ports = PortsImpl()
    note = service.update_note(ports, uuid.UUID(note_id), note_request)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str):
    ports = PortsImpl()
    success = service.delete_note(ports, uuid.UUID(note_id))
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    return {"detail": "Note deleted successfully"}