""" Post-processing processes on the corpora in the ACQDIV-DB. """

import argparse
import logging
import sqlalchemy as sa
import os

from configparser import ConfigParser

import acqdiv.database.database_backend as db
from acqdiv.ini.CorpusConfigParser import CorpusConfigParser
from acqdiv.util.util import get_path_of_most_recent_database


class PostProcessor:

    def __init__(self):
        self.engine = None
        self.conn = None
        self.corpora_in_DB = {}
        self.roles = None

    def postprocess(self, test=False):
        """Global setup and then call post-processes."""
        self.set_engine(test=test)
        self.set_roles()
        self.set_config_parsers()
        self.process_tables()

    def set_engine(self, test=False):
        """Set the engine.

        Args:
            test (bool): Is the test DB run?
        """
        if test:
            self.engine = sa.create_engine('sqlite:///database/test.sqlite3')
        else:
            db_path = get_path_of_most_recent_database()
            self.engine = sa.create_engine(db_path)
            print('Postprocessing {}...'.format(db_path))

    def configure_connection(self):
        self.conn.execute('PRAGMA synchronous = OFF')
        self.conn.execute('PRAGMA journal_mode = MEMORY')
        self.conn.execution_options(compiled_cache={})

    def set_config_parsers(self):
        with self.engine.begin() as self.conn:
            self.configure_connection()

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
        """Process the tables.

        Hint: Break down transactions (with self.engine.begin() as self.conn)
        into smaller transactions when memory starts to run out!
        """
        with self.engine.begin() as self.conn:
            self.configure_connection()
            print("Processing speakers table...")
            self.process_speakers_table()

        with self.engine.begin() as self.conn:
            self.configure_connection()
            print("Processing utterances table...")
            self.process_utterances_table()

    def get_config(self, corpus):
        """Return the corpus config parser."""
        return self.corpora_in_DB[corpus]

    def process_speakers_table(self):
        """Post-process speakers table."""
        self._speakers_unify_unknowns()
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

        for row in rows:
            role = row.role_raw
            gender = row.gender

            if role in self.roles['role_mapping']:
                role = self.roles['role_mapping'][role]
                # all unknown's and none's listed in the ini become NULL
                if role == 'Unknown' or role == 'None':
                    role = None

            # Inference to gender
            if gender is None:
                if row.role_raw in self.roles['role2gender']:
                    gender = self.roles['role2gender'][row.role_raw]

            # Inference to macrorole
            if row.role_raw in self.roles['role2macrorole']:
                macrorole = self.roles['role2macrorole'][row.role_raw]
            else:
                macrorole = None

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
        print("_utterances_get_uniquespeaker_ids")
        self._utterances_get_uniquespeaker_ids()

        print("_utterances_get_directedness")
        self._utterances_get_directedness()

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


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()

    postprocessor = PostProcessor()
    postprocessor.postprocess(test=args.t)


if __name__ == "__main__":
    main()