"""Model for the ACQDIV database."""

from sqlalchemy import (Text, Column, Integer, Boolean, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Corpus(Base):
    """Model for the corpus."""
    __tablename__ = 'corpora'

    id = Column(Text, primary_key=True)
    language = Column(Text)
    iso_639_3 = Column(Text)
    glottolog_code = Column(Text)
    owner = Column(Text)
    acronym = Column(Text)
    name = Column(Text)


class Session(Base):
    """Model for the session."""
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    corpus = Column(Text, ForeignKey('corpora.id'))
    source_id = Column(Text, nullable=False)
    media_id = Column(Text)
    date = Column(Text)
    duration = Column(Integer)
    # SQLAlchemy relationship definitions:
    speakers = relationship('Speaker', backref='Session')
    utterances = relationship('Utterance', backref='Session')
    words = relationship('Word', backref='Session')
    morphemes = relationship('Morpheme', backref='Session')


class Speaker(Base):
    """Model for the session speaker."""
    __tablename__ = 'speakers'

    id = Column(Integer, primary_key=True)
    session_id_fk = Column(Integer, ForeignKey('sessions.id'))
    uniquespeaker_id_fk = Column(Integer, ForeignKey('uniquespeakers.id'))
    age_raw = Column(Text)
    age = Column(Text)
    age_in_days = Column(Integer)
    role_raw = Column(Text)
    role = Column(Text)
    macrorole = Column(Text)
    languages_spoken = Column(Text)


class UniqueSpeaker(Base):
    """Model for the unique speaker across all corpora."""
    __tablename__ = 'uniquespeakers'

    id = Column(Integer, primary_key=True)
    speaker_label = Column(Text)
    name = Column(Text)
    birthdate = Column(Text)
    gender = Column(Text)
    corpus = Column(Integer, ForeignKey('corpora.id'))


class Utterance(Base):
    """Model for the utterance of a session."""
    __tablename__ = 'utterances'

    id = Column(Integer, primary_key=True)
    session_id_fk = Column(Integer, ForeignKey('sessions.id'))
    source_id = Column(Text)
    speaker_id_fk = Column(Integer, ForeignKey('speakers.id'))
    addressee_id_fk = Column(Integer, ForeignKey('speakers.id'))
    utterance_raw = Column(Text)
    utterance = Column(Text)
    translation = Column(Text)
    morpheme = Column(Text)
    gloss_raw = Column(Text)
    pos_raw = Column(Text)
    sentence_type = Column(Text)
    childdirected = Column(Boolean)
    start = Column(Text)
    end = Column(Text)
    start_raw = Column(Text)
    end_raw = Column(Text)
    comment = Column(Text)
    # SQLAlchemy relationship definitions:
    words = relationship('Word', backref='Utterance')
    morphemes = relationship('Morpheme', backref='Utterance')


class Word(Base):
    """Model for the word of an utterance."""
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    utterance_id_fk = Column(Integer, ForeignKey('utterances.id'))
    language = Column(Text)
    word = Column(Text)
    pos = Column(Text)
    pos_ud = Column(Text)
    word_actual = Column(Text)
    word_target = Column(Text)
    # SQLAlchemy relationship definitions:
    morphemes = relationship('Morpheme', backref='Word')


class Morpheme(Base):
    """Model for the morpheme of an utterance."""
    __tablename__ = 'morphemes'

    id = Column(Integer, primary_key=True)
    utterance_id_fk = Column(Integer, ForeignKey('utterances.id'))
    word_id_fk = Column(Integer, ForeignKey('words.id'))
    language = Column(Text)
    type = Column(Text)
    morpheme = Column(Text)
    gloss_raw = Column(Text)
    gloss = Column(Text)
    pos_raw = Column(Text)
    pos = Column(Text)
    lemma_id = Column(Text)
