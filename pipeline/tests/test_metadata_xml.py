#-*- coding: utf-8 -*-

import unittest
import re, os, sys

current_dir = os.getcwd()
sys.path.append(current_dir)

import metadata as metadata
import unittest
import parsers as parsers



# metadata tests
class TestMetadataParser(unittest.TestCase):

    def setUp(self):
        self.cfg = parsers.CorpusConfigParser()

class TestImdiParser(TestMetadataParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Russian.ini")
        self.imdi = metadata.Imdi(self.cfg, "../corpora/Russian/imdi/A00210817.imdi")

    def testBasicImdiParsing(self):
        for k, v in self.imdi.metadata.items():
            self.assertFalse(v == None)

    def testImdiDateField(self):
        self.assertFalse(self.imdi.metadata["session"]["date"] == None)

class TestXMLParser(TestMetadataParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Cree.ini")
        self.xml = metadata.Chat(self.cfg, "../corpora/Cree/xml/02-A1-2005-03-25.xml")

    def testBasicXMLParsing(self):
        for k, v in self.xml.metadata.items():
            self.assertFalse(v == None)


if __name__ == "__main__":
    current_dir = os.getcwd()
    sys.path.append(current_dir)
    
    import metadata as metadata
    import time
    import unittest
    import parsers as parsers