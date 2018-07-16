import unittest
from acqdiv.parsers.xml.CHATReader import CHATReader


"""The metadata is a combination of hiia.cha (Sesotho), aki20803.ch 
(Japanese_Miyata) and made up data to cover more cases. 

For the test to work, make sure to have test.cha in the same directory.
The file is a version of hiia.cha where the metadata is modified.
"""

# pep8 not possible to avoid unwanted line breaks in string
metadata = """@Languages:\tsme
@Participants:\tMEM Mme_Manyili Grandmother , CHI Hlobohang Target_Child , KAT Katherine_Demuth Investigator , MHL Mahlobohang Mother , MOL Mololo Cousin
@ID:\tsme|Sesotho|MEM|||||Grandmother|||
@ID:\tsme|Sesotho|CHI|2;2.||||Target_Child|||
@ID:\tsme|Sesotho|KAT|||||Investigator|||
@ID:\tsme|Sesotho|MHL|||||Mother|||
@ID:\tsme|Sesotho|MOL|4;6.||||Cousin|||
@Birth of CHI:\t14-JAN-2006
@Birth of ADU:\t11-OCT-1974
@Birth of BOY:\t25-JAN-1991
@Media:\th2ab, audio
@Comment:\tGem 4'25" - 64'25"; Overall time 75'00 all snd kana jmor cha ok Wakachi2002; JMOR04.1 Note: if main line and ort tier differ , the main line is the correct one
@Warning:\trecorded time: 1:00:00
@Comment:\tuses desu and V-masu
@Situation:\tAki and AMO preparing to look at book , "Miichan no otsukai"
"""
languages = 'sme'
ptcs = 'MEM Mme_Manyili Grandmother\nCHI Hlobohang Target_Child\nKAT Katherine_Demuth Investigator\nMHL Mahlobohang Mother\nMOL Mololo Cousin'
ids = """sme|Sesotho|MEM|||||Grandmother|||
sme|Sesotho|CHI|2;2.||||Target_Child|||
sme|Sesotho|KAT|||||Investigator|||
sme|Sesotho|MHL|||||Mother|||
sme|Sesotho|MOL|4;6.||||Cousin|||"""
birth_of_x = """14-JAN-2006\n11-OCT-1974\n25-JAN-1991"""
media = 'h2ab, audio'
comment = """Gem 4'25" - 64'25"; Overall time 75'00 all snd kana jmor cha ok Wakachi2002; JMOR04.1 Note: if main line and ort tier differ , the main line is the correct one
uses desu and V-masu"""
warning = 'recorded time: 1:00:00'
situation = 'Aki and AMO preparing to look at book , "Miichan no otsukai"'


class TestCHATCleaner(unittest.TestCase):
    """
    Class to test the CHATReader.

    Before executing this test, copy the file 09-A1-2005-10-17.cha 
    into acqdiv/corpora/Cree/.
    """

    reader = CHATReader()
    path = './test.cha'
    maxDiff = None

    def test_get_uid_correct_format(self):
        """Test for the get_uid-method.

        Test if ids have correct format.
        """
        ids_list = [self.reader.get_uid()
                    for rec in CHATReader.iter_records(self.path)]
        for id_ in ids_list:
            char = id_[0]
            num = int(id_[1:])
            self.assertEqual(id_, 'u'+str(num))

    def test_get_uid_unique(self):
        """Test for the get_uid-method.

        Test for uniqueness of ids.
        """

        ids_list = [self.reader.get_uid()
                    for rec in CHATReader.iter_records(self.path)]
        ids_set = set(ids_list)
        self.assertEqual(len(ids_list), len(ids_set))

    def test_get_metadata(self):
        """Test for the get_metadata-method.

        It is assumed, that only the lines after "@BEGIN" are extracted.
        It is assumed, that the entire lines are always extracted 
        (meaning, that the last line still has a newline character).
        """
        self.assertEqual(self.reader.get_metadata(self.path), metadata)

    def test_get_metadata_field_languages(self):
        """Test for the get_metadata_field-method.

        Test languages.
        It is assumed that whitespace-characters at the 
        beginning and at the end are stripped off.
        """
        self.assertEqual(self.reader.get_metadata_field(
            metadata, 'Languages'), languages)

    def test_get_metadata_field_participants(self):
        """Test for the get_metadata_field-method.

        Test participants.
        It is assumed that whitespace-characters at the 
        beginning and at the end are stripped off.
        """
        self.assertEqual(
            self.reader.get_metadata_field(metadata, 'Participants'), ptcs)

    def test_get_metadata_field_ID(self):
        """Test for the get_metadata_field-method.

        Test IDs.
        It is assumed that whitespace-characters at the 
        beginning and at the end are stripped off.
        """
        self.assertEqual(self.reader.get_metadata_field(metadata, 'ID'), ids)

    def test_get_metadata_field_birth(self):
        """Test for the get_metadata_field-method.

        Test birth-fields.
        It is assumed that whitespace-characters at the 
        beginning and at the end are stripped off.
        """
        b_chi = self.reader.get_metadata_field(metadata, 'Birth of CHI')
        b_adu = self.reader.get_metadata_field(metadata, 'Birth of ADU')
        b_boy = self.reader.get_metadata_field(metadata, 'Birth of BOY')
        birth_of_all = '{}\n{}\n{}'.format(b_chi, b_adu, b_boy)


if __name__ == '__main__':
    unittest.main()
