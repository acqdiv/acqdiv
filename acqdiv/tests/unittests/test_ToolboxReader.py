import unittest
from acqdiv.parsers.toolbox.readers.ToolboxReader import *


class TestToolboxReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # if needed set up a file 'Toolbox.txt' later
        file_path = 'test_files/Chintang.txt'
        cls.reader = ToolboxReader(file_path)

    def test_make_rec(self):
        record = ('\\ref session_name.001\n'
                  '\\ELANBegin 00:50:11.150\n'
                  '\\ELANEnd 00:50:22.350\n'
                  '\\ELANParticipant MAR\n'
                  '\\gw  w1        w2\n'
                  '\\mph w1pfxseg-   w1stemseg   -w1sfxseg  w2stemseg\n'
                  '\\mgl w1pfxgloss- w1stemgloss -w1sfxgloss w2stemgloss\n'
                  '\\lg C-           C           -C        N\n'
                  '\\id w1pfxID-     w1stemID    -w1sfxID    w2stemID\n'
                  '\\ps w1pfxpos-    w1stempos   -w1sfxpos   w2stempos\n'
                  '\\eng This is the translation.\n'
                  '\\tos child directed\n'
                  '\\nep ?')
        actual_output = ToolboxReader.make_rec(record)
        utterance = {
            'speaker_label': 'MAR',
            'addressee': None,
            'utterance_raw': None,
            'utterance': None,
            'sentence_type': None,
            'childdirected': None,
            'source_id': 'session_name.001',
            'start_raw': '00:50:11.150',
            'end_raw': '00:50:22.350',
            'translation': 'This is the translation.',
            'comment': None,
            'warning': None,
            'morpheme': None,
            'gloss_raw': None,
            'pos_raw': 'w1pfxpos- w1stempos -w1sfxpos w2stempos'
        }
        words = []
        morphemes = []
        desired_output = (utterance, words, morphemes)
        self.assertEqual(actual_output, desired_output)

    def test_get_record_dict(self):
        record = ('\\ref session_name.001\n'
                  '\\ELANBegin 00:50:11.150\n'
                  '\\ELANEnd 00:50:22.350\n'
                  '\\ELANParticipant MAR\n'
                  '\\nep ?')
        actual_output = ToolboxReader.get_record_dict(record)
        desired_output = {
            'ref': 'session_name.001',
            'ELANBegin': '00:50:11.150',
            'ELANEnd': '00:50:22.350',
            'ELANParticipant': 'MAR',
            'nep': '?'
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_tiers(self):
        record = ('\\ref session_name.001\n'
                  '\\ELANBegin 00:50:11.150\n'
                  '\\ELANEnd 00:50:22.350\n'
                  '\\ELANParticipant MAR\n'
                  '\\nep ?')
        actual_output = ToolboxReader.get_tiers(record)
        desired_output = [
            '\\ref session_name.001',
            '\\ELANBegin 00:50:11.150',
            '\\ELANEnd 00:50:22.350',
            '\\ELANParticipant MAR',
            '\\nep ?'
        ]
        self.assertEqual(actual_output, desired_output)

    def test_get_tier(self):
        tier = '\\ref session_name.001'
        actual_output = ToolboxReader.get_tier(tier)
        desired_output = ('ref', 'session_name.001')
        self.assertEqual(actual_output, desired_output)

    def test_remove_redundant_whitespaces(self):
        string = '  no such     thing       '
        actual_output = ToolboxReader.remove_redundant_whitespaces(string)
        desired_output = 'no such thing'
        self.assertEqual(actual_output, desired_output)

    def test_is_record_true(self):
        rec_dict = {
            'ref': 'session_name.001',
            'ELANBegin': '00:50:11.150',
            'ELANEnd': '00:50:22.350',
            'ELANParticipant': 'MAR',
            'nep': '?'
        }
        self.assertTrue(ToolboxReader.is_record(rec_dict))

    def test_is_record_false(self):
        rec_dict = {
            '@participant': 'PA1 name2 PA2 name2',
        }
        self.assertFalse(ToolboxReader.is_record(rec_dict))

    # ---------- utterance data ----------

    def test_get_utterance_data(self):
        rec_dict = {
            'ref': 'session_name.001',
            'ELANBegin': '00:50:11.150',
            'ELANEnd': '00:50:22.350',
            'ELANParticipant': 'MAR',
            'tx': 'w1 w2 .',
            'mb': 'w1pfxseg-   w1stemseg   -w1sfxseg      w2stemseg',
            'ge': 'w1pfxgloss- w1stemgloss -w1sfxgloss    w2stemgloss',
            'ps': 'w1pfxpos-   w1stempos   -w1sfxpos      w2stempos',
            'lg': 'language-    language   -language      language',
            'eng': 'This is the translation',
            'tos': 'child directed',
            'nep': '?'
        }
        actual_output = ToolboxReader.get_utterance_data(rec_dict)
        desired_output = {
            'speaker_label': 'MAR',
            'addressee': '',
            'utterance_raw': 'w1 w2 .',
            'utterance': 'w1 w2',
            'sentence_type': 'default',
            'childdirected': None,
            'source_id': 'session_name.001',
            'start_raw': '00:50:11.150',
            'end_raw': '00:50:22.350',
            'translation': 'This is the translation',
            'comment': '',
            'warning': '',
            'morpheme': 'w1pfxseg-   w1stemseg   -w1sfxseg      w2stemseg',
            'gloss_raw': 'w1pfxgloss- w1stemgloss -w1sfxgloss    w2stemgloss',
            'pos_raw': 'w1pfxpos-   w1stempos   -w1sfxpos      w2stempos'
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_data_empty_dict(self):
        rec_dict = {}
        actual_output = ToolboxReader.get_utterance_data(rec_dict)
        desired_output = {
            'speaker_label': '',
            'addressee': '',
            'utterance_raw': '',
            'utterance': '',
            'sentence_type': '',
            'childdirected': None,
            'source_id': '',
            'start_raw': '',
            'end_raw': '',
            'translation': '',
            'comment': '',
            'warning': '',
            'morpheme': '',
            'gloss_raw': '',
            'pos_raw': ''
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_source_id(self):
        rec_dict = {'ref': 'session_name.001'}
        actual_output = ToolboxReader.get_source_id(rec_dict)
        desired_output = 'session_name.001'
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_label(self):
        rec_dict = {'ELANParticipant': 'MAR'}
        actual_output = ToolboxReader.get_speaker_label(rec_dict)
        desired_output = 'MAR'
        self.assertEqual(actual_output, desired_output)

    def test_get_addressee(self):
        rec_dict = {'add': 'MAR'}
        actual_output = ToolboxReader.get_addressee(rec_dict)
        desired_output = 'MAR'
        self.assertEqual(actual_output, desired_output)

    def test_get_start_raw(self):
        rec_dict = {'ELANBegin': '00:11:22'}
        actual_output = ToolboxReader.get_start_raw(rec_dict)
        desired_output = '00:11:22'
        self.assertEqual(actual_output, desired_output)

    def test_get_end_raw(self):
        rec_dict = {'ELANEnd': '00:11:22'}
        actual_output = ToolboxReader.get_end_raw(rec_dict)
        desired_output = '00:11:22'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_raw(self):
        rec_dict = {'tx': 'an utterance'}
        actual_output = ToolboxReader.get_utterance_raw(rec_dict)
        desired_output = 'an utterance'
        self.assertEqual(actual_output, desired_output)

    def test_get_sentence_type(self):
        rec_dict = {'tx': 'an utterance .'}
        actual_output = ToolboxReader.get_sentence_type(rec_dict)
        desired_output = 'default'
        self.assertEqual(actual_output, desired_output)

    def test_get_childdirected(self):
        rec_dict = {}
        actual_output = ToolboxReader.get_childdirected(rec_dict)
        desired_output = None
        self.assertEqual(actual_output, desired_output)

    def test_get_translation(self):
        rec_dict = {'eng': 'the translation'}
        actual_output = ToolboxReader.get_translation(rec_dict)
        desired_output = 'the translation'
        self.assertEqual(actual_output, desired_output)

    def test_get_comment(self):
        rec_dict = {'comment': 'a comment'}
        actual_output = ToolboxReader.get_comment(rec_dict)
        desired_output = 'a comment'
        self.assertEqual(actual_output, desired_output)

    def test_get_warning(self):
        """TODO: Figure out desired behaviour."""
        pass

    def test_add_utterance_warnings(self):
        """Not implemented for general ToolboxReader"""
        pass

    # ---------- words data ----------

    def test_get_words_data(self):
        rec_dict = {
            'tx': 'This is a test'
        }
        actual_output = ToolboxReader.get_words_data(rec_dict)
        desired_output = [
            {'word': 'This', 'word_actual': 'This'},
            {'word': 'is', 'word_actual': 'is'},
            {'word': 'a', 'word_actual': 'a'},
            {'word': 'test', 'word_actual': 'test'},
        ]
        self.assertEqual(actual_output, desired_output)

    def test_get_words(self):
        utterance = 'A test utterance'
        actual_output = ToolboxReader.get_words(utterance)
        desired_output = ['A', 'test', 'utterance']
        self.assertEqual(actual_output, desired_output)

    # ---------- morphemes data ----------

    def test_get_morphemes_data_single_morpheme_word(self):
        rec_dict = {
            'mb': 'w1pfxseg',
            'ge': 'w1pfxgloss',
            'ps': 'w1pfxpos',
            'lg': 'language'
        }
        actual_output = ToolboxReader.get_morphemes_data(rec_dict)
        desired_output = [
            [
                {'morpheme': 'w1pfxseg',
                 'gloss_raw': 'w1pfxgloss',
                 'pos_raw': 'w1pfxpos',
                 'morpheme_language': 'language',
                 'type': 'target',
                 'warning': None
                 }
            ]
        ]
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes_data_multiple_morpheme_words(self):
        rec_dict = {
            'mb': 'w1pfxseg-   w1stemseg   -w1sfxseg      w2stemseg',
            'ge': 'w1pfxgloss- w1stemgloss -w1sfxgloss    w2stemgloss',
            'ps': 'w1pfxpos-   w1stempos   -w1sfxpos      w2stempos',
            'lg': 'language-    language   -language      language'
        }
        actual_output = ToolboxReader.get_morphemes_data(rec_dict)
        desired_output = [
            [
                {'morpheme': 'w1pfxseg-',
                 'gloss_raw': 'w1pfxgloss-',
                 'pos_raw': 'w1pfxpos-',
                 'morpheme_language': 'language-',
                 'type': 'target',
                 'warning': None
                 },
                {'morpheme': 'w1stemseg',
                 'gloss_raw': 'w1stemgloss',
                 'pos_raw': 'w1stempos',
                 'morpheme_language': 'language',
                 'type': 'target',
                 'warning': None},
                {'morpheme': '-w1sfxseg',
                 'gloss_raw': '-w1sfxgloss',
                 'pos_raw': '-w1sfxpos',
                 'morpheme_language': '-language',
                 'type': 'target',
                 'warning': None}
            ],
            [
                {'morpheme': 'w2stemseg',
                 'gloss_raw': 'w2stemgloss',
                 'pos_raw': 'w2stempos',
                 'morpheme_language': 'language',
                 'type': 'target',
                 'warning': None}
            ]
        ]
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes_data_empty_dict(self):
        rec_dict = {}
        actual_output = ToolboxReader.get_morphemes_data(rec_dict)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_morphology_data_single_morpheme_word(self):
        rec_dict = {
            'mb': 'w1pfxseg-   w1stemseg   -w1sfxseg',
            'ge': 'w1pfxgloss- w1stemgloss -w1sfxgloss',
            'ps': 'w1pfxpos-   w1stempos   -w1sfxpos',
            'lg': 'language-    language   -language'
        }
        actual_output = ToolboxReader.get_morphology_data(rec_dict)
        segments = [['w1pfxseg-', 'w1stemseg', '-w1sfxseg']]
        glosses = [['w1pfxgloss-', 'w1stemgloss', '-w1sfxgloss']]
        poses = [['w1pfxpos-', 'w1stempos', '-w1sfxpos']]
        langs = [['language-', 'language', '-language']]
        desired_output = (segments, glosses, poses, langs)
        self.assertEqual(actual_output, desired_output)

    def test_get_morphology_data_multiple_morpheme_words(self):
        rec_dict = {
            'mb': 'w1pfxseg-   w1stemseg   -w1sfxseg      w2stemseg',
            'ge': 'w1pfxgloss- w1stemgloss -w1sfxgloss    w2stemgloss',
            'ps': 'w1pfxpos-   w1stempos   -w1sfxpos      w2stempos',
            'lg': 'language-    language   -language      language'
        }
        actual_output = ToolboxReader.get_morphology_data(rec_dict)
        segments = [['w1pfxseg-', 'w1stemseg', '-w1sfxseg'], ['w2stemseg']]
        glosses = [['w1pfxgloss-', 'w1stemgloss', '-w1sfxgloss'],
                   ['w2stemgloss']]
        poses = [['w1pfxpos-', 'w1stempos', '-w1sfxpos'], ['w2stempos']]
        langs = [['language-', 'language', '-language'], ['language']]
        desired_output = (segments, glosses, poses, langs)
        self.assertEqual(actual_output, desired_output)

    def test_get_morphology_data_empty_dict(self):
        rec_dict = {}
        actual_output = ToolboxReader.get_morphology_data(rec_dict)
        desired_output = ([], [], [], [])
        self.assertEqual(actual_output, desired_output)

    # ---------- morpheme tier ----------

    def test_get_seg_tier(self):
        rec_dict = {
            'mb': 'w1pfxseg-   w1stemseg   -w1sfxseg      w2stemseg'
        }
        actual_output = ToolboxReader.get_seg_tier(rec_dict)
        desired_output = 'w1pfxseg-   w1stemseg   -w1sfxseg      w2stemseg'
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier(self):
        rec_dict = {
            'ge': 'w1pfxgloss- w1stemgloss -w1sfxgloss    w2stemgloss'
        }
        actual_output = ToolboxReader.get_gloss_tier(rec_dict)
        desired_output = 'w1pfxgloss- w1stemgloss -w1sfxgloss    w2stemgloss'
        self.assertEqual(actual_output, desired_output)

    def test_pos_tier(self):
        rec_dict = {
            'ps': 'w1pfxpos-   w1stempos   -w1sfxpos      w2stempos'
        }
        actual_output = ToolboxReader.get_pos_tier(rec_dict)
        desired_output = 'w1pfxpos-   w1stempos   -w1sfxpos      w2stempos'
        self.assertEqual(actual_output, desired_output)

    def test_get_lang_tier(self):
        rec_dict = {
            'lg': 'language    language     language      language'
        }
        actual_output = ToolboxReader.get_lang_tier(rec_dict)
        desired_output = 'language    language     language      language'
        self.assertEqual(actual_output, desired_output)

    # ---------- morpheme words ----------

    def test_get_morpheme_words(self):
        morpheme_tier = 'w1pfxseg-   w1stemseg   -w1sfxseg    w2stemseg'
        actual_output = ToolboxReader.get_morpheme_words(morpheme_tier)
        desired_output = ['w1pfxseg-   w1stemseg   -w1sfxseg', 'w2stemseg']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_empty_string(self):
        morpheme_tier = ''
        actual_output = ToolboxReader.get_morpheme_words(morpheme_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_words(self):
        morpheme_tier = 'w1pfxseg-   w1stemseg   -w1sfxseg      w2stemseg'
        actual_output = ToolboxReader.get_seg_words(morpheme_tier)
        desired_output = ['w1pfxseg-   w1stemseg   -w1sfxseg', 'w2stemseg']
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_words_empty_string(self):
        morpheme_tier = ''
        actual_output = ToolboxReader.get_seg_words(morpheme_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_words(self):
        morpheme_tier = 'w1pfxgloss- w1stemgloss -w1sfxgloss    w2stemgloss'
        actual_output = ToolboxReader.get_seg_words(morpheme_tier)
        desired_output = ['w1pfxgloss- w1stemgloss -w1sfxgloss', 'w2stemgloss']
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_words_empty_string(self):
        morpheme_tier = ''
        actual_output = ToolboxReader.get_seg_words(morpheme_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_words(self):
        morpheme_tier = 'w1pfxpos-   w1stempos   -w1sfxpos      w2stempos'
        actual_output = ToolboxReader.get_seg_words(morpheme_tier)
        desired_output = ['w1pfxpos-   w1stempos   -w1sfxpos', 'w2stempos']
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_words_empty_string(self):
        morpheme_tier = ''
        actual_output = ToolboxReader.get_seg_words(morpheme_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_lang_words(self):
        morpheme_tier = 'language-    language   -language      language'
        actual_output = ToolboxReader.get_seg_words(morpheme_tier)
        desired_output = ['language-    language   -language', 'language']
        self.assertEqual(actual_output, desired_output)

    def test_get_lang_words_empty_string(self):
        morpheme_tier = ''
        actual_output = ToolboxReader.get_seg_words(morpheme_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    # ---------- morphemes ----------

    def test_get_morphemes(self):
        morpheme_word = 'w1pfxseg-   w1stemseg   -w1sfxseg'
        actual_output = ToolboxReader.get_morphemes(morpheme_word)
        desired_output = ['w1pfxseg-', 'w1stemseg', '-w1sfxseg']
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes_empty_string(self):
        morpheme_word = ''
        actual_output = ToolboxReader.get_morphemes(morpheme_word)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_segs(self):
        segment_word = 'w1pfxseg-   w1stemseg   -w1sfxseg'
        actual_output = ToolboxReader.get_segs(segment_word)
        desired_output = ['w1pfxseg-', 'w1stemseg', '-w1sfxseg']
        self.assertEqual(actual_output, desired_output)

    def test_get_glosses(self):
        gloss_word = 'w1pfxgloss- w1stemgloss -w1sfxgloss'
        actual_output = ToolboxReader.get_glosses(gloss_word)
        desired_output = ['w1pfxgloss-', 'w1stemgloss', '-w1sfxgloss']
        self.assertEqual(actual_output, desired_output)

    def test_get_poses(self):
        pos_word = 'w1pfxpos-   w1stempos   -w1sfxpos'
        actual_output = ToolboxReader.get_poses(pos_word)
        desired_output = ['w1pfxpos-', 'w1stempos', '-w1sfxpos']
        self.assertEqual(actual_output, desired_output)

    def test_get_langs(self):
        morpheme_lang_word = 'language-    language   -language'
        actual_output = ToolboxReader.get_langs(morpheme_lang_word)
        desired_output = ['language-', 'language', '-language']
        self.assertEqual(actual_output, desired_output)

    def test_get_list_of_list_morphemes_seg_tier(self):
        rec_dict = {
            'mb': 'w1pfxseg-   w1stemseg   -w1sfxseg      w2stemseg',
            'ge': 'w1pfxgloss- w1stemgloss -w1sfxgloss    w2stemgloss',
            'ps': 'w1pfxpos-   w1stempos   -w1sfxpos      w2stempos',
            'lg': 'language-    language   -language      language'
        }
        actual_output = ToolboxReader.get_list_of_list_morphemes(
            rec_dict,
            ToolboxReader.get_seg_tier,
            ToolboxReader.get_seg_words,
            ToolboxReader.get_segs,
            ToolboxReader.clean_seg_tier,
            ToolboxReader.clean_seg_word,
            ToolboxReader.clean_seg
        )
        desired_output = [
            ['w1pfxseg-', 'w1stemseg', '-w1sfxseg'],
            ['w2stemseg']
        ]
        self.assertEqual(actual_output, desired_output)

    def test_get_list_of_list_morphemes_empty_dict(self):
        rec_dict = {}
        actual_output = ToolboxReader.get_list_of_list_morphemes(
            rec_dict,
            ToolboxReader.get_seg_tier,
            ToolboxReader.get_seg_words,
            ToolboxReader.get_segs,
            ToolboxReader.clean_seg_tier,
            ToolboxReader.clean_seg_word,
            ToolboxReader.clean_seg
        )
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_fix_mm_misalignments_no_missalignment(self):
        segments = [['w1pfxseg-', 'w1stemseg', '-w1sfxseg'], ['w2stemseg']]
        glosses = [['w1pfxgloss-', 'w1stemgloss', '-w1sfxgloss'],
                   ['w2stemgloss']]
        poses = [['w1pfxpos-', 'w1stempos', '-w1sfxpos'], ['w2stempos']]
        langs = [['language-', 'language', '-language'], ['language']]
        morphology_data = (segments, glosses, poses, langs)
        actual_output = ToolboxReader.fix_mm_misalignments(morphology_data)
        desired_output = morphology_data
        self.assertEqual(actual_output, desired_output)

    def test_fix_mm_misalignments_segments_missaligned(self):
        segments = [['w1pfxseg-', '-w1sfxseg'], ['w2stemseg']]
        glosses = [['w1pfxgloss-', 'w1stemgloss', '-w1sfxgloss'],
                   ['w2stemgloss']]
        poses = [['w1pfxpos-', 'w1stempos', '-w1sfxpos'], ['w2stempos']]
        langs = [['language-', 'language', '-language'], ['language']]
        morphology_data = (segments, glosses, poses, langs)
        actual_output = ToolboxReader.fix_mm_misalignments(morphology_data)
        desired_output = ([[], []], glosses, poses, langs)
        self.assertEqual(actual_output, desired_output)

    def test_fix_mm_misalignments_segment_words_missaligned(self):
        segments = [['w1pfxseg-', 'w1stemseg', '-w1sfxseg']]
        glosses = [['w1pfxgloss-', 'w1stemgloss', '-w1sfxgloss'],
                   ['w2stemgloss']]
        poses = [['w1pfxpos-', 'w1stempos', '-w1sfxpos'], ['w2stempos']]
        langs = [['language-', 'language', '-language'], ['language']]
        morphology_data = (segments, glosses, poses, langs)
        actual_output = ToolboxReader.fix_mm_misalignments(morphology_data)
        desired_output = ([[], []], glosses, poses, langs)
        self.assertEqual(actual_output, desired_output)

    def test_fix_mm_misalignments_empty_list_input(self):
        morphology_data = ([], [], [], [], [])
        actual_output = ToolboxReader.fix_mm_misalignments(morphology_data)
        desired_output = ([], [], [], [], [])
        self.assertEqual(actual_output, desired_output)

    def test_struct_eqv_no_nesting_struct_is_equal(self):
        xs = [2]
        ys = [5]
        actual_output = ToolboxReader.struct_eqv(xs, ys)
        desired_output = True
        self.assertEqual(actual_output, desired_output)

    def test_struct_eqv_no_nesting_struct_is_different(self):
        xs = [2]
        ys = []
        actual_output = ToolboxReader.struct_eqv(xs, ys)
        desired_output = False
        self.assertEqual(actual_output, desired_output)

    def test_struct_eqv_nesting_struct_is_equal(self):
        xs = [[3, 4], [2]]
        ys = [[1, 7], [6]]
        actual_output = ToolboxReader.struct_eqv(xs, ys)
        desired_output = True
        self.assertEqual(actual_output, desired_output)

    def test_struct_eqv_nesting_struct_is_different(self):
        xs = [[3, 4], []]
        ys = [[1, 7], [6]]
        actual_output = ToolboxReader.struct_eqv(xs, ys)
        desired_output = False
        self.assertEqual(actual_output, desired_output)

    def test_struct_eqv_multiple_nesting_struct_is_equal(self):
        xs = [[3, [[4]]], [1, []]]
        ys = [[1, [[7]]], [2, []]]
        actual_output = ToolboxReader.struct_eqv(xs, ys)
        desired_output = True
        self.assertEqual(actual_output, desired_output)

    def test_struct_eqv_multiple_nesting_struct_is_different(self):
        xs = [[3, [[4, 3]]], [1, []]]
        ys = [[1, [[7]]], [2, [], []]]
        actual_output = ToolboxReader.struct_eqv(xs, ys)
        desired_output = False
        self.assertEqual(actual_output, desired_output)

    def test_struct_eqv_empty_lists(self):
        xs = []
        ys = []
        actual_output = ToolboxReader.struct_eqv(xs, ys)
        desired_output = True
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_dict_no_warning(self):
        morpheme = ('segment', 'gloss', 'pos', 'language')
        actual_output = ToolboxReader.get_morpheme_dict(morpheme)
        desired_output = {
            'morpheme': 'segment',
            'gloss_raw': 'gloss',
            'pos_raw': 'pos',
            'morpheme_language': 'language',
            'type': 'target',
            'warning': None
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_dict_with_warning(self):
        morpheme = ('segment', 'gloss', 'pos', 'language')
        ToolboxReader.warnings = ['warning 1', 'warning 2']
        actual_output = ToolboxReader.get_morpheme_dict(morpheme)
        desired_output = {
            'morpheme': 'segment',
            'gloss_raw': 'gloss',
            'pos_raw': 'pos',
            'morpheme_language': 'language',
            'type': 'target',
            'warning': 'warning 1 warning 2'
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_dict_with_warnings(self):
        morpheme = ('segment', 'gloss', 'pos', 'language')
        ToolboxReader.warnings = ['warning 1', 'warning 2']
        actual_output = ToolboxReader.get_morpheme_dict(morpheme)
        desired_output = {
            'morpheme': 'segment',
            'gloss_raw': 'gloss',
            'pos_raw': 'pos',
            'morpheme_language': 'language',
            'type': 'target',
            'warning': 'warning 1 warning 2'
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_dict_with_empty_fields(self):
        morpheme = (None, 'gloss', None, 'language')
        actual_output = ToolboxReader.get_morpheme_dict(morpheme)
        desired_output = {
            'morpheme': None,
            'gloss_raw': 'gloss',
            'pos_raw': None,
            'morpheme_language': 'language',
            'type': 'target',
            'warning': None
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_type(self):
        actual_output = ToolboxReader.get_morpheme_type()
        desired_output = 'target'
        self.assertEqual(actual_output, desired_output)

    # ---------- miscellaneous ----------

    def test_add_word_language_same_length(self):
        """TODO: add_word_language needs documentation"""
        words = [{'word': 'word1'}, {'word': 'word2'}, {'word': 'word3'}]
        morphemes = [
            [{'morpheme_language': 'a_lang'}],
            [{'morpheme_language': 'a_lang'}],
            [{'morpheme_language': 'a_lang'}]
        ]
        ToolboxReader.add_word_language(words, morphemes)
        desired = [
            {'word': 'word1', 'word_language': 'a_lang'},
            {'word': 'word2', 'word_language': 'a_lang'},
            {'word': 'word3', 'word_language': 'a_lang'}
        ]
        self.assertEqual(words, desired)

    def test_fix_wm_misalignments_not_misaligned(self):
        words = [{}, {}]
        morphemes = [{}, {}]
        ToolboxReader.fix_wm_misalignments(words, morphemes)
        desired = [{}, {}]
        self.assertEqual(words, desired)

    def test_fix_wm_misalignments_misaligned(self):
        words = [{}, {}]
        morphemes = [{}, {}, {}]
        ToolboxReader.fix_wm_misalignments(words, morphemes)
        desired = [{}, {}, {}]
        self.assertEqual(words, desired)

    def test_fix_wm_misalignments_misaligned_no_words(self):
        words = []
        morphemes = [{}]
        ToolboxReader.fix_wm_misalignments(words, morphemes)
        desired = [{}]
        self.assertEqual(words, desired)

    def test_fix_wm_misalignments_no_words_no_morphemes(self):
        words = []
        morphemes = []
        ToolboxReader.fix_wm_misalignments(words, morphemes)
        desired = []
        self.assertEqual(words, desired)

    def test_null_empty_values_multiple_empty_values(self):
        dictionary = {1: '', 2: 'hey', 3: ''}
        ToolboxReader.null_empty_values(dictionary)
        desired = {1: None, 2: 'hey', 3: None}
        self.assertEqual(dictionary, desired)

    def test_null_empty_values_empty_dict(self):
        dictionary = {}
        ToolboxReader.null_empty_values(dictionary)
        desired = {}
        self.assertEqual(dictionary, desired)

    # ---------- cleaners ----------

    # ---------- utterance ----------

    def test_unify_unknown_xxx(self):
        utterance = 'xxx are xxx'
        actual_output = ToolboxReader.unify_unknown(utterance)
        desired_output = '??? are ???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_www(self):
        utterance = 'here www examples'
        actual_output = ToolboxReader.unify_unknown(utterance)
        desired_output = 'here ??? examples'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_stars(self):
        utterance = 'here *** examples'
        actual_output = ToolboxReader.unify_unknown(utterance)
        desired_output = 'here ??? examples'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_xxx_stars_www(self):
        utterance = 'xxx *** www, ***'
        actual_output = ToolboxReader.unify_unknown(utterance)
        desired_output = '??? ??? ???, ???'
        self.assertEqual(actual_output, desired_output)

    def test_unify_unknown_empty_string(self):
        utterance = ''
        actual_output = ToolboxReader.unify_unknown(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_stars_xxx(self):
        utterance = 'These *** some good xxx .'
        actual_output = ToolboxReader.clean_utterance(utterance)
        desired_output = 'These ??? some good ??? .'
        self.assertEqual(actual_output, desired_output)

    def test_clean_utterance_empty_string(self):
        utterance = ''
        actual_output = ToolboxReader.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- utterance word ----------

    def test_clean_word_xxx(self):
        utterance = 'xxx-less'
        actual_output = ToolboxReader.clean_utterance(utterance)
        desired_output = '???-less'
        self.assertEqual(actual_output, desired_output)

    def test_clean_word_empty_string(self):
        utterance = ''
        actual_output = ToolboxReader.clean_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- morphology tiers ----------

    def test_clean_morph_tier(self):
        morph_tier = 'the morph tier'
        actual_output = ToolboxReader.clean_morph_tier(morph_tier)
        desired_output = 'the morph tier'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_tier(self):
        seg_tier = 'the seg tier'
        actual_output = ToolboxReader.clean_seg_tier(seg_tier)
        desired_output = 'the seg tier'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_tier(self):
        gloss_tier = 'the gloss tier'
        actual_output = ToolboxReader.clean_gloss_tier(gloss_tier)
        desired_output = 'the gloss tier'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_tier(self):
        pos_tier = 'the pos tier'
        actual_output = ToolboxReader.clean_pos_tier(pos_tier)
        desired_output = 'the pos tier'
        self.assertEqual(actual_output, desired_output)

    def test_clean_lang_tier(self):
        lang_tier = 'the lang tier'
        actual_output = ToolboxReader.clean_lang_tier(lang_tier)
        desired_output = 'the lang tier'
        self.assertEqual(actual_output, desired_output)

    # ---------- morpheme words ----------

    def test_clean_morpheme_word(self):
        morpheme_word = 'mor-word'
        actual_output = ToolboxReader.clean_morpheme_word(morpheme_word)
        desired_output = 'mor-word'
        self.assertEqual(actual_output, desired_output)

    def test_clean_seg_word(self):
        seg_word = 'seg-word'
        actual_output = ToolboxReader.clean_seg_word(seg_word)
        desired_output = 'seg-word'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss_word(self):
        gloss_word = 'gloss-word'
        actual_output = ToolboxReader.clean_gloss_word(gloss_word)
        desired_output = 'gloss-word'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos_word(self):
        pos_word = 'pos-word'
        actual_output = ToolboxReader.clean_pos_word(pos_word)
        desired_output = 'pos-word'
        self.assertEqual(actual_output, desired_output)

    def test_clean_lang_word(self):
        lang_word = 'lang-word'
        actual_output = ToolboxReader.clean_lang_word(lang_word)
        desired_output = 'lang-word'
        self.assertEqual(actual_output, desired_output)

    # ---------- morphemes ----------

    def test_clean_morpheme(self):
        morpheme = 'morpheme'
        actual_output = ToolboxReader.clean_morpheme(morpheme)
        desired_output = 'morpheme'
        self.assertEqual(actual_output, desired_output)
    
    def test_clean_seg(self):
        seg = 'seg'
        actual_output = ToolboxReader.clean_seg(seg)
        desired_output = 'seg'
        self.assertEqual(actual_output, desired_output)

    def test_clean_gloss(self):
        gloss = 'gloss'
        actual_output = ToolboxReader.clean_gloss(gloss)
        desired_output = 'gloss'
        self.assertEqual(actual_output, desired_output)

    def test_clean_pos(self):
        pos = 'pos'
        actual_output = ToolboxReader.clean_pos(pos)
        desired_output = 'pos'
        self.assertEqual(actual_output, desired_output)

    def test_clean_lang(self):
        lang = 'lang'
        actual_output = ToolboxReader.clean_lang(lang)
        desired_output = 'lang'
        self.assertEqual(actual_output, desired_output)

    def test___repr__(self):
        """Test for correct represenation of class.

        If needed create a file 'Toolbox.txt' and use this file
        instead of 'Chintang.txt'.
        """
        reader = ToolboxReader('./Chintang.txt')
        actual_output = reader.__repr__()
        desired_output = "ToolboxReader('./Chintang.txt')"
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
