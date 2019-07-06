import unittest
import io
from acqdiv.parsers.chat.readers.RawCHATReader import RawCHATReader
from acqdiv.parsers.chat.readers.BaseCHATReader import BaseCHATReader


class TestCHATReader(unittest.TestCase):
    """Class to test the RawCHATReader."""

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

        actual_output = list(RawCHATReader.iter_metadata_fields(session))
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

        actual_output = list(RawCHATReader.iter_metadata_fields(session))
        desired_output = [('@Participants:\tMEM Mme_Manyili Grandmother , '
                           'CHI Hlobohang Target_Child'),
                          '@Comment:\tHere comes a comment.']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_metadata_field ----------

    def test_get_metadata_field_normal_field(self):
        """Test get_metadata_field for a normal field."""
        actual_output = RawCHATReader.get_metadata_field('@Languages:\tsme')
        desired_output = ('Languages', 'sme')
        self.assertEqual(actual_output, desired_output)

    def test_get_metadata_field_multi_valued_field(self):
        """Test get_metadata_field for a field with multiple values."""
        ptcs_field = '@Participants:\tMEM Mme_Manyili Grandmother , ' \
                     'CHI Hlobohang Target_Child , ' \
                     'KAT Katherine_Demuth Investigator'
        actual_output = RawCHATReader.get_metadata_field(ptcs_field)
        ptcs = 'MEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , ' \
               'KAT Katherine_Demuth Investigator'
        desired_output = ('Participants', ptcs)
        self.assertEqual(actual_output, desired_output)

    # ---------- get_media_fields ----------

    def test_get_media_fields_two_fields(self):
        """Test get_media_fields method for two field input."""
        actual_output = RawCHATReader.get_media_fields('h2ab, audio')
        desired_output = ('h2ab', 'audio', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_media_fields_three_fields(self):
        """Test get_media_fields for three field input."""
        input_str = 'h2ab, audio, unknown speaker'
        actual_output = RawCHATReader.get_media_fields(input_str)
        desired_output = ('h2ab', 'audio', 'unknown speaker')
        self.assertEqual(actual_output, desired_output)

    # ---------- get_media_filename ----------

    def test_get_media_filename(self):
        """Test get_media_filename with standard case of 3 fields."""
        media_fields = ['h2ab', 'video', 'unlinked']
        actual_output = RawCHATReader.get_media_filename(media_fields)
        desired_output = 'h2ab'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_media_format ----------

    def test_get_media_format(self):
        """Test get_media_format with standard case of 3 fields."""
        media_fields = ['h2ab', 'video', 'unlinked']
        actual_output = RawCHATReader.get_media_format(media_fields)
        desired_output = 'video'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_media_comment ----------

    def test_get_media_comment(self):
        """Test get_media_comment with standard case of 3 fields."""
        media_fields = ['h2ab', 'video', 'unlinked']
        actual_output = RawCHATReader.get_media_comment(media_fields)
        desired_output = 'unlinked'
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_participants ----------

    def test_iter_participants(self):
        """Test iter_participants for a normal case."""
        ptcs = 'MEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , ' \
               'KAT Katherine_Demuth Investigator'
        actual_output = list(RawCHATReader.iter_participants(ptcs))
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
        actual_output = list(RawCHATReader.iter_participants(ptcs))
        ptcs_list = ['MEM Mme_Manyili Grandmother',
                     'CHI Hlobohang Target_Child',
                     'KAT Katherine_Demuth Investigator']
        desired_output = ptcs_list
        self.assertEqual(actual_output, desired_output)

    # ---------- get_participant_fields ----------

    def test_get_participant_fields_one_field(self):
        """Test get_participant_fields for one field input."""
        actual_output = RawCHATReader.get_participant_fields('MEM')
        desired_output = ('MEM', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_fields_two_fields(self):
        """Test get_participant_fields for two field input."""
        actual_output = RawCHATReader.get_participant_fields('MEM Grandmother')
        desired_output = ('MEM', '', 'Grandmother')
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_fields_three_fields(self):
        """Test get_participant_fields for three field input"""
        ptcs_field = 'CHI Hlobohang Target_Child'
        actual_output = RawCHATReader.get_participant_fields(ptcs_field)
        desired_output = ('CHI', 'Hlobohang', 'Target_Child')
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_multiple_whitespaces(self):
        """Test with multiple whitespaces"""
        ptcs_field = 'CHI   Sara  Target_Child'
        actual_output = RawCHATReader.get_participant_fields(ptcs_field)
        desired_output = ('CHI', 'Sara', 'Target_Child')
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_fields ----------

    def test_get_id_fields_all_empty_fields(self):
        """Test get_id_fields for the case of all fields being empty."""
        input_str = '||||||||||'
        actual_output = RawCHATReader.get_id_fields(input_str)
        desired_output = ('', '', '', '', '', '', '', '', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_id_fields_some_empty(self):
        """The the get_id_fields-method.

        Test get_id_fields for the case of some fields
        being empty and some fields containing information.
        """
        id_fields = 'sme|Sesotho|MEM||female|||Grandmother|||'
        actual_output = RawCHATReader.get_id_fields(id_fields)
        desired_output = ('sme', 'Sesotho', 'MEM', '', 'female', '',
                          '', 'Grandmother', '', '')
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_language ----------

    def test_get_id_language(self):
        """Test get_id_language with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_language(id_fields)
        desired_output = 'sme'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_corpus ----------

    def test_get_id_corpus(self):
        """Test get_id_corpus with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_corpus(id_fields)
        desired_output = 'Sesotho'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_code ----------

    def test_get_id_code(self):
        """Test get_id_code with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_code(id_fields)
        desired_output = 'MEM'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_age ----------

    def test_get_id_age(self):
        """Test get_id_age with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_age(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_sex ----------

    def test_get_id_sex(self):
        """Test get_id_sex with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_sex(id_fields)
        desired_output = 'female'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_group ----------

    def test_get_id_group(self):
        """Test get_id_group with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_group(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_ses ----------

    def test_get_id_ses(self):
        """Test get_id_ses with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_ses(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_role ----------

    def test_get_id_role(self):
        """Test get_id_role with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_role(id_fields)
        desired_output = 'Grandmother'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_education ----------

    def test_get_id_education(self):
        """Test get_id_education with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_education(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_id_custom ----------

    def test_get_id_custom(self):
        """Test get_id_custom with id-fields of MEM of test.cha."""
        id_fields = ('sme', 'Sesotho', 'MEM', '', 'female', '', '',
                     'Grandmother', '', '')
        actual_output = RawCHATReader.get_id_custom(id_fields)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- replace_line_breaks ----------

    def test_replace_line_breaks_single(self):
        """Test replace_line_breaks for single line break."""
        input_str = 'n^name ij\n\tsm2s-t^p_v^leave-m^s.'
        actual_output = RawCHATReader._replace_line_breaks(input_str)
        desired_output = 'n^name ij sm2s-t^p_v^leave-m^s.'
        self.assertEqual(actual_output, desired_output)

    def test_replace_line_breaks_multiple(self):
        """Test replace_line_breaks for two following linebreaks."""
        input_str = 'n^name ij sm2s-t^p_v^leave-m^s n^name\n\t' \
                    'sm1-t^p-v^play-m^s pr house(9 , 10/6)/lc ' \
                    'sm1-t^p-v^chat-m^s\n\tcj n^name .'
        actual_output = RawCHATReader._replace_line_breaks(input_str)
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
        actual_output = list(RawCHATReader.iter_records(session))
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

    def test_iter_records_line_breaks(self):
        session = ('@UTF8\n@Begin\n@Birth of CHI:\t14-JAN-2006\n'
                   '*MEM:\tke line\n\tbreak . \x1528048_31840\x15\n'
                   '%gls:\tke line\n\tbreak .\n'
                   '@End\n')
        actual_output = list(RawCHATReader.iter_records(session))
        desired_output = [
            '*MEM:\tke line break . \x1528048_31840\x15\n'
            '%gls:\tke line break .'
        ]
        self.assertEqual(actual_output, desired_output)

    # ---------- get_mainline ----------

    def test_get_mainline_standard_case(self):
        """Test get_mainline for a standard record."""
        record = '*KAT:	ke eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What is it ?\n%sit:	Points to tape'
        actual_output = RawCHATReader.get_mainline(record)
        desired_output = '*KAT:	ke eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_star_in_mainline(self):
        """Test get_mainline with a star in the mainline."""
        record = '*KAT:	ke *eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What is it ?\n%sit:	Points to tape'
        actual_output = RawCHATReader.get_mainline(record)
        desired_output = '*KAT:	ke *eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_star_in_dependent_tier(self):
        """Test get_mainline with a star in the dependent tier."""
        record = '*KAT:	ke eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What *is it ?\n%sit:	Points to tape'
        actual_output = RawCHATReader.get_mainline(record)
        desired_output = '*KAT:	ke eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    # ---------- get_mainline_fields ----------

    def test_get_mainline_fields_with_time(self):
        """Test get_mainline_fields for mainline with timestamp."""
        mainline = '*KAT:	ke eng ? 0_8551'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_time_multiple_spaces(self):
        """Test get_mainline_fields with multiple spaces before timestamp.

        Attested in Japanese MiiPro.
        """
        mainline = '*KAT:	ke eng ?  0_8551'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_no_space_before_time(self):
        """Test get_mainline_fields for no space before the timestamp.

        There is no space between the terminator and the timestamp. Such
        examples can be found for example in Japanese_MiiPro.
        """
        mainline = '*KAT:	ke eng ?0_8551'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_single_postcode(self):
        """Test get_mainline_fields for mainline with postcode."""
        mainline = '*KAT:	ke eng ? [+ neg]'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ? [+ neg]', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_multiple_postcodes(self):
        """Test get_mainline_fields for mainline with postcodes."""
        mainline = '*KAT:	ke eng ? [+ neg] [+ req]'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ? [+ neg] [+ req]', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_postcode_multiple_spaces(self):
        """Test get_mainline_fields with multiple spaces before postcode.

        Attested in Japanese MiiPro.
        """
        mainline = '*KAT:	ke eng ?  [+ neg]'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?  [+ neg]', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_no_space_before_postcode(self):
        """Test get_mainline_fields for no space before the postcode.

        There is no space between the terminator and the postcode. Such
        examples can be found for example in Japanese_MiiPro.
        """
        mainline = '*KAT:	ke eng ?[+ neg]'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?[+ neg]', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_multiple_postcodes_and_time(self):
        """Test get_mainline_fields for mainline with postcodes."""
        mainline = '*KAT:	ke eng ? [+ neg] [+ req] 0_8551'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ? [+ neg] [+ req]', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_without_time(self):
        """Test get mainline fields for mainline without timestamp"""
        mainline = '*KAT:	ke eng ntho ena e?'
        actual_output = RawCHATReader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ntho ena e?', '', '')
        self.assertEqual(actual_output, desired_output)

    # ---------- get_utterance_words ----------

    def test_get_utterance_words_standard_case(self):
        """Test get_utterance_words for standard input."""
        utterance = 'ke eng ntho ena e?'
        actual_output = RawCHATReader.get_utterance_words(utterance)
        desired_output = ['ke', 'eng', 'ntho', 'ena', 'e?']
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words_empty_string(self):
        """Test get_utterance_words for standard input."""
        utterance = ''
        actual_output = RawCHATReader.get_utterance_words(utterance)
        desired_output = []
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words_multiple_blank_spaces(self):
        """Test get_utterance_words with multiple blank spaces."""
        utterance = 'ke eng  ntho ena   e?'
        actual_output = RawCHATReader.get_utterance_words(utterance)
        desired_output = ['ke', 'eng', 'ntho', 'ena', 'e?']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_utterance_terminator ----------

    def test_get_utterance_terminator_space_before(self):
        """Test get_utterance_terminator with space before."""
        utterance = 'Das ist ein Test .'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_no_space_before(self):
        """Test get_utterance_terminator with no space before."""
        utterance = 'Das ist ein Test.'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode(self):
        """Test get_utterance_terminator with postcode."""
        utterance = 'Das ist ein Test . [+ postcode]'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode_no_space(self):
        """Test get_utterance_terminator with postcode and no space."""
        utterance = 'Das ist ein Test .[+ postcode]'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_postcode_multiple_spaces(self):
        """Test get_utterance_terminator with postcode and multiple spaces."""
        utterance = 'Das ist ein Test .  [+ postcode]'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_non_terminator_dot(self):
        """Test get_utterance_terminator with a non-terminator dot."""
        utterance = 'Das ist (.) ein Test ? [+ postcode]'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_no_terminator(self):
        """Test get_utterance_terminator with no terminator."""
        utterance = 'Das ist ein Test'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_empty_string(self):
        """Test get_utterance_terminator with empty string."""
        utterance = ''
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_question(self):
        """Test get_utterance_terminator with question mark."""
        utterance = 'this is a test ?'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_exclamation(self):
        """Test get_utterance_terminator with exclamation mark."""
        utterance = 'this is a test !'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '!'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_broken_for_coding(self):
        """Test get_utterance_terminator with broken-for-coding mark."""
        utterance = 'this is a test +.'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_trail_off(self):
        """Test get_utterance_terminator with trail-off mark."""
        utterance = 'this is a test +...'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+...'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_trail_off_of_a_question(self):
        """Test get_utterance_terminator with trail-off-of-a-question mark."""
        utterance = 'this is a test +..?'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+..?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_question_with_exclamation(self):
        """Test get_utterance_terminator with question-exclamation mark."""
        utterance = 'this is a test +!?'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+!?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_interruption(self):
        """Test get_utterance_terminator with interruption mark."""
        utterance = 'this is a test +/.'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+/.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_interruption_of_a_question(self):
        """Test get_utterance_terminator with interruption-question mark."""
        utterance = 'this is a test +/?'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+/?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_self_interruption(self):
        """Test get_utterance_terminator with self-interruption mark."""
        utterance = 'this is a test +//.'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+//.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_self_interrupted_question(self):
        """Test get_utterance_terminator with self-interrupted-question."""
        utterance = 'this is a test +//?'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+//?'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_quotation_follows(self):
        """Test get_utterance_terminator with quotation-follows mark."""
        utterance = 'this is a test +"/.'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+"/.'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_quotation_precedes(self):
        """Test get_utterance_terminator with quotation-precedes mark."""
        utterance = 'this is a test +".'
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '+".'
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_terminator_trailing_whitespace(self):
        """Test get_utterance_terminator with trailing whitespace."""
        utterance = 'Is this a test ? '
        actual_output = RawCHATReader.get_utterance_terminator(utterance)
        desired_output = '?'
        self.assertEqual(actual_output, desired_output)

    # ---------- iter_dependent_tiers ----------

    def test_iter_dependent_tiers_standard_case(self):
        """Test iter_dependent_tiers for standard input."""
        record = '*CHI:	ke ntencha ncha . 8551_19738\n%gls:	ke ntho ' \
                 'e-ncha .\n%cod:	cp thing(9 , 10) 9-aj .\n' \
                 '%eng:	A new thing'
        actual_output = list(RawCHATReader.iter_dependent_tiers(record))
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
        actual_output = list(RawCHATReader.iter_dependent_tiers(record))
        desired_output = ['%gls:	ke ntho e-ncha .',
                          '%cod%:	cp thing(9 , 10) 9-aj .',
                          '%eng:	A new% thing']
        self.assertEqual(actual_output, desired_output)

    # ---------- get_dependent_tier ----------

    def test_get_dependent_tier_standard_case(self):
        """Test get_dependent_tier for standard input."""
        dep_tier = '%eng:	A new thing'
        actual_output = RawCHATReader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thing')
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_additional_colon(self):
        """Test get_dependent_tier with colon.

        Test get_dependent_tier for input where a
        colon appears in the content of the dependent tier,
        """

        dep_tier = '%eng:	A new thi:ng'
        actual_output = RawCHATReader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thi:ng')
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_additional_percent(self):
        """Test get_dependent_tier with percent sign.

        Test get_dependent_tier for the case of there
        being a percent sign in the dependent tier."
        """
        dep_tier = '%eng:	A new thing%'
        actual_output = RawCHATReader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thing%')
        self.assertEqual(actual_output, desired_output)


###############################################################################

class TestACQDIVCHATReaderMetadata(unittest.TestCase):
    """Test metadata readers of BaseCHATReader.

    Excluding speaker metadata.
    """

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '@Date:\t12-SEP-1997\n'
                   '@Media:\tmedia_filename, audio\n'
                   '@End')
        cls.reader = BaseCHATReader()
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
    """Test speaker readers of BaseCHATReader."""

    @classmethod
    def setUpClass(cls):
        session = ('@UTF8\n'
                   '@Begin\n'
                   '@Participants:\tCHI Hlobohang Target_Child\n'
                   '@ID:\tsme|Sesotho|CHI|2;2.||||Target_Child|||\n'
                   '@Birth of CHI:\t14-JAN-2006\n'
                   '@End')
        cls.reader = BaseCHATReader()
        cls.reader.read(io.StringIO(session))
        cls.reader.load_next_speaker()

    def test_get_target_child(self):
        actual_output = self.reader.get_target_child()
        desired_output = ('CHI', 'Hlobohang')
        self.assertEqual(actual_output, desired_output)

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
    """Test record readers of BaseCHATReader."""

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
        cls.reader = BaseCHATReader()
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
    """Test iterator methods of BaseCHATReader."""

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
        cls.reader = BaseCHATReader()
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
        cls.reader = BaseCHATReader()
        cls.reader.read(io.StringIO(session))

    def test_target_child_set(self):
        """Test whether _target_child is set."""
        actual_output = self.reader._target_child
        desired_output = ('CHI', 'Daniel')
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
    """Class to test all static and class methods of BaseCHATReader."""

    # ---------- morphology ----------

    def test_get_standard_form(self):
        """Test get_standard_form."""
        actual_output = BaseCHATReader.get_standard_form()
        desired_output = 'actual'
        self.assertEqual(actual_output, desired_output)

    def test_get_word_language(self):
        """Test get_word_language."""
        actual_output = BaseCHATReader.get_word_language('dal')
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # ---------- get_morpheme_words ----------

    def test_get_morpheme_words(self):
        """Test get_morpheme_words."""
        mor_tier = 'This is an example'
        actual_output = BaseCHATReader.get_morpheme_words(mor_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_words_multiple_whitespaces(self):
        """Test get_morpheme_words."""
        mor_tier = 'This  is   an example'
        actual_output = BaseCHATReader.get_morpheme_words(mor_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_seg_words(self):
        """Test get_seg_words."""
        seg_tier = 'This is an example'
        actual_output = BaseCHATReader.get_seg_words(seg_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_gloss_words(self):
        """Test get_gloss_words."""
        gloss_tier = 'This is an example'
        actual_output = BaseCHATReader.get_gloss_words(gloss_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_pos_words(self):
        """Test get_pos_words."""
        pos_tier = 'This is an example'
        actual_output = BaseCHATReader.get_seg_words(pos_tier)
        desired_output = ['This', 'is', 'an', 'example']
        self.assertEqual(actual_output, desired_output)

    def test_get_main_morpheme(self):
        """Test get_main_morpheme."""
        actual_output = BaseCHATReader.get_main_morpheme()
        desired_output = 'gloss'
        self.assertEqual(actual_output, desired_output)

    def test_get_morpheme_language(self):
        """Test get_morpheme_language. Should return an empty string."""
        seg = 'Hatschi'
        gloss = 'sneeze'
        pos = 'N'
        actual_output = BaseCHATReader.get_morpheme_language(seg, gloss, pos)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    def test_get_morphemes(self):
        """Test get_morphemes."""
        seg_word = 'mor1-mor2-mor3'
        actual_output = BaseCHATReader.get_morphemes(seg_word)
        desired_output = ['mor1', 'mor2', 'mor3']
        return self.assertEqual(actual_output, desired_output)

    def test_get_segments(self):
        """Test get_segments."""
        seg_word = 'mor1-mor2-mor3'
        actual_output = BaseCHATReader.get_segments(seg_word)
        desired_output = ['mor1', 'mor2', 'mor3']
        return self.assertEqual(actual_output, desired_output)

    def test_get_glosses(self):
        """Test get_glosses."""
        gloss_word = 'mor1-mor2-mor3'
        actual_output = BaseCHATReader.get_glosses(gloss_word)
        desired_output = ['mor1', 'mor2', 'mor3']
        return self.assertEqual(actual_output, desired_output)

    def test_get_poses(self):
        """Test get_poses."""
        pos_word = 'mor1-mor2-mor3'
        actual_output = BaseCHATReader.get_poses(pos_word)
        desired_output = ['mor1', 'mor2', 'mor3']
        return self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
