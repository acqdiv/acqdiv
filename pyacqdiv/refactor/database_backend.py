""" ORM declarations, database table definitions """

# TODO: set the correct values nullable, unique, etc.
# TODO: pull out the Speakers from Session info into a separate table
# TODO: create the links between the database tables
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#eager-loading

from sqlalchemy import create_engine, Text, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import _declarative_constructor

from sqlalchemy.engine.url import URL

Base = declarative_base()
# DeclarativeBase = declarative_base()

def db_connect():
    """ Performs database connection. We can add a database settings
    from settings.py later. Returns sqlalchemy engine instance.
    """
    # TODO: add postgres settings and change to postgres
    # return create_engine(URL(**settings.DATABASE))
    return create_engine('sqlite:///_acqdiv.sqlite3', echo=False)

def create_tables(engine):
    """ """
    # Drop all the database tables first
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)

# NOTE: apparently sqla Base objects do not need constructors; they seem to be discouraged

class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    # session_id = Column(Text, nullable=True, unique=False)
    session_id = Column(Text, nullable=False, unique=False)
    transcript_id = Column(Text, nullable=True, unique=False)
    language = Column(Text, nullable=True, unique=False)
    corpus = Column(Text, nullable=True, unique=False)
    date = Column(Text, nullable=True, unique=False)
    genre = Column(Text, nullable=True, unique=False)
    situation = Column(Text, nullable=True, unique=False)
    address = Column(Text, nullable=True, unique=False)
    continent = Column(Text, nullable=True, unique=False)
    country = Column(Text, nullable=True, unique=False)

    # foreign relationships
    speakers = relationship('Speaker', backref='session') #, lazy='dynamic')


class Speaker(Base):
    # TODO: we will have to make a link between speakers and speakers in each session/record/utterance

    __tablename__ = 'speaker'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('session.session_id'))
    label = Column(Text, nullable=True, unique=False)
    name = Column(Text, nullable=True, unique=False)
    # age_in_days = Column(Integer, nullable=True, unique=False)
    age = Column(Text, nullable=True, unique=False)
    birthdate = Column(Text, nullable=True, unique=False)
    gender = Column(Text, nullable=True, unique=False)
    role = Column(Text, nullable=True, unique=False)
    language = Column(Text, nullable=True, unique=False)

    # optional pretty formatting
    def __repr__(self):
        return "Speaker(%s)" % (self.name)


class Utterance(Base):
    __tablename__ = 'utterance'

    id = Column(Integer, primary_key=True)
    corpus = Column(Text, nullable=True, unique=False) # for sorting convenience
    # should probably be called:
    # session_id = Column(Text, ForeignKey('session.session_id'))
    parent_id = Column(Text, ForeignKey('session.session_id'))
    warnings = Column(Text, nullable=True, unique=False) # Robert's warnings!
    utterance_id = Column(Text, nullable=True, unique=False)
    utterance_type = Column(Text, nullable=True, unique=False)
    utterance = Column(Text, nullable=True, unique=False)
    utterance_cleaned = Column(Text, nullable=True, unique=False)
    morpheme = Column(Text, nullable=True, unique=False) # morpheme line
    word = Column(Text, nullable=True, unique=False) # words line? what is Robert's "full_word"?
    pos = Column(Text, nullable=True, unique=False) # parts of speech line
    speaker_id = Column(Text, nullable=True, unique=False)
    speaker_label = Column(Text, nullable=True, unique=False)
    u_orthographic = Column(Text, nullable=True, unique=False) # orthographic utterance
    u_phonetic = Column(Text, nullable=True, unique=False) # phonetic utterance
    sentence_type = Column(Text, nullable=True, unique=False)
    translation = Column(Text, nullable=True, unique=False)
    timestamp_start = Column(Text, nullable=True, unique=False)
    timestamp_end = Column(Text, nullable=True, unique=False)
    comment = Column(Text, nullable=True, unique=False)
    addressee = Column(Text, nullable=True, unique=False) # exists at least in Russian
    gloss = Column(Text, nullable=True, unique=False) # what to do with the "gloss"?


    #Morphemes = sa.Column(sa.Text, nullable=False, unique=False) # concatenated MorphemeIDs per utterance
    #Words = sa.Column(sa.Text, nullable=False, unique=True) # concatenated WordIDs per utterance

    #Session = sa.relationship('Session', backref=backref('Utterances', order_by=id))

class Word(Base):
    # TODO: should we do unique word id assignment in post-processing?
    __tablename__ = 'words'

    # fk...
    # SessionID = sa.Column(sa.Text, nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    # SM: i'm thinking the word_id is redundant if it's just session|utterance + id counter
    # TODO: see postprocessor.py
    word_id = Column(Text, nullable=True, unique=False)
    word = Column(Text, nullable=True, unique=False)
    word_target = Column(Text, nullable=True, unique=False)
    parent_id = Column(Text, ForeignKey('utterance.id'))
    #Utterance = relationship('Utterance',  backref=backref('Words', order_by=ID))
    # TODO: double check that we're all using the same warning|s
    warning = Column(Text, nullable=True, unique=False)
    warnings = Column(Text, nullable=True, unique=False)

class Morpheme(Base):
    __tablename__ = 'morphemes'

    # fk...
    # SessionID = sa.Column(sa.Text, nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    # TODO: see postprocessor.py
    morpheme_id = Column(Text, nullable=True, unique=False)
    parent_id = Column(Text, ForeignKey('utterance.id'))
    morpheme = Column(Text, nullable=True, unique=False)
    morpheme_target = Column(Text, nullable=True, unique=False)
    gloss = Column(Text, nullable=True, unique=False)
    clean_gloss = Column(Text, nullable=True, unique=False)
    gloss_target = Column(Text, nullable=True, unique=False)
    pos = Column(Text, nullable=True, unique=False)
    pos_target = Column(Text, nullable=True, unique=False)
    segment = Column(Text, nullable=True, unique=False)
    segment_target = Column(Text, nullable=True, unique=False)

class Warnings(Base):
    # Table for warnings found in parsing (should be record/multiple levels?)
    # Types of data errors in Toolbox files from Toolbox parsing:
    # missing records (/ref)

    __tablename__ = 'warnings'

    id = Column(Text, primary_key=True)
    parent_id = Column(Text, ForeignKey('utterance.id'))
    warning = Column(Text, nullable=True, unique=False)
