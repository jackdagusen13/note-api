from typing import Optional

from pydantic import BaseModel, Tag



class TagRequest(BaseModel):
    name: str


class NoteRequest(BaseModel):
    title: str
    description: str
    tag_names: list[str] = []


class NoteUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tag_names: list[str] = []