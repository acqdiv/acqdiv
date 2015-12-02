""" ORM declarations, database table definitions

TODO: investigate:

http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#eager-loading

from sqlalchemy.ext.declarative.api import _declarative_constructor
from sqlalchemy.engine.url import URL

"""

from sqlalchemy import create_engine, Text, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def db_connect():
    """ Performs database connection.

    We can add a database settings in settings.py, e.g. for postgres: return create_engine(URL(**settings.DATABASE))

    Returns:
        sqlalchemy engine instance
    """
    return create_engine('sqlite:///_acqdiv.sqlite3', echo=False)


def create_tables(engine):
    """ Drops all databases before creating them.

        Args:
            engine: a sqlalchemy database engine
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)


class Session(Base):
    """ Sessions table.

    Each input file is a row. To note:
        - session_id field is the input filename
        - source_id field is the id given in the session file
        - media field is an associate media file by filename
    """
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    session_id = Column(Text, nullable=False, unique=False)
    corpus = Column(Text, nullable=True, unique=False)
    language = Column(Text, nullable=True, unique=False)
    date = Column(Text, nullable=True, unique=False)
    source_id = Column(Text, nullable=True, unique=False)
    media = Column(Text, nullable=True, unique=False)
    media_type = Column(Text, nullable=True, unique=False)
    speakers = relationship('Speaker', backref='session') #, lazy='dynamic')


class Speaker(Base):
    """ Speaker table; each row is a speaker in a session. Speakers may appear in > 1 session
    """
    __tablename__ = 'speakers'

    id = Column(Integer, primary_key=True)
    session_id_fk = Column(Integer, ForeignKey('sessions.id'))
    corpus = Column(Text, nullable=True, unique=False)
    language = Column(Text, nullable=True, unique=False)
    speaker_label = Column(Text, nullable=True, unique=False)
    name = Column(Text, nullable=True, unique=False)
    age_raw = Column(Text, nullable=True, unique=False)
    age = Column(Text, nullable=True, unique=False)
    age_in_days = Column(Integer, nullable=True, unique=False)
    gender_raw = Column(Text, nullable=True, unique=False)
    gender = Column(Text, nullable=True, unique=False)
    role_raw = Column(Text, nullable=True, unique=False)
    role = Column(Text, nullable=True, unique=False)
    macrorole = Column(Text, nullable=True, unique=False)
    languages_spoken = Column(Text, nullable=True, unique=False)
    birthdate = Column(Text, nullable=True, unique=False)

    # TODO: optional pretty formatting for printing
    def __repr__(self):
        return "Speaker(%s)" % (self.name)

class Unique_Speaker(Base):
    """ Unique speakers across all corpora
    """
    __tablename__ = 'uniquespeakers'

    id = Column(Integer, primary_key=True)
    global_id = Column(Text, nullable=True, unique=False)
    speaker_label = Column(Text, nullable=True, unique=False)
    name = Column(Text, nullable=True, unique=False)
    birthdate = Column(Text, nullable=True, unique=False)
    gender = Column(Text, nullable=True, unique=False)
    corpus = Column(Text, nullable=True, unique=False)

class Utterance(Base):
    """ Utterances in all sessions.

    To note:
        - utterance_id is the id in the original files (not unique across corpora, e.g. u1, u1)
        - addressee not in all corpora
        - _raw vs !_raw is distinction between original input and cleaned/manipulated output
    """
    __tablename__ = 'utterances'

    id = Column(Integer, primary_key=True)
    session_id_fk = Column(Text, ForeignKey('sessions.id'))
    corpus = Column(Text, nullable=True, unique=False)
    language = Column(Text, nullable=True, unique=False)
    utterance_id = Column(Text, nullable=True, unique=False)
    speaker_label = Column(Text, nullable=True, unique=False)
    addressee = Column(Text, nullable=True, unique=False)
    utterance_raw = Column(Text, nullable=True, unique=False)
    utterance = Column(Text, nullable=True, unique=False)
    translation = Column(Text, nullable=True, unique=False)
    sentence_type = Column(Text, nullable=True, unique=False)
    start = Column(Text, nullable=True, unique=False)
    end = Column(Text, nullable=True, unique=False)
    start_raw = Column(Text, nullable=True, unique=False)
    end_raw = Column(Text, nullable=True, unique=False)
    word = Column(Text, nullable=True, unique=False)
    morpheme = Column(Text, nullable=True, unique=False)
    gloss_raw = Column(Text, nullable=True, unique=False)
    pos_raw = Column(Text, nullable=True, unique=False)
    comment = Column(Text, nullable=True, unique=False)
    warning = Column(Text, nullable=True, unique=False)


class Word(Base):
    """ Words table.

    TODO: get unique words and assign ids in the postprocessor
    """
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    session_id_fk = Column(Text, ForeignKey('sessions.id'))
    utterance_id_fk = Column(Text, ForeignKey('utterances.id'))
    corpus = Column(Text, nullable=True, unique=False)
    language = Column(Text, nullable=True, unique=False)
    word = Column(Text, nullable=True, unique=False)
    word_actual = Column(Text, nullable=True, unique=False)
    word_target = Column(Text, nullable=True, unique=False)
    warning = Column(Text, nullable=True, unique=False)
    # Utterance = relationship('Utterance',  backref=backref('Words', order_by=ID))


class Morpheme(Base):
    """ Morphemes table
    """
    __tablename__ = 'morphemes'

    id = Column(Integer, primary_key=True)
    session_id_fk = Column(Text, ForeignKey('sessions.id'))
    utterance_id_fk = Column(Text, ForeignKey('utterances.id'))
    corpus = Column(Text, nullable=True, unique=False)
    language = Column(Text, nullable=True, unique=False)
    type = Column(Text, nullable=True, unique=False)
    morpheme = Column(Text, nullable=True, unique=False)
    gloss_raw = Column(Text, nullable=True, unique=False)
    gloss = Column(Text, nullable=True, unique=False)
    pos_raw = Column(Text, nullable=True, unique=False)
    pos = Column(Text, nullable=True, unique=False)


class Warnings(Base):
    """ Warnings found during parsing
    """
    __tablename__ = 'warnings'

    id = Column(Integer,primary_key=True)
    corpus = Column(Text, nullable=True, unique=False)
    utterance_id_fk = Column(Text, ForeignKey('utterances.id'))
    warning = Column(Text, nullable=True, unique=False)
