import contextlib
from dataclasses import dataclass
from typing import Generator
from src.adapter.note_adapter import NoteTagsAdapter
from src.domain.protocols.note import MutableStore, NoteMutation, NoteQuery, PortsInterface, TagMutation, TagQuery
from src.adapter.schema import get_session_maker
from sqlalchemy.orm import Session

@dataclass
class Store:
    session: Session

    @property
    def note(self) -> NoteQuery:
        return NoteTagsAdapter(self.session)

    @property
    def tags(self) -> TagQuery:
        return NoteTagsAdapter(self.session)


@dataclass
class MutableStore:
    session: Session

    @property
    def note(self) -> NoteMutation:
        return NoteTagsAdapter(self.session)

    @property
    def tags(self) -> TagMutation:
        return NoteTagsAdapter(self.session)


class PortsImpl(PortsInterface):
    def __init__(self) -> None:
        self._session_maker = get_session_maker()

    @contextlib.contextmanager
    def store(self) -> Generator[Store, None, None]:
        with self._session_maker.begin() as session:
            yield Store(session=session)

    @contextlib.contextmanager
    def mutable_store(self) -> Generator[MutableStore, None, None]:
        with self._session_maker.begin() as session:
            yield MutableStore(session=session)