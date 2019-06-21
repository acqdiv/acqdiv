import unittest

from acqdiv.parsers.corpora.main.turkish.TurkishReader import TurkishReader


class TestTurkishReader(unittest.TestCase):

    def test_iter_morphemes_no_suffixes(self):
        """Test iter_morphemes with only stem."""
        word = 'STEMPOS|stem'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem', '', 'STEMPOS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_sub_POS(self):
        """Test iter_morphemes with sub POS tag."""
        word = 'STEMPOS:STEMSUBPOS|stem'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem', '', 'STEMPOS:STEMSUBPOS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_multiple_suffixes(self):
        """Test iter_morphemes with multiple suffixes."""
        word = 'STEMPOS|stem-SFX1-SFX2-SFX3'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem', '', 'STEMPOS'),
                          ('', 'SFX1', 'sfx'),
                          ('', 'SFX2', 'sfx'),
                          ('', 'SFX3', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffix_sub_gloss(self):
        """Test iter_morphemes with suffix sub gloss."""
        word = 'STEMPOS|stem-SFX1-SFX2&SUBSFX2-SFX3'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem', '', 'STEMPOS'),
                          ('', 'SFX1', 'sfx'),
                          ('', 'SFX2&SUBSFX2', 'sfx'),
                          ('', 'SFX3', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_underscore(self):
        """Test iter_morphemes with underscore."""
        word = 'STEMPOS|stem1_stem2-SFX'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem1_stem2', '', 'STEMPOS'),
                          ('', 'SFX', 'sfx')]
        self.assertEqual(actual_output, desired_output)