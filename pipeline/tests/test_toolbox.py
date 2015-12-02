import unittest
import re, codecs, os, sys

current_dir = os.getcwd()
sys.path.append(current_dir)

import unittest
from itertools import islice
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

 
    def test_utterances(self):
        """ Test if all Russian utterances are loaded """
        self.assertEqual(len(list(self.parser.next_utterance())), 624)
        
    def test_sentence_type(self):
        """ Test if get_sentence_type() works for Russian """
        #self.assertFalse(self.toolbx.config['corpus']['corpus'] == None)
        self.assertEqual(self.toolbx.get_sentence_type('kakaja uzhasnaja pogoda!'),'imperative')
        self.assertEqual(self.toolbx.get_sentence_type('a shto ty dumaeshq?'),'question')
        self.assertEqual(self.toolbx.get_sentence_type('eto dolzhno bytq difolt.'),'default')
        
    def test_clean_utterance(self):
        """ Test if clean_utterance() works for Russian """
        self.assertEqual(self.toolbx.clean_utterance('eto nado udalitq [xxx] i eto [?] tozhe'), 'eto nado udalitq  i eto  tozhe')
        
    def test_get_words(self):
        """ Test if get_words() works for Russian """
        #input_utterance is utterance nbr 622 from Russian test file (but can actually be any other "special case" utterance)
        #print(input_utterance[0]['utterance'])
        #print(self.toolbx.get_words(input_utterance[0]))
        input_utterance = next(islice(self.parser.next_utterance(), 621,621+1))
        self.assertEqual(str(self.toolbx.get_words(input_utterance[0])), "[OrderedDict([('word', 'idi'), ('utterance_id_fk', 'A00210817_622')]), OrderedDict([('word', 'prinesi'), ('utterance_id_fk', 'A00210817_622')]), OrderedDict([('word', 'tank'), ('utterance_id_fk', 'A00210817_622')])]")
        
    def test_get_morphemes(self):
        """ Test if get_morphemes() works for Russian"""
        input_utterance = next(islice(self.parser.next_utterance(), 621,621+1))
        #print(self.toolbx.get_morphemes(input_utterance[0]))
        self.assertEqual(str(self.toolbx.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', 'idti'), ('utterance_id_fk', 'A00210817_622')]), OrderedDict([('morpheme', 'prinesti'), ('utterance_id_fk', 'A00210817_622')]), OrderedDict([('morpheme', 'tank'), ('utterance_id_fk', 'A00210817_622')])]")
    
    def test_do_inference(self):
        """ Test if do_inference() works for Russian """
        input_utterance = next(islice(self.parser.next_utterance(), 621,621+1))
        self.assertEqual(str(self.toolbx.do_inference(input_utterance[0])), "[OrderedDict([('utterance_id_fk', 'A00210817_622'), ('pos_raw', 'V'), ('gloss_raw', 'IMP:2:SG:IRREFL:IPFV')]), OrderedDict([('utterance_id_fk', 'A00210817_622'), ('pos_raw', 'V'), ('gloss_raw', 'IMP:2:SG:IRREFL:PFV')]), OrderedDict([('utterance_id_fk', 'A00210817_622'), ('pos_raw', 'NOUN'), ('gloss_raw', 'M:SG:ACC:INAN')])]")
        
    
#    

## Chintang
class TestChintangParser(TestToolboxParser):
    def setUp(self):
        super().setUp()
        self.cfg.read("Chintang.ini")
        self.infile = codecs.open("../corpora/Chintang/toolbox/CLDLCh1R01S01.txt", "r", "utf-8")
        self.file_path = "../corpora/Chintang/toolbox/CLDLCh1R01S01.txt"
        self.toolbx = toolbox.ToolboxFile(self.cfg,self.infile)
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
        
    def test_tlbxfile_loaded(self):
        """ Test if Chintang Toolbox object was loaded """
        self.assertFalse(self.toolbx == None)
        
    def test_sentence_type(self):
        """ Test if get_sentence_type() works for Chintang """
        #self.assertFalse(self.toolbx.config['corpus']['corpus'] == None)
        self.assertEqual(self.toolbx.get_sentence_type('habinɨŋ habinɨŋ।'),'default')
        self.assertEqual(self.toolbx.get_sentence_type('tosaŋa theme meʔtoko?'),'question')
        self.assertEqual(self.toolbx.get_sentence_type('kulukke ei!'),'exclamation')
        
    def test_get_words(self):
        """ Test if get_words() works for Chintang """
        #input_utterance is utterance nbr 1 from Chintang test file (but can actually be any other "special case" utterance)
        input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
        self.assertEqual(str(self.toolbx.get_words(input_utterance[0])), "[OrderedDict([('word', 'habinɨŋ'), ('utterance_id_fk', 'CLDLCh1R01S01.001')]), OrderedDict([('word', 'habinɨŋ'), ('utterance_id_fk', 'CLDLCh1R01S01.001')])]")

    def test_get_morphemes(self):
        """ Test if get_morphemes() works for Chintang"""
        input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
        #print(self.toolbx.get_morphemes(input_utterance[0]))
        self.assertEqual(str(self.toolbx.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', 'hap-i-nɨŋ'), ('utterance_id_fk', 'CLDLCh1R01S01.001')]), OrderedDict([('morpheme', 'hap-i-nɨŋ'), ('utterance_id_fk', 'CLDLCh1R01S01.001')])]")
    
    def test_do_inference(self):
        """ Test if do_inference() works for Chintang """
        input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
        #print(self.toolbx.do_inference(input_utterance[0]))
        self.assertEqual(str(self.toolbx.do_inference(input_utterance[0])), "[OrderedDict([('utterance_id_fk', 'CLDLCh1R01S01.001'), ('morpheme', 'hap'), ('gloss_raw', 'cry'), ('pos_raw', 'vi')]), OrderedDict([('utterance_id_fk', 'CLDLCh1R01S01.001'), ('morpheme', '-i'), ('gloss_raw', '-1/2pS/P'), ('pos_raw', '-gm')]), OrderedDict([('utterance_id_fk', 'CLDLCh1R01S01.001'), ('morpheme', '-nɨŋ'), ('gloss_raw', '-NEG'), ('pos_raw', '-gm')]), OrderedDict([('utterance_id_fk', 'CLDLCh1R01S01.001'), ('morpheme', 'hap'), ('gloss_raw', 'cry'), ('pos_raw', 'vi')]), OrderedDict([('utterance_id_fk', 'CLDLCh1R01S01.001'), ('morpheme', '-i'), ('gloss_raw', '-1/2pS/P'), ('pos_raw', '-gm')]), OrderedDict([('utterance_id_fk', 'CLDLCh1R01S01.001'), ('morpheme', '-nɨŋ'), ('gloss_raw', '-NEG'), ('pos_raw', '-gm')])]") 
        

## Indonesian
class TestIndonesianParser(TestToolboxParser):
    def setUp(self):
        super().setUp()
        self.cfg.read("Indonesian.ini")
        self.infile = codecs.open("../corpora/Indonesian/toolbox/HIZ-1999-05-20.txt", "r", "utf-8")
        self.file_path = "../corpora/Indonesian/toolbox/HIZ-1999-05-20.txt"
        self.toolbx = toolbox.ToolboxFile(self.cfg,self.infile)
        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
        
    def test_tlbxfile_loaded(self):
        """ Test if Indonesian Toolbox object was loaded """
        self.assertFalse(self.toolbx == None)
    
    def test_sentence_type(self):
        """ Test if get_sentence_type() works for Indonesian """
        #self.assertFalse(self.toolbx.config['corpus']['corpus'] == None)
        self.assertEqual(self.toolbx.get_sentence_type('da da.'),'default')
        self.assertEqual(self.toolbx.get_sentence_type('Opa Tono mana, Opa Tono?'),'question')
        self.assertEqual(self.toolbx.get_sentence_type('eh, bediri!'),'imperative')
        
    def test_get_words(self):
        """ Test if get_words() works for Indonesian """
        #input_utterance is utterance nbr 1 from Indonesian test file (but can actually be any other "special case" utterance)
        input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
        self.assertEqual(str(self.toolbx.get_words(input_utterance[0])), "[OrderedDict([('utterance_id_fk', '736551094519120405'), ('word_target', 'da'), ('word', 'da')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('word_target', 'da'), ('word', 'da')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('word_target', 'xx'), ('word', 'xx')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('word_target', 'Tante'), ('word', 'Tante')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('word_target', 'Tante'), ('word', 'Tante')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('word_target', 'Tante'), ('word', 'Tante')])]")
    
    def test_get_morphemes(self):
        """ Test if get_morphemes() works for Chintang"""
        input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
        self.assertEqual(str(self.toolbx.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', 'da'), ('utterance_id_fk', '736551094519120405')]), OrderedDict([('morpheme', 'da'), ('utterance_id_fk', '736551094519120405')]), OrderedDict([('morpheme', 'xx'), ('utterance_id_fk', '736551094519120405')]), OrderedDict([('morpheme', 'Tante'), ('utterance_id_fk', '736551094519120405')]), OrderedDict([('morpheme', 'Tante'), ('utterance_id_fk', '736551094519120405')]), OrderedDict([('morpheme', 'Tante'), ('utterance_id_fk', '736551094519120405')])]")
    
    def test_do_inference(self):
        """ Test if do_inference() works for Chintang """
        input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
        self.assertEqual(str(self.toolbx.do_inference(input_utterance[0])), "[OrderedDict([('utterance_id_fk', '736551094519120405'), ('gloss_raw', 'bye')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('gloss_raw', 'bye')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('gloss_raw', 'xx')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('gloss_raw', 'aunt')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('gloss_raw', 'aunt')]), OrderedDict([('utterance_id_fk', '736551094519120405'), ('gloss_raw', 'aunt')])]") 
        
 
    

        

if __name__ == "__main__":
    current_dir = os.getcwd()
    sys.path.append(current_dir)
    
    import unittest
    from itertools import islice
    import toolbox as toolbox
    import parsers as parsers
    from parsers import *
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        