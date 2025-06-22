from typing import Optional
import uuid
from src.domain.models import Note, Tag
from src.domain.protocols.note import NoteMutation, TagMutation, TagQuery
from src.domain.requests import NoteRequest, TagRequest
from .schema import NoteRow, TagRow, engine, note_tags_association


from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select, insert, update, delete

SessionLocal = sessionmaker(bind=engine)


class NoteTagsAdapter(NoteMutation, TagMutation, TagQuery, TagMutation):
    def __init__(self, session: Session = SessionLocal()) -> None:
        self._session = session

    def get_note(self, note_id: str) -> Optional[Note]:
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

        return Note.model_validate(note_row, update={"tags": tag_rows})

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
            Note.model_validate(note, update={"tags": tag_map.get(note.id, [])})
            for note in note_rows
        ]


    def create_note(self, note: NoteRequest) -> Note:
            new_note = Note(id=uuid.uuid4(), **note.model_dump())

            if note.tags:
                tag_ids = []
                existing_tags = {
                    tag.name: tag.id
                    for tag in self._session.query(TagRow).filter(TagRow.name.in_([t.name for t in note.tags])).all()
                }

                for tag_data in note.tags:
                    tag_name = tag_data.name
                    if tag_name in existing_tags:
                        tag_ids.append(existing_tags[tag_name])
                    else:
                        new_tag_id = uuid.uuid4()
                        self._session.execute(insert(TagRow).values(id=new_tag_id, name=tag_name))
                        tag_ids.append(new_tag_id)

            self._session.execute(
                insert(NoteRow).values(new_note.model_dump())
            )

            if tag_ids:
                self._session.execute(
                    insert(note_tags_association).values([
                        {"note_id": new_note.id, "tag_id": tag_id} for tag_id in tag_ids
                    ])
                )

            return new_note

    def update_note(self, note_id: uuid.UUID, updated_note: NoteRequest) -> Note:
        update_data = updated_note.model_dump(exclude={"tags"})
        self._session.execute(
            update(NoteRow)
            .where(NoteRow.id == note_id)
            .values(**update_data)
        )

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

    def get_tag(self, id: str) -> list[Tag]:
        """Retrieve tags linked to a specific note ID."""
        results = (
            self._session.query(TagRow)
            .join(note_tags_association, TagRow.id == note_tags_association.c.tag_id)
            .filter(note_tags_association.c.note_id == id)
            .all()
        )
        return [Tag.model_validate(tag) for tag in results]

    def get_tags(self) -> list[Tag]:
        """Retrieve all tags."""
        tags = self._session.query(TagRow).all()
        return [Tag.model_validate(tag) for tag in tags]

    def create_tag(self, tag: TagRequest) -> list[Tag]:
        """Create a new tag."""
        tag_id = uuid.uuid4()
        new_tag = Tag(id=tag_id, **tag.model_dump())
        self._session.execute(
            insert(TagRow).values(id=tag_id, name=new_tag.name)
        )
        self._session.commit()
        return [new_tag]
