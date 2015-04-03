from unittest import TestCase


class Tests(TestCase):
    def test_repair_lines(self):
        from pyacqdiv.lib.chat import repair_lines

        self.assertEquals(repair_lines([]), [])
        self.assertEquals(repair_lines(['']), [''])
        self.assertEquals(repair_lines(['abc']), ['abc'])
        self.assertEquals(repair_lines(['*']), ['*'])
        self.assertEquals(repair_lines(['*', 'abc']), ['* abc'])
        self.assertEquals(repair_lines(['*', 'abc', '@']), ['* abc', '@'])

