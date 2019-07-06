import unittest

from acqdiv.parsers.corpora.main.english.EnglishManchester1Reader import \
    EnglishManchester1Reader


class TestEnglishManchester1ReaderGeneric(unittest.TestCase):

    # ---------- get_word_language ----------

    def test_get_word_language_english(self):
        word = 'yes'
        actual_output = EnglishManchester1Reader.get_word_language(word)
        desired_output = 'English'
        self.assertEqual(actual_output, desired_output)

    def test_get_word_language_french(self):
        word = 'oui@s:fra'
        actual_output = EnglishManchester1Reader.get_word_language(word)
        desired_output = 'French'
        self.assertEqual(actual_output, desired_output)

    def test_get_word_language_italian(self):
        word = 'si@s:ita'
        actual_output = EnglishManchester1Reader.get_word_language(word)
        desired_output = 'Italian'
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_morphemes ----------

    def test_iter_morphemes_stem_no_gloss(self):
        """Test iter_morphemes with stem and no gloss."""
        word = 'stem:POS|stem&FUS'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stem&FUS', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_stem_gloss(self):
        """Test iter_morphemes with stem and gloss."""
        word = 'stem:POS|stem&FUS=stemgloss'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stemgloss', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffixes(self):
        """Test iter_morphemes with suffixes."""
        word = 'stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stem&FUS', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes(self):
        """Test iter_morphemes with prefixes."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('pfxone', 'pfxone', 'pfx'),
                          ('pfxtwo', 'pfxtwo', 'pfx'),
                          ('stem&FUS', 'stem&FUS', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes_suffixes_stemgloss(self):
        """Test iter_morphemes with prefixes, suffixes and stem gloss."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('pfxone', 'pfxone', 'pfx'),
                          ('pfxtwo', 'pfxtwo', 'pfx'),
                          ('stem&FUS', 'stem&FUS', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound(self):
        """Test iter_morphemes with compound."""
        word = 'CMPPOS|+CMPPOSONE|cmpstemone+CMPPOSTWO|cmpstemtwo'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('=cmpstemone', 'cmpstemone', 'CMPPOSONE'),
                          ('=cmpstemtwo', 'cmpstemtwo', 'CMPPOSTWO')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_suffixes(self):
        """Test iter_morphemes with compound and suffixes."""
        word = ('CMPPOS|+CMPPOSONE|cmpstemone-SFXONE'
                '+CMPPOSTWO|cmpstemtwo-SFXTWO')
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('=cmpstemone', 'cmpstemone', 'CMPPOSONE'),
                          ('', 'SFXONE', 'sfx'),
                          ('=cmpstemtwo', 'cmpstemtwo', 'CMPPOSTWO'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_clitic(self):
        """Test iter_morphemes with clitic."""
        word = 'stem:POSone|stem&FUSone~stem:POStwo|stem&FUStwo'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUSone', 'stem&FUSone', 'stem:POSone'),
                          ('stem&FUStwo', 'stem&FUStwo', 'stem:POStwo')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_clitic_suffix(self):
        """Test iter_morphemes with clitic and suffix."""
        word = 'stem:POSone|stem&FUSone-SFX~stem:POStwo|stem&FUStwo'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUSone', 'stem&FUSone', 'stem:POSone'),
                          ('', 'SFX', 'sfx'),
                          ('stem&FUStwo', 'stem&FUStwo', 'stem:POStwo')]
        self.assertEqual(actual_output, desired_output)

    # ---------- get_morpheme_language ----------

    def test_get_morpheme_languageEnglish(self):
        """Test get_morpheme_language with English."""
        seg = ''
        gloss = ''
        pos = 'N'
        actual_output = EnglishManchester1Reader.get_morpheme_language(
            seg, gloss, pos)
        desired_output = 'English'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_languageL2(self):
        """Test get_morpheme_language with L2."""
        seg = ''
        gloss = ''
        pos = 'L2'
        actual_output = EnglishManchester1Reader.get_morpheme_language(
            seg, gloss, pos)
        desired_output = 'FOREIGN'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_segments ----------

    def test_get_segments(self):
        """Test get_segments."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = EnglishManchester1Reader.get_segments(word)
        desired_output = ['pfxone', 'pfxtwo', 'stem&FUS', '', '']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_glosses ----------

    def test_get_glosses(self):
        """Test get_glosses."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = EnglishManchester1Reader.get_glosses(word)
        desired_output = ['pfxone', 'pfxtwo', 'stem&FUS', 'SFXONE', 'SFXTWO']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_poses ----------

    def test_get_poses(self):
        """Test get_poses."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = EnglishManchester1Reader.get_poses(word)
        desired_output = ['pfx', 'pfx', 'stem:POS', 'sfx', 'sfx']
        self.assertEqual(actual_output, desired_output)