import contextlib
from typing import Generator
from domain.protocols.note import MutableStore, Ports as PortsInterface, Store
from src.adapter.schema import get_session_maker

class Ports(PortsInterface):
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