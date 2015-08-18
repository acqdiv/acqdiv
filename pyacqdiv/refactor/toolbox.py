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

    _separator = re.compile(b'\r?\n\r?\n(\r?\n)')

    def __init__(self, config, file_path):
        self.path = file_path
        self.config = config
        self.session_id = self.config['record_tiers']['record_marker']
        self.record_marker = self.config['record_tiers']['record_marker']

        #self.tier_matches = collections.OrderedDict()
        #for k, v in self.config['record_tiers'].items():
        #    b = bytearray(v.encode())
        #    self.tier_matches[k] = re.compile(b.decode())

        # self.record_marker = self.config['record_tiers']['record_marker']
        # self.regex = re.compile(self.record_marker, re.MULTILINE)
        # self._separator = re.compile(b'\r?\n\r?\n(\r?\n)')

        # self.record_separator = re.compile(b'\\n{2,}')
        self.tier_separator = re.compile(b'\n')
        self.field_markers = []

        for k, v in self.config['record_tiers'].items():
            self.field_markers.append(k)

        # TODO: get sentence type, etc...

    # TODO: return utterances, words, morphemes, as ordered dictionaries?
    def __iter__(self):
        record_marker = re.compile(br'\\ref')
        with open (self.path, 'rb') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                ma = record_marker.search(data)
                header = data[:ma.start()].decode()
                pos = ma.start()
                for ma in record_marker.finditer(data, ma.end()):
                    utterances = collections.OrderedDict()
                    # utterances['session_id'] = self.session_id

                    record = data[pos:ma.start()]
                    tiers = self.tier_separator.split(record)
                    for tier in tiers:
                        tokens = re.split(b'\\s+', tier, maxsplit=1)
                        field_marker = tokens[0].decode()
                        field_marker = field_marker.replace("\\", "")
                        content = "None"
                        if len(tokens) > 1:
                            content = tokens[1].decode()
                            content = re.sub('\\s+', ' ', content)

                        if field_marker in self.field_markers:
                            utterances[self.config['record_tiers'][field_marker]] = content

                    yield utterances
                    pos = ma.start()
                """
                ma = self._separator.search(data, pos)
                if ma is None:
                    footer = ''
                    yield data[pos:].decode()
                else:
                    footer = data[ma.start(1):].decode()
                    yield data[pos:ma.start(1)].decode()
                self.header, self.footer = header, footer
                """


    def make_rec(self, data):
        return data.decode(self.encoding)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.path)


class Record(collections.OrderedDict):
    """ Toolbox records in file """
    # report if record is missing
    def __init__(**kwargs):
        pass

    def clean(self):
        # use Robert's cleaning functions
        pass

class UtteranceType(object):
    # form to function mapping from punctuation to sentence type
    pass


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

    # cfg.read("Chintang.ini")
    # f = "../../corpora/Chintang/toolbox/CLDLCh1R01S02.txt"

    # cfg.read("Russian.ini")
    # f = "../../corpora/Russian/toolbox/A00210817.txt"

    cfg.read("Indonesian.ini")
    f = "../../corpora/Indonesian/toolbox/HIZ-010601.txt"


    t = ToolboxFile(cfg, f)
    for record in t:
        print(record)
        #for k, v in record.items():
        #    print(k, "\t", v)

    # should we clean the records here on a corpus-by-corpus basis?
    # or should we insert data structures as is into the db?


