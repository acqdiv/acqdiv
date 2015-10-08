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
        self.morpheme_type = self.config['morphemes']['type']
        # get filename
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]

        # attach session file path to config?
        # filename = os.path.splitext(os.path.basename(self.file_path))[0]
        # self.config.set('paths', 'filename', filename)

        # start up db session
        self.Session = sessionmaker(bind=engine)


    def process_session(self):
        # Config contains maps from corpus-specific labels -> database column names
        self.parser = SessionParser.create_parser(self.config, self.file_path)

        # Get session metadata (via labels defined in corpus config)
        session_metadata = self.parser.get_session_metadata()
        d = {}
        for k, v in session_metadata.items():
            if k in self.config['session_labels'].keys():
                d[self.config['session_labels'][k]] = v
        d['session_id'] = self.filename
        d['language'] = self.language
        d['corpus'] = self.corpus
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
                if k in self.config['speaker_labels'].keys():
                    d[self.config['speaker_labels'][k]] = v
                #if not k in self.config['speaker_labels'].values():
                #    continue
                #d[k] = v
            d['session_id_fk'] = self.filename
            d['language'] = self.language
            d['corpus'] = self.corpus
            self.speaker_entries.append(Speaker(**d))

        #Get unique speaker metadata, and only data specified in columns + language
        self.unique_speaker_entries = []
        columns = ['speaker_label', 'name', 'birthdate', 'gender']
        dmeta = {}
        for speaker in self.parser.next_speaker():
            d = {}
            for k, v in speaker.items():
                if k in self.config['speaker_labels'].keys():
                    d[self.config['speaker_labels'][k]] = v
            d_new = {}
            d_new['language'] = self.language
            #in case key not available in current d, value is None
            for key in columns:
                try:
                    d_new[key] = d[key]
                except KeyError:
                    d_new[key] = None
            #only add to table if not yet added
            self.unique_speaker_entries.append(Unique_Speaker(**d_new))

        # TODO(stiv): Need to add to each utterance some kind of joining key.
        # I think it makes sense to construct/add it here, since this is where
        # we do database stuff, and not in the parser (there's no reason the parser
        # should have to know about primary keys - it's a parser, not a db)

        # CHATXML or Toolbox body parsing begins...
        self.utterances = []
        self.words = []
        self.morphemes = []
        self.warnings = []

        if self.format == "Toolbox":
            # Utterances
            for utterance, words, morphemes, inferences in self.parser.next_utterance():
                utterance['session_id_fk'] = self.filename
                utterance['corpus'] = self.corpus
                utterance['language'] = self.language
                # TODO: determine utterance type from config
                utterance['utterance_type'] = self.config['utterance']['type']         
                self.utterances.append(Utterance(**utterance))
                
                # words
                for word in words:
                    word['language'] = self.language
                    word['corpus'] = self.corpus
                    self.words.append(Word(**word))

                # morphemes
                if utterance['corpus'] == 'Russian':
                    morphemes_inferences = collections.OrderedDict()
                    morphemes_warnings = collections.OrderedDict()
                    for (morpheme,inference) in it.zip_longest(morphemes,inferences):
                        try:
                            morphemes_inferences['utterance_id_fk'] = morpheme['utterance_id_fk']
                            # TODO: fix this to read from the config
                            morphemes_inferences['corpus'] = self.corpus
                            morphemes_inferences['language'] = self.language
                            morphemes_inferences['type'] = self.morpheme_type
                            morphemes_inferences['morpheme'] = morpheme['morpheme']
                            #morphemes_inferences['segment'] = morpheme['segment_target']
                            morphemes_inferences['pos_raw'] = inference['pos_raw']
                            morphemes_inferences['gloss_raw'] = inference['gloss_raw']
                            if 'warning' in inference.keys():
                                # TODO: fix this to read from the config
                                morphemes_warnings['corpus'] = utterance['corpus']
                                morphemes_warnings['utterance_id_fk'] = morpheme['utterance_id_fk']
                                morphemes_warnings['language'] = utterance['language']
                                morphemes_warnings['warning'] = inference['warning']
                                self.warnings.append(Warnings(**morphemes_warnings))
                        except TypeError:
                            continue
                        except KeyError:
                            continue
                        self.morphemes.append(Morpheme(**morphemes_inferences))
                                 
                
                elif utterance['corpus'] == 'Chintang':
                    morphemes_inferences = collections.OrderedDict()
                    morphemes_warnings = collections.OrderedDict()
                    ## inference parsing
                    for inference in inferences:
                        try:
                            morphemes_inferences['utterance_id_fk'] = inference['utterance_id_fk']
                            morphemes_inferences['corpus'] = self.corpus
                            morphemes_inferences['language'] = self.language
                            morphemes_inferences['type'] = self.morpheme_type
                            morphemes_inferences['morpheme'] = inference['morpheme']
                            #morphemes_inferences['segment_target'] = inference['morpheme']
                            morphemes_inferences['gloss_raw'] = inference['gloss_raw']
                            morphemes_inferences['pos_raw'] = inference['pos_raw']
                            if 'warning' in inference.keys():
                                morphemes_warnings['corpus'] = utterance['corpus']
                                morphemes_warnings['utterance_id_fk'] = inference['utterance_id_fk']
                                morphemes_warnings['warning'] = inference['warning']
                                self.warnings.append(Warnings(**morphemes_warnings))
                        except KeyError:
                            continue
                        except TypeError:
                            continue
                            
                        self.morphemes.append(Morpheme(**morphemes_inferences))
                                                        
                
                elif utterance['corpus'] == 'Indonesian':
                    morphemes_warnings = collections.OrderedDict()
                    morphemes_inferences = collections.OrderedDict()
                    for (morpheme,inference) in it.zip_longest(morphemes,inferences):
                        try:
                            morphemes_inferences['utterance_id_fk'] = morpheme['utterance_id_fk']
                            morphemes_inferences['corpus'] = self.corpus
                            morphemes_inferences['language'] = self.language
                            morphemes_inferences['type'] = self.morpheme_type
                            morphemes_inferences['morpheme'] = morpheme['morpheme']
                            # morphemes_inferences['segment'] = morpheme['morpheme']
                            morphemes_inferences['gloss_raw'] = inference['gloss_raw']
                            if 'warning' in inference.keys():
                                morphemes_warnings['corpus'] = utterance['corpus']
                                morphemes_warnings['utterance_id_fk'] = morpheme['utterance_id_fk']
                                morphemes_warnings['warning'] = inference['warning']
                                self.warnings.append(Warnings(**morphemes_warnings))
                        except TypeError:
                            continue
                        except KeyError:
                            continue
                            
                        self.morphemes.append(Morpheme(**morphemes_inferences))

        elif self.format == "JSON":
            for utterance, words, morphemes in self.parser.next_utterance():
                utterance['session_id_fk'] = self.filename
                utterance['corpus'] = self.corpus
                utterance['language'] = self.language
                self.utterances.append(Utterance(**utterance))

                for word in words:
                    word['utterance_id_fk'] = utterance['utterance_id']
                    word['corpus'] = self.corpus
                    word['language'] = self.language
                    self.words.append(Word(**word))

                for morpheme in morphemes:
                    morpheme['utterance_id_fk'] = utterance['utterance_id']
                    morpheme['corpus'] = self.corpus
                    morpheme['language'] = self.language
                    morpheme['type'] = self.morpheme_type
                    self.morphemes.append(Morpheme(**morpheme))

        # TODO: remove / comment out
        elif self.format == "ChatXML":
            #TODO(chysi): this doesn't look like a generator to me!!!
            for u, words, morphemes in self.parser.next_utterance():
                u.parent_id = self.file_path
                #TODO: u.ids counted per session
                # we need a better way of making them unique across corpora
                # dirty, dirty hack:
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
            session.add_all(self.unique_speaker_entries)
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

