#-*- coding: utf-8 -*-

import unittest
import re, os, sys

current_dir = os.getcwd()
sys.path.append(current_dir)

import metadata as metadata
import unittest
import parsers as parsers



# xml parsing tests
class TestXMLParser(unittest.TestCase):

    def setUp(self):
        self.cfg = parsers.CorpusConfigParser()

class TestCreeParser(TestXMLParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Cree.ini")
        self.infile = codecs.open("../corpora/test/Cree.xml", "r", "utf-8")
        self.file_path = "../corpora/test/Cree.xml"
        #self.toolbx = toolbox.ToolboxFile(self.cfg,self.infile)
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)

    #def testBasicXMLParsing(self):
    #    for k, v in self.xml.metadata.items():
    #        self.assertFalse(v == None)

class TestInuktitutParser(TestXMLParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Inuktitut.ini")
        self.infile = codecs.open("../corpora/test/Inuktitut.xml", "r", "utf-8")
        self.file_path = "../corpora/test/Inuktitut.xml"
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
        
    ## TODO define test functions
        
class TestJapanese_MiiProParser(TestXMLParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Japanese_MiiPro.ini")
        self.infile = codecs.open("../corpora/test/Japanese_MiiPro.xml", "r", "utf-8")
        self.file_path = "../corpora/test/Japanese_MiiPro.xml"
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
        
    ## TODO define test functions
        
class TestSesothoParser(TestXMLParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Sesotho.ini")
        self.infile = codecs.open("../corpora/test/Sesotho.xml", "r", "utf-8")
        self.file_path = "../corpora/test/Sesotho.xml"
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
        
    ## TODO define test functions
        
class TestTurkishParser(TestXMLParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Turkish.ini")
        self.infile = codecs.open("../corpora/test/Turkish.xml", "r", "utf-8")
        self.file_path = "../corpora/test/Turkish.xml"
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
    
    ## TODO define test functions
        
class TestYucatecParser(TestXMLParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Yucatec.ini")
        self.infile = codecs.open("../corpora/test/Yucatec.xml", "r", "utf-8")
        self.file_path = "../corpora/test/Yucatec.xml"
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
    
    ## TODO define test functions


if __name__ == "__main__":
    current_dir = os.getcwd()
    sys.path.append(current_dir)
    
    import metadata as metadata
    import time
    import unittest
    import parsers as parsers

