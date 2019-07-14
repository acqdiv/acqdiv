import unittest

from acqdiv.parsers.toolbox.readers.ToolboxFileParser import ToolboxFileParser


class TestToolboxFileParser(unittest.TestCase):
    
    def test_get_record_dict(self):
        record = ('\\ref session_name.001\n'
                  '\\ELANBegin 00:50:11.150\n'
                  '\\ELANEnd 00:50:22.350\n'
                  '\\ELANParticipant MAR\n'
                  '\\nep ?')
        actual_output = ToolboxFileParser.get_record_dict(record)
        desired_output = {
            'ref': 'session_name.001',
            'ELANBegin': '00:50:11.150',
            'ELANEnd': '00:50:22.350',
            'ELANParticipant': 'MAR',
            'nep': '?'
        }
        self.assertEqual(actual_output, desired_output)

    def test_get_tiers(self):
        record = ('\\ref session_name.001\n'
                  '\\ELANBegin 00:50:11.150\n'
                  '\\ELANEnd 00:50:22.350\n'
                  '\\ELANParticipant MAR\n'
                  '\\nep ?')
        actual_output = ToolboxFileParser.get_tiers(record)
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
        actual_output = ToolboxFileParser.get_tier(tier)
        desired_output = ('ref', 'session_name.001')
        self.assertEqual(actual_output, desired_output)
