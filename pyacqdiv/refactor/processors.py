""" Processors for acqdiv corpora
"""

import sys

from sqlalchemy.orm import sessionmaker

from parsers import *
from database_backend import *


# If it turns out that these really don't do anything but the loops, we can get rid of
# the Corp[us|ora]Processor classes and just make them, well, loops. In some function.
class CorporaProcessor(object):
    def process_corpora(self, config):
        for corpus_config in config:
            c = CorpusProcessor(corpus_config)
            c.process_corpus()


class CorpusProcessor(object):
    def __init__(self, cfg, engine):
        self.cfg = cfg
        self.engine = engine

    def process_corpus(self):
        for session_file in self.cfg.session_files:
            print("Processing:", session_file)
            # Create a session based on the format type given in config.
            s = SessionProcessor(self.cfg, session_file, self.engine)
            s.process_session()
            s.commit()


# SessionProcessor invokes a parser to get the extracted data, and then interacts
# with the ORM backend to push data to it.
class SessionProcessor(object):
    # TODO: Does the Session object need a primary key? Is that passed in from the caller
    # (ie, when we know about the Corpus-level data)?
    def __init__(self, cfg, file_path, engine):
        self.config = cfg
        self.file_path = file_path
        self.Session = sessionmaker(bind=engine) # sqla session

    def process_session(self):
        # Init parser with config and pass in file path.
        # Config contains map of standard label -> local label.
        self.parser = SessionParser.create_parser(self.config, self.file_path)

        # Now start asking the parser for stuff...
        # For example:

        # Session table stuff in db (metadata)
        # session_metadata = self.parser.get_session_metadata()

        # Speakers table stuff in db
        # TODO(stiv): Define Speaker table
        """
        speakers = []
        for s in self.parser.next_speaker():
            # TODO(stiv): Do we also need to add some kind of key for joining to the s?
            speakers.append(s)

        # TODO(stiv): Need to add to each utterance some kind of joining key.
        # I think it makes sense to construct/add it here, since this is where
        # we do database stuff, and not in the parser (there's no reason the parser
        # should have to know about primary keys - it's a parser, not a db)
        utterances = []
        for u in self.parser.next_utterance():
            utterances.append(u)
        # Then write it to the backend.
        commit(session_metadata, speakers, utterances)
        """

    def commit(self):
    # def commit(self, session_metadata, speakers, utterances):
        # Set up the connection to the backend.
        # TODO(stiv): Put some kind of namespace on the db session stuff, to distinguish
        # it from the recording sessions. Sessions, sessions everywhere!

        # TODO: figure out what goes where why: http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
        # engine = create_engine('dbms://user:pwd@host/dbname')
        # engine = create_engine('sqlite:///_corpora.sqlite3', echo=False)
        # Base.metadata.create_all(engine)
        # SessionMaker = sessionmaker(bind=engine)

        session = self.Session()

        session_entry = Session(session_id=self.file_path)
        speaker_entries = []
        for i in range(0, 10):
            # fuck... do we really have to do this FK assignment "manually"??
            speaker_entry = Speaker(parent_id=self.file_path, speaker_label="CHI"+str(i), speaker_name="Child"+str(i))
            speaker_entries.append(speaker_entry)

        # entry = Speaker(**item)
        # self.db_session = SessionMaker()

        try:
            session.add(session_entry)
            session.add_all(speaker_entries)
            session.commit()
            # self.db_session.add(session_metadata)
            # self.db_session.add_all(self.speakers)
            # self.db_session.add_all(utterances)
            # self.db_session.commit()
        except:
            # TODO: print some error message? log it?
            # self.db_session.rollback()
            session.rollback()
            raise
        finally:
            session.close()

# can we return from the metadata parser some json object, etc., that we can then
# unpack for session.add_all ?

"""
>>> session.add_all([
...     User(name='wendy', fullname='Wendy Williams', password='foobar'),
...     User(name='mary', fullname='Mary Contrary', password='xxg527'),
...     User(name='fred', fullname='Fred Flinstone', password='blah')])
"""

