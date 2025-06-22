from src.domain.models import Note, Tag
from src.domain.protocols.note import Ports
from src.domain.requests import NoteRequest, TagRequest

def get_note(ports: Ports, note_id: str) -> Note:
    with ports.store() as store:
        return store.note.get_note(note_id)

def get_all_notes(ports: Ports) -> list[Note]:
    with ports.store() as store:
        return store.note.get_notes()

def create_note(
    ports: Ports, note_request: NoteRequest
) -> Note:
    with ports.mutable_store() as store:
        return store.note.create_note(note_request)


def update_note(
    ports: Ports, note_request: NoteRequest
) -> Note:
    with ports.mutable_store() as store:
        return store.note.update_note(note_request)

def delete_note(ports: Ports, note_id: str) -> bool:
    with ports.mutable_store() as store:
        return store.note.delete_note(note_id)

def get_tag(ports: Ports, tag_id: str) -> list[Tag]:
    with ports.store() as store:
        return store.tag.get_tag(tag_id)

def get_all_tags(ports: Ports) -> list[Tag]:
    with ports.store() as store:
        return store.tag.get_tags()


def create_tag(ports: Ports, tag_request: TagRequest) -> Tag:
    with ports.mutable_store() as store:
        return store.tag.create_tag(tag_request)