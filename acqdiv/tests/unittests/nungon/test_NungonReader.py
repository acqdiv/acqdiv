import unittest

from acqdiv.parsers.nungon.NungonReader import NungonReader


class TestNungonReader(unittest.TestCase):

    # ---------- get_morpheme_words ----------

    def test_get_morpheme_words_blank_spaces(self):
        """Test get_morpheme_words with blank spaces."""
        morph_tier = 'This is a test'
        actual_output = NungonReader.get_morpheme_words(morph_tier)
        desired_output = ['This', 'is', 'a', 'test']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_multiple_whitespaces(self):
        """Test get_morpheme_words with multiple whitespaces."""
        morph_tier = 'This   is  a  test'
        actual_output = NungonReader.get_morpheme_words(morph_tier)
        desired_output = ['This', 'is', 'a', 'test']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_clitics(self):
        """Test get_morpheme_words with clitics."""
        morph_tier = 'This=is a=test'
        actual_output = NungonReader.get_morpheme_words(morph_tier)
        desired_output = ['This', 'is', 'a', 'test']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_clitics_empty_string(self):
        """Test get_morpheme_words with empty string."""
        morph_tier = ''
        actual_output = NungonReader.get_morpheme_words(morph_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    # ---------- get_segments ----------

    def test_get_segments(self):
        """Test get_segments."""
        seg_word = 'one-two-three-four'
        actual_output = NungonReader.get_segments(seg_word)
        desired_output = ['one', 'two', 'three', 'four']
        self.assertEqual(actual_output, desired_output)

    def test_get_segments_empty_string(self):
        """Test get_segments with empty string."""
        seg_word = ''
        actual_output = NungonReader.get_segments(seg_word)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_gloss_pos ----------

    def test_get_iter_gloss_pos_only_stem(self):
        """Test iter_gloss_pos with only stem."""
        word = 'stempos^stemgloss'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('stemgloss', 'stempos')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_suffixes(self):
        """Test iter_gloss_pos with suffixes."""
        word = 'stempos^stemgloss-sfx1-sfx2.fs'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('stemgloss', 'stempos'),
                          ('sfx1', 'sfx'),
                          ('sfx2.fs', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_prefixes(self):
        """Test iter_gloss_pos with prefixes."""
        word = 'pfx1-pfx2.fs-stempos^stemgloss'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('pfx1', 'pfx'),
                          ('pfx2.fs', 'pfx'),
                          ('stemgloss', 'stempos')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_prefixes_suffixes(self):
        """Test iter_gloss_pos with prefixes and suffixes."""
        word = 'pfx1-pfx2.fs-stempos^stemgloss-sfx1-sfx2.fs'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('pfx1', 'pfx'),
                          ('pfx2.fs', 'pfx'),
                          ('stemgloss', 'stempos'),
                          ('sfx1', 'sfx'),
                          ('sfx2.fs', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_no_stem_one_morpheme(self):
        """Test iter_gloss_pos with one morpheme and no stem marker."""
        word = 'gloss'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('gloss', '')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_no_stem_multiple_morphemes(self):
        """Test iter_gloss_pos with multiple morphemes and no stem marker."""
        word = 'gloss1.fs-gloss2-gloss3'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('gloss1.fs', ''), ('gloss2', ''), ('gloss3', '')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_multiple_carets(self):
        """Test iter_gloss_pos with multiple carets."""
        word = 'n^v^stem-sfx'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('stem', 'n^v'), ('sfx', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    # ---------- get_glosses ----------

    def test_get_glosses(self):
        """Test get_glosses."""
        word = 'pfx1-pfx2.fs-stempos^stemgloss-sfx1-sfx2.fs'
        actual_output = NungonReader.get_glosses(word)
        desired_output = ['pfx1', 'pfx2.fs', 'stemgloss', 'sfx1', 'sfx2.fs']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_poses ----------

    def test_get_poses(self):
        """Test get_poses."""
        word = 'pfx1-pfx2.fs-stempos^stemgloss-sfx1-sfx2.fs'
        actual_output = NungonReader.get_poses(word)
        desired_output = ['pfx', 'pfx', 'stempos', 'sfx', 'sfx']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_morpheme_language ----------

    def test_get_morpheme_language_tok_pisin(self):
        """Test get_morpheme_language with Tok Pisin."""
        seg = ''
        gloss = ''
        pos = 'tpn'
        actual_output = NungonReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'Tok Pisin'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language_english(self):
        """Test get_morpheme_language with English."""
        seg = ''
        gloss = ''
        pos = 'engn'
        actual_output = NungonReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'English'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language_nungon(self):
        """Test get_morpheme_language with Nungon."""
        seg = ''
        gloss = ''
        pos = 'n'
        actual_output = NungonReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'Nungon'
        self.assertEqual(actual_output, desired_output)