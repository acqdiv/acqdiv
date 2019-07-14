import unittest

from acqdiv.parsers.corpora.main.chintang.ChintangReader import ChintangReader


class TestChintangReader(unittest.TestCase):

    def test_get_utterance_raw_key_exists(self):
        rec_dict = {
            'gw': 'the raw utterance .'
        }
        actual_output = ChintangReader.get_actual_utterance(rec_dict)
        desired_output = 'the raw utterance .'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_raw_key_does_not_exists(self):
        rec_dict = {
            'a': 'the raw utterance .'
        }
        actual_output = ChintangReader.get_actual_utterance(rec_dict)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_tier_key_exists(self):
        rec_dict = {
            'mph': 'the seg tier .'
        }
        actual_output = ChintangReader.get_seg_tier(rec_dict)
        desired_output = 'the seg tier .'
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_tier_key_does_not_exist(self):
        rec_dict = {
            'mp': 'the seg tier .'
        }
        actual_output = ChintangReader.get_seg_tier(rec_dict)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier_key_exists(self):
        rec_dict = {
            'mgl': 'the gloss tier .'
        }
        actual_output = ChintangReader.get_gloss_tier(rec_dict)
        desired_output = 'the gloss tier .'
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier_key_does_not_exist(self):
        rec_dict = {
            'm': 'the gloss tier .'
        }
        actual_output = ChintangReader.get_gloss_tier(rec_dict)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier_key_exists(self):
        rec_dict = {
            'ps': 'the pos tier .'
        }
        actual_output = ChintangReader.get_pos_tier(rec_dict)
        desired_output = 'the pos tier .'
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier_key_does_not_exist(self):
        rec_dict = {
            's': 'the pos tier .'
        }
        actual_output = ChintangReader.get_pos_tier(rec_dict)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_lang_tier_key_exists(self):
        rec_dict = {
            'lg': 'the lang tier .'
        }
        actual_output = ChintangReader.get_lang_tier(rec_dict)
        desired_output = 'the lang tier .'
        self.assertEqual(actual_output, desired_output)

    def test_get_lang_tier_key_does_not_exist(self):
        rec_dict = {
            'l': 'the lang tier .'
        }
        actual_output = ChintangReader.get_lang_tier(rec_dict)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_childdirected_tos_childdirected(self):
        rec_dict = {
            'tos': 'this is directed to a child'
        }
        output = ChintangReader.get_childdirected(rec_dict)
        self.assertTrue(output)

    def test_get_childdirected_tos_not_childdirected(self):
        rec_dict = {
            'tos': 'this is directed to an adult'
        }
        output = ChintangReader.get_childdirected(rec_dict)
        self.assertFalse(output)

    def test_get_childdirected_TOS_childdirected(self):
        rec_dict = {
            'TOS': 'this is directed to a child'
        }
        output = ChintangReader.get_childdirected(rec_dict)
        self.assertTrue(output)

    def test_get_childdirected_TOS_not_childdirected(self):
        rec_dict = {
            'TOS': 'this is directed to an adult'
        }
        output = ChintangReader.get_childdirected(rec_dict)
        self.assertFalse(output)

    def test_get_childdirected_key_does_not_exist(self):
        rec_dict = {}
        output = ChintangReader.get_childdirected(rec_dict)
        self.assertIsNone(output)

    def test_get_id_tier_key_exists(self):
        rec_dict = {
            'id': 3
        }
        actual_output = ChintangReader.get_id_tier(rec_dict)
        desired_output = 3
        self.assertEqual(actual_output, desired_output)

    def test_get_id_tier_key_does_not_exist(self):
        rec_dict = {}
        actual_output = ChintangReader.get_id_tier(rec_dict)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_id_words_two_morpheme_words(self):
        id_tier = 'w1pfxseg-   w1stemseg   -w1sfxseg    w2stemseg'
        actual_output = ChintangReader.get_id_words(id_tier)
        desired_output = ['w1pfxseg-   w1stemseg   -w1sfxseg', 'w2stemseg']
        self.assertEqual(actual_output, desired_output)

    def test_get_id_words_empty_string(self):
        id_tier = ''
        actual_output = ChintangReader.get_id_words(id_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_ids(self):
        id_word = 'w1pfx-   w1stem   -w1sfx w2stem -w2sfx'
        actual_output = ChintangReader.get_id_words(id_word)
        desired_output = ['w1pfx-   w1stem   -w1sfx', 'w2stem -w2sfx']
        self.assertEqual(actual_output, desired_output)

    def test_get_sentence_type(self):
        pass
