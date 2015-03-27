import os
import unittest
from tempfile import mkdtemp
import shutil

from pyacqdiv.util import pkg_path


def test_data(*comps):
    """Access test data files.

    :param comps: Path components of the data file path relative to the tests/data dir.
    :return: Absolute path to the specified test data file.
    """
    return pkg_path('tests', 'data', *comps)


class WithTempDir(unittest.TestCase):
    def setUp(self):
        self.tmp = mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def tmp_path(self, *comps):
        return os.path.join(self.tmp, *comps)
