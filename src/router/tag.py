from fastapi import APIRouter

from src.domain.models import Tag
from src.contexts.note import Ports

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/")
def get_tags() -> list[Tag]:
    ports = Ports()
    with ports.store() as store:
        return store.tag.get_tags()

@router.get("/{tag_id}")
def get_tag(tag_id: str) -> Tag:
    ports = Ports()
    with ports.store() as store:
        tag = store.tag.get_tag(tag_id)
        if not tag:
            raise ValueError(f"Tag with ID {tag_id} not found")
        return tag

@router.post("/")
def create_tag(tag: Tag) -> Tag:
    ports = Ports()
    with ports.mutable_store() as store:
        return store.tag.create_tag(tag)
