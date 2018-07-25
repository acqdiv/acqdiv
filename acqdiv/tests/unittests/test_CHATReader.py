import unittest
from acqdiv.parsers.xml.CHATReader import CHATReader
from acqdiv.parsers.xml.CHATReader import ACQDIVCHATReader

"""The metadata is a combination of hiia.cha (Sesotho), aki20803.ch 
(Japanese Miyata) and made up data to cover more cases. 

For the test to work, make sure to have test.cha in the same directory.
The file is a version of hiia.cha where the metadata is modified and 
most of the records are deleted.
"""


class TestCHATReader(unittest.TestCase):
    """Class to test the CHATReader."""

    @classmethod
    def setUpClass(cls):
        cls.session_file_path = './test.cha'
        cls.reader = CHATReader()
        cls.maxDiff = None

    def test_iter_metadata_fields(self):
        """Test iter_metadata_fields with normal intput."""
        actual_output = list(self.reader.iter_metadata_fields('./test.cha'))
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

    def test_get_metadata_field_normal_field(self):
        """Test get_metadata_field for a normal field."""
        actual_output = self.reader.get_metadata_field('@Languages:\tsme')
        desired_output = ('Languages', 'sme')
        self.assertEqual(actual_output, desired_output)

    def test_get_metadata_field_multi_valued_field(self):
        """Test get_metadata_field for a field with multiple values."""
        ptcs_field = '@Participants:\tMEM Mme_Manyili Grandmother , ' \
                     'CHI Hlobohang Target_Child , ' \
                     'KAT Katherine_Demuth Investigator'
        actual_output = self.reader.get_metadata_field(ptcs_field)
        ptcs = 'MEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , ' \
               'KAT Katherine_Demuth Investigator'
        desired_output = ('Participants', ptcs)
        self.assertEqual(actual_output, desired_output)

    def test_get_media_fields_two_fields(self):
        """Test get_media_fields method for two field input."""
        actual_output = self.reader.get_media_fields('h2ab, audio')
        desired_output = ('h2ab', 'audio', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_media_fields_three_fields(self):
        """Test get_media_fields for three field input."""
        input_str = 'h2ab, audio, unknown speaker'
        actual_output = self.reader.get_media_fields(input_str)
        desired_output = ('h2ab', 'audio', 'unknown speaker')
        self.assertEqual(actual_output, desired_output)

    def test_iter_participants(self):
        """Test iter_participants for a normal case."""
        ptcs = 'MEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , ' \
               'KAT Katherine_Demuth Investigator'
        actual_output = list(self.reader.iter_participants(ptcs))
        ptcs_list = ['MEM Mme_Manyili Grandmother',
                     'CHI Hlobohang Target_Child',
                     'KAT Katherine_Demuth Investigator']
        desired_output = ptcs_list
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_fields_two_fields(self):
        """Test get_participant_fields for two field input."""
        actual_output = self.reader.get_participant_fields('MEM Grandmother')
        desired_output = ('MEM', '', 'Grandmother')
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_fields_three_fields(self):
        """Test get_participant_fields for three field input"""
        ptcs_field = 'CHI Hlobohang Target_Child'
        actual_output = self.reader.get_participant_fields(ptcs_field)
        desired_output = ('CHI', 'Hlobohang', 'Target_Child')
        self.assertEqual(actual_output, desired_output)

    def test_get_id_fields_all_empty_fields(self):
        """Test get_id_fields for the case of all fields being empty."""
        input_str = '||||||||||'
        actual_output = self.reader.get_id_fields(input_str)
        desired_output = ('', '', '', '', '', '', '', '', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_id_fields_some_empty(self):
        """The the get_id_fields-method.

        Test get_id_fields for the case of some fields
        being empty and some fields containing information.
        """
        input_str = 'sme|Sesotho|MEM||female|||Grandmother|||'
        actual_output = self.reader.get_id_fields(input_str)
        desired_output = ('sme', 'Sesotho', 'MEM', '', 'female', '',
                          '', 'Grandmother', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_replace_line_breaks_single(self):
        """Test replace_line_breaks for single line break."""
        input_str = 'n^name ij\n\tsm2s-t^p_v^leave-m^s.'
        actual_output = self.reader._replace_line_breaks(input_str)
        desired_output = 'n^name ij sm2s-t^p_v^leave-m^s.'
        self.assertEqual(actual_output, desired_output)

    def test_replace_line_breaks_multiple(self):
        """Test replace_line_breaks for two following linebreaks."""
        input_str = 'n^name ij sm2s-t^p_v^leave-m^s n^name\n\t' \
                    'sm1-t^p-v^play-m^s pr house(9 , 10/6)/lc ' \
                    'sm1-t^p-v^chat-m^s\n\tcj n^name .'
        actual_output = self.reader._replace_line_breaks(input_str)
        desired_output = 'n^name ij sm2s-t^p_v^leave-m^s n^name ' \
                         'sm1-t^p-v^play-m^s pr house(9 , 10/6)/lc ' \
                         'sm1-t^p-v^chat-m^s cj n^name .'
        self.assertEqual(actual_output, desired_output)

    def test_iter_records(self):
        """Test iter_records for multiple records. (standard case)"""
        actual_output = list(self.reader.iter_records('./test.cha'))
        desired_output = ['*MEM:\tke eng ? 0_8551\n%gls:\tke eng ?\n%cod:\t'
                          'cp wh ?\n%eng:\tWhat is it ?\n%sit:\tPoints to '
                          'tape\n%add:\tCHI\n',
                          '*CHI:\tke ntencha ncha . 8551_19738\n'
                          '%gls:\tke ntho e-ncha .\n%cod:\tcp thing(9 , 10) '
                          '9-aj .\n%eng:\tA new thing\n%com:\ttest comment\n',
                          '*MEM:\tke eng ntho ena e? 19738_24653\n%gls:\t'
                          'ke eng ntho ena e ?\n%cod:\tcp wh thing(9 , 10) '
                          'd9 ij ?\n%eng:\tWhat is this thing ?\n%sit:\t'
                          'Points to tape\n',
                          '*CHI:\te nte ena . 24300_28048\n%gls:\tke ntho '
                          'ena .\n%cod:\tcp thing(9 , 10) d9 .\n%eng:\t'
                          'It is this thing\n',
                          '*MEM:\tke khomba\nkhomba . 28048_31840\n%gls:	'
                          'kekumbakumba .\n%cod:\tcp tape_recorder(9 , 10) .'
                          '\n%eng:\tIt is a stereo']
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_standard_case(self):
        """Test get_mainline for a standard record."""
        record = '*KAT:	ke eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What is it ?\n%sit:	Points to tape'
        actual_output = self.reader.get_mainline(record)
        desired_output = '*KAT:	ke eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_star_in_mainline(self):
        """Test get_mainline with a star in the mainline."""
        record = '*KAT:	ke *eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What is it ?\n%sit:	Points to tape'
        actual_output = self.reader.get_mainline(record)
        desired_output = '*KAT:	ke *eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_star_in_dependent_tier(self):
        """Test get_mainline with a star in the dependent tier."""
        record = '*KAT:	ke eng ? 0_8551\n%gls:	ke eng ?\n%cod:	cp wh ?' \
                 '\n%eng:	What *is it ?\n%sit:	Points to tape'
        actual_output = self.reader.get_mainline(record)
        desired_output = '*KAT:	ke eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_time(self):
        """Test get_mainline_fields for mainline with timestamp."""
        mainline = '*KAT:	ke eng ? 0_8551'
        actual_output = self.reader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_single_postcode(self):
        """Test get_mainline_fields for mainline with postcode."""
        mainline = '*KAT:	ke eng ? [+ neg]'
        actual_output = self.reader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_multiple_postcodes(self):
        """Test get_mainline_fields for mainline with postcodes."""
        mainline = '*KAT:	ke eng ? [+ neg] [+ req]'
        actual_output = self.reader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_multiple_postcodes_and_time(self):
        """Test get_mainline_fields for mainline with postcodes."""
        mainline = '*KAT:	ke eng ? [+ neg] [+ req] 0_8551'
        actual_output = self.reader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_time_and_multiple_postcodes(self):
        """Test get_mainline_fields for mainline with postcodes."""
        mainline = '*KAT:	ke eng ? 0_8551 [+ neg] [+ req]'
        actual_output = self.reader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_without_time(self):
        """Test get mainline fields for mainline without timestamp"""
        mainline = '*KAT:	ke eng ntho ena e?'
        actual_output = self.reader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ntho ena e?', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words(self):
        """Test get_utterance_words for standard input."""
        utterance = 'ke eng ntho ena e?'
        actual_output = self.reader.get_utterance_words(utterance)
        desired_output = ['ke', 'eng', 'ntho', 'ena', 'e?']
        self.assertEqual(actual_output, desired_output)

    def test_iter_dependent_tiers_standard_case(self):
        """Test iter_dependent_tiers for standard input."""
        record = '*CHI:	ke ntencha ncha . 8551_19738\n%gls:	ke ntho ' \
                 'e-ncha .\n%cod:	cp thing(9 , 10) 9-aj .\n' \
                 '%eng:	A new thing'
        actual_output = list(self.reader.iter_dependent_tiers(record))
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
        actual_output = list(self.reader.iter_dependent_tiers(record))
        desired_output = ['%gls:	ke ntho e-ncha .',
                          '%cod%:	cp thing(9 , 10) 9-aj .',
                          '%eng:	A new% thing']
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_standard_case(self):
        """Test get_dependent_tier for standard input."""
        dep_tier = '%eng:	A new thing'
        actual_output = self.reader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thing')
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_additional_colon(self):
        """Test get_dependent_tier with colon.

        Test get_dependent_tier for input where a
        colon appears in the content of the dependent tier,
        """

        dep_tier = '%eng:	A new thi:ng'
        actual_output = self.reader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thi:ng')
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_additional_percent(self):
        """Test get_dependent_tier with percent sign.

        Test get_dependent_tier for the case of there
        being a percent sign in the dependent tier."
        """
        dep_tier = '%eng:	A new thing%'
        actual_output = self.reader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thing%')
        self.assertEqual(actual_output, desired_output)


###############################################################################

class TestACQDIVCHATReader(unittest.TestCase):
    """Class to test the ACQDIVCHATReader."""

    def setUp(self):
        session_file_path = './test.cha'
        self.reader = ACQDIVCHATReader(session_file_path)
        self.maxDiff = None

    def test_get_metadata_fields(self):
        """Test get_metadata_fields with the test.cha-file."""
        actual_output = self.reader.get_metadata_fields()
        desired_output = {
            'Languages': 'sme',
            'Date': '12-SEP-1997',
            'Participants': ('MEM Mme_Manyili Grandmother , '
                             'CHI Hlobohang Target_Child'),
            'ID': {
                'MEM': ('sme', 'Sesotho', 'MEM', '', 'female',
                        '', '', 'Grandmother', '', ''),
                'CHI': ('sme', 'Sesotho', 'CHI', '2;2.',
                        '', '', '', 'Target_Child', '', '')
            },
            'Birth of CHI': '14-JAN-2006',
            'Birth of MEM': '11-OCT-1974',
            'Media': 'h2ab, audio',
            'Comment': (  # 'all snd kana jmor cha ok Wakachi2002; '
                # Since the AQDIVCHATReader in its current state
                # does not need to capture comments, the line
                # above, which tests the case of two comments
                # in the same session metadata is commented out.
                'uses desu and V-masu'),
            'Warning': 'recorded time: 1:00:00',
            'Situation': ('Aki and AMO preparing to look at book , '
                          '"Miichan no otsukai"')
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_session_date(self):
        """Test get_session_date with test.cha. """
        actual_output = self.reader.get_session_date()
        desired_output = '12-SEP-1997'
        self.assertEqual(actual_output, desired_output)

    def test_get_session_filename(self):
        """Test get_session_filename for sessions name of 'test.cha'."""
        actual_output = self.reader.get_session_filename()
        desired_output = 'h2ab'
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_iterator(self):
        """Test get_speaker_iterator for the speakers in 'test.cha'."""
        actual_output = list(self.reader.get_speaker_iterator())
        desired_output = ['MEM Mme_Manyili Grandmother',
                          'CHI Hlobohang Target_Child']
        self.assertEqual(actual_output, desired_output)

    def test_load_next_speaker(self):
        """Test load_next_speaker for the speakers in 'test.cha'"""
        actual_output = []
        while self.reader.load_next_speaker() != 0:
            pf = self.reader._participant_fields
            idf = self.reader._id_fields
            actual_output.append((pf, idf))
        desired_output = [
            (('MEM', 'Mme_Manyili', 'Grandmother'),
             ('sme', 'Sesotho', 'MEM', '', 'female',
              '', '', 'Grandmother', '', '')),
            (('CHI', 'Hlobohang', 'Target_Child'),
             ('sme', 'Sesotho', 'CHI', '2;2.', '',
              '', '', 'Target_Child', '', ''))
        ]
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_age(self):
        actual_output = []
        while self.reader.load_next_speaker() != 0:
            actual_output.append(self.reader.get_speaker_age())
        desired_output = ['', '2;2.']
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_birthdate(self):
        """Test get_speaker_birthdate with test.cha."""
        actual_output = []
        while self.reader.load_next_speaker() != 0:
            speaker_birthdate = self.reader.get_speaker_birthdate()
            actual_output.append(speaker_birthdate)
        desired_output = ['11-OCT-1974', '14-JAN-2006']
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_gender(self):
        """Test get_speaker_gender with test.cha."""
        actual_output = []
        while self.reader.load_next_speaker() != 0:
            actual_output.append(self.reader.get_speaker_gender())
        desired_output = ['female', '']
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_label(self):
        """Test get_speaker_label with test.cha."""
        actual_output = []
        while self.reader.load_next_speaker() != 0:
            actual_output.append(self.reader.get_speaker_label())
        desired_output = ['MEM', 'CHI']
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_language(self):
        """Test get_speaker_language with test.cha."""
        actual_output = []
        while self.reader.load_next_speaker() != 0:
            actual_output.append(self.reader.get_speaker_language())
        desired_output = ['sme', 'sme']
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_name(self):
        """Test get_speaker_name with test.cha."""
        actual_output = []
        while self.reader.load_next_speaker() != 0:
            actual_output.append(self.reader.get_speaker_name())
        desired_output = ['Mme_Manyili', 'Hlobohang']
        self.assertEqual(actual_output, desired_output)

    def test_get_speaker_role(self):
        """Test get_speaker_role with test.cha."""
        actual_output = []
        while self.reader.load_next_speaker() != 0:
            actual_output.append(self.reader.get_speaker_role())
        desired_output = ['Grandmother', 'Target_Child']
        self.assertEqual(actual_output, desired_output)

    def test_get_record_iterator(self):
        """Test get_record_iterator with test.cha."""
        actual_output = list(self.reader.get_record_iterator())
        desired_output = [
            '*MEM:\tke eng ? 0_8551\n%gls:\tke eng ?\n%cod:\tcp '
            'wh ?\n%eng:\tWhat is it ?\n%sit:\tPoints to tape\n%add:\tCHI\n',
            '*CHI:\tke ntencha ncha . 8551_19738\n%gls:\tke ntho '
            'e-ncha .\n%cod:\tcp thing(9 , 10) 9-aj .\n%eng:\tA new thing\n'
            '%com:\ttest comment\n',
            '*MEM:	ke eng ntho ena e? 19738_24653\n%gls:\tke eng ntho ena '
            'e ?\n%cod:\tcp wh thing(9 , 10) d9 ij ?\n%eng:\tWhat is this '
            'thing ?\n%sit:\tPoints to tape\n',
            '*CHI:\te nte ena . 24300_28048\n%gls:\tke ntho ena .\n%cod:'
            '\tcp thing(9 , 10) d9 .\n%eng:\tIt is this thing\n',
            '*MEM:\tke khomba\nkhomba . 28048_31840\n%gls:\tkekumbakumba .'
            '\n%cod:\tcp tape_recorder(9 , 10) .\n%eng:\tIt is a stereo'
        ]
        self.assertEqual(actual_output, desired_output)

    def test_load_next_record(self):
        """Test load_next_record for the records in 'test.cha'

        At the moment the method throws an Error because of a problem
        of the regex on line 302-303 in the CHATReader.
        -> regex on line 301 assumes, that all mainlines have a
        terminator this is not true and can be tested with:
        grep -P '^\*\w{2,3}?:\t((?![.!?]).)*$' */cha/*.cha
        """
        actual_output = []
        while self.reader.load_next_record() != 0:
            uid = self.reader._uid
            main_line_fields = self.reader._main_line_fields
            dep_tiers = self.reader._dependent_tiers
            actual_output.append((uid, main_line_fields, dep_tiers))
        desired_output = [
            (0, ('MEM', 'ke eng ?', '0', '8551'),
             {
                 'gls': 'ke eng ?', 'cod': 'cp wh ?',
                 'eng': 'What is it ?', 'sit':
                 'Points to tape'
             }),
            (1, ('CHI', 'ke ntencha ncha .', '8551', '19738'),
             {
                 'gls': 'ke eng ?', 'cod': 'cp wh ?',
                 'eng': 'What is it ?',
                 'sit': 'Points to tape'
             }),
            (2, ('MEM', 'ke eng ntho ena e?', '19738', '24653'),
             {
                 'gls': 'ke ntho e-ncha .',
                 'cod': 'cp thing(9 , 10) 9-aj .',
                 'eng': 'A new thing',
                 'com': 'test comment'
             }),
            (3, ('CHI', 'e nte ena .', '24300', '28048'),
             {
                 'gls': 'ke eng ntho ena e ?',
                 'cod': 'cp wh thing(9 , 10) d9 ij ?',
                 'eng': 'What is this thing ?', 'sit': 'Points to tape'
             }),
            (4, ('*MEM', 'ke khomba', '', ''),
             {
                 'gls': 'kekumbakumba .',
                 'cod': 'cp tape_recorder(9 , 10) .',
                 'eng': 'It is a stereo'
             })
        ]
        self.assertEqual(actual_output, desired_output)

    def test_get_uid(self):
        """Test get_uid with test.cha."""
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_uid())
        desired_output = ['u0', 'u1', 'u2', 'u3', 'u4']
        self.assertEqual(actual_output, desired_output)

    def test_get_addressee(self):
        """Test get_addressee with test.cha."""
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_addressee())
        desired_output = ['CHI', '', '', '', '']
        self.assertEqual(actual_output, desired_output)

    def test_get_translation(self):
        """Test get_translation with test.cha."""
        actual_output = ['What is it ?', 'A new thing',
                         'What is this thing ?', 'It is this thing',
                         'It is a stereo']
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_translation())
        desired_output = ['CHI', '', '', '', '']
        self.assertEqual(actual_output, desired_output)

    def test_get_comments(self):
        """Test get_comments with test.cha."""
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_translation())
        desired_output = ['', 'test comment', '', '', '']
        self.assertEqual(actual_output, desired_output)

    def test_get_record_speaker_label(self):
        """Test get_record_speaker_label with test.cha."""
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_record_speaker_label())
        desired_output = ['MEM', 'CHI', 'MEM', 'CHI', 'MEM']
        self.assertEqual(actual_output, desired_output)

    def test_get_start_time(self):
        """Test get_start_time with test.cha."""
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_start_time())
        desired_output = ['0', '8551', '19738', '24300', '28048']
        self.assertEqual(actual_output, desired_output)

    def test_get_end_time(self):
        """Test get_end_time with test.cha."""
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_end_time())
        desired_output = ['8551', '19738', '24653', '28048', '31840']
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance(self):
        """Test get_utterance with test.cha."""
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_utterance())
        desired_output = ['ke eng ?', 'ke ntencha ncha .',
                          'ke eng ntho ena e?', 'e nte ena .',
                          'ke khomba']
        self.assertEqual(actual_output, desired_output)

    def test_get_sentence_type_test_dot_cha_utts(self):
        """Test get_sentence_type with test.cha.

        The default type has a period as utterance terminator.
        """
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_sentence_type())
        desired_output = ['question', 'default', 'question',
                          'default', 'unknown']
        # The last utterance has no terminator. This desired_output
        # assumes, that such cases get the sentence type 'unknown'.
        self.assertEqual(actual_output, desired_output)

    # TODO: more test cases for get_sentence type?

    # Test for the get_shortening_actual-method.
    # All examples are modified versions of real utterances.

    def test_get_shortening_actual_standard_case(self):
        """Test get_shortening_actual with 1 shortening occurence."""
        utterance = 'na:(ra)da <dükäm lan> [?] [>] ?'
        actual_output = self.reader.get_shortening_actual(utterance)
        desired_output = 'na:da <dükäm lan> [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_multiple_shortenings(self):
        """Test get_shortening_actual with 3 shortening occurence."""
        utterance = '(o)na:(ra)da dükäm lan(da) [?] [>] ?'
        actual_output = self.reader.get_shortening_actual(utterance)
        desired_output = 'na:da dükäm lan [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_non_shortening_parentheses(self):
        """Test get_shortening_actual with non shortening parentheses."""
        utterance = 'mo:(ra)da (.) mu ?'
        actual_output = self.reader.get_shortening_actual(utterance)
        desired_output = 'mo:da (.) mu ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_special_characters(self):
        """Test get_shortening_actual with special chars in parentheses."""
        utterance = 'Tu:(ğ)çe .'
        actual_output = self.reader.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_no_shortening(self):
        """Test get_shortening_actual using utt without shortening."""
        utterance = 'Tu:çe .'
        actual_output = self.reader.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_actual_empty_string(self):
        """Test get_shortening_actual with an empty string."""
        utterance = 'Tu:çe .'
        actual_output = self.reader.get_shortening_actual(utterance)
        desired_output = 'Tu:çe .'
        self.assertEqual(actual_output, desired_output)

    # Test for the get_shortening_target-method.

    def test_get_shortening_target_standard_case(self):
        """Test get_shortening_target with 1 shortening occurence."""
        utterance = 'na:(ra)da <dükäm lan> [?] [>] ?'
        actual_output = self.reader.get_shortening_target(utterance)
        desired_output = 'na:rada <dükäm lan> [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_multiple_shortenings(self):
        """Test get_shortening_target with 3 shortening occurence."""
        utterance = '(o)na:(ra)da dükäm lan(da) [?] [>] ?'
        actual_output = self.reader.get_shortening_target(utterance)
        desired_output = 'ona:rada dükäm landa [?] [>] ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_non_shortening_parentheses(self):
        """Test get_shortening_target with non shortening parentheses."""
        utterance = 'mo:(ra)da (.) mu ?'
        actual_output = self.reader.get_shortening_target(utterance)
        desired_output = 'mo:rada (.) mu ?'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_special_characters(self):
        """Test get_shortening_target with special chars in parentheses."""
        utterance = 'Mu:(ğ)ça .'
        actual_output = self.reader.get_shortening_target(utterance)
        desired_output = 'Mu:ğça .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_no_shortening(self):
        """Test get_shortening_target using utt without a shortening."""
        utterance = 'Mu:ça .'
        actual_output = self.reader.get_shortening_target(utterance)
        desired_output = 'Mu:ça .'
        self.assertEqual(actual_output, desired_output)

    def test_get_shortening_target_empty_string(self):
        """Test get_shortening_target with an empty string."""
        utterance = ''
        actual_output = self.reader.get_shortening_target(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_replacement_actual-method.

    def test_get_replacement_actual_one_replacement(self):
        """Test get_replacement_actual with 1 replacement."""
        utterance = 'yarasam [: yorosom] .'
        actual_output = self.reader.get_replacement_actual(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_multiple_replacements(self):
        """Test get_replacement_actual with 3 replacements."""
        utterance = 'yarasam [: yorosom] yarasam [: yorosom] ' \
                    'yarasam [: yorosom] .'
        actual_output = self.reader.get_replacement_actual(utterance)
        desired_output = 'yarasam yarasam yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_no_replacement(self):
        """Test get_replacement_actual with no replacement."""
        utterance = 'yarasam .'
        actual_output = self.reader.get_replacement_actual(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_actual_empty_string(self):
        """Test get_replacement_actual with an empty string."""
        utterance = ''
        actual_output = self.reader.get_replacement_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_replacement_target-method.

    def test_get_replacement_target_one_replacement(self):
        """Test get_replacement_target with 1 replacement."""
        utterance = 'yarasam [: yorosom] .'
        actual_output = self.reader.get_replacement_target(utterance)
        desired_output = 'yorosom .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_multiple_replacements(self):
        """Test get_replacement_target with 3 replacements."""
        utterance = 'yarasam [: yorosom] yarasam [: yorosom] ' \
                    'yarasam [: yorosom] .'
        actual_output = self.reader.get_replacement_target(utterance)
        desired_output = 'yorosom yorosom yorosom .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_no_replacement(self):
        """Test get_replacement_target with no replacement."""
        utterance = 'yarasam .'
        actual_output = self.reader.get_replacement_target(utterance)
        desired_output = 'yarasam .'
        self.assertEqual(actual_output, desired_output)

    def test_get_replacement_target_empty_string(self):
        """Test get_replacement_target with an empty string."""
        utterance = ''
        actual_output = self.reader.get_replacement_target(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_fragment_actual-method.

    def test_get_fragment_actual_one_fragment(self):
        """Test get_fragment_actual with 1 fragment."""
        utterance = '&ab .'
        actual_output = self.reader.get_fragment_actual(utterance)
        desired_output = 'ab .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_multiple_fragments(self):
        """Test get_fragment_actual with 3 fragments."""
        utterance = '&ab a &ab b &ab .'
        actual_output = self.reader.get_fragment_actual(utterance)
        desired_output = 'ab a ab b ab .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_no_fragments(self):
        """Test get_fragment_actual using an utt without fragments."""
        utterance = 'a b .'
        actual_output = self.reader.get_fragment_actual(utterance)
        desired_output = 'a b .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_actual_empty_string(self):
        """Test get_fragment_actual with an empty string."""
        utterance = ''
        actual_output = self.reader.get_fragment_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_fragment_target-method.

    def test_get_fragment_target_one_fragment(self):
        """Test get_fragment_target with 1 fragment."""
        utterance = '&ab .'
        actual_output = self.reader.get_fragment_target(utterance)
        desired_output = 'ab .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_multiple_fragments(self):
        """Test get_fragment_target with 3 fragments."""
        utterance = '&ab a &ab b &ab .'
        actual_output = self.reader.get_fragment_target(utterance)
        desired_output = 'ab a ab b ab .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_no_fragments(self):
        """Test get_fragment_target using an utt without fragments."""
        utterance = 'a b .'
        actual_output = self.reader.get_fragment_target(utterance)
        desired_output = 'a b .'
        self.assertEqual(actual_output, desired_output)

    def test_get_fragment_target_empty_string(self):
        """Test get_fragment_target with an empty string."""
        utterance = ''
        actual_output = self.reader.get_fragment_actual(utterance)
        desired_output = ''
        self.assertEqual(actual_output, desired_output)

    # Tests for the get_actual_utterance method.

    def test_get_actual_utterance_test_dot_cha(self):
        """Test get_actual_utterance with test.cha."""
        actual_output = []
        while self.reader.load_next_record() != 0:
            actual_output.append(self.reader.get_actual_utterance())
        desired_output = ['ke eng ?', 'ke ntencha ncha .',
                          'ke eng ntho ena e?', 'e nte ena .',
                          'ke khomba']
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_one_occurence_of_each(self):
        """Test with 1 shortening, 1 fragment and 1 replacement."""
        self.reader._main_line_fields = (
            'CHI',
            'Mu:(ğ)ça &ab yarasam [: yorosom]',
            '',
            ''
        )
        actual_output = self.reader.get_actual_utterance()
        desired_output = 'Mu:ça ab yarasam'
        self.assertEqual(actual_output, desired_output)

    def test_get_actual_utterance_multiple_occurences_of_each(self):
        """Test with 2 shortenings, 2 fragments and 2 replacements."""
        pass

    def test_get_actual_utterance_no_occurences(self):
        """Test get_actual_utterance using an utt without occurences."""
        pass

    def test_get_actual_utterance_empty_string(self):
        """Test get_actual_utterance with an empty string."""
        pass

    # Tests for the get_actual_utterance method.

    def test_get_target_utterance_one_occurence_of_each(self):
        """Test with 1 shortening, 1 fragment and 1 replacement."""
        pass

    def test_get_target_utterance_multiple_occurences_of_each(self):
        """Test with 1 shortening, 1 fragment and 1 replacement."""
        pass

    def test_get_target_utterance_no_occurences(self):
        """Test get_actual_utterance using an utt without occurences."""
        pass

    def test_get_target_utterance_empty_string(self):
        """Test get_target_utterance with an empty string."""
        pass

    # ----------------------------

    def test_get_standard_form(self):
        """Test get_standard_form.

        TODO: What is there to test?
        """
        pass

    def test_get_word_languge(self):
        """Test get_word_language.

        TODO: What is there to test?
        """
        pass


if __name__ == '__main__':
    unittest.main()
