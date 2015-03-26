import os
from io import open
from tempfile import TemporaryDirectory
import shutil
import csv
import logging
log = logging.getLogger(__name__)

import chardet

import pyacqdiv


def read_csv(path, skip_header=True, **kw):
    rows = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, **kw)
        for lineno, row in enumerate(reader):
            if not skip_header or lineno > 0:
                rows.append(row)
    return rows


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


def pkg_path(*comps):
    return os.path.abspath(os.path.join(os.path.dirname(pyacqdiv.__file__), *comps))


def split_words(s, sep=','):
    return [w.strip() for w in s.split(sep)]


def existing_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path
