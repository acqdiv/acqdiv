#!/usr/bin/bash
#-*- coding: utf-8 -*-

# Test suite for the acqdiv processors and database

import database_backend as db
import metadata
import parsers
import postprocessor as pp
import unittest

# metadata tests

class TestMetadataParser(unittest.TestCase):

    def setUp(self):
        self.cfg = parsers.CorpusConfigParser()

class TestImdiParser(TestMetadataParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Russian.ini")
        self.imdi = metadata.Imdi(self.cfg, "../../corpora/Russian/metadata/A00210817.imdi")

    def testBasicImdiParsing(self):
        for k, v in self.imdi.metadata.items():
            self.assertFalse(v == None)

    def testImdiDateField(self):
        self.assertFalse(self.imdi.metadata["session"]["date"] == None)

if __name__ == "__main__":
    unittest.main()
