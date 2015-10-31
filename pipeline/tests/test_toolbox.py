import unittest
import re, codecs

#lingdp: I had to import the modules by using pipeline.module, otherwise it didn't work (ImportError)
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
        
    def test_tlbxfile_loaded(self):
        """ Test if Toolbox object was loaded """
        self.assertFalse(self.toolbx == None)
    
    
    #TODO: strange, this yielded "True", now all of a sudden "False"... hmmm...
    #def test_utterances(self):
    #    """ Test if __init__() works """
    #    self.assertTrue(self.toolbx.__init__(self.cfg, "../corpora/Russian/toolbox/A00210817.txt") == True)
    
    
    #TODO: Write tests to check input/output of the following ToolboxFile methods:
    # - get_sentence_type()
    # - clean_utterance()
    # - get_warnings()
    # - get_words()
    # - get_morphemes()
    # - do_inference()
        

if __name__ == "__main__":
    main()
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        