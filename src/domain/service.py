import uuid
from src.domain.models import Note, Tag, TagWithNotes
from src.domain.protocols.note import PortsInterface
from src.domain.requests import NoteRequest, NoteUpdateRequest, TagRequest

def get_note(ports: PortsInterface, note_id: uuid.UUID) -> Note:
    with ports.store() as store:
        return store.note.get_note(note_id)

def get_all_notes(ports: PortsInterface) -> list[Note]:
    with ports.store() as store:
        return store.note.get_notes()

def create_note(
    ports: PortsInterface, note_request: NoteRequest
) -> Note:
    with ports.mutable_store() as store:
        return store.note.create_note(note_request)


def update_note(
    ports: PortsInterface, note_id: uuid.UUID, note_request: NoteUpdateRequest
) -> Note:
    with ports.mutable_store() as store:
        note = store.note.update_note(note_id, note_request)
        return note

def delete_note(ports: PortsInterface, note_id: str) -> bool:
    with ports.mutable_store() as store:
        return store.note.delete_note(note_id)

def get_tag(ports: PortsInterface, name: str) -> list[TagWithNotes]:
    with ports.store() as store:
        return store.tags.get_tag(name)

def get_all_tags(ports: PortsInterface) -> list[Tag]:
    with ports.store() as store:
        return store.tags.get_tags()


def create_tag(ports: PortsInterface, tag_request: TagRequest) -> Tag:
    with ports.mutable_store() as store:
        return store.tags.create_tag(tag_request)