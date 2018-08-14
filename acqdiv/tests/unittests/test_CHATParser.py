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
        self.session_file_path = './test_CHATParser.cha'
        self.parser = InuktitutParser(self.session_file_path)
        self.maxDiff = None

    def test_get_reader(self):
        """Test if InuktitutReader is returned."""
        actual_reader = self.parser.get_reader()
        self.assertTrue(isinstance(actual_reader, InuktitutReader))

    def test_get_cleaner(self):
        """Test get_cleaner."""
        actual_cleaner = self.parser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, InuktitutCleaner))

    def test_next_utterance_no_misalignments_one_word(self):
        """Test next_utterance with one word and one morpheme. (Inuktitut)"""
        session_str = (
            '*MAE:\tAllaigutama  .\n%eng:\tGive me a comb  .\n%xmor:\tNR|'
            'ollaoguto^comb+NI|mim^MOD_SG .\n%tim:\t00:01:32\n%add:\tRO\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'MAE',
            'addressee': 'RO',
            'utterance_raw': 'Allaigutama  .',
            'utterance': 'Allaigutama',
            'translation': 'Give me a comb  .',
            'morpheme': 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            'gloss_raw': 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            'pos_raw': 'NR|ollaoguto^comb+NI|mim^MOD_SG .',
            'sentence_type': 'default',
            'start_raw': '00:01:32',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [{
            'word_language': None,
            'word': 'Allaigutama',
            'word_actual': 'Allaigutama',
            'word_target': 'Allaigutama',
            'warning': None
        }]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ollaoguto',
                    'gloss_raw': 'comb',
                    'pos_raw': 'NR'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'mim',
                    'gloss_raw': 'MOD_SG',
                    'pos_raw': 'NI'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignments_multiple_words(self):
        """Test next_utterance with two words and morphemes. (Inuktitut)"""
        session_str = (
            '*AUN:\tana nitu  ?\n%eng:\tit hurts there  ?\n%xmor:\t'
            'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana nitu  ?',
            'utterance': 'ana nitu',
            'translation': 'it hurts there  ?',
            'morpheme': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'gloss_raw': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'pos_raw': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nitu',
                'word_actual': 'nitu',
                'word_target': 'nitu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ta',
                    'gloss_raw': 'here',
                    'pos_raw': 'NN'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ane',
                    'gloss_raw': 'VIA',
                    'pos_raw': 'LO'
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'nir',
                    'gloss_raw': 'hurt',
                    'pos_raw': 'VP'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'jaq',
                    'gloss_raw': 'PAR_3sS',
                    'pos_raw': 'VN'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_words_misaligned(self):
        """Test next_utterance with less words than morphemes. (Inuktitut)"""
        session_str = (
            '*AUN:\tana  ?\n%eng:\tit hurts there ?\n%xmor:\t'
            'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana  ?',
            'utterance': 'ana',
            'translation': 'it hurts there ?',
            'morpheme': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'gloss_raw': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'pos_raw': 'NN|ta^here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ta',
                    'gloss_raw': 'here',
                    'pos_raw': 'NN'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ane',
                    'gloss_raw': 'VIA',
                    'pos_raw': 'LO'
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'nir',
                    'gloss_raw': 'hurt',
                    'pos_raw': 'VP'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'jaq',
                    'gloss_raw': 'PAR_3sS',
                    'pos_raw': 'VN'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_segments_misaligned(self):
        """Test next_utterance, fewer segments than other tiers. (Inuktitut)"""
        session_str = (
            '*AUN:\tana nitu  ?\n%eng:\tit hurts there  ?\n%xmor:\t'
            'NN|here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana nitu  ?',
            'utterance': 'ana nitu',
            'translation': 'it hurts there  ?',
            'morpheme': 'NN|here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'gloss_raw': 'NN|here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'pos_raw': 'NN|here+LO|ane^VIA VP|nir^hurt+VN|jaq^PAR_3sS ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nitu',
                'word_actual': 'nitu',
                'word_target': 'nitu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ane',
                    'gloss_raw': 'VIA',
                    'pos_raw': 'LO'
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'nir',
                    'gloss_raw': 'hurt',
                    'pos_raw': 'VP'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'jaq',
                    'gloss_raw': 'PAR_3sS',
                    'pos_raw': 'VN'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_gloss_misaligned(self):
        """Test next_utterance, fewer glosses than other tiers. (Inuktitut)"""
        session_str = (
            '*AUN:\tana nitu  ?\n%eng:\tit hurts there  ?\n%xmor:\t'
            'NN|ta+LO|ane^VIA VP|nir^hurt+VN|jaq ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana nitu  ?',
            'utterance': 'ana nitu',
            'translation': 'it hurts there  ?',
            'morpheme': 'NN|ta+LO|ane^VIA VP|nir^hurt+VN|jaq ?',
            'gloss_raw': 'NN|ta+LO|ane^VIA VP|nir^hurt+VN|jaq ?',
            'pos_raw': 'NN|ta+LO|ane^VIA VP|nir^hurt+VN|jaq ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nitu',
                'word_actual': 'nitu',
                'word_target': 'nitu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ane',
                    'gloss_raw': 'VIA',
                    'pos_raw': 'LO'
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'nir',
                    'gloss_raw': 'hurt',
                    'pos_raw': 'VP'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_poses_misaligned(self):
        """Test next_utterance, fewer poses than other tiers. (Inuktitut)"""
        session_str = (
            '*AUN:\tana nitu  ?\n%eng:\tit hurts there  ?\n%xmor:\t'
            'NN|ta^here+ane^VIA nir^hurt+VN|jaq^PAR_3sS ?\n%xcod:\t'
            '$VAN $ATA:vl\n%tim:\t00:02:07\n%add:\tWOL\n@End'
        )
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'AUN',
            'addressee': 'WOL',
            'utterance_raw': 'ana nitu  ?',
            'utterance': 'ana nitu',
            'translation': 'it hurts there  ?',
            'morpheme': 'NN|ta^here+ane^VIA nir^hurt+VN|jaq^PAR_3sS ?',
            'gloss_raw': 'NN|ta^here+ane^VIA nir^hurt+VN|jaq^PAR_3sS ?',
            'pos_raw': 'NN|ta^here+ane^VIA nir^hurt+VN|jaq^PAR_3sS ?',
            'sentence_type': 'question',
            'start_raw': '00:02:07',
            'end_raw': None,
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'ana',
                'word_actual': 'ana',
                'word_target': 'ana',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nitu',
                'word_actual': 'nitu',
                'word_target': 'nitu',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'ta',
                    'gloss_raw': 'here',
                    'pos_raw': 'NN'
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                }
            ],
            [
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': None,
                    'gloss_raw': None,
                    'pos_raw': None
                },
                {
                    'morpheme_language': 'Inuktitut',
                    'morpheme': 'jaq',
                    'gloss_raw': 'PAR_3sS',
                    'pos_raw': 'VN'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

###############################################################################


class TestJapaneseMiiProParser(unittest.TestCase):
    """Class to test the JapaneseMiiProParser."""

    def setUp(self):
        self.session_file_path = './test_CHATParser.cha'
        self.parser = JapaneseMiiProParser(self.session_file_path)
        self.maxDiff = None

    def test_get_reader(self):
        """Test if JapaneseMiiProReader is returned."""
        actual_reader = self.parser.get_reader()
        self.assertTrue(isinstance(actual_reader, JapaneseMiiProReader))

    def test_get_cleaner(self):
        """Test if JapaneseMiiProCleaner is returned."""
        actual_cleaner = self.parser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, JapaneseMiiProCleaner))

    def test_next_utterance_no_misalignments_single_word(self):
        """Test next_utterance with utt containing no misalignemnts."""
        session_str = ('*MOT:\tnani ? 107252_107995\n%xtrn:\tn:deic:wh|nani'
                       ' ?\n%ort:\t何 ?\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'nani ?',
            'utterance': 'nani',
            'translation': None,
            'morpheme': 'n:deic:wh|nani ?',
            'gloss_raw': 'n:deic:wh|nani ?',
            'pos_raw': 'n:deic:wh|nani ?',
            'sentence_type': 'question',
            'start_raw': '107252',
            'end_raw': '107995',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'nani',
                'word_actual': 'nani',
                'word_target': 'nani',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'nani',
                    'morpheme_language': None,
                    'pos_raw': 'n:deic:wh'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignments_multiple_words(self):
        """Test next_utterance with utt containing no misalignemnts."""
        session_str = ('tom20010724.cha:*MOT:\tHonochan doozo . '
                       '4087868_4089193\n%xtrn:\tn:prop|Hono-chan co:g|doozo'
                       ' .\n%ort:\tホノちゃんどうぞ。\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'Honochan doozo .',
            'utterance': 'Honochan doozo',
            'translation': None,
            'morpheme': 'n:prop|Hono-chan co:g|doozo .',
            'gloss_raw': 'n:prop|Hono-chan co:g|doozo .',
            'pos_raw': 'n:prop|Hono-chan co:g|doozo .',
            'sentence_type': 'default',
            'start_raw': '4087868',
            'end_raw': '4089193',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'Honochan',
                'word_actual': 'Honochan',
                'word_target': 'Honochan',
                'warning': None
            },
            {
                'word_language': 'Japanese',
                'word': 'doozo',
                'word_actual': 'doozo',
                'word_target': 'doozo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'Hono',
                    'morpheme_language': None,
                    'pos_raw': 'n:prop'
                },
                {
                    'gloss_raw': 'chan',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'doozo',
                    'morpheme_language': None,
                    'pos_raw': 'co:g'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_words_misaligned(self):
        """Test next_utterance with too few words. (JapaneseMiiPro)"""
        session_str = ('tom20010724.cha:*MOT:\tdoozo . '
                       '4087868_4089193\n%xtrn:\tn:prop|Hono-chan co:g|doozo'
                       ' .\n%ort:\tホノちゃんどうぞ。\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'doozo .',
            'utterance': 'doozo',
            'translation': None,
            'morpheme': 'n:prop|Hono-chan co:g|doozo .',
            'gloss_raw': 'n:prop|Hono-chan co:g|doozo .',
            'pos_raw': 'n:prop|Hono-chan co:g|doozo .',
            'sentence_type': 'default',
            'start_raw': '4087868',
            'end_raw': '4089193',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'doozo',
                'word_actual': 'doozo',
                'word_target': 'doozo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'Hono',
                    'morpheme_language': None,
                    'pos_raw': 'n:prop'
                },
                {
                    'gloss_raw': 'chan',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'doozo',
                    'morpheme_language': None,
                    'pos_raw': 'co:g'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_segments_misaligned(self):
        """Test next_utterance with too few segments. (JapaneseMiiPro)"""
        session_str = ('tom20010724.cha:*MOT:\tHonochan doozo . '
                       '4087868_4089193\n%xtrn:\tn:prop|Hono-chan co:g|'
                       ' .\n%ort:\tホノちゃんどうぞ。\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'Honochan doozo .',
            'utterance': 'Honochan doozo',
            'translation': None,
            'morpheme': 'n:prop|Hono-chan co:g| .',
            'gloss_raw': 'n:prop|Hono-chan co:g| .',
            'pos_raw': 'n:prop|Hono-chan co:g| .',
            'sentence_type': 'default',
            'start_raw': '4087868',
            'end_raw': '4089193',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'Honochan',
                'word_actual': 'Honochan',
                'word_target': 'Honochan',
                'warning': None
            },
            {
                'word_language': 'Japanese',
                'word': 'doozo',
                'word_actual': 'doozo',
                'word_target': 'doozo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'Hono',
                    'morpheme_language': None,
                    'pos_raw': 'n:prop'
                },
                {
                    'gloss_raw': 'chan',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'co:g'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_poses_misaligned(self):
        """Test next_utterance with too few poses. (JapaneseMiiPro)"""
        session_str = ('tom20010724.cha:*MOT:\tHonochan doozo . '
                       '4087868_4089193\n%xtrn:\t|Hono-chan co:g|doozo'
                       ' .\n%ort:\tホノちゃんどうぞ。\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'MOT',
            'addressee': None,
            'utterance_raw': 'Honochan doozo .',
            'utterance': 'Honochan doozo',
            'translation': None,
            'morpheme': '|Hono-chan co:g|doozo .',
            'gloss_raw': '|Hono-chan co:g|doozo .',
            'pos_raw': '|Hono-chan co:g|doozo .',
            'sentence_type': 'default',
            'start_raw': '4087868',
            'end_raw': '4089193',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': 'Japanese',
                'word': 'Honochan',
                'word_actual': 'Honochan',
                'word_target': 'Honochan',
                'warning': None
            },
            {
                'word_language': 'Japanese',
                'word': 'doozo',
                'word_actual': 'doozo',
                'word_target': 'doozo',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'Hono',
                    'morpheme_language': None,
                    'pos_raw': None
                },
                {
                    'gloss_raw': 'chan',
                    'morpheme': None,
                    'morpheme_language': None,
                    'pos_raw': 'sfx'
                },
            ],
            [
                {
                    'gloss_raw': None,
                    'morpheme': 'doozo',
                    'morpheme_language': None,
                    'pos_raw': 'co:g'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

###############################################################################


class TestCreeParser(unittest.TestCase):
    """Class to test the CreeParser."""

    def setUp(self):
        self.session_file_path = './test_CHATParser.cha'
        self.parser = CreeParser(self.session_file_path)
        self.maxDiff = None

    def test_get_reader(self):
        """Test get_reader."""
        actual_reader = self.parser.get_reader()
        self.assertTrue(isinstance(actual_reader, CreeReader))

    def test_get_cleaner(self):
        """Test get_cleaner."""
        actual_cleaner = self.parser.get_cleaner()
        self.assertTrue(isinstance(actual_cleaner, CreeCleaner))

    def test_next_utterance_no_misalignments_single_word(self):
        """Test next_utterance with utt containing no misalignemnts."""
        session_str = ('*CHI:\tchair . 2883660_2884622\n%pho:\t*\n%mod:\t*\n'
                       '%eng:\tohhhhhh\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'CHI',
            'addressee': None,
            'utterance_raw': 'chair .',
            'utterance': 'chair',
            'translation': 'ohhhhhh',
            'morpheme': None,
            'gloss_raw': None,
            'pos_raw': None,
            'sentence_type': 'default',
            'start_raw': '2883660',
            'end_raw': '2884622',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'chair',
                'word_actual': 'chair',
                'word_target': 'chair',
                'warning': None
            }
        ]
        morpheme_list = []
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

    def test_next_utterance_no_misalignments_multiple_words(self):
        """Test next_utterance with utt containing no misalignemnts."""

        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.parser.reader.read(io.StringIO(session_str))
        actual_output = list(self.parser.next_utterance())[0]
        utt_dict = {
            'source_id': 'u0',
            'speaker_label': 'CHI',
            'addressee': None,
            'utterance_raw': '‹wâu nîyi› .',
            'utterance': 'wâu nîyi',
            'translation': 'egg me',
            'morpheme': '[wo *]',
            'gloss_raw': '[egg 1]',
            'pos_raw': '[ni pro]',
            'sentence_type': 'default',
            'start_raw': '1198552',
            'end_raw': '1209903',
            'comment': None,
            'warning': None
        }
        words_list = [
            {
                'word_language': None,
                'word': 'wâu',
                'word_actual': 'wâu',
                'word_target': 'wâu',
                'warning': None
            },
            {
                'word_language': None,
                'word': 'nîyi',
                'word_actual': 'nîyi',
                'word_target': 'nîyi',
                'warning': None
            }
        ]
        morpheme_list = [
            [
                {
                    'gloss_raw': 'egg',
                    'morpheme': 'wo',
                    'morpheme_language': 'Cree',
                    'pos_raw': 'ni'
                },
            ],
            [
                {
                    'gloss_raw': '1',
                    'morpheme': None,
                    'morpheme_language': 'Cree',
                    'pos_raw': 'pro'
                }
            ]
        ]
        desired_output = (utt_dict, words_list, morpheme_list)
        self.assertEqual(actual_output, desired_output)

if __name__ == '__main__':
    unittest.main()
