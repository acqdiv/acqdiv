""" Parse toolbox files
"""

import re
import sys
import os
import collections
import contextlib
import mmap
import re

class ToolboxFile(object):
    """ Toolbox Standard Format text file as iterable over records """

    def __init__(self, config, file_path):
        self.path = file_path
        filename = os.path.basename(self.path)
        self.session_id = os.path.splitext(filename)[0]
        self.config = config
        self.record_marker = config['record_tiers']['record_marker']

        #self.tier_matches = collections.OrderedDict()
        #for k, v in self.config['record_tiers'].items():
        #    b = bytearray(v.encode())
        #    self.tier_matches[k] = re.compile(b.decode())

        # self.record_marker = self.config['record_tiers']['record_marker']
        # self.regex = re.compile(self.record_marker, re.MULTILINE)
        # self._separator = re.compile(b'\r?\n\r?\n(\r?\n)')

        # self.record_separator = re.compile(b'\\n{2,}')
        self.tier_separator = re.compile(b'\n')
        self.tier_labels = []

        for k, v in self.config['record_tiers'].items():
            self.tier_labels.append(k)
        # self.parse_records()


        # print(self.session_id)

    def __iter__(self):
        record_marker = re.compile(br'\\ref')
        with open (self.path, 'rb') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                ma = record_marker.search(data)
                header = data[:ma.start()].decode()
                pos = ma.start()
                for ma in record_marker.finditer(data, ma.end()):
                    container = collections.OrderedDict()
                    # container['session_id'] = self.session_id

                    record = data[pos:ma.start()]
                    tiers = self.tier_separator.split(record)
                    for tier in tiers:
                        tokens = re.split(b'\\s+', tier, maxsplit=1)
                        # print(tokens)

                        tier_label = tokens[0].decode()
                        tier_label = tier_label.replace("\\", "")

                        if tier_label in self.tier_labels:
                            container[self.config['record_tiers'][tier_label]] = tiers[1].decode().strip()

                    pos = ma.start()
                    yield container

    """
    def __iter__(self):
        # make toolbox file an iterable over its records
        # make_rec = self.make_rec
        with open (self.path, 'rb') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                records = self.record_separator.split(data)
                for record in records:
                    yield record
    """

    def make_rec(self, data):
        return data.decode(self.encoding)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.path)

    """
    def parse(self):
        self.body = open(self.path).read()
        self.body = re.sub(u'\ufeff', '', self.body)
        tiers = re.split('\\n{2,}', self.body)
        # tiers = re.split(r'\r?\n\r?\n(\r?\n)', self.body)
        for t in tiers:
            print(t)
            print()
    """


class Record(collections.OrderedDict):
    """ Toolbox records in file """

    # report if record is missing
    pass

    # should we clean the records here on a corpus-by-corpus basis?
    # or should we insert data structures as is into the db?

@contextlib.contextmanager
def memorymapped(path, access=mmap.ACCESS_READ):
    """Return a block context with path as memory-mapped file."""
    fd = open(path)
    try:
        m = mmap.mmap(fd.fileno(), 0, access=access)
    except:
        fd.close()
        raise
    try:
        yield m
    finally:
        m.close()
        fd.close()


if __name__ == "__main__":
    from parsers import CorpusConfigParser

    cfg = CorpusConfigParser()

    cfg.read("Chintang.ini")
    f = "../../corpora/Chintang/toolbox/CLDLCh1R01S02.txt"

    # cfg.read("Russian.ini")
    # f = "../../corpora/Russian/toolbox/A00210817.txt"

    t = ToolboxFile(cfg, f)
    for record in t:
        print(record)

