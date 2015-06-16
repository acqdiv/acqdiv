# for now call xml2json (installed script)
# think about and talk to Robert about how to incorporate external-python libraries to pyacqdiv

# drop the unneeded
import os, sys
import shutil
from collections import defaultdict
from copy import copy
from io import open
from tempfile import TemporaryDirectory
import shutil
import csv
import logging
log = logging.getLogger(__name__)

import chardet
import pyacqdiv


def utf8(path):
    with open(path, 'rb') as fp:
        encoding = chardet.detect(fp.read())['encoding']

    if encoding == 'utf-8':
        return

    with TemporaryDirectory() as tmp_dir:
        with open(path, "r", encoding=encoding) as infile:
            oname = os.path.join(tmp_dir, os.path.basename(path))
            with open(oname, "w", encoding='utf8') as outfile:
                for line in infile:
                    outfile.write(line.strip() + "\n")

        # now both infile and outfile are closed, so we can copy.
        shutil.copy(oname, path)

    log.info("reencoding %s from %s to utf-8" % (path, encoding))

def setup_json(self):
    """Copy files from copora directory to cleaning/input and rewrite to UTF-8.
    :return: Number of session files copied to input.
    """
    assert existing_dir(self.input_path())
    count = 0
    for dir_path, subdir_list, file_list in os.walk(self.cfg['src']):
        for fname in file_list:
            if fname.startswith('.'):
                continue
            dst = self.input_path(self.code['clean_filename'](fname))
            shutil.copy(os.path.join(dir_path, fname), dst)
            utf8(dst)
            count += 1
    return count

if __name__=="__main__":
    


