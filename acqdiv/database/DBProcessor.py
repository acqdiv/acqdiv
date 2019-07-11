"""Corpus and session processors to turn ACQDIV raw input corpora
(Toolbox, CHAT) into ACQDIV database.
"""

import os
import sqlalchemy as sa

import acqdiv.database.database_backend as db


class DBProcessor(object):
    """ DBProcessor invokes a parser to get the extracted data, and then interacts
        with the SQLAlchemy ORM backend to push data to it.
    """
    def __init__(self, cfg, file_path, session_parser, engine):
        """ Init parser with corpus metadata_path, file path, a parser factory and a database engine.

        Args:
            cfg: CorpusConfigParser
            file_path: path to raw session input file
            session_parser: The session parser.
            engine: SQLAlchemy database engine

        """
        self.config = cfg
        self.file_path = file_path
        self.session_parser = session_parser
        self.engine = engine
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]

        # Commonly used variables from the corpus metadata_path file.
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
        insert_sess, insert_speaker, insert_utt, insert_word, insert_morph = \
            (sa.insert(model, bind=conn).execute for model in (db.Session, db.Speaker, db.Utterance, db.Word, db.Morpheme))

        session_metadata = self.session_parser.get_session_metadata()
        
        # try:
        #     duration = session_metadata['duration']
        # except KeyError:
        #     duration = None

        session_labels = self.config['session_labels']
        # We overwrite a few values in the retrieved session metadata.
        d = self._extract(session_metadata, session_labels, source_id=self.filename, language=self.language, corpus=self.corpus) # , duration=duration)

        # Populate sessions table.
        s_id, = insert_sess(**d).inserted_primary_key

        # Populate the speakers table.
        speaker_labels = self.config['speaker_labels']
        for speaker in self.session_parser.next_speaker():
            d = self._extract(speaker, speaker_labels,
                              language=self.language, corpus=self.corpus)
            insert_speaker(session_id_fk=s_id, **d)

        # Populate the utterances, words and morphemes tables.
        for utterance, words, morphemes in self.session_parser.next_utterance():
            if utterance is None:
                continue

            utterance.update(corpus=self.corpus, language=self.language)
            u_id, = insert_utt(session_id_fk=s_id, **utterance).inserted_primary_key

            w_ids = []
            for w in words:
                if w:
                    w.update(corpus=self.corpus, language=self.language)
                    w_id, = insert_word(session_id_fk=s_id, utterance_id_fk=u_id, **w).inserted_primary_key
                    w_ids.append(w_id)

            link_to_word = len(morphemes) == len(w_ids)

            for i, mword in enumerate(morphemes):
                w_id = w_ids[i] if link_to_word else None

                for m in mword:
                    m.update(corpus=self.corpus, language=self.language, type=self.morpheme_type)
                    insert_morph(session_id_fk=s_id, utterance_id_fk=u_id, word_id_fk=w_id, **m)