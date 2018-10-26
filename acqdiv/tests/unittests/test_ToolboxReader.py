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
        pass

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
            'tx': 'This is a test .'
        }
        actual_output = ToolboxReader.get_words_data(rec_dict)
        desired_output = [
            {'word': 'This', 'word_actual': 'This'},
            {'word': 'is', 'word_actual': 'is'},
            {'word': 'a', 'word_actual': 'a'},
            {'word': 'test', 'word_actual': 'test'},
        ]
        self.assertEqual(actual_output, desired_output)



if __name__ == '__main__':
    unittest.main()