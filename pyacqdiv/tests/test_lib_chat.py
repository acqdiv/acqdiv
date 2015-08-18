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
        self.assertEquals(repair_lines(['%mor:\t1\n', ' 2']), ['%mor:\t1 2'])
        self.assertEquals(repair_lines(['%mor:\t1\n', ' \t2']), ['%mor:\t1 2'])
        self.assertEquals(repair_lines(['%mor:\t1\n', ' \t2\n', ' 3']), ['%mor:\t1 2 3'])

