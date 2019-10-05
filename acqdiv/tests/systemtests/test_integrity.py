import unittest
import os
import re
import csv
import configparser
import sqlalchemy as sa

from dateutil.parser import parse
from sqlalchemy.orm import sessionmaker

from acqdiv.util.path import get_path_of_most_recent_database


class IntegrityTest(unittest.TestCase):
    """Integrity tests on the production database."""

    cwd_path = os.path.dirname(__file__)
    session = None
    meta = None
    cfg = None
    f_no_nulls = None
    f_proportions = None

    @classmethod
    def setUpClass(cls):
        """Setup test resources."""
        # Load database
        database_path = get_path_of_most_recent_database()
        engine = sa.create_engine(database_path)
        cls.meta = sa.MetaData(engine, reflect=True)
        session_class = sessionmaker(bind=engine)
        cls.session = session_class()

        # Load database counts
        config = os.path.join(
            cls.cwd_path, "resources/production_counts.ini")
        cls.cfg = configparser.ConfigParser()
        cls.cfg.read(config)

        # Load list of tables from csv file and
        # check that the specified table and their columns contain no NULLs
        cls.f_no_nulls = open(os.path.join(
                                cls.cwd_path,
                                "resources/tables-no-nulls-allowed.csv"), "r")
        cls.reader_tables_no_nulls = csv.reader(cls.f_no_nulls)
        next(cls.reader_tables_no_nulls)  # Skip the header

        # Load list of tables from csv file and check for coverage proportion.
        cls.f_proportions = open(os.path.join(
                                    cls.cwd_path,
                                    "resources/tables-proportions-filled.csv"),
                                 "r")
        cls.reader_proportion_nulls = csv.reader(cls.f_proportions)
        next(cls.reader_proportion_nulls)  # Skip the header

    @classmethod
    def tearDownClass(cls):
        """Tear down the test resources."""
        cls.session.close()
        cls.f_no_nulls.close()
        cls.f_proportions.close()

    def test_columns_for_all_null(self):
        """Any column with all NULL rows should throw an error."""
        for table in self.meta.tables.values():
            for column in table.c:
                if str(column) not in [
                        'morphemes.lemma_id',
                        'morphemes.warning',
                        'utterances.warning',
                        'words.warning'
                        ]:
                    self._column_contains_all_nulls(table, column)

    def test_columns_for_any_null(self):
        """ User specified columns should never have a NULL row. """
        for row in self.reader_tables_no_nulls:
            table = row[0]
            column = row[1]
            self._column_contains_null(table, column)

    def test_counts(self):
        """Use the fixture database gold counts and check production DB."""
        mismatched_counts = []
        for section in self.cfg:
            if section == "default":
                continue
            for option in self.cfg[section]:
                count = int(self.cfg[section][option])
                res = self.session.execute(
                    "select count(*) from %s where corpus = '%s'"
                    % (option, section))
                actual = res.fetchone()[0]

                if actual != count:
                    mismatched_counts.append((section, option, count, actual))

        self.assertEqual(len(mismatched_counts), 0,
                         msg="Mismatched session counts: {}"
                         .format(mismatched_counts))

    def test_sentence_type(self):
        """ Check sentence types in database vs whitelist. """
        query = "select sentence_type from utterances group by sentence_type"
        sentence_types = [
            None,
            # ACQDIV sentence types
            "default",
            "question",
            "exclamation",
            "imperative",
            # CHAT specific
            'transcription break',
            "trail off",
            'trail off of question',
            'question with exclamation',
            'interruption',
            'interruption of a question',
            'self-interruption',
            'self-interrupted question',
            'quotation follows',
            "quotation precedes",
        ]

        self._in_whitelist(query, sentence_types)

    def test_gender(self):
        """ Check genders in database vs whitelist. """
        query = "select gender from uniquespeakers group by gender"
        gender = ["Female", "Male", None]
        self._in_whitelist(query, gender)

    def test_pos(self):
        """ Check pos in database vs whitelist. """
        query = "select pos from morphemes group by pos"

        poses = [
            "ADJ", "ADV", "ART", "AUX", "CLF", "CONJ", "IDEOPH",
            "INTJ", "N", "NUM", "PVB", "pfx", "POST",
            "PREP", "PRODEM", "PTCL", "QUANT", "sfx", "stem", "V", "???"]

        res = self.session.execute(query)
        rows = res.fetchall()
        for row in rows:
            pos = row[0]

            if pos is not None:
                # for amalgams (e.g. see Tuatschin)
                for sub_pos in pos.split('+'):
                    self.assertIn(
                        sub_pos, poses,
                        msg='%s returned by (%s).' % (sub_pos, query))

    def test_pos_ud(self):
        """ Check UD pos (on word level) in database vs whitelist. """
        query = "select pos_ud from words group by pos_ud"
        poses = [
            None, "ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN",
            "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB",
            "X"]

        res = self.session.execute(query)
        rows = res.fetchall()
        for row in rows:
            pos = row[0]

            if pos is not None:
                # for amalgams (e.g. see Tuatschin)
                for sub_pos in pos.split('+'):
                    self.assertIn(
                        sub_pos, poses,
                        msg='%s returned by (%s).' % (sub_pos, query))

    def test_role(self):
        """ Check roles in database vs whitelist. """
        query = "select role from speakers group by role"
        roles = [
            "Adult",
            "Aunt",
            "Babysitter",
            "Brother",
            "Caller",
            "Caretaker",
            "Child",
            "Cousin",
            "Daughter",
            "Family_Friend",
            "Father",
            "Friend",
            "Grandfather",
            "Grandmother",
            "Great-Grandfather",
            "Great-Grandmother",
            "Housekeeper",
            "Mother",
            "Neighbour",
            "Nephew",
            "Niece",
            "Playmate",
            "Research_Team",
            "Sibling",
            "Sister",
            "Sister-in-law",
            "Son",
            "Speaker",
            "Student",
            "Subject",
            "Target_Child",
            "Teacher",
            "Teenager",
            "Twin_Brother",
            "Uncle",
            "Visitor",
            None
        ]
        self._in_whitelist(query, roles)

    def test_macrorole(self):
        """ Check macroles in database vs whitelist. """
        query = "select macrorole from speakers group by macrorole"
        macroroles = ["Adult", "Child", "Target_Child", None]
        self._in_whitelist(query, macroroles)

    def test_speaker_ages(self):
        # should be able to check it in various db columns
        query = "select age from speakers group by age"
        _pattern_speaker_ages = re.compile(
            r'^(\d\d?(;(0?[0-9]|1[01]).([012]?[0-9]|30))?)$')
        self._in_string(query, _pattern_speaker_ages)

    def test_date_sessions(self):
        """ Check date in sessions.date """
        query = "select date from sessions group by date"
        self._is_valid_date(query)

    def test_date_uniquespeakers(self):
        """ Check birthdates in uniquespeakers.birthdate """
        query = "select birthdate from uniquespeakers group by birthdate"
        self._is_valid_date(query)

    def test_language_per_morpheme(self):
        """ Check whether the language mapping is working as intended """
        query = "SELECT DISTINCT language FROM morphemes"
        langs = [
            "Arabic",
            "Bantawa",
            "Chintang",
            "Chintang/Bantawa",
            "Chintang/Nepali",
            "Cree",
            "English",
            'FOREIGN',
            "German",
            "Hindi",
            'Kuanua',
            'Ku Waru',
            "Indonesian",
            "Inuktitut",
            "Japanese",
            "Nepali",
            'Qaqet',
            "Russian",
            "Sesotho",
            "Tuatschin",
            "Turkish",
            "Yucatec",
            "Nungon",
            "Tok Pisin",
            None
        ]
        self._in_whitelist(query, langs)

    def test_more_target_children_per_session(self):
        """Check whether there is only one target child per session."""
        query = """SELECT session_id_fk
                   FROM speakers
                   WHERE role == 'Target_Child' OR macrorole == 'Target_Child'
                   GROUP BY session_id_fk HAVING COUNT(session_id_fk) > 1"""
        msg = "Session {} has more than one target child"
        for session_id in self.session.execute(query):
            self.fail(msg=msg.format(session_id[0]))

    def test_no_target_child_for_session(self):
        """Check whether every session has a target child."""
        query = """SELECT id, corpus, source_id
                   FROM vsessions
                   WHERE target_child_fk IS NULL"""
        msg = "Sessions {} do not have a target child."
        sessions = []
        for id_corpus_source_id in self.session.execute(query):
            sessions.append(id_corpus_source_id)

        if sessions:
            self.fail(msg=msg.format(sessions))

    """ Private methods below. """
    def _column_contains_null(self, table, column):
        """ Test if any row in column is NULL. """
        query = "select count(*) from %s where %s is NULL" % (table, column)
        res = self.session.execute(query)
        result = res.fetchone()[0]
        self.assertEqual(result, 0, msg='%s %s' % (res, query))

    def _column_contains_all_nulls(self, table, column):
        """ Test if rows in a column are all NULL. """
        query = "select count(*) from %s where %s is not NULL" \
                % (table, column)
        res = self.session.execute(query)
        result = res.fetchone()[0]
        self.assertGreater(result, 0, msg='%s %s' % (res, query))

    def _is_valid_date(self, query):
        """Check if input string is NULL or adheres to dateutils format."""
        res = self.session.execute(query)
        rows = res.fetchall()
        for row in rows:
            value = row[0]
            is_valid = False
            if value is None or self._is_date(value):
                is_valid = True
            self.assertTrue(is_valid,
                            msg=('Date value %s is not NULL and does not '
                                 'confirm to dateutils.parser '
                                 'in the query (%s).') % (value, query))

    def _is_date(self, string):
        """ Check for valid dateutils.parser format. """
        try:
            parse(string)
            return True
        except ValueError:
            return False

    def _is_match(self, string, pattern):
        """ Check if regex valid against string. """
        if pattern.search(string) is None:
            return False
        else:
            return True

    def _validate_string(self, query, pattern, is_string):
        """Validate if unique strings in a column conform to some regex."""
        res = self.session.execute(query)
        rows = res.fetchall()
        for row in rows:
            value = row[0]
            if value is not None:
                is_valid = self._is_match(value, pattern)
                if is_string:
                    self.assertTrue(
                        is_valid, msg='%s %s (%s)' % (value, is_valid, query))
                else:
                    self.assertFalse(
                        is_valid, msg='%s -- %s -- (%s)'
                                      % (value, is_valid, query))

    def _in_string(self, query, pattern):
        """ Check whether the input string is valid given a regex pattern. """
        return self._validate_string(query, pattern, is_string=True)

    def _not_in_string(self, query, pattern):
        return self._validate_string(query, pattern, is_string=False)

    def _in_whitelist(self, query, filter_list):
        self._check_filter_list(query, filter_list, is_whitelist=True)

    def _not_in_blacklist(self, query, filter_list):
        self._check_filter_list(query, filter_list, is_whitelist=False)

    def _check_filter_list(self, query, filter_list, is_whitelist):
        """Check if results are in list.

        Given a SQL query that returns a unique list of elements,
        e.g. select column from table group by column,
        check that the result types are in the whitelist (or not).
        """
        res = self.session.execute(query)
        rows = res.fetchall()
        for row in rows:
            label = row[0]
            if is_whitelist:  # This is whitelist.
                self.assertIn(
                    label,
                    filter_list,
                    msg='%s returned by (%s).' % (label, query))
            else:             # This is a blacklist.
                self.assertNotIn(
                    label,
                    filter_list,
                    msg='value found in (%s) is not permitted')

    def compute_null_proportion(
            self, query, corpus, table, column, expected, fails):

        res = self.session.execute(query.format(
                table=table, column=column, corpus=corpus))

        result = res.fetchall()

        if result:
            not_null_count = 0
            total = 0

            for r in result:
                val = r[0]
                total += 1
                if (val is not None
                        and not re.fullmatch(r'[\s*?#wxy0]*', str(val))):
                    not_null_count += 1

            actual = not_null_count / total

            t = (corpus, table, column, actual, expected)
            # print((corpus, table, column, actual, expected))

            if actual < expected:
                fails.append(t)

    def test_columns_for_proportion_null(self):
        """ Check proportion of nulls per table per corpus. """
        corpora = ["Chintang", "Cree", "Indonesian", "Inuktitut",
                   "Japanese_Miyata", "Japanese_MiiPro", "Russian",
                   "Sesotho", "Turkish", "Yucatec"]

        query = """
            SELECT {column}
            FROM v{table}
            WHERE corpus = '{corpus}'
        """

        msg = 'Proportion of non-NULL values too low:'

        fails = []

        # print('Computing proportions of non-nulls:')

        for row in self.reader_proportion_nulls:

            table = row[0]
            column = row[1]
            corpus = row[2]
            expected = float(row[3])

            if corpus == 'all':
                for corpus in corpora:
                    self.compute_null_proportion(
                        query, corpus, table, column, expected, fails)
            else:
                self.compute_null_proportion(
                    query, corpus, table, column, expected, fails)

        self.assertListEqual(fails, [], msg=msg+str(fails))

    def test_speaker_proportions(self):
        """Check proportion of (unique)speakers in utterances."""
        # in percent
        lowerbound = 70
        upperbound = 120

        uspeaker_sql = """

            SELECT
                t1.corpus,
                all_uniquespeakers,
                uniquespeakers_in_utterances,
                ROUND((CAST(uniquespeakers_in_utterances AS float)
                    /all_uniquespeakers)*100) AS proportion

            FROM
                (
                    SELECT corpus, COUNT(*) AS all_uniquespeakers
                    FROM uniquespeakers
                    GROUP BY corpus
                ) t1

                INNER JOIN

                (
                    SELECT vspeakers.corpus, 
                        COUNT(distinct vspeakers.uniquespeaker_id_fk)
                            AS uniquespeakers_in_utterances
                    FROM vutterances, vspeakers
                    WHERE vutterances.speaker_id_fk = vspeakers.id
                    GROUP BY vspeakers.corpus
                ) t2

                ON t1.corpus = t2.corpus"""

        speaker_sql = """
            SELECT
                t1.corpus,
                all_speakers,
                speakers_in_utterances,
                ROUND((CAST(speakers_in_utterances AS float)/all_speakers)*100)
                    AS proportion

            FROM
                (
                    SELECT corpus, COUNT(*) as all_speakers
                    FROM vspeakers
                    GROUP BY corpus
                ) t1

                INNER JOIN

                (
                    SELECT corpus, COUNT(distinct speaker_id_fk)
                        AS speakers_in_utterances
                    FROM vutterances
                    GROUP BY corpus
                ) t2

                ON t1.corpus = t2.corpus"""

        # check the uniquespeakers
        rows = self.session.execute(uspeaker_sql)
        for corpus, _, _, proportion in rows:
            self.assertGreaterEqual(
                proportion, lowerbound,
                msg="Proportion for uniquespeakers in {} too low.".format(
                        corpus))
            self.assertLessEqual(
                proportion, upperbound,
                msg="Proportion for uniquespeakers in {} too high.".format(
                        corpus))

        # check the speakers
        rows = self.session.execute(speaker_sql)
        for corpus, _, _, proportion in rows:
            # Russian has a lower threshold due to errors in the metadata
            # to be fixed via #512
            if corpus == "Russian":
                self.assertGreaterEqual(
                    proportion, 60,
                    msg="Proportion for speakers in {} too low.".format(
                            corpus))
            else:
                self.assertGreaterEqual(
                    proportion, lowerbound,
                    msg="Proportion for speakers in {} too low.".format(
                            corpus))

            self.assertLessEqual(
                proportion, upperbound,
                msg="Proportion for speakers in {} too high.".format(
                        corpus))


if __name__ == '__main__':
    unittest.main()
