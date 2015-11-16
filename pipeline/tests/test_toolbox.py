import unittest
import re, codecs, os, sys

current_dir = os.getcwd()
sys.path.append(current_dir)

import database_backend as db
import metadata as metadata
import processors as processors
import postprocessor as pp
import time
import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from itertools import islice, count

import toolbox as toolbox
import parsers as parsers
from parsers import *


class TestToolboxParser(unittest.TestCase):
    """ Tests for Toolbox parser """
    
    def setUp(self):
        self.cfg = parsers.CorpusConfigParser()
    

## Russian
class TestRussianParser(TestToolboxParser):
    
    def setUp(self):
        super().setUp()
        self.cfg.read("Russian.ini")
        self.infile = codecs.open("../corpora/Russian/toolbox/A00210817.txt", "r", "utf-8")
        self.file_path = "../corpora/Russian/toolbox/A00210817.txt"
        self.toolbx = toolbox.ToolboxFile(self.cfg,self.infile)
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
        
    def test_tlbxfile_loaded(self):
        """ Test if Russian Toolbox object was loaded """
        self.assertFalse(self.toolbx == None)
        #print(self.toolbx.field_markers)
        #print(self.toolbx.__dict__)

    #def test_case1(self):
    #    """ Test if __init__() works """
    #    self.assertFalse(self.toolbx.config['corpus']['corpus'] == None)
    
    def test_utterances(self):
        """ Test if all Russian utterances are loaded """
        self.assertEqual(len(list(self.parser.next_utterance())), 624)
        #for elem in self.parser.next_utterance():
        #    print(elem['utterance_id'], '\n')
        
        
    def test_sentence_type(self):
        """ Test if Russian sentence_type works """
        #self.assertFalse(self.toolbx.config['corpus']['corpus'] == None)
        self.assertEqual(self.toolbx.get_sentence_type('kakaja uzhasnaja pogoda!'),'imperative')
        self.assertEqual(self.toolbx.get_sentence_type('a shto ty dumaeshq?'),'question')
        self.assertEqual(self.toolbx.get_sentence_type('eto dolzhno bytq difolt.'),'default')
        
    def test_clean_utterance(self):
        """ Test if Russian clean_utterance works """
        self.assertEqual(self.toolbx.clean_utterance('eto nado udalitq [xxx] i eto [?] tozhe'), 'eto nado udalitq  i eto  tozhe')
    
    #TODO: Write tests to check input/output of the following ToolboxFile methods:
    # - get_words()
    # - get_morphemes()
    # - do_inference()
    # - get_warnings()
        
    def test_get_words(self):
        """ Test if Russian get_words() works """
        pass
        #for utterance, word, morpheme, inferences in self.parser.next_utterance():
        #    print(self.toolbx.get_words(utterance), '\n')
        #utterance = next(islice(self.parser.next_utterance(), 621,621+1))
        #print(self.toolbx.get_words(utterance))
    
    def test_get_morphemes(self):
        """ Test if Russian get_morphemes() works """
        #for utterance, word, morpheme, inferences in self.parser.next_utterance():
        #    print(self.toolbx.get_morphemes(utterance), '\n')
        pass
    
    def test_do_inference(self):
        """ Test if Russian do_inference() works """
        #pass
        for utterance, word, morpheme, inferences in self.parser.next_utterance():
            print(self.toolbx.do_inference(utterance), '\n')
        
    
    

## Chintang
class TestChintangParser(TestToolboxParser):
    def setUp(self):
        super().setUp()
        self.cfg.read("Chintang.ini")
        self.infile = codecs.open("../corpora/Chintang/toolbox/CLDLCh1R01S01.txt", "r", "utf-8")
        self.toolbx = toolbox.ToolboxFile(self.cfg,self.infile)
        #self.assertTrue(self.toolbx.__init__(self.cfg, "../corpora/Russian/toolbox/A00210817.txt") == True)
        
    def test_tlbxfile_loaded(self):
        """ Test if Chintang Toolbox object was loaded """
        self.assertFalse(self.toolbx == None)
        

## Indonesian
class TestIndonesianParser(TestToolboxParser):
    def setUp(self):
        super().setUp()
        self.cfg.read("Indonesian.ini")
        self.infile = codecs.open("../corpora/Indonesian/toolbox/HIZ-1999-05-20.txt", "r", "utf-8")
        self.toolbx = toolbox.ToolboxFile(self.cfg,self.infile)
        
    def test_tlbxfile_loaded(self):
        """ Test if Indonesian Toolbox object was loaded """
        self.assertFalse(self.toolbx == None)
    
    

        

if __name__ == "__main__":
    current_dir = os.getcwd()
    sys.path.append(current_dir)
    
    import database_backend as db
    import metadata as metadata
    import processors as processors
    import postprocessor as pp
    import time
    import unittest
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import func
    
    import toolbox as toolbox
    import parsers as parsers
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        