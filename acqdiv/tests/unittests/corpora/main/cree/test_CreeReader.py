import io
import unittest

from acqdiv.parsers.corpora.main.cree.CreeReader import CreeReader


class TestCreeReader(unittest.TestCase):
    """Class to test the CreeReader."""

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

    def test_get_main_morpheme(self):
        """Test get_main_morpheme. Should return 'segment'."""
        actual_output = CreeReader.get_main_morpheme()
        desired_output = 'segment'
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_tier_seg_tier_present(self):
        """Test get_seg_tier with utt containing seg_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        reader = CreeReader(io.StringIO(session_str))
        reader.load_next_record()
        actual_output = reader.get_seg_tier()
        desired_output = '[wo *]'
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_tier_seg_tier_absent(self):
        """Test get_seg_tier with utt not containing a seg_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xmormea:\t'
                       '[egg 1]\n@End')
        reader = CreeReader(io.StringIO(session_str))
        reader.load_next_record()
        actual_output = reader.get_seg_tier()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier_gloss_tier_present(self):
        """Test get_gloss_tier with utt containing gloss_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        reader = CreeReader(io.StringIO(session_str))
        reader.load_next_record()
        actual_output = reader.get_gloss_tier()
        desired_output = '[egg 1]'
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier_gloss_tier_absent(self):
        """Test get_gloss_tier with utt not containing a gloss_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n@End')
        reader = CreeReader(io.StringIO(session_str))
        reader.load_next_record()
        actual_output = reader.get_gloss_tier()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier_pos_tier_present(self):
        """Test get_pos_tier with utt containing pos_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        reader = CreeReader(io.StringIO(session_str))
        reader.load_next_record()
        actual_output = reader.get_pos_tier()
        desired_output = '[ni pro]'
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier_pos_tier_absent(self):
        """Test get_pos_tier with utt not containing a pos_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        reader = CreeReader(io.StringIO(session_str))
        reader.load_next_record()
        actual_output = reader.get_pos_tier()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes_one_tilde(self):
        """Test get_morphemes with morpheme-word containing one tilde."""
        morph_word = 'first~second'
        actual_output = CreeReader.get_morphemes(morph_word)
        desired_output = ['first', 'second']
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes_multiple_tildes(self):
        """Test get_morphemes with morpheme-word containing 3 tildes."""
        morph_word = 'first~second~third~fourth'
        actual_output = CreeReader.get_morphemes(morph_word)
        desired_output = ['first', 'second', 'third', 'fourth']
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes_no_tilde(self):
        """Test get_morphemes with morpheme-word containing no tilde."""
        morph_word = 'first'
        actual_output = CreeReader.get_morphemes(morph_word)
        desired_output = ['first']
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes_empty_string(self):
        """Test get_morphemes with morpheme-word containing no tilde."""
        morph_word = ''
        actual_output = CreeReader.get_morphemes(morph_word)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_segments(self):
        """Test get_segments.

        Just one test because the method only calls get_morphemes.
        """
        seg_word = 'first'
        actual_output = CreeReader.get_segments(seg_word)
        desired_output = ['first']
        self.assertEqual(actual_output, desired_output)

    def test_get_glosses(self):
        """Test get_glosses.

        Just one test because the method only calls get_morphemes.
        """
        seg_word = 'first~second'
        actual_output = CreeReader.get_glosses(seg_word)
        desired_output = ['first', 'second']
        self.assertEqual(actual_output, desired_output)

    def test_get_poses(self):
        """Test get_poses.

        Just one test because the method only calls get_morphemes.
        """
        seg_word = 'first~second~third'
        actual_output = CreeReader.get_glosses(seg_word)
        desired_output = ['first', 'second', 'third']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language_cree(self):
        """Test get_morpheme_language with (pseudo-)cree morpheme."""
        seg = 'hem'
        gloss = '1sg'
        pos = 'V'
        actual_output = CreeReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'Cree'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language_english(self):
        """Test get_morpheme_language with english mopheme."""
        seg = 'fly'
        gloss = 'Eng'
        pos = 'V'
        actual_output = CreeReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'English'
        self.assertEqual(actual_output, desired_output)