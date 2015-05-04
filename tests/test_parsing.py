# -*- coding: utf-8 -*-
import unittest
import codecs
import os
import sys
#os.chdir('../acqdiv') ## change to main dir of repository
mywd = os.getcwd()

if str(mywd).endswith('/acqdiv'):
        pass
else:
        os.chdir('../../acqdiv') ## change to main dir of repository
reload(sys)  
sys.setdefaultencoding('utf8') ## needed to avoid UnicodeDecodeError for Japanese, Cree and Turkish!
from extraction.parsing.corpus_parser import parserTest


'''
test script that can be run with nosetests to compare goldstandard json files with the
generated json output files from the parser.
It uses the parserTest()-function from corrpus_parser.py to call the parser.

usage (from main folder of repo): $ nosetests tests/test_parsing.py  or $ nosetests tests/

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
        output,gold = files_to_compare("tests/parsing/Inuktitut/Inuktitut_prettyprint.txt", "tests/parsing/Inuktitut/Inuktitut_goldstandard.txt")
        self.assertEqual(output, gold)

    
    def test_indonesian(self):
        '''test if Indonesian output is correct.'''
        parserTest("Indonesian")
        output,gold = files_to_compare("tests/parsing/Indonesian/Indonesian_prettyprint.txt", "tests/parsing/Indonesian/Indonesian_goldstandard.txt")
        self.assertEqual(output, gold)
    
    def test_russian(self):
        '''test if Russian output is correct.'''
        parserTest("Russian")
        output,gold = files_to_compare("tests/parsing/Russian/Russian_prettyprint.txt", "tests/parsing/Russian/Russian_goldstandard.txt")
        self.assertEqual(output, gold)
        
    def test_sesotho(self):
        '''test if Sesotho output is correct.'''
        parserTest("Sesotho")
        output,gold = files_to_compare("tests/parsing/Sesotho/Sesotho_prettyprint.txt", "tests/parsing/Sesotho/Sesotho_goldstandard.txt")
        self.assertEqual(output, gold)
        
    def test_japanese_miipro(self):
        '''test if Japanese_MiiPro output is correct.'''
        parserTest("Japanese_MiiPro")
        output,gold = files_to_compare("tests/parsing/Japanese_MiiPro/Japanese_MiiPro_prettyprint.txt", "tests/parsing/Japanese_MiiPro/Japanese_MiiPro_goldstandard.txt")
        self.assertEqual(output, gold)
    
    def test_japanese_miyata(self):
        '''test if Japanese_Miyata output is correct.'''
        parserTest("Japanese_Miyata")
        output,gold = files_to_compare("tests/parsing/Japanese_Miyata/Japanese_Miyata_prettyprint.txt", "tests/parsing/Japanese_Miyata/Japanese_Miyata_goldstandard.txt")
        self.assertEqual(output, gold)
    
    def test_cree(self):
        '''test if Cree output is correct.'''
        parserTest("Cree")
        output,gold = files_to_compare("tests/parsing/Cree/Cree_prettyprint.txt", "tests/parsing/Cree/Cree_goldstandard.txt")
        self.assertEqual(output, gold)
    
    ##def test_turkish(self):
    ##    parserTest("Turkish_KULLD")
    ##    output,gold = files_to_compare("tests/parsing/Turkish_KULLD/Turkish_KULLD_prettyprint.txt", "tests/parsing/Turkish_KULLD/Turkish_KULLD_goldstandard.txt")
    ##    self.assertEqual(output, gold)
    #
    #def test_yucatec(self):
    #    '''test if Cree output is correct.'''
    #    parserTest("Yucatec")
    #    output,gold = files_to_compare("tests/parsing/Yucatec/Yucatec_prettyprint.txt", "tests/parsing/Yucatec/Yucatec_goldstandard.txt")
    #    self.assertEqual(output, gold)
    
    def test_chintang(self):
        '''test if Chintang output is correct.'''
        parserTest("Chintang")
        output,gold = files_to_compare("tests/parsing/Chintang/Chintang_prettyprint.txt", "tests/parsing/Chintang/Chintang_goldstandard.txt")
        self.assertEqual(output, gold)
    
if __name__ == '__main__':
    unittest.main()

