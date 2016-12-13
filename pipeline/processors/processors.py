""" Corpus and session processors to turn ACQDIV raw input corpora (Toolbox, ChatXML, JSON) into ACQDIV-DB
"""

import collections
import glob
import itertools as it
import logging
import os
import pdb
import re
import sys

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
        self.unique_speakers = {}

    def process_corpus(self):
        """ Loops all raw corpus session input files and processes each and the commits the data to the database.
        """
        for session_file in glob.glob(self.cfg['paths']['sessions']):
            print("\t", session_file)
            s = SessionProcessor(self.cfg, session_file,
                                 self.parser_factory, self.engine,
                                 self.unique_speakers)
            try:
                s.process_session()
            except Exception as e:
                logger.warning("Aborted processing of file {}: "
                               "exception: {}".format(session_file, type(e)),
                               exc_info=sys.exc_info())
            # TODO: uncomment when XMLParsers are finished
            # s.commit()


class SessionProcessor(object):
    """ SessionProcessor invokes a parser to get the extracted data, and then interacts
        with the SQLAlchemy ORM backend to push data to it.
    """
    def __init__(self, cfg, file_path, parser_factory, engine, unique_speakers):
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
        self.unique_speakers = unique_speakers

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
        sessiondict = {}
        for k, v in session_metadata.items():
            if k in self.config['session_labels'].keys():
                sessiondict[self.config['session_labels'][k]] = v

        # SM: someday we could clean this up across ini files
        sessiondict['source_id'] = self.filename
        sessiondict['language'] = self.language
        sessiondict['corpus'] = self.corpus

        self.session = db.Session(**sessiondict)

        # Get speaker metadata and populate the speakers table
        for speaker in self.parser.next_speaker():
            speakerdict = {}
            for k, v in speaker.items():
                if k in self.config['speaker_labels'].keys():
                    speakerdict[self.config['speaker_labels'][k]] = v
            speakerdict['corpus'] = self.corpus
            speakerdict['language'] = self.language

            # A unique speaker is defined as a unique combination of name,
            # birth date, speaker label and corpus
            t = (speakerdict.get('name'), speakerdict.get('birthdate'),
                 speakerdict.get('speaker_label'))
            if t not in self.unique_speakers:
                # create unique speaker row
                uniquedict = {}
                uniquedict['corpus'] = speakerdict.get('corpus')
                uniquedict['speaker_label'] = speakerdict.get('speaker_label')
                uniquedict['name'] = speakerdict.get('name')
                uniquedict['birthdate'] = speakerdict.get('birthdate')
                self.unique_speakers[t] = db.UniqueSpeaker(**uniquedict)

            s = Speaker(**speakerdict)
            self.unique_speakers[t].speakers.append(s)
            self.session.speakers.append(s)


        # Get the sessions utterances, words and morphemes to populate those db tables
        for utterance, words, morphemes in self.parser.next_utterance():
            # TODO: move this post processing (before the age, etc.) if it improves performance
            if utterance is None:
                logger.info("Skipping nonce utterance in {}".format(
                    self.file_path))
                continue
            utterance['corpus'] = self.corpus
            utterance['language'] = self.language
            try:
                this_speaker = next(filter(
                    lambda s: s.speaker_label == utterance['speaker_label'],
                    self.session.speakers))
                this_unique_speaker = self.unique_speakers[
                    (this_speaker.name, this_speaker.birthdate,
                    this_speaker.speaker_label)]
            except KeyError:
                this_speaker = None
                this_unique_speaker = None
            except StopIteration:
                this_speaker = None
                this_unique_speaker = None

            u = Utterance(**utterance)
            if this_speaker is not None:
                this_speaker.utterances.append(u)
            if this_unique_speaker is not None:
                this_unique_speaker.utterances.append(u)

            wlen = len(words)
            mlen = len(morphemes)

            # TODO: Deal with Indonesian...

            # In Chintang the number of words may be longer than the number of morphemes -- error handling
            # print("words:", words)
            #
            #if len(words) > len(morphemes):
            #    logger.info("There are more words than morphemes in "
            #    "{} utterance {}".format(self.corpus, utterance['source_id']))

            # Populate the words
            for i in range(0, wlen):
                # TODO: move this post processing (before the age, etc.) if it improves performance
                if words[i] != {}:
                    words[i]['corpus'] = self.corpus
                    if words[i].get('language') is None:
                        words[i]['language'] = self.language

                    # TODO: is it cheaper to append a list here?
                    word = Word(**words[i])
                    u.words.append(word)
                    self.session.words.append(word)

            # Populate the morphemes
            # wlen with dummy words excluded
            new_wlen = len(u.words)
            for i in range(0, wlen):
                try:
                    for j in range(0, len(morphemes[i])): # loop morphemes
                        # TODO: move this post processing (before the age, etc.) if it improves performance
                        morphemes[i][j]['corpus'] = self.corpus
                        if morphemes[i][j].get('language') is None:
                            morphemes[i][j]['language'] = self.language
                        morphemes[i][j]['type'] = self.morpheme_type

                        morpheme = Morpheme(**morphemes[i][j])
                        if new_wlen == mlen:
                            # only link words and morpheme words if there are
                            # equal amounts of both
                            u.words[i].morphemes.append(morpheme)
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
            session.add_all(self.unique_speakers.values())
            session.commit()
        except:
            # TODO: print some error message? log it?
            session.rollback()
            raise
        finally:
            session.close()
