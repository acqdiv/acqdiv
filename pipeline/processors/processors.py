""" Corpus and session processors to turn ACQDIV raw input corpora (Toolbox, ChatXML, JSON) into ACQDIV-DB
"""

import collections
import glob
import itertools as it
import logging
import os
import pdb
import re

from sqlalchemy.orm import sessionmaker

from parsers import *
from database_backend import *
import database_backend as db

logger = logging.getLogger('pipeline.' + __name__)


class CorpusProcessor(object):
    """ Handler for processing each session file in particular corpus.
    """
    def __init__(self, cfg, engine):
        """ Initializes a CorpusProcessor object then calls a SessionProcessor for each session input file.

        Args:
            cfg: CorpusConfigParser
            engine: sqlalchemy database engine
        """
        self.cfg = cfg
        self.engine = engine
        # Create the correct SessionParser (e.g. ToolboxParser, XMLParser)
        self.parser_factory = SessionParser.create_parser_factory(self.cfg)

    def process_corpus(self):
        """ Loops all raw corpus session input files and processes each and the commits the data to the database.
        """
        for session_file in glob.glob(self.cfg['paths']['sessions']):
            print("\t", session_file)
            s = SessionProcessor(self.cfg, session_file, 
                    self.parser_factory, self.engine)
            try:
                s.process_session()
            except Exception as e:
                logger.warning("Aborted processing of file {}: "
                            "exception: {}".format(session_file, type(e)))
            # TODO: uncomment when XMLParsers are finished
            # s.commit()


class SessionProcessor(object):
    """ SessionProcessor invokes a parser to get the extracted data, and then interacts
        with the SQLAlchemy ORM backend to push data to it.
    """
    def __init__(self, cfg, file_path, parser_factory, engine):
        """ Init parser with corpus config, file path, a parser factory and a database engine.

        Args:
            cfg: CorpusConfigParser
            file_path: path to raw session input file
            parser_factory: SessionParser (given
            engine: SQLAlchemy database engine
        """
        self.config = cfg
        self.file_path = file_path
        self.parser_factory = parser_factory

        # TODO: do we need these variables?
        self.language = self.config['corpus']['language']
        self.corpus = self.config['corpus']['corpus']
        self.format = self.config['corpus']['format']
        self.morpheme_type = self.config['morphemes']['type']

        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]
        self.Session = sessionmaker(bind=engine)


    def process_session(self):
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

        # TODO: remove this when we're on XML
        self.session_entry = Session(**d)

        # Get speaker metadata and populate the speakers table
        self.speaker_entries = []
        for speaker in self.parser.next_speaker():
            d = {}
            for k, v in speaker.items():
                if k in self.config['speaker_labels'].keys():
                    d[self.config['speaker_labels'][k]] = v
            # TODO: move this post processing (before the age, etc.) if it improves performance
            d['corpus'] = self.corpus
            d['language'] = self.language
            self.session.speakers.append(Speaker(**d))

        # Get the sessions utterances, words and morphemes to populate those db tables
        for utterance, words, morphemes in self.parser.next_utterance():
            # TODO: move this post processing (before the age, etc.) if it improves performance
            utterance['corpus'] = self.corpus
            utterance['language'] = self.language

            u = Utterance(**utterance)

            # TODO: Deal with Indonesian...

            # In Chintang the number of words may be longer than the number of morphemes -- error handling
            # print("words:", words)
            #
            #if len(words) > len(morphemes):
            #    logger.info("There are more words than morphemes in "
            #    "{} utterance {}".format(self.corpus, utterance['source_id']))

            # Populate the words
            for i in range(0, len(words)):
                # TODO: move this post processing (before the age, etc.) if it improves performance
                words[i]['corpus'] = self.corpus
                words[i]['language'] = self.language

                word = Word(**words[i])
                # TODO: is it cheaper to append a list here?
                word = Word(**words[i])
                u.words.append(word)
                self.session.words.append(word)

                # Populate the morphemes
                try:
                    for j in range(0, len(morphemes[i])): # loop morphemes
                        # TODO: move this post processing (before the age, etc.) if it improves performance
                        morphemes[i][j]['corpus'] = self.corpus
                        morphemes[i][j]['language'] = self.language

                        morpheme = Morpheme(**morphemes[i][j])
                        word.morphemes.append(morpheme)
                        u.morphemes.append(morpheme)
                        self.session.morphemes.append(morpheme)
                except TypeError:
                    logger.warn("Error processing morphemes in "
                                "word {} in {} utterance {}".format(i, 
                                    self.corpus, utterance['source_id']))
                except IndexError:
                    logger.info("Word {} in {} utterance {} "
                                "has no morphemes".format(i, self.corpus,
                                    utterance['source_id']))

            self.session.utterances.append(u)
        self.commit()


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
