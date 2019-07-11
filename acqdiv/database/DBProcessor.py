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
    def __init__(self, corpus, engine, test=False):
        """ Init parser with corpus metadata_path, file path, a parser factory and a database engine.

        Args:
            corpus (acqdiv.model.Corpus.Corpus): The corpus.
            engine: SQLAlchemy database engine

        """
        self.corpus = corpus
        self.test = test
        self.engine = engine

    def process_corpus(self):
        for session in self.corpus.sessions:
            self.process_session(session)

            if self.test:
                break


    def process_session(self, session):
        with self.engine.begin() as conn:
            conn.execute('PRAGMA synchronous = OFF')
            conn.execute('PRAGMA journal_mode = MEMORY')
            self._process_session(conn.execution_options(compiled_cache={}),
                                  session)


    @staticmethod
    def _extract(dict_, keymap, **kwargs):
        result = {keymap[k]: dict_[k] for k in (keymap.keys() & dict_.keys())}
        result.update(kwargs)
        return result


    def _process_session(self, conn, session):
        corpus = self.corpus.corpus
        language = self.corpus.language
        morpheme_type = self.corpus.morpheme_type

        insert_sess, insert_speaker, insert_utt, insert_word, insert_morph = \
            (sa.insert(model, bind=conn).execute for model in (db.Session, db.Speaker, db.Utterance, db.Word, db.Morpheme))

        session_metadata = session.get_session_metadata()
        
        # try:
        #     duration = session_metadata['duration']
        # except KeyError:
        #     duration = None

        session_labels = self.corpus.session_labels
        # We overwrite a few values in the retrieved session metadata.
        d = self._extract(session_metadata,
                          session_labels,
                          language=language,
                          corpus=corpus) # , duration=duration)

        # Populate sessions table.
        s_id, = insert_sess(**d).inserted_primary_key

        # Populate the speakers table.
        speaker_labels = self.corpus.speaker_labels
        for speaker in session.next_speaker():
            d = self._extract(speaker,
                              speaker_labels,
                              language=language,
                              corpus=corpus)
            insert_speaker(session_id_fk=s_id, **d)

        # Populate the utterances, words and morphemes tables.
        for utterance, words, morphemes in session.next_utterance():
            if utterance is None:
                continue

            utterance.update(corpus=corpus,
                             language=language)
            u_id, = insert_utt(session_id_fk=s_id, **utterance).inserted_primary_key

            w_ids = []
            for w in words:
                if w:
                    w.update(corpus=corpus,
                             language=language)
                    w_id, = insert_word(session_id_fk=s_id, utterance_id_fk=u_id, **w).inserted_primary_key
                    w_ids.append(w_id)

            link_to_word = len(morphemes) == len(w_ids)

            for i, mword in enumerate(morphemes):
                w_id = w_ids[i] if link_to_word else None

                for m in mword:
                    m.update(corpus=corpus,
                             language=language,
                             type=morpheme_type)
                    insert_morph(session_id_fk=s_id, utterance_id_fk=u_id, word_id_fk=w_id, **m)