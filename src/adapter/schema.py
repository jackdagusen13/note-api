import uuid
from sqlalchemy import (
    UUID,
    Table,
    create_engine,
    String,
    Column,
    ForeignKey,
    inspect,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    """Base Model for Rows"""


note_tags_association = Table(
    'note_tags',
    Base.metadata,
    Column('note_id', UUID, ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', UUID, ForeignKey('tags.id'), primary_key=True)
)

class TagRow(Base):
    __tablename__ = 'tags'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)

    notes = relationship('NoteRow', secondary=note_tags_association, back_populates='tags')


class NoteRow(Base):
    __tablename__ = 'notes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    tags = relationship('TagRow', secondary=note_tags_association, back_populates='notes')


engine = create_engine(url="sqlite:///notes.db", echo=True)


def get_session_maker() -> sessionmaker:
    insp = inspect(engine)
    return sessionmaker(bind=engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)