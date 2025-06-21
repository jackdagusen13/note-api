from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class Tag(BaseModel):
    id: str
    name: str


class Note(BaseModel):
    id: str
    title: str
    description: str
    tags: Optional[list[Tag]] = None


class TagWithNotes(BaseModel):
    id: str
    name: str
    notes: list[Note]