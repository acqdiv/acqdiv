import unittest
from acqdiv.parsers.toolbox.readers.ToolboxReader import *


class TestToolboxReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.reader = ToolboxReader()

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
            'tx': '@Participants: CHI Tim child, MOT Lisa mother',
        }
        self.assertFalse(ToolboxReader.is_record(rec_dict))

    # ---------- utterance data ----------

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

    def test_get_actual_utterance(self):
        rec_dict = {'tx': 'an utterance'}
        actual_output = ToolboxReader.get_actual_utterance(rec_dict)
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
        desired_output = ''
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

    # ---------- words data ----------

    def test_get_words(self):
        utterance = 'A test utterance'
        actual_output = ToolboxReader.get_words(utterance)
        desired_output = ['A', 'test', 'utterance']
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

    def test_get_morpheme_words_clitics(self):
        morpheme_tier = 'w1pfxseg=   w1stemseg   =w1sfxseg    w2stemseg'
        actual_output = ToolboxReader.get_morpheme_words(morpheme_tier)
        desired_output = ['w1pfxseg=   w1stemseg   =w1sfxseg', 'w2stemseg']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_clitics_and_affixes(self):
        morpheme_tier = 'w1pfxseg=   w1stemseg   -w1sfxseg    w2stemseg'
        actual_output = ToolboxReader.get_morpheme_words(morpheme_tier)
        desired_output = ['w1pfxseg=   w1stemseg   -w1sfxseg', 'w2stemseg']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_very_complex(self):
        morpheme_tier = 'abc=   de- fgh   -ijk -lmno =pkr =st    uv -w  xyz'
        actual_output = ToolboxReader.get_morpheme_words(morpheme_tier)
        desired_output = ['abc=   de- fgh   -ijk -lmno =pkr =st',
                          'uv -w',
                          'xyz']
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

    def test_get_morpheme_type(self):
        actual_output = ToolboxReader.get_morpheme_type()
        desired_output = 'target'
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
