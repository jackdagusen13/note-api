from sqlalchemy import (
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
    Column('note_id', String, ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', String, ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

    notes = relationship('Note', secondary=note_tags_association, back_populates='tags')


class Note(Base):
    __tablename__ = 'notes'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    tags = relationship('Tag', secondary=note_tags_association, back_populates='notes')


engine = create_engine(url="sqlite:///places.db", echo=True)


def get_session_maker() -> sessionmaker:
    insp = inspect(engine)
    return sessionmaker(bind=engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)