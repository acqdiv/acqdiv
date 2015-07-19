""" Processors for acqdiv corpora
"""

# If it turns out that these really don't do anything but the loops, we can get rid of
# the Corp[us|ora]Processor classes and just make them, well, loops. In some function.
class CorporaProcessor(object):
    def process_corpora(self, config):
        for corpus_config in config:
            c = Corpus(corpus_config)
            c.process_corpus()


class CorpusProcessor(object):
    def __init__(self, config):
        self.config = config

    def process_corpus(self):
        for session_config in self.config:
        # Create a session based on the format type given in config.
        s = SessionProcessor(session_config)
        s.process()


# SessionProcessor invokes a parser to get the extracted data, and then interacts
# with the ORM backend to push data to it.
class SessionProcessor(object):
    # TODO: Does the Session object need a primary key? Is that passed in from the caller
    # (ie, when we know about the Corpus-level data)?
    def __init__(self, config):
        self.config = config

    def process_session(self):
        # Init parser with config.
        # config contains map of standard label -> local label.
        self.parser = SessionParser.create_parser(self.config)
        # Now start asking the parser for stuff...
        # For example:

        # Session table stuff in db (metadata)
        session_metadata = self.parser.get_session_metadata()

        # Speakers table stuff in db
        # TODO(stiv): Define Speaker table
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

    def commit(self, session_metadata, speakers, utterances):
        # Set up the connection to the backend.
        # TODO(stiv): Put some kind of namespace on the db session stuff, to distinguish
        # it from the recording sessions. Sessions, sessions everywhere!
        # engine = create_engine('dbms://user:pwd@host/dbname')
        engine = create_engine('sqlite:///_corpora.sqlite3', echo=False)
        Base.metadata.create_all(engine)
        SessionMaker = sessionmaker(bind=engine)
        self.db_session = SessionMaker()
        try:
            self.db_session.add(session_metadata)
            self.db_session.add_all(speakers)
            self.db_session.add_all(utterances)
            self.db_session.commit()
        except:
            # TODO: print some error message?
            self.db_session.rollback()
