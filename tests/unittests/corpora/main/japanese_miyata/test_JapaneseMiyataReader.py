import unittest
from acqdiv.parsers.corpora.main.japanese_miyata.reader import \
    JapaneseMiyataReader


class TestJapaneseMiyataReader(unittest.TestCase):

    # Tests for the iter_morphemes-method.

    def test_iter_morphemes_stem_no_gloss(self):
        """Test iter_morphemes with stem and no gloss."""
        word = 'stem:POS|stem'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('stem', '', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_stem_gloss(self):
        """Test iter_morphemes with stem and gloss."""
        word = 'stem:POS|stem=stemgloss'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('stem', 'stemgloss', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffixes_no_stemgloss(self):
        """Test iter_morphemes with suffixes and no stem gloss."""
        word = 'stem:POS|stem-SFXONE-SFXTWO'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('stem', '', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffixes_stemgloss(self):
        """Test iter_morphemes with suffixes and stem gloss."""
        word = 'stem:POS|stem-SFXONE-SFXTWO=stemgloss'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('stem', 'stemgloss', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffixes_colon(self):
        """Test iter_morphemes with suffix and colon."""
        word = 'stem:POS|stem-SFXONE:contr-SFXTWO:SFXTWOseg=stemgloss'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('stem', 'stemgloss', 'stem:POS'),
                          ('', 'SFXONE:contr', 'sfx'),
                          ('SFXTWOseg', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes(self):
        """Test iter_morphemes with prefixes."""
        word = 'pfxone#pfxtwo#stem:POS|stem=stemgloss'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('pfxone', '', 'pfx'),
                          ('pfxtwo', '', 'pfx'),
                          ('stem', 'stemgloss', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes_suffixes_stemgloss(self):
        """Test iter_morphemes with prefixes, suffixes and stem gloss."""
        word = 'pfxone#pfxtwo#stem:POS|stem-SFXONE-SFXTWO=stemgloss'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('pfxone', '', 'pfx'),
                          ('pfxtwo', '', 'pfx'),
                          ('stem', 'stemgloss', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_no_gloss(self):
        """Test iter_morphemes with compound and no stem gloss."""
        word = 'CMPPOS|+CMPPOSONE|cmpstemone+CMPPOSTWO|cmpstemtwo'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('=cmpstemone', '', 'CMPPOSONE'),
                          ('=cmpstemtwo', '', 'CMPPOSTWO')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_gloss(self):
        """Test iter_morphemes with compound and stem gloss."""
        word = 'CMPPOS|+CMPPOSONE|cmpstemone+CMPPOSTWO|cmpstemtwo=cmpgloss'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('=cmpstemone', 'cmpgloss', 'CMPPOSONE'),
                          ('=cmpstemtwo', 'cmpgloss', 'CMPPOSTWO')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_suffixes(self):
        """Test iter_morphemes with compound and suffixes."""
        word = ('CMPPOS|+CMPPOSONE|cmpstemone-SFXONE'
                '+CMPPOSTWO|cmpstemtwo-SFXTWO=cmpgloss')
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('=cmpstemone', 'cmpgloss', 'CMPPOSONE'),
                          ('', 'SFXONE', 'sfx'),
                          ('=cmpstemtwo', 'cmpgloss', 'CMPPOSTWO'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_prefix(self):
        """Test iter_morphemes with compound and prefix."""
        word = ('pfxone#CMPPOS|+CMPPOSONE|cmpstemone-SFXONE'
                '+CMPPOSTWO|cmpstemtwo-SFXTWO=cmpgloss')
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('pfxone', '', 'pfx'),
                          ('=cmpstemone', 'cmpgloss', 'CMPPOSONE'),
                          ('', 'SFXONE', 'sfx'),
                          ('=cmpstemtwo', 'cmpgloss', 'CMPPOSTWO'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_sfx_gloss(self):
        """Test iter_morphemes with suffix segment."""
        word = 'stem:POS|stem-sfxseg=stemgloss_SFXGLOSS'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('stem', 'stemgloss', 'stem:POS'),
                          ('sfxseg', 'SFXGLOSS', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_multiple_stem_glosses(self):
        """Test iter_morphemes with multiple stem glosses."""
        word = 'stem:POS|stem-sfxseg=stemgloss1_stemgloss2_SFXGLOSS'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('stem', 'stemgloss1_stemgloss2', 'stem:POS'),
                          ('sfxseg', 'SFXGLOSS', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_fusionalsfx(self):
        """Test iter_morphemes with fusional suffix."""
        word = 'stem:POS|stem&FUS=stemgloss'
        actual_output = list(JapaneseMiyataReader.iter_morphemes(word))
        desired_output = [('stem', 'stemgloss.FUS', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)