import io
import unittest

from acqdiv.parsers.corpora.main.inuktitut.reader import \
    InuktitutReader


class TestInuktitutReader(unittest.TestCase):
    """Class to test the InuktitutReader."""

    def setUp(self):

        session = (
            '@UTF8\n'
            '@Begin\n'
            '@Languages:\tsme\n'
            '@Date:\t12-SEP-1997\n'
            '@Participants:\tMEM Mme_Manyili Grandmother , '
            'CHI Hlobohang Target_Child\n'
            '@ID:\tsme|Sesotho|MEM||female|||Grandmother|||\n'
            '@ID:\tsme|Sesotho|CHI|2;2.||||Target_Child|||\n'
            '@Birth of CHI:\t14-JAN-2006\n'
            '@Birth of MEM:\t11-OCT-1974\n'
            '@Media:\th2ab, audio\n'
            '@Comment:\tall snd kana jmor cha ok Wakachi2002;\n'
            '@Warning:\trecorded time: 1:00:00\n'
            '@Comment:\tuses desu and V-masu\n'
            '@Situation:\tAki and AMO preparing to look at book , '
            '"Miichan no otsukai"\n'
            '*MEM:\tke eng ? 0_8551\n'
            '%gls:\tke eng ?\n'
            '%cod:\tcp wh ?\n'
            '%eng:\tWhat is it ?\n'
            '%sit:\tPoints to tape\n'
            '%com:\tis furious\n'
            '%add:\tCHI\n'
            '*CHI:\tke ntencha ncha . 8551_19738\n'
            '%gls:\tke ntho e-ncha .\n'
            '%cod:\tcp thing(9 , 10) 9-aj .\n'
            '%eng:\tA new thing\n'
            '%com:\ttest comment\n'
            '*MEM:\tke eng ntho ena e? 19738_24653\n'
            '%gls:\tke eng ntho ena e ?\n'
            '%cod:\tcp wh thing(9 , 10) d9 ij ?\n'
            '%eng:\tWhat is this thing ?\n'
            '%sit:\tPoints to tape\n'
            '*CHI:\te nte ena . 24300_28048\n'
            '%gls:\tke ntho ena .\n'
            '%cod:\tcp thing(9 , 10) d9 .\n'
            '%eng:\tIt is this thing\n'
            '*MEM:\tke khomba\n'
            '\tkhomba . 28048_31840\n'
            '%gls:\tkekumbakumba .\n'
            '%cod:\tcp tape_recorder(9 , 10) .\n'
            '%eng:\tIt is a stereo\n'
            '@End')

        self.reader = InuktitutReader(io.StringIO(session))
        self.reader.load_next_record()
        self.maxDiff = None

    def test_get_start_time_start_time_present(self):
        """Test get_start_time for a case a start time existing."""
        self.reader.record.dependent_tiers['tim'] = '19301'
        actual_output = self.reader.get_start_time()
        desired_output = '19301'
        self.assertEqual(actual_output, desired_output)

    def test_get_start_time_start_time_absent(self):
        """Test get_start_time for a case no start time existing."""
        self.reader._dependent_tiers = {
            'utt': 'ha be'
        }
        actual_output = self.reader.get_start_time()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_end_time(self):
        """Test get_end_time. Result should be empty string."""
        actual_output = self.reader.get_end_time()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_target_alternative-method.

    def test_get_actual_alternative_single_alternative(self):
        """Test get_actual_alternative with 1 alternative."""
        utterance = 'nuutuinnaq [=? nauk tainna]'
        actual_output = InuktitutReader.get_actual_alternative(utterance)
        desired_output = 'nauk tainna'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_alternative_two_alternatives(self):
        """Test get_actual_alternative with 2 alternatives."""
        utterance = ('nuutuinnaq [=? nauk tainna] hela nuutuinnaq '
                     '[=? nauk tainna] .')
        actual_output = InuktitutReader.get_actual_alternative(utterance)
        desired_output = 'nauk tainna hela nauk tainna .'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_alternative_no_alternatives(self):
        """Test get_actual_alternative with 2 alternatives."""
        utterance = 'nuutuinnaq hela nuutuinnaq .'
        actual_output = InuktitutReader.get_actual_alternative(utterance)
        desired_output = 'nuutuinnaq hela nuutuinnaq .'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_alternative_empty_string(self):
        """Test get_actual_alternative with 2 alternatives."""
        utterance = ''
        actual_output = self.reader.get_actual_alternative(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_target_alternative-method.

    def test_get_target_alternative_single_alternative(self):
        """Test get_target_alternative with 1 alternative."""
        utterance = 'nuutuinnaq [=? nauk tainna]'
        actual_output = InuktitutReader.get_target_alternative(utterance)
        desired_output = 'nuutuinnaq'
        self.assertEqual(actual_output, desired_output)

    def test_get_target_alternative_two_alternatives(self):
        """Test get_target_alternative with 2 alternatives."""
        utterance = ('nuutuinnaq [=? nauk tainna] hela nuutuinnaq '
                     '[=? nauk tainna] .')
        actual_output = InuktitutReader.get_target_alternative(utterance)
        desired_output = 'nuutuinnaq hela nuutuinnaq .'
        self.assertEqual(actual_output, desired_output)

    # Test for the get_actual_utterance-method.

    def test_get_actual_utterance_one_per_inference_type(self):
        """Test get_actual_utterance with 1 example per inference type.

        Inference types:
        - alternatives
        - fragments
        - replacement
        - shortening
        """
        self.reader.record.utterance = \
            'nuutuinnaq [=? nauk tainna] mu:(ğ)ça &ab yarasam [: yorosom] .'
        actual_output = self.reader.get_actual_utterance()
        desired_output = 'nauk tainna mu:ça ab yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_two_per_inference_type(self):
        """Test get_actual_utterance with 2 examples per inference type.

        Inference types:
        - alternatives
        - fragments
        - replacement
        - shortening
        """
        self.reader.record.utterance = (
            '&ab mu:(ğ)ça nuutuinnaq [=? nauk tainna] mu:(ğ)ça &ab yarasam '
            '[: yorosom] yarasam [: yorosom] nuutuinnaq [=? nauk tainna] .')
        actual_output = self.reader.get_actual_utterance()
        desired_output = ('ab mu:ça nauk tainna mu:ça ab '
                          'yarasam yarasam nauk tainna .')
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_empty_string(self):
        """Test get_actual_utterance with an empty string."""
        self.reader.record.utterance = ''
        actual_output = self.reader.get_actual_utterance()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_target_utterance-method.

    def test_get_target_utterance_one_per_inference_type(self):
        """Test get_target_utterance with 1 example per inference type.

        Inference types:
        - alternatives
        - fragments
        - replacement
        - shortening
        """
        self.reader.record.utterance = \
            'nuutuinnaq [=? nauk tainna] mu:(ğ)ça &ab yarasam [: yorosom] .'
        actual_output = self.reader.get_target_utterance()
        desired_output = 'nuutuinnaq mu:ğça xxx yorosom .'
        self.assertEqual(actual_output, desired_output)

    def test_get_target_utterance_two_per_inference_type(self):
        """Test get_target_utterance with 2 examples per inference type.

        Inference types:
        - alternatives
        - fragments
        - replacement
        - shortening
        """
        self.reader.record.utterance = (
            '&ab mu:(ğ)ça nuutuinnaq [=? nauk tainna] mu:(ğ)ça &ab yarasam '
            '[: yorosom] yarasam [: yorosom] nuutuinnaq [=? nauk tainna] .')
        actual_output = self.reader.get_target_utterance()
        desired_output = ('xxx mu:ğça nuutuinnaq mu:ğça xxx '
                          'yorosom yorosom nuutuinnaq .')
        self.assertEqual(actual_output, desired_output)

    def test_get_target_utterance_empty_string(self):
        """Test get_target_utterance with an empty string."""
        self.reader.record.utterance = ''
        actual_output = self.reader.get_target_utterance()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_morph_tier-method.

    def test_get_morph_tier_morph_tier_present(self):
        """Test get_morph_tier with test.cha."""
        self.reader.record.dependent_tiers['xmor'] = 'test mor tier'
        actual_output = self.reader.get_morph_tier()
        desired_output = 'test mor tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_morph_tier_morph_tier_absent(self):
        """Test get_morph_tier with test.cha."""
        self.reader.record.dependent_tiers['xmor'] = ''
        actual_output = self.reader.get_morph_tier()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the iter_morphemes-method.

    def test_iter_morphemes_standard_case(self):
        """Test iter_morphemes with a morph in the expected format."""
        morph_word = 'WH|nani^whereat'
        actual_output = list(InuktitutReader.iter_morphemes(morph_word))
        desired_output = [('WH', 'nani', 'whereat')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_multiple_morphemes(self):
        """Test iter_morphemes with 3 morphe-words."""
        morph_words = 'VR|malik^follow+VV|liq^POL+VI|gitsi^IMP_2pS'
        actual_output = list(InuktitutReader.iter_morphemes(morph_words))
        desired_output = [('VR', 'malik', 'follow'),
                          ('VV', 'liq', 'POL'),
                          ('VI', 'gitsi', 'IMP_2pS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_no_match(self):
        """Test iter_morphemes with a morpheme that yields no match."""
        morph_word = 'WH|nani|whereat'
        actual_output = list(InuktitutReader.iter_morphemes(morph_word))
        desired_output = [('', '', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_empty_string(self):
        """Test iter_morphemes with an empty string."""
        morph_word = ''
        actual_output = list(InuktitutReader.iter_morphemes(morph_word))
        desired_output = [('', '', '')]
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_segments-method.

    def test_get_segments(self):
        """Test get_segments with a standard segment word."""
        xmor = 'VN|paaq^remove+VI|got^IMP_2sS'
        actual_output = InuktitutReader.get_segments(xmor)
        desired_output = ['paaq', 'got']
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_glosses-method.

    def test_get_glosses(self):
        """Test get_glosses with a standard gloss word."""
        xmor = 'VN|paaq^remove+VI|got^IMP_2sS'
        actual_output = InuktitutReader.get_glosses(xmor)
        desired_output = ['remove', 'IMP_2sS']
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_poses-method.

    def test_get_poses(self):
        """Test get_poses with a standard pos word."""
        xmor = 'VN|paaq^remove+VI|got^IMP_2sS'
        actual_output = InuktitutReader.get_poses(xmor)
        desired_output = ['VN', 'VI']
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_morpheme_language-method.

    def test_get_morpheme_language_inuktitut(self):
        """Test get_morpheme_language with a morpheme in Inuktitut."""
        seg, gloss, pos = 'ba', '1sg', 'V'
        actual_output = InuktitutReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'Inuktitut'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language_english(self):
        """Test get_morpheme_language with a morpheme in Inuktitut."""
        seg, gloss, pos = 'ba@e', '1sg', 'V'
        actual_output = InuktitutReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'English'
        self.assertEqual(actual_output, desired_output)