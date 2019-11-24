import unittest
import subprocess
import sqlite3
import os
import configparser
import datetime
from pathlib import Path


class CLITest(unittest.TestCase):

    db_path = None
    cfg_parser = None
    cfg = None
    old_corpora_dir = None
    old_db_dir = None

    @classmethod
    def setUpClass(cls) -> None:
        unittest_dir = Path(__file__).parent
        resources_dir = unittest_dir / 'resources'

        # Read the config
        cls.cfg = resources_dir / 'config.ini'
        cls.cfg_parser = configparser.ConfigParser()
        cls.cfg_parser.read(cls.cfg)

        # Save old paths in config
        cls.old_corpora_dir = cls.cfg_parser['.global']['corpora_dir']
        cls.old_db_dir = cls.cfg_parser['.global']['db_dir']

        # Change paths in config
        corpora_dir = resources_dir / 'corpora'
        cls.cfg_parser['.global']['corpora_dir'] = str(corpora_dir)
        cls.cfg_parser['.global']['db_dir'] = str(resources_dir)

        # Write new paths to config
        with open(cls.cfg, 'w') as configfile:
            cls.cfg_parser.write(configfile)

        # Run CLI
        subprocess.run(f'acqdiv load -c {cls.cfg}', shell=True)

        date = datetime.datetime.now().strftime('%Y-%m-%d')
        cls.db_path = resources_dir / f'acqdiv_corpus_{date}.sqlite3'
        conn = sqlite3.connect(str(cls.db_path))
        cls.cursor = conn.cursor()

    def test_n_corpora(self):
        res = self.cursor.execute('SELECT * FROM corpora')
        self.assertEqual(len(res.fetchall()), 10)

    def test_n_utterances(self):
        res = self.cursor.execute('SELECT * FROM utterances')
        self.assertEqual(len(res.fetchall()), 15)

    @classmethod
    def tearDownClass(cls) -> None:
        # Write old paths back to config
        cls.cfg_parser['.global']['corpora_dir'] = cls.old_corpora_dir
        cls.cfg_parser['.global']['db_dir'] = cls.old_db_dir
        with open(cls.cfg, 'w') as configfile:
            cls.cfg_parser.write(configfile)

        # Delete database
        os.remove(cls.db_path)


if __name__ == '__main__':
    unittest.main()
