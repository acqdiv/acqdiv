""" Corpus and session processors to turn ACQDIV raw input corpora (Toolbox, ChatXML, JSON) into ACQDIV database.
"""

import glob
import logging
import os
import sys

import sqlalchemy as sa

from parsers import *
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
        """ Loops over all raw corpus session input files and processes each and the commits the data to the database.
        """
        for session_file in glob.glob(self.cfg['paths']['sessions']):
            print("\t", session_file)
            s = SessionProcessor(self.cfg, session_file, 
                    self.parser_factory, self.engine)
            try:
                s.process_session()
            except Exception as e:
                logger.warning("Aborted processing of file {}: "
                               "exception: {}".format(session_file, type(e)),
                               exc_info=sys.exc_info())


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
        self.engine = engine
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]

        # Commonly used variables from the corpus config file.
        self.language = self.config['corpus']['language']
        self.corpus = self.config['corpus']['corpus']
        self.format = self.config['corpus']['format']
        self.morpheme_type = self.config['morphemes']['type']


    def process_session(self):
        with self.engine.begin() as conn:
            conn.execute('PRAGMA synchronous = OFF')
            conn.execute('PRAGMA journal_mode = MEMORY')
            self._process_session(conn.execution_options(compiled_cache={}))


    @staticmethod
    def _extract(dict_, keymap, **kwargs):
        result = {keymap[k]: dict_[k] for k in (keymap.keys() & dict_.keys())}
        result.update(kwargs)
        return result


    def _process_session(self, conn):
        # insert_sess, insert_speaker, insert_utt, insert_word = \
        #    (sa.insert(model, bind=conn).execute for model in (db.Session, db.Speaker, db.Utterance, db.Word))

        insert_sess, insert_speaker, insert_utt, insert_word, insert_morph = \
            (sa.insert(model, bind=conn).execute for model in (db.Session, db.Speaker, db.Utterance, db.Word, db.Morpheme))


        self.parser = self.parser_factory(self.file_path)
        session_metadata = self.parser.get_session_metadata()
        session_labels = self.config['session_labels']
        # We overwrite a few values in the retrieved session metadata.
        d = self._extract(session_metadata, session_labels, source_id=self.filename, language=self.language, corpus=self.corpus)

        # Populate sessions table.
        s_id, = insert_sess(**d).inserted_primary_key

        # Populate the speakers table.
        speaker_labels = self.config['speaker_labels']
        for speaker in self.parser.next_speaker():
            d = self._extract(speaker, speaker_labels,
                              language=self.language, corpus=self.corpus)
            insert_speaker(session_id_fk=s_id, **d)

        # Populate the utterances, words and morphemes tables.
        for utterance, words, morphemes in self.parser.next_utterance():
            if utterance is None:
                logger.info("Skipping nonce utterance in {}".format(self.file_path))
                continue

            utterance.update(corpus=self.corpus, language=self.language)
            u_id, = insert_utt(session_id_fk=s_id, **utterance).inserted_primary_key

            w_ids = []
            for w in words:
                if w:
                    w.update(corpus=self.corpus, language=self.language)
                    w_id, = insert_word(session_id_fk=s_id, utterance_id_fk=u_id, **w).inserted_primary_key
                else:
                    w_id = None
                w_ids.append(w_id)

            no_word_link = len(morphemes) != len(words)
            # no_word_link = len(morphemes) != len(words) or any(None in w_ids)

            # Morphemes
            for i in range(0, w_ids):
                w_id = None if no_word_link else w_ids[i]

                try:
                    for j in range(0, len(morphemes[i])):
                        # TODO: move this post processing (before the age, etc.) if it improves performance
                        morphemes[i][j]['corpus'] = self.corpus
                        morphemes[i][j]['language'] = self.language
                        morphemes[i][j]['type'] = self.morpheme_type

                        if len(w_id) == len(morphemes[i]):
                        # only link words and morpheme words if there are equal amounts of both
                        #    u.words[i].morphemes.append(morpheme)
                        #u.morphemes.append(morpheme)
                        # self.session.morphemes.append(morpheme)

                            insert_morph(session_id_fk=s_id, utterance_id_fk=u_id, word_id_fk=w_id[i], **morphemes[i][j])

                except TypeError:
                    logger.warn("Error processing morphemes in "
                                "word {} in {} utterance {}".format(i,
                                                                    self.corpus, utterance['source_id']))
                except IndexError:
                    logger.warn("Word {} in {} utterance {} "
                                "has no morphemes".format(i, self.corpus,
                                                          utterance['source_id']))