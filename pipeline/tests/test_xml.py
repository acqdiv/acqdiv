##-*- coding: utf-8 -*-
#
#import unittest
#import re, os, sys, codecs
#
#current_dir = os.getcwd()
#sys.path.append(current_dir)
#
#import metadata as metadata
#import unittest
#import parsers as parsers
#from parsers import *
#import XMLreader as xmlreader
#
#
#
## xml parsing tests
#class TestXMLParser(unittest.TestCase):
#
#    def setUp(self):
#        self.cfg = parsers.CorpusConfigParser()
#
#class TestCreeParser(TestXMLParser):
#
#    def setUp(self):
#        super().setUp()
#        self.cfg.read("Cree.ini")
#        self.infile = codecs.open("../corpora/test/Cree.xml", "r", "utf-8")
#        self.file_path = "../corpora/test/Cree.xml"
#        #self.xmlreader = xmlreader.ACQDIVCorpusReader(self.cfg,self.infile) #??
#        ## ACQDIVCorpusReader(corpus_root, '.*.xml') ?? Where does the .ini come in?
#        self.parser = SessionParser.create_parser(self.cfg, self.file_path) ## currently creates json parser, but needs to create xml-parser!
#
#    #def test_xmlfile_loaded(self):
#    #    """ Test if Cree XML object was loaded """
#    #    pass
#    #    #self.assertFalse(self.xmlreader == None)
#    #    # TODO
#    
#    #def test_utterances(self):
#    #    """ Test if all Cree utterances from the test file are loaded """
#    #    self.assertEqual(len(list(self.parser.next_utterance())), 11)
#        
#        
#    #def test_sentence_type(self):
#    #    """ Test if get_sentence_type() works for Cree """
#    #    # TODO
#    #    pass
#    #    
#    #def test_clean_utterance(self):
#    #    """ Test if clean_utterance() works for Cree"""
#    #    # example frm toolbox below
#    #    #self.assertEqual(self.toolbx.clean_utterance('eto nado udalitq [xxx] i eto [?] tozhe'), 'eto nado udalitq  i eto  tozhe')
#    #    # TODO
#    #    pass
#    #    
#    #def test_get_words(self):
#    #    """ Test if get_words() works for Cree """
#    #    # get_words() should return sth like this for the first utterance in Cree.xml test file:
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_words(input_utterance[0])), "[OrderedDict([('word_actual', 'mîn'), ('word_target', 'mîn'), ('word', 'mîn'), ('utterance_id_fk', 'u700')]), OrderedDict([('word_actual', 'kiyâ'), ('word_target', 'kiyâ'), ('word', 'kiyâ'), ('utterance_id_fk', 'u700')]), OrderedDict([('word_actual', 'îhî'), ('word_target', 'îhî'), ('word', 'îhî'), ('utterance_id_fk', 'u700')])]")
#    #    pass
#    #    
#    #def test_get_morphemes(self):
#    #    """ Test if get_morphemes() works for Cree"""
#    #    # get_morphemes should return sth like this for first utterance in Cree.xml test file:
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', 'ˈmin'), ('gloss_raw', 'again'), ('pos_raw', 'p,quant')]), OrderedDict([('morpheme', 'ˈɡa'), ('gloss_raw', 'also'), ('pos_raw', 'p,conj')]), OrderedDict([('morpheme', 'ə̃ˈhə̃'), ('gloss_raw', 'yes'), ('pos_raw', 'p,aff')])]")
#    #    pass
#    #
#    #def test_do_inference(self):
#    #    """ Test if do_inference() works for Cree """
#    #    # Hmm, how to do that for XML parser? Will there be sth like this? TODO
#    #    # below example from toolbox
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 621,621+1))
#    #    #self.assertEqual(str(self.xmlreader.do_inference(input_utterance[0])), "[OrderedDict([('utterance_id_fk', 'A00210817_622'), ('pos_raw', 'V'), ('gloss_raw', 'IMP:2:SG:IRREFL:IPFV')]), OrderedDict([('utterance_id_fk', 'A00210817_622'), ('pos_raw', 'V'), ('gloss_raw', 'IMP:2:SG:IRREFL:PFV')]), OrderedDict([('utterance_id_fk', 'A00210817_622'), ('pos_raw', 'NOUN'), ('gloss_raw', 'M:SG:ACC:INAN')])]")
#    #    pass
#    
#    
#class TestInuktitutParser(TestXMLParser):
#
#    def setUp(self):
#        super().setUp()
#        self.cfg.read("Inuktitut.ini")
#        self.infile = codecs.open("../corpora/test/Inuktitut.xml", "r", "utf-8")
#        self.file_path = "../corpora/test/Inuktitut.xml"
#        #self.xmlreader = xmlreader.ACQDIVCorpusReader(self.cfg,self.infile) #??
#        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
#        
#    #def test_xmlfile_loaded(self):
#    #    """ Test if Inuktitut XML object was loaded """
#    #    #self.assertFalse(self.xmlreader == None)
#    #    # TODO
#    #    pass
#    #
#    #def test_utterances(self):
#    #    """ Test if all Inuktitut utterances from the test file are loaded """
#    #    self.assertEqual(len(list(self.parser.next_utterance())), 27)
#    #    
#    #def test_sentence_type(self):
#    #    """ Test if get_sentence_type() works for Inuktitut """
#    #    # TODO
#    #    pass
#    #    
#    #def test_clean_utterance(self):
#    #    """ Test if clean_utterance() works for Inuktitut"""
#    #    # TODO
#    #    pass
#    #    
#    #def test_get_words(self):
#    #    """ Test if get_words() works for Inuktitut """
#    #    #get_words() for the 5th sentence in the test file should return sth like this:
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 4,4+1))
#    #    #self.assertEqual(str(self.xmlreader.get_words(input_utterance[0])), "[OrderedDict([('word_actual', 'tursuniitu'), ('word_target', 'tursuniitu'), ('word', 'tursuniitu'), ('utterance_id_fk', 'u710')]), OrderedDict([('word_actual', 'qimmianirtisijuruluulirtu'), ('word_target', 'qimmianirtisijuruluulirtu'), ('warning', 'transcription insecure'), ('word', 'qimmianirtisijuruluulirtu'), ('utterance_id_fk', 'u710')])]")
#    #
#    #def test_get_morphemes(self):
#    #    """ Test if get_morphemes() works for Inuktitut"""
#    #    # get_morphemes() should return sth like this for the 7th utterance in the test file:
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 6,6+1))
#    #    #self.assertEqual(str(self.xmlreader.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', 'vunga'), ('gloss_raw', 'IND_1sS'), ('pos_raw', 'VI')]), OrderedDict([('morpheme', 'vunga'), ('gloss_raw', 'IND_1sS'), ('pos_raw', 'VI')]), OrderedDict([('morpheme', 'vunga'), ('gloss_raw', 'IND_1sS'), ('pos_raw', 'VI')])]")
#    #
#    #def test_do_inference(self):
#    #    """ Test if do_inference() works for Inuktitut """
#    #    # TODO
#    #    pass
#        
#class TestJapanese_MiiProParser(TestXMLParser):
#
#    def setUp(self):
#        super().setUp()
#        self.cfg.read("Japanese_MiiPro.ini")
#        self.infile = codecs.open("../corpora/test/Japanese_MiiPro.xml", "r", "utf-8")
#        self.file_path = "../corpora/test/Japanese_MiiPro.xml"
#        #self.xmlreader = xmlreader.ACQDIVCorpusReader(self.cfg,self.infile) #??
#        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
#        
#    #def test_xmlfile_loaded(self):
#    #    """ Test if Japanese_MiiPro XML object was loaded """
#    #    #self.assertFalse(self.xmlreader == None)
#    #    # TODO
#    #    pass
#    #
#    #def test_utterances(self):
#    #    """ Test if all MiiPro utterances from the test file are loaded """
#    #    self.assertEqual(len(list(self.parser.next_utterance())), 16)
#    #    
#    #def test_sentence_type(self):
#    #    """ Test if get_sentence_type() works for MiiPro """
#    #    # TODO
#    #    pass
#    #    
#    #def test_clean_utterance(self):
#    #    """ Test if clean_utterance() works for MiiPro"""
#    #    # TODO
#    #    pass
#    #    
#    #def test_get_words(self):
#    #    """ Test if get_words() works for MiiPro """
#    #    # get_words() should return this from the 4th utterance of the Japanese_MiiPro.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 3,3+1))
#    #    #self.assertEqual(str(self.xmlreader.get_words(input_utterance[0])), "[OrderedDict([('word_actual', 'okkii'), ('word_target', 'okkii'), ('word', 'okkii'), ('utterance_id_fk', 'u1779')]), OrderedDict([('word_actual', 'nyannyan'), ('word_target', 'nyannyan'), ('word', 'nyannyan'), ('utterance_id_fk', 'u1779')]), OrderedDict([('word_actual', 'da'), ('word_target', 'da'), ('word', 'da'), ('utterance_id_fk', 'u1779')]), OrderedDict([('word_actual', 'ne'), ('word_target', 'ne'), ('word', 'ne'), ('utterance_id_fk', 'u1779')])]")
#    #    pass
#    #
#    #def test_get_morphemes(self):
#    #    """ Test if get_morphemes() works for MiiPro"""
#    #    # get_morphemes() should return this from the 4th utterance of the Japanese_MiiPro.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 3,3+1))
#    #    #self.assertEqual(str(self.xmlreader.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', '???'), ('gloss_raw', 'PRES'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', '???'), ('gloss_raw', 'PRES'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', 'nyaanya'), ('gloss_raw', '???'), ('pos_raw', 'n:mot')]), OrderedDict([('morpheme', 'da.PRES'), ('gloss_raw', '???'), ('pos_raw', 'v:cop')]), OrderedDict([('morpheme', 'ne'), ('gloss_raw', '???'), ('pos_raw', 'ptl:fina')])]")
#    #    pass
#    #
#    #def test_do_inference(self):
#    #    """ Test if do_inference() works for MiiPro """
#    #    # TODO
#    #    pass
#
#class TestJapanese_MiyataParser(TestXMLParser):
#
#    def setUp(self):
#        super().setUp()
#        self.cfg.read("Japanese_Miyata.ini")
#        self.infile = codecs.open("../corpora/test/Japanese_Miyata.xml", "r", "utf-8")
#        self.file_path = "../corpora/test/Japanese_MiiPro.xml"
#        #self.xmlreader = xmlreader.ACQDIVCorpusReader(self.cfg,self.infile) #??
#        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
#        
#    #def test_xmlfile_loaded(self):
#    #    """ Test if Japanese_Miyata XML object was loaded """
#    #    #self.assertFalse(self.xmlreader == None)
#    #    # TODO
#    #    pass
#    #
#    #def test_utterances(self):
#    #    """ Test if all Miyata utterances from the test file are loaded """
#    #    self.assertEqual(len(list(self.parser.next_utterance())), 13)
#    #    
#    #def test_sentence_type(self):
#    #    """ Test if get_sentence_type() works for Miyata """
#    #    # TODO
#    #    pass
#    #    
#    #def test_clean_utterance(self):
#    #    """ Test if clean_utterance() works for Miyata"""
#    #    # TODO
#    #    pass
#    #    
#    #def test_get_words(self):
#    #    """ Test if get_words() works for Miyata """
#    #    # get_words() should return this from the 1st utterance of the Japanese_Miyata.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_words(input_utterance[0])), "[OrderedDict([('word_actual', 'zoosan'), ('word_target', 'zoosan'), ('word', 'zoosan')]), OrderedDict([('word_actual', 'Taishookun'), ('word_target', 'Taishookun'), ('word', 'Taishookun')])]")
#    #    pass
#    #
#    #def test_get_morphemes(self):
#    #    """ Test if get_morphemes() works for Miyata"""
#    #    # get_morphemes() should return this from the 4th utterance of the Japanese_Miyata.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', '???'), ('gloss_raw', 'san'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', '???'), ('gloss_raw', 'san'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', '???'), ('gloss_raw', 'kun'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', '???'), ('gloss_raw', 'kun'), ('pos_raw', 'sfx')])]")
#    #    pass
#    #
#    #def test_do_inference(self):
#    #    """ Test if do_inference() works for Miyata """
#    #    # TODO
#    #    pass
#        
#class TestSesothoParser(TestXMLParser):
#
#    def setUp(self):
#        super().setUp()
#        self.cfg.read("Sesotho.ini")
#        self.infile = codecs.open("../corpora/test/Sesotho.xml", "r", "utf-8")
#        self.file_path = "../corpora/test/Sesotho.xml"
#        #self.xmlreader = xmlreader.ACQDIVCorpusReader(self.cfg,self.infile) #??
#        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
#        
#    #def test_xmlfile_loaded(self):
#    #    """ Test if Sesotho XML object was loaded """
#    #    #self.assertFalse(self.xmlreader == None)
#    #    # TODO
#    #    pass
#    #
#    #def test_utterances(self):
#    #    """ Test if all Sesotho utterances from the test file are loaded """
#    #    self.assertEqual(len(list(self.parser.next_utterance())), 11)
#    #    
#    #    
#    #def test_sentence_type(self):
#    #    """ Test if get_sentence_type() works for Sesotho """
#    #    # TODO
#    #    pass
#    #    
#    #def test_clean_utterance(self):
#    #    """ Test if clean_utterance() works for Sesotho"""
#    #    # TODO
#    #    pass
#    #    
#    #def test_get_words(self):
#    #    """ Test if get_words() works for Sesotho """
#    #    # get_words() should return this from the 1st utterance of the Turkish.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_words(input_utterance[0])), "[OrderedDict([('word_actual', 'ke'), ('word_target', 'ke'), ('word', 'ke'), ('utterance_id_fk', 'u381')]), OrderedDict([('word_actual', 'Tsebo'), ('word_target', 'Tsebo'), ('word', 'Tsebo'), ('utterance_id_fk', 'u381')]), OrderedDict([('word_actual', 'o'), ('word_target', 'o'), ('word', 'o'), ('utterance_id_fk', 'u381')]), OrderedDict([('word_actual', 'ntsa'), ('word_target', 'ntsa'), ('word', 'ntsa'), ('utterance_id_fk', 'u381')]), OrderedDict([('word_actual', 'nkotla'), ('word_target', 'nkotla'), ('word', 'nkotla'), ('utterance_id_fk', 'u381')])]")
#    #    pass
#    #
#    #def test_get_morphemes(self):
#    #    """ Test if get_morphemes() works for Sesotho"""
#    #    # get_morphemes() should return this from the 4th utterance of the Sesotho.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', 'ke'), ('gloss_raw', 'cp'), ('pos_raw', 'cop')]), OrderedDict([('morpheme', 'Tsebo'), ('gloss_raw', 'a_name'), ('pos_raw', '???')]), OrderedDict([('morpheme', 'a'), ('gloss_raw', 'm^pt'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', 'a'), ('gloss_raw', 'm^pt'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', 'a'), ('gloss_raw', 'm^pt'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', 'a'), ('gloss_raw', 'm^pt'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', 'a'), ('gloss_raw', 'm^pt'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', 'a'), ('gloss_raw', 'm^pt'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', 'a'), ('gloss_raw', 'm^pt'), ('pos_raw', 'sfx')])]")
#    #    pass
#    #
#    #def test_do_inference(self):
#    #    """ Test if do_inference() works for Sesotho """
#    #    # TODO
#    #    pass
#        
#class TestTurkishParser(TestXMLParser):
#
#    def setUp(self):
#        super().setUp()
#        self.cfg.read("Turkish.ini")
#        self.infile = codecs.open("../corpora/test/Turkish.xml", "r", "utf-8")
#        self.file_path = "../corpora/test/Turkish.xml"
#        #self.xmlreader = xmlreader.ACQDIVCorpusReader(self.cfg,self.infile) #??
#        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
#    
#    #def test_xmlfile_loaded(self):
#    #    """ Test if Turkish XML object was loaded """
#    #    #self.assertFalse(self.xmlreader == None)
#    #    # TODO
#    #    pass
#    #
#    #def test_utterances(self):
#    #    """ Test if all Turkish utterances from the test file are loaded """
#    #    self.assertEqual(len(list(self.parser.next_utterance())), 14)
#    #    
#    #    
#    #def test_sentence_type(self):
#    #    """ Test if get_sentence_type() works for Turkish """
#    #    # TODO
#    #    pass
#    #    
#    #def test_clean_utterance(self):
#    #    """ Test if clean_utterance() works for Turkish"""
#    #    # TODO
#    #    pass
#    #    
#    #def test_get_words(self):
#    #    """ Test if get_words() works for Turkish """
#    #    # get_words() should return this from the 1st utterance of the Turkish.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_words(input_utterance[0])), "[OrderedDict([('word_actual', 'otur'), ('word_target', 'otur'), ('word', 'otur'), ('utterance_id_fk', 'u1925')]), OrderedDict([('word_actual', 'bakalım'), ('word_target', 'bakalım'), ('word', 'bakalım'), ('utterance_id_fk', 'u1925')])]")
#    #    pass
#    #
#    #def test_get_morphemes(self):
#    #    """ Test if get_morphemes() works for Turkish"""
#    #    # get_morphemes() should return this from the 4th utterance of the Turkish.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', '???'), ('gloss_raw', 'OPT&1P'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', '???'), ('gloss_raw', 'OPT&1P'), ('pos_raw', 'sfx')])]")
#    #    pass
#    #
#    #def test_do_inference(self):
#    #    """ Test if do_inference() works for Turkish """
#    #    # TODO
#    #    pass
#        
#class TestYucatecParser(TestXMLParser):
#
#    def setUp(self):
#        super().setUp()
#        self.cfg.read("Yucatec.ini")
#        self.infile = codecs.open("../corpora/test/Yucatec.xml", "r", "utf-8")
#        self.file_path = "../corpora/test/Yucatec.xml"
#        #self.xmlreader = xmlreader.ACQDIVCorpusReader(self.cfg,self.infile) #??
#        self.parser = SessionParser.create_parser(self.cfg, self.file_path)
#    
#    #def test_xmlfile_loaded(self):
#    #    """ Test if Yucatec XML object was loaded """
#    #    # TODO
#    #    pass
#    #
#    #def test_utterances(self):
#    #    """ Test if all Yucatec utterances from the test file are loaded """
#    #    self.assertEqual(len(list(self.parser.next_utterance())), 12)
#    #    
#    #    
#    #def test_sentence_type(self):
#    #    """ Test if get_sentence_type() works for Yucatec """
#    #    # TODO
#    #    pass
#    #    
#    #def test_clean_utterance(self):
#    #    """ Test if clean_utterance() works for Yucatec"""
#    #    # TODO
#    #    pass
#    #    
#    #def test_get_words(self):
#    #    """ Test if get_words() works for Yucatec """
#    #    # get_words() should return this from the 1st utterance of the Yucatec.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_words(input_utterance[0])), "[OrderedDict([('word_actual', '???'), ('word_target', 'xáchet'), ('word', 'xáchet'), ('utterance_id_fk', 'u0')]), OrderedDict([('word_actual', '???'), ('word_target', 'apool'), ('word', 'apool'), ('utterance_id_fk', 'u0')])]")
#    #    pass
#    #
#    #def test_get_morphemes(self):
#    #    """ Test if get_morphemes() works for Yucatec"""
#    #    # get_morphemes() should return this from the 4th utterance of the Yucatec.xml test file
#    #    #input_utterance = next(islice(self.parser.next_utterance(), 0,0+1))
#    #    #self.assertEqual(str(self.xmlreader.get_morphemes(input_utterance[0])),"[OrderedDict([('morpheme', '0'), ('gloss_raw', 'IMP'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', '0'), ('gloss_raw', 'IMP'), ('pos_raw', 'sfx')]), OrderedDict([('morpheme', 'pool'), ('gloss_raw', '???'), ('pos_raw', 'S')]), OrderedDict([('morpheme', 'pool'), ('gloss_raw', '???'), ('pos_raw', 'S')])]")
#    #    pass
#    #
#    #def test_do_inference(self):
#    #    """ Test if do_inference() works for Yucatec """
#    #    # TODO
#    #    pass
#
#
#if __name__ == "__main__":
#    current_dir = os.getcwd()
#    sys.path.append(current_dir)
#    
#    import metadata as metadata
#    import time
#    import unittest
#    import parsers as parsers
#
