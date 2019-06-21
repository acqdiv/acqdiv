import unittest

from acqdiv.parsers.yucatec.YucatecReader import YucatecReader


class TestYucatecReader(unittest.TestCase):

    # ---------- get_utterance_words ----------

    def test_get_utterance_words_standard_case(self):
        """Test get_utterance_words for standard input."""
        utterance = 'ke eng ntho ena e?'
        actual_output = YucatecReader.get_utterance_words(utterance)
        desired_output = ['ke', 'eng', 'ntho', 'ena', 'e?']
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words_empty_string(self):
        """Test get_utterance_words for standard input."""
        utterance = ''
        actual_output = YucatecReader.get_utterance_words(utterance)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words_multiple_blank_spaces(self):
        """Test get_utterance_words with multiple blank spaces."""
        utterance = 'ke eng  ntho ena   e?'
        actual_output = YucatecReader.get_utterance_words(utterance)
        desired_output = ['ke', 'eng', 'ntho', 'ena', 'e?']
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words_ampersand(self):
        """Test with ampersand."""
        utterance = 'This is&a test'
        actual_output = YucatecReader.get_utterance_words(utterance)
        desired_output = ['This', 'is', 'a', 'test']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_morpheme_words ----------

    def test_get_morpheme_words_no_clitics(self):
        """Test get_morpheme_words with no clitics."""
        morph_tier = 'P|ráʔ P|riʔ P|ruʔ'
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = ['P|ráʔ', 'P|riʔ', 'P|ruʔ']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_multiple_spaces(self):
        """Test get_morpheme_words with multiple spaces."""
        morph_tier = 'P|ráʔ  P|riʔ   P|ruʔ'
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = ['P|ráʔ', 'P|riʔ', 'P|ruʔ']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_empty_string(self):
        """Test get_morpheme_words with empty string."""
        morph_tier = ''
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_proclitic(self):
        """Test get_morpheme_words with a proclitic."""
        morph_tier = 'P|ráʔ P|riʔ P|kiʔ&P|ruʔ'
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = ['P|ráʔ', 'P|riʔ', 'P|kiʔ', 'P|ruʔ']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_postclitic(self):
        """Test get_morpheme_words with a postclitic."""
        morph_tier = 'P|ráʔ P|riʔ P|ruʔ+P|kuʔ'
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = ['P|ráʔ', 'P|riʔ', 'P|ruʔ', 'P|kuʔ']
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_morphemes ----------

    def test_iter_morphemes_completely_unstructured(self):
        """Test iter_morphemes with completely unstructured word."""
        word = 'mone-mtwo-mthree'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('mone', '', ''),
                          ('mtwo', '', ''),
                          ('mthree', '', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_prefixes(self):
        """Test iter_morphemes with structured prefixes."""
        word = 'PFXGLOSS1|pfxone#PFXGLOSS2|pfxtwo#N|stem'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('pfxone', 'PFXGLOSS1', 'pfx'),
                          ('pfxtwo', 'PFXGLOSS2', 'pfx'),
                          ('stem', '', 'N')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_stem_with_pos(self):
        """Test iter_morphemes with structured stem with POS tag."""
        word = 'N|stem'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'N')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_stem_with_gloss(self):
        """Test iter_morphemes with structured stem only with gloss."""
        word = 'STEMPOS|stem'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', 'STEMPOS', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_unstructured_stem_with_seg(self):
        """Test iter_morphemes with unstructured stem with segment."""
        word = 'stem'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_unstructured_stem_with_gloss(self):
        """Test iter_morphemes with unstructured stem with segment."""
        word = 'STEMGLOSS1'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('', 'STEMGLOSS1', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_suffixes(self):
        """Test iter_morphemes with structured suffixes."""
        word = 'N|stem:SFXGLOSS1|-sfxone:SFXGLOSS2|-sfxtwo'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'N'),
                          ('sfxone', 'SFXGLOSS1', 'sfx'),
                          ('sfxtwo', 'SFXGLOSS2', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_suffixes_without_dash(self):
        """Test iter_morphemes with structured suffixes without dash."""
        word = 'N|stem:SFXGLOSS1|sfxone:SFXGLOSS2|sfxtwo'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'N'),
                          ('sfxone', 'SFXGLOSS1', 'sfx'),
                          ('sfxtwo', 'SFXGLOSS2', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_unstructured_suffixes(self):
        """Test iter_morphemes with unstructured suffixes."""
        word = 'N|stem-SFX1-SFX2'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'N'),
                          ('', 'SFX1', 'sfx'),
                          ('', 'SFX2', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes_suffixes(self):
        """Test iter_morphemes with prefixes and suffixes."""
        word = ('PFXGLOSS1|pfxone#PFXGLOSS2|pfxtwo#'
                'N|stem'
                ':SFXGLOSS1|-sfxone:SFXGLOSS2|-sfxtwo')
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('pfxone', 'PFXGLOSS1', 'pfx'),
                          ('pfxtwo', 'PFXGLOSS2', 'pfx'),
                          ('stem', '', 'N'),
                          ('sfxone', 'SFXGLOSS1', 'sfx'),
                          ('sfxtwo', 'SFXGLOSS2', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_subpos_subgloss_colon(self):
        """Test iter_morphemes with sub POS tag and sub glosses with colons."""
        word = ('PFXGLOSS:PFXSUBGLOSS|pfx#'
                'N:PROP|stem'
                ':SFXGLOSS:SFXSUBGLOSS|-sfx')
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('pfx', 'PFXGLOSS:PFXSUBGLOSS', 'pfx'),
                          ('stem', '', 'N:PROP'),
                          ('sfx', 'SFXGLOSS:SFXSUBGLOSS', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_subpos_subgloss_dot(self):
        """Test iter_morphemes with sub POS tag and sub glosses with dots."""
        word = ('PFXGLOSS.PFXSUBGLOSS|pfx#'
                'N.PROP|stem'
                ':SFXGLOSS.SFXSUBGLOSS|-sfx')
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('pfx', 'PFXGLOSS.PFXSUBGLOSS', 'pfx'),
                          ('stem', '', 'N.PROP'),
                          ('sfx', 'SFXGLOSS.SFXSUBGLOSS', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_untranscribed(self):
        """Test iter_morphemes with untranscribed morpheme."""
        word = 'xxx'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('', '', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_dash_stem(self):
        """Test with dash in front of stem."""
        word = 'CLFR.INAN|-stem:PRON|-sfx'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'CLFR.INAN'),
                          ('sfx', 'PRON', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_0(self):
        """Test with 0."""
        word = 'V:TRANS|stem:IMP|-0:PREP|sfx'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'V:TRANS'),
                          ('0', 'IMP', 'sfx'),
                          ('sfx', 'PREP', 'sfx')]
        self.assertEqual(actual_output, desired_output)