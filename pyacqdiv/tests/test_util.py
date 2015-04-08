from pyacqdiv.tests.util import WithTempDir


class Tests(WithTempDir):
    def test_csv(self):
        from pyacqdiv.util import read_csv, write_csv

        inrows = [['col1', 'col2'], ['äüö', 'abc']]
        fname = self.tmp_path('test.csv')
        write_csv(fname, inrows)
        outrows = read_csv(fname, skip_header=False)
        self.assertEquals(inrows, outrows)
