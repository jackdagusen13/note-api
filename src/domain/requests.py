from typing import Optional

from pydantic import BaseModel, Tag



class TagRequest(BaseModel):
    name: str


class NoteRequest(BaseModel):
    title: str
    description: str
    tags: Optional[list[TagRequest]] = None
