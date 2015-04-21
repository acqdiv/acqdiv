# -*- coding: utf-8 -*-
import unittest
import codecs
import os
import sys
os.chdir('../acqdiv') ## change to main dir of repository
reload(sys)  
sys.setdefaultencoding('utf8') ## needed to avoid UnicodeDecodeError for Japanese, Cree and Turkish!
from extraction.parsing.corpus_parser import parserTest


'''
test script that can be run with nosetests to compare goldstandard json files with the
generated json output files from the parser.
It uses the parserTest()-function from corrpus_parser.py to call the parser.

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
    
    
    
    def test_inuktitut(self):
        '''test if Inuktitut output is correct.'''
        parserTest("Inuktitut")
        output,gold = files_to_compare("tests/parsing/output_test/Inuktitut_prettyprint.txt", "tests/parsing/Inuktitut_prettyprint.txt")
        self.assertEqual(output, gold)
    
    def test_indonesian(self):
        '''test if Indonesian output is correct.'''
        parserTest("Indonesian")
        output,gold = files_to_compare("tests/parsing/output_test/Indonesian_prettyprint.txt", "tests/parsing/Indonesian_prettyprint.txt")
        self.assertEqual(output, gold)
    
    def test_russian(self):
        '''test if Russian output is correct.'''
        parserTest("Russian")
        output,gold = files_to_compare("tests/parsing/output_test/Russian_prettyprint.txt", "tests/parsing/Russian_prettyprint.txt")
        self.assertEqual(output, gold)
        
    def test_sesotho(self):
        '''test if Sesotho output is correct.'''
        parserTest("Sesotho")
        output,gold = files_to_compare("tests/parsing/output_test/Sesotho_prettyprint.txt", "tests/parsing/Sesotho_prettyprint.txt")
        self.assertEqual(output, gold)
        
    def test_japanese_miipro(self):
        '''test if Japanese_MiiPro output is correct.'''
        parserTest("Japanese_MiiPro")
        output,gold = files_to_compare("tests/parsing/output_test/Japanese_MiiPro_prettyprint.txt", "tests/parsing/Japanese_MiiPro_prettyprint.txt")
        self.assertEqual(output, gold)
    
    def test_japanese_miyata(self):
        '''test if Japanese_Miyata output is correct.'''
        parserTest("Japanese_Miyata")
        output,gold = files_to_compare("tests/parsing/output_test/Japanese_Miyata_prettyprint.txt", "tests/parsing/Japanese_Miyata_prettyprint.txt")
        self.assertEqual(output, gold)
    
    def test_cree(self):
        '''test if Cree output is correct.'''
        parserTest("Cree")
        output,gold = files_to_compare("tests/parsing/output_test/Cree_prettyprint.txt", "tests/parsing/Cree_prettyprint.txt")
        self.assertEqual(output, gold)
    
    ##def test_turkish(self):
    ##    parserTest("Turkish_KULLD")
    ##    output,gold = files_to_compare("tests/parsing/output_test/Turkish_KULLD.json", "tests/parsing/Turkish_KULLD.json")
    ##    self.assertEqual(output, gold)
    #
    #def test_yucatec(self):
    #    '''test if Cree output is correct.'''
    #    parserTest("Yucatec")
    #    output,gold = files_to_compare("tests/parsing/output_test/Yucatec_prettyprint.txt", "tests/parsing/Yucatec_prettyprint.txt")
    #    self.assertEqual(output, gold)
    
    #def test_chintang(self):
    #    '''test if Chintang output is correct.'''
    #    parserTest("Chintang")
    #    output,gold = files_to_compare("tests/parsing/output_test/Chintang_prettyprint.txt", "tests/parsing/Chintang_prettyprint.txt")
    #    self.assertEqual(output, gold)
    
if __name__ == '__main__':
    unittest.main()

