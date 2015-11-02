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

import toolbox as toolbox
import parsers as parsers



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
        self.toolbx = toolbox.ToolboxFile(self.cfg,self.infile)
        #self.assertTrue(self.toolbx.__init__(self.cfg, "../corpora/Russian/toolbox/A00210817.txt") == True)
        
    def test_tlbxfile_loaded(self):
        """ Test if Toolbox object was loaded """
        self.assertFalse(self.toolbx == None)
    
    def test_utterances(self):
        """ Test if __init__() works """
        self.assertFalse(self.toolbx.config['corpus']['corpus'] == None)
    
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
    # - get_sentence_type()
    # - clean_utterance()
    # - get_warnings()
    # - get_words()
    # - get_morphemes()
    # - do_inference()
    
#class TestChintangParser(TestToolboxParser):
#    def setUp(self):
#        super().setUp()
#        self.cfg.read("Russian.ini")
#        self.infile = codecs.open("../corpora/Chintang/toolbox/CLDLCh1R01S01.txt", "r", "utf-8")
#        self.toolbx = toolbox.ToolboxFile(self.cfg,self.infile)
    
        

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
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        