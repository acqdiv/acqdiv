import unittest
import io
from acqdiv.parsers.chat.readers.CHATReader import CHATReader
from acqdiv.parsers.chat.readers.ACQDIVCHATReader import ACQDIVCHATReader
from acqdiv.parsers.chat.readers.InuktitutReader import InuktitutReader
from acqdiv.parsers.chat.readers.JapaneseMiiProReader import \
    JapaneseMiiProReader
from acqdiv.parsers.chat.readers.CreeReader import CreeReader
from acqdiv.parsers.chat.readers.EnglishManchester1Reader import \
    EnglishManchester1Reader
from acqdiv.parsers.chat.readers.SesothoReader import SesothoReader
from acqdiv.parsers.chat.readers.TurkishReader import TurkishReader
from acqdiv.parsers.chat.readers.YucatecReader import YucatecReader
from acqdiv.parsers.chat.readers.NungonReader import NungonReader


class TestCHATReader(unittest.TestCase):
    """Class to test the CHATReader."""

    # ---------- iter_metadata_fields ----------

    def test_iter_metadata_fields(self):
        """Test iter_metadata_fields with normal intput."""
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
            '*MEM:\tke eng ? \x150_8551\x15\n%gls:\tke eng ?\n'
            '@End')

        actual_output = list(CHATReader.iter_metadata_fields(session))
        desired_output = ['@Languages:\tsme',
                          '@Date:\t12-SEP-1997',
                          ('@Participants:\tMEM Mme_Manyili Grandmother , '
                           'CHI Hlobohang Target_Child'),
                          '@ID:\tsme|Sesotho|MEM||female|||Grandmother|||',
                          '@ID:\tsme|Sesotho|CHI|2;2.||||Target_Child|||',
                          '@Birth of CHI:\t14-JAN-2006',
                          '@Birth of MEM:\t11-OCT-1974',
                          '@Media:\th2ab, audio',
                          '@Comment:\tall snd kana jmor cha ok Wakachi2002;',
                          '@Warning:\trecorded time: 1:00:00',
                          '@Comment:\tuses desu and V-masu',
                          '@Situation:\tAki and AMO preparing to look at '
                          'book , "Miichan no otsukai"']
        self.assertEqual(actual_output, desired_output)

    def test_iter_metadata_fields_line_breaks(self):
        """Test iter_metadata_fields with line breaks.

        Attested in Japanese MiiPro.
        """
        session = (
            '@UTF8\n'
            '@Begin\n'
            '@Participants:\tMEM Mme_Manyili Grandmother ,\n\t'
            'CHI Hlobohang Target_Child\n'
            '@Comment:\tHere comes a comment.\n'
            '*MEM:\tke eng ? \x150_8551\x15\n%gls:\tke eng ?\n'
            '@End')

        actual_output = list(CHATReader.iter_metadata_fields(session))
        desired_output = [('@Participants:\tMEM Mme_Manyili Grandmother , '
                           'CHI Hlobohang Target_Child'),
                          '@Comment:\tHere comes a comment.']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_metadata_field ----------

    def test_get_metadata_field_normal_field(self):
        """Test get_metadata_field for a normal field."""
        actual_output = CHATReader.get_metadata_field('@Languages:\tsme')
        desired_output = ('Languages', 'sme')
        self.assertEqual(actual_output, desired_output)

    def test_get_metadata_field_multi_valued_field(self):
        """Test get_metadata_field for a field with multiple values."""
        ptcs_field = '@Participants:\tMEM Mme_Manyili Grandmother , ' \
                     'CHI Hlobohang Target_Child , ' \
                     'KAT Katherine_Demuth Investigator'
        actual_output = CHATReader.get_metadata_field(ptcs_field)
        ptcs = 'MEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , ' \
               'KAT Katherine_Demuth Investigator'
        desired_output = ('Participants', ptcs)
        self.assertEqual(actual_output, desired_output)

    # ---------- get_media_fields ----------

    def test_get_media_fields_two_fields(self):
        """Test get_media_fields method for two field input."""
        actual_output = CHATReader.get_media_fields('h2ab, audio')
        desired_output = ('h2ab', 'audio', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_media_fields_three_fields(self):
        """Test get_media_fields for three field input."""
        input_str = 'h2ab, audio, unknown speaker'
        actual_output = CHATReader.get_media_fields(input_str)
        desired_output = ('h2ab', 'audio', 'unknown speaker')
        self.assertEqual(actual_output, desired_output)

    # ---------- get_media_filename ----------

    def test_get_media_filename(self):
        """Test get_media_filename with standard case of 3 fields."""
        media_fields = ['h2ab', 'video', 'unlinked']
        actual_output = CHATReader.get_media_filename(media_fields)
        desired_output = 'h2ab'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_media_format ----------

    def test_get_media_format(self):
        """Test get_media_format with standard case of 3 fields."""
        media_fields = ['h2ab', 'video', 'unlinked']
        actual_output = CHATReader.get_media_format(media_fields)
        desired_output = 'video'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_media_comment ----------

    def test_get_media_comment(self):
        """Test get_media_comment with standard case of 3 fields."""
        media_fields = ['h2ab', 'video', 'unlinked']
        actual_output = CHATReader.get_media_comment(media_fields)
        desired_output = 'unlinked'
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_participants ----------

    def test_iter_participants(self):
        """Test iter_participants for a normal case."""
        ptcs = 'MEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , ' \
               'KAT Katherine_Demuth Investigator'
        actual_output = list(CHATReader.iter_participants(ptcs))
        ptcs_list = ['MEM Mme_Manyili Grandmother',
                     'CHI Hlobohang Target_Child',
                     'KAT Katherine_Demuth Investigator']
        desired_output = ptcs_list
        self.assertEqual(actual_output, desired_output)

    def test_iter_participants_multiple_spaces(self):
        """Test iter_participants with multiple spaces.

        Attested in Japanese MiiPro.
        """
        ptcs = ('MEM Mme_Manyili Grandmother,  '
                'CHI Hlobohang Target_Child,  '
                'KAT Katherine_Demuth Investigator')
        actual_output = list(CHATReader.iter_participants(ptcs))
        ptcs_list = ['MEM Mme_Manyili Grandmother',
                     'CHI Hlobohang Target_Child',
                     'KAT Katherine_Demuth Investigator']
        desired_output = ptcs_list
        self.assertEqual(actual_output, desired_output)

    # ---------- get_participant_fields ----------

    def test_get_participant_fields_one_field(self):
        """Test get_participant_fields for one field input."""
        actual_output = CHATReader.get_participant_fields('MEM')
        desired_output = ('MEM', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_fields_two_fields(self):
        """Test get_participant_fields for two field input."""
        actual_output = CHATReader.get_participant_fields('MEM Grandmother')
        desired_output = ('MEM', '', 'Grandmother')
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_fields_three_fields(self):
        """Test get_participant_fields for three field input"""
        ptcs_field = 'CHI Hlobohang Target_Child'
        actual_output = CHATReader.get_participant_fields(ptcs_field)
        desired_output = ('CHI', 'Hlobohang', 'Target_Child')
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_fields ----------

    def test_get_id_fields_all_empty_fields(self):
        """Test get_id_fields for the case of all fields being empty."""
        input_str = '||||||||||'
        actual_output = CHATReader.get_id_fields(input_str)
        desired_output = ('', '', '', '', '', '', '', '', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_id_fields_some_empty(self):
        """The the get_id_fields-method.

        Test get_id_fields for the case of some fields
        being empty and some fields containing information.
        """
        id_fields = 'sme|Sesotho|MEM||female|||Grandmother|||'
        actual_output = CHATReader.get_id_fields(id_fields)
        desired_output = ('sme', 'Sesotho', 'MEM', '', 'female', '',
                          '', 'Grandmother', '', '')
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_language ----------

    def test_get_id_language(self):
        """Test get_id_language with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_language(id_fields)
        desired_output = 'sme'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_corpus ----------

    def test_get_id_corpus(self):
        """Test get_id_corpus with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_corpus(id_fields)
        desired_output = 'Sesotho'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_code ----------

    def test_get_id_code(self):
        """Test get_id_code with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_code(id_fields)
        desired_output = 'MEM'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_age ----------

    def test_get_id_age(self):
        """Test get_id_age with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_age(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_sex ----------

    def test_get_id_sex(self):
        """Test get_id_sex with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_sex(id_fields)
        desired_output = 'female'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_group ----------

    def test_get_id_group(self):
        """Test get_id_group with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_group(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_ses ----------

    def test_get_id_ses(self):
        """Test get_id_ses with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_ses(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_role ----------

    def test_get_id_role(self):
        """Test get_id_role with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_role(id_fields)
        desired_output = 'Grandmother'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_education ----------

    def test_get_id_education(self):
        """Test get_id_education with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_education(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_custom ----------

    def test_get_id_custom(self):
        """Test get_id_custom with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = CHATReader.get_id_custom(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- replace_line_breaks ----------

    def test_replace_line_breaks_single(self):
        """Test replace_line_breaks for single line break."""
        input_str = 'n^name ij\n\tsm2s-t^p_v^leave-m^s.'
        actual_output = CHATReader._replace_line_breaks(input_str)
        desired_output = 'n^name ij sm2s-t^p_v^leave-m^s.'
        self.assertEqual(actual_output, desired_output)

    def test_replace_line_breaks_multiple(self):
        """Test replace_line_breaks for two following linebreaks."""
        input_str = 'n^name ij sm2s-t^p_v^leave-m^s n^name\n\t' \
                    'sm1-t^p-v^play-m^s pr house(9 , 10/6)/lc ' \
                    'sm1-t^p-v^chat-m^s\n\tcj n^name .'
        actual_output = CHATReader._replace_line_breaks(input_str)
        desired_output = 'n^name ij sm2s-t^p_v^leave-m^s n^name ' \
                         'sm1-t^p-v^play-m^s pr house(9 , 10/6)/lc ' \
                         'sm1-t^p-v^chat-m^s cj n^name .'
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_records ----------

    def test_iter_records(self):
        """Test iter_records for multiple records. (standard case)"""
        session = ('@UTF8\n@Begin\n@Birth of CHI:\t14-JAN-2006\n'
                   '*MEM:\tke eng ? \x150_8551\x15\n%gls:\tke eng ?\n%cod:\t'
                   'cp wh ?\n%eng:\tWhat is it ?\n%sit:\tPoints to '
                   'tape\n%com:\tis furious\n%add:\tCHI\n'
                   '*CHI:\tke ntencha ncha . \x158551_19738\x15\n'
                   '%gls:\tke ntho e-ncha .\n%cod:\tcp thing(9 , 10) '
                   '9-aj .\n%eng:\tA new thing\n%com:\ttest comment\n'
                   '*MEM:\tke eng ntho ena e? \x1519738_24653\x15\n%gls:\t'
                   'ke eng ntho ena e ?\n%cod:\tcp wh thing(9 , 10) '
                   'd9 ij ?\n%eng:\tWhat is this thing ?\n%sit:\t'
                   'Points to tape\n'
                   '*CHI:\te nte ena . \x1524300_28048\x15\n%gls:\tke ntho '
                   'ena .\n%cod:\tcp thing(9 , 10) d9 .\n%eng:\t'
                   'It is this thing\n'
                   '*MEM:\tke khomba\n\tkhomba . \x1528048_31840\x15\n%gls:\t'
                   'kekumbakumba .\n%cod:\tcp tape_recorder(9 , 10) .'
                   '\n%eng:\tIt is a stereo\n@End\n')
        actual_output = list(CHATReader.iter_records(session))
        desired_output = ['*MEM:\tke eng ? 0_8551\n%gls:\tke eng ?\n%cod:\t'
                          'cp wh ?\n%eng:\tWhat is it ?\n%sit:\tPoints to '
                          'tape\n%com:\tis furious\n%add:\tCHI',
                          '*CHI:\tke ntencha ncha . 8551_19738\n'
                          '%gls:\tke ntho e-ncha .\n%cod:\tcp thing(9 , 10) '
                          '9-aj .\n%eng:\tA new thing\n%com:\ttest comment',
                          '*MEM:\tke eng ntho ena e? 19738_24653\n%gls:\t'
                          'ke eng ntho ena e ?\n%cod:\tcp wh thing(9 , 10) '
                          'd9 ij ?\n%eng:\tWhat is this thing ?\n%sit:\t'
                          'Points to tape',
                          '*CHI:\te nte ena . 24300_28048\n%gls:\tke ntho '
                          'ena .\n%cod:\tcp thing(9 , 10) d9 .\n%eng:\t'
                          'It is this thing',
                          '*MEM:\tke khomba khomba . 28048_31840\n%gls:	'
                          'kekumbakumba .\n%cod:\tcp tape_recorder(9 , 10) .'
                          '\n%eng:\tIt is a stereo']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_mainline ----------

    def test_get_mainline_standard_case(self):
        """Test get_mainline for a standard record."""
        record = '*KAT:	ke eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What is it ?\n%sit:	Points to tape'
        actual_output = CHATReader.get_mainline(record)
        desired_output = '*KAT:	ke eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_star_in_mainline(self):
        """Test get_mainline with a star in the mainline."""
        record = '*KAT:	ke *eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What is it ?\n%sit:	Points to tape'
        actual_output = CHATReader.get_mainline(record)
        desired_output = '*KAT:	ke *eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_star_in_dependent_tier(self):
        """Test get_mainline with a star in the dependent tier."""
        record = '*KAT:	ke eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What *is it ?\n%sit:	Points to tape'
        actual_output = CHATReader.get_mainline(record)
        desired_output = '*KAT:	ke eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_mainline_fields ----------

    def test_get_mainline_fields_with_time(self):
        """Test get_mainline_fields for mainline with timestamp."""
        mainline = '*KAT:	ke eng ? 0_8551'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_time_multiple_spaces(self):
        """Test get_mainline_fields with multiple spaces before timestamp.

        Attested in Japanese MiiPro.
        """
        mainline = '*KAT:	ke eng ?  0_8551'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_no_space_before_time(self):
        """Test get_mainline_fields for no space before the timestamp.

        There is no space between the terminator and the timestamp. Such
        examples can be found for example in Japanese_MiiPro.
        """
        mainline = '*KAT:	ke eng ?0_8551'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_single_postcode(self):
        """Test get_mainline_fields for mainline with postcode."""
        mainline = '*KAT:	ke eng ? [+ neg]'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ? [+ neg]', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_multiple_postcodes(self):
        """Test get_mainline_fields for mainline with postcodes."""
        mainline = '*KAT:	ke eng ? [+ neg] [+ req]'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ? [+ neg] [+ req]', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_postcode_multiple_spaces(self):
        """Test get_mainline_fields with multiple spaces before postcode.

        Attested in Japanese MiiPro.
        """
        mainline = '*KAT:	ke eng ?  [+ neg]'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?  [+ neg]', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_no_space_before_postcode(self):
        """Test get_mainline_fields for no space before the postcode.

        There is no space between the terminator and the postcode. Such
        examples can be found for example in Japanese_MiiPro.
        """
        mainline = '*KAT:	ke eng ?[+ neg]'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?[+ neg]', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_multiple_postcodes_and_time(self):
        """Test get_mainline_fields for mainline with postcodes."""
        mainline = '*KAT:	ke eng ? [+ neg] [+ req] 0_8551'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ? [+ neg] [+ req]', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_without_time(self):
        """Test get mainline fields for mainline without timestamp"""
        mainline = '*KAT:	ke eng ntho ena e?'
        actual_output = CHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ntho ena e?', '', '')
        self.assertEqual(actual_output, desired_output)

    # ---------- get_utterance_words ----------

    def test_get_utterance_words_standard_case(self):
        """Test get_utterance_words for standard input."""
        utterance = 'ke eng ntho ena e?'
        actual_output = CHATReader.get_utterance_words(utterance)
        desired_output = ['ke', 'eng', 'ntho', 'ena', 'e?']
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words_empty_string(self):
        """Test get_utterance_words for standard input."""
        utterance = ''
        actual_output = CHATReader.get_utterance_words(utterance)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words_multiple_blank_spaces(self):
        """Test get_utterance_words with multiple blank spaces."""
        utterance = 'ke eng  ntho ena   e?'
        actual_output = CHATReader.get_utterance_words(utterance)
        desired_output = ['ke', 'eng', 'ntho', 'ena', 'e?']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_utterance_terminator ----------

    def test_get_utterance_terminator_space_before(self):
        """Test get_utterance_terminator with space before."""
        utterance = 'Das ist ein Test .'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_no_space_before(self):
        """Test get_utterance_terminator with no space before."""
        utterance = 'Das ist ein Test.'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode(self):
        """Test get_utterance_terminator with postcode."""
        utterance = 'Das ist ein Test . [+ postcode]'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode_no_space(self):
        """Test get_utterance_terminator with postcode and no space."""
        utterance = 'Das ist ein Test .[+ postcode]'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode_multiple_spaces(self):
        """Test get_utterance_terminator with postcode and multiple spaces."""
        utterance = 'Das ist ein Test .  [+ postcode]'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_non_terminator_dot(self):
        """Test get_utterance_terminator with a non-terminator dot."""
        utterance = 'Das ist (.) ein Test ? [+ postcode]'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_no_terminator(self):
        """Test get_utterance_terminator with no terminator."""
        utterance = 'Das ist ein Test'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_empty_string(self):
        """Test get_utterance_terminator with empty string."""
        utterance = ''
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_question(self):
        """Test get_utterance_terminator with question mark."""
        utterance = 'this is a test ?'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_exclamation(self):
        """Test get_utterance_terminator with exclamation mark."""
        utterance = 'this is a test !'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '!'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_broken_for_coding(self):
        """Test get_utterance_terminator with broken-for-coding mark."""
        utterance = 'this is a test +.'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_trail_off(self):
        """Test get_utterance_terminator with trail-off mark."""
        utterance = 'this is a test +...'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+...'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_trail_off_of_a_question(self):
        """Test get_utterance_terminator with trail-off-of-a-question mark."""
        utterance = 'this is a test +..?'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+..?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_question_with_exclamation(self):
        """Test get_utterance_terminator with question-exclamation mark."""
        utterance = 'this is a test +!?'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+!?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_interruption(self):
        """Test get_utterance_terminator with interruption mark."""
        utterance = 'this is a test +/.'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+/.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_interruption_of_a_question(self):
        """Test get_utterance_terminator with interruption-question mark."""
        utterance = 'this is a test +/?'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+/?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_self_interruption(self):
        """Test get_utterance_terminator with self-interruption mark."""
        utterance = 'this is a test +//.'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+//.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_self_interrupted_question(self):
        """Test get_utterance_terminator with self-interrupted-question."""
        utterance = 'this is a test +//?'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+//?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_quotation_follows(self):
        """Test get_utterance_terminator with quotation-follows mark."""
        utterance = 'this is a test +"/.'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+"/.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_quotation_precedes(self):
        """Test get_utterance_terminator with quotation-precedes mark."""
        utterance = 'this is a test +".'
        actual_output = CHATReader.get_utterance_terminator(utterance)
        desired_output = '+".'
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_dependent_tiers ----------

    def test_iter_dependent_tiers_standard_case(self):
        """Test iter_dependent_tiers for standard input."""
        record = '*CHI:	ke ntencha ncha . 8551_19738\n%gls:	ke ntho ' \
                 'e-ncha .\n%cod:	cp thing(9 , 10) 9-aj .\n' \
                 '%eng:	A new thing'
        actual_output = list(CHATReader.iter_dependent_tiers(record))
        desired_output = ['%gls:	ke ntho e-ncha .',
                          '%cod:	cp thing(9 , 10) 9-aj .',
                          '%eng:	A new thing']
        self.assertEqual(actual_output, desired_output)

    def test_iter_dependent_tiers_with_additional_percent_signs(self):
        """Test iter_dependent_tiers with an additional percent sign.

        Test iter_dependent_tiers for the case of there being
        an additional percent sign in a dependent tier.
        """
        record = '*CHI:	ke ntencha ncha . 8551_19738\n%gls:	ke ntho ' \
                 'e-ncha .\n%cod%:	cp thing(9 , 10) 9-aj .\n' \
                 '%eng:	A new% thing'
        actual_output = list(CHATReader.iter_dependent_tiers(record))
        desired_output = ['%gls:	ke ntho e-ncha .',
                          '%cod%:	cp thing(9 , 10) 9-aj .',
                          '%eng:	A new% thing']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_dependent_tier ----------

    def test_get_dependent_tier_standard_case(self):
        """Test get_dependent_tier for standard input."""
        dep_tier = '%eng:	A new thing'
        actual_output = CHATReader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thing')
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_additional_colon(self):
        """Test get_dependent_tier with colon.

        Test get_dependent_tier for input where a
        colon appears in the content of the dependent tier,
        """

        dep_tier = '%eng:	A new thi:ng'
        actual_output = CHATReader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thi:ng')
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_additional_percent(self):
        """Test get_dependent_tier with percent sign.

        Test get_dependent_tier for the case of there
        being a percent sign in the dependent tier."
        """
        dep_tier = '%eng:	A new thing%'
        actual_output = CHATReader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thing%')
        self.assertEqual(actual_output, desired_output)


###############################################################################

class TestACQDIVCHATReaderMetadata(unittest.TestCase):
    """Test metadata readers of ACQDIVCHATReader.

    Excluding speaker metadata.
    """

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '@Date:\t12-SEP-1997\n'
                   '@Media:\tmedia_filename, audio\n'
                   '@End')
        cls.reader = ACQDIVCHATReader()
        cls.reader.read(io.StringIO(session))

    def test_get_session_date(self):
        """Test get_session_date with test.cha. """
        actual_output = self.reader.get_session_date()
        desired_output = '12-SEP-1997'
        self.assertEqual(actual_output, desired_output)

    def test_get_session_media_filename(self):
        """Test get_session_media_filename for sessions name of 'test.cha'."""
        actual_output = self.reader.get_session_media_filename()
        desired_output = 'media_filename'
        self.assertEqual(actual_output, desired_output)


class TestACQDIVCHATReaderSpeaker(unittest.TestCase):
    """Test speaker readers of ACQDIVCHATReader."""

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '@Participants:\tCHI Hlobohang Target_Child\n'
                   '@ID:\tsme|Sesotho|CHI|2;2.||||Target_Child|||\n'
                   '@Birth of CHI:\t14-JAN-2006\n'
                   '@End')
        cls.reader = ACQDIVCHATReader()
        cls.reader.read(io.StringIO(session))
        cls.reader.load_next_speaker()

    def test_get_speaker_age(self):
        actual_output = self.reader.get_speaker_age()
        desired_output = '2;2.'
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_birthdate(self):
        """Test get_speaker_birthdate with test.cha."""
        actual_output = self.reader.get_speaker_birthdate()
        desired_output = '14-JAN-2006'
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_gender(self):
        """Test get_speaker_gender with test.cha."""
        actual_output = self.reader.get_speaker_gender()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_label(self):
        """Test get_speaker_label with test.cha."""
        actual_output = self.reader.get_speaker_label()
        desired_output = 'CHI'
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_language(self):
        """Test get_speaker_language with test.cha."""
        actual_output = self.reader.get_speaker_language()
        desired_output = 'sme'
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_name(self):
        """Test get_speaker_name with test.cha."""
        actual_output = self.reader.get_speaker_name()
        desired_output = 'Hlobohang'
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_role(self):
        """Test get_speaker_role with test.cha."""
        actual_output = self.reader.get_speaker_role()
        desired_output = 'Target_Child'
        self.assertEqual(actual_output, desired_output)


class TestACQDIVCHATReaderRecord(unittest.TestCase):
    """Test record readers of ACQDIVCHATReader."""

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '*MEM:\t&foo ma(i)nline [: utterance]. \x150_1111\x15\n'
                   '%add:\tADD\n'
                   '%sit:\tThis is the situation\n'
                   '%act:\tThis is the action\n'
                   '%mor:\tThis is the morphology tier\n'
                   '%eng:\tThis is the translation.\n'
                   '%com:\tThis is the comment\n'
                   '%exp:\tThis is the explanation\n'
                   '@End')
        cls.reader = ACQDIVCHATReader()
        cls.reader.read(io.StringIO(session))
        cls.reader.load_next_record()

    def test_get_uid(self):
        """Test get_uid."""
        actual_output = self.reader.get_uid()
        desired_output = '0'
        self.assertEqual(actual_output, desired_output)

    def test_get_addressee(self):
        """Test get_addressee."""
        actual_output = self.reader.get_addressee()
        desired_output = 'ADD'
        self.assertEqual(actual_output, desired_output)

    def test_get_translation(self):
        """Test get_translation."""
        actual_output = self.reader.get_translation()
        desired_output = 'This is the translation.'
        self.assertEqual(actual_output, desired_output)

    def test_get_comments(self):
        """Test get_comments."""
        actual_output = self.reader.get_comments()
        desired_output = ('This is the comment; '
                          'This is the situation; '
                          'This is the action; '
                          'This is the explanation')
        self.assertEqual(actual_output, desired_output)

    def test_get_record_speaker_label(self):
        """Test get_record_speaker_label."""
        actual_output = self.reader.get_record_speaker_label()
        desired_output = 'MEM'
        self.assertEqual(actual_output, desired_output)

    def test_get_start_time(self):
        """Test get_start_time."""
        actual_output = self.reader.get_start_time()
        desired_output = '0'
        self.assertEqual(actual_output, desired_output)

    def test_get_end_time(self):
        """Test get_end_time."""
        actual_output = self.reader.get_end_time()
        desired_output = '1111'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance(self):
        """Test get_utterance."""
        actual_output = self.reader.get_utterance()
        desired_output = '&foo ma(i)nline [: utterance].'
        self.assertEqual(actual_output, desired_output)

    def get_actual_utterance(self):
        actual_output = self.reader.get_actual_utterance()
        desired_output = 'foo manline.'
        self.assertEqual(actual_output, desired_output)

    def test_get_target_utterance(self):
        """Test get_utterance."""
        actual_output = self.reader.get_target_utterance()
        desired_output = 'xxx utterance.'
        self.assertEqual(actual_output, desired_output)

    def test_get_sentence_type(self):
        """Test get_sentence_type."""
        actual_output = self.reader.get_sentence_type()
        desired_output = 'default'
        self.assertEqual(actual_output, desired_output)

    def test_get_morph_tier(self):
        """Test get_morph_tier."""
        actual_output = self.reader.get_morph_tier()
        desired_output = 'This is the morphology tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_tier(self):
        actual_output = self.reader.get_seg_tier()
        desired_output = 'This is the morphology tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier(self):
        actual_output = self.reader.get_gloss_tier()
        desired_output = 'This is the morphology tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier(self):
        actual_output = self.reader.get_pos_tier()
        desired_output = 'This is the morphology tier'
        self.assertEqual(actual_output, desired_output)


class TestACQDIVCHATReaderIterators(unittest.TestCase):
    """Test iterator methods of ACQDIVCHATReader."""

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '@Participants:\tMOT Kim Mother, CHI Daniel Target_Child\n'
                   '@ID:\t|English|MOT|||||Mother|||\n'
                   '@ID:\t|English|CHI|2;8.|male|||Target_Child|||\n'
                   '*MOT:\tThis is the first mainline of MOT .\n'
                   '%eng:\tThis is the translation\n'
                   '*CHI:\tThis is the first mainline of CHI .\n'
                   '%gls:\tThis is the gls tier\n'
                   '%cod:\tThis is the cod tier\n'
                   '*MOT:\tThis is the second mainline of MOT .\n'
                   '@End')
        cls.reader = ACQDIVCHATReader()
        cls.reader.read(io.StringIO(session))

    def test_load_next_speaker(self):
        """Test load_next_speaker."""
        actual_output = []
        while self.reader.load_next_speaker():
            actual_output.append(self.reader._speaker)
        desired_output = [
            {'id': ('', 'English', 'MOT', '', '', '', '', 'Mother', '', ''),
             'participant': ('MOT', 'Kim', 'Mother')},
            {'id': ('', 'English', 'CHI', '2;8.', 'male', '', '',
                    'Target_Child', '', ''),
             'participant': ('CHI', 'Daniel', 'Target_Child')}]
        self.assertEqual(actual_output, desired_output)

    def test_load_next_record(self):
        """Test load_next_record."""
        actual_output = []
        while self.reader.load_next_record():
            uid = self.reader._uid
            main_line_fields = self.reader._main_line_fields
            dep_tiers = self.reader._dependent_tiers
            actual_output.append((uid, main_line_fields, dep_tiers))
        desired_output = [
            (0,
             ('MOT', 'This is the first mainline of MOT .', '', ''),
             {'eng': 'This is the translation'}),
            (1,
             ('CHI', 'This is the first mainline of CHI .', '', ''),
             {'gls': 'This is the gls tier', 'cod': 'This is the cod tier'}),
            (2,
             ('MOT', 'This is the second mainline of MOT .', '', ''),
             {})
        ]
        self.assertEqual(actual_output, desired_output)


class TestACQDIVCHATReaderRead(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        session = (
            '@UTF8\n'
            '@Begin\n'
            '@Date:\t12-SEP-1997\n'
            '@Participants:\tMOT Kim Mother, CHI Daniel Target_Child\n'
            '@ID:\t|English|MOT|||||Mother|||\n'
            '@ID:\t|English|CHI|2;8.|male|||Target_Child|||\n'
            '@Birth of CHI:\t19-FEB-2005\n'
            '@End')
        cls.reader = ACQDIVCHATReader()
        cls.reader.read(io.StringIO(session))

    def test_target_child_set(self):
        """Test whether _target_child is set."""
        actual_output = self.reader._target_child
        desired_output = 'CHI'
        self.assertEqual(actual_output, desired_output)

    def test_metadata_set(self):
        """Test whether _metadata is set."""
        actual_output = self.reader._metadata
        desired_output = {'Date': '12-SEP-1997',
                          'Birth of CHI': '19-FEB-2005'}
        self.assertEqual(actual_output, desired_output)

    def test_speakers_set(self):
        """Test whether _speakers is set."""
        actual_output = self.reader._speakers
        desired_output = {
            'MOT': {
                'id': ('', 'English', 'MOT', '', '', '', '', 'Mother', '', ''),
                'participant': ('MOT', 'Kim', 'Mother')},
            'CHI': {
                'id': ('', 'English', 'CHI', '2;8.', 'male', '', '',
                       'Target_Child', '', ''),
                'participant': ('CHI', 'Daniel', 'Target_Child')}
        }
        self.assertEqual(actual_output, desired_output)

    def test_speaker_iterator_set(self):
        """Test whether _speaker_iterator is set."""
        actual_output = list(self.reader._speaker_iterator)
        desired_output = ['MOT', 'CHI']
        self.assertEqual(actual_output, desired_output)

    def test_record_iterator_set(self):
        actual_output = list(self.reader._record_iterator)
        desired_output = []
        self.assertEqual(actual_output, desired_output)


class TestACQDIVCHATReaderGeneric(unittest.TestCase):
    """Class to test all static and class methods of ACQDIVCHATReader."""

    # ---------- actual & target ----------

    # Test for the get_shortening_actual-method.

    def test_get_shortening_actual_standard_case(self):
        """Test get_shortening_actual with 1 shortening occurence."""
        utterance = 'na:(ra)da <dükäm lan> [?] [>] ?'
        actual_output = ACQDIVCHATReader.get_shortening_actual(utterance)
        desired_output = 'na:da <dükäm lan> [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_multiple_shortenings(self):
        """Test get_shortening_actual with 3 shortening occurence."""
        utterance = '(o)na:(ra)da dükäm lan(da) [?] [>] ?'
        actual_output = ACQDIVCHATReader.get_shortening_actual(utterance)
        desired_output = 'na:da dükäm lan [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_non_shortening_parentheses(self):
        """Test get_shortening_actual with non shortening parentheses."""
        utterance = 'mo:(ra)da (.) mu ?'
        actual_output = ACQDIVCHATReader.get_shortening_actual(utterance)
        desired_output = 'mo:da (.) mu ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_special_characters(self):
        """Test get_shortening_actual with special chars in parentheses."""
        utterance = 'Tu:(ğ)çe .'
        actual_output = ACQDIVCHATReader.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_no_shortening(self):
        """Test get_shortening_actual using utt without shortening."""
        utterance = 'Tu:çe .'
        actual_output = ACQDIVCHATReader.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_empty_string(self):
        """Test get_shortening_actual with an empty string."""
        utterance = 'Tu:çe .'
        actual_output = ACQDIVCHATReader.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    # Test for the get_shortening_target-method.

    def test_get_shortening_target_standard_case(self):
        """Test get_shortening_target with 1 shortening occurence."""
        utterance = 'na:(ra)da <dükäm lan> [?] [>] ?'
        actual_output = ACQDIVCHATReader.get_shortening_target(utterance)
        desired_output = 'na:rada <dükäm lan> [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_multiple_shortenings(self):
        """Test get_shortening_target with 3 shortening occurence."""
        utterance = '(o)na:(ra)da dükäm lan(da) [?] [>] ?'
        actual_output = ACQDIVCHATReader.get_shortening_target(utterance)
        desired_output = 'ona:rada dükäm landa [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_non_shortening_parentheses(self):
        """Test get_shortening_target with non shortening parentheses."""
        utterance = 'mo:(ra)da (.) mu ?'
        actual_output = ACQDIVCHATReader.get_shortening_target(utterance)
        desired_output = 'mo:rada (.) mu ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_special_characters(self):
        """Test get_shortening_target with special chars in parentheses."""
        utterance = 'Mu:(ğ)ça .'
        actual_output = ACQDIVCHATReader.get_shortening_target(utterance)
        desired_output = 'Mu:ğça .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_no_shortening(self):
        """Test get_shortening_target using utt without a shortening."""
        utterance = 'Mu:ça .'
        actual_output = ACQDIVCHATReader.get_shortening_target(utterance)
        desired_output = 'Mu:ça .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_empty_string(self):
        """Test get_shortening_target with an empty string."""
        utterance = ''
        actual_output = ACQDIVCHATReader.get_shortening_target(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_replacement_actual-method.

    def test_get_replacement_actual_one_replacement(self):
        """Test get_replacement_actual with 1 replacement."""
        utterance = 'yarasam [: yorosom] .'
        actual_output = ACQDIVCHATReader.get_replacement_actual(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_multiple_replacements(self):
        """Test get_replacement_actual with 3 replacements."""
        utterance = 'yarasam [: yorosom] yarasam [: yorosom] ' \
                    'yarasam [: yorosom] .'
        actual_output = ACQDIVCHATReader.get_replacement_actual(utterance)
        desired_output = 'yarasam yarasam yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_no_replacement(self):
        """Test get_replacement_actual with no replacement."""
        utterance = 'yarasam .'
        actual_output = ACQDIVCHATReader.get_replacement_actual(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_empty_string(self):
        """Test get_replacement_actual with an empty string."""
        utterance = ''
        actual_output = ACQDIVCHATReader.get_replacement_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_replacement_target-method.

    def test_get_replacement_target_one_replacement(self):
        """Test get_replacement_target with 1 replacement."""
        utterance = 'yarasam [: yorosom] .'
        actual_output = ACQDIVCHATReader.get_replacement_target(utterance)
        desired_output = 'yorosom .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_multiple_replacements(self):
        """Test get_replacement_target with 3 replacements."""
        utterance = 'yarasam [: yorosom] yarasam [: yorosom] ' \
                    'yarasam [: yorosom] .'
        actual_output = ACQDIVCHATReader.get_replacement_target(utterance)
        desired_output = 'yorosom yorosom yorosom .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_no_replacement(self):
        """Test get_replacement_target with no replacement."""
        utterance = 'yarasam .'
        actual_output = ACQDIVCHATReader.get_replacement_target(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_empty_string(self):
        """Test get_replacement_target with an empty string."""
        utterance = ''
        actual_output = ACQDIVCHATReader.get_replacement_target(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_one_by_two(self):
        """Test get_replacement_target with 1 replacement."""
        utterance = 'shoulda [: should have]'
        actual_output = ACQDIVCHATReader.get_replacement_target(utterance)
        desired_output = 'should_have'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_one_by_three(self):
        """Test get_replacement_target with 1 replacement."""
        utterance = 'shouldada [: should have done]'
        actual_output = ACQDIVCHATReader.get_replacement_target(utterance)
        desired_output = 'should_have_done'
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_fragment_actual-method.

    def test_get_fragment_actual_one_fragment(self):
        """Test get_fragment_actual with 1 fragment."""
        utterance = '&ab .'
        actual_output = ACQDIVCHATReader.get_fragment_actual(utterance)
        desired_output = 'ab .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_multiple_fragments(self):
        """Test get_fragment_actual with 3 fragments."""
        utterance = '&ab a &ab b &ab .'
        actual_output = ACQDIVCHATReader.get_fragment_actual(utterance)
        desired_output = 'ab a ab b ab .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_no_fragments(self):
        """Test get_fragment_actual using an utt without fragments."""
        utterance = 'a b .'
        actual_output = ACQDIVCHATReader.get_fragment_actual(utterance)
        desired_output = 'a b .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_empty_string(self):
        """Test get_fragment_actual with an empty string."""
        utterance = ''
        actual_output = ACQDIVCHATReader.get_fragment_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_ampersand_outside(self):
        """Test get_fragment_actual with ampersand outside fragment."""
        utterance = '&=laugh &wow &-um'
        actual_output = ACQDIVCHATReader.get_fragment_actual(utterance)
        desired_output = '&=laugh wow &-um'
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_fragment_target-method.

    def test_get_fragment_target_one_fragment(self):
        """Test get_fragment_target with 1 fragment."""
        utterance = '&ab .'
        actual_output = ACQDIVCHATReader.get_fragment_target(utterance)
        desired_output = 'xxx .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_multiple_fragments(self):
        """Test get_fragment_target with 3 fragments."""
        utterance = '&ab a &ab b &ab .'
        actual_output = ACQDIVCHATReader.get_fragment_target(utterance)
        desired_output = 'xxx a xxx b xxx .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_no_fragments(self):
        """Test get_fragment_target using an utt without fragments."""
        utterance = 'a b .'
        actual_output = ACQDIVCHATReader.get_fragment_target(utterance)
        desired_output = 'a b .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_empty_string(self):
        """Test get_fragment_target with an empty string."""
        utterance = ''
        actual_output = ACQDIVCHATReader.get_fragment_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_ampersand_outside(self):
        """Test get_fragment_target with ampersand outside fragment."""
        utterance = '&=laugh &wow &-um'
        actual_output = ACQDIVCHATReader.get_fragment_target(utterance)
        desired_output = '&=laugh xxx &-um'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_retracing_actual ----------

    def test_get_retracing_actual_retracing(self):
        """Test get_retracing_actual."""
        utterance = 'this is [/] is a test'
        actual_output = ACQDIVCHATReader.get_retracing_actual(utterance)
        desired_output = 'this is is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_retracing_several_words(self):
        """Test get_retracing_actual."""
        utterance = '<this is> [/] this is a test'
        actual_output = ACQDIVCHATReader.get_retracing_actual(utterance)
        desired_output = 'this is this is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_correction(self):
        """Test get_retracing_actual."""
        utterance = 'this us [//] is a test'
        actual_output = ACQDIVCHATReader.get_retracing_actual(utterance)
        desired_output = 'this us is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_correction_several_words(self):
        """Test get_retracing_actual."""
        utterance = '<this us> [//] this is a test'
        actual_output = ACQDIVCHATReader.get_retracing_actual(utterance)
        desired_output = 'this us this is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_reformulation(self):
        """Test get_retracing_actual."""
        utterance = 'what [///] why do you eat'
        actual_output = ACQDIVCHATReader.get_retracing_actual(utterance)
        desired_output = 'what why do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_reformulation_several_words(self):
        """Test get_retracing_actual."""
        utterance = '<for what> [///] why do you eat'
        actual_output = ACQDIVCHATReader.get_retracing_actual(utterance)
        desired_output = 'for what why do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_false_start(self):
        """Test get_retracing_actual."""
        utterance = 'I want [/-] would do that'
        actual_output = ACQDIVCHATReader.get_retracing_actual(utterance)
        desired_output = 'I want would do that'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_actual_false_start_several_words(self):
        """Test get_retracing_actual."""
        utterance = '<I want> [///] what do you eat'
        actual_output = ACQDIVCHATReader.get_retracing_actual(utterance)
        desired_output = 'I want what do you eat'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_retracing_target ----------

    def test_get_retracing_target_retracing(self):
        """Test get_retracing_target."""
        utterance = 'this is [/] is a test'
        actual_output = ACQDIVCHATReader.get_retracing_target(utterance)
        desired_output = 'this is is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_retracing_several_words(self):
        """Test get_retracing_target."""
        utterance = '<this is> [/] this is a test'
        actual_output = ACQDIVCHATReader.get_retracing_target(utterance)
        desired_output = 'this is this is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_correction(self):
        """Test get_retracing_target."""
        utterance = 'this us [//] is a test'
        actual_output = ACQDIVCHATReader.get_retracing_target(utterance)
        desired_output = 'this is is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_correction_several_words(self):
        """Test get_retracing_target."""
        utterance = '<this us> [//] this is a test'
        actual_output = ACQDIVCHATReader.get_retracing_target(utterance)
        desired_output = 'this us this is a test'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_reformulation(self):
        """Test get_retracing_target."""
        utterance = 'what [///] why do you eat'
        actual_output = ACQDIVCHATReader.get_retracing_target(utterance)
        desired_output = 'what why do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_reformulation_several_words(self):
        """Test get_retracing_target."""
        utterance = '<for what> [///] why do you eat'
        actual_output = ACQDIVCHATReader.get_retracing_target(utterance)
        desired_output = 'for what why do you eat'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_false_start(self):
        """Test get_retracing_target."""
        utterance = 'I want [/-] would do that'
        actual_output = ACQDIVCHATReader.get_retracing_target(utterance)
        desired_output = 'I want would do that'
        self.assertEqual(actual_output, desired_output)

    def test_get_retracing_target_false_start_several_words(self):
        """Test get_retracing_target."""
        utterance = '<I want> [///] what do you eat'
        actual_output = ACQDIVCHATReader.get_retracing_target(utterance)
        desired_output = 'I want what do you eat'
        self.assertEqual(actual_output, desired_output)

    # ---------- to_actual_utterance ----------

    def test_to_actual_utterance_empty_string(self):
        utterance = ''
        actual_output = ACQDIVCHATReader.to_actual_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_no_occurrences(self):
        """Test get_actual_utterance using an utt without occurrences."""
        utterance = 'mu:ça yarasam ab yarasam ac'
        actual_output = ACQDIVCHATReader.to_actual_utterance(utterance)
        desired_output = 'mu:ça yarasam ab yarasam ac'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_one_occurence_of_each(self):
        """Test with 1 shortening, 1 fragment and 1 replacement."""
        utterance = 'Mu:(ğ)ça &ab yarasam [: yorosom]'
        actual_output = ACQDIVCHATReader.to_actual_utterance(utterance)
        desired_output = 'Mu:ça ab yarasam'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_multiple_occurences_of_each(self):
        """Test with 2 shortenings, 2 fragments and 2 replacements."""
        utterance = ('(A)mu:(ğ)ça yarasam [: yorosom] '
                     '&ab yarasam [: yorosom] &ac')
        actual_output = ACQDIVCHATReader.to_actual_utterance(utterance)
        desired_output = 'mu:ça yarasam ab yarasam ac'
        self.assertEqual(actual_output, desired_output)

    def test_to_target_utterance_empty_string(self):
        utterance = ''
        actual_output = ACQDIVCHATReader.to_target_utterance(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_to_target_utterance_no_occurrences(self):
        """Test to_target_utterance using an utterance without occurrences."""
        utterance = 'mu:ça yarasam ab yarasam ac'
        actual_output = ACQDIVCHATReader.to_target_utterance(utterance)
        desired_output = 'mu:ça yarasam ab yarasam ac'
        self.assertEqual(actual_output, desired_output)

    def test_to_target_utterance_one_occurrence_of_each(self):
        """Test with 1 shortening, 1 fragment and 1 replacement."""
        utterance = 'Mu:(ğ)ça &ab yarasam [: yorosom]'
        actual_output = ACQDIVCHATReader.to_target_utterance(utterance)
        desired_output = 'Mu:ğça xxx yorosom'
        self.assertEqual(actual_output, desired_output)

    def test_to_target_utterance_multiple_occurrences_of_each(self):
        """Test with 2 shortenings, 2 fragments and 2 replacements."""
        utterance = ('yarasam [: yorosom] '
                     '&ab (a)mu:(ğ)ça  &ac yarasam [: yorosom]')
        actual_output = ACQDIVCHATReader.to_target_utterance(utterance)
        desired_output = 'yorosom xxx amu:ğça  xxx yorosom'
        self.assertEqual(actual_output, desired_output)

    # ---------- morphology ----------

    def test_get_standard_form(self):
        """Test get_standard_form."""
        actual_output = ACQDIVCHATReader.get_standard_form()
        desired_output = 'actual'
        self.assertEqual(actual_output, desired_output)

    def test_get_word_language(self):
        """Test get_word_language."""
        actual_output = ACQDIVCHATReader.get_word_language('dal')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_morpheme_words ----------

    def test_get_morpheme_words(self):
        """Test get_morpheme_words."""
        mor_tier = 'This is an example'
        actual_output = ACQDIVCHATReader.get_morpheme_words(mor_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_multiple_whitespaces(self):
        """Test get_morpheme_words."""
        mor_tier = 'This  is   an example'
        actual_output = ACQDIVCHATReader.get_morpheme_words(mor_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_words(self):
        """Test get_seg_words."""
        seg_tier = 'This is an example'
        actual_output = ACQDIVCHATReader.get_seg_words(seg_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_words(self):
        """Test get_gloss_words."""
        gloss_tier = 'This is an example'
        actual_output = ACQDIVCHATReader.get_gloss_words(gloss_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_words(self):
        """Test get_pos_words."""
        pos_tier = 'This is an example'
        actual_output = ACQDIVCHATReader.get_seg_words(pos_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_main_morpheme(self):
        """Test get_main_morpheme."""
        actual_output = ACQDIVCHATReader.get_main_morpheme()
        desired_output = 'gloss'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language(self):
        """Test get_morpheme_language. Should return an empty string."""
        seg = 'Hatschi'
        gloss = 'sneeze'
        pos = 'N'
        actual_output = ACQDIVCHATReader.get_morpheme_language(seg, gloss, pos)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes(self):
        """Test get_morphemes."""
        seg_word = 'mor1-mor2-mor3'
        actual_output = ACQDIVCHATReader.get_morphemes(seg_word)
        desired_output = ['mor1', 'mor2', 'mor3']
        return self.assertEqual(actual_output, desired_output)

    def test_get_segments(self):
        """Test get_segments."""
        seg_word = 'mor1-mor2-mor3'
        actual_output = ACQDIVCHATReader.get_segments(seg_word)
        desired_output = ['mor1', 'mor2', 'mor3']
        return self.assertEqual(actual_output, desired_output)

    def test_get_glosses(self):
        """Test get_glosses."""
        gloss_word = 'mor1-mor2-mor3'
        actual_output = ACQDIVCHATReader.get_glosses(gloss_word)
        desired_output = ['mor1', 'mor2', 'mor3']
        return self.assertEqual(actual_output, desired_output)

    def test_get_poses(self):
        """Test get_poses."""
        pos_word = 'mor1-mor2-mor3'
        actual_output = ACQDIVCHATReader.get_poses(pos_word)
        desired_output = ['mor1', 'mor2', 'mor3']
        return self.assertEqual(actual_output, desired_output)

###############################################################################


class TestEnglishManchester1ReaderGeneric(unittest.TestCase):

    # ---------- get_word_language ----------

    def test_get_word_language_english(self):
        word = 'yes'
        actual_output = EnglishManchester1Reader.get_word_language(word)
        desired_output = 'English'
        self.assertEqual(actual_output, desired_output)

    def test_get_word_language_french(self):
        word = 'oui@s:fra'
        actual_output = EnglishManchester1Reader.get_word_language(word)
        desired_output = 'French'
        self.assertEqual(actual_output, desired_output)

    def test_get_word_language_italian(self):
        word = 'si@s:ita'
        actual_output = EnglishManchester1Reader.get_word_language(word)
        desired_output = 'Italian'
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_morphemes ----------

    def test_iter_morphemes_stem_no_gloss(self):
        """Test iter_morphemes with stem and no gloss."""
        word = 'stem:POS|stem&FUS'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stem&FUS', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_stem_gloss(self):
        """Test iter_morphemes with stem and gloss."""
        word = 'stem:POS|stem&FUS=stemgloss'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stemgloss', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffixes(self):
        """Test iter_morphemes with suffixes."""
        word = 'stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stem&FUS', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes(self):
        """Test iter_morphemes with prefixes."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('pfxone', 'pfxone', 'pfx'),
                          ('pfxtwo', 'pfxtwo', 'pfx'),
                          ('stem&FUS', 'stem&FUS', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes_suffixes_stemgloss(self):
        """Test iter_morphemes with prefixes, suffixes and stem gloss."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('pfxone', 'pfxone', 'pfx'),
                          ('pfxtwo', 'pfxtwo', 'pfx'),
                          ('stem&FUS', 'stem&FUS', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound(self):
        """Test iter_morphemes with compound."""
        word = 'CMPPOS|+CMPPOSONE|cmpstemone+CMPPOSTWO|cmpstemtwo'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('=cmpstemone', 'cmpstemone', 'CMPPOSONE'),
                          ('=cmpstemtwo', 'cmpstemtwo', 'CMPPOSTWO')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_suffixes(self):
        """Test iter_morphemes with compound and suffixes."""
        word = ('CMPPOS|+CMPPOSONE|cmpstemone-SFXONE'
                '+CMPPOSTWO|cmpstemtwo-SFXTWO')
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('=cmpstemone', 'cmpstemone', 'CMPPOSONE'),
                          ('', 'SFXONE', 'sfx'),
                          ('=cmpstemtwo', 'cmpstemtwo', 'CMPPOSTWO'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_clitic(self):
        """Test iter_morphemes with clitic."""
        word = 'stem:POSone|stem&FUSone~stem:POStwo|stem&FUStwo'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUSone', 'stem&FUSone', 'stem:POSone'),
                          ('stem&FUStwo', 'stem&FUStwo', 'stem:POStwo')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_clitic_suffix(self):
        """Test iter_morphemes with clitic and suffix."""
        word = 'stem:POSone|stem&FUSone-SFX~stem:POStwo|stem&FUStwo'
        actual_output = list(EnglishManchester1Reader.iter_morphemes(word))
        desired_output = [('stem&FUSone', 'stem&FUSone', 'stem:POSone'),
                          ('', 'SFX', 'sfx'),
                          ('stem&FUStwo', 'stem&FUStwo', 'stem:POStwo')]
        self.assertEqual(actual_output, desired_output)

    # ---------- get_morpheme_language ----------

    def test_get_morpheme_languageEnglish(self):
        """Test get_morpheme_language with English."""
        seg = ''
        gloss = ''
        pos = 'N'
        actual_output = EnglishManchester1Reader.get_morpheme_language(
            seg, gloss, pos)
        desired_output = 'English'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_languageL2(self):
        """Test get_morpheme_language with L2."""
        seg = ''
        gloss = ''
        pos = 'L2'
        actual_output = EnglishManchester1Reader.get_morpheme_language(
            seg, gloss, pos)
        desired_output = 'L2'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_segments ----------

    def test_get_segments(self):
        """Test get_segments."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = EnglishManchester1Reader.get_segments(word)
        desired_output = ['pfxone', 'pfxtwo', 'stem&FUS', '', '']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_glosses ----------

    def test_get_glosses(self):
        """Test get_glosses."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = EnglishManchester1Reader.get_glosses(word)
        desired_output = ['pfxone', 'pfxtwo', 'stem&FUS', 'SFXONE', 'SFXTWO']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_poses ----------

    def test_get_poses(self):
        """Test get_poses."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = EnglishManchester1Reader.get_poses(word)
        desired_output = ['pfx', 'pfx', 'stem:POS', 'sfx', 'sfx']
        self.assertEqual(actual_output, desired_output)


class TestEnglishManchester1ReaderSpeaker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '@Participants:\tMOT Mother , CHI Anna Target_Child\n'
                   '@ID:\teng|Manchester|MOT||female|||Mother|||\n'
                   '@ID:\teng|Manchester|CHI|1;10.07||||Target_Child|||\n'
                   '@End')
        cls.reader = EnglishManchester1Reader()
        cls.reader.read(io.StringIO(session))
        cls.reader.load_next_speaker()

    def test_get_speaker_name(self):
        """Test get_speaker_name."""
        actual_output = self.reader.get_speaker_name()
        desired_output = 'Mother of Anna'
        self.assertEqual(actual_output, desired_output)


###############################################################################

# TODO: test in the same way as ACQDIVCHATReader

class TestInuktitutReader(unittest.TestCase):
    """Class to test the InuktitutReader."""

    def setUp(self):
        session_file_path = './test.cha'
        self.reader = InuktitutReader()
        with open(session_file_path) as session_file:
            self.reader.read(session_file)
        self.maxDiff = None

    def test_get_start_time_start_time_present(self):
        """Test get_start_time for a case a start time existing."""
        self.reader._dependent_tiers = {
            'utt': 'ha be',
            'tim': '19301'
        }
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
        self.reader._main_line_fields = (
            'CHI',
            'nuutuinnaq [=? nauk tainna] mu:(ğ)ça &ab yarasam [: yorosom] .',
            '',
            ''
        )
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
        self.reader._main_line_fields = (
            'CHI',
            ('&ab mu:(ğ)ça nuutuinnaq [=? nauk tainna] mu:(ğ)ça &ab yarasam '
             '[: yorosom] yarasam [: yorosom] nuutuinnaq [=? nauk tainna] .'),
            '',
            ''
        )
        actual_output = self.reader.get_actual_utterance()
        desired_output = ('ab mu:ça nauk tainna mu:ça ab '
                          'yarasam yarasam nauk tainna .')
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_empty_string(self):
        """Test get_actual_utterance with an empty string."""
        self.reader._main_line_fields = ('CHI', '', '', '')
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
        self.reader._main_line_fields = (
            'CHI',
            'nuutuinnaq [=? nauk tainna] mu:(ğ)ça &ab yarasam [: yorosom] .',
            '',
            ''
        )
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
        self.reader._main_line_fields = (
            'CHI',
            ('&ab mu:(ğ)ça nuutuinnaq [=? nauk tainna] mu:(ğ)ça &ab yarasam '
             '[: yorosom] yarasam [: yorosom] nuutuinnaq [=? nauk tainna] .'),
            '',
            ''
        )
        actual_output = self.reader.get_target_utterance()
        desired_output = ('xxx mu:ğça nuutuinnaq mu:ğça xxx '
                          'yorosom yorosom nuutuinnaq .')
        self.assertEqual(actual_output, desired_output)

    def test_get_target_utterance_empty_string(self):
        """Test get_target_utterance with an empty string."""
        self.reader._main_line_fields = ('CHI', '', '', '')
        actual_output = self.reader.get_target_utterance()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_morph_tier-method.

    def test_get_morph_tier_morph_tier_present(self):
        """Test get_morph_tier with test.cha."""
        self.reader._dependent_tiers = {'xmor': 'test mor tier'}
        actual_output = self.reader.get_morph_tier()
        desired_output = 'test mor tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_morph_tier_morph_tier_absent(self):
        """Test get_morph_tier with test.cha."""
        self.reader._dependent_tiers = {'xmor': ''}
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

###############################################################################


class TestJapaneseMiiProReader(unittest.TestCase):

    # Tests for the iter_morphemes-method.

    def test_iter_morphemes_stem_no_gloss(self):
        """Test iter_morphemes with stem and no gloss."""
        word = 'stem:POS|stem&FUS'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('stem&FUS', '', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_stem_gloss(self):
        """Test iter_morphemes with stem and gloss."""
        word = 'stem:POS|stem&FUS=stemgloss'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stemgloss', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffixes_no_stemgloss(self):
        """Test iter_morphemes with suffixes and no stem gloss."""
        word = 'stem:POS|stem&FUS-SFXONE-SFXTWO'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('stem&FUS', '', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffixes_stemgloss(self):
        """Test iter_morphemes with suffixes and stem gloss."""
        word = 'stem:POS|stem&FUS-SFXONE-SFXTWO=stemgloss'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stemgloss', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffixes_colon(self):
        """Test iter_morphemes with suffix and colon."""
        word = 'stem:POS|stem&FUS-SFXONE:contr-SFXTWO:SFXTWOseg=stemgloss'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('stem&FUS', 'stemgloss', 'stem:POS'),
                          ('', 'SFXONE:contr', 'sfx'),
                          ('SFXTWOseg', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes(self):
        """Test iter_morphemes with prefixes."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS=stemgloss'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('pfxone', '', 'pfx'),
                          ('pfxtwo', '', 'pfx'),
                          ('stem&FUS', 'stemgloss', 'stem:POS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes_suffixes_stemgloss(self):
        """Test iter_morphemes with prefixes, suffixes and stem gloss."""
        word = 'pfxone#pfxtwo#stem:POS|stem&FUS-SFXONE-SFXTWO=stemgloss'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('pfxone', '', 'pfx'),
                          ('pfxtwo', '', 'pfx'),
                          ('stem&FUS', 'stemgloss', 'stem:POS'),
                          ('', 'SFXONE', 'sfx'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_no_gloss(self):
        """Test iter_morphemes with compound and no stem gloss."""
        word = 'CMPPOS|+CMPPOSONE|cmpstemone+CMPPOSTWO|cmpstemtwo'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('=cmpstemone', '', 'CMPPOSONE'),
                          ('=cmpstemtwo', '', 'CMPPOSTWO')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_gloss(self):
        """Test iter_morphemes with compound and stem gloss."""
        word = 'CMPPOS|+CMPPOSONE|cmpstemone+CMPPOSTWO|cmpstemtwo=cmpgloss'
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('=cmpstemone', 'cmpgloss', 'CMPPOSONE'),
                          ('=cmpstemtwo', 'cmpgloss', 'CMPPOSTWO')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_suffixes(self):
        """Test iter_morphemes with compound and suffixes."""
        word = ('CMPPOS|+CMPPOSONE|cmpstemone-SFXONE'
                '+CMPPOSTWO|cmpstemtwo-SFXTWO=cmpgloss')
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('=cmpstemone', 'cmpgloss', 'CMPPOSONE'),
                          ('', 'SFXONE', 'sfx'),
                          ('=cmpstemtwo', 'cmpgloss', 'CMPPOSTWO'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_compound_prefix(self):
        """Test iter_morphemes with compound and prefix."""
        word = ('pfxone#CMPPOS|+CMPPOSONE|cmpstemone-SFXONE'
                '+CMPPOSTWO|cmpstemtwo-SFXTWO=cmpgloss')
        actual_output = list(JapaneseMiiProReader.iter_morphemes(word))
        desired_output = [('pfxone', '', 'pfx'),
                          ('=cmpstemone', 'cmpgloss', 'CMPPOSONE'),
                          ('', 'SFXONE', 'sfx'),
                          ('=cmpstemtwo', 'cmpgloss', 'CMPPOSTWO'),
                          ('', 'SFXTWO', 'sfx')]
        self.assertEqual(actual_output, desired_output)

###############################################################################


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
        """Test get_utterance with standard case of only hyphens."""
        record = ('*CHI:\tplaceholder\n%gls:\ter-e m-ph-e ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader.get_utterance()
        desired_output = 'ere mphe ntho ena .'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance(self):
        """Test get_actual_utterance with standard case of only hyphens."""
        record = ('*CHI:\tplaceholder\n%gls:\ter-e m-ph-e ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader.get_utterance()
        desired_output = 'ere mphe ntho ena .'
        self.assertEqual(actual_output, desired_output)

    def test_get_target_utterance(self):
        """Test get_target_utterance with standard case of only hyphens."""
        record = ('*CHI:\tplaceholder\n%gls:\ter-e m-ph-e ntho ena .\n%cod:'
                  '\tplaceholder\n@End')
        self.reader.read(io.StringIO(record))
        self.reader.load_next_record()
        actual_output = self.reader.get_utterance()
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


###############################################################################


class TestTurkishReader(unittest.TestCase):

    def test_iter_morphemes_no_suffixes(self):
        """Test iter_morphemes with only stem."""
        word = 'STEMPOS|stem'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem', '', 'STEMPOS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_sub_POS(self):
        """Test iter_morphemes with sub POS tag."""
        word = 'STEMPOS:STEMSUBPOS|stem'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem', '', 'STEMPOS:STEMSUBPOS')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_multiple_suffixes(self):
        """Test iter_morphemes with multiple suffixes."""
        word = 'STEMPOS|stem-SFX1-SFX2-SFX3'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem', '', 'STEMPOS'),
                          ('', 'SFX1', 'sfx'),
                          ('', 'SFX2', 'sfx'),
                          ('', 'SFX3', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_suffix_sub_gloss(self):
        """Test iter_morphemes with suffix sub gloss."""
        word = 'STEMPOS|stem-SFX1-SFX2&SUBSFX2-SFX3'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem', '', 'STEMPOS'),
                          ('', 'SFX1', 'sfx'),
                          ('', 'SFX2&SUBSFX2', 'sfx'),
                          ('', 'SFX3', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_underscore(self):
        """Test iter_morphemes with underscore."""
        word = 'STEMPOS|stem1_stem2-SFX'
        actual_output = list(TurkishReader.iter_morphemes(word))
        desired_output = [('stem1_stem2', '', 'STEMPOS'),
                          ('', 'SFX', 'sfx')]
        self.assertEqual(actual_output, desired_output)


###############################################################################

class TestCreeReader(unittest.TestCase):
    """Class to test the CreeReader."""

    @classmethod
    def setUpClass(cls):
        cls.reader = CreeReader()
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
        self.reader.read(io.StringIO(session_str))
        self.reader.load_next_record()
        actual_output = self.reader.get_seg_tier()
        desired_output = '[wo *]'
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_tier_seg_tier_absent(self):
        """Test get_seg_tier with utt not containing a seg_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.reader.read(io.StringIO(session_str))
        self.reader.load_next_record()
        actual_output = self.reader.get_seg_tier()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier_gloss_tier_present(self):
        """Test get_gloss_tier with utt containing gloss_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.reader.read(io.StringIO(session_str))
        self.reader.load_next_record()
        actual_output = self.reader.get_gloss_tier()
        desired_output = '[egg 1]'
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier_gloss_tier_absent(self):
        """Test get_gloss_tier with utt not containing a gloss_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n@End')
        self.reader.read(io.StringIO(session_str))
        self.reader.load_next_record()
        actual_output = self.reader.get_gloss_tier()
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier_pos_tier_present(self):
        """Test get_pos_tier with utt containing pos_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xmortyp:\t[ni pro]\n%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.reader.read(io.StringIO(session_str))
        self.reader.load_next_record()
        actual_output = self.reader.get_pos_tier()
        desired_output = '[ni pro]'
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier_pos_tier_absent(self):
        """Test get_pos_tier with utt not containing a pos_tier."""
        session_str = ('*CHI:\t‹wâu nîyi› . 1198552_1209903\n%pho:\t‹wo ni›'
                       '\n%mod:\t‹ˈwo *›\n%eng:\tegg me\n%xactmor:\t[wo ni]\n'
                       '%xtarmor:\t[wo *]\n%xmormea:\t'
                       '[egg 1]\n@End')
        self.reader.read(io.StringIO(session_str))
        self.reader.load_next_record()
        actual_output = self.reader.get_pos_tier()
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

###############################################################################


class TestYucatecReader(unittest.TestCase):

    # ---------- get_morpheme_words ----------

    def test_get_morpheme_words_no_clitics(self):
        """Test get_morpheme_words with no clitics."""
        morph_tier = 'P|ráʔ P|riʔ P|ruʔ'
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = ['P|ráʔ', 'P|riʔ', 'P|ruʔ']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_multiple_spaces(self):
        """Test get_morpheme_words with multiple spaces."""
        morph_tier = 'P|ráʔ  P|riʔ   P|ruʔ'
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = ['P|ráʔ', 'P|riʔ', 'P|ruʔ']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_empty_string(self):
        """Test get_morpheme_words with empty string."""
        morph_tier = ''
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_proclitic(self):
        """Test get_morpheme_words with a proclitic."""
        morph_tier = 'P|ráʔ P|riʔ P|kiʔ&P|ruʔ'
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = ['P|ráʔ', 'P|riʔ', 'P|kiʔ', 'P|ruʔ']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_postclitic(self):
        """Test get_morpheme_words with a postclitic."""
        morph_tier = 'P|ráʔ P|riʔ P|ruʔ+P|kuʔ'
        actual_output = YucatecReader.get_morpheme_words(morph_tier)
        desired_output = ['P|ráʔ', 'P|riʔ', 'P|ruʔ', 'P|kuʔ']
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_morphemes ----------

    def test_iter_morphemes_completely_unstructured(self):
        """Test iter_morphemes with completely unstructured word."""
        word = 'mone-mtwo-mthree'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('mone', '', ''),
                          ('mtwo', '', ''),
                          ('mthree', '', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_prefixes(self):
        """Test iter_morphemes with structured prefixes."""
        word = 'PFXGLOSS1|pfxone#PFXGLOSS2|pfxtwo#N|stem'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('pfxone', 'PFXGLOSS1', 'pfx'),
                          ('pfxtwo', 'PFXGLOSS2', 'pfx'),
                          ('stem', '', 'N')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_stem_with_pos(self):
        """Test iter_morphemes with structured stem with POS tag."""
        word = 'N|stem'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'N')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_stem_with_gloss(self):
        """Test iter_morphemes with structured stem only with gloss."""
        word = 'STEMPOS|stem'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', 'STEMPOS', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_unstructured_stem_with_seg(self):
        """Test iter_morphemes with unstructured stem with segment."""
        word = 'stem'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_unstructured_stem_with_gloss(self):
        """Test iter_morphemes with unstructured stem with segment."""
        word = 'STEMGLOSS1'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('', 'STEMGLOSS1', '')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_suffixes(self):
        """Test iter_morphemes with structured suffixes."""
        word = 'N|stem:SFXGLOSS1|-sfxone:SFXGLOSS2|-sfxtwo'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'N'),
                          ('sfxone', 'SFXGLOSS1', 'sfx'),
                          ('sfxtwo', 'SFXGLOSS2', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_structured_suffixes_without_dash(self):
        """Test iter_morphemes with structured suffixes without dash."""
        word = 'N|stem:SFXGLOSS1|sfxone:SFXGLOSS2|sfxtwo'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'N'),
                          ('sfxone', 'SFXGLOSS1', 'sfx'),
                          ('sfxtwo', 'SFXGLOSS2', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_unstructured_suffixes(self):
        """Test iter_morphemes with unstructured suffixes."""
        word = 'N|stem-SFX1-SFX2'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('stem', '', 'N'),
                          ('', 'SFX1', 'sfx'),
                          ('', 'SFX2', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_prefixes_suffixes(self):
        """Test iter_morphemes with prefixes and suffixes."""
        word = ('PFXGLOSS1|pfxone#PFXGLOSS2|pfxtwo#'
                'N|stem'
                ':SFXGLOSS1|-sfxone:SFXGLOSS2|-sfxtwo')
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('pfxone', 'PFXGLOSS1', 'pfx'),
                          ('pfxtwo', 'PFXGLOSS2', 'pfx'),
                          ('stem', '', 'N'),
                          ('sfxone', 'SFXGLOSS1', 'sfx'),
                          ('sfxtwo', 'SFXGLOSS2', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_subpos_subgloss(self):
        """Test iter_morphemes with sub POS tag and sub glosses."""
        word = ('PFXGLOSS:PFXSUBGLOSS|pfx#'
                'N:PROP|stem'
                ':SFXGLOSS:SFXSUBGLOSS|-sfx')
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('pfx', 'PFXGLOSS:PFXSUBGLOSS', 'pfx'),
                          ('stem', '', 'N:PROP'),
                          ('sfx', 'SFXGLOSS:SFXSUBGLOSS', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_iter_morphemes_untranscribed(self):
        """Test iter_morphemes with untranscribed morpheme."""
        word = 'xxx'
        actual_output = list(YucatecReader.iter_morphemes(word))
        desired_output = [('', '', '')]
        self.assertEqual(actual_output, desired_output)

###############################################################################


class TestNungonReader(unittest.TestCase):

    # ---------- get_morpheme_words ----------

    def test_get_morpheme_words_blank_spaces(self):
        """Test get_morpheme_words with blank spaces."""
        morph_tier = 'This is a test'
        actual_output = NungonReader.get_morpheme_words(morph_tier)
        desired_output = ['This', 'is', 'a', 'test']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_multiple_whitespaces(self):
        """Test get_morpheme_words with multiple whitespaces."""
        morph_tier = 'This   is  a  test'
        actual_output = NungonReader.get_morpheme_words(morph_tier)
        desired_output = ['This', 'is', 'a', 'test']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_clitics(self):
        """Test get_morpheme_words with clitics."""
        morph_tier = 'This=is a=test'
        actual_output = NungonReader.get_morpheme_words(morph_tier)
        desired_output = ['This', 'is', 'a', 'test']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_clitics_empty_string(self):
        """Test get_morpheme_words with empty string."""
        morph_tier = ''
        actual_output = NungonReader.get_morpheme_words(morph_tier)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    # ---------- get_segments ----------

    def test_get_segments(self):
        """Test get_segments."""
        seg_word = 'one-two-three-four'
        actual_output = NungonReader.get_segments(seg_word)
        desired_output = ['one', 'two', 'three', 'four']
        self.assertEqual(actual_output, desired_output)

    def test_get_segments_empty_string(self):
        """Test get_segments with empty string."""
        seg_word = ''
        actual_output = NungonReader.get_segments(seg_word)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_gloss_pos ----------

    def test_get_iter_gloss_pos_only_stem(self):
        """Test iter_gloss_pos with only stem."""
        word = 'stempos^stemgloss'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('stemgloss', 'stempos')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_suffixes(self):
        """Test iter_gloss_pos with suffixes."""
        word = 'stempos^stemgloss-sfx1-sfx2.fs'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('stemgloss', 'stempos'),
                          ('sfx1', 'sfx'),
                          ('sfx2.fs', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_prefixes(self):
        """Test iter_gloss_pos with prefixes."""
        word = 'pfx1-pfx2.fs-stempos^stemgloss'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('pfx1', 'pfx'),
                          ('pfx2.fs', 'pfx'),
                          ('stemgloss', 'stempos')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_prefixes_suffixes(self):
        """Test iter_gloss_pos with prefixes and suffixes."""
        word = 'pfx1-pfx2.fs-stempos^stemgloss-sfx1-sfx2.fs'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('pfx1', 'pfx'),
                          ('pfx2.fs', 'pfx'),
                          ('stemgloss', 'stempos'),
                          ('sfx1', 'sfx'),
                          ('sfx2.fs', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_no_stem_one_morpheme(self):
        """Test iter_gloss_pos with one morpheme and no stem marker."""
        word = 'gloss'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('gloss', '')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_no_stem_multiple_morphemes(self):
        """Test iter_gloss_pos with multiple morphemes and no stem marker."""
        word = 'gloss1.fs-gloss2-gloss3'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('gloss1.fs', ''), ('gloss2', ''), ('gloss3', '')]
        self.assertEqual(actual_output, desired_output)

    def test_get_iter_gloss_pos_multiple_carets(self):
        """Test iter_gloss_pos with multiple carets."""
        word = 'n^v^stem-sfx'
        actual_output = list(NungonReader.iter_gloss_pos(word))
        desired_output = [('stem', 'n^v'), ('sfx', 'sfx')]
        self.assertEqual(actual_output, desired_output)

    # ---------- get_glosses ----------

    def test_get_glosses(self):
        """Test get_glosses."""
        word = 'pfx1-pfx2.fs-stempos^stemgloss-sfx1-sfx2.fs'
        actual_output = NungonReader.get_glosses(word)
        desired_output = ['pfx1', 'pfx2.fs', 'stemgloss', 'sfx1', 'sfx2.fs']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_poses ----------

    def test_get_poses(self):
        """Test get_poses."""
        word = 'pfx1-pfx2.fs-stempos^stemgloss-sfx1-sfx2.fs'
        actual_output = NungonReader.get_poses(word)
        desired_output = ['pfx', 'pfx', 'stempos', 'sfx', 'sfx']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_morpheme_language ----------

    def test_get_morpheme_language_tok_pisin(self):
        """Test get_morpheme_language with Tok Pisin."""
        seg = ''
        gloss = ''
        pos = 'tpn'
        actual_output = NungonReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'Tok Pisin'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language_english(self):
        """Test get_morpheme_language with English."""
        seg = ''
        gloss = ''
        pos = 'engn'
        actual_output = NungonReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'English'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language_nungon(self):
        """Test get_morpheme_language with Nungon."""
        seg = ''
        gloss = ''
        pos = 'n'
        actual_output = NungonReader.get_morpheme_language(seg, gloss, pos)
        desired_output = 'Nungon'
        self.assertEqual(actual_output, desired_output)


class TestNungonReaderRecord(unittest.TestCase):
    """Test record readers of NungonReader."""

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '*MEM:\t&foo ma(i)nline [: utterance]. \x150_1111\x15\n'
                   '%xgls:\tThis is the segment tier\n'
                   '%xcod:\tThis is the gloss/POS tier\n'
                   '@End')
        cls.reader = NungonReader()
        cls.reader.read(io.StringIO(session))
        cls.reader.load_next_record()

    def test_get_seg_tier(self):
        actual_output = self.reader.get_seg_tier()
        desired_output = 'This is the segment tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_tier(self):
        actual_output = self.reader.get_gloss_tier()
        desired_output = 'This is the gloss/POS tier'
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_tier(self):
        actual_output = self.reader.get_pos_tier()
        desired_output = 'This is the gloss/POS tier'
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
