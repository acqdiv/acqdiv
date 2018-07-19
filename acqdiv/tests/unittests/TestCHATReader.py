import unittest
from acqdiv.parsers.xml.CHATReader import CHATReader

"""The metadata is a combination of hiia.cha (Sesotho), aki20803.ch 
(Japanese Miyata) and made up data to cover more cases. 

For the test to work, make sure to have test.cha in the same directory.
The file is a version of hiia.cha where the metadata is modified and 
most of the records are deleted.
"""


class TestCHATCleaner(unittest.TestCase):
    """Class to test the CHATReader.
    """

    reader = CHATReader()
    path = './test.cha'
    maxDiff = None

    def test_iter_metadata_fields(self):
        """Test iter_metadata_fields with normal intput."""
        actual_output = list(self.reader.iter_metadata_fields('./test.cha'))
        desired_output = ['@Languages:\tsme',
                          '@Participants:\tMEM Mme_Manyili Grandmother , '
                          'CHI Hlobohang Target_Child , '
                          'KAT Katherine_Demuth Investigator',
                          '@ID:\tsme|Sesotho|MEM|||||Grandmother|||',
                          '@ID:\tsme|Sesotho|CHI|2;2.||||Target_Child|||',
                          '@Birth of CHI:\t14-JAN-2006',
                          '@Birth of ADU:\t11-OCT-1974',
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
        """Test get_metadata_field for a field with
        multiple values.
        """
        ptcs_field = '@Participants:\tMEM Mme_Manyili Grandmother , ' \
                     'CHI Hlobohang Target_Child , ' \
                     'KAT Katherine_Demuth Investigator'
        actual_output = self.reader.get_metadata_field(ptcs_field)
        ptcs = 'MEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , ' \
               'KAT Katherine_Demuth Investigator'
        desired_output = ('Participants', ptcs)
        self.assertEqual(actual_output, desired_output)

    def test_get_media_fields_two_fields(self):
        """Test get_media_fields for the case of only
        two fields being in the chat metadata.
        """
        actual_output = self.reader.get_media_fields('h2ab, audio')
        desired_output = ('h2ab', 'audio', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_media_fields_three_fields(self):
        """Test get_media_fields for the case of three
        fields being in the chat metadata.
        """
        input_str = 'h2ab, audio, unknown speaker'
        actual_output = self.reader.get_media_fields(input_str)
        desired_output = ('h2ab', 'audio', 'unknown speaker')
        self.assertEqual(actual_output, desired_output)

    def test_iter_participants(self):
        """Test iter_participants for a normal case.
        """
        ptcs = 'MEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , ' \
               'KAT Katherine_Demuth Investigator'
        actual_output = list(self.reader.iter_participants(ptcs))
        ptcs_list = ['MEM Mme_Manyili Grandmother',
                     'CHI Hlobohang Target_Child',
                     'KAT Katherine_Demuth Investigator']
        desired_output = ptcs_list
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_fields_two_fields(self):
        """Test get_participant_fields for the case of only
        two fields being specified in the chat metadata.
        """
        actual_output = self.reader.get_participant_fields('MEM Grandmother')
        desired_output = ('MEM', '', 'Grandmother')
        self.assertEqual(actual_output, desired_output)

    def test_get_participant_fields_three_fields(self):
        """Test get_participant_fields for the case of three
        fields being specified in the chat metadata.
        """
        ptcs_field = 'CHI Hlobohang Target_Child'
        actual_output = self.reader.get_participant_fields(ptcs_field)
        desired_output = ('CHI', 'Hlobohang', 'Target_Child')
        self.assertEqual(actual_output, desired_output)

    def test_get_id_fields_all_empty_fields(self):
        """Test get_id_fields for the case of all fields
        being empty.
        """
        input_str = '||||||||||'
        actual_output = self.reader.get_id_fields(input_str)
        desired_output = ('', '', '', '', '', '', '', '', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_id_fields_some_empty(self):
        """Test get_id_fields for the case of some fields
        being empty and some fields containing information.
        """
        input_str = 'sme|Sesotho|MEM|||||Grandmother|||'
        actual_output = self.reader.get_id_fields(input_str)
        desired_output = ('sme', 'Sesotho', 'MEM', '', '', '',
                          '', 'Grandmother', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_replace_line_breaks_single(self):
        """Test replace_line_breaks for the standart case
        of only one line break at a time.
        """
        input_str = 'n^name ij\n\tsm2s-t^p_v^leave-m^s.'
        actual_output = self.reader._replace_line_breaks(input_str)
        desired_output = 'n^name ij sm2s-t^p_v^leave-m^s.'
        self.assertEqual(actual_output, desired_output)

    def test_replace_line_breaks_multiple(self):
        """Test replace_line_breaks for the case of
        two following linebreaks.
        """
        input_str = 'n^name ij sm2s-t^p_v^leave-m^s n^name\n\t' \
                    'sm1-t^p-v^play-m^s pr house(9 , 10/6)/lc ' \
                    'sm1-t^p-v^chat-m^s\n\tcj n^name .'
        actual_output = self.reader._replace_line_breaks(input_str)
        desired_output = 'n^name ij sm2s-t^p_v^leave-m^s n^name ' \
                         'sm1-t^p-v^play-m^s pr house(9 , 10/6)/lc ' \
                         'sm1-t^p-v^chat-m^s cj n^name .'
        self.assertEqual(actual_output, desired_output)

    def test_iter_records(self):
        """Test iter_records for the standart case of
        multiple records.
        """
        actual_output = list(self.reader.iter_records('./test.cha'))
        desired_output = ['*KAT:\tke eng ? 0_8551\n%gls:\tke eng ?\n%cod:\t'
                          'cp wh ?\n%eng:\tWhat is it ?\n%sit:\tPoints to '
                          'tape\n',
                          '*CHI:\tke ntencha ncha . 8551_19738\n'
                          '%gls:\tke ntho e-ncha .\n%cod:\tcp thing(9 , 10) '
                          '9-aj .\n%eng:\tA new thing\n',
                          '*KAT:\tke eng ntho ena e? 19738_24653\n%gls:\t'
                          'ke eng ntho ena e ?\n%cod:\tcp wh thing(9 , 10) '
                          'd9 ij ?\n%eng:\tWhat is this thing ?\n%sit:\t'
                          'Points to tape\n',
                          '*CHI:\te nte ena . 24300_28048\n%gls:\tke ntho '
                          'ena .\n%cod:\tcp thing(9 , 10) d9 .\n%eng:\t'
                          'It is this thing\n',
                          '*MOL:\tke khomba\nkhomba . 28048_31840\n%gls:	'
                          'kekumbakumba .\n%cod:\tcp tape_recorder(9 , 10) .'
                          '\n%eng:\tIt is a stereo\n']
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_standart_case(self):
        """Test get_mainline for a standart record."""
        record = '*KAT:	ke eng ? 0_8551%gls:	ke eng ?%cod:	cp wh ?' \
                 '%eng:	What is it ?%sit:	Points to tape'
        actual_output = self.reader.get_mainline(record)
        desired_output = '*KAT:	ke eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_star_in_mainline(self):
        """Test get_mainline for a record which contains a
        star somewhere in the mainline.
        """
        record = '*KAT:	ke *eng ? 0_8551%gls:	ke eng ?%cod:	cp wh ?' \
                 '%eng:	What is it ?%sit:	Points to tape'
        actual_output = self.reader.get_mainline(record)
        desired_output = '*KAT:	ke *eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_star_in_dependent_tier(self):
        """Test get_mainline for a record which contains a
        star in a dependent tier.
        """
        record = '*KAT:	ke eng ? 0_8551%gls:	ke eng ?%cod:	cp wh ?' \
                 '%eng:	What *is it ?%sit:	Points to tape'
        actual_output = self.reader.get_mainline(record)
        desired_output = '*KAT:	ke eng ? 0_8551'
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_with_time(self):
        """Test get_mainline_fields for the case
        of there being a timestamp.
        """
        mainline = '*KAT:	ke eng ? 0_8551'
        actual_output = self.reader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ?', '0', '8551')
        self.assertEqual(actual_output, desired_output)

    def test_get_mainline_fields_without_time(self):
        """Test get mainline fields for the case of
        no timestamp being there.
        """
        mainline = '*KAT:	ke eng ntho ena e?'
        actual_output = self.reader.get_mainline_fields(mainline)
        desired_output = ('KAT', 'ke eng ntho ena e?', '', '')
        self.assertEqual(actual_output, desired_output)

    def test_get_utterance_words(self):
        """Test get_utterance_words for standart input."""
        utterance = 'ke eng ntho ena e?'
        actual_output = self.reader.get_utterance_words(utterance)
        desired_output = ['ke', 'eng', 'ntho', 'ena', 'e']
        self.assertEqual(actual_output, desired_output)

    def test_iter_dependent_tiers_standart_case(self):
        """Test iter_dependent_tiers for standart input."""
        record = '*CHI:	ke ntencha ncha . 8551_19738\n%gls:	ke ntho ' \
                 'e-ncha .\n%cod:	cp thing(9 , 10) 9-aj .\n'
        actual_output = list(self.reader.iter_dependent_tiers(record))
        desired_output = ['%gls:	ke ntho e-ncha .',
                          '%cod:	cp thing(9 , 10) 9-aj .',
                          '%eng:	A new thing']
        self.assertEqual(actual_output, desired_output)

    def test_iter_dependent_tiers_with_additional_percent_signs(self):
        """Test iter_dependent_tiers for the case of there being
        an additional percent sign a dependent tier.
        """
        record = '*CHI:	ke ntencha ncha . 8551_19738\n%gls:	ke ntho ' \
                 'e-ncha .\n%cod%:	cp thing(9 , 10) 9-aj .\n' \
                 '%eng:	A new% thing'
        actual_output = list(self.reader.iter_dependent_tiers(record))
        desired_output = ['%gls:	ke ntho e-ncha .',
                          '%cod%:	cp thing(9 , 10) 9-aj .',
                          '%eng:	A new% thing']
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_standart_case(self):
        """Test get_dependent_tier for standart input."""
        dep_tier = '%eng:	A new thing'
        actual_output = self.reader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thing')
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_additional_colon(self):
        """Test get_dependent_tier for input where a
        colon appears in the content of the dependent tier,
        """

        dep_tier = '%eng:	A new thi:ng'
        actual_output = self.reader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thi:ng')
        self.assertEqual(actual_output, desired_output)

    def test_get_dependent_tier_additional_percent(self):
        """Test get_dependent_tier for the case of there
        being a percent sign in the dependent tier.
        """
        dep_tier = '%eng:	A new thing%'
        actual_output = self.reader.get_dependent_tier(dep_tier)
        desired_output = ('eng', 'A new thing%')
        self.assertEqual(actual_output, desired_output)


if __name__ == '__main__':
    unittest.main()
