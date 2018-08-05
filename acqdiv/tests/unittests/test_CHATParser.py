import io
import unittest
from acqdiv.parsers.xml.CHATParser import *
from acqdiv.parsers.xml.CHATReader import *
from acqdiv.parsers.xml.CHATCleaner import *


class TestCHATParser(unittest.TestCase):
    """Class to test the CHATParser."""

    def setUp(self):
        self.session_file_path = './test_CHATParser.cha'
        self.parser = CHATParser(self.session_file_path)
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader."""
        actual_reader = CHATParser.get_reader()
        self.assertTrue(isinstance(actual_reader, ACQDIVCHATReader))

    def test_get_cleaner(self):
        """Test get_cleaner."""
        actual_cleaner = CHATParser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, CHATCleaner))

    def test_get_session_metadata(self):
        """Test get_session_metadata with test.cha."""
        session_str = (
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
            '*MEM:\tke eng ? \x150_8551\x15\n%gls:\tke eng ?\n'
            '@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = self.parser.get_session_metadata()
        desired_output = {
            'date': '1997-09-12',
            'media_filename': 'h2ab'
        }
        self.assertEqual(actual_output, desired_output)

    def test_next_speaker(self):
        """Test next_speaker with test.cha."""
        session_str = (
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
            '*MEM:\tke eng ? \x150_8551\x15\n%gls:\tke eng ?\n'
            '@End')
        self.parser.reader.read(io.StringIO(session_str))
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
        utt_str = (
            '@Begin\n*MEM:\tke eng ? 0_8551\n%gls:\tke eng ?\n%cod:\tcp wh ?'
            '\n%eng:\tWhat is it ?\n%sit:\tPoints to tape\n%com:\tis furious\n'
            '%add:\tCHI\n@End'
        )
        self.parser.reader.read(io.StringIO(utt_str))
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
            'comment': 'is furious; Points to tape',
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
        utt0_morpheme_list = []
        desired_output = (utt0_utt_dict, utt0_word_list, utt0_morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_last_utterance_all_tiers_misaligned(self):
        """Test next_utterance with the last utterance of test.cha.

        The utterance contains three words, but only one gloss word
        and two words in the coding tier.
        """
        session_str = (
            '*MEM:\tke khomba\nkhomba . 28048_31840\n%gls:\tkekumbakumba .\n'
            '%cod:\tcp tape_recorder(9 , 10) .\n%eng:\tIt is a stereo\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_utt_dict = {
            'source_id': 'u0',
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
        utt_morpheme_list = []
        desired_output = (utt_utt_dict, utt_word_list, utt_morpheme_list)
        self.assertEqual(actual_output, desired_output)

    # TODO: Decide if test is necessary, if yes, fix test
    # def test_next_utterance_no_misalignment(self):
    #     """Test next_utterance with a record with no misalignments.
    #
    #     Each tier contains two words.
    #     """
    #     session_str = (
    #         '*CHI:\tke ntencha ncha .8551_19738\n% gls:\tke ntho e-ncha .\n% '
    #         'cod:\tcp thing(9, 10) 9 - aj .\n% eng:\tA new thing\n% com:\ttest '
    #         'comment\n@End'
    #     )
    #     self.parser.reader.read(io.StringIO(session_str))
    #     actual_output = list(self.parser.next_utterance())[0]
    #     utt_dict = {
    #         'source_id': 'u0',
    #         'speaker_label': 'MEM',
    #         'addressee': None,
    #         'utterance_raw': 'ke ntencha ncha .',
    #         'utterance': 'ke ntencha ncha',
    #         'translation': None,
    #         'morpheme': None,
    #         'gloss_raw': None,
    #         'pos_raw': None,
    #         'sentence_type': 'default',
    #         'start_raw': None,
    #         'end_raw': '19738',
    #         'comment': 'test comment',
    #         'warning': None
    #     }
    #     word_list = [
    #         {
    #             'word_language': None,
    #             'word': 'an',
    #             'word_actual': 'an',
    #             'word_target': 'an',
    #             'warning': None
    #         },
    #         {
    #             'word_language': None,
    #             'word': 'ke',
    #             'word_actual': 'ke',
    #             'word_target': 'ke',
    #             'warning': None
    #         }]
    #     morpheme_list = []
    #     desired_output = (utt_dict, word_list, morpheme_list)
    #     self.assertEqual(actual_output, desired_output)

    @unittest.skip('Not finished.')
    def test_next_utterance_misalignment_words_tier(self):
        """Test next_utterance with a words vs morph misalignment.

        There is 1 word in the utterance, but two words on each
        morphology tier.
        """
        session = ('@Languages:\tsme\n*MEM:\tke ? 0_8551\n%gls:\tke eng ?'
                   '\n%cod:\tcp wh ?\n%eng:\tWhat is it ?')
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'MEM',
            'addressee': 'CHI',
            'utterance_raw': 'ke ?',
            'utterance': 'ke',
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
        word_list = [
            {
                'word_language': None,
                'word': 'ke',
                'word_actual': 'ke',
                'word_target': 'ke',
                'warning': None
            },
        ]
        morpheme_list = []
        desired_output = (utt_dict, word_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    @unittest.skip('Not finished.')
    def test_next_utterance_misalignment_gloss_tier(self):
        """Test next_utterance with a gloss vs other tiers misalignment.

        There is one gloss-word but two words on all other tiers.
        """
        session = ('@Languages:\tsme\n*MEM:\tke eng ? 0_8551\n%gls:\tke '
                   'eng ?\n%cod:\tcp ?\n%eng:\tWhat is it ?')
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
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
        word_list = [
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
        morpheme_list = []
        desired_output = (utt_dict, word_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    @unittest.skip('Not finished.')
    def test_next_utterance_misalignments_segments_tier(self):
        """Test next_utterance with segment vs other tiers misalignemnt.

        There is one segment word but two words on all other tiers.
        """
        session = ('@Languages:\tsme\n*MEM:\tke eng ? 0_8551\n%gls:\tke '
                   '?\n%cod:\tcp wh ?\n%eng:\tWhat is it ?')
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
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
        word_list = [
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
        morpheme_list = []
        desired_output = (utt_dict, word_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    @unittest.skip('Not finished.')
    def test_next_utterance_misalignment_pos_tier(self):
        """Test next_utterance with pos vs other tiers misalignment.

        There is one pos-word but two words on all other tiers.
        """
        session = ('@Languages:\tsme\n*MEM:\tke eng ? 0_8551\n%gls:\tke '
                   '?\n%cod:\tcp wh ?\n%pos:\tV N\n%eng:\tWhat is it ?')
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
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
        word_list = [
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
        morpheme_list = []
        desired_output = (utt_dict, word_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

###############################################################################


class TestInuktitutParser(unittest.TestCase):
    """
    Class to test InuktitutParser.
    """

    def setUp(self):
        self.session_file_path = './test_InuktitutParsers.cha'
        self.parser = InuktitutParser(self.session_file_path)
        self.maxDiff = None

    def test_get_reader(self):
        """Test if a correctly initialized reader is returned."""
        actual_reader = self.parser.get_reader()
        desired_reader = InuktitutReader()
        actual_output = [type(actual_reader), actual_reader.session_file_path]
        desired_output = [type(desired_reader), desired_reader.session_file_path]
        self.assertEqual(actual_output, desired_output)

if __name__ == '__main__':
    unittest.main()
