import io
import unittest

from acqdiv.parsers.corpora.main.sesotho.SesothoReader import SesothoReader


class TestSesothoReader(unittest.TestCase):

    def setUp(self):
        self.reader = SesothoReader()
        self.maxDiff = None

    def test_join_morph_to_utt_only_hyphens(self):
        """Test join_morph_to_utt with standard case of only hyphens."""
        record = ('*CHI:\tplaceholder\n%gls:\ter-e m-ph-e ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader._join_morph_to_utt()
        desired_output = 'ere mphe ntho ena .'
        self.assertEqual(actual_output, desired_output)

    def test_join_morph_to_utt_hyphens_and_parentheses(self):
        """Test join_morph_to_utt with hyphens and parentheses."""
        record = ('*CHI:\tplaceholder\n%gls:\ter-e m-ph-e (ag)ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader._join_morph_to_utt()
        desired_output = 'ere mphe (ag)ntho ena .'
        self.assertEqual(actual_output, desired_output)

    def test_join_morph_to_utt_empty_string(self):
        """Test join_morph_to_utt with an empty string.

        The wrong naming of the gloss tier leads to an empty string
        to be processed.
        """
        record = ('*CHI:\tplaceholder\n%gla:\ter-e m-ph-e (ag)ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader._join_morph_to_utt()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance(self):
        """Test get_utterance."""
        record = ('*CHI:\tbla blu bli .\n%gls:\ter-e m-ph-e ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader.get_utterance()
        desired_output = 'bla blu bli .'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance(self):
        """Test get_actual_utterance with standard case of only hyphens."""
        record = ('*CHI:\tplaceholder\n%gls:\ter-e m-ph-e ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader.get_actual_utterance()
        desired_output = 'ere mphe ntho ena .'
        self.assertEqual(actual_output, desired_output)

    def test_get_target_utterance(self):
        """Test get_target_utterance with standard case of only hyphens."""
        record = ('*CHI:\tplaceholder\n%gls:\ter-e m-ph-e ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader.get_target_utterance()
        desired_output = 'ere mphe ntho ena .'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_noun_prefix(self):
        """Test infer_poses with with a prefix of a noun.

        The entire morpheme word is: n^6-eye(5 , 6)'
        """
        mor = 'n^6'
        actual_output = self.reader.infer_pos(mor, 2)
        desired_output = 'pfx'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_noun_stem(self):
        """Test infer_poses with a noun stem.

        The entire morpheme word is: n^6-eye(5 , 6)'
        """
        mor = 'eye(5 , 6)'
        actual_output = self.reader.infer_pos(mor, 2)
        desired_output = 'n'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_verb_prefix(self):
        """Test infer_poses with the prefix of a verb.

        The entire morpheme word is: 'sm2s-t^f1-v^say-m^in'
        """
        mor = 'sm2s'
        actual_output = self.reader.infer_pos(mor, 4)
        desired_output = 'pfx'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_verb_suffix(self):
        """Test infer_poses with the suffix of a verb.

        The entire morpheme word is: 'sm2s-t^f1-v^say-m^in'
        """
        mor = 'm^in'
        # First infer pos of stem for passed_stem to be set to True.
        self.reader.infer_pos('v^say', 4)
        actual_output = self.reader.infer_pos(mor, 4)
        desired_output = 'sfx'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_verb_stem(self):
        """Test infer_poses with a verb stem.

        The verb contains 2 suffixes and one prefix.
        The entire morpheme word is: 'sm2s-t^f1-v^say-m^in'
        """
        mor = 'v^say'
        actual_output = self.reader.infer_pos(mor, 4)
        desired_output = 'v'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_nominal_concord(self):
        """Test infer_poses with a nominal concord."""
        mor = 'obr3'
        actual_output = self.reader.infer_pos(mor, 1)
        desired_output = 'obr'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_particle(self):
        """Test infer_poses with a particle."""
        mor = 'loc'
        actual_output = self.reader.infer_pos(mor, 1)
        desired_output = 'loc'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_free_person_marker(self):
        """Test infer_poses with a free person marker."""
        mor = 'sm1s'
        actual_output = self.reader.infer_pos(mor, 1)
        desired_output = 'afx.detached'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_copula(self):
        """Test infer_poses with a copula."""
        mor = 'cp'
        actual_output = self.reader.infer_pos(mor, 1)
        desired_output = 'cop'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_ideophone(self):
        """Test infer_poses with an ideophone."""
        mor = 'id^jump'
        actual_output = self.reader.infer_pos(mor, 1)
        desired_output = 'ideoph'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_untranscibed(self):
        """Test infer_poses with an untranscribed morpheme word."""
        mor = 'xxx'
        actual_output = self.reader.infer_pos(mor, 1)
        desired_output = 'none'
        self.assertEqual(actual_output, desired_output)

    def test_infer_poses_empty_string(self):
        """Test infer_poses with an empty string."""
        mor = ''
        actual_output = self.reader.infer_pos(mor, 1)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_single(self):
        """Test iter_morphemes with a morpheme word containing one morpheme."""
        morph_word = 'id^jump'
        actual_output = list(self.reader.iter_gloss_pos(morph_word))
        desired_output = [('id^jump', 'ideoph')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_multiple(self):
        """Test iter_morphemes with a morpheme word containing 4 morphemes."""
        morph_word = 'sm1-t^p-v^say-m^in'
        actual_output = list(self.reader.iter_gloss_pos(morph_word))
        desired_output = [('sm1', 'pfx'),
                          ('t^p', 'pfx'),
                          ('v^say', 'v'),
                          ('m^in', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_empty_string(self):
        """Test iter_morphemes with an empty string."""
        morph_word = ''
        actual_output = list(self.reader.iter_gloss_pos(morph_word))
        desired_output = [('', '')]
        self.assertEqual(actual_output, desired_output)

    def test_get_segments_standard_case(self):
        """Test get_segments with hyphen separated segment word."""
        seg_word = 'prefix-stem-affix'
        actual_output = SesothoReader.get_segments(seg_word)
        desired_output = ['prefix', 'stem', 'affix']
        self.assertEqual(actual_output, desired_output)

    def test_get_segments_empty_string(self):
        """Test get_segments with an empty string."""
        seg_word = ''
        actual_output = SesothoReader.get_segments(seg_word)
        desired_output = ['']
        self.assertEqual(actual_output, desired_output)

    def test_get_glosses_standard_case(self):
        """Test get_glosses with  hyphen separated gloss word."""
        seg_word = 'sm1-t^p-v^say-m^in'
        actual_output = self.reader.get_glosses(seg_word)
        desired_output = ['sm1', 't^p', 'v^say', 'm^in']
        self.assertEqual(actual_output, desired_output)

    def test_get_glosses_empty_string(self):
        """Test get_glosses with an empty string."""
        seg_word = ''
        actual_output = self.reader.get_segments(seg_word)
        desired_output = ['']
        self.assertEqual(actual_output, desired_output)

    def test_get_poses_standard_case(self):
        """Test get_poses with a hyphen separated pos word."""
        seg_word = 'sm1-t^p-v^say-m^in'
        actual_output = self.reader.get_poses(seg_word)
        desired_output = ['pfx', 'pfx', 'v', 'sfx']
        self.assertEqual(actual_output, desired_output)

    def test_get_poses_empty_string(self):
        """Test get_poses with an empty string."""
        seg_word = ''
        actual_output = self.reader.get_poses(seg_word)
        desired_output = ['']
        self.assertEqual(actual_output, desired_output)