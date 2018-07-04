import unittest
from acqdiv.parsers.xml.CHATCleaner import CHATCleaner


class TestCHATCleaner(unittest.TestCase):
	'''
	class to test CHATCleaner
	'''

	def test_remove_redundant_whitespaces(self):
		self.assertEqual(CHATCleaner.remove_redundant_whitespaces(' h h'), 'h h')
		self.assertEqual(CHATCleaner.remove_redundant_whitespaces('h h '), 'h h')
		self.assertEqual(CHATCleaner.remove_redundant_whitespaces('h  h'), 'h h')
		self.assertEqual(CHATCleaner.remove_redundant_whitespaces('\th \t\th\t'), 'h h')
		self.assertEqual(CHATCleaner.remove_redundant_whitespaces('\nh\n\n h\n'), 'h h')
		self.assertEqual(CHATCleaner.remove_redundant_whitespaces('\rh\r\r h\r'), 'h h')
		


if __name__ == '__main__':
	unittest.main()