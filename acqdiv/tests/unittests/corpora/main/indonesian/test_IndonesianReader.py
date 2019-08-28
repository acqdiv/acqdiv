import unittest

from acqdiv.parsers.corpora.main.indonesian.IndonesianReader \
    import IndonesianReader as Rd
from acqdiv.parsers.toolbox.model.Record import Record


class IndonesianReaderTest(unittest.TestCase):

    def test_is_record(self):
        rec = Record()
        rec['sp'] = 'MOT'
        rec['tx'] = 'Bla Blu'
        actual = Rd.is_record(rec)
        desired = True
        self.assertEqual(actual, desired)

    def test_is_record_AUX(self):
        rec = Record()
        rec['sp'] = 'AUX'
        rec['tx'] = 'Bla Blu'
        actual = Rd.is_record(rec)
        desired = False
        self.assertEqual(actual, desired)

    def test_is_record_PAR(self):
        rec = Record()
        rec['sp'] = '@PAR'
        rec['tx'] = 'Bla Blu'
        actual = Rd.is_record(rec)
        desired = False
        self.assertEqual(actual, desired)



if __name__ == '__main__':
    unittest.main()
