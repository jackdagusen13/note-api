import contextlib
from typing import Protocol, Optional, Generator

from domain.models import Note, Tag
from domain.requests import NoteRequest, TagRequest


class NoteQuery(Protocol):
    def get_note(note_id: str) -> Optional[Note]:
        """Retrieve a note by its ID."""

    def get_notes() -> list[Note]:
        """Retrieve all notes."""


class NoteMutation(NoteQuery, Protocol):
    def create_note(note: NoteRequest) -> Note:
        """Create a new note."""

    def update_note(note: NoteRequest) -> Note:
        """Update an existing note."""

    def delete_note(self, note_id: str) -> bool:
        """Delete an existing note."""


class TagQuery(Protocol):
    def get_tag(id: str) -> list[Tag]:
        """Retrieve a tag by it note ID."""

    def get_tags() -> list[Note]:
        """Retrieve all tags."""


class TagMutation(Protocol):
    def create_tag(id: TagRequest) -> list[Tag]:
        """Create a new tag."""


class Store(Protocol):
    note: NoteQuery
    tag: TagQuery


class MutableStore(Protocol):
    note: NoteMutation
    tag: TagMutation


class Ports(Protocol):
    @contextlib.contextmanager
    def store(self) -> Generator[Store, None, None]:
        """Read only transactions"""

    @contextlib.contextmanager
    def mutable_store(self) -> Generator[MutableStore, None, None]:
        """Read and mutation transactions"""