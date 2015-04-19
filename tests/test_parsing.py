import unittest
import codecs
import os
import sys
os.chdir('../acqdiv') ## make script available from main dir of repository
sys.path.append("extraction/parsing") 
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
        output,gold = files_to_compare("corpora_processed/parsed/Inuktitut.json", "tests/parsing_updated/Inuktitut.json")
        self.assertEqual(output, gold)
    
    def test_indonesian(self):
        '''test if Indonesian output is correct.'''
        parser("Indonesian")
        output,gold = files_to_compare("corpora_processed/parsed/Indonesian.json", "tests/parsing_updated/Indonesian.json")
        self.assertEqual(output, gold)

    def test_russian(self):
        '''test if Russian output is correct.'''
        parser("Russian")
        output,gold = files_to_compare("corpora_processed/parsed/Russian.json", "tests/parsing_updated/Russian.json")
        self.assertEqual(output, gold)
        
    def test_sesotho(self):
        '''test if Sesotho output is correct.'''
        parser("Sesotho")
        output,gold = files_to_compare("corpora_processed/parsed/Sesotho.json", "tests/parsing_updated/Sesotho.json")
        self.assertEqual(output, gold)
        

    ##def test_japanese_miipro(self):
    ##    parser("Japanese_MiiPro")
    ##    output,gold = files_to_compare("corpora_processed/parsed/Japanese_MiiPro.json", "tests/parsing/Japanese_MiiPro.json")
    ##    self.assertEqual(output, gold)
    
    ##def test_japanese_miyata(self):
    ##    '''test if Japanese_Miyata output is correct.'''
    ##    parser("Japanese_Miyata")
    ##    output,gold = files_to_compare("corpora_processed/parsed/Japanese_Miyata.json", "tests/parsing/Japanese_Miyata.json")
    ##    self.assertEqual(output, gold)
    
    ##def test_cree(self):
    ##    '''test if Cree output is correct.'''
    ##    parser("Cree")
    ##    output,gold = files_to_compare("tests/parsing/Cree_goldstandard.xml", "tests/parsing/Cree.json")
    ##    self.assertEqual(output, gold)
    
    ##def test_turkish(self):
    ##    parser("Turkish_KULLD")
    ##    output,gold = files_to_compare("corpora_processed/parsed/Turkish_KULLD.json", "tests/parsing/Turkish_KULLD.json")
    ##    self.assertEqual(output, gold)
    #
    
if __name__ == '__main__':
    unittest.main()

