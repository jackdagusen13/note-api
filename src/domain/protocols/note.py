import contextlib
from typing import Protocol, Optional, Generator
import uuid

from src.domain.models import Note, Tag, TagWithNotes
from src.domain.requests import NoteRequest, NoteUpdateRequest, TagRequest


class NoteQuery(Protocol):
    def get_note(note_id: uuid.UUID) -> Optional[Note]:
        """Retrieve a note by its ID."""

    def get_notes() -> list[Note]:
        """Retrieve all notes."""


class NoteMutation(NoteQuery, Protocol):
    def create_note(note: NoteRequest) -> Note:
        """Create a new note."""

    def update_note(note_id: uuid.UUID, note: NoteUpdateRequest) -> Note:
        """Update an existing note."""

    def delete_note(note_id: uuid.UUID) -> bool:
        """Delete an existing note."""


class TagQuery(Protocol):
    def get_tag(name: str) -> Optional[TagWithNotes]:
        """Retrieve a tag by its name."""

    def get_tags() -> list[Tag]:
        """Retrieve all tags."""


class TagMutation(TagQuery, Protocol):
    def create_tag(id: TagRequest) -> list[Tag]:
        """Create a new tag."""


class Store(Protocol):
    note: NoteQuery
    tags: TagQuery


class MutableStore(Protocol):
    note: NoteMutation
    tags: TagMutation


class PortsInterface(Protocol):
    @contextlib.contextmanager
    def store(self) -> Generator[Store, None, None]:
        """Read only transactions"""

    @contextlib.contextmanager
    def mutable_store(self) -> Generator[MutableStore, None, None]:
        """Read and mutation transactions"""