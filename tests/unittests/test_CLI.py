import unittest
import subprocess
import sqlite3
import datetime
from pathlib import Path


class CLITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        unittest_dir = Path(__file__).parent
        cfg = unittest_dir / 'resources/config.ini'
        subprocess.run(f'acqdiv load -c {cfg}', shell=True)
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        path = unittest_dir / f'resources/acqdiv_corpus_{date}.sqlite3'
        conn = sqlite3.connect(str(path))
        cls.cursor = conn.cursor()

    def test_n_corpora(self):
        res = self.cursor.execute('SELECT * FROM corpora')
        self.assertEqual(len(res.fetchall()), 9)

    def test_n_utterances(self):
        res = self.cursor.execute('SELECT * FROM utterances')
        self.assertEqual(len(res.fetchall()), 14)


if __name__ == '__main__':
    unittest.main()
