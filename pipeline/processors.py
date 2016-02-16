""" Processors for acqdiv corpora
"""

import itertools as it
import re
import collections
from sqlalchemy.orm import sessionmaker
from parsers import *
from database_backend import *


class CorpusProcessor(object):
    """ Handler for processing each session file in particular corpus
    """
    def __init__(self, cfg, engine):
        """ Initializes a CorpusProcessor object

        Args:
            cfg: a corpus config file
            engine: sqlalchemy database engine
        """
        self.cfg = cfg
        self.engine = engine
        self.parser_factory = SessionParser.create_parser_factory(self.cfg)

    def process_corpus(self):
        """ Creates a SessionProcessor given a config and input file.
        """
        for session_file in self.cfg.session_files:
            print("Processing:", session_file)
            s = SessionProcessor(self.cfg, session_file, 
                    self.parser_factory, self.engine)
            s.process_session()
            s.commit()


class SessionProcessor(object):
    """ SessionProcessor invokes a parser to get the extracted data, and then interacts
        with the ORM backend to push data to it.
    """
    def __init__(self, cfg, file_path, parser_factory, engine):
        """ Init parser with corpus config. Pass in file path to process. Create sqla session.

        Args:
            cfg: a corpus config file
            file_path: path to input file
            engine: sqlalchemy database engine
        """
        self.config = cfg
        self.file_path = file_path
        self.parser_factory = parser_factory
        self.language = self.config['corpus']['language']
        self.corpus = self.config['corpus']['corpus']
        self.format = self.config['corpus']['format']
        self.morpheme_type = self.config['morphemes']['type']
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]
        self.Session = sessionmaker(bind=engine)

    def process_session(self):
        """ Process function for each file; creates dictionaries and inserts them into the database via sqla
        """
        # Config contains maps from corpus-specific labels -> database column names
        self.parser = self.parser_factory(self.file_path)

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

        # Get speaker metadata; capture data specified in corpus config
        self.speaker_entries = []
        for speaker in self.parser.next_speaker():
            d = {}
            for k, v in speaker.items():
                if k in self.config['speaker_labels'].keys():
                    d[self.config['speaker_labels'][k]] = v

            d['session_id_fk'] = self.filename
            d['language'] = self.language
            d['corpus'] = self.corpus

            #if 'Non_Human' in d['role_raw']:
            #    print(d)

            """ WHAT IS THIS?
            if 'Non_Human' in d['role_raw']:
                continue
            else:
                self.speaker_entries.append(Speaker(**d))
            """
            self.speaker_entries.append(Speaker(**d))

        # Begin CHATXML or Toolbox body parsing
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
                self.utterances.append(Utterance(**utterance))
                
                # words
                for word in words:
                    word['session_id_fk'] = self.filename
                    word['language'] = self.language
                    word['corpus'] = self.corpus
                    if self.config['corpus']['corpus'] in ['Chintang', 'Russian']:
                        word['word_actual'] = word['word']
                    self.words.append(Word(**word))

                # morphemes
                if utterance['corpus'] == 'Russian':
                    morphemes_inferences = collections.OrderedDict()
                    morphemes_warnings = collections.OrderedDict()
                    for (morpheme,inference) in it.zip_longest(morphemes,inferences):
                        try:
                            morphemes_inferences['session_id_fk'] = self.filename
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
                            morphemes_inferences['session_id_fk'] = self.filename
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
                            morphemes_inferences['session_id_fk'] = self.filename
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

        # TODO: this will be replaced with CHAT XML parsing
        elif self.format == "JSON":
            for utterance, words, morphemes in self.parser.next_utterance():
                utterance['session_id_fk'] = self.filename
                utterance['corpus'] = self.corpus
                utterance['language'] = self.language
                self.utterances.append(Utterance(**utterance))

                for word in words:
                    word['session_id_fk'] = self.filename
                    word['utterance_id_fk'] = utterance['utterance_id']
                    word['corpus'] = self.corpus
                    word['language'] = self.language
                    # JSON files have utterance and word level warnings, but sometimes words are misaligned and
                    # the warning is at the utterance level -- give the user some love and tell them where to look
                    # if the word is returned NULL due to misalignment
                    if not 'word' in word:
                        word['warning'] = "See warning in Utterance table at: {}, {} ".format(word['session_id_fk'], word['utterance_id_fk'])
                    self.words.append(Word(**word))

                for morpheme in morphemes:
                    morpheme['session_id_fk'] = self.filename
                    morpheme['utterance_id_fk'] = utterance['utterance_id']
                    morpheme['corpus'] = self.corpus
                    morpheme['language'] = self.language
                    morpheme['type'] = self.morpheme_type
                    self.morphemes.append(Morpheme(**morpheme))

        elif self.format == "ChatXML":
            for raw_u, raw_words, raw_morphemes in self.parser.next_utterance():
                utterance = {}
                for k in raw_u:
                    if k in self.config['json_mappings_utterance']:
                        label = self.config['json_mappings_utterance'][k]
                        utterance[label] = raw_u[k]
                    else:
                        utterance[k] = raw_u[k]

                utterance['session_id_fk'] = self.filename
                utterance['corpus'] = self.corpus
                utterance['language'] = self.language
                del utterance['phonetic_target']
                del utterance['phonetic']
                self.utterances.append(Utterance(**utterance))

                for raw_word in raw_words:
                    word = {}
                    for k in raw_word:
                        if k in self.config['json_mappings_words']:
                            label = self.config['json_mappings_words'][k]
                            word[label] = raw_word[k]
                        else:
                            word[k] = raw_word[k]
                    word['word'] = word[self.config['json_mappings_words']
                                            ['word']]
                    word['session_id_fk'] = self.filename
                    word['utterance_id_fk'] = utterance['utterance_id']
                    word['corpus'] = self.corpus
                    word['language'] = self.language
                    # JSON files have utterance and word level warnings, but sometimes words are misaligned and
                    # the warning is at the utterance level -- give the user some love and tell them where to look
                    # if the word is returned NULL due to misalignment
                    if not 'word' in word:
                        word['warning'] = ("See warning in Utterance table at: "
                              "{}, {} ".format(word['session_id_fk'], 
                                    word['utterance_id_fk']))
                    del word['word_id']
                    self.words.append(Word(**word))

                for mword in raw_morphemes:
                    for raw_morpheme in mword:
                        morpheme = {}
                        try:
                            for k in raw_morpheme:
                                if k in self.config['json_mappings_morphemes']:
                                    label = self.config['json_mappings_morphemes'][k]
                                    morpheme[label] = raw_morpheme[k]
                                else:
                                    morpheme[k] = raw_morpheme[k]
                                morpheme['session_id_fk'] = self.filename
                                morpheme['utterance_id_fk'] = utterance['utterance_id']
                                morpheme['corpus'] = self.corpus
                                morpheme['language'] = self.language
                                morpheme['type'] = self.morpheme_type
                            self.morphemes.append(Morpheme(**morpheme))
                        except TypeError as t:
                            print(("TypeError! in " + self.filename + " morpheme: " + str(t)),file=sys.stderr)
        else:
            raise Exception("Error: unknown corpus format!")


    def commit(self):
        """ Commits the dictionaries returned from parsing to the database.
        """
        session = self.Session()

        try:
            session.add(self.session_entry)
            session.add_all(self.speaker_entries)
            session.add_all(self.utterances)
            session.add_all(self.words)
            session.add_all(self.morphemes)
            session.add_all(self.warnings)
            session.commit()
        except:
            # TODO: print some error message? log it?
            session.rollback()
            raise
        finally:
            session.close()
