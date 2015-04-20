# -*- coding: utf-8 -*-
import unittest
import codecs
import os
import sys
os.chdir('../acqdiv') ## make script available from main dir of repository
sys.path.append("extraction/parsing")
reload(sys)  
sys.setdefaultencoding('utf8')
#from extraction.parsing.corpus_parser_test import parser  ## why doesn't this work (even if I have __init__.py everywhere)??
from corpus_parser import parser

'''
test script that can be run with nosetests to compare goldstandard json files with the
generated json output files from the parser

usage (from main folder of repo): $ nosetests tests/test_parsing.py

'''
def files_to_compare(output, gold):
        with codecs.open(output, "r", "utf-8") as output:
            output = output.read()
        with codecs.open(gold, "r", "utf-8") as goldfile:
            gold = goldfile.read()
        return(output, gold)


class Test_Parser(unittest.TestCase):
    maxDiff = None #for printing large output
    
    def setUp(self):
        pass
    
    
    ##PROBLEM: Cree, Japanese (both) and Turkish generate UnicodeDecodeError?? How to solve that?
    
    
    def test_inuktitut(self):
        '''test if Inuktitut output is correct.'''
        parser("Inuktitut")
        output,gold = files_to_compare("corpora_processed/parsed/Inuktitut_prettyprint.txt", "tests/parsing_updated/Inuktitut_prettyprint.txt")
        self.assertEqual(output, gold)
    
    def test_indonesian(self):
        '''test if Indonesian output is correct.'''
        parser("Indonesian")
        output,gold = files_to_compare("corpora_processed/parsed/Indonesian_prettyprint.txt", "tests/parsing_updated/Indonesian_prettyprint.txt")
        self.assertEqual(output, gold)
    
    def test_russian(self):
        '''test if Russian output is correct.'''
        parser("Russian")
        output,gold = files_to_compare("corpora_processed/parsed/Russian_prettyprint.txt", "tests/parsing_updated/Russian_prettyprint.txt")
        self.assertEqual(output, gold)
        
    def test_sesotho(self):
        '''test if Sesotho output is correct.'''
        parser("Sesotho")
        output,gold = files_to_compare("corpora_processed/parsed/Sesotho_prettyprint.txt", "tests/parsing_updated/Sesotho_prettyprint.txt")
        self.assertEqual(output, gold)
        
    def test_japanese_miipro(self):
        '''test if Japanese_MiiPro output is correct.'''
        parser("Japanese_MiiPro")
        output,gold = files_to_compare("corpora_processed/parsed/Japanese_MiiPro_prettyprint.txt", "tests/parsing_updated/Japanese_MiiPro_prettyprint.txt")
        self.assertEqual(output, gold)
    
    def test_japanese_miyata(self):
        '''test if Japanese_Miyata output is correct.'''
        parser("Japanese_Miyata")
        output,gold = files_to_compare("corpora_processed/parsed/Japanese_Miyata_prettyprint.txt", "tests/parsing_updated/Japanese_Miyata_prettyprint.txt")
        self.assertEqual(output, gold)
    
    def test_cree(self):
        '''test if Cree output is correct.'''
        parser("Cree")
        output,gold = files_to_compare("corpora_processed/parsed/Cree_prettyprint.txt", "tests/parsing_updated/Cree_prettyprint.txt")
        self.assertEqual(output, gold)
    
    ##def test_turkish(self):
    ##    parser("Turkish_KULLD")
    ##    output,gold = files_to_compare("corpora_processed/parsed/Turkish_KULLD.json", "tests/parsing/Turkish_KULLD.json")
    ##    self.assertEqual(output, gold)
    #
    #def test_yucatec(self):
    #    '''test if Cree output is correct.'''
    #    parser("Yucatec")
    #    output,gold = files_to_compare("corpora_processed/parsed/Yucatec_prettyprint.txt", "tests/parsing_updated/Yucatec_prettyprint.txt")
    #    self.assertEqual(output, gold)
    
    #def test_chintang(self):
    #    '''test if Chintang output is correct.'''
    #    parser("Chintang")
    #    output,gold = files_to_compare("corpora_processed/parsed/Chintang_prettyprint.txt", "tests/parsing_updated/Chintang_prettyprint.txt")
    #    self.assertEqual(output, gold)
    
if __name__ == '__main__':
    unittest.main()

