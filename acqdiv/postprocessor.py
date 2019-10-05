""" Post-processing processes on the corpora in the ACQDIV-DB. """

import argparse
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

    def process_speakers_table(self):
        """Post-process speakers table."""
        self._speakers_get_unique_speakers()

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