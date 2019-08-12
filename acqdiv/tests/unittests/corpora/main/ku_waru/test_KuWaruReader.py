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

    def test_get_pos_words_parentheses(self):
        pos_tier = 'pro   n(TP)  v  (eV) -v:PROG'
        actual_output = KuWaruReader.get_pos_words(pos_tier)
        desired_output = [
            'pro',
            'n(TP)',
            'v  (eV) -v:PROG'
        ]
        self.assertEqual(actual_output, desired_output)

    def test_get_poses_affixes(self):
        pos_word = 'bla- dem      -prt -post'
        actual_output = KuWaruReader.get_poses(pos_word)
        desired_output = ['bla-', 'dem', '-prt', '-post']
        self.assertEqual(actual_output, desired_output)

    def test_get_poses_clitics(self):
        pos_word = 'bla= dem      =prt =post'
        actual_output = KuWaruReader.get_poses(pos_word)
        desired_output = ['bla=', 'dem', '=prt', '=post']
        self.assertEqual(actual_output, desired_output)

    def test_get_poses_affixes_and_clitics(self):
        pos_word = 'bla= blu- dem      -prt =post'
        actual_output = KuWaruReader.get_poses(pos_word)
        desired_output = ['bla=', 'blu-', 'dem', '-prt', '=post']
        self.assertEqual(actual_output, desired_output)

    def test_get_poses_parentheses(self):
        pos_word = 'v  (eV) -v:PROG'
        actual_output = KuWaruReader.get_poses(pos_word)
        desired_output = ['v  (eV)', '-v:PROG']
        self.assertEqual(actual_output, desired_output)
