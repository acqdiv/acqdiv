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

    def _process_session(self, conn, corpus, session_parser):
        """Add session data to the database.

        Args:
            conn (Connection): The DB connection.
            corpus (acqdiv.model.Corpus.Corpus): The corpus.
            session_parser (acqdiv.parsers.SessionParser.SessionParser):
                The session.
        """
        corpus_name = corpus.corpus
        language = corpus.language
        morpheme_type = corpus.morpheme_type

        # Get insert functions
        insert_sess, insert_speaker, insert_utt, insert_word, insert_morph = \
            (sa.insert(model, bind=conn).execute
             for model in (db.Session,
                           db.Speaker,
                           db.Utterance,
                           db.Word,
                           db.Morpheme))

        session = session_parser.parse()

        # Populate Sessions table
        s_id, = insert_sess(
            corpus=corpus_name,
            language=language,
            date=session.date,
            source_id=session.source_id,
            media_id=session.media_filename if session.media_filename else None
        ).inserted_primary_key

        # Populate Speakers table
        for speaker in session.speakers:
            insert_speaker(
                session_id_fk=s_id,
                corpus=corpus_name,
                language=language,
                birthdate=speaker.birth_date,
                gender_raw=speaker.gender_raw,
                speaker_label=speaker.code,
                age_raw=speaker.age_raw,
                role_raw=speaker.role_raw,
                name=speaker.name,
                languages_spoken=speaker.languages_spoken
            )

        # Populate the utterances, words and morphemes tables.
        for utt in session.utterances:

            u_id, = insert_utt(
                session_id_fk=s_id,
                corpus=corpus_name,
                language=language,
                source_id=utt.source_id,
                speaker_label=utt.speaker_label,
                addressee=utt.addressee if utt.addressee else None,
                utterance_raw=utt.utterance_raw if utt.utterance_raw else None,
                utterance=utt.utterance if utt.utterance else None,
                translation=utt.translation if utt.translation else None,
                morpheme=utt.morpheme if utt.morpheme else None,
                gloss_raw=utt.gloss_raw if utt.gloss_raw else None,
                pos_raw=utt.pos_raw if utt.pos_raw else None,
                sentence_type=utt.sentence_type if utt.sentence_type else None,
                childdirected=utt.childdirected if utt.childdirected else None,
                start_raw=utt.start_raw if utt.start_raw else None,
                end_raw=utt.end_raw if utt.end_raw else None,
                comment=utt.comment if utt.comment else None,
                warning=utt.warning if utt.warning else None
            ).inserted_primary_key

            w_ids = []
            for w in utt.words:

                w_id, = insert_word(
                    session_id_fk=s_id,
                    utterance_id_fk=u_id,
                    corpus=corpus_name,
                    language=language,
                    word_language=w.word_language if w.word_language else None,
                    word=w.word if w.word else None,
                    word_actual=w.word_actual if w.word_actual else None,
                    word_target=w.word_target if w.word_target else None,
                    warning=w.warning if w.warning else None

                ).inserted_primary_key

                w_ids.append(w_id)

            morphemes = utt.morphemes

            link_to_word = len(morphemes) == len(w_ids)

            for i, mword in enumerate(morphemes):
                w_id = w_ids[i] if link_to_word else None

                for m in mword:

                    insert_morph(
                        session_id_fk=s_id,
                        utterance_id_fk=u_id,
                        word_id_fk=w_id,
                        corpus=corpus_name,
                        language=language,
                        morpheme_language=
                        m.morpheme_language if m.morpheme_language else None,
                        type=morpheme_type,
                        morpheme=m.morpheme if m.morpheme else None,
                        gloss_raw=m.gloss_raw if m.gloss_raw else None,
                        pos_raw=m.pos_raw if m.pos_raw else None,
                        lemma_id=m.lemma_id if m.lemma_id else None,
                        warning=m.warning if m.warning else None
                    )
