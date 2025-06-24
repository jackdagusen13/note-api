from fastapi import APIRouter, HTTPException, Query

from src.domain import service
from src.domain.models import Tag, TagWithNotes
from src.contexts.note import PortsImpl

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=TagWithNotes)
def get_tag(name: str = Query()) -> TagWithNotes:
    ports = PortsImpl()
    tag = service.get_tag(ports, name)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.get("/all", response_model=list[Tag], )
def get_tags() -> list[Tag]:
    ports = PortsImpl()
    return service.get_all_tags(ports)

@router.post("/")
def create_tag(tag: Tag) -> Tag:
    ports = PortsImpl()
    return service.create_tag(ports, tag)
