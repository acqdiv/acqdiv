""" ORM declarations, database table definitions """

# TODO: set the correct values nullable, unique, etc.
# TODO: pull out the Speakers from Session info into a separate table
# TODO: create the links between the database tables
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#eager-loading
# NOTE: apparently sqla Base objects do not need constructors; they seem to be discouraged

from sqlalchemy import create_engine, Text, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import _declarative_constructor

from sqlalchemy.engine.url import URL

Base = declarative_base()
# DeclarativeBase = declarative_base()

def db_connect():
    """ Performs database connection. We can add a database settings
    in settings.py later. Returns sqlalchemy engine instance.
    """
    # TODO: if we want to add postgres settings and change to postgres
    # return create_engine(URL(**settings.DATABASE))
    return create_engine('sqlite:///_acqdiv.sqlite3', echo=False)

def create_tables(engine):
    """ """
    # Drop all the database tables first
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)

class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    # session_id = Column(Text, nullable=True, unique=False)
    session_id = Column(Text, nullable=False, unique=False) # filename
    language = Column(Text, nullable=True, unique=False)
    corpus = Column(Text, nullable=True, unique=False)
    date = Column(Text, nullable=True, unique=False)
    genre = Column(Text, nullable=True, unique=False)
    situation = Column(Text, nullable=True, unique=False)
    # this stuff seems mostly blank because we are not extracing metadata from the .cdc files
    # address = Column(Text, nullable=True, unique=False)
    # continent = Column(Text, nullable=True, unique=False)
    # country = Column(Text, nullable=True, unique=False)
    transcript_id = Column(Text, nullable=True, unique=False) # original file name via ID in XML files (Chintang, Cree, Indonesian & Russian)

    # foreign relationships
    speakers = relationship('Speaker', backref='session') #, lazy='dynamic')


class Speaker(Base):
    # TODO: we will have to make a link between speakers and speakers in each session/record/utterance
    __tablename__ = 'speaker'

    id = Column(Integer, primary_key=True)
    session_id_fk = Column(Integer, ForeignKey('session.session_id'))
    # label = Column(Text, nullable=True, unique=False)
    # TODO: add speaker id
    speaker_id = Column(Text, nullable=True, unique=False)
    name = Column(Text, nullable=True, unique=False)
    age = Column(Text, nullable=True, unique=False)
    age_in_days = Column(Integer, nullable=True, unique=False)
    gender = Column(Text, nullable=True, unique=False)
    role = Column(Text, nullable=True, unique=False)
    language = Column(Text, nullable=True, unique=False)
    birthdate = Column(Text, nullable=True, unique=False)

    # optional pretty formatting
    def __repr__(self):
        return "Speaker(%s)" % (self.name)


class Utterance(Base):
    __tablename__ = 'utterance'

    id = Column(Integer, primary_key=True)
    session_id_fk = Column(Text, ForeignKey('session.session_id'))
    corpus = Column(Text, nullable=True, unique=False) # for sorting convenience
    utterance_id = Column(Text, nullable=True, unique=False) # utterance id in original file
    utterance_type = Column(Text, nullable=True, unique=False) # phonetic or orthographic
    utterance = Column(Text, nullable=True, unique=False) # original utterance
    utterance_cleaned = Column(Text, nullable=True, unique=False) # our cleaned-up utterance
    morpheme = Column(Text, nullable=True, unique=False) # morpheme line
    word = Column(Text, nullable=True, unique=False) # words line? what is Robert's "full_word"?
    pos = Column(Text, nullable=True, unique=False) # parts of speech line
    speaker_id = Column(Text, nullable=True, unique=False)
    # speaker_label = Column(Text, nullable=True, unique=False) # -> speaker_id
    u_orthographic = Column(Text, nullable=True, unique=False) # orthographic utterance
    u_phonetic = Column(Text, nullable=True, unique=False) # phonetic utterance
    sentence_type = Column(Text, nullable=True, unique=False)
    translation = Column(Text, nullable=True, unique=False)
    timestamp_start = Column(Text, nullable=True, unique=False)
    timestamp_end = Column(Text, nullable=True, unique=False)
    comment = Column(Text, nullable=True, unique=False)
    addressee = Column(Text, nullable=True, unique=False) # exists at least in Russian
    gloss = Column(Text, nullable=True, unique=False) # what to do with the "gloss"?
    warnings = Column(Text, nullable=True, unique=False) # Robert's warnings!

    #Morphemes = sa.Column(sa.Text, nullable=False, unique=False) # concatenated MorphemeIDs per utterance
    #Words = sa.Column(sa.Text, nullable=False, unique=True) # concatenated WordIDs per utterance

    #Session = sa.relationship('Session', backref=backref('Utterances', order_by=id))

class Word(Base):
    # TODO: should we do unique word id assignment in post-processing?
    __tablename__ = 'words'

    # fk...
    # SessionID = sa.Column(sa.Text, nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    utterance_id_fk = Column(Text, ForeignKey('utterance.id'))
    corpus = Column(Text, nullable=True, unique=False) # for sorting convenience
    #Utterance = relationship('Utterance',  backref=backref('Words', order_by=ID))
    word = Column(Text, nullable=True, unique=False)
    word_target = Column(Text, nullable=True, unique=False)
    warnings = Column(Text, nullable=True, unique=False)
    # TODO: get unique words and assign ids in the postprocessor
    word_id = Column(Text, nullable=True, unique=False)



class Morpheme(Base):
    __tablename__ = 'morphemes'

    # fk...
    # SessionID = sa.Column(sa.Text, nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
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
    # TODO: get unique morphemes and assign ids in the postprocessor
    morpheme_id = Column(Text, nullable=True, unique=False)



class Warnings(Base):
    # Table for warnings found in parsing (should be record/multiple levels?)
    # Types of data errors in Toolbox files from Toolbox parsing:
    # missing records (/ref)

    __tablename__ = 'warnings'

    #id = Column(Text, primary_key=True) ## @bambooforest Is that a mistake?
    id = Column(Integer,primary_key=True)
    corpus = Column(Text, nullable=True, unique=False)
    parent_id = Column(Text, ForeignKey('utterance.id'))
    warning = Column(Text, nullable=True, unique=False)
