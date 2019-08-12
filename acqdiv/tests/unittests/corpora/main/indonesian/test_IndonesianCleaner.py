import unittest

from acqdiv.parsers.corpora.main.indonesian.IndonesianCleaner \
    import IndonesianCleaner


class IndonesianCleanerTest(unittest.TestCase):

    def test_clean_utterance(self):
        utterance = '0.'
        actual = IndonesianCleaner.clean_utterance(utterance)
        expected = '???'
        self.assertEqual(actual, expected)
