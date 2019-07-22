import unittest

from acqdiv.parsers.corpora.main.ku_waru.KuWaruReader import KuWaruReader


class TestKuWaruReader(unittest.TestCase):

    def test_get_pos_words(self):
        pos_tier = 'prt(TP) n      n    =post dem      =prt =post v   -v:FUT'
        actual_output = KuWaruReader.get_pos_words(pos_tier)
        desired_output = [
            'prt(TP)',
            'n',
            'n    =post',
            'dem      =prt =post',
            'v   -v:FUT'
        ]
        self.assertEqual(actual_output, desired_output)
