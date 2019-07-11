import datetime

import sqlalchemy as sa
from sqlalchemy import create_engine

from acqdiv.database.database_backend import Base
import acqdiv.database.database_backend as db


class DBProcessor(object):
    """Methods for adding corpus data to the database."""

    def __init__(self, test=False):
        """Initialize DB engine.

        Args:
            test (bool): Is testing mode used?
        """
        self.test = test
        self.engine = self._get_engine(test=self.test)

    @classmethod
    def _get_engine(cls, test=False):
        """Return a database engine.

        Args:
            test (bool): Is the test DB used?

        Returns:
            Engine: The DB engine.
        """
        if test:
            print("Writing test database to: database/test.sqlite3")
            print()
            engine = cls.db_connect('sqlite:///database/test.sqlite3')
            cls.create_tables(engine)
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            path = 'sqlite:///database/acqdiv_corpus_{}.sqlite3'.format(date)
            print("Writing database to: {}".format(path))
            print()
            engine = cls.db_connect(path)
            cls.create_tables(engine)

        return engine

    @staticmethod
    def db_connect(path):
        """Perform database connection.

        If desired, add database settings in settings.py, e.g. for postgres:
        return create_engine(URL(**settings.DATABASE)).

        Args:
            path (str) : Path to DB.

        Returns:
            SQLAlchemy engine instance.
        """
        return create_engine(path, echo=False)

    @staticmethod
    def create_tables(engine):
        """Drop all tables before creating them.

            Args:
                engine: An sqlalchemy database engine.
        """
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(engine)

    def process_corpus(self, corpus):
        """Add the corpus data to the database.

        Args:
            corpus (acqdiv.model.Corpus.Corpus): The corpus.
        """
        for session in corpus.sessions:
            self.process_session(corpus, session)

            if self.test:
                break

    def process_session(self, corpus, session):
        """Add session data to the database.

        Args:
            corpus (acqdiv.model.Corpus.Corpus): The corpus.
            session (acqdiv.parsers.SessionParser.SessionParser): The session.
        """
        with self.engine.begin() as conn:
            conn.execute('PRAGMA synchronous = OFF')
            conn.execute('PRAGMA journal_mode = MEMORY')
            self._process_session(conn.execution_options(compiled_cache={}),
                                  corpus,
                                  session)

    @staticmethod
    def _extract(dict_, keymap, **kwargs):
        result = {keymap[k]: dict_[k]
                  for k in (keymap.keys() & dict_.keys())}
        result.update(kwargs)
        return result

    def _process_session(self, conn, corpus, session):
        """Add session data to the database.

        Args:
            conn (Connection): The DB connection.
            corpus (acqdiv.model.Corpus.Corpus): The corpus.
            session (acqdiv.parsers.SessionParser.SessionParser): The session.
        """
        corpus_name = corpus.corpus
        language = corpus.language
        morpheme_type = corpus.morpheme_type

        insert_sess, insert_speaker, insert_utt, insert_word, insert_morph = \
            (sa.insert(model, bind=conn).execute
             for model in (db.Session,
                           db.Speaker,
                           db.Utterance,
                           db.Word,
                           db.Morpheme))

        session_metadata = session.get_session_metadata()
        
        # try:
        #     duration = session_metadata['duration']
        # except KeyError:
        #     duration = None

        session_labels = corpus.session_labels
        # We overwrite a few values in the retrieved session metadata.
        d = self._extract(session_metadata,
                          session_labels,
                          language=language,
                          corpus=corpus_name)  # , duration=duration)

        # Populate sessions table.
        s_id, = insert_sess(**d).inserted_primary_key

        # Populate the speakers table.
        speaker_labels = corpus.speaker_labels
        for speaker in session.next_speaker():
            d = self._extract(speaker,
                              speaker_labels,
                              language=language,
                              corpus=corpus_name)
            insert_speaker(session_id_fk=s_id, **d)

        # Populate the utterances, words and morphemes tables.
        for utterance, words, morphemes in session.next_utterance():
            if utterance is None:
                continue

            utterance.update(corpus=corpus_name,
                             language=language)
            u_id, = insert_utt(
                session_id_fk=s_id, **utterance).inserted_primary_key

            w_ids = []
            for w in words:
                if w:
                    w.update(corpus=corpus_name,
                             language=language)
                    w_id, = insert_word(
                        session_id_fk=s_id,
                        utterance_id_fk=u_id, **w).inserted_primary_key
                    w_ids.append(w_id)

            link_to_word = len(morphemes) == len(w_ids)

            for i, mword in enumerate(morphemes):
                w_id = w_ids[i] if link_to_word else None

                for m in mword:
                    m.update(corpus=corpus_name,
                             language=language,
                             type=morpheme_type)
                    insert_morph(
                        session_id_fk=s_id,
                        utterance_id_fk=u_id,
                        word_id_fk=w_id,
                        **m)
