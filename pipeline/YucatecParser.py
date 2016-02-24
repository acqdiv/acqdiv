# -*- coding: utf-8 -*-

import re
import sys
import itertools

from lxml import etree
from XMLParser import XMLParser

class YucatecParser(XMLParser):
    def next_utterance(self):
        for u in self._get_utts():
            # morph = self._morphology_inference(u)
            """
            for w, ms in itertools.takewhile(lambda x: x[1] != None,
                    itertools.zip_longest(u['words'], morph)):
                for m in ms:
                    try:
                        m['word_id_fk'] = w['word_id']
                    except TypeError:
                        m = None
                        continue
            """
            # u['morphology'] = morph
            # u['morphology'] = None
            yield u['utterance'], u['words'], u['morphology']