""" Processors for acqdiv corpora
"""

import sys
import itertools as it

from sqlalchemy.orm import sessionmaker

from parsers import *
from database_backend import *


# If it turns out that these really don't do anything but the loops, we can get rid of
# the Corp[us|ora]Processor classes and just make them, well, loops. In some function.
# class CorporaProcessor(object):
#    def process_corpora(self, config):
#        for corpus_config in config:
#            c = CorpusProcessor(corpus_config)
#            c.process_corpus()


class CorpusProcessor(object):
    """ Handler for processing each session file in particular corpus
    """
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


class SessionProcessor(object):
    """ SessionProcessor invokes a parser to get the extracted data, and then interacts
        with the ORM backend to push data to it.
    """
    # TODO: Does the Session object need a primary key? Is that passed in from the caller
    # (ie, when we know about the Corpus-level data)?

    def __init__(self, cfg, file_path, engine):
        # Init parser with corpus config. Pass in file path to process. Create sqla session.
        self.config = cfg
        self.file_path = file_path
        self.language = self.config['corpus']['language']
        self.corpus = self.config['corpus']['corpus']
        self.format = self.config['corpus']['format']

        # attach session file path to config
        filename = os.path.splitext(os.path.basename(self.file_path))[0]
        self.config.set('paths', 'filename', filename)

        # start up db session
        self.Session = sessionmaker(bind=engine)


    def process_session(self):
        # Config contains map of standard label -> local label.
        self.parser = SessionParser.create_parser(self.config, self.file_path)

        # Now start asking the parser for stuff...

        # Get session metadata via labels defined in corpus config and create Session instance
        # TODO: deal with IMDI's dict in dict encoding of location:
        # address = session_metadata['location']['address'],
        # continent = session_metadata['location']['continent'],
        # country = session_metadata['location']['country']
        session_metadata = self.parser.get_session_metadata()
        d = {}
        for k, v in self.config['session_labels'].items():
            d[k] = session_metadata[v]
        d['session_id'] = self.file_path
        self.session_entry = Session(**d)

        # Get speaker metadata
        self.speaker_entries = []
        for speaker in self.parser.next_speaker():
            d = {}
            for k, v in self.config['speaker_labels'].items():
                d[k] = speaker[v]
            d['parent_id'] = self.file_path
            self.speaker_entries.append(Speaker(**d))

        # Body parsing
        if self.format == "Toolbox":
            self.utterances = []
            for utterance in self.parser.next_utterance():
                self.utterances.append(Utterance(**utterance))

        # TODO(stiv): Need to add to each utterance some kind of joining key.
        # I think it makes sense to construct/add it here, since this is where
        # we do database stuff, and not in the parser (there's no reason the parser
        # should have to know about primary keys - it's a parser, not a db)

        elif self.format == "ChatXML":
            #TODO(chysi): this doesn't look like a generator to me!!!
            self.utterances = []
            self.words = []
            self.morphemes = []
            for u, words, morphemes in self.parser.next_utterance():
                u.parent_id = self.file_path
                #TODO: u.ids counted per session
                # we need a better way of making them unique across corpora
                #dirty, dirty hack:
                u.utterance_id = u.parent_id + "_" + u.utterance_id
                self.utterances.append(u)

                for w, m, i in it.takewhile(lambda x: x[0] and x[1], it.zip_longest(words(u), morphemes(u), it.count())):
                    w.parent_id = u.utterance_id
                    w.word_id = u.utterance_id + 'w' + str(i)
                    self.words.append(w)
                    m.parent_id = u.utterance_id
                    m.morpheme_id = u.utterance_id + 'm' + str(i)
                    self.morphemes.append(m)

        else:
            raise Exception("Error: unknown corpus format!")

        # Then write it to the backend.
        # commit(session_metadata, speakers, utterances)


    def commit(self):
        # def commit(self, session_metadata, speakers, utterances):
        # TODO(stiv): Put some kind of namespace on the db session stuff, to distinguish
        # it from the recording sessions. Sessions, sessions everywhere!
        session = self.Session()

        # entry = Speaker(**item)
        # self.db_session = SessionMaker()

        try:
            session.add(self.session_entry)
            session.add_all(self.speaker_entries)
            session.add_all(self.utterances)
            # session.add_all(self.words)
            # session.add_all(self.morphemes)
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

