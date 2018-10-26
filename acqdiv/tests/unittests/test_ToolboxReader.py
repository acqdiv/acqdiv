import unittest
from acqdiv.parsers.toolbox.readers.ToolboxReader import *


class TestToolboxReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # if needed set up a file 'Toolbox.txt' later
        file_path = 'test_files/Chintang.txt'
        cls.reader = ToolboxReader(file_path)

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

    def test_is_record(self):
        pass




if __name__ == '__main__':
    unittest.main()