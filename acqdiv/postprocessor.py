""" Post-processing processes on the corpora in the ACQDIV-DB. """

import re
import sys
import time
import csv
import argparse
import logging
import sqlalchemy as sa
import glob
import os

from itertools import groupby
from configparser import ConfigParser

import acqdiv.database_backend as db
from acqdiv.parsers.CorpusConfigParser import CorpusConfigParser
from acqdiv.processors import age


class PostProcessor:

    cleaned_age = re.compile('\d{1,2};\d{1,2}\.\d')
    age_pattern = re.compile(".*;.*\..*")

    def __init__(self):
        self.engine = None
        self.conn = None
        self.corpora_in_DB = {}
        self.roles = None
        self.pos_index = {}
        self.pos_raw_index = {}

    def postprocess(self, test=False):
        """Global setup and then call post-processes."""

        start_time = time.time()

        self.set_engine(test=test)

        with self.engine.begin() as self.conn:
            self.configure_connection()
            self.set_config_parsers()
            self.set_roles()
            self.process_tables()

        print("%s seconds --- Finished" % (time.time() - start_time))
        print()
        print('Next, run tests:')

        if test:
            print('acqdiv test')
        else:
            print('acqdiv test -f')
        print()

    def set_engine(self, test=False):
        """Set the engine.

        Args:
            test (bool): Is the test DB run?
        """
        if test:
            self.engine = sa.create_engine('sqlite:///database/test.sqlite3')
        else:
            chosen_path = None
            # chose most recent sqlite file in the database directory
            for path in sorted(glob.glob('database/acqdiv_corpus_*.sqlite3'),
                               reverse=True):
                chosen_path = path
                break

            if chosen_path is None:
                logging.error('No sqlite file exists! Run the loader first.\n')
                sys.exit(1)

            self.engine = sa.create_engine('sqlite:///{}'.format(chosen_path))
            print('Postprocessing {}...'.format(chosen_path))

    def configure_connection(self):
        self.conn.execute('PRAGMA synchronous = OFF')
        self.conn.execute('PRAGMA journal_mode = MEMORY')
        self.conn.execution_options(compiled_cache={})

    def set_config_parsers(self):
        s = sa.select([db.Session.corpus]).distinct()
        for row in self.conn.execute(s):
            corpus = row[0]
            ccp = CorpusConfigParser()

            main_ini_path = 'ini/' + corpus + '.ini'
            phonbank_ini_path = 'ini/Phonbank/' + corpus + '.ini'

            if os.path.isfile(main_ini_path):
                ccp.read(main_ini_path)
            elif os.path.isfile(phonbank_ini_path):
                ccp.read(phonbank_ini_path)
            else:
                print('No ini found for: ', corpus)
                continue

            self.corpora_in_DB[corpus] = ccp

    def set_roles(self):
        """Load the role-mapping ini for unifying roles."""
        self.roles = ConfigParser(delimiters='=')
        self.roles.optionxform = str
        self.roles.read("ini/role_mapping.ini")

    def process_tables(self):
        # Update database tables
        print("Processing speakers table...")
        self.process_speakers_table()

        print("Processing utterances table...")
        self.process_utterances_table()

        print("Processing morphemes table...")
        self.process_morphemes_table()

        print("Processing words table...")
        self.process_words_table()

        print("Processing sessions table...")
        self.process_sessions_table()

    def get_config(self, corpus):
        """Return the corpus config parser."""
        return self.corpora_in_DB[corpus]

    def process_speakers_table(self):
        """Post-process speakers table."""
        self._speakers_unify_unknowns()
        self._speakers_indonesian_experimenters()
        self._speakers_update_age()
        self._speakers_standardize_gender_labels()
        self._speakers_standardize_roles()
        self._speakers_standardize_macroroles()
        self._speakers_get_unique_speakers()
        self._speakers_get_target_children()

    def _speakers_unify_unknowns(self):
        """Unify unknown values for speakers."""
        s = sa.select([db.Speaker.id, db.Speaker.name, db.Speaker.birthdate,
                       db.Speaker.speaker_label])
        rows = self.conn.execute(s)
        results = []
        null_values = {'Unknown', 'Unspecified', 'None', 'Unidentified', ''}

        for row in rows:
            has_changed = False

            if row.name in null_values:
                name = None
                has_changed = True
            else:
                name = row.name

            if row.birthdate in null_values:
                birthdate = None
                has_changed = True
            else:
                birthdate = row.birthdate

            if row.speaker_label in null_values:
                speaker_label = None
                has_changed = True
            else:
                speaker_label = row.speaker_label

            if has_changed:
                results.append({'speaker_id': row.id, 'name': name,
                                'birthdate': birthdate,
                                'speaker_label': speaker_label})

        rows.close()
        self._update_rows(db.Speaker.__table__, 'speaker_id', results)

    def _speakers_update_age(self):
        """Age standardization.

        Group by corpus and call age function depending on corpus
        input format (IMDI of CHAT XML).
        """
        s = sa.select([db.Speaker.id, db.Speaker.session_id_fk, db.Speaker.corpus,
                       db.Speaker.age_raw, db.Speaker.birthdate])
        query = self.conn.execute(s)
        for corpus, rows in groupby(query, lambda r: r[2]):
            config = self.get_config(corpus)
            results = []
            if config["metadata"]["type"] == "imdi":
                results = self._update_imdi_age(rows)
            elif config["metadata"]["type"] == "cha":
                results = self._update_cha_age(rows)
            # Indonesian
            else:
                results = self._update_xml_age(rows)
            self._update_rows(db.Speaker.__table__, "speaker_id", results)
        query.close()

    def _speakers_indonesian_experimenters(self):
        """Configuration replacements for Indonesian experimenter speaker labels.

        Updates the speakers table.
        """
        cfg = self.get_config('Indonesian')
        s = sa.select(
            [db.Speaker.id, db.Speaker.speaker_label, db.Speaker.name]).where(
            db.Speaker.corpus == 'Indonesian')
        rows = self.conn.execute(s)
        results = []
        for row in rows:
            if row.speaker_label == 'EXP':
                results.append({'speaker_id': row.id,
                                'speaker_label': cfg['exp_labels'][row.name]})
        rows.close()
        self._update_rows(db.Speaker.__table__, 'speaker_id', results)

    def _speakers_standardize_gender_labels(self):
        """Standardize gender labels in the speakers table."""
        s = sa.select([db.Speaker.id, db.Speaker.gender_raw])
        rows = self.conn.execute(s)
        results = []
        for row in rows:
            if row.gender_raw is not None:
                if row.gender_raw.lower() == 'female':
                    results.append({'speaker_id': row.id, 'gender': 'Female'})
                elif row.gender_raw.lower() == 'male':
                    results.append({'speaker_id': row.id, 'gender': 'Male'})
                else:
                    results.append({'speaker_id': row.id, 'gender': None})
            else:
                results.append({'speaker_id': row.id, 'gender': None})
        rows.close()
        self._update_rows(db.Speaker.__table__, 'speaker_id', results)

    def _speakers_standardize_roles(self):
        """Unify speaker roles and draw inferences to related values.

        Each corpus has its own set of speaker roles. This function uses
        "role_mapping.ini" to assign a unified role to each speaker according
        to the mappings in role_mapping.ini.
        The mapping is either based on the original role or the speaker_label
        (depending on how the corpora handles role encoding).
        The role column in the speaker table contains the unified roles.
        """
        s = sa.select([
            db.Speaker.id, db.Speaker.role_raw, db.Speaker.role,
            db.Speaker.gender_raw, db.Speaker.gender, db.Speaker.macrorole,
            db.Speaker.corpus])
        rows = self.conn.execute(s)
        results = []
        not_found = set()

        for row in rows:
            role = row.role_raw
            gender = row.gender
            macrorole = None

            if role in self.roles['role_mapping']:
                role = self.roles['role_mapping'][role]
                # all unknown's and none's listed in the ini become NULL
                if role == 'Unknown' or role == 'None':
                    role = None
            else:
                not_found.add((role, row.corpus))

            # Inference to gender
            if gender is None:
                if row.role_raw in self.roles['role2gender']:
                    gender = self.roles['role2gender'][row.role_raw]

            # Inference to macrorole
            if row.role_raw in self.roles['role2macrorole']:
                macrorole = self.roles['role2macrorole'][row.role_raw]
            else:
                macrorole = None

            for item in not_found:
                logging.warning(
                    '\'{}\' from {} not found in role_mapping.ini'.format(item[0],
                                                                          item[1]),
                    exc_info=sys.exc_info())

            results.append({'speaker_id': row.id, 'role': role, 'gender': gender,
                            'macrorole': macrorole})

        rows.close()
        self._update_rows(db.Speaker.__table__, 'speaker_id', results)

    def _speakers_standardize_macroroles(self):
        """Define macrorole (= Adult, Child, Target_Child, Unknown)

        This function assigns an age category to each speaker. If there is
        no information on age available it uses "role_mappings.ini" to define
        which age category a speaker belongs to. The mapping is based on either
        the speaker's original role or speaker_label (depending on how the corpora
        handles role encoding).
        """
        # TODO: this method is completely dependent on ages
        # TODO: no warnings are given if the age input is wrong!
        # overwrite role mapping (except target child) if speaker is under 12
        # (e.g. if child is an aunt which is mapped to 'Adult' per default)

        s = sa.select([
            db.Speaker.id, db.Speaker.corpus, db.Speaker.speaker_label,
            db.Speaker.age_in_days, db.Speaker.macrorole, db.Speaker.role])
        rows = self.conn.execute(s)
        results = []

        for row in rows:
            # Inference by age: adults are >= 12yrs, i.e. > 4380 days.
            if row.age_in_days and row.macrorole != "Target_Child":
                if row.age_in_days <= 4380:
                    results.append({'speaker_id': row.id, 'macrorole': "Child"})
                else:
                    results.append({'speaker_id': row.id, 'macrorole': "Adult"})

            # Inference by speaker label on a per-corpus base
            elif row.macrorole is None:
                if (self.roles.has_section(row.corpus)
                        and row.speaker_label in self.roles[row.corpus]):
                    macrorole = self.roles[row.corpus][row.speaker_label]

                    # ignore all unknown's in the ini file
                    if macrorole != 'Unknown':
                        results.append({'speaker_id': row.id,
                                        'macrorole': macrorole})

        rows.close()
        self._update_rows(db.Speaker.__table__, 'speaker_id', results)

    def _speakers_get_unique_speakers(self):
        """Populate the the unique speakers table.

        Also populate uniquespeaker_id_fk in the speakers table.

        Uniqueness is determined by a combination of corpus, name, speaker label
        and birthdate.
        """
        s = sa.select([db.Speaker])
        rows = self.conn.execute(s)
        unique_speakers = []
        unique_speaker_ids = []
        identifiers = []

        for row in rows:
            t = (row.name, row.birthdate, row.speaker_label, row.corpus)
            if t not in identifiers:
                identifiers.append(t)
                # Create unique speaker rows.
                unique_speaker_id = identifiers.index(t) + 1
                unique_speakers.append({
                    'id': unique_speaker_id, 'corpus': row.corpus,
                    'speaker_label': row.speaker_label, 'name': row.name,
                    'birthdate': row.birthdate, 'gender': row.gender})

            unique_speaker_ids.append({
                'speaker_id': row.id,
                'uniquespeaker_id_fk': identifiers.index(t) + 1})

        rows.close()
        self._update_rows(db.Speaker.__table__, 'speaker_id', unique_speaker_ids)
        self._insert_rows(db.UniqueSpeaker.__table__, unique_speakers)

    def _speakers_get_target_children(self):
        """Set target children for sessions.

        Also adapt roles and macroroles if there are multiple target children
        per session.
        """
        s = sa.select([db.Speaker]).where(db.Speaker.role == "Target_Child")
        rows = self.conn.execute(s)
        targets_per_session = {}
        tc_id_results = []
        non_targets_results = []

        # Store target children per session.
        for row in rows:
            if row.session_id_fk in targets_per_session:
                targets_per_session[row.session_id_fk].add(row.uniquespeaker_id_fk)
            else:
                targets_per_session[row.session_id_fk] = {row.uniquespeaker_id_fk}

        # Go through all session ids and get the target children for this session.
        for session_id in targets_per_session:
            targets = targets_per_session[session_id]
            # Get session row.
            query = sa.select([db.Session]).where(db.Session.id == session_id)
            rec = self.conn.execute(query).fetchone()

            # If there is one target child only.
            if len(targets) == 1:
                # Just set target child for the session.
                target_child_fk = targets.pop()
                tc_id_results.append(
                    {'session_id': session_id, 'target_child_fk': target_child_fk})

            # If several target children infer target child from source id.
            else:
                if rec.corpus == "Chintang":
                    # Get target child label and get right target child id.
                    label = rec.source_id[2:7]
                    tc_id_query = sa.select([db.UniqueSpeaker]).where(sa.and_(
                        db.UniqueSpeaker.corpus == rec.corpus,
                        db.UniqueSpeaker.speaker_label == label))
                    tc_id_result = self.conn.execute(tc_id_query).fetchone()
                    tc_id = tc_id_result.id

                elif rec.corpus == "Russian":
                    # Session code's first letter matches that of speaker label.
                    letter = rec.source_id[0]
                    # Get right target child id.
                    tc_id_query = sa.select([db.Speaker]).where(sa.and_(
                        db.Speaker.corpus == rec.corpus,
                        db.Speaker.role == "Target_Child",
                        db.Speaker.speaker_label.like("{}%".format(letter))))
                    tc_id_result = self.conn.execute(tc_id_query).fetchone()
                    tc_id = tc_id_result.uniquespeaker_id_fk

                elif rec.corpus == "Yucatec":
                    label = rec.source_id[:3]
                    tc_id_query = sa.select([db.UniqueSpeaker]).where(sa.and_(
                        db.UniqueSpeaker.corpus == rec.corpus,
                        db.UniqueSpeaker.speaker_label == label))
                    tc_id_result = self.conn.execute(tc_id_query).fetchone()
                    tc_id = tc_id_result.id

                else:
                    logging.warning(
                        "Multiple target children for session {} in {}".format(
                            session_id, rec.corpus))
                    continue

                # Set this target child for the session.
                tc_id_results.append(
                    {'session_id': session_id, 'target_child_fk': tc_id})

                # Adapt role and macrorole of children that are not target anymore.
                non_targets_query = sa.select([db.Speaker]).where(sa.and_(
                    db.Speaker.role == "Target_Child",
                    db.Speaker.session_id_fk == session_id,
                    db.Speaker.uniquespeaker_id_fk != tc_id))
                non_targets = self.conn.execute(non_targets_query)

                for row in non_targets:
                    non_targets_results.append(
                        {'speaker_id': row.id, 'role': "Child",
                         'macrorole': "Child"})
        rows.close()
        self._update_rows(db.Session.__table__, 'session_id', tc_id_results)
        self._update_rows(db.Speaker.__table__, 'speaker_id', non_targets_results)

    def process_utterances_table(self):
        """Post-process utterances table."""
        print("_utterances_standardize_timestamps")
        self._utterances_standardize_timestamps()

        print("_utterances_change_indonesian_speaker_labels")
        self._utterances_change_indonesian_speaker_labels()

        print("_utterances_get_uniquespeaker_ids")
        self._utterances_get_uniquespeaker_ids()

        print("_utterances_get_directedness")
        self._utterances_get_directedness()

        print("_utterances_unify_unknowns")
        self._utterances_unify_unknowns()

    def _utterances_standardize_timestamps(self):
        """Unify the time stamps."""
        s = sa.select(
            [db.Utterance.id, db.Utterance.start_raw, db.Utterance.end_raw])
        rows = self.conn.execute(s)
        results = []
        for row in rows:
            if row.start_raw:  # .isnot(None):
                try:
                    start = age.unify_timestamps(row.start_raw)
                    end = age.unify_timestamps(row.end_raw)
                    results.append(
                        {'utterance_id': row.id, 'start': start, 'end': end})
                except Exception as e:
                    logging.warning('Error unifying timestamps: {}'.format(row, e),
                                   exc_info=sys.exc_info())
        rows.close()
        self._update_rows(db.Utterance.__table__, 'utterance_id', results)

    def _utterances_change_indonesian_speaker_labels(self):
        s = sa.select([db.Utterance.id, db.Utterance.speaker_label]).where(
            db.Utterance.corpus == "Indonesian")
        rows = self.conn.execute(s)
        results = []
        for row in rows:
            if row.speaker_label:
                if not 'EXP' in row.speaker_label:
                    results.append({'utterance_id': row.id,
                                    'speaker_label': row.speaker_label[0:3]})
                else:
                    results.append({'utterance_id': row.id,
                                    'speaker_label': row.speaker_label[3:]})
        rows.close()
        self._update_rows(db.Utterance.__table__, 'utterance_id', results)

    def _utterances_get_uniquespeaker_ids(self):
        """Add speaker ids and unique speaker ids to utterances table."""
        s = sa.select([db.Utterance.id,
                       db.Utterance.speaker_label,
                       db.Utterance.session_id_fk,
                       db.Utterance.corpus,
                       db.Speaker.id.label('speaker_id'),
                       db.Speaker.uniquespeaker_id_fk]).\
            select_from(
                sa.outerjoin(db.Utterance, db.Speaker, sa.and_(
                    db.Utterance.speaker_label == db.Speaker.speaker_label,
                    db.Utterance.session_id_fk == db.Speaker.session_id_fk,
                    db.Utterance.corpus == db.Speaker.corpus
                )))

        rows = self.conn.execute(s)

        results = []
        for row in rows:
            if row.speaker_label:
                results.append({'utterance_id': row.id,
                                'uniquespeaker_id_fk': row.uniquespeaker_id_fk,
                                'speaker_id_fk': row.speaker_id})
        rows.close()
        self._update_rows(db.Utterance.__table__, 'utterance_id', results)

    def _utterances_get_directedness(self):
        """Infer child directedness for each utterance. Skips Chintang.

        If the utterance is or is not child directed, we denote this with 1 or 0.
        We use None (NULL) if the corpus is not annotated for child directedness.
        """
        s = sa.select([db.Utterance.id,
                       db.Utterance.corpus,
                       db.Utterance.addressee,
                       db.Utterance.speaker_label,
                       db.Speaker.macrorole]).\
            select_from(
                sa.outerjoin(db.Utterance, db.Speaker, sa.and_(
                    db.Utterance.addressee == db.Speaker.speaker_label,
                    db.Utterance.session_id_fk == db.Speaker.session_id_fk
                ))).\
            where(db.Utterance.corpus != 'Chintang')

        rows = self.conn.execute(s)

        results = []
        for row in rows:
            if row.addressee:
                if (row.macrorole == 'Target_Child'
                        and row.speaker_label != row.addressee):
                    results.append({'utterance_id': row.id, 'childdirected': 1})
                else:
                    results.append({'utterance_id': row.id, 'childdirected': 0})
            else:
                results.append({'utterance_id': row.id, 'childdirected': None})
        rows.close()
        self._update_rows(db.Utterance.__table__, 'utterance_id', results)

    def _utterances_unify_unknowns(self):
        """Unify unknown values for utterances."""
        s = sa.select([
            db.Utterance.id, db.Utterance.addressee,
            db.Utterance.utterance_raw, db.Utterance.utterance,
            db.Utterance.translation, db.Utterance.morpheme,
            db.Utterance.gloss_raw, db.Utterance.pos_raw])
        rows = self.conn.execute(s)
        results = []
        for row in rows:
            # only update rows whose values have changed (to save memory)
            has_changed = False

            if row.addressee == "???":
                addressee = None
                has_changed = True
            else:
                addressee = row.addressee

            if row.utterance_raw == "":
                utterance_raw = None
                has_changed = True
            else:
                utterance_raw = row.utterance_raw

            if row.gloss_raw == "":
                gloss_raw = None
                has_changed = True
            else:
                gloss_raw = row.gloss_raw

            if row.pos_raw == "":
                pos_raw = None
                has_changed = True
            else:
                pos_raw = row.pos_raw

            if row.utterance in {"???", "", "0"}:
                utterance = None
                has_changed = True
            else:
                utterance = row.utterance

            if row.translation is None:
                translation = None
            else:
                # Set to NULL if translation only consists of ???/xxx/www
                if (re.fullmatch(r"\?{1,3}\.?|x{2,3}\.?|0 ?\.?|w{2,3}\.?",
                                 row.translation)):
                    translation = None
                else:
                    # Replace by ??? if it partially consists of www/xxx
                    translation = re.sub(r"www|xxx?", "???",
                                         row.translation)

                if translation != row.translation:
                    has_changed = True

            if row.morpheme is None:
                morpheme = None
            else:
                if (row.morpheme in {"", "?", "ww", "xxx"} or
                        re.fullmatch(r"((\?\?\? ?)|(-\?\?\? ?))+", row.morpheme)):
                    morpheme = None
                else:
                    morpheme = re.sub(r"www|xxx?|\*\*\*", "???", row.morpheme)

                if morpheme != row.morpheme:
                    has_changed = True

            if has_changed:
                results.append({
                    "utterance_id": row.id, "addressee": addressee,
                    "utterance_raw": utterance_raw, "utterance": utterance,
                    "translation": translation, "morpheme": morpheme,
                    "gloss_raw": gloss_raw, "pos_raw": pos_raw})

        rows.close()
        self._update_rows(db.Utterance.__table__, "utterance_id", results)

    def process_morphemes_table(self):
        """Post-process the morphemes table."""
        print("_morphemes_infer_pos_chintang")
        self._morphemes_infer_pos_chintang()

        print("_morphemes_infer_pos_indonesian")
        self._morphemes_infer_pos_indonesian()

        print("_morphemes_infer_pos")
        self._morphemes_infer_pos()

        print("_morphemes_infer_lemma_id_chintang")
        self._morphemes_infer_lemma_id_chintang()

        print("_morphemes_infer_labels")
        self._morphemes_infer_labels()

        print("_morphemes_unify_label")
        self._morphemes_unify_label()

        print("_morphemes_unify_label_qaqet")
        self._morphemes_unify_label_qaqet()

        print('_morphemes_unify_gloss_tuatschin()')
        self._morphemes_unify_gloss_tuatschin()

        print("_morphemes_get_pos_indexes")
        self._morphemes_get_pos_indexes()

        print("_morphemes_unify_unknowns")
        self._morphemes_unify_unknowns()

    def _morphemes_infer_pos_chintang(self):
        """Chintang part-of-speech inference.

        Also removes hyphens from raw input data.
        """
        s = sa.select(
            [db.Morpheme.id, db.Morpheme.corpus, db.Morpheme.pos_raw]).where(
            db.Morpheme.corpus == "Chintang")
        rows = self.conn.execute(s)
        results = []
        for row in rows:
            if row.pos_raw:
                if row.pos_raw.startswith('-'):
                    results.append({'morpheme_id': row.id, 'pos_raw': "sfx"})
                elif row.pos_raw.endswith('-'):
                    results.append({'morpheme_id': row.id, 'pos_raw': "pfx"})
        rows.close()
        self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def _morphemes_infer_pos_indonesian(self):
        """Indonesian part-of-speech inference.

        Clean up affix markers "-"; assign sfx, pfx, stem.
        """
        s = sa.select([db.Morpheme.id, db.Morpheme.corpus, db.Morpheme.gloss_raw,
                       db.Morpheme.pos_raw]).where(
            db.Morpheme.corpus == "Indonesian")
        rows = self.conn.execute(s)
        results = []
        for row in rows:
            if row.gloss_raw:
                if row.gloss_raw.startswith('-'):
                    results.append({'morpheme_id': row.id, 'pos_raw': "sfx"})
                elif row.gloss_raw.endswith('-'):
                    results.append({'morpheme_id': row.id, 'pos_raw': "pfx"})
                elif row.gloss_raw == '???':
                    results.append({'morpheme_id': row.id, 'pos_raw': "???"})
                else:
                    if row.pos_raw not in {'sfx', 'pfx', '???'}:
                        results.append({'morpheme_id': row.id, 'pos_raw': "stem"})
        rows.close()
        self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def _morphemes_infer_pos(self):
        """Part-of-speech inference.

        Clean up affix markers "-"; assign sfx, pfx, stem.
        """
        for corpus in ['Indonesian', 'Chintang']:
            s = sa.\
                select([db.Morpheme.id,
                        db.Morpheme.corpus,
                        db.Morpheme.morpheme,
                        db.Morpheme.gloss_raw,
                        db.Morpheme.pos_raw]).\
                where(db.Morpheme.corpus == corpus)
            rows = self.conn.execute(s)
            results = []
            for row in rows:
                morpheme = None if row.morpheme is None else row.morpheme.replace(
                    '-', '')
                gloss_raw = None if row.gloss_raw is None else row.gloss_raw.replace(
                    '-', '')
                pos_raw = None if row.pos_raw is None else row.pos_raw.replace(
                    '-', '')
                results.append(
                    {'morpheme_id': row.id, 'pos_raw': pos_raw, 'gloss_raw': gloss_raw,
                     'morpheme': morpheme})
            rows.close()
            self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def _morphemes_infer_lemma_id_chintang(self):
        """ Chintang morpheme dict id inference. Clean up affix markers "-". """
        s = sa.select([db.Morpheme.id, db.Morpheme.lemma_id]).where(db.Morpheme.corpus == "Chintang")
        rows = self.conn.execute(s)
        results = []
        for row in rows:
            # TODO: handle IDs containing letters (invalid?) and more than one IDs separated by '|' (added automatically?)
            lemma_id = None if row.lemma_id is None else row.lemma_id.replace('-', '')
            results.append({'morpheme_id': row.id, 'lemma_id': lemma_id})
        rows.close()
        self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def _morphemes_infer_labels(self):
        """Perform morpheme and POS tag substitutions given the metadata_path file.

        Indonesian, Japanese_MiiPro, Japanese_Miyata, Sesotho and Turkish have
        substitutions defined in their metadata_path files.
        """
        s = sa.select([db.Morpheme.id, db.Morpheme.corpus, db.Morpheme.gloss_raw,
                       db.Morpheme.pos, db.Morpheme.morpheme])
        query = self.conn.execute(s)
        results = []
        for corpus, rows in groupby(query, lambda r: r[1]):
            config = self.get_config(corpus)
            if config['morphemes']['substitutions'] == 'yes':
                target_tier = config['morphemes']['target_tier']
                substitutions = config['substitutions']
                for row in rows:
                    result = None if row.gloss_raw not in substitutions else \
                    substitutions[row.gloss_raw]
                    if result:
                        if target_tier == "morpheme":
                            results.append(
                                {'morpheme_id': row.id, 'morpheme': result,
                                 'pos': row.pos})
                        if target_tier == "pos":
                            results.append(
                                {'morpheme_id': row.id, 'morpheme': row.morpheme,
                                 'pos': result})
        query.close()
        self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def _morphemes_unify_label(self):
        """Key-value substitutions for morphological glosses and parts-of-speech.

        If no key is defined in the corpus ini file, then None (NULL) is written
        to the database.
        """
        # TODO: Insert some debugging here if the labels are missing?

        for corpus in self.corpora_in_DB:
            print(corpus)

            s = sa.\
                select([db.Morpheme.id,
                        db.Morpheme.corpus,
                        db.Morpheme.gloss_raw,
                        db.Morpheme.pos_raw]).\
                where(db.Morpheme.corpus == corpus)

            query = self.conn.execute(s)

            config = self.get_config(corpus)
            glosses = config['gloss']
            poses = config['pos']

            results = []
            for row in query:
                gloss = None if row.gloss_raw not in glosses else glosses[
                    row.gloss_raw]
                pos = None if row.pos_raw not in poses else poses[row.pos_raw]
                results.append({'morpheme_id': row.id, 'gloss': gloss, 'pos': pos})

            query.close()
            self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def _morphemes_unify_gloss_tuatschin(self):
        s = sa.select(
            [db.Morpheme.id, db.Morpheme.corpus, db.Morpheme.gloss_raw,
             db.Morpheme.pos_raw]).where(db.Morpheme.corpus == 'Tuatschin')
        query = self.conn.execute(s)
        results = []
        for corpus, rows in groupby(query, lambda r: r[1]):
            config = self.get_config(corpus)
            glosses = config['gloss']

            for row in rows:
                if row.gloss_raw:
                    # replace person/number combinations first
                    pnum_regex = re.compile(r'([0123])\.(Sing)')
                    gloss = pnum_regex.sub(r'\1SG', row.gloss_raw)
                    pnum_regex = re.compile(r'([0123])\.(Plur)')
                    gloss = pnum_regex.sub(r'\1PL', gloss)

                    parts = []
                    is_null = False
                    for part in gloss.split('.'):
                        if re.search(r'[0123](SG|PL)', part):
                            parts.append(part)
                        else:
                            if part in glosses:
                                part = glosses[part]

                                if part != '???':
                                    parts.append(part)
                                else:
                                    is_null = True
                                    break
                            else:
                                is_null = True
                                break

                    if is_null:
                        gloss = None
                    else:
                        gloss = '.'.join(parts)

                else:
                    gloss = None

                results.append({'morpheme_id': row.id, 'gloss': gloss})
        query.close()
        self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def _morphemes_unify_label_qaqet(self):
        """Infer gloss and pos for Qaqet.

        Use pos_raw und gloss_raw to infer pos and gloss. Other than in
        _morphemes_unify_label raw_labels are first split (by '.') into
        atomic labels before substitution. The substituted
        atomic labels are then joined again to complex labels (by '.').

        If no subsitute for the given label is found, it gets a None/Null.
        If no substitute is found for only one atomic label in a complex
        label then the not found label gets a '???' (while the other labels
        are normally substituted).
        """
        s = sa.select([db.Morpheme.id, db.Morpheme.corpus, db.Morpheme.gloss_raw,
                       db.Morpheme.pos_raw]).where(
            db.Morpheme.corpus == 'Qaqet')
        query = self.conn.execute(s)
        results = []
        for corpus, rows in groupby(query, lambda r: r[1]):
            config = self.get_config(corpus)
            glosses = config['gloss']
            poses = config['pos']
            for row in rows:

                # Get the gloss label.
                if row.gloss_raw:
                    atms_gloss_raw = row.gloss_raw.split('.')
                    gloss = []
                    for atm_gl_raw in atms_gloss_raw:
                        if atm_gl_raw not in glosses:
                            atm_gl = '???'
                        else:
                            atm_gl = glosses[atm_gl_raw]
                        gloss.append(atm_gl)
                    # If all atm_poses are '???', set to None.
                    for atm_gloss in gloss:
                        if atm_gloss != '???':
                            gloss = '.'.join(gloss)
                            break
                    else:
                        gloss = None
                else:
                    gloss = None

                # Get the POS label.
                if row.pos_raw and row.pos_raw in poses:
                    pos = poses[row.pos_raw]
                else:
                    pos = None

                results.append({'morpheme_id': row.id, 'gloss': gloss, 'pos': pos})
        query.close()
        self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def _morphemes_get_pos_indexes(self):
        """Infer the word's part-of-speech (raw and processed).

        Infer from the morphemes table as index for word pos assignment.
        """
        s = sa.select([db.Morpheme.id, db.Morpheme.pos, db.Morpheme.pos_raw,
                       db.Morpheme.word_id_fk])
        rows = self.conn.execute(s)
        for row in rows:
            if row.pos not in ["sfx", "pfx"]:
                # row.id will be int type in other tables when look up occurs
                # type it int here for convenience
                try:
                    self.pos_index[int(row.word_id_fk)] = row.pos
                except TypeError:
                    pass
                try:
                    self.pos_raw_index[int(row.word_id_fk)] = row.pos_raw
                except TypeError:
                    pass
        rows.close()

    def _morphemes_unify_unknowns(self):
        """Unify unknown values for morphemes."""
        for corpus in self.corpora_in_DB:
            s = sa.select([db.Morpheme.id,
                           db.Morpheme.morpheme,
                           db.Morpheme.gloss_raw,
                           db.Morpheme.gloss,
                           db.Morpheme.pos,
                           db.Morpheme.pos_raw,
                           db.Morpheme.lemma_id]).\
                where(db.Morpheme.corpus == corpus)

            rows = self.conn.execute(s)
            results = []
            null_values = {'???', '?', '', 'ww', 'xxx', '***'}

            for row in rows:
                has_changed = False

                if row.morpheme in null_values:
                    morpheme = None
                    has_changed = True
                else:
                    morpheme = row.morpheme

                if row.gloss_raw == '':
                    gloss_raw = None
                    has_changed = True
                else:
                    gloss_raw = row.gloss_raw

                if row.gloss in null_values:
                    gloss = None
                    has_changed = True
                else:
                    gloss = row.gloss

                if row.pos_raw == '':
                    pos_raw = None
                    has_changed = True
                else:
                    pos_raw = row.pos_raw

                if row.pos in null_values:
                    pos = None
                    has_changed = True
                else:
                    pos = row.pos

                if row.lemma_id in null_values:
                    lemma_id = None
                    has_changed = True
                else:
                    lemma_id = row.lemma_id

                if has_changed:
                    results.append({
                        'morpheme_id': row.id,
                        'morpheme': morpheme,
                        'gloss_raw': gloss_raw,
                        'gloss': gloss,
                        'pos_raw': pos_raw,
                        'pos': pos,
                        'lemma_id': lemma_id})

            rows.close()
            self._update_rows(db.Morpheme.__table__, 'morpheme_id', results)

    def process_words_table(self):
        """Add POS labels to the word table."""
        print("_words_add_pos_labels")
        self._words_add_pos_labels()

        print("_words_unify_unknowns")
        self._words_unify_unknowns()

    def _words_unify_unknowns(self):
        """Unify unknown values for words."""
        for corpus in self.corpora_in_DB:
            s = sa.select([db.Word.id,
                           db.Word.word,
                           db.Word.word_actual,
                           db.Word.word_target,
                           db.Word.pos]).\
                where(db.Word.corpus == corpus)

            rows = self.conn.execute(s)
            results = []
            null_values = {"", "xx", "ww", "???", "?", "0"}

            for row in rows:
                has_changed = False

                if row.word_actual in null_values:
                    word_actual = None
                    has_changed = True
                else:
                    word_actual = row.word_actual

                if row.word_target in null_values:
                    word_target = None
                    has_changed = True
                else:
                    word_target = row.word_target

                if row.word in null_values or row.word is None:
                    # If word (= word_actual (except Yucatec)) is missing
                    # use word_target if it's not NULL
                    if word_target is not None:
                        word = word_target
                    else:
                        word = None
                    has_changed = True
                else:
                    word = row.word

                if row.pos == '???':
                    pos = None
                    has_changed = True
                else:
                    pos = row.pos

                if has_changed:
                    results.append({
                        'word_id': row.id,
                        'word': word,
                        'word_actual': word_actual,
                        'word_target': word_target,
                        'pos': pos})

            self._update_rows(db.Word.__table__, 'word_id', results)

    def _words_add_pos_labels(self):
        """Add POS labels (processed and UD)."""
        for corpus in self.corpora_in_DB:

            s = sa.select([db.Word.id,
                           db.Word.corpus]).\
                where(db.Word.corpus == corpus)

            query = self.conn.execute(s)
            results_pos = []
            results_pos_ud = []
            config = self.get_config(corpus)
            poses_ud = config['pos_ud']

            for row in query:
                if row.id in self.pos_index:
                    results_pos.append(
                        {'word_id': row.id, 'pos': self.pos_index[row.id]})
                if row.id in self.pos_raw_index:
                    # tag in index is pos_raw, so first get UD equivalent
                    pos_raw = self.pos_raw_index[row.id]
                    if pos_raw in poses_ud:
                        pos_ud = poses_ud[pos_raw]

                        if pos_ud == '???':
                            pos_ud = None
                    else:
                        pos_ud = None

                    # now add
                    results_pos_ud.append({'word_id': row.id, 'pos_ud': pos_ud})
            query.close()
            self._update_rows(db.Word.__table__, 'word_id', results_pos)
            self._update_rows(db.Word.__table__, 'word_id', results_pos_ud)

    def process_sessions_table(self):
        self._insert_durations()

    def _insert_durations(self):
        """Read session durations from ini/durations.csv and insert the matches into the sessions table.
        """
        durations = []

        with open('ini/session_durations.csv', 'r', encoding='utf8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                duration = row['duration']
                # Skip rows with empty durations
                if duration == '':
                    continue
                session_id = row['id']
                durations.append({'session_id': session_id, 'duration': duration})

        self._update_rows(db.Session.__table__, 'session_id', durations)

    ### Util functions ###
    def _update_rows(self, t, binder, rows):
        """Update rows for a given table.

        Args:
            t: sql-alchemy-table
            binder: str, bindparameter, normally the column acting as primary key
            rows: list of dicts with col-name as key and insert value as value
        """
        stmt = t.update().where(t.c.id == sa.bindparam(binder)).values()

        try:
            self.conn.execute(stmt, rows)
        except sa.exc.StatementError:
            pass

    def _insert_rows(self, t, rows):
        """Insert rows for a given table.

        Bind parameter and list of dictionaries contain column-value mappings.
        """
        stmt = t.insert().values()
        try:
            self.conn.execute(stmt, rows)
        except sa.exc.IntegrityError:
            pass

    def _update_imdi_age(self, rows):
        """Process speaker ages in IMDI corpora.

        Finds all the recording sessions in the corpus in the metadata_path. Then,
        for each speaker in the session:

        First attempts to calculate ages from the speaker's birth date and
        the session's recording date. For speakers where this fails, looks for
        speakers that already have a properly formatted age, transfers this age
        from the age_raw column to the age column and calculates
        age_in_days from it.

        Finally, it looks for speakers that only have an age in years
         and does the same.
        """
        results = []
        for row in rows:
            if row.birthdate is not None:
                try:
                    session_date = self._get_session_date(row.session_id_fk)
                    recording_date = age.numerize_date(session_date)
                    birth_date = age.numerize_date(row.birthdate)
                    ages = age.format_imdi_age(birth_date, recording_date)
                    formatted_age = ages[0]
                    age_in_days = ages[1]
                    results.append({'speaker_id': row.id, 'age': formatted_age,
                                    'age_in_days': age_in_days})
                except age.BirthdateError:
                    logging.warning(
                        'Couldn\'t calculate age of speaker {} from birth and '
                        'recording dates: '
                        'Invalid birthdate.'.format(row.id),
                        exc_info=sys.exc_info())
                except age.SessionDateError:
                    logging.warning(
                        'Couldn\'t calculate age of speaker {} from birth and '
                        'recording dates: '
                        'Invalid recording date.'.format(row.id),
                        exc_info=sys.exc_info())

            if re.fullmatch(self.age_pattern, row.age_raw):
                formatted_age = row.age_raw
                age_in_days = age.calculate_xml_days(row.age_raw)
                results.append({'speaker_id': row.id, 'age': formatted_age,
                                'age_in_days': age_in_days})

            if ("None" not in row.age_raw
                    or "Un" not in row.age_raw
                    or row.age is None):
                if not self.cleaned_age.fullmatch(row.age_raw):
                    try:
                        ages = age.clean_incomplete_ages(row.age_raw)
                        formatted_age = ages[0]
                        age_in_days = ages[1]
                        results.append({'speaker_id': row.id, 'age': formatted_age,
                                        'age_in_days': age_in_days})
                    except ValueError:
                        logging.warning(
                            'Couldn\'t transform age of speaker {}'.format(row.id),
                            exc_info=sys.exc_info())
        return results

    def _update_cha_age(self, rows):
        """Process speaker ages in CHAT corpora."""
        results = []
        for row in rows:
            if row.age_raw:
                new_age = age.format_cha_age(row.age_raw)
                if new_age:
                    aid = age.calculate_xml_days(new_age)
                    results.append(
                        {'speaker_id': row.id, 'age': new_age, 'age_in_days': aid})
        return results

    def _update_xml_age(self, rows):
        """Process speaker ages in BaseCHATParser XML corpora.

        Finds all speakers from the corpus in the metadata_path and
        calls methods from age.py to fill in the age and age_in_days columns.
        """
        results = []
        for row in rows:
            if row.age_raw:
                new_age = age.format_xml_age(row.age_raw)
                if new_age:
                    aid = age.calculate_xml_days(new_age)
                    results.append(
                        {'speaker_id': row.id, 'age': new_age, 'age_in_days': aid})
        return results

    def _get_session_date(self, session_id):
        """Return the session date from the session table. """
        s = sa.select([db.Session]).where(db.Session.id == session_id)
        row = self.conn.execute(s).fetchone()
        return row.date


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()

    postprocessor = PostProcessor()
    postprocessor.postprocess(test=args.t)


if __name__ == "__main__":
    main()