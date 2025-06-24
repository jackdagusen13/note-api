from typing import Optional
import uuid
from src.domain.models import Note, Tag, TagWithNotes
from src.domain.protocols.note import NoteMutation, TagMutation
from src.domain.requests import NoteRequest, NoteUpdateRequest, TagRequest
from .schema import NoteRow, TagRow, engine, note_tags_association


from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import insert, update
from sqlalchemy.orm import joinedload

SessionLocal = sessionmaker(bind=engine)


class NoteTagsAdapter(NoteMutation, TagMutation):
    def __init__(self, session: Session = SessionLocal()) -> None:
        self._session = session

    def get_note(self, note_id: uuid.UUID) -> Optional[Note]:
        note_row = (
            self._session.query(NoteRow)
            .filter(NoteRow.id == note_id)
            .first()
        )

        if not note_row:
            return None

        tag_rows = (
            self._session.query(TagRow)
            .join(note_tags_association, TagRow.id == note_tags_association.c.tag_id)
            .filter(note_tags_association.c.note_id == note_id)
            .all()
        )

        note_row.tags = tag_rows

        return Note.model_validate(note_row, from_attributes=True)

    def get_notes(self) -> list[Note]:
        note_rows = self._session.query(NoteRow).all()

        note_tag_pairs = (
            self._session.query(note_tags_association.c.note_id, TagRow)
            .join(TagRow, TagRow.id == note_tags_association.c.tag_id)
            .all()
        )

        from collections import defaultdict
        tag_map = defaultdict(list)
        for note_id, tag in note_tag_pairs:
            tag_map[note_id].append(tag)

        return [
            Note.model_validate(note, from_attributes=True).model_copy(update={"tags": tag_map.get(note.id, [])})
            for note in note_rows
        ]

    def create_note(self, request: NoteRequest) -> Note:
        new_note_id = uuid.uuid4()
        new_note = Note(id=new_note_id, **request.model_dump())

        self._session.execute(
            insert(NoteRow).values(
                id=new_note.id,
                title=new_note.title,
                description=new_note.description
            )
        )

        tag_ids = []
        if request.tag_names:
            for tag_name in request.tag_names:
                tag_row = self._session.query(TagRow).filter(TagRow.name == tag_name).first()
                if not tag_row:
                    tag_id = uuid.uuid4()
                    tag_row = TagRow(id=tag_id, name=tag_name)
                    self._session.add(tag_row)

                tag_ids.append(tag_row.id)
                self._session.execute(
                    note_tags_association.insert().values(note_id=new_note_id, tag_id=tag_row.id)
                )

        note_request = self.get_note(new_note_id)

        self._session.commit()

        return note_request


    def update_note(self, note_id: uuid.UUID, updated_note: NoteUpdateRequest) -> Note:
        # Update note fields
        update_values = {}
        if updated_note.title is not None:
            update_values["title"] = updated_note.title
        if updated_note.description is not None:
            update_values["description"] = updated_note.description

        if update_values:
            self._session.execute(
            update(NoteRow)
            .where(NoteRow.id == note_id)
            .values(**update_values)
            )

        if updated_note.tag_names:
            # Remove existing associations
            self._session.execute(
                note_tags_association.delete().where(note_tags_association.c.note_id == note_id)
            )

            for tag_name in updated_note.tag_names:
                tag_row = self._session.query(TagRow).filter(TagRow.name == tag_name).first()
                if not tag_row:
                    tag_id = uuid.uuid4()
                    self._session.execute(
                        insert(TagRow).values(id=tag_id, name=tag_name)
                    )
                    tag_row = self._session.query(TagRow).filter(TagRow.id == tag_id).first()
                self._session.execute(
                    note_tags_association.insert().values(note_id=note_id, tag_id=tag_row.id)
                )

        commited_note = self.get_note(note_id)
        self._session.commit()

        return commited_note

    def delete_note(self, note_id: str) -> bool:
        note = self._session.query(NoteRow).filter(NoteRow.id == note_id).first()
        if not note:
            return False

        self._session.execute(
            note_tags_association.delete().where(note_tags_association.c.note_id == note_id)
        )

        self._session.delete(note)
        self._session.commit()
        return True

    def get_tag(self, name: str) -> Optional[TagWithNotes]:
        tag_row = (
            self._session.query(TagRow)
            .options(joinedload(TagRow.notes))
            .filter(TagRow.name == name)
            .first()
        )
        if not tag_row:
            return None

        notes = [
            Note(
                id=note.id,
                title=note.title,
                description=note.description,
                tags=[Tag(name=t.name) for t in note.tags]
            )
            for note in tag_row.notes
        ]

        return TagWithNotes(
            id=tag_row.id,
            name=tag_row.name,
            notes=notes
        )

    def get_tags(self) -> list[Tag]:
        """Retrieve all tags."""
        tags = self._session.query(TagRow).all()
        return [Tag.model_validate(tag.__dict__) for tag in tags]

    def create_tag(self, tag: TagRequest) -> list[Tag]:
        """Create a new tag."""
        tag_id = uuid.uuid4()
        new_tag = Tag(id=tag_id, **tag.model_dump())
        self._session.execute(
            insert(TagRow).values(id=tag_id, name=new_tag.name)
        )
        self._session.commit()
        return [new_tag]
