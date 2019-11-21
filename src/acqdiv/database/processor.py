import datetime
import subprocess
import pathlib

import sqlalchemy as sa
from sqlalchemy import create_engine

from acqdiv.database.model import Base
import acqdiv.database.model as db
from acqdiv.util.path import get_full_path


class DBProcessor:
    """Methods for adding corpus data to the database."""

    def __init__(self, db_dir='database'):
        """Initialize DB engine.

        Args:
            db_dir (str): Where the database is written to.
        """
        self.engine = self.get_engine(db_dir)

        # initialize them once for each session
        # to increase performance
        self.insert_corpus_func = None
        self.insert_session_func = None
        self.insert_speaker_func = None
        self.insert_utt_func = None
        self.insert_word_func = None
        self.insert_morph_func = None

    @classmethod
    def get_engine(cls, db_dir):
        """Return a database engine.

        Args:
            db_dir (str): Where the database is written to.

        Returns:
            Engine: The DB engine.
        """
        db_dir = pathlib.Path(db_dir)
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        path = db_dir / f'acqdiv_corpus_{date}.sqlite3'

        print(f"Writing database to: {path.resolve()}")
        print()
        engine = create_engine(f'sqlite:///{str(path)}', echo=False)
        cls.create_tables(engine)
        cls.create_views(path)

        return engine

    @staticmethod
    def create_tables(engine):
        """Drop all tables before creating them.

            Args:
                engine: An sqlalchemy database engine.
        """
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def create_views(db_path):
        view_path = get_full_path('database/views.sql')
        cmd = f'sqlite3 {db_path} < {view_path}'
        subprocess.run(cmd, shell=True)

    def insert_corpus(self, corpus):
        """Insert the corpus into the database.

        Args:
            corpus (acqdiv.model.corpus.Corpus): The corpus.
        """
        with self.engine.begin() as conn:
            conn.execute('PRAGMA synchronous = OFF')
            conn.execute('PRAGMA journal_mode = MEMORY')
            conn = conn.execution_options(compiled_cache={})
            self.insert_corpus_func = sa.insert(db.Corpus, bind=conn).execute
            c_id = self.insert_corpus_metadata(corpus)

        uspeakers_dict = {}

        for session in corpus.sessions:
            self.insert_session(session, c_id, uspeakers_dict)

    def insert_corpus_metadata(self, corpus):
        """Insert the data into the `Corpus` table.

        Args:
            corpus (acqdiv.model.corpus.Corpus): The corpus.

        Returns:
            str: The ID of the corpus.
        """
        c_id, = self.insert_corpus_func(
            id=corpus.corpus,
            language=corpus.language,
            iso_639_3=corpus.iso_639_3,
            glottolog_code=corpus.glottolog_code,
            owner=corpus.owner,
            acronym=corpus.acronym,
            name=corpus.name,
        ).inserted_primary_key

        return c_id

    def insert_session(self, session, c_id, uspeakers_dict):
        """Insert the session into the database.

        Args:
            session (acqdiv.model.session.Session): The session.
            c_id (str): The corpus ID.
        """
        with self.engine.begin() as conn:
            conn.execute('PRAGMA synchronous = OFF')
            conn.execute('PRAGMA journal_mode = MEMORY')
            conn = conn.execution_options(compiled_cache={})

            self.insert_session_func = sa.insert(db.Session, bind=conn).execute
            self.insert_speaker_func = sa.insert(db.Speaker, bind=conn).execute
            self.insert_uspeaker_func = sa.insert(
                db.UniqueSpeaker, bind=conn).execute
            self.insert_utt_func = sa.insert(db.Utterance, bind=conn).execute
            self.insert_word_func = sa.insert(db.Word, bind=conn).execute
            self.insert_morph_func = sa.insert(db.Morpheme, bind=conn).execute

            s_id = self.insert_session_metadata(session, c_id)
            speakers_dict = self.insert_speakers(
                session.speakers, s_id, c_id, uspeakers_dict)
            self.insert_utterances(session.utterances, s_id, speakers_dict)

    def insert_session_metadata(self, session, c_id):
        s_id, = self.insert_session_func(
            corpus=c_id,
            date=session.date,
            source_id=session.source_id,
            duration=session.duration if session.duration else None,
            media_id=session.media_filename if session.media_filename else None
        ).inserted_primary_key

        return s_id

    def insert_speakers(self, speakers, s_id, c_id, uspeakers_dict):
        speakers_dict = {
            None: None
        }
        for speaker in speakers:
            if speaker.uniquespeaker in uspeakers_dict:
                usp_id = uspeakers_dict[speaker.uniquespeaker]
            else:
                usp_id = self.insert_uspeaker(speaker.uniquespeaker, c_id)
                uspeakers_dict[speaker.uniquespeaker] = usp_id

            sp_id = self.insert_speaker(speaker, s_id, usp_id)
            speakers_dict[speaker] = sp_id

        return speakers_dict

    def insert_uspeaker(self, uspeaker, c_id):
        usp_id, = self.insert_uspeaker_func(
            corpus=c_id,
            name=uspeaker.name if uspeaker.name else None,
            birthdate=uspeaker.birth_date if uspeaker.birth_date else None,
            gender_raw=uspeaker.gender_raw if uspeaker.gender_raw else None,
            gender=uspeaker.gender if uspeaker.gender else None,
            speaker_label=uspeaker.code if uspeaker.code else None,
        ).inserted_primary_key

        return usp_id

    def insert_speaker(self, speaker, s_id, usp_id):
        sp_id, = self.insert_speaker_func(
            session_id_fk=s_id,
            uniquespeaker_id_fk=usp_id,
            age_raw=speaker.age_raw if speaker.age_raw else None,
            age=speaker.age if speaker.age else None,
            age_in_days=speaker.age_in_days if speaker.age_in_days else None,
            role_raw=speaker.role_raw if speaker.role_raw else None,
            role=speaker.role if speaker.role else None,
            macrorole=speaker.macro_role if speaker.macro_role else None,
            languages_spoken=speaker.languages_spoken
            if speaker.languages_spoken else None
        ).inserted_primary_key

        return sp_id

    def insert_utterances(self, utterances, s_id, speakers_dict):
        for utt in utterances:
            u_id = self.insert_utterance(utt, s_id, speakers_dict)
            w_ids = self.insert_words(utt.words, u_id)
            self.insert_morphemes(utt.morphemes, u_id, w_ids)

    def insert_utterance(self, utt, s_id, speakers_dict):
        u_id, = self.insert_utt_func(
            session_id_fk=s_id,
            source_id=utt.source_id,
            speaker_id_fk=speakers_dict[utt.speaker],
            addressee_id_fk=speakers_dict[utt.addressee],
            utterance_raw=utt.utterance_raw if utt.utterance_raw else None,
            utterance=utt.utterance if utt.utterance else None,
            translation=utt.translation if utt.translation else None,
            morpheme=utt.morpheme_raw if utt.morpheme_raw else None,
            gloss_raw=utt.gloss_raw if utt.gloss_raw else None,
            pos_raw=utt.pos_raw if utt.pos_raw else None,
            sentence_type=utt.sentence_type if utt.sentence_type else None,
            childdirected=utt.childdirected
            if isinstance(utt.childdirected, bool) else None,
            start_raw=utt.start_raw if utt.start_raw else None,
            start=utt.start if utt.start else None,
            end_raw=utt.end_raw if utt.end_raw else None,
            end=utt.end if utt.end else None,
            comment=utt.comment if utt.comment else None,
        ).inserted_primary_key

        return u_id

    def insert_words(self, words, u_id):
        w_ids = []
        for w in words:
            w_id = self.insert_word(w, u_id)
            w_ids.append(w_id)

        return w_ids

    def insert_word(self, w, u_id):
        w_id, = self.insert_word_func(
            utterance_id_fk=u_id,
            language=w.word_language if w.word_language else None,
            word=w.word if w.word else None,
            word_actual=w.word_actual if w.word_actual else None,
            word_target=w.word_target if w.word_target else None,
            pos=w.pos if w.pos else None,
            pos_ud=w.pos_ud if w.pos_ud else None,

        ).inserted_primary_key

        return w_id

    def insert_morphemes(self, morphemes, u_id, w_ids):
        link_to_word = len(morphemes) == len(w_ids)

        for i, mword in enumerate(morphemes):
            w_id = w_ids[i] if link_to_word else None

            for m in mword:
                self.insert_morpheme(m, u_id, w_id)

    def insert_morpheme(self, m, u_id, w_id):
        """Insert the morpheme.

        Args:
            m (acqdiv.model.morpheme.Morpheme): The morpheme instance.
            u_id (str): The utterance ID.
            w_id (str): The word ID.
        """
        self.insert_morph_func(
            utterance_id_fk=u_id,
            word_id_fk=w_id,
            language=m.morpheme_language if m.morpheme_language else None,
            type=m.type if m.type else None,
            morpheme=m.morpheme if m.morpheme else None,
            gloss_raw=m.gloss_raw if m.gloss_raw else None,
            gloss=m.gloss if m.gloss else None,
            pos_raw=m.pos_raw if m.pos_raw else None,
            pos=m.pos if m.pos else None,
            lemma_id=m.lemma_id if m.lemma_id else None,
        )
