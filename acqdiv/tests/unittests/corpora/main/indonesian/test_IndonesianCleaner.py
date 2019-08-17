import unittest

from acqdiv.parsers.corpora.main.indonesian.IndonesianCleaner \
    import IndonesianCleaner as Cl


class IndonesianCleanerTest(unittest.TestCase):

    def test_clean_utterance(self):
        utterance = '0.'
        actual = Cl.clean_utterance(utterance)
        expected = '???'
        self.assertEqual(actual, expected)

    def test_clean_gloss(self):
        gloss = 'N-'
        actual = Cl.clean_gloss(gloss)
        expected = 'AV'
        self.assertEqual(actual, expected)

    def test_clean_pos(self):
        pos = 'bye'
        actual = Cl.clean_pos(pos)
        expected = 'stem'
        self.assertEqual(actual, expected)

    def test_clean_pos_ud(self):
        pos_ud = 'bye'
        actual = Cl.clean_pos_ud(pos_ud)
        expected = ''
        self.assertEqual(actual, expected)
