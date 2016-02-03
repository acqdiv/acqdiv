""" Processors for raw corpora input to ACQDIV DB
"""

import itertools as it
import re
import collections
import logging
from sqlalchemy.orm import sessionmaker
from parsers import *
from database_backend import *
import database_backend as db

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(filemode='w')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('errors.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


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
        with the SQLAlchemy ORM backend to push data to it.
    """
    def __init__(self, cfg, file_path, parser_factory, engine):
        """ Init parser with a corpus-specific config that contains labels->database column name mappings,
        Args:
            cfg: a corpus config file
            file_path: path to input file
            engine: sqlalchemy database engine
        """
        self.config = cfg
        self.file_path = file_path
        self.parser_factory = parser_factory
        # factor this shit out
        self.language = self.config['corpus']['language']
        self.corpus = self.config['corpus']['corpus']
        self.format = self.config['corpus']['format']
        self.morpheme_type = self.config['morphemes']['type']
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]
        self.Session = sessionmaker(bind=engine)

    def process_session(self):
        """ Process function for each file; creates dictionaries and inserts them into the database via sqla
        """
        self.parser = self.parser_factory(self.file_path)

        # Returns all session metadata and gets corpus-specific sessions table mappings to populate the db
        session_metadata = self.parser.get_session_metadata()
        d = {}
        for k, v in session_metadata.items():
            if k in self.config['session_labels'].keys():
                d[self.config['session_labels'][k]] = v
        # SM: someday we could clean this up across ini files
        d['source_id'] = self.filename
        d['language'] = self.language
        d['corpus'] = self.corpus

        self.session = db.Session(**d)

        # Get speaker metadata and populate the speakers table
        self.speaker_entries = []
        for speaker in self.parser.next_speaker():
            d = {}
            for k, v in speaker.items():
                if k in self.config['speaker_labels'].keys():
                    d[self.config['speaker_labels'][k]] = v
            self.session.speakers.append(Speaker(**d))

            # TODO: check this
            #if 'Non_Human' in d['role_raw']:
            #    print(d)

            """ WHAT IS THIS?
            if 'Non_Human' in d['role_raw']:
                continue
            else:
                self.speaker_entries.append(Speaker(**d))
            """
            # self.speaker_entries.append(Speaker(**d))

        """
        # Begin CHATXML or Toolbox body parsing
        self.utterances = []
        self.words = []
        self.morphemes = []
        self.warnings = []
        """

        if self.format == "Toolbox":
            # Get the sessions utterances, words and morphemes to populate those db tables
            for utterance, words, morphemes in self.parser.next_utterance():
                # TODO: move this post processing (before the age, etc.)
                # utterance['corpus'] = self.corpus
                # utterance['language'] = self.language
                u = Utterance(**utterance)

                # In Chintang the number of words may be longer than the number of morphemes -- error handling
                if len(words) > len(morphemes):
                    logger.info("There are more words than morphemes in %s", utterance['source_id'])
                    continue

                # Populate the words
                for i in range(0, len(words)):
                    word = Word(**words[i])
                    # is it cheaper to append a list here?
                    u.words.append(word)
                    self.session.words.append(word)

                    # Populate the morphemes
                    for j in range(0, len(morphemes[i])): # loop morphemes
                        morpheme = Morpheme(**morphemes[i][j])
                        word.morphemes.append(morpheme)
                        u.morphemes.append(morpheme)
                        self.session.morphemes.append(morpheme)
                self.session.utterances.append(u)


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

        """
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
                    for morpheme in mword:
                        try:
                            morpheme['session_id_fk'] = self.filename
                            morpheme['utterance_id_fk'] = utterance['utterance_id']
                            morpheme['corpus'] = self.corpus
                            morpheme['language'] = self.language
                            morpheme['type'] = self.morpheme_type
                            self.morphemes.append(Morpheme(**morpheme))
                        except TypeError:
                            pass
        else:
            raise Exception("Error: unknown corpus format!")
        """

    def commit(self):
        """ Commits the dictionaries returned from parsing to the database.
        """
        session = self.Session()

        try:
            session.add(self.session)
            session.commit()
        except:
            # TODO: print some error message? log it?
            session.rollback()
            raise
        finally:
            session.close()
