""" Processors for acqdiv corpora
"""

import sys
import itertools as it
from sqlalchemy.orm import sessionmaker

from parsers import *
from database_backend import *


# If it turns out that these really don't do anything but the loops, we can get rid of
# the Corp[us|ora]Processor classes and just make them, well, loops. In some function.
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

    # TODO: should we add the corpus level data, e.g. metadata, to the database here?

class SessionProcessor(object):
    """ SessionProcessor invokes a parser to get the extracted data, and then interacts
        with the ORM backend to push data to it.
    """
    # TODO: Does the Session object need a primary key? Is that passed in from the caller
    # (ie, when we know about the Corpus-level data)?

    def __init__(self, cfg, file_path, engine):
        # Init parser with corpus config. Pass in file path to process. Create sqla session.
        # Probably don't need to be too self-ish here...
        self.config = cfg
        self.file_path = file_path
        self.language = self.config['corpus']['language']
        self.corpus = self.config['corpus']['corpus']
        self.format = self.config['corpus']['format']
        # get filename
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]

        # attach session file path to config?
        # filename = os.path.splitext(os.path.basename(self.file_path))[0]
        # self.config.set('paths', 'filename', filename)

        # start up db session
        self.Session = sessionmaker(bind=engine)


    def process_session(self):
        # Config contains map of standard label -> local label.
        self.parser = SessionParser.create_parser(self.config, self.file_path)

        # Now start asking the parser for stuff...

        # Get session metadata (via labels defined in corpus config)
        session_metadata = self.parser.get_session_metadata()
        d = {}
        for k, v in session_metadata.items():
            if not k in self.config['session_labels']:
                continue
            db_column_name = self.config['session_labels'][k]
            d[db_column_name] = v
        d['session_id'] = self.filename
        self.session_entry = Session(**d)

        # TODO: deal with IMDI's dict in dict encoding of location (perhaps in CorpusConfigProcessor):
        # address = session_metadata['location']['address'],
        # continent = session_metadata['location']['continent'],
        # country = session_metadata['location']['country']

        # Get speaker metadata; capture data specified in corpus config
        self.speaker_entries = []
        for speaker in self.parser.next_speaker():
            d = {}
            for k, v in speaker.items():
                if not k in self.config['speaker_labels']:
                    continue
                db_column_name = self.config['speaker_labels'][k]
                d[db_column_name] = v
            d['parent_id'] = self.filename
            self.speaker_entries.append(Speaker(**d))

        # TODO(stiv): Need to add to each utterance some kind of joining key.
        # I think it makes sense to construct/add it here, since this is where
        # we do database stuff, and not in the parser (there's no reason the parser
        # should have to know about primary keys - it's a parser, not a db)

        # CHATXML | Toolbox body parsing begins...
        self.utterances = []
        self.words = []
        self.morphemes = []
        self.warnings = []

        if self.format == "Toolbox":
            # Utterance parsing
            for utterance, words, morphemes, inferences, warnings in self.parser.next_utterance():
                utterance['parent_id'] = self.filename
                utterance['corpus'] = self.corpus
                # TODO: determine utterance type from config
                utterance['utterance_type'] = self.config['utterance']['type']
                self.utterances.append(Utterance(**utterance))
               # print(inferences)
                
                # word parsing
                for word in words:
                    self.words.append(Word(**word))
                    
                # morpheme parsing | not-so-nice-solution (@bambooforest, I know, I know, no iterating over dictionaries, but this was the only way I managed to get all the info into the Morpheme-table)
                # not so nice solution (that works at least): inference and morpheme parsing at once with ugly iterating over dictionary (at least it populates the db)
                if utterance['corpus'] == 'Russian':
                    morphemes_inferences = collections.OrderedDict()
                    for (morpheme,inference) in zip(morphemes,inferences):
                        morphemes_inferences['parent_id'] = morpheme['parent_id']
                        morphemes_inferences['morpheme'] = morpheme['morpheme']
                        morphemes_inferences['pos'] = inference['pos']
                        morphemes_inferences['gloss'] = inference['gloss']
                        self.morphemes.append(Morpheme(**morphemes_inferences))
                
                ## nicer solution, dsnt work for Russian and still needs to be checked for inference for Chintang and Indonesian -------------------------------------------------- 
                elif utterance['corpus'] in ['Chintang', 'Indonesian']:
                    # morpheme parsing
                    for morpheme in morphemes:
                        self.morphemes.append(Morpheme(**morpheme))
                    
                    # inference parsing
                    for inference in inferences:
                       self.morphemes.append(Morpheme(**inference)) ## <<-- THIS only "appends" to Morpheme table, how can I insert this data by using the same parent_id key??
                ## ---------------------------------------------------------------------------------------------------------------------------------------------------------------
                
                
                
                # warnings
                ## TODO: that doesn't work yet (plus, the things I'm doing in toolbox.py for warnings do not render a correct structure -- I'll hv to check that again!) 
                #print(warnings)
                #self.warnings.append(Warnings(**warnings))
                ## This fails with the following error:
                ##sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: warnings.id [SQL: 'INSERT INTO warnings (parent_id, warning) VALUES (?, ?)'] [parameters: ('A00210817_1', None)]
                    

            
        elif self.format == "JSON":
            for u in self.parser.next_utterance():
                print(u)
            #    for utterance, words in self.parser.next_utterance():
            #        pass

        elif self.format == "ChatXML":
            #TODO(chysi): this doesn't look like a generator to me!!!
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

        # Now write the database to the backend.
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
            session.add_all(self.words)
            session.add_all(self.morphemes)
            #session.merge(self.morphemes)
            session.add_all(self.warnings)
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

