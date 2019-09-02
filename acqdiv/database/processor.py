import datetime

import sqlalchemy as sa
from sqlalchemy import create_engine

from acqdiv.database.model import Base
import acqdiv.database.model as db


class DBProcessor:
    """Methods for adding corpus data to the database."""

    def __init__(self, test=False):
        """Initialize DB engine.

        Args:
            test (bool): Is testing mode used?
        """
        self.test = test
        self.engine = self.get_engine(test=self.test)

        # initialize them once for each corpus
        self.corpus_name = None
        self.language = None

        # initialize them once for each session
        # to increase performance
        self.insert_session_func = None
        self.insert_speaker_func = None
        self.insert_utt_func = None
        self.insert_word_func = None
        self.insert_morph_func = None

    @classmethod
    def get_engine(cls, test=False):
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

    def insert_corpus(self, corpus):
        """Insert the corpus into the database.

        Args:
            corpus (acqdiv.model.corpus.Corpus): The corpus.
        """
        self.corpus_name = corpus.corpus
        self.language = corpus.language

        for session in corpus.sessions:
            self.insert_session(session)

            if self.test:
                break

    def insert_session(self, session):
        """Insert the session into the database.

        Args:
            session (acqdiv.model.session.Session): The session.
        """
        with self.engine.begin() as conn:
            conn.execute('PRAGMA synchronous = OFF')
            conn.execute('PRAGMA journal_mode = MEMORY')
            conn = conn.execution_options(compiled_cache={})

            self.insert_session_func = sa.insert(db.Session, bind=conn).execute
            self.insert_speaker_func = sa.insert(db.Speaker, bind=conn).execute
            self.insert_utt_func = sa.insert(db.Utterance, bind=conn).execute
            self.insert_word_func = sa.insert(db.Word, bind=conn).execute
            self.insert_morph_func = sa.insert(db.Morpheme, bind=conn).execute

            s_id = self.insert_session_metadata(session)
            self.insert_speakers(session.speakers, s_id)
            self.insert_utterances(session.utterances, s_id)

    def insert_session_metadata(self, session):
        s_id, = self.insert_session_func(
            corpus=self.corpus_name,
            language=self.language,
            date=session.date,
            source_id=session.source_id,
            duration=session.duration if session.duration else None,
            media_id=session.media_filename if session.media_filename else None
        ).inserted_primary_key

        return s_id

    def insert_speakers(self, speakers, s_id):
        for speaker in speakers:
            self.insert_speaker(speaker, s_id)

    def insert_speaker(self, speaker, s_id):
        self.insert_speaker_func(
            session_id_fk=s_id,
            corpus=self.corpus_name,
            language=self.language,
            birthdate=speaker.birth_date if speaker.birth_date else None,
            gender_raw=speaker.gender_raw if speaker.gender_raw else None,
            gender=speaker.gender if speaker.gender else None,
            speaker_label=speaker.code if speaker.code else None,
            age_raw=speaker.age_raw if speaker.age_raw else None,
            age=speaker.age if speaker.age else None,
            age_in_days=speaker.age_in_days if speaker.age_in_days else None,
            role_raw=speaker.role_raw if speaker.role_raw else None,
            role=speaker.role if speaker.role else None,
            macrorole=speaker.macro_role if speaker.macro_role else None,
            name=speaker.name if speaker.name else None,
            languages_spoken=speaker.languages_spoken
            if speaker.languages_spoken else None
        )

    def insert_utterances(self, utterances, s_id):
        for utt in utterances:
            u_id = self.insert_utterance(utt, s_id)
            w_ids = self.insert_words(utt.words, s_id, u_id)
            self.insert_morphemes(utt.morphemes, s_id, u_id, w_ids)

    def insert_utterance(self, utt, s_id):
        u_id, = self.insert_utt_func(
            session_id_fk=s_id,
            corpus=self.corpus_name,
            language=self.language,
            source_id=utt.source_id,
            speaker_label=utt.speaker_label,
            addressee=utt.addressee if utt.addressee else None,
            utterance_raw=utt.utterance_raw if utt.utterance_raw else None,
            utterance=utt.utterance if utt.utterance else None,
            translation=utt.translation if utt.translation else None,
            morpheme=utt.morpheme_raw if utt.morpheme_raw else None,
            gloss_raw=utt.gloss_raw if utt.gloss_raw else None,
            pos_raw=utt.pos_raw if utt.pos_raw else None,
            sentence_type=utt.sentence_type if utt.sentence_type else None,
            childdirected=utt.childdirected if utt.childdirected else None,
            start_raw=utt.start_raw if utt.start_raw else None,
            start=utt.start if utt.start else None,
            end_raw=utt.end_raw if utt.end_raw else None,
            end=utt.end if utt.end else None,
            comment=utt.comment if utt.comment else None,
            warning=utt.warning if utt.warning else None
        ).inserted_primary_key

        return u_id

    def insert_words(self, words, s_id, u_id):
        w_ids = []
        for w in words:
            w_id = self.insert_word(w, s_id, u_id)
            w_ids.append(w_id)

        return w_ids

    def insert_word(self, w, s_id, u_id):
        w_id, = self.insert_word_func(
            session_id_fk=s_id,
            utterance_id_fk=u_id,
            corpus=self.corpus_name,
            language=self.language,
            word_language=w.word_language if w.word_language else None,
            word=w.word if w.word else None,
            word_actual=w.word_actual if w.word_actual else None,
            word_target=w.word_target if w.word_target else None,
            pos=w.pos if w.pos else None,
            pos_ud=w.pos_ud if w.pos_ud else None,
            warning=w.warning if w.warning else None

        ).inserted_primary_key

        return w_id

    def insert_morphemes(self, morphemes, s_id, u_id, w_ids):
        link_to_word = len(morphemes) == len(w_ids)

        for i, mword in enumerate(morphemes):
            w_id = w_ids[i] if link_to_word else None

            for m in mword:
                self.insert_morpheme(m, s_id, u_id, w_id)

    def insert_morpheme(self, m, s_id, u_id, w_id):
        """Insert the morpheme.

        Args:
            m (acqdiv.model.morpheme.Morpheme): The morpheme instance.
            s_id (str): The session ID.
            u_id (str): The utterance ID.
            w_id (str): The word ID.
        """
        self.insert_morph_func(
            session_id_fk=s_id,
            utterance_id_fk=u_id,
            word_id_fk=w_id,
            corpus=self.corpus_name,
            language=self.language,
            morpheme_language=
            m.morpheme_language if m.morpheme_language else None,
            type=m.type if m.type else None,
            morpheme=m.morpheme if m.morpheme else None,
            gloss_raw=m.gloss_raw if m.gloss_raw else None,
            gloss=m.gloss if m.gloss else None,
            pos_raw=m.pos_raw if m.pos_raw else None,
            pos=m.pos if m.pos else None,
            lemma_id=m.lemma_id if m.lemma_id else None,
            warning=m.warning if m.warning else None
        )
