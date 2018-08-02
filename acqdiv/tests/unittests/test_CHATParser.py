import unittest
from acqdiv.parsers.xml.CHATParser import CHATParser
from acqdiv.parsers.xml.CHATReader import *


class TestCHATParser(unittest.TestCase):
    """Class to test the CHATParser."""

    def setUp(self):
        self.session_file_path = './test_CHATParser.cha'
        self.parser = CHATParser(self.session_file_path)
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader with test.cha."""
        actual_reader = self.parser.get_reader()
        desired_reader = ACQDIVCHATReader()
        actual_output = [type(actual_reader), actual_reader.session_file]
        desired_output = [type(desired_reader), desired_reader.session_file]
        self.assertEqual(actual_output, desired_output)

    def test_get_cleaner(self):
        """Test get_cleaner with test.cha."""
        actual_cleaner = self.parser.get_reader()
        desired_cleaner = ACQDIVCHATReader()
        actual_output = [type(actual_cleaner), actual_cleaner.session_file]
        desired_output = [type(desired_cleaner), desired_cleaner.session_file]
        self.assertEqual(actual_output, desired_output)

    def test_get_session_metadata(self):
        """Test get_session_metadata with test.cha."""
        actual_output = self.parser.get_session_metadata()
        desired_output = {
            'date': '1997-09-12',
            'media_filename': 'h2ab'
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_speaker(self):
        """Test next_speaker with test.cha."""
        actual_output = list(self.parser.next_speaker())
        mem_dict = {
            'speaker_label': 'MEM',
            'name': 'Mme_Manyili',
            'age_raw': None,
            'gender_raw': 'female',
            'role_raw': 'Grandmother',
            'languages_spoken': 'sme',
            'birthdate': '1974-10-11'
        }
        chi_dict = {
            'speaker_label': 'CHI',
            'name': 'Hlobohang',
            'age_raw': '2;2.',
            'gender_raw': None,
            'role_raw': 'Target_Child',
            'languages_spoken': 'sme',
            'birthdate': '2006-01-14'
        }
        desired_output = [mem_dict, chi_dict]
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_test_first_utterance(self):
        """Test next utterance with the first utterance of test.cha."""
        actual_output = list(self.parser.next_utterance())[0]
        utt0_utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'MEM',
            'addressee': 'CHI',
            'utterance_raw': 'ke eng ?',
            'utterance': 'ke eng',
            'translation': 'What is it ?',
            'morpheme': None,
            'gloss_raw': None,
            'pos_raw': None,
            'sentence_type': 'question',
            'start_raw': '0',
            'end_raw': '8551',
            'comment': 'Points to tape',
            'warning': None
        }
        utt0_word_list = [
            {
                'word_language': None,
                'word': 'ke',
                'word_actual': 'ke',
                'word_target': 'ke',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'eng',
                'word_actual': 'eng',
                'word_target': 'eng',
                'warning': None
            }
        ]
        utt0_morpheme_list = [
            # {
            #     'morpheme_language': None,
            #     'morpheme': 'ke',
            #     'gloss_raw': 'cp',
            #     'pos_raw': None
            # },
            # {
            #     'morpheme_language': None,
            #     'morpheme': 'eng',
            #     'gloss_raw': 'wh',
            #     'pos_raw': None
            # }
        ]
        desired_output = (utt0_utt_dict, utt0_word_list, utt0_morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_last_utterance_all_tiers_misaligned(self):
        """Test next_utterance with the last utterance of test.cha.

        The utterance contains three words, but only one gloss word
        and two words in the coding tier.

        TODO: what should be the number of None-morphemes?
        """
        actual_output = list(self.parser.next_utterance())[-1]
        utt_utt_dict = {
            'source_id': 'u6',
            'speaker_label': 'MEM',
            'addressee': None,
            'utterance_raw': 'ke khomba khomba .',
            'utterance': 'ke khomba khomba',
            'translation': 'It is a stereo',
            'morpheme': None,
            'gloss_raw': None,
            'pos_raw': None,
            'sentence_type': 'default',
            'start_raw': '28048',
            'end_raw': '31840',
            'comment': None,
            'warning': None
        }
        utt_word_list = [
            {
                'word_language': None,
                'word': 'ke',
                'word_actual': 'ke',
                'word_target': 'ke',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'khomba',
                'word_actual': 'khomba',
                'word_target': 'khomba',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'khomba',
                'word_actual': 'khomba',
                'word_target': 'khomba',
                'warning': None
            }
        ]
        utt_morpheme_list = [
            # {
            #     'morpheme_language': None,
            #     'morpheme': None,
            #     'gloss_raw': None,
            #     'pos_raw': None
            # },
            # {
            #     'morpheme_language': None,
            #     'morpheme': None,
            #     'gloss_raw': None,
            #     'pos_raw': None
            # }
        ]
        desired_output = (utt_utt_dict, utt_word_list, utt_morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignment(self):
        """Test next_utterance with a record with no misalignments.

        Each tier contains two words.
        """
        actual_output = list(self.parser.next_utterance())[1]
        utt_dict = {
            'source_id': 'u1',
            'speaker_label': 'MEM',
            'addressee': None,
            'utterance_raw': 'an ke .',
            'utterance': 'an ke',
            'translation': None,
            'morpheme': None,
            'gloss_raw': None,
            'pos_raw': None,
            'sentence_type': 'default',
            'start_raw': None,
            'end_raw': None,
            'comment': 'test case no misalignments',
            'warning': None
        }
        word_list = [
            {
                'word_language': None,
                'word': 'an',
                'word_actual': 'an',
                'word_target': 'an',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'ke',
                'word_actual': 'ke',
                'word_target': 'ke',
                'warning': None
            }]
        morpheme_list = []
        desired_output = (utt_dict, word_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_misalignment_words_tier(self):
        """Test next_utterance with a words vs morph misalignment.

        There is 1 word in the utterance, but two words on each
        morphology tier.
        """
        pass

    def test_next_utterance_misalignment_gloss_tier(self):
        """Test next_utterance with a gloss vs other tiers misalignment.

        There is one gloss-word but two words on all other tiers.
        """
        pass

    def test_next_utterance_misalignments_segments_tier(self):
        """Test next_utterance with segment vs other tiers misalignemnt.

        There is one segment word but two words on all other tiers.
        """
        pass

    def test_next_utterance_misalignment_pos_tier(self):
        """Test next_utterance with pos vs other tiers misalignment.

        There is one pos-word but two words on all other tiers.
        """
        pass


if __name__ == '__main__':
    unittest.main()
