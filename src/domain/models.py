import uuid
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class Tag(BaseModel):
    name: str


class Note(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    tags: list[Tag] = []


class TagWithNotes(BaseModel):
    id: uuid.UUID
    name: str
    notes: list[Note] = []