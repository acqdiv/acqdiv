""" Post-processing processes on the corpora in the ACQDIV-DB. """

import argparse
import logging
import sqlalchemy as sa

import acqdiv.database.model as db
from acqdiv.util.path import get_path_of_most_recent_database


class PostProcessor:

    def __init__(self):
        self.engine = None
        self.conn = None

    def postprocess(self, test=False):
        """Global setup and then call post-processes."""
        self.set_engine(test=test)
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

    def process_speakers_table(self):
        """Post-process speakers table."""
        self._speakers_get_unique_speakers()
        self._speakers_get_target_children()

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
        print("_utterances_get_directedness")
        self._utterances_get_directedness()

    def _utterances_get_directedness(self):
        """Infer child directedness for each utterance. Skips Chintang.

        If the utterance is or is not child directed, we denote this with 1 or 0.
        We use None (NULL) if the corpus is not annotated for child directedness.
        """
        s = sa.select([db.Utterance.id,
                       db.Utterance.corpus,
                       db.Utterance.addressee_id_fk,
                       db.Utterance.speaker_id_fk,
                       db.Speaker.macrorole]).\
            select_from(
                sa.outerjoin(db.Utterance, db.Speaker, sa.and_(
                    db.Utterance.addressee_id_fk == db.Speaker.id,
                    db.Utterance.session_id_fk == db.Speaker.session_id_fk
                ))).\
            where(db.Utterance.corpus != 'Chintang')

        rows = self.conn.execute(s)

        results = []
        for row in rows:
            if row.addressee_id_fk:
                if (row.macrorole == 'Target_Child'
                        and row.speaker_id_fk != row.addressee_id_fk):
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