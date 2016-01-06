## -*- coding: utf-8 -*-

import os
import sys

current_dir = os.getcwd()
sys.path.append(current_dir)

import database_backend as db
import processors as processors
import postprocessor as pp
import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import parsers as parsers


# helper functions
def connect(corpus):
    """ Performs database connection. We can add a database settings
    from settings.py later. Returns sqlalchemy engine instance for each xml test corpus.
    """
    return db.create_engine('sqlite:///tests/test_xml_acqdiv_'+corpus+'.sqlite3', echo=False)

def make_session(corpus):
    engine = connect(corpus)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def load_database(configs, engine):
    db.create_tables(engine)

    for config in configs:
        # Parse the config file and call the sessions processor
        cfg = parsers.CorpusConfigParser()
        cfg.read(config)
        cfg.session_files = cfg.session_testfiles
            
        # Process by parsing the files and adding extracted data to the db
        c = processors.CorpusProcessor(cfg, engine)
        c.process_corpus()
        
        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        pp.update_age(cfg, engine)
        pp.unify_glosses(cfg, engine)
        
        

class XMLTestCree(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize database connection and drop and then create tables on each call.
        # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
        engine = connect('Cree')
        cls.configs = ['Cree.ini']
        load_database(cls.configs, engine)
    

    def test_sessions(self):
        """
        Test if sessions for Cree test file are loaded
        """
        session = make_session('Cree')
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(XMLTestCree.configs))
        
        s = select([db.Session])
        result = session.execute(s)
        self.assertEqual(str(result.fetchall()), "[(1, 'Cree', 'Cree', 'Cree', '2005-03-25', 'Cree', 'Cree', 'video')]")
        
        session.close()
        
        
    def test_utterances(self):
        """
        Test if all utterances for Cree test file are loaded
        """
        session = make_session('Cree')
        self.assertEqual(session.query(db.Utterance).count(), 1)
        
        s_cree = select([db.Utterance])
        result_cree = session.execute(s_cree)
        self.assertEqual(str(result_inuk.fetchall()), "[(1, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u702', 'LOU', 'SHA', 'here shanley have a plate', 'here shanley have a plate', 'here shanley. have a plate.', 'default', '3386.000', None, '0:56:26', None, 'here shanley have a plate', None, None, None, None, 'not glossed'), (13, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u705', 'ALI', 'DAN', 'aunatakka', 'aunatakka', \"it's this one here.\", 'default', '3399.000', None, '0:56:39', None, 'aunatakka', None, None, None, 'points at a piece of meat', None), (14, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u706', 'ALI', 'ALI', 'una', 'una', 'this one.', 'default', '3401.000', None, '0:56:41', None, 'una', None, None, None, None, None), (15, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u707', 'ALI', 'ALI', 'una', 'una', 'this one.', 'default', '3402.000', None, '0:56:42', None, 'una', None, None, None, None, None), (16, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u710', 'MAR', 'JUP', 'tursuniitu qimmianirtisijuruluulirtu', 'tursuniitu qimmianirtisijuruluulirtu', '<he is letting> [?] the porch smell like a dog.', 'default', '1279.000', None, '00:21:19', None, 'tursuniitu qimmianirtisijuruluulirtu', None, None, None, 'COR', 'not glossed'), (17, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u711', 'DAN', 'ALI', 'angijuaa', 'angijuaa', 'the big one .', 'default', '1628.000', None, '0:27:08', None, 'angijuaa', None, None, None, None, 'not glossed; not glossed'), (18, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u703', 'ALI', 'LOU', '???tutusivunga', '???tutusivunga', \"xxx-I'm having some.\", 'default', '3389.000', None, '0:56:29', None, '???tutusivunga', None, None, None, '$CHK:u', None), (19, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u714', 'ALI', 'DAN', '??? ???mat mat??? ???mat???', '??? ???mat mat??? ???mat???', None, 'default', '310.000', None, '00:05:10', None, '??? ???mat mat??? ???mat???', None, None, None, 'commenting on the keyboard with the plug', 'not glossed'), (20, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u704', 'ALI', 'DAN', 'un anna', 'un anna', 'this one.', 'default', '3396.000', None, '0:56:36', None, 'un anna', None, None, None, None, None), (21, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u708', 'JUP', 'MAR', '', '', '0 [=! whining].', 'action', '1905.000', None, '0:31:45', None, '', None, None, None, 'complaining and still unhappy about not being able to go outside; COR', 'empty utterance; not glossed'), (22, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u709', 'ALI', 'himself', None, None, '0 [=!singing] .', 'action', '146.000', None, '0:02:26', None, None, None, None, None, None, 'empty utterance; not glossed'), (23, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u712', 'JUP', 'SLF', 'Qangattajuuraaluk', 'Qangattajuuraaluk', 'Big airplane !', 'exclamation', '160.000', None, '00:02:40', None, 'Qangattajuuraaluk', None, None, None, None, 'not glossed'), (24, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u713', 'ALI', 'DAN', 'nauk ???', 'nauk ???', \"Let's see xxx .\", 'default', '262.000', None, '00:04:22', None, 'nauk ???', None, None, None, None, None), (25, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u715', 'ALI', 'LOU', 'av uvanga', 'av uvanga', 'it belongs to me .', 'default', '702.000', None, '00:11:42', None, 'av uvanga', None, None, None, None, None), (26, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u716', 'ALI', 'DAN', '???', '???', 'xxx [=? that is mine] .', 'default', '494.000', None, '00:08:14', None, '???', None, None, None, 'speaking very softly; difficult to understand; $CHK:c', None), (27, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u717', 'ALI', 'LOU', 'avungaunna', 'avungaunna', 'it comes from there .', 'default', '705.000', None, '00:11:45', None, 'avungaunna', None, None, None, None, 'gloss insecure'), (28, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u718', 'JUP', 'ITT', 'Shaamiitumi', 'Shaamiitumi', 'At the (side)-table ...', 'trail off', '585.000', None, '00:09:45', None, 'Shaamiitumi', None, None, None, \"JUP's talking about the tool he took from the sideandtable.\", None), (29, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u719', 'DAI', 'MAE', 'Imminingai langavait takugit hai imaak Ima takugit Mae hai takugit imaak Imaak Imaa hai Imaa hai imaak imaak imaak Laurilli', 'Imminingai langavait takugit hai imaak Ima takugit Mae hai takugit imaak Imaak Imaa hai Imaa hai imaak imaak imaak Laurilli', 'Like this Do it by yourself Like this Look Mae, like this See See Like this Like this Like this Your turn .', 'default', '2343.000', None, '00:39:03', None, 'Imminingai langavait takugit hai imaak Ima takugit Mae hai takugit imaak Imaak Imaa hai Imaa hai imaak imaak imaak Laurilli', None, None, None, 'showing MAE how to braid', None), (30, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u720', 'ALI', 'DAN', 'Naa naa', 'Naa naa', 'No no .', 'default', '40.000', None, '00:00:40', None, 'Naa naa', None, None, None, None, None), (31, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u721', 'JUP', 'MAR', 'qaungatillaunga', 'qaungatillaunga', 'make me go out [=? make me go here] [=? make me go up there] .', 'default', '2152.000', None, '00:35:52', None, 'qaungatillaunga', None, None, None, 'sitting on the floor looking at MAR; $CHK', None), (32, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u722', 'JUP', 'MAR', 'nimattingillugu kuvisuuraaluu', 'nimattingillugu kuvisuuraaluu', \"Don't shake or move It will spill all over ?\", 'question', '942.000', None, '00:15:42', None, 'nimattingillugu kuvisuuraaluu', None, None, None, 'referring to the popcan.', None), (33, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u723', 'JUP', None, 'Anana', 'Anana', 'Ouch !', 'exclamation', '5013.000', None, '01:23:33', None, 'Anana', None, None, None, None, 'not glossed'), (34, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u724', 'JUP', 'ITT', '', '', '0 .', 'action', '977.000', None, '00:16:17', None, '', None, None, None, 'points to telephone; COR', 'empty utterance; not glossed'), (35, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u725', 'ALI', 'DAN', '', '', '0 [=! vocalizing] .', 'action', '428.000', None, '00:07:08', None, '', None, None, None, None, 'empty utterance; not glossed'), (36, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u152', 'ALI', 'SLF', 'una apisimajuq', 'una apisimajuq', 'this one here is broken .', 'default', '550.000', None, '00:09:10', None, 'una apisimajuq', None, None, None, 'inspecting his chair', 'gloss insecure'), (37, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u171', 'ALI', 'DAN', 'aju ajuksigatta', 'aju ajuksigatta', \"stuck [//] we're stuck .\", 'default', '581.000', None, '00:09:41', None, 'aju ajuksigatta', None, None, None, None, None), (38, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u109', 'ALI', 'DAN', 'Kaanata Kaanata Kaanata Kaanata Kaanata Kaanata', 'Kaanata Kaanata Kaanata Kaanata Kaanata Kaanata', 'Canada .', 'default', None, None, None, None, 'Kaanata Kaanata Kaanata Kaanata Kaanata Kaanata', None, None, None, None, 'broken alignment full_word : segments/glosses')]")
        
        session.close()
        
        
    def test_words(self):
        """
        Test if all words for Cree test file are loaded
        """
        session = make_session('Cree')
        self.assertEqual(session.query(db.Word).count(), 22)
        
        s_cree = select([db.Word])
        result_cree = session.execute(s_cree)
        self.assertEqual(str(result_cree.fetchall()), "[(1, 'Cree', 'u700', 'Cree', 'Cree', 'mîn', 'mîn', 'mîn', None), (2, 'Cree', 'u700', 'Cree', 'Cree', 'kiyâ', 'kiyâ', 'kiyâ', None), (3, 'Cree', 'u700', 'Cree', 'Cree', 'îhî', 'îhî', 'îhî', None), (4, 'Cree', 'u701', 'Cree', 'Cree', 'kiyâ', 'kiyâ', 'kiyâ', None), (5, 'Cree', 'u701', 'Cree', 'Cree', None, None, None, 'See warning in Utterance table at: Cree, u701 '), (6, 'Cree', 'u702', 'Cree', 'Cree', 'Nuwich', 'Nuwich', 'Nuwich', None), (7, 'Cree', 'u702', 'Cree', 'Cree', 'uwiitaayimaa', 'uwiitaayimaa', 'uwiitaayimaa', None), (8, 'Cree', 'u704', 'Cree', 'Cree', 'Miin', 'Miin', 'Miin', None), (9, 'Cree', 'u704', 'Cree', 'Cree', 'aa', 'aa', 'aa', None), (10, 'Cree', 'u705', 'Cree', 'Cree', 'mîn', 'mîn', 'mîn', None), (11, 'Cree', 'u705', 'Cree', 'Cree', 'kiyâ', 'kiyâ', 'kiyâ', None), (12, 'Cree', 'u707', 'Cree', 'Cree', 'mâu', 'mâu', 'mâu', None), (13, 'Cree', 'u710', 'Cree', 'Cree', 'Aakuu', 'Aakuu', 'Aakuu', None), (14, 'Cree', 'u710', 'Cree', 'Cree', 'maak', 'maak', 'maak', None), (15, 'Cree', 'u710', 'Cree', 'Cree', 'aa', 'aa', 'aa', None), (16, 'Cree', 'u710', 'Cree', 'Cree', 'naatihwaahtaau', 'naatihwaahtaau', 'naatihwaahtaau', None), (17, 'Cree', 'u710', 'Cree', 'Cree', 'aai', 'aai', 'aai', None), (18, 'Cree', 'u706', 'Cree', 'Cree', 'two', 'two', 'two', None), (19, 'Cree', 'u703', 'Cree', 'Cree', 'tv', 'tv', 'tv', None), (20, 'Cree', 'u708', 'Cree', 'Cree', '???', '???', '???', None), (21, 'Cree', 'u708', 'Cree', 'Cree', None, None, None, 'See warning in Utterance table at: Cree, u708 '), (22, 'Cree', 'u709', 'Cree', 'Cree', '???', '???', '???', None)]")
        
        session.close()
        
    def test_morphemes(self):
        """
        Test if all morphemes for Cree test file are loaded
        """
        session = make_session('Cree')
        self.assertEqual(session.query(db.Morpheme).count(), 9)
        
        s_cree = select([db.Morpheme])
        result_cree = session.execute(s_cree)
        self.assertEqual(str(result_cree.fetchall()), "[(1, 'Cree', 'u700', 'Cree', 'Cree', 'target', 'ˈmin', 'again', 'again', 'p,quant', None), (2, 'Cree', 'u700', 'Cree', 'Cree', 'target', 'ˈɡa', 'also', 'also', 'p,conj', None), (3, 'Cree', 'u700', 'Cree', 'Cree', 'target', 'ə̃ˈhə̃', 'yes', 'yes', 'p,aff', None), (4, 'Cree', 'u701', 'Cree', 'Cree', 'target', 'ˈɡa', 'also', 'also', 'p,conj', None), (5, 'Cree', 'u705', 'Cree', 'Cree', 'target', 'ˈmin', 'again', 'again', 'p,quant', None), (6, 'Cree', 'u705', 'Cree', 'Cree', 'target', 'ˈɡa', 'also', 'also', 'p,conj', None), (7, 'Cree', 'u707', 'Cree', 'Cree', 'target', 'ˈmaw', 'here.it.is', 'here.it.is', 'p,dem', None), (8, 'Cree', 'u706', 'Cree', 'Cree', 'target', 'tʰu', 'two', 'two', 'Eng', None), (9, 'Cree', 'u703', 'Cree', 'Cree', 'target', 'ˈtʰivi', 'tv', 'tv', 'Eng', None)]")
        
        session.close()
    
    def test_speakers(self):
        """
        Test if all speakers for Cree test file are loaded
        """
        session = make_session('Cree')
        self.assertEqual(session.query(db.Speaker).count(), 2)
        
        s_cree = select([db.Speaker])
        result_cree = session.execute(s_cree)
        self.assertEqual(str(result_cree.fetchall()), "[(1, 'Cree', 'Cree', 'Cree', 'CHI', 'Ani', 'P2Y1M14D', '2;1.14', 774, 'female', 'Female', 'Target_Child', 'Target_Child', 'Target_Child', None, '2003-01-24'), (2, 'Cree', 'Cree', 'Cree', 'DAN', 'Daniel', 'P3Y7M19D', '3;7.19', 1324, 'male', 'Male', 'Brother', 'Brother', 'Child', None, None)]")
        
        session.close()
        
    def test_uniquespeakers(self):
        """
        Test if all unique speakers for Cree test file are loaded
        """
        session = make_session('Cree')
        self.assertEqual(session.query(db.Uniquespeakers).count(),2)
        s_cree = select([db.Uniquespeaker])
        result_cree = session.execute(s_cree)
        self.assertEqual(str(result_cree.fetchall()), "[(1, 'CHI', 'Ani', '2003-01-24', 'Female', 'Cree', 'Target_Child'), (2, 'DAN', 'Daniel', None, 'Male', 'Cree', 'Child')]")
        
        session.close()
        
        
        
class XMLTestInuktitut(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = connect('Inuktitut')
        cls.configs = ['Inuktitut.ini']
        load_database(cls.configs, engine)
    

    def test_sessions(self):
        """
        Test if sessions for Inuktitut test file are loaded
        """
        session = make_session('Inuktitut')
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(XMLTestInuktitut.configs))
        
        s = select([db.Session])
        result = session.execute(s)
        self.assertEqual(str(result.fetchall()), "[(1, 'Inuktitut', 'Inuktitut', 'Inuktitut', '1989-03-03', 'Inuktitut', 'Inuktitut', 'video unlinked')]")
        
        session.close()
        
        
    def test_utterances(self):
        """
        Test if all utterances for Inuktitut test file are loaded
        """
        session = make_session('Inuktitut')
        self.assertEqual(session.query(db.Utterance).count(), 27)
        
        s_inuk = select([db.Utterance])
        result_inuk = session.execute(s_inuk)
        self.assertEqual(str(result_inuk.fetchall()),"[(1, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u702', 'LOU', 'SHA', 'here shanley have a plate', 'here shanley have a plate', 'here shanley. have a plate.', 'default', '3386.000', None, '0:56:26', None, 'here shanley have a plate', None, None, None, None, 'not glossed'), (2, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u705', 'ALI', 'DAN', 'aunatakka', 'aunatakka', \"it's this one here.\", 'default', '3399.000', None, '0:56:39', None, 'aunatakka', None, None, None, 'points at a piece of meat', None), (3, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u706', 'ALI', 'ALI', 'una', 'una', 'this one.', 'default', '3401.000', None, '0:56:41', None, 'una', None, None, None, None, None), (4, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u707', 'ALI', 'ALI', 'una', 'una', 'this one.', 'default', '3402.000', None, '0:56:42', None, 'una', None, None, None, None, None), (5, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u710', 'MAR', 'JUP', 'tursuniitu qimmianirtisijuruluulirtu', 'tursuniitu qimmianirtisijuruluulirtu', '<he is letting> [?] the porch smell like a dog.', 'default', '1279.000', None, '00:21:19', None, 'tursuniitu qimmianirtisijuruluulirtu', None, None, None, 'COR', 'not glossed'), (6, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u711', 'DAN', 'ALI', 'angijuaa', 'angijuaa', 'the big one .', 'default', '1628.000', None, '0:27:08', None, 'angijuaa', None, None, None, None, 'not glossed; not glossed'), (7, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u703', 'ALI', 'LOU', '???tutusivunga', '???tutusivunga', \"xxx-I'm having some.\", 'default', '3389.000', None, '0:56:29', None, '???tutusivunga', None, None, None, '$CHK:u', None), (8, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u714', 'ALI', 'DAN', '??? ???mat mat??? ???mat???', '??? ???mat mat??? ???mat???', None, 'default', '310.000', None, '00:05:10', None, '??? ???mat mat??? ???mat???', None, None, None, 'commenting on the keyboard with the plug', 'not glossed'), (9, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u704', 'ALI', 'DAN', 'un anna', 'un anna', 'this one.', 'default', '3396.000', None, '0:56:36', None, 'un anna', None, None, None, None, None), (10, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u708', 'JUP', 'MAR', '', '', '0 [=! whining].', 'action', '1905.000', None, '0:31:45', None, '', None, None, None, 'complaining and still unhappy about not being able to go outside; COR', 'empty utterance; not glossed'), (11, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u709', 'ALI', 'himself', None, None, '0 [=!singing] .', 'action', '146.000', None, '0:02:26', None, None, None, None, None, None, 'empty utterance; not glossed'), (12, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u712', 'JUP', 'SLF', 'Qangattajuuraaluk', 'Qangattajuuraaluk', 'Big airplane !', 'exclamation', '160.000', None, '00:02:40', None, 'Qangattajuuraaluk', None, None, None, None, 'not glossed'), (13, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u713', 'ALI', 'DAN', 'nauk ???', 'nauk ???', \"Let's see xxx .\", 'default', '262.000', None, '00:04:22', None, 'nauk ???', None, None, None, None, None), (14, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u715', 'ALI', 'LOU', 'av uvanga', 'av uvanga', 'it belongs to me .', 'default', '702.000', None, '00:11:42', None, 'av uvanga', None, None, None, None, None), (15, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u716', 'ALI', 'DAN', '???', '???', 'xxx [=? that is mine] .', 'default', '494.000', None, '00:08:14', None, '???', None, None, None, 'speaking very softly; difficult to understand; $CHK:c', None), (16, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u717', 'ALI', 'LOU', 'avungaunna', 'avungaunna', 'it comes from there .', 'default', '705.000', None, '00:11:45', None, 'avungaunna', None, None, None, None, 'gloss insecure'), (17, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u718', 'JUP', 'ITT', 'Shaamiitumi', 'Shaamiitumi', 'At the (side)-table ...', 'trail off', '585.000', None, '00:09:45', None, 'Shaamiitumi', None, None, None, \"JUP's talking about the tool he took from the sideandtable.\", None), (18, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u719', 'DAI', 'MAE', 'Imminingai langavait takugit hai imaak Ima takugit Mae hai takugit imaak Imaak Imaa hai Imaa hai imaak imaak imaak Laurilli', 'Imminingai langavait takugit hai imaak Ima takugit Mae hai takugit imaak Imaak Imaa hai Imaa hai imaak imaak imaak Laurilli', 'Like this Do it by yourself Like this Look Mae, like this See See Like this Like this Like this Your turn .', 'default', '2343.000', None, '00:39:03', None, 'Imminingai langavait takugit hai imaak Ima takugit Mae hai takugit imaak Imaak Imaa hai Imaa hai imaak imaak imaak Laurilli', None, None, None, 'showing MAE how to braid', None), (19, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u720', 'ALI', 'DAN', 'Naa naa', 'Naa naa', 'No no .', 'default', '40.000', None, '00:00:40', None, 'Naa naa', None, None, None, None, None), (20, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u721', 'JUP', 'MAR', 'qaungatillaunga', 'qaungatillaunga', 'make me go out [=? make me go here] [=? make me go up there] .', 'default', '2152.000', None, '00:35:52', None, 'qaungatillaunga', None, None, None, 'sitting on the floor looking at MAR; $CHK', None), (21, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u722', 'JUP', 'MAR', 'nimattingillugu kuvisuuraaluu', 'nimattingillugu kuvisuuraaluu', \"Don't shake or move It will spill all over ?\", 'question', '942.000', None, '00:15:42', None, 'nimattingillugu kuvisuuraaluu', None, None, None, 'referring to the popcan.', None), (22, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u723', 'JUP', None, 'Anana', 'Anana', 'Ouch !', 'exclamation', '5013.000', None, '01:23:33', None, 'Anana', None, None, None, None, 'not glossed'), (23, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u724', 'JUP', 'ITT', '', '', '0 .', 'action', '977.000', None, '00:16:17', None, '', None, None, None, 'points to telephone; COR', 'empty utterance; not glossed'), (24, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u725', 'ALI', 'DAN', '', '', '0 [=! vocalizing] .', 'action', '428.000', None, '00:07:08', None, '', None, None, None, None, 'empty utterance; not glossed'), (25, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u152', 'ALI', 'SLF', 'una apisimajuq', 'una apisimajuq', 'this one here is broken .', 'default', '550.000', None, '00:09:10', None, 'una apisimajuq', None, None, None, 'inspecting his chair', 'gloss insecure'), (26, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u171', 'ALI', 'DAN', 'aju ajuksigatta', 'aju ajuksigatta', \"stuck [//] we're stuck .\", 'default', '581.000', None, '00:09:41', None, 'aju ajuksigatta', None, None, None, None, None), (27, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'u109', 'ALI', 'DAN', 'Kaanata Kaanata Kaanata Kaanata Kaanata Kaanata', 'Kaanata Kaanata Kaanata Kaanata Kaanata Kaanata', 'Canada .', 'default', None, None, None, None, 'Kaanata Kaanata Kaanata Kaanata Kaanata Kaanata', None, None, None, None, 'broken alignment full_word : segments/glosses')]")
        
        session.close()
        
        
    def test_words(self):
        """
        Test if all words for Inuktitut test file are loaded
        """
        session = make_session('Inuktitut')
        self.assertEqual(session.query(db.Word).count(), 63)
        
        s_inuk = select([db.Word])
        result_inuk = session.execute(s_inuk)
        self.assertEqual(str(result_inuk.fetchall()), "[(1, 'Inuktitut', 'u702', 'Inuktitut', 'Inuktitut', 'here', 'here', 'here', None), (2, 'Inuktitut', 'u702', 'Inuktitut', 'Inuktitut', 'shanley', 'shanley', 'shanley', None), (3, 'Inuktitut', 'u702', 'Inuktitut', 'Inuktitut', 'have', 'have', 'have', None), (4, 'Inuktitut', 'u702', 'Inuktitut', 'Inuktitut', 'a', 'a', 'a', None), (5, 'Inuktitut', 'u702', 'Inuktitut', 'Inuktitut', 'plate', 'plate', 'plate', None), (6, 'Inuktitut', 'u705', 'Inuktitut', 'Inuktitut', 'aunatakka', 'aunatakka', 'aunatakka', None), (7, 'Inuktitut', 'u706', 'Inuktitut', 'Inuktitut', 'una', 'una', 'una', None), (8, 'Inuktitut', 'u707', 'Inuktitut', 'Inuktitut', 'una', 'una', 'una', None), (9, 'Inuktitut', 'u710', 'Inuktitut', 'Inuktitut', 'tursuniitu', 'tursuniitu', 'tursuniitu', None), (10, 'Inuktitut', 'u710', 'Inuktitut', 'Inuktitut', 'qimmianirtisijuruluulirtu', 'qimmianirtisijuruluulirtu', 'qimmianirtisijuruluulirtu', 'transcription insecure'), (11, 'Inuktitut', 'u711', 'Inuktitut', 'Inuktitut', 'angijuaa', 'angijuaa', 'angijuaa', None), (12, 'Inuktitut', 'u703', 'Inuktitut', 'Inuktitut', '???tutusivunga', '???tutusivunga', '???tutusivunga', None), (13, 'Inuktitut', 'u714', 'Inuktitut', 'Inuktitut', '???', '???', '???', None), (14, 'Inuktitut', 'u714', 'Inuktitut', 'Inuktitut', '???mat', '???mat', '???mat', None), (15, 'Inuktitut', 'u714', 'Inuktitut', 'Inuktitut', 'mat???', 'mat???', 'mat???', None), (16, 'Inuktitut', 'u714', 'Inuktitut', 'Inuktitut', '???mat???', '???mat???', '???mat???', None), (17, 'Inuktitut', 'u704', 'Inuktitut', 'Inuktitut', 'un', 'un', 'un', None), (18, 'Inuktitut', 'u704', 'Inuktitut', 'Inuktitut', 'anna', 'anna', 'anna', None), (19, 'Inuktitut', 'u712', 'Inuktitut', 'Inuktitut', 'Qangattajuuraaluk', 'Qangattajuuraaluk', 'Qangattajuuraaluk', None), (20, 'Inuktitut', 'u713', 'Inuktitut', 'Inuktitut', 'nauk', 'nauk', 'nauk', None), (21, 'Inuktitut', 'u713', 'Inuktitut', 'Inuktitut', '???', '???', '???', None), (22, 'Inuktitut', 'u715', 'Inuktitut', 'Inuktitut', 'av', 'av', '???', 'not glossed'), (23, 'Inuktitut', 'u715', 'Inuktitut', 'Inuktitut', 'uvanga', 'uvanga', 'uvanga', None), (24, 'Inuktitut', 'u716', 'Inuktitut', 'Inuktitut', '???', '???', 'unaliuna piga', None), (25, 'Inuktitut', 'u717', 'Inuktitut', 'Inuktitut', 'avungaunna', 'avungaunna', 'avungaunna', None), (26, 'Inuktitut', 'u718', 'Inuktitut', 'Inuktitut', 'Shaamiitumi', 'Shaamiitumi', 'Shaamiitumi', None), (27, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'Imminingai', 'Imminingai', 'Imminingai', None), (28, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'langavait', 'langavait', 'langavait', None), (29, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'takugit', 'takugit', 'takugit', None), (30, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'hai', 'hai', 'hai', None), (31, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'imaak', 'imaak', 'imaak', None), (32, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'Ima', 'Ima', 'Ima', None), (33, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'takugit', 'takugit', 'takugit', None), (34, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'Mae', 'Mae', 'Mae', None), (35, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'hai', 'hai', 'hai', None), (36, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'takugit', 'takugit', 'takugit', None), (37, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'imaak', 'imaak', 'imaak', None), (38, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'Imaak', 'Imaak', 'Imaak', None), (39, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'Imaa', 'Imaa', 'Imaa', None), (40, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'hai', 'hai', 'hai', None), (41, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'Imaa', 'Imaa', 'Imaa', None), (42, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'hai', 'hai', 'hai', None), (43, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'imaak', 'imaak', 'imaak', None), (44, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'imaak', 'imaak', 'imaak', None), (45, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'imaak', 'imaak', 'imaak', None), (46, 'Inuktitut', 'u719', 'Inuktitut', 'Inuktitut', 'Laurilli', 'Laurilli', 'Laurilli', None), (47, 'Inuktitut', 'u720', 'Inuktitut', 'Inuktitut', 'Naa', 'Naa', 'Naa', None), (48, 'Inuktitut', 'u720', 'Inuktitut', 'Inuktitut', 'naa', 'naa', 'naa', None), (49, 'Inuktitut', 'u721', 'Inuktitut', 'Inuktitut', 'qaungatillaunga', 'qaungatillaunga', 'maungatillaunga', None), (50, 'Inuktitut', 'u722', 'Inuktitut', 'Inuktitut', 'nimattingillugu', 'nimattingillugu', 'nimattingillugu', None), (51, 'Inuktitut', 'u722', 'Inuktitut', 'Inuktitut', 'kuvisuuraaluu', 'kuvisuuraaluu', 'kuvisuuraaluu', None), (52, 'Inuktitut', 'u723', 'Inuktitut', 'Inuktitut', 'Anana', 'Anana', 'Anana', None), (53, 'Inuktitut', 'u152', 'Inuktitut', 'Inuktitut', 'una', 'una', 'una', None), (54, 'Inuktitut', 'u152', 'Inuktitut', 'Inuktitut', 'apisimajuq', 'apisimajuq', 'napisimajuq', None), (55, 'Inuktitut', 'u171', 'Inuktitut', 'Inuktitut', 'aju', 'aju', 'ajursi', None), (56, 'Inuktitut', 'u171', 'Inuktitut', 'Inuktitut', 'ajuksigatta', 'ajuksigatta', 'ajuksigatta', None), (57, 'Inuktitut', 'u109', 'Inuktitut', 'Inuktitut', 'Kaanata', 'Kaanata', 'Kaanata', None), (58, 'Inuktitut', 'u109', 'Inuktitut', 'Inuktitut', 'Kaanata', 'Kaanata', 'Kaanata', None), (59, 'Inuktitut', 'u109', 'Inuktitut', 'Inuktitut', 'Kaanata', 'Kaanata', 'Kaanata', None), (60, 'Inuktitut', 'u109', 'Inuktitut', 'Inuktitut', 'Kaanata', 'Kaanata', 'Kaanata', None), (61, 'Inuktitut', 'u109', 'Inuktitut', 'Inuktitut', 'Kaanata', 'Kaanata', 'Kaanata', None), (62, 'Inuktitut', 'u109', 'Inuktitut', 'Inuktitut', 'Kaanata', 'Kaanata', 'Kaanata', None), (63, 'Inuktitut', 'u109', 'Inuktitut', 'Inuktitut', None, None, None, 'See warning in Utterance table at: Inuktitut, u109 ')]")
        
        session.close()
        
        
    def test_morphemes(self):
        """
        Test if all morphemes for Inuktitut test file are loaded
        """
        session = make_session('Inuktitut')
        self.assertEqual(session.query(db.Morpheme).count(), 82)
        
        s_inuk = select([db.Morpheme])
        result_inuk = session.execute(s_inuk)
        self.assertEqual(str(result_inuk.fetchall()),"[(1, 'Inuktitut', 'u705', None, 'Inuktitut', 'Inuktitut', 'target', 'u', 'here.SG_ST', 'here.STAT.SG', 'DR', None), (2, 'Inuktitut', 'u705', None, 'Inuktitut', 'Inuktitut', 'target', 'na', 'ABS_SG', 'ABS.SG', 'DI', None), (3, 'Inuktitut', 'u705', None, 'Inuktitut', 'Inuktitut', 'target', 'tagga', 'there_it_is', 'there_it_is', 'DEM', None), (4, 'Inuktitut', 'u706', None, 'Inuktitut', 'Inuktitut', 'target', 'u', 'here.SG_ST', 'here.STAT.SG', 'DR', None), (5, 'Inuktitut', 'u706', None, 'Inuktitut', 'Inuktitut', 'target', 'na', 'ABS_SG', 'ABS.SG', 'DI', None), (6, 'Inuktitut', 'u707', None, 'Inuktitut', 'Inuktitut', 'target', 'u', 'here.SG_ST', 'here.STAT.SG', 'DR', None), (7, 'Inuktitut', 'u707', None, 'Inuktitut', 'Inuktitut', 'target', 'na', 'ABS_SG', 'ABS.SG', 'DI', None), (8, 'Inuktitut', 'u703', None, 'Inuktitut', 'Inuktitut', 'target', '???', '???', '???', '???', None), (9, 'Inuktitut', 'u703', None, 'Inuktitut', 'Inuktitut', 'target', 'si', 'PRSP', 'PRS', 'VV.ASP', None), (10, 'Inuktitut', 'u703', None, 'Inuktitut', 'Inuktitut', 'target', 'vunga', 'IND_1sS', 'IND1.1SG.S', 'VI', None), (11, 'Inuktitut', 'u704', None, 'Inuktitut', 'Inuktitut', 'target', 'u', 'here.SG_ST', 'here.STAT.SG', 'DR', None), (12, 'Inuktitut', 'u704', None, 'Inuktitut', 'Inuktitut', 'target', 'u', 'here.SG_ST', 'here.STAT.SG', 'DR', None), (13, 'Inuktitut', 'u704', None, 'Inuktitut', 'Inuktitut', 'target', 'na', 'ABS_SG', 'ABS.SG', 'DI', None), (14, 'Inuktitut', 'u713', None, 'Inuktitut', 'Inuktitut', 'target', 'nauk', 'where', 'where', 'WH', None), (15, 'Inuktitut', 'u713', None, 'Inuktitut', 'Inuktitut', 'target', '???', '???', '???', '???', None), (16, 'Inuktitut', 'u715', None, 'Inuktitut', 'Inuktitut', 'target', 'uvanga', '1_SG_ABS_ERG', '1SG', 'PRO', None), (17, 'Inuktitut', 'u716', None, 'Inuktitut', 'Inuktitut', 'target', '???', '???', '???', '???', None), (18, 'Inuktitut', 'u717', None, 'Inuktitut', 'Inuktitut', 'target', 'av', 'there_away', 'there_away', 'LR', None), (19, 'Inuktitut', 'u717', None, 'Inuktitut', 'Inuktitut', 'target', 'unnga', 'ALL', 'ALL', 'LI', None), (20, 'Inuktitut', 'u717', None, 'Inuktitut', 'Inuktitut', 'target', 'anngat', 'ABL', 'ABL', 'LI', None), (21, 'Inuktitut', 'u718', None, 'Inuktitut', 'Inuktitut', 'target', 'saa', 'table', 'table', 'NR', None), (22, 'Inuktitut', 'u718', None, 'Inuktitut', 'Inuktitut', 'target', 'mi', 'LOC_SG', 'LOC.SG', 'NI', None), (23, 'Inuktitut', 'u718', None, 'Inuktitut', 'Inuktitut', 'target', 'juq', 'that_which', 'that_which', 'NZ', None), (24, 'Inuktitut', 'u718', None, 'Inuktitut', 'Inuktitut', 'target', 'mik', 'MOD_SG', 'INSTR.SG', 'NI', None), (25, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'immi', 'self.ANA', 'REFL', 'PRO', None), (26, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'nik', 'MOD_PL', 'INSTR.PL', 'NI', None), (27, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'ai', 'greetings', 'greetings', 'IACT', None), (28, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'langa', 'FUT', 'FUT', 'VV.TNS', None), (29, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'vait', 'IND_2sS_3sO', 'IND1.2SG>3SG', 'VI', None), (30, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'taku', 'see', 'see', 'VR', None), (31, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'git', 'IMP_2sS', 'IMP.2SG.S', 'VI', None), (32, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'hai', 'AFF', 'ATTN', 'EXCL', None), (33, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (34, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (35, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'taku', 'see', 'see', 'VR', None), (36, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'git', 'IMP_2sS', 'IMP.2SG.S', 'VI', None), (37, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'mae', 'mae', 'mae', 'NR.PROP', None), (38, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'hai', 'AFF', 'ATTN', 'EXCL', None), (39, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'taku', 'see', 'see', 'VR', None), (40, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'git', 'IMP_2sS', 'IMP.2SG.S', 'VI', None), (41, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (42, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (43, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (44, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'hai', 'AFF', 'ATTN', 'EXCL', None), (45, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (46, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'hai', 'AFF', 'ATTN', 'EXCL', None), (47, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (48, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (49, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'imaak', 'like_this', 'like_this', 'ADV', None), (50, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'lauq', 'POL', 'POL', 'VV', None), (51, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'git', 'IMP_2sS', 'IMP.2SG.S', 'VI', None), (52, 'Inuktitut', 'u719', None, 'Inuktitut', 'Inuktitut', 'target', 'li', 'and', 'and', 'CONJ', None), (53, 'Inuktitut', 'u720', None, 'Inuktitut', 'Inuktitut', 'target', 'no', 'no', 'no', 'IACT', None), (54, 'Inuktitut', 'u720', None, 'Inuktitut', 'Inuktitut', 'target', 'no', 'no', 'no', 'IACT', None), (55, 'Inuktitut', 'u721', None, 'Inuktitut', 'Inuktitut', 'target', 'ma', 'here', 'here', 'LR', None), (56, 'Inuktitut', 'u721', None, 'Inuktitut', 'Inuktitut', 'target', 'unnga', 'ALL', 'ALL', 'LI', None), (57, 'Inuktitut', 'u721', None, 'Inuktitut', 'Inuktitut', 'target', 'aq', 'go_by_way_of', 'go_by_way_of', 'VZ', None), (58, 'Inuktitut', 'u721', None, 'Inuktitut', 'Inuktitut', 'target', 'tit', 'CAUS', 'CAUS', 'VV.VA', None), (59, 'Inuktitut', 'u721', None, 'Inuktitut', 'Inuktitut', 'target', 'lauq', 'POL', 'POL', 'VV', None), (60, 'Inuktitut', 'u721', None, 'Inuktitut', 'Inuktitut', 'target', 'nnga', 'IMP_2sS_1sO', 'IMP.2SG>1SG', 'VI', None), (61, 'Inuktitut', 'u722', None, 'Inuktitut', 'Inuktitut', 'target', 'nimak', 'move_around', 'move_around', 'VR', None), (62, 'Inuktitut', 'u722', None, 'Inuktitut', 'Inuktitut', 'target', 'tit', 'CAUS', 'CAUS', 'VV.VA', None), (63, 'Inuktitut', 'u722', None, 'Inuktitut', 'Inuktitut', 'target', 'nngit', 'NEG', 'NEG', 'VV', None), (64, 'Inuktitut', 'u722', None, 'Inuktitut', 'Inuktitut', 'target', 'lugu', 'ICM_XxS_3sO', 'CONTEMP.FUT.3SG.O', 'VI', None), (65, 'Inuktitut', 'u722', None, 'Inuktitut', 'Inuktitut', 'target', 'kuvi', 'pour', 'pour', 'VR', None), (66, 'Inuktitut', 'u722', None, 'Inuktitut', 'Inuktitut', 'target', 'suuq', 'HAB', 'HAB', 'NZ', None), (67, 'Inuktitut', 'u722', None, 'Inuktitut', 'Inuktitut', 'target', 'aluk', 'EMPH', 'EMPH', 'NN.AUG', None), (68, 'Inuktitut', 'u152', None, 'Inuktitut', 'Inuktitut', 'target', 'u', 'here.SG_ST', 'here.STAT.SG', 'DR', None), (69, 'Inuktitut', 'u152', None, 'Inuktitut', 'Inuktitut', 'target', 'na', 'ABS_SG', 'ABS.SG', 'DI', None), (70, 'Inuktitut', 'u152', None, 'Inuktitut', 'Inuktitut', 'target', 'napi', 'break', 'break', 'VR', None), (71, 'Inuktitut', 'u152', None, 'Inuktitut', 'Inuktitut', 'target', 'sima', 'PERF', 'PFV', 'VV.ASP', None), (72, 'Inuktitut', 'u152', None, 'Inuktitut', 'Inuktitut', 'target', 'juq', 'PAR_3sS', 'IND2.3SG.S', 'VI', None), (73, 'Inuktitut', 'u171', None, 'Inuktitut', 'Inuktitut', 'target', 'ajursit', 'be_stuck', 'be_stuck', 'VR', None), (74, 'Inuktitut', 'u171', None, 'Inuktitut', 'Inuktitut', 'target', 'ajursit', 'be_stuck', 'be_stuck', 'VR', None), (75, 'Inuktitut', 'u171', None, 'Inuktitut', 'Inuktitut', 'target', 'gatta', 'CSV_1pS', 'CAUSAL.1PL.S', 'VI', None), (76, 'Inuktitut', 'u109', None, 'Inuktitut', 'Inuktitut', 'target', 'canada', 'canada', 'canada', 'NR.PROP', None), (77, 'Inuktitut', 'u109', None, 'Inuktitut', 'Inuktitut', 'target', 'canada', 'canada', 'canada', 'NR.PROP', None), (78, 'Inuktitut', 'u109', None, 'Inuktitut', 'Inuktitut', 'target', 'canada', 'canada', 'canada', 'NR.PROP', None), (79, 'Inuktitut', 'u109', None, 'Inuktitut', 'Inuktitut', 'target', 'canada', 'canada', 'canada', 'NR.PROP', None), (80, 'Inuktitut', 'u109', None, 'Inuktitut', 'Inuktitut', 'target', 'canada', 'canada', 'canada', 'NR.PROP', None), (81, 'Inuktitut', 'u109', None, 'Inuktitut', 'Inuktitut', 'target', 'canada', 'canada', 'canada', 'NR.PROP', None), (82, 'Inuktitut', 'u109', None, 'Inuktitut', 'Inuktitut', 'target', 'canada', 'canada', 'canada', 'NR.PROP', None)]")
        
        session.close()
    
    def test_speakers(self):
        """
        Test if all speakers for Inuktitut test file are loaded
        """
        session = make_session('Inuktitut')
        self.assertEqual(session.query(db.Speaker).count(), 2)
        
        s_inuk = select([db.Speaker])
        result_inuk = session.execute(s_inuk)
        self.assertEqual(str(result_inuk.fetchall()), "[(1, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'ALI', 'Alec', 'P2Y6M6D', '2;6.6', 916, 'male', 'Male', 'Target_Child', 'Target_Child', 'Target_Child', 'ike', '1986-08-25'), (2, 'Inuktitut', 'Inuktitut', 'Inuktitut', 'DAN', 'Daniel', 'P3Y7M19D', '3;7.19', 1324, 'male', 'Male', 'Brother', 'Brother', 'Child', 'ike', None)]")
        
        session.close()
        
    def test_uniquespeakers(self):
        """
        Test if all unique speakers for Cree test file are loaded
        """
        session = make_session('Inuktitut')
        self.assertEqual(session.query(db.Uniquespeakers).count(),2)
        
        s_inuk = select([db.Uniquespeakers])
        result_inuk = session.execute(s_inuk)
        self.assertEqual(str(result_inuk.fetchall()), "[(1, 'ALI', 'Alec', '1986-08-25', 'Male', 'Inuktitut'), (2, 'DAN', 'Daniel', None, 'Male', 'Inuktitut')]")
        
        session.close()
        
    
class XMLTestJapaneseMiiPro(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = connect('Japanese_MiiPro')
        cls.configs = ['Japanese_MiiPro.ini']
        load_database(cls.configs, engine)
    

    def test_sessions(self):
        """
        Test if sessions for JapaneseMiiPro test file are loaded
        """
        session = make_session('Japanese_MiiPro')
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(XMLTestJapaneseMiiPro.configs))
        
        s = select([db.Session])
        result = session.execute(s)
        self.assertEqual(str(result.fetchall()), "[(1, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', '1984-01-01', 'Japanese_MiiPro', 'Japanese_MiiPro', None)]")
        session.close()
        
        
    def test_utterances(self):
        """
        Test if all utterances for JapaneseMiiPro test files are loaded
        """
        session = make_session('Japanese_MiiPro')
        self.assertEqual(session.query(db.Utterance).count(), 16)
        
        s_jap_mii = select([db.Utterance])
        result_jap_mii = session.execute(s_jap_mii)
        self.assertEqual(str(result_jap_mii.fectchall()), "[(1, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1776', 'APR', None, 'nyan', 'nyan', None, 'default', '3863.507', '3864.379', '3863.507', '3864.379', 'nyan', None, None, None, None, None), (2, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1777', 'MOT', None, 'yoisho', 'yoisho', None, 'default', '3864.378', '3867.375', '3864.378', '3867.375', 'yoisho', None, None, None, None, None), (3, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1778', 'APR', None, 'nyan', 'nyan', None, 'default', '3866.342', '3867.744', '3866.342', '3867.744', 'nyan', None, None, None, None, None), (4, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1779', 'MOT', None, 'okkii nyannyan da ne', 'okkii nyannyan da ne', None, 'default', '3867.712', '3870.383', '3867.712', '3870.383', 'okkii nyannyan da ne', None, None, None, None, None), (5, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1780', 'APR', None, 'nyan', 'nyan', None, 'default', '3869.907', '3870.768', '3869.907', '3870.768', 'nyan', None, None, None, None, None), (6, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1781', 'MOT', None, 'hai oshimai', 'hai oshimai', None, 'default', '3870.592', '3873.121', '3870.592', '3873.121', 'hai oshimai', None, None, None, None, None), (7, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1784', 'MOT', None, 'minna dashita no Honochan minna dashita no Honochan minna dashita no Honochan', 'minna dashita no Honochan minna dashita no Honochan minna dashita no Honochan', None, 'question', '852.704', '860.891', '852.704', '860.891', 'minna dashita no Honochan minna dashita no Honochan minna dashita no Honochan', None, None, None, None, None), (8, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1782', 'MOT', None, 'un shou shou shou', 'un shou shou shou', None, 'default', '4410.894', '4412.159', '4410.894', '4412.159', 'un shou shou shou', None, None, None, None, None), (9, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1783', 'MOT', None, 'kuso kuso kuso hetappi', 'kuso kuso kuso hetappi', None, 'default', '4490.171', '4493.061', '4490.171', '4493.061', 'kuso kuso kuso hetappi', None, None, None, None, None), (10, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u1785', 'APR', None, 'kotchi no wa maeka yatte ii', 'kotchi no wa maeka yatte ii', None, 'question', '1314.739', '1317.889', '1314.739', '1317.889', 'kotchi no wa maeka yatte ii', None, None, None, None, None), (11, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u46', 'MOT', None, '??? chigaimasu ne', '??? chigaimasu ne', None, 'default', '87.512', '88.917', '87.512', '88.917', '??? chigaimasu ne', None, None, None, None, 'not glossed'), (12, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u189', 'APR', None, 'dakara nne chotto matte', 'dakara nne chotto matte', None, 'exclamation', '474.723', '477.585', '474.723', '477.585', 'dakara nne chotto matte', None, None, None, None, None), (13, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u23', 'APR', None, 'Akko mite te', 'Akko mite te', None, 'exclamation', '40.287', '42.265', '40.287', '42.265', 'Akko mite te', None, None, None, None, None), (14, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u32', 'APR', None, 'kore chotto kore kore kore kore n', 'kore chotto kore kore kore kore n', None, 'default', '53.396', '57.494', '53.396', '57.494', 'kore chotto kore kore kore kore n', None, None, None, None, None), (15, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u255', 'APR', None, 'dakara a omis ano re reji wa atchi', 'dakara a omis ano re reji wa atchi', None, 'default', '689.572', '695.917', '689.572', '695.917', 'dakara a omis ano re reji wa atchi', None, None, None, None, None), (16, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'u287', 'APR', None, 'aq shooboosha motte kitenee', 'aq shooboosha motte kitenee', None, 'default', '708.811', '711.464', '708.811', '711.464', 'aq shooboosha motte kitenee', None, None, None, None, None)]")
        
        session.close()
        
        
    def test_words(self):
        """
        Test if all words for JapaneseMiiPro test file are loaded
        """
        session = make_session('Japanese_MiiPro')
        self.assertEqual(session.query(db.Word).count(), 67)
        
        s_jap_mii = select([db.Word])
        result_jap_mii = session.execute(s_jap_mii)
        self.assertEqual(str(result_jap_mii.fetchall()), "[(1, 'Japanese_MiiPro', 'u1776', 'Japanese_MiiPro', 'Japanese', 'nyan', 'nyan', 'nyan', None), (2, 'Japanese_MiiPro', 'u1777', 'Japanese_MiiPro', 'Japanese', 'yoisho', 'yoisho', 'yoisho', None), (3, 'Japanese_MiiPro', 'u1778', 'Japanese_MiiPro', 'Japanese', 'nyan', 'nyan', 'nyan', None), (4, 'Japanese_MiiPro', 'u1779', 'Japanese_MiiPro', 'Japanese', 'okkii', 'okkii', 'okkii', None), (5, 'Japanese_MiiPro', 'u1779', 'Japanese_MiiPro', 'Japanese', 'nyannyan', 'nyannyan', 'nyannyan', None), (6, 'Japanese_MiiPro', 'u1779', 'Japanese_MiiPro', 'Japanese', 'da', 'da', 'da', None), (7, 'Japanese_MiiPro', 'u1779', 'Japanese_MiiPro', 'Japanese', 'ne', 'ne', 'ne', None), (8, 'Japanese_MiiPro', 'u1780', 'Japanese_MiiPro', 'Japanese', 'nyan', 'nyan', 'nyan', None), (9, 'Japanese_MiiPro', 'u1781', 'Japanese_MiiPro', 'Japanese', 'hai', 'hai', 'hai', None), (10, 'Japanese_MiiPro', 'u1781', 'Japanese_MiiPro', 'Japanese', 'oshimai', 'oshimai', 'oshimai', None), (11, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'minna', 'minna', 'minna', None), (12, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'dashita', 'dashita', 'dashita', None), (13, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'no', 'no', 'no', None), (14, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'Honochan', 'Honochan', 'Honochan', None), (15, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'minna', 'minna', 'minna', None), (16, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'dashita', 'dashita', 'dashita', None), (17, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'no', 'no', 'no', None), (18, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'Honochan', 'Honochan', 'Honochan', None), (19, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'minna', 'minna', 'minna', None), (20, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'dashita', 'dashita', 'dashita', None), (21, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'no', 'no', 'no', None), (22, 'Japanese_MiiPro', 'u1784', 'Japanese_MiiPro', 'Japanese', 'Honochan', 'Honochan', 'Honochan', None), (23, 'Japanese_MiiPro', 'u1782', 'Japanese_MiiPro', 'Japanese', 'un', 'un', 'un', None), (24, 'Japanese_MiiPro', 'u1782', 'Japanese_MiiPro', 'Japanese', 'shou', 'shou', 'soo', None), (25, 'Japanese_MiiPro', 'u1782', 'Japanese_MiiPro', 'Japanese', 'shou', 'shou', 'soo', None), (26, 'Japanese_MiiPro', 'u1782', 'Japanese_MiiPro', 'Japanese', 'shou', 'shou', 'soo', None), (27, 'Japanese_MiiPro', 'u1783', 'Japanese_MiiPro', 'Japanese', 'kuso', 'kuso', 'kuso', None), (28, 'Japanese_MiiPro', 'u1783', 'Japanese_MiiPro', 'Japanese', 'kuso', 'kuso', 'kuso', None), (29, 'Japanese_MiiPro', 'u1783', 'Japanese_MiiPro', 'Japanese', 'kuso', 'kuso', 'kuso', None), (30, 'Japanese_MiiPro', 'u1783', 'Japanese_MiiPro', 'Japanese', 'hetappi', 'hetappi', 'hetappi', None), (31, 'Japanese_MiiPro', 'u1785', 'Japanese_MiiPro', 'Japanese', 'kotchi', 'kotchi', 'kotchi', None), (32, 'Japanese_MiiPro', 'u1785', 'Japanese_MiiPro', 'Japanese', 'no', 'no', 'no', None), (33, 'Japanese_MiiPro', 'u1785', 'Japanese_MiiPro', 'Japanese', 'wa', 'wa', 'wa', None), (34, 'Japanese_MiiPro', 'u1785', 'Japanese_MiiPro', 'Japanese', 'maeka', 'maeka', 'moo', None), (35, 'Japanese_MiiPro', 'u1785', 'Japanese_MiiPro', 'Japanese', None, None, 'ikkai', 'See warning in Utterance table at: Japanese_MiiPro, u1785 '), (36, 'Japanese_MiiPro', 'u1785', 'Japanese_MiiPro', 'Japanese', 'yatte', 'yatte', 'yatte', None), (37, 'Japanese_MiiPro', 'u1785', 'Japanese_MiiPro', 'Japanese', 'ii', 'ii', 'ii', None), (38, 'Japanese_MiiPro', 'u46', 'Japanese_MiiPro', 'Japanese', '???', '???', '???', 'not glossed'), (39, 'Japanese_MiiPro', 'u46', 'Japanese_MiiPro', 'Japanese', 'chigaimasu', 'chigaimasu', 'chigaimasu', None), (40, 'Japanese_MiiPro', 'u46', 'Japanese_MiiPro', 'Japanese', 'ne', 'ne', 'ne', None), (41, 'Japanese_MiiPro', 'u189', 'Japanese_MiiPro', 'Japanese', 'dakara', 'dakara', 'dakara', None), (42, 'Japanese_MiiPro', 'u189', 'Japanese_MiiPro', 'Japanese', 'nne', 'nne', '???', 'not glossed'), (43, 'Japanese_MiiPro', 'u189', 'Japanese_MiiPro', 'Japanese', 'chotto', 'chotto', 'chotto', None), (44, 'Japanese_MiiPro', 'u189', 'Japanese_MiiPro', 'Japanese', 'matte', 'matte', 'matte', None), (45, 'Japanese_MiiPro', 'u23', 'Japanese_MiiPro', 'Japanese', 'Akko', 'Akko', 'Akko', None), (46, 'Japanese_MiiPro', 'u23', 'Japanese_MiiPro', 'Japanese', 'mite', 'mite', 'mite', None), (47, 'Japanese_MiiPro', 'u23', 'Japanese_MiiPro', 'Japanese', 'te', 'te', 'ite', None), (48, 'Japanese_MiiPro', 'u32', 'Japanese_MiiPro', 'Japanese', 'kore', 'kore', 'kore', None), (49, 'Japanese_MiiPro', 'u32', 'Japanese_MiiPro', 'Japanese', 'chotto', 'chotto', 'chotto', None), (50, 'Japanese_MiiPro', 'u32', 'Japanese_MiiPro', 'Japanese', 'kore', 'kore', 'kore', None), (51, 'Japanese_MiiPro', 'u32', 'Japanese_MiiPro', 'Japanese', 'kore', 'kore', 'kore', None), (52, 'Japanese_MiiPro', 'u32', 'Japanese_MiiPro', 'Japanese', 'kore', 'kore', 'kore', None), (53, 'Japanese_MiiPro', 'u32', 'Japanese_MiiPro', 'Japanese', 'kore', 'kore', 'kore', None), (54, 'Japanese_MiiPro', 'u32', 'Japanese_MiiPro', 'Japanese', 'n', 'n', 'n', None), (55, 'Japanese_MiiPro', 'u255', 'Japanese_MiiPro', 'Japanese', 'dakara', 'dakara', 'dakara', None), (56, 'Japanese_MiiPro', 'u255', 'Japanese_MiiPro', 'Japanese', 'a', 'a', '???', 'not glossed'), (57, 'Japanese_MiiPro', 'u255', 'Japanese_MiiPro', 'Japanese', 'omis', 'omis', 'omise', None), (58, 'Japanese_MiiPro', 'u255', 'Japanese_MiiPro', 'Japanese', 'ano', 'ano', 'ano', None), (59, 'Japanese_MiiPro', 'u255', 'Japanese_MiiPro', 'Japanese', 're', 're', '???', 'not glossed'), (60, 'Japanese_MiiPro', 'u255', 'Japanese_MiiPro', 'Japanese', 'reji', 'reji', 'reji', None), (61, 'Japanese_MiiPro', 'u255', 'Japanese_MiiPro', 'Japanese', 'wa', 'wa', 'wa', None), (62, 'Japanese_MiiPro', 'u255', 'Japanese_MiiPro', 'Japanese', 'atchi', 'atchi', 'atchi', None), (63, 'Japanese_MiiPro', 'u287', 'Japanese_MiiPro', 'Japanese', 'aq', 'aq', 'aq', None), (64, 'Japanese_MiiPro', 'u287', 'Japanese_MiiPro', 'Japanese', 'shooboosha', 'shooboosha', 'shooboosha', None), (65, 'Japanese_MiiPro', 'u287', 'Japanese_MiiPro', 'Japanese', 'motte', 'motte', 'motte', None), (66, 'Japanese_MiiPro', 'u287', 'Japanese_MiiPro', 'Japanese', 'kitenee', 'kitenee', 'kite', None), (67, 'Japanese_MiiPro', 'u287', 'Japanese_MiiPro', 'Japanese', None, None, 'inai', 'See warning in Utterance table at: Japanese_MiiPro, u287 ')]")
    
        session.close()
       
       
    def test_morphemes(self):
        """
        Test if all morphemes for JapaneseMiiPro test file are loaded
        """
        session = make_session('Japanese_MiiPro')
        self.assertEqual(session.query(db.Morpheme).count(), 83)
        
        s_jap_mii = select([db.Morpheme])
        result_jap_mii = session.execute(s_jap_mii)
        self.assertEqual(str(result_jap_mii.fetchall()), "[(1, 'Japanese_MiiPro', 'u1776', None, 'Japanese_MiiPro', 'Japanese', 'target', 'nyan', '???', '???', 'onoma', None), (2, 'Japanese_MiiPro', 'u1777', None, 'Japanese_MiiPro', 'Japanese', 'target', 'yoisho', '???', '???', 'co:i', None), (3, 'Japanese_MiiPro', 'u1778', None, 'Japanese_MiiPro', 'Japanese', 'target', 'nyan', '???', '???', 'onoma', None), (4, 'Japanese_MiiPro', 'u1779', None, 'Japanese_MiiPro', 'Japanese', 'target', 'okki', '???', '???', 'adj:mot', None), (5, 'Japanese_MiiPro', 'u1779', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'PRES', 'PRS', 'sfx', None), (6, 'Japanese_MiiPro', 'u1779', None, 'Japanese_MiiPro', 'Japanese', 'target', 'nyaanya', '???', '???', 'n:mot', None), (7, 'Japanese_MiiPro', 'u1779', None, 'Japanese_MiiPro', 'Japanese', 'target', 'da.PRES', '???', '???', 'v:cop', None), (8, 'Japanese_MiiPro', 'u1779', None, 'Japanese_MiiPro', 'Japanese', 'target', 'ne', '???', '???', 'ptl:fina', None), (9, 'Japanese_MiiPro', 'u1780', None, 'Japanese_MiiPro', 'Japanese', 'target', 'nyan', '???', '???', 'onoma', None), (10, 'Japanese_MiiPro', 'u1781', None, 'Japanese_MiiPro', 'Japanese', 'target', 'hai', '???', '???', 'co:i', None), (11, 'Japanese_MiiPro', 'u1781', None, 'Japanese_MiiPro', 'Japanese', 'target', 'o', '???', '???', 'pfx', None), (12, 'Japanese_MiiPro', 'u1781', None, 'Japanese_MiiPro', 'Japanese', 'target', 'shimaw', '???', '???', 'v:c', None), (13, 'Japanese_MiiPro', 'u1781', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'SGER', 'NMLZ', 'sfx', None), (14, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'mina', '???', '???', 'n:deic:prs', None), (15, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'das', '???', '???', 'v:c', None), (16, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'PAST', 'PST', 'sfx', None), (17, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'no', '???', '???', 'ptl:fina', None), (18, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (19, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (20, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (21, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (22, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (23, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (24, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (25, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (26, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (27, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (28, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (29, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (30, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (31, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (32, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (33, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (34, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Hono', '???', '???', 'n:prop', None), (35, 'Japanese_MiiPro', 'u1784', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'chan', 'chan', 'sfx', None), (36, 'Japanese_MiiPro', 'u1782', None, 'Japanese_MiiPro', 'Japanese', 'target', 'un', '???', '???', 'co:i', None), (37, 'Japanese_MiiPro', 'u1782', None, 'Japanese_MiiPro', 'Japanese', 'target', 'soo', '???', '???', 'co:i', None), (38, 'Japanese_MiiPro', 'u1782', None, 'Japanese_MiiPro', 'Japanese', 'target', 'soo', '???', '???', 'co:i', None), (39, 'Japanese_MiiPro', 'u1782', None, 'Japanese_MiiPro', 'Japanese', 'target', 'soo', '???', '???', 'co:i', None), (40, 'Japanese_MiiPro', 'u1783', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kuso', '???', '???', 'n', None), (41, 'Japanese_MiiPro', 'u1783', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kuso', '???', '???', 'n', None), (42, 'Japanese_MiiPro', 'u1783', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kuso', '???', '???', 'n', None), (43, 'Japanese_MiiPro', 'u1783', None, 'Japanese_MiiPro', 'Japanese', 'target', 'hetappi', '???', '???', 'n', None), (44, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kotchi', '???', '???', 'n:deic:dem', None), (45, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', 'no', '???', '???', 'ptl:case', None), (46, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', 'wa', '???', '???', 'ptl:top', None), (47, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', 'moo', '???', '???', 'adv', None), (48, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', 'ichi', 'times', 'times', 'num', None), (49, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'kai', 'kai', 'sfx', None), (50, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', 'yar', 'do/give', 'do/give', 'v:c', None), (51, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'CONN', 'CVB', 'sfx', None), (52, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', 'i', '???', '???', 'adj', None), (53, 'Japanese_MiiPro', 'u1785', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'PRES', 'PRS', 'sfx', None), (54, 'Japanese_MiiPro', 'u189', None, 'Japanese_MiiPro', 'Japanese', 'target', 'dakara', '???', '???', 'conj', None), (55, 'Japanese_MiiPro', 'u189', None, 'Japanese_MiiPro', 'Japanese', 'target', 'chotto', '???', '???', 'adv', None), (56, 'Japanese_MiiPro', 'u189', None, 'Japanese_MiiPro', 'Japanese', 'target', 'mat', '???', '???', 'v:c', None), (57, 'Japanese_MiiPro', 'u189', None, 'Japanese_MiiPro', 'Japanese', 'target', 'te', 'IMP', 'IMP', 'sfx', None), (58, 'Japanese_MiiPro', 'u23', None, 'Japanese_MiiPro', 'Japanese', 'target', 'Akko', '???', '???', 'n:prop', None), (59, 'Japanese_MiiPro', 'u23', None, 'Japanese_MiiPro', 'Japanese', 'target', 'mi', '???', '???', 'v:v', None), (60, 'Japanese_MiiPro', 'u23', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'CONN', 'CVB', 'sfx', None), (61, 'Japanese_MiiPro', 'u23', None, 'Japanese_MiiPro', 'Japanese', 'target', 'i', '???', '???', 'v:v:sub', None), (62, 'Japanese_MiiPro', 'u23', None, 'Japanese_MiiPro', 'Japanese', 'target', 'te', 'IMP', 'IMP', 'sfx', None), (63, 'Japanese_MiiPro', 'u32', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kore', '???', '???', 'n:deic:dem', None), (64, 'Japanese_MiiPro', 'u32', None, 'Japanese_MiiPro', 'Japanese', 'target', 'chotto', '???', '???', 'adv', None), (65, 'Japanese_MiiPro', 'u32', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kore', '???', '???', 'n:deic:dem', None), (66, 'Japanese_MiiPro', 'u32', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kore', '???', '???', 'n:deic:dem', None), (67, 'Japanese_MiiPro', 'u32', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kore', '???', '???', 'n:deic:dem', None), (68, 'Japanese_MiiPro', 'u32', None, 'Japanese_MiiPro', 'Japanese', 'target', 'kore', '???', '???', 'n:deic:dem', None), (69, 'Japanese_MiiPro', 'u32', None, 'Japanese_MiiPro', 'Japanese', 'target', 'n', '???', '???', 'co:i', None), (70, 'Japanese_MiiPro', 'u255', None, 'Japanese_MiiPro', 'Japanese', 'target', 'dakara', '???', '???', 'conj', None), (71, 'Japanese_MiiPro', 'u255', None, 'Japanese_MiiPro', 'Japanese', 'target', 'ano', '???', '???', 'adn:deic:dem', None), (72, 'Japanese_MiiPro', 'u255', None, 'Japanese_MiiPro', 'Japanese', 'target', 'reji', '???', '???', 'n', None), (73, 'Japanese_MiiPro', 'u255', None, 'Japanese_MiiPro', 'Japanese', 'target', 'wa', '???', '???', 'ptl:top', None), (74, 'Japanese_MiiPro', 'u255', None, 'Japanese_MiiPro', 'Japanese', 'target', 'atchi', '???', '???', 'n:deic:dem', None), (75, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', 'aq', '???', '???', 'co:i', None), (76, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', 'shooboosha', '???', '???', 'n', None), (77, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', 'mot', '???', '???', 'v:c', None), (78, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'CONN', 'CVB', 'sfx', None), (79, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', 'ku', '???', '???', 'v:ir:sub', None), (80, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'CONN', 'CVB', 'sfx', None), (81, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', 'i', '???', '???', 'v:v:sub', None), (82, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'NEG', 'NEG', 'sfx', None), (83, 'Japanese_MiiPro', 'u287', None, 'Japanese_MiiPro', 'Japanese', 'target', '???', 'PRES', 'PRS', 'sfx', None)]")
        
        session.close()
    
    
    def test_speakers(self):
        """
        Test if all speakers for JapaneseMiiPro test file are loaded
        """
        session = make_session('Japanese_MiiPro')
        self.assertEqual(session.query(db.Speaker).count(), 2)
        
        s_jap_mii = select([db.Speaker])
        result_jap_mii = session.execute(s_jap_mii)
        self.assertEqual(str(result_jap_mii.fetchall()), "[(1, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'ALS', 'Asatokun', 'P3Y0M1D', '3;0.1', 1096, 'male', 'Male', 'Target_Child', 'Target_Child', 'Target_Child', 'jpn', None), (2, 'Japanese_MiiPro', 'Japanese_MiiPro', 'Japanese', 'MOT', None, None, None, None, 'female', 'Female', 'Mother', 'Mother', 'Adult', 'jpn', None)]")
        
        session.close()
        
        
    def test_uniquespeakers(self):
        """
        Test if all unique speakers for JapaneseMiiPro test file are loaded
        """
        session = make_session('Japanese_MiiPro')
        self.assertEqual(session.query(db.Uniquespeakers).count(),2)
        
        s_jap_mii = select([db.Uniquespeakers])
        result_jap_mii = session.execute(s_jap_mii)
        self.assertEqual(str(result_cree.fetchall()), "[(1, 'ALS', 'Asatokun', None, 'Male', 'Japanese_MiiPro'), (2, 'MOT', None, None, 'Female', 'Japanese_MiiPro')]")
        
        session.close()
        
    
class XMLTestJapaneseMiyata(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = connect('Japanese_Miyata')
        cls.configs = ['Japanese_Miyata.ini']
        load_database(cls.configs, engine)
    

    def test_sessions(self):
        """
        Test if sessions for JapaneseMiyata test file are loaded
        """
        session = make_session('Japanese_Miyata')
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(XMLTestJapaneseMiyata.configs))
        
        s = select([db.Session])
        result = session.execute(s)
        self.assertEqual(str(result.fetchall()), "[(1, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', '1989-03-06', 'Japanese_Miyata', 'Miyata-Aki', None)]")
        session.close()
        
        
    def test_utterances(self):
        """
        Test if all utterances for JapaneseMiyata test files are loaded
        """
        session = make_session('Japanese_Miyata')
        self.assertEqual(session.query(db.Utterance).count(), 13)
        
        s_jap_miy = select([db.Utterance])
        result_jap_miy = session.execute(s_jap_miy)
        self.assertEqual(str(result_jap_miy.fetchall()), "[(1, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1085', 'TMO', None, 'zoosan Taishookun', 'zoosan Taishookun', None, 'default', '1473.443', '1475.254', '1473.443', '1475.254', 'zoosan Taishookun', None, None, None, None, None), (2, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1086', 'TMO', None, 'kiiro mo atta', 'kiiro mo atta', None, 'default', '1505.729', '1506.740', '1505.729', '1506.740', 'kiiro mo atta', None, None, None, None, None), (3, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1088', 'TMO', None, 'nai', 'nai', None, 'default', None, None, None, None, 'nai', None, None, None, 'has put cookie into lego door , F has taken it away', None), (4, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1089', 'TMO', None, 'oi', 'oi', None, 'default', None, None, None, None, 'oi', None, None, None, 'R stands up suddenly; to kitchen', None), (5, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1090', 'TMO', None, 'mugicha', 'mugicha', None, 'default', None, None, None, None, 'mugicha', None, None, None, None, None), (6, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1091', 'TMO', None, 'nonjattara ato choodai', 'nonjattara ato choodai', None, 'exclamation', None, None, None, None, 'nonjattara ato choodai', None, None, None, None, None), (7, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1093', 'TMO', None, 'kore wa dohifuni hairu no', 'kore wa dohifuni hairu no', None, 'question', None, None, None, None, 'kore wa dohifuni hairu no', None, None, None, None, None), (8, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1087', 'TMO', None, 'njanja', 'njanja', None, 'default', None, None, None, None, 'njanja', None, None, None, 'pulls hand away , goes away', None), (9, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1092', 'TMO', None, 'bakkai bakkai bakkai', 'bakkai bakkai bakkai', None, 'default', '241.143', '244.266', '241.143', '244.266', 'bakkai bakkai bakkai', None, None, None, None, None), (10, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u1094', 'TMO', None, 'bakku bakku', 'bakku bakku', None, 'default', None, None, None, None, 'bakku bakku', None, None, None, None, None), (11, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u63', 'AMO', None, '??? sagasoo ka kok kara', '??? sagasoo ka kok kara', None, 'question', None, None, None, None, '??? sagasoo ka kok kara', None, None, None, 'AMO takes PhonoCards', None), (12, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u230', 'CHI', None, 'Suuzesan no ʃan mitai', 'Suuzesan no ʃan mitai', None, 'default', None, None, None, None, 'Suuzesan no ʃan mitai', None, None, None, 'meaning bicycle trousers clip', None), (13, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'u313', 'CHI', None, 'naʃinai tsuiteru no', 'naʃinai tsuiteru no', None, 'default', None, None, None, None, 'naʃinai tsuiteru no', None, None, None, None, None)]")
        
        session.close()
        
        
    def test_words(self):
        """
        Test if all words for JapaneseMiyata test file are loaded
        """
        session = make_session('Japanese_Miyata')
        self.assertEqual(session.query(db.Word).count(), 39)
        
        s_jap_miy = select([db.Word])
        result_jap_miy = session.execute(s_jap_miy)
        self.assertEqual(str(result_jap_miy.fetchall()), "[(1, 'Japanese_Miyata', 'u1085', 'Japanese_Miyata', 'Japanese', 'zoosan', 'zoosan', 'zoosan', None), (2, 'Japanese_Miyata', 'u1085', 'Japanese_Miyata', 'Japanese', 'Taishookun', 'Taishookun', 'Taishookun', None), (3, 'Japanese_Miyata', 'u1086', 'Japanese_Miyata', 'Japanese', 'kiiro', 'kiiro', 'kiiro', None), (4, 'Japanese_Miyata', 'u1086', 'Japanese_Miyata', 'Japanese', 'mo', 'mo', 'mo', None), (5, 'Japanese_Miyata', 'u1086', 'Japanese_Miyata', 'Japanese', 'atta', 'atta', 'atta', None), (6, 'Japanese_Miyata', 'u1088', 'Japanese_Miyata', 'Japanese', 'nai', 'nai', 'nai', None), (7, 'Japanese_Miyata', 'u1089', 'Japanese_Miyata', 'Japanese', 'oi', 'oi', 'oi', None), (8, 'Japanese_Miyata', 'u1090', 'Japanese_Miyata', 'Japanese', 'mugicha', 'mugicha', 'mugicha', None), (9, 'Japanese_Miyata', 'u1091', 'Japanese_Miyata', 'Japanese', 'nonjattara', 'nonjattara', 'nonjattara', None), (10, 'Japanese_Miyata', 'u1091', 'Japanese_Miyata', 'Japanese', 'ato', 'ato', 'ato', None), (11, 'Japanese_Miyata', 'u1091', 'Japanese_Miyata', 'Japanese', 'choodai', 'choodai', 'choodai', None), (12, 'Japanese_Miyata', 'u1093', 'Japanese_Miyata', 'Japanese', 'kore', 'kore', 'kore', None), (13, 'Japanese_Miyata', 'u1093', 'Japanese_Miyata', 'Japanese', 'wa', 'wa', 'wa', None), (14, 'Japanese_Miyata', 'u1093', 'Japanese_Miyata', 'Japanese', 'dohifuni', 'dohifuni', 'dooiu', None), (15, 'Japanese_Miyata', 'u1093', 'Japanese_Miyata', 'Japanese', None, None, 'fuu', 'See warning in Utterance table at: Japanese_Miyata, u1093 '), (16, 'Japanese_Miyata', 'u1093', 'Japanese_Miyata', 'Japanese', None, None, 'ni', 'See warning in Utterance table at: Japanese_Miyata, u1093 '), (17, 'Japanese_Miyata', 'u1093', 'Japanese_Miyata', 'Japanese', 'hairu', 'hairu', 'hairu', None), (18, 'Japanese_Miyata', 'u1093', 'Japanese_Miyata', 'Japanese', 'no', 'no', 'no', None), (19, 'Japanese_Miyata', 'u1087', 'Japanese_Miyata', 'Japanese', 'njanja', 'njanja', 'nainai', None), (20, 'Japanese_Miyata', 'u1092', 'Japanese_Miyata', 'Japanese', 'bakkai', 'bakkai', 'bakkari', None), (21, 'Japanese_Miyata', 'u1092', 'Japanese_Miyata', 'Japanese', 'bakkai', 'bakkai', 'bakkari', None), (22, 'Japanese_Miyata', 'u1092', 'Japanese_Miyata', 'Japanese', 'bakkai', 'bakkai', 'bakkari', None), (23, 'Japanese_Miyata', 'u1094', 'Japanese_Miyata', 'Japanese', 'bakku', 'bakku', 'bakku', None), (24, 'Japanese_Miyata', 'u1094', 'Japanese_Miyata', 'Japanese', 'bakku', 'bakku', 'bakku', None), (25, 'Japanese_Miyata', 'u63', 'Japanese_Miyata', 'Japanese', '???', '???', '???', 'not glossed'), (26, 'Japanese_Miyata', 'u63', 'Japanese_Miyata', 'Japanese', 'sagasoo', 'sagasoo', 'sagasoo', None), (27, 'Japanese_Miyata', 'u63', 'Japanese_Miyata', 'Japanese', 'ka', 'ka', 'ka', None), (28, 'Japanese_Miyata', 'u63', 'Japanese_Miyata', 'Japanese', 'kok', 'kok', 'koko', None), (29, 'Japanese_Miyata', 'u63', 'Japanese_Miyata', 'Japanese', 'kara', 'kara', 'kara', None), (30, 'Japanese_Miyata', 'u63', 'Japanese_Miyata', 'Japanese', None, None, None, 'See warning in Utterance table at: Japanese_Miyata, u63 '), (31, 'Japanese_Miyata', 'u230', 'Japanese_Miyata', 'Japanese', 'Suuzesan', 'Suuzesan', 'Suuzesan', None), (32, 'Japanese_Miyata', 'u230', 'Japanese_Miyata', 'Japanese', 'no', 'no', 'no', None), (33, 'Japanese_Miyata', 'u230', 'Japanese_Miyata', 'Japanese', 'ʃan', 'ʃan', '???', 'not glossed; not glossed'), (34, 'Japanese_Miyata', 'u230', 'Japanese_Miyata', 'Japanese', 'mitai', 'mitai', 'mitai', None), (35, 'Japanese_Miyata', 'u230', 'Japanese_Miyata', 'Japanese', None, None, None, 'See warning in Utterance table at: Japanese_Miyata, u230 '), (36, 'Japanese_Miyata', 'u313', 'Japanese_Miyata', 'Japanese', 'naʃinai', 'naʃinai', '???', 'not glossed; transcription insecure; not glossed'), (37, 'Japanese_Miyata', 'u313', 'Japanese_Miyata', 'Japanese', 'tsuiteru', 'tsuiteru', 'tsuiteru', None), (38, 'Japanese_Miyata', 'u313', 'Japanese_Miyata', 'Japanese', 'no', 'no', 'no', None), (39, 'Japanese_Miyata', 'u313', 'Japanese_Miyata', 'Japanese', None, None, None, 'See warning in Utterance table at: Japanese_Miyata, u313 ')]")
        
        session.close()
        
        
    def test_morphemes(self):
        """
        Test if all morphemes for JapaneseMiyata test file are loaded
        """
        session = make_session('Japanese_Miyata')
        self.assertEqual(session.query(db.Morpheme).count(), 44)
        
        s_jap_miy = select([db.Morpheme])
        result_jap_miy = session.execute(s_jap_miy)
        self.assertEqual(str(result_jap_miy.fetchall()), "[(1, 'Japanese_Miyata', 'u1085', None, 'Japanese_Miyata', 'Japanese', 'target', 'zoo', 'elephant', 'elephant', 'n', None), (2, 'Japanese_Miyata', 'u1085', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'san', 'san', 'sfx', None), (3, 'Japanese_Miyata', 'u1085', None, 'Japanese_Miyata', 'Japanese', 'target', 'Taishoo', 'Taishoo', 'Taishoo', 'n.prop', None), (4, 'Japanese_Miyata', 'u1085', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'kun', 'kun', 'sfx', None), (5, 'Japanese_Miyata', 'u1086', None, 'Japanese_Miyata', 'Japanese', 'target', 'ki=iro', 'yellow_color', 'yellow_color', 'n', None), (6, 'Japanese_Miyata', 'u1086', None, 'Japanese_Miyata', 'Japanese', 'target', 'mo', 'too', 'too', 'ptl.foc', None), (7, 'Japanese_Miyata', 'u1086', None, 'Japanese_Miyata', 'Japanese', 'target', 'ar', 'be', 'be', 'v.ir', None), (8, 'Japanese_Miyata', 'u1086', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'PAST', 'PST', 'sfx', None), (9, 'Japanese_Miyata', 'u1088', None, 'Japanese_Miyata', 'Japanese', 'target', 'ar', 'be.NEG', 'be.NEG', 'v.ir', None), (10, 'Japanese_Miyata', 'u1088', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'PRES', 'PRS', 'sfx', None), (11, 'Japanese_Miyata', 'u1089', None, 'Japanese_Miyata', 'Japanese', 'target', 'oi', 'hey', 'hey', 'co.i', None), (12, 'Japanese_Miyata', 'u1090', None, 'Japanese_Miyata', 'Japanese', 'target', 'mugi=cha', 'barley_tea', 'barley_tea', 'n', None), (13, 'Japanese_Miyata', 'u1091', None, 'Japanese_Miyata', 'Japanese', 'target', 'nom', 'drink', 'drink', 'v.c', None), (14, 'Japanese_Miyata', 'u1091', None, 'Japanese_Miyata', 'Japanese', 'target', 'tara', 'COMPL', 'CHANGE', 'sfx', None), (15, 'Japanese_Miyata', 'u1091', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'COND', 'COND', 'sfx', None), (16, 'Japanese_Miyata', 'u1091', None, 'Japanese_Miyata', 'Japanese', 'target', 'ato', 'after', 'after', 'n', None), (17, 'Japanese_Miyata', 'u1091', None, 'Japanese_Miyata', 'Japanese', 'target', 'choodai', 'give_me.IMP', 'give_me.IMP', 'v.ir', None), (18, 'Japanese_Miyata', 'u1093', None, 'Japanese_Miyata', 'Japanese', 'target', 'kore', 'this', 'this', 'n.deic.dem', None), (19, 'Japanese_Miyata', 'u1093', None, 'Japanese_Miyata', 'Japanese', 'target', 'wa', 'TOP', 'TOP', 'ptl.top', None), (20, 'Japanese_Miyata', 'u1093', None, 'Japanese_Miyata', 'Japanese', 'target', 'dooiu', 'what_kind', 'what_kind', 'adn.deic.wh', None), (21, 'Japanese_Miyata', 'u1093', None, 'Japanese_Miyata', 'Japanese', 'target', 'fuu', 'manner', 'manner', 'n.fml', None), (22, 'Japanese_Miyata', 'u1093', None, 'Japanese_Miyata', 'Japanese', 'target', 'ni', 'be.ADV', 'be.ADV', 'v.cop', None), (23, 'Japanese_Miyata', 'u1093', None, 'Japanese_Miyata', 'Japanese', 'target', 'hair', 'enter', 'enter', 'v.c', None), (24, 'Japanese_Miyata', 'u1093', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'PRES', 'PRS', 'sfx', None), (25, 'Japanese_Miyata', 'u1093', None, 'Japanese_Miyata', 'Japanese', 'target', 'no', 'FINA', 'PRAG', 'ptl.fina', None), (26, 'Japanese_Miyata', 'u1087', None, 'Japanese_Miyata', 'Japanese', 'target', 'nainai', 'allgone', 'allgone', 'n.vn.mot', None), (27, 'Japanese_Miyata', 'u1092', None, 'Japanese_Miyata', 'Japanese', 'target', 'bakari', 'almost', 'almost', 'ptl.foc', None), (28, 'Japanese_Miyata', 'u1092', None, 'Japanese_Miyata', 'Japanese', 'target', 'bakari', 'almost', 'almost', 'ptl.foc', None), (29, 'Japanese_Miyata', 'u1092', None, 'Japanese_Miyata', 'Japanese', 'target', 'bakari', 'almost', 'almost', 'ptl.foc', None), (30, 'Japanese_Miyata', 'u1094', None, 'Japanese_Miyata', 'Japanese', 'target', 'bakku', 'back', 'back', 'n.vn', None), (31, 'Japanese_Miyata', 'u1094', None, 'Japanese_Miyata', 'Japanese', 'target', 'bakku', 'back', 'back', 'n.vn', None), (32, 'Japanese_Miyata', 'u63', None, 'Japanese_Miyata', 'Japanese', 'target', 'sagas', 'search', 'search', 'v.c', None), (33, 'Japanese_Miyata', 'u63', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'HORT', 'HORT', 'sfx', None), (34, 'Japanese_Miyata', 'u63', None, 'Japanese_Miyata', 'Japanese', 'target', 'ka', 'Q', 'Q', 'ptl.fina', None), (35, 'Japanese_Miyata', 'u63', None, 'Japanese_Miyata', 'Japanese', 'target', 'koko', 'here', 'here', 'n.deic.dem', None), (36, 'Japanese_Miyata', 'u63', None, 'Japanese_Miyata', 'Japanese', 'target', 'kara', 'from', 'from', 'ptl.post', None), (37, 'Japanese_Miyata', 'u230', None, 'Japanese_Miyata', 'Japanese', 'target', 'Suuze', 'Suse', 'Suse', 'n.prop', None), (38, 'Japanese_Miyata', 'u230', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'san', 'san', 'sfx', None), (39, 'Japanese_Miyata', 'u230', None, 'Japanese_Miyata', 'Japanese', 'target', 'no', 'GEN', 'GEN', 'ptl.attr', None), (40, 'Japanese_Miyata', 'u230', None, 'Japanese_Miyata', 'Japanese', 'target', 'mitai', 'looks_like', 'looks_like', 'smod', None), (41, 'Japanese_Miyata', 'u313', None, 'Japanese_Miyata', 'Japanese', 'target', 'tsuk', 'attach', 'attach', 'v.c', None), (42, 'Japanese_Miyata', 'u313', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'ASP', 'IPFV', 'sfx', None), (43, 'Japanese_Miyata', 'u313', None, 'Japanese_Miyata', 'Japanese', 'target', '???', 'PRES', 'PRS', 'sfx', None), (44, 'Japanese_Miyata', 'u313', None, 'Japanese_Miyata', 'Japanese', 'target', 'no', 'FINA', 'PRAG', 'ptl.fina', None)]")
        
        session.close()
    
    def test_speakers(self):
        """
        Test if all speakers for JapaneseMiyata test file are loaded
        """
        session = make_session('Japanese_Miyata')
        self.assertEqual(session.query(db.Speaker).count(), 2)
        s_jap_miy = select([db.Speaker])
        result_jap_miy = session.execute(s_jap_miy)
        
        self.assertEqual(str(result_jap_miy.fetchall()), "[(1, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'CHI', 'Akifumi', 'P1Y5M7D', '1;5.7', 522, None, 'Unspecified', 'Target_Child', 'Target_Child', 'Target_Child', 'jpn', None), (2, 'Japanese_Miyata', 'Japanese_Miyata', 'Japanese', 'AMO', 'Okaasan', None, None, None, None, 'Unspecified', 'Mother', 'Mother', 'Adult', 'jpn', None)]")
        
        session.close()
        
    def test_uniquespeakers(self):
        """
        Test if all unique speakers for JapaneseMiyata test file are loaded
        """
        session = make_session('Japanese_Miyata')
        self.assertEqual(session.query(db.Uniquespeakers).count(), 2)
        
        s_jap_miy = select([db.Uniquespeakers])
        result_jap_miy = session.execute(s_jap_miy)
        self.assertEqual(str(result_jap_miy.fetchall()), "[(1, 'CHI', 'Akifumi', None, 'Unspecified', 'Japanese_Miyata'), (2, 'AMO', 'Okaasan', None, 'Unspecified', 'Japanese_Miyata')]")
        
        session.close()
        
    
class XMLTestSesotho(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = connect('Sesotho')
        cls.configs = ['Sesotho.ini']
        load_database(cls.configs, engine)
    

    def test_sessions(self):
        """
        Test if sessions for Sesotho test file are loaded
        """
        session = make_session('Sesotho')
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(XMLTestSesotho.configs))
        
        s = select([db.Session])
        result = session.execute(s)
        self.assertEqual(str(result.fetchall()), "[(1, 'Sesotho', 'Sesotho', 'Sesotho', '1984-01-01', 'Sesotho', 'Sesotho', 'audio')]")
        session.close()
        
        
    def test_utterances(self):
        """
        Test if all utterances for Sesotho test file are loaded
        """
        session = make_session('Sesotho')
        self.assertEqual(session.query(db.Utterance).count(), 11)
        
        s_seso = select([db.Utterance])
        result_seso = session.execute(s_seso)
        self.assertEqual(str(result_seso.fetchall()), "[(1, 'Sesotho', 'Sesotho', 'Sesotho', 'u381', 'HLE', None, 'ke Tsebo o ntsa nkotla', 'ke Tsebo o ntsa nkotla', 'It is Tsebo who is still me hitting', 'default', '1878.400', '1884.843', '1878.400', '1884.843', 'ke Tsebo o ntsa nkotla', None, None, None, None, 'broken alignment full_word : glosses_target'), (2, 'Sesotho', 'Sesotho', 'Sesotho', 'u382', 'MAR', None, 'mohlankwane makhweshepe a teng ka lebekereng', 'mohlankwane makhweshepe a teng ka lebekereng', 'That day the rough peach was in the cup ?', 'default', '2919.123', '2930.498', '2919.123', '2930.498', 'mohlankwane makhweshepe a teng ka lebekereng', None, None, None, 'Restored gls.', 'broken alignment full_word : glosses_target'), (3, 'Sesotho', 'Sesotho', 'Sesotho', 'u383', 'HLE', None, 'ke Tsebo o ntsa nkotla', 'ke Tsebo o ntsa nkotla', 'It is Tsebo who is still me hitting', 'default', '1878.400', '1884.843', '1878.400', '1884.843', 'ke Tsebo o ntsa nkotla', None, None, None, None, 'broken alignment full_word : glosses_target'), (4, 'Sesotho', 'Sesotho', 'Sesotho', 'u384', 'MAR', None, 'ho bua teng ha o tsebe o tseba ho bina', 'ho bua teng ha o tsebe o tseba ho bina', \"To talk you don't know you know how to sing\", 'default', None, None, None, None, 'ho bua teng ha o tsebe o tseba ho bina', None, None, None, 'Restored cod.', 'broken alignment full_word : glosses_target'), (5, 'Sesotho', 'Sesotho', 'Sesotho', 'u385', 'CHI', None, 'bo butle Lineo ke qhetsole', 'bo butle Lineo ke qhetsole', 'Wait Lineo so I can break', 'default', '239.645', '241.835', '239.645', '241.835', 'bo butle Lineo ke qhetsole', None, None, None, None, 'broken alignment full_word : glosses_target'), (6, 'Sesotho', 'Sesotho', 'Sesotho', 'u386', 'NEU', None, 'ke tla kuka wane wa nkhono', 'ke tla kuka wane wa nkhono', 'I will take that one for grandmother', 'default', '1800.848', '1803.446', '1800.848', '1803.446', 'ke tla kuka wane wa nkhono', None, None, None, None, 'broken alignment full_word : glosses_target'), (7, 'Sesotho', 'Sesotho', 'Sesotho', 'u387', 'CHI', None, 'jwale ha re sa bue tjee', 'jwale ha re sa bue tjee', 'Now we do not talk like this', 'default', '1641.281', '1644.161', '1641.281', '1644.161', 'jwale ha re sa bue tjee', None, None, None, None, 'broken alignment full_word : glosses_target'), (8, 'Sesotho', 'Sesotho', 'Sesotho', 'u388', 'CHI', None, 'ebile etabwile a e nkileng', 'ebile etabwile a e nkileng', 'It is even torn the one he has taken', 'default', None, None, None, None, 'ebile etabwile a e nkileng', None, None, None, None, 'broken alignment full_word : glosses_target'), (9, 'Sesotho', 'Sesotho', 'Sesotho', 'u390', 'NTS', None, 'molakaladi ha o mongata lekgale', 'molakaladi ha o mongata lekgale', 'Molakaladi is so much', 'default', None, None, None, None, 'molakaladi ha o mongata lekgale', None, None, None, None, None), (10, 'Sesotho', 'Sesotho', 'Sesotho', 'u389', 'CHI', None, 'le na ta iyetsa tsikitsiki', 'le na ta iyetsa tsikitsiki', 'And me I will tickle you tsiki tsiki', 'default', '2849.169', '2853.369', '2849.169', '2853.369', 'le na ta iyetsa tsikitsiki', None, None, None, None, None), (11, 'Sesotho', 'Sesotho', 'Sesotho', 'u41', 'TLN', None, 'mme Mach ??? okae', 'mme Mach ??? okae', 'Where is mother Machaka?', 'question', '360.400', '367.551', '360.400', '367.551', 'mme Mach ??? okae', None, None, None, None, None)]")
        
        session.close()
        
        
        
    def test_words(self):
        """
        Test if all words for Sesotho test file are loaded
        """
        session = make_session('Sesotho')
        self.assertEqual(session.query(db.Word).count(), 64)
        
        s_seso = select([db.Word])
        result_seso = session.execute(s_seso)
        self.assertEqual(str(result_seso.fetchall()), "[(1, 'Sesotho', 'u381', 'Sesotho', 'Sesotho', 'ke', 'ke', 'ke', None), (2, 'Sesotho', 'u381', 'Sesotho', 'Sesotho', 'Tsebo', 'Tsebo', 'Tsebo', None), (3, 'Sesotho', 'u381', 'Sesotho', 'Sesotho', 'o', 'o', 'o', None), (4, 'Sesotho', 'u381', 'Sesotho', 'Sesotho', 'ntsa', 'ntsa', 'ntsa', None), (5, 'Sesotho', 'u381', 'Sesotho', 'Sesotho', 'nkotla', 'nkotla', 'nkotla', None), (6, 'Sesotho', 'u382', 'Sesotho', 'Sesotho', 'mohlankwane', 'mohlankwane', 'mohlankwane', None), (7, 'Sesotho', 'u382', 'Sesotho', 'Sesotho', 'makhweshepe', 'makhweshepe', 'makhweshepe', None), (8, 'Sesotho', 'u382', 'Sesotho', 'Sesotho', 'a', 'a', 'a', None), (9, 'Sesotho', 'u382', 'Sesotho', 'Sesotho', 'teng', 'teng', 'teng', None), (10, 'Sesotho', 'u382', 'Sesotho', 'Sesotho', 'ka', 'ka', 'ka', None), (11, 'Sesotho', 'u382', 'Sesotho', 'Sesotho', 'lebekereng', 'lebekereng', 'lebekereng', None), (12, 'Sesotho', 'u382', 'Sesotho', 'Sesotho', None, None, None, 'See warning in Utterance table at: Sesotho, u382 '), (13, 'Sesotho', 'u382', 'Sesotho', 'Sesotho', None, None, None, 'See warning in Utterance table at: Sesotho, u382 '), (14, 'Sesotho', 'u383', 'Sesotho', 'Sesotho', 'ke', 'ke', 'ke', None), (15, 'Sesotho', 'u383', 'Sesotho', 'Sesotho', 'Tsebo', 'Tsebo', 'Tsebo', None), (16, 'Sesotho', 'u383', 'Sesotho', 'Sesotho', 'o', 'o', 'o', None), (17, 'Sesotho', 'u383', 'Sesotho', 'Sesotho', 'ntsa', 'ntsa', 'ntsa', None), (18, 'Sesotho', 'u383', 'Sesotho', 'Sesotho', 'nkotla', 'nkotla', 'nkotla', None), (19, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'ho', 'ho', 'ho', None), (20, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'bua', 'bua', 'bua', None), (21, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'teng', 'teng', 'teng', None), (22, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'ha', 'ha', 'ha', None), (23, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'o', 'o', 'o', None), (24, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'tsebe', 'tsebe', 'tsebe', None), (25, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'o', 'o', 'o', None), (26, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'tseba', 'tseba', 'tseba', None), (27, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'ho', 'ho', 'ho', None), (28, 'Sesotho', 'u384', 'Sesotho', 'Sesotho', 'bina', 'bina', 'bina', None), (29, 'Sesotho', 'u385', 'Sesotho', 'Sesotho', 'bo', 'bo', 'bo', None), (30, 'Sesotho', 'u385', 'Sesotho', 'Sesotho', 'butle', 'butle', 'butle', None), (31, 'Sesotho', 'u385', 'Sesotho', 'Sesotho', 'Lineo', 'Lineo', 'Lineo', None), (32, 'Sesotho', 'u385', 'Sesotho', 'Sesotho', 'ke', 'ke', 'ke', None), (33, 'Sesotho', 'u385', 'Sesotho', 'Sesotho', 'qhetsole', 'qhetsole', 'qhetsole', None), (34, 'Sesotho', 'u386', 'Sesotho', 'Sesotho', 'ke', 'ke', 'ke', None), (35, 'Sesotho', 'u386', 'Sesotho', 'Sesotho', 'tla', 'tla', 'tla', None), (36, 'Sesotho', 'u386', 'Sesotho', 'Sesotho', 'kuka', 'kuka', 'kuka', None), (37, 'Sesotho', 'u386', 'Sesotho', 'Sesotho', 'wane', 'wane', 'wane', None), (38, 'Sesotho', 'u386', 'Sesotho', 'Sesotho', 'wa', 'wa', 'wa', None), (39, 'Sesotho', 'u386', 'Sesotho', 'Sesotho', 'nkhono', 'nkhono', 'nkhono', None), (40, 'Sesotho', 'u387', 'Sesotho', 'Sesotho', 'jwale', 'jwale', 'jwale', None), (41, 'Sesotho', 'u387', 'Sesotho', 'Sesotho', 'ha', 'ha', 'ha', None), (42, 'Sesotho', 'u387', 'Sesotho', 'Sesotho', 're', 're', 're', None), (43, 'Sesotho', 'u387', 'Sesotho', 'Sesotho', 'sa', 'sa', 'sa', None), (44, 'Sesotho', 'u387', 'Sesotho', 'Sesotho', 'bue', 'bue', 'bue', None), (45, 'Sesotho', 'u387', 'Sesotho', 'Sesotho', 'tjee', 'tjee', 'tjee', None), (46, 'Sesotho', 'u388', 'Sesotho', 'Sesotho', 'ebile', 'ebile', 'ebile', None), (47, 'Sesotho', 'u388', 'Sesotho', 'Sesotho', 'etabwile', 'etabwile', 'etabwile', None), (48, 'Sesotho', 'u388', 'Sesotho', 'Sesotho', 'a', 'a', 'a', None), (49, 'Sesotho', 'u388', 'Sesotho', 'Sesotho', 'e', 'e', 'e', None), (50, 'Sesotho', 'u388', 'Sesotho', 'Sesotho', 'nkileng', 'nkileng', 'nkileng', None), (51, 'Sesotho', 'u390', 'Sesotho', 'Sesotho', 'molakaladi', 'molakaladi', 'molakaladi', None), (52, 'Sesotho', 'u390', 'Sesotho', 'Sesotho', 'ha', 'ha', 'ha', None), (53, 'Sesotho', 'u390', 'Sesotho', 'Sesotho', 'o', 'o', 'o', None), (54, 'Sesotho', 'u390', 'Sesotho', 'Sesotho', 'mongata', 'mongata', 'mongata', None), (55, 'Sesotho', 'u390', 'Sesotho', 'Sesotho', 'lekgale', 'lekgale', 'lekgale', None), (56, 'Sesotho', 'u389', 'Sesotho', 'Sesotho', 'le', 'le', 'le', None), (57, 'Sesotho', 'u389', 'Sesotho', 'Sesotho', 'na', 'na', 'na', None), (58, 'Sesotho', 'u389', 'Sesotho', 'Sesotho', 'ta', 'ta', 'ita', None), (59, 'Sesotho', 'u389', 'Sesotho', 'Sesotho', 'iyetsa', 'iyetsa', 'iyetsa', None), (60, 'Sesotho', 'u389', 'Sesotho', 'Sesotho', 'tsikitsiki', 'tsikitsiki', 'tsikitsiki', None), (61, 'Sesotho', 'u41', 'Sesotho', 'Sesotho', 'mme', 'mme', 'mme', None), (62, 'Sesotho', 'u41', 'Sesotho', 'Sesotho', 'Mach', 'Mach', 'Mach', None), (63, 'Sesotho', 'u41', 'Sesotho', 'Sesotho', '???', '???', '???', None), (64, 'Sesotho', 'u41', 'Sesotho', 'Sesotho', 'okae', 'okae', 'okae', None)]")
        
        session.close()
        
        
    def test_morphemes(self):
        """
        Test if all morphemes for Sesotho test file are loaded
        """
        session = make_session('Sesotho')
        self.assertEqual(session.query(db.Morpheme).count(), 98)
        
        s_seso = select([db.Morpheme])
        result_seso = session.execute(s_seso)
        self.assertEqual(str(result_seso.fetchall()), "[(1, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'ke', 'cp', 'COP', 'cop', None), (2, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'Tsebo', 'a_name', 'a_name', '???', None), (3, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'ya', 'sr1', 'I.S.REL', 'pfx', None), (4, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'ntse', 't^pp', 'PST.CONT', 'pfx', None), (5, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'ng', 'rl', 'REL.LOC', 'pfx', None), (6, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'a', 'sm1', 'I.S', 'pfx', None), (7, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'n', 'om1s', '1SG.OBJ', 'pfx', None), (8, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'kotl', 'beat', 'beat', 'v', None), (9, 'Sesotho', 'u381', None, 'Sesotho', 'Sesotho', 'target', 'a', 'm^pt', 'SBJV2', 'sfx', None), (10, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'mo', '3', '3', 'pfx', None), (11, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'hla', 'day(3,4)', 'day(3,4)', 'n', None), (12, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'wane', '3', '3', 'd', None), (13, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'oo', '3', '3', 'obr', None), (14, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'ma', '6', '6', 'pfx', None), (15, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'khweshepe', 'rough_one(5,6)', 'rough_one(5,6)', 'n', None), (16, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'a', 'sm6', 'VI.S', 'pfx', None), (17, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'le', 'cp', 'COP', 'pfx', None), (18, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'teng', 'loc', 'loc', 'loc', None), (19, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'ka', 'pr', 'PREP', 'pr', None), (20, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'le', '5', '5', 'pfx', None), (21, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'bekere', 'cup(5,6)', 'cup(5,6)', 'n', None), (22, 'Sesotho', 'u382', None, 'Sesotho', 'Sesotho', 'target', 'ng', 'lc', 'LOC', 'sfx', None), (23, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'ke', 'cp', 'COP', 'cop', None), (24, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'Tsebo', 'a_name', 'a_name', '???', None), (25, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'ya', 'sr1', 'I.S.REL', 'pfx', None), (26, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'ntse', 't^pp', 'PST.CONT', 'pfx', None), (27, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'ng', 'rl', 'REL.LOC', 'pfx', None), (28, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'a', 'sm1', 'I.S', 'pfx', None), (29, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'n', 'om1s', '1SG.OBJ', 'pfx', None), (30, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'kotl', 'beat', 'beat', 'v', None), (31, 'Sesotho', 'u383', None, 'Sesotho', 'Sesotho', 'target', 'a', 'm^pt', 'SBJV2', 'sfx', None), (32, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'ho', 'if', 'if', 'pfx', None), (33, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'bu', 's^speak', 's^speak', 'pfx', None), (34, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'a', 'm^pt', 'SBJV2', 'pfx', None), (35, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'teng', 'loc', 'loc', 'loc', None), (36, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'ha', 'ng', 'NEG', 'ng', None), (37, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'u', 'sm2s', '2SG.S', 'pfx', None), (38, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'tseb', 't^p_know', 't^p_know', 'v', None), (39, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'e', 'm^x', 'NEG', 'sfx', None), (40, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'u', 'sm2s', '2SG.S', 'pfx', None), (41, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'tseb', 't^p_know', 't^p_know', 'v', None), (42, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'a', 'm^in', 'm^in', 'sfx', None), (43, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'ho', 'if', 'if', 'pfx', None), (44, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'bin', 'sing', 'sing', 'v', None), (45, 'Sesotho', 'u384', None, 'Sesotho', 'Sesotho', 'target', 'a', 'm^pt', 'SBJV2', 'sfx', None), (46, 'Sesotho', 'u385', None, 'Sesotho', 'Sesotho', 'target', 'bo', 'ij', 'INTJ', 'ij', None), (47, 'Sesotho', 'u385', None, 'Sesotho', 'Sesotho', 'target', 'butle', 'ij', 'INTJ', 'ij', None), (48, 'Sesotho', 'u385', None, 'Sesotho', 'Sesotho', 'target', 'Lineo', 'a_name', 'a_name', '???', None), (49, 'Sesotho', 'u385', None, 'Sesotho', 'Sesotho', 'target', 'ke', 'sm1s', '1SG.S', 'pfx', None), (50, 'Sesotho', 'u385', None, 'Sesotho', 'Sesotho', 'target', 'qhetsol', 't^p_give_a_part_to', 't^p_give_a_part_to', 'v', None), (51, 'Sesotho', 'u385', None, 'Sesotho', 'Sesotho', 'target', 'e', 'm^s', 'SBJV', 'sfx', None), (52, 'Sesotho', 'u386', None, 'Sesotho', 'Sesotho', 'target', 'ke', 'sm1s', '1SG.S', 'pfx', None), (53, 'Sesotho', 'u386', None, 'Sesotho', 'Sesotho', 'target', 'tla', 't^f1', 'FUT1', 'pfx', None), (54, 'Sesotho', 'u386', None, 'Sesotho', 'Sesotho', 'target', 'nk', 'take', 'take', 'v', None), (55, 'Sesotho', 'u386', None, 'Sesotho', 'Sesotho', 'target', 'a', 'm^in', 'm^in', 'sfx', None), (56, 'Sesotho', 'u386', None, 'Sesotho', 'Sesotho', 'target', 'wane', '3', '3', 'd', None), (57, 'Sesotho', 'u386', None, 'Sesotho', 'Sesotho', 'target', 'wa', '3', '3', 'ps', None), (58, 'Sesotho', 'u386', None, 'Sesotho', 'Sesotho', 'target', 'nkhono', 'grandmother(1a,2a)', 'grandmother(1a,2a)', 'n', None), (59, 'Sesotho', 'u387', None, 'Sesotho', 'Sesotho', 'target', 'jwale', 'av', 'ADV', 'av', None), (60, 'Sesotho', 'u387', None, 'Sesotho', 'Sesotho', 'target', 'ha', 'ng', 'NEG', 'ng', None), (61, 'Sesotho', 'u387', None, 'Sesotho', 'Sesotho', 'target', 're', 'sm1p', '1PL.S', 'pfx', None), (62, 'Sesotho', 'u387', None, 'Sesotho', 'Sesotho', 'target', 'sa', 't^sa', 'PERS', 'pfx', None), (63, 'Sesotho', 'u387', None, 'Sesotho', 'Sesotho', 'target', 'bu', 'speak', 'speak', 'v', None), (64, 'Sesotho', 'u387', None, 'Sesotho', 'Sesotho', 'target', 'e', 'm^x', 'NEG', 'sfx', None), (65, 'Sesotho', 'u387', None, 'Sesotho', 'Sesotho', 'target', 'tjee', 'av', 'ADV', 'av', None), (66, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'ebile', 'cj', 'CONJ', 'cj', None), (67, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'e', 'sm9', 'IX.S', 'pfx', None), (68, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'taboh', 'tear/nt', 'tear.COS', 'v', None), (69, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'il', 't^pf', 'PRF', 'sfx', None), (70, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'e', 'm^in', 'm^in', 'sfx', None), (71, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'eo', '9', '9', 'or', None), (72, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'a', 'sm1', 'I.S', 'pfx', None), (73, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'e', 'om9', 'IX.OBJ', 'pfx', None), (74, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'nk', 'take', 'take', 'v', None), (75, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'il', 't^pf', 'PRF', 'sfx', None), (76, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'e', 'm^pt', 'SBJV2', 'sfx', None), (77, 'Sesotho', 'u388', None, 'Sesotho', 'Sesotho', 'target', 'ng', 'rl', 'REL.LOC', 'sfx', None), (78, 'Sesotho', 'u390', None, 'Sesotho', 'Sesotho', 'target', 'mo', '3', '3', 'pfx', None), (79, 'Sesotho', 'u390', None, 'Sesotho', 'Sesotho', 'target', 'lakaladi', 'edible_bulb(3,4)', 'edible_bulb(3,4)', 'n', None), (80, 'Sesotho', 'u390', None, 'Sesotho', 'Sesotho', 'target', 'ha', 'cd', 'cd', 'cd', None), (81, 'Sesotho', 'u390', None, 'Sesotho', 'Sesotho', 'target', 'o', 'sm3', 'III.S', 'afx.detached', None), (82, 'Sesotho', 'u390', None, 'Sesotho', 'Sesotho', 'target', 'mo', '3', '3', 'pfx', None), (83, 'Sesotho', 'u390', None, 'Sesotho', 'Sesotho', 'target', 'ngata', 'aj', 'aj', 'aj', None), (84, 'Sesotho', 'u390', None, 'Sesotho', 'Sesotho', 'target', 'lekhale', 'av', 'ADV', 'av', None), (85, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'le', 'cj', 'CONJ', 'cj', None), (86, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'nna', '1s', '1SG', 'pn', None), (87, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'ke', 'sm1s', '1SG.S', 'pfx', None), (88, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'tla', 't^f1', 'FUT1', 'pfx', None), (89, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'u', 'om2s', '2SG.OBJ', 'pfx', None), (90, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'ntsikiny', 'tickle', 'tickle', 'v', None), (91, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'ets', 'c', 'CAUS', 'sfx', None), (92, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'a', 'm^in', 'm^in', 'sfx', None), (93, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'tsiki', '???', '???', 'none', None), (94, 'Sesotho', 'u389', None, 'Sesotho', 'Sesotho', 'target', 'tsiki', '???', '???', 'none', None), (95, 'Sesotho', 'u41', None, 'Sesotho', 'Sesotho', 'target', 'mme', 'mother(1a,2a)', 'mother(1a,2a)', 'n', None), (96, 'Sesotho', 'u41', None, 'Sesotho', 'Sesotho', 'target', 'Machaka', 'a_name', 'a_name', '???', None), (97, 'Sesotho', 'u41', None, 'Sesotho', 'Sesotho', 'target', 'o', 'cp1', 'I.COP', 'cop', None), (98, 'Sesotho', 'u41', None, 'Sesotho', 'Sesotho', 'target', 'kae', 'wh', 'WH.Q', 'wh', None)]")
        
        session.close()
        
    
    def test_speakers(self):
        """
        Test if all speakers for Sesotho test file are loaded
        """
        session = make_session('Sesotho')
        self.assertEqual(session.query(db.Speaker).count(), 2)
        
        s_seso = select([db.Speaker])
        result_seso = session.execute(s_seso)
        self.assertEqual(str(result_seso.fetchall()), "[(1, 'Sesotho', 'Sesotho', 'Sesotho', 'NTS', 'Ntselleng', None, None, None, None, 'Unspecified', 'Playmate', 'Playmate', 'Child', 'sme', None), (2, 'Sesotho', 'Sesotho', 'Sesotho', 'RPL', 'Rapelang', None, None, None, None, 'Unspecified', 'Playmate', 'Playmate', 'Child', 'sme', None)]")
        
        session.close()
        
        
    def test_uniquespeakers(self):
        """
        Test if all unique speakers for Sesotho test file are loaded
        """
        session = make_session('Sesotho')
        self.assertEqual(session.query(db.Uniquespeakers).count(),2)
        
        s_seso = select([db.Uniquespeakers])
        result_seso = session.execute(s_seso)
        self.assertEqual(str(result_seso.fetchall()), "[(1, 'NTS', 'Ntselleng', None, 'Unspecified', 'Sesotho'), (2, 'RPL', 'Rapelang', None, 'Unspecified', 'Sesotho')]")
        
        session.close()
        
        
class XMLTestTurkish(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = connect('Turkish')
        cls.configs = ['Turkish.ini']
        load_database(cls.configs, engine)
    

    def test_sessions(self):
        """
        Test if sessions for Turkish test file are loaded
        """
        session = make_session('Turkish')
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(XMLTestTurkish.configs))
        
        s = select([db.Session])
        result = session.execute(s)
        self.assertEqual(str(result.fetchall()), "[(1, 'Turkish', 'Turkish_KULLD', 'Turkish', '2002-05-23', 'Turkish', 'Turkish_KULLD', 'video')]")
        
        session.close()
        
        
    def test_utterances(self):
        """
        Test if all utterances for Turkish test file are loaded
        """
        session = make_session('Turkish')
        self.assertEqual(session.query(db.Utterance).count(), 14)
        
        s_turk = select([db.Utterance])
        result_turk = session.execute(s_turk)
        self.assertEqual(str(result_turk.fetchall()), "[(1, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1925', 'MOT', None, 'otur bakalım', 'otur bakalım', None, 'default', None, None, None, None, 'otur bakalım', None, None, None, None, None), (2, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1929', 'MOT', None, 'bir tek bu var', 'bir tek bu var', None, 'default', None, None, None, None, 'bir tek bu var', None, None, None, None, None), (3, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1933', 'MOT', None, 'onu kaldırdı Necla', 'onu kaldırdı Necla', None, 'default', None, None, None, None, 'onu kaldırdı Necla', None, None, None, None, None), (4, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1934', 'MOT', None, 'Necla kaldırdı', 'Necla kaldırdı', None, 'default', None, None, None, None, 'Necla kaldırdı', None, None, None, None, None), (5, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1935', 'AUN', None, 'sen gel bana sen gel taytay gel', 'sen gel bana sen gel taytay gel', None, 'default', None, None, None, None, 'sen gel bana sen gel taytay gel', None, None, None, \"AUN holds CHI's hand. CHI is still holding pens. They are walking together to armchair.\", None), (6, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1926', 'CHI', None, 'bi tan dı', 'bi tan dı', None, 'default', '3745.000', None, '01:02:25', None, 'bi tan dı', None, None, None, None, None), (7, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1927', 'CHI', None, 'bi tan da', 'bi tan da', None, 'default', '3746.000', None, '01:02:26', None, 'bi tan da', None, None, None, None, None), (8, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1931', 'CHI', None, 'bi tan da', 'bi tan da', None, 'default', '3753.000', None, '01:02:33', None, 'bi tan da', None, None, None, None, None), (9, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1928', 'MOT', None, 'bi tane daha minder yok', 'bi tane daha minder yok', None, 'default', None, None, None, None, 'bi tane daha minder yok', None, None, None, None, None), (10, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1930', 'MOT', None, 'bi de çadırdakiler var', 'bi de çadırdakiler var', None, 'default', None, None, None, None, 'bi de çadırdakiler var', None, None, None, None, None), (11, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u1932', 'MOT', None, 'bi tane daha vardı ama yok', 'bi tane daha vardı ama yok', None, 'default', None, None, None, None, 'bi tane daha vardı ama yok', None, None, None, None, None), (12, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u296', 'AYL', None, 'anlaştık baya anlaştık baya', 'anlaştık baya anlaştık baya', None, 'default', None, None, None, None, 'anlaştık baya anlaştık baya', None, None, None, None, None), (13, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u603', 'MOT', None, 'lokma al alınca bağrıyoruz', 'lokma al alınca bağrıyoruz', None, 'default', None, None, None, None, 'lokma al alınca bağrıyoruz', None, None, None, None, None), (14, 'Turkish', 'Turkish_KULLD', 'Turkish', 'u119', 'AYL', None, 'zaten doğuş doğuş kilonun şeyi hiç bi_şeyle diğil', 'zaten doğuş doğuş kilonun şeyi hiç bi_şeyle diğil', None, 'default', None, None, None, None, 'zaten doğuş doğuş kilonun şeyi hiç bi_şeyle diğil', None, None, None, None, None)]")
        
        session.close()
        
        
        
    def test_words(self):
        """
        Test if all words for Turkish test file are loaded
        """
        session = make_session('Turkish')
        self.assertEqual(session.query(db.Word).count(), 59)
        
        s_turk = select([db.Word])
        result_turk = session.execute(s_turk)
        self.assertEqual(str(result_turk.fetchall()), "[(1, 'Turkish', 'u1925', 'Turkish_KULLD', 'Turkish', 'otur', 'otur', 'otur', None), (2, 'Turkish', 'u1925', 'Turkish_KULLD', 'Turkish', 'bakalım', 'bakalım', 'bakalım', None), (3, 'Turkish', 'u1929', 'Turkish_KULLD', 'Turkish', 'bir', 'bir', 'bir', None), (4, 'Turkish', 'u1929', 'Turkish_KULLD', 'Turkish', 'tek', 'tek', 'tek', None), (5, 'Turkish', 'u1929', 'Turkish_KULLD', 'Turkish', 'bu', 'bu', 'bu', None), (6, 'Turkish', 'u1929', 'Turkish_KULLD', 'Turkish', 'var', 'var', 'var', None), (7, 'Turkish', 'u1933', 'Turkish_KULLD', 'Turkish', 'onu', 'onu', 'onu', None), (8, 'Turkish', 'u1933', 'Turkish_KULLD', 'Turkish', 'kaldırdı', 'kaldırdı', 'kaldırdı', None), (9, 'Turkish', 'u1933', 'Turkish_KULLD', 'Turkish', 'Necla', 'Necla', 'Necla', None), (10, 'Turkish', 'u1934', 'Turkish_KULLD', 'Turkish', 'Necla', 'Necla', 'Necla', None), (11, 'Turkish', 'u1934', 'Turkish_KULLD', 'Turkish', 'kaldırdı', 'kaldırdı', 'kaldırdı', None), (12, 'Turkish', 'u1935', 'Turkish_KULLD', 'Turkish', 'sen', 'sen', 'sen', None), (13, 'Turkish', 'u1935', 'Turkish_KULLD', 'Turkish', 'gel', 'gel', 'gel', None), (14, 'Turkish', 'u1935', 'Turkish_KULLD', 'Turkish', 'bana', 'bana', 'bana', None), (15, 'Turkish', 'u1935', 'Turkish_KULLD', 'Turkish', 'sen', 'sen', 'sen', None), (16, 'Turkish', 'u1935', 'Turkish_KULLD', 'Turkish', 'gel', 'gel', 'gel', None), (17, 'Turkish', 'u1935', 'Turkish_KULLD', 'Turkish', 'taytay', 'taytay', 'taytay', 'not glossed'), (18, 'Turkish', 'u1935', 'Turkish_KULLD', 'Turkish', 'gel', 'gel', 'gel', None), (19, 'Turkish', 'u1926', 'Turkish_KULLD', 'Turkish', 'bi', 'bi', 'bir', None), (20, 'Turkish', 'u1926', 'Turkish_KULLD', 'Turkish', 'tan', 'tan', 'tane', None), (21, 'Turkish', 'u1926', 'Turkish_KULLD', 'Turkish', 'dı', 'dı', 'daha', None), (22, 'Turkish', 'u1927', 'Turkish_KULLD', 'Turkish', 'bi', 'bi', 'bir', None), (23, 'Turkish', 'u1927', 'Turkish_KULLD', 'Turkish', 'tan', 'tan', 'tane', None), (24, 'Turkish', 'u1927', 'Turkish_KULLD', 'Turkish', 'da', 'da', 'daha', None), (25, 'Turkish', 'u1931', 'Turkish_KULLD', 'Turkish', 'bi', 'bi', 'bir', None), (26, 'Turkish', 'u1931', 'Turkish_KULLD', 'Turkish', 'tan', 'tan', 'tane', None), (27, 'Turkish', 'u1931', 'Turkish_KULLD', 'Turkish', 'da', 'da', 'daha', None), (28, 'Turkish', 'u1928', 'Turkish_KULLD', 'Turkish', 'bi', 'bi', 'bir', None), (29, 'Turkish', 'u1928', 'Turkish_KULLD', 'Turkish', 'tane', 'tane', 'tane', None), (30, 'Turkish', 'u1928', 'Turkish_KULLD', 'Turkish', 'daha', 'daha', 'daha', None), (31, 'Turkish', 'u1928', 'Turkish_KULLD', 'Turkish', 'minder', 'minder', 'minder', None), (32, 'Turkish', 'u1928', 'Turkish_KULLD', 'Turkish', 'yok', 'yok', 'yok', None), (33, 'Turkish', 'u1930', 'Turkish_KULLD', 'Turkish', 'bi', 'bi', 'bir', None), (34, 'Turkish', 'u1930', 'Turkish_KULLD', 'Turkish', 'de', 'de', 'de', None), (35, 'Turkish', 'u1930', 'Turkish_KULLD', 'Turkish', 'çadırdakiler', 'çadırdakiler', 'çadırdakiler', None), (36, 'Turkish', 'u1930', 'Turkish_KULLD', 'Turkish', 'var', 'var', 'var', None), (37, 'Turkish', 'u1932', 'Turkish_KULLD', 'Turkish', 'bi', 'bi', 'bir', None), (38, 'Turkish', 'u1932', 'Turkish_KULLD', 'Turkish', 'tane', 'tane', 'tane', None), (39, 'Turkish', 'u1932', 'Turkish_KULLD', 'Turkish', 'daha', 'daha', 'daha', None), (40, 'Turkish', 'u1932', 'Turkish_KULLD', 'Turkish', 'vardı', 'vardı', 'vardı', None), (41, 'Turkish', 'u1932', 'Turkish_KULLD', 'Turkish', 'ama', 'ama', 'ama', None), (42, 'Turkish', 'u1932', 'Turkish_KULLD', 'Turkish', 'yok', 'yok', 'yok', None), (43, 'Turkish', 'u296', 'Turkish_KULLD', 'Turkish', 'anlaştık', 'anlaştık', 'anlaştık', None), (44, 'Turkish', 'u296', 'Turkish_KULLD', 'Turkish', 'baya', 'baya', 'baya', None), (45, 'Turkish', 'u296', 'Turkish_KULLD', 'Turkish', 'anlaştık', 'anlaştık', 'anlaştık', None), (46, 'Turkish', 'u296', 'Turkish_KULLD', 'Turkish', 'baya', 'baya', 'baya', None), (47, 'Turkish', 'u603', 'Turkish_KULLD', 'Turkish', 'lokma', 'lokma', 'lokma', None), (48, 'Turkish', 'u603', 'Turkish_KULLD', 'Turkish', 'al', 'al', 'al', None), (49, 'Turkish', 'u603', 'Turkish_KULLD', 'Turkish', 'alınca', 'alınca', 'alınca', None), (50, 'Turkish', 'u603', 'Turkish_KULLD', 'Turkish', 'bağrıyoruz', 'bağrıyoruz', 'bağrıyoruz', None), (51, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', 'zaten', 'zaten', 'zaten', None), (52, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', 'doğuş', 'doğuş', 'doğuş', 'not glossed; search ahead'), (53, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', 'doğuş', 'doğuş', 'doğuş', None), (54, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', 'kilonun', 'kilonun', 'kilonun', None), (55, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', 'şeyi', 'şeyi', 'şeyi', None), (56, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', 'hiç', 'hiç', 'hiç', None), (57, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', 'bi_şeyle', 'bi_şeyle', 'bir_şeyle', None), (58, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', None, None, None, 'See warning in Utterance table at: Turkish, u119 '), (59, 'Turkish', 'u119', 'Turkish_KULLD', 'Turkish', 'diğil', 'diğil', 'değil', None)]")
        
        session.close()
        
    def test_morphemes(self):
        """
        Test if all morphemes for Turkish test file are loaded
        """
        session = make_session('Turkish')
        self.assertEqual(session.query(db.Morpheme).count(), 33)
        
        s_turk = select([db.Morpheme])
        result_turk = session.execute(s_turk)
        self.assertEqual(str(result_turk.fetchall()), "[(1, 'Turkish', 'u1925', None, 'Turkish_KULLD', 'Turkish', 'target', 'bak', '???', '???', 'V', None), (2, 'Turkish', 'u1925', None, 'Turkish_KULLD', 'Turkish', 'target', '???', 'OPT&1P', 'OPT&1P', 'sfx', None), (3, 'Turkish', 'u1929', None, 'Turkish_KULLD', 'Turkish', 'target', 'tek', '???', '???', 'ADJ', None), (4, 'Turkish', 'u1929', None, 'Turkish_KULLD', 'Turkish', 'target', 'var', '???', '???', 'EXIST', None), (5, 'Turkish', 'u1933', None, 'Turkish_KULLD', 'Turkish', 'target', 'kaldır', '???', '???', 'V', None), (6, 'Turkish', 'u1933', None, 'Turkish_KULLD', 'Turkish', 'target', '???', 'PAST', 'PAST', 'sfx', None), (7, 'Turkish', 'u1933', None, 'Turkish_KULLD', 'Turkish', 'target', 'Necla', '???', '???', 'N:PROP', None), (8, 'Turkish', 'u1934', None, 'Turkish_KULLD', 'Turkish', 'target', 'kaldır', '???', '???', 'V', None), (9, 'Turkish', 'u1934', None, 'Turkish_KULLD', 'Turkish', 'target', '???', 'PAST', 'PAST', 'sfx', None), (10, 'Turkish', 'u1935', None, 'Turkish_KULLD', 'Turkish', 'target', 'gel', '???', '???', 'V', None), (11, 'Turkish', 'u1935', None, 'Turkish_KULLD', 'Turkish', 'target', 'sen', '???', '???', 'PRO', None), (12, 'Turkish', 'u1935', None, 'Turkish_KULLD', 'Turkish', 'target', 'gel', '???', '???', 'V', None), (13, 'Turkish', 'u1926', None, 'Turkish_KULLD', 'Turkish', 'target', 'tane', '???', '???', 'N', None), (14, 'Turkish', 'u1926', None, 'Turkish_KULLD', 'Turkish', 'target', 'daha', '???', '???', 'ADV', None), (15, 'Turkish', 'u1927', None, 'Turkish_KULLD', 'Turkish', 'target', 'tane', '???', '???', 'N', None), (16, 'Turkish', 'u1927', None, 'Turkish_KULLD', 'Turkish', 'target', 'daha', '???', '???', 'ADV', None), (17, 'Turkish', 'u1931', None, 'Turkish_KULLD', 'Turkish', 'target', 'tane', '???', '???', 'N', None), (18, 'Turkish', 'u1931', None, 'Turkish_KULLD', 'Turkish', 'target', 'daha', '???', '???', 'ADV', None), (19, 'Turkish', 'u1928', None, 'Turkish_KULLD', 'Turkish', 'target', 'tane', '???', '???', 'N', None), (20, 'Turkish', 'u1928', None, 'Turkish_KULLD', 'Turkish', 'target', 'minder', '???', '???', 'N', None), (21, 'Turkish', 'u1928', None, 'Turkish_KULLD', 'Turkish', 'target', 'yok', '???', '???', 'EXIST', None), (22, 'Turkish', 'u1930', None, 'Turkish_KULLD', 'Turkish', 'target', 'de', '???', '???', 'CONJ', None), (23, 'Turkish', 'u1930', None, 'Turkish_KULLD', 'Turkish', 'target', 'var', '???', '???', 'EXIST', None), (24, 'Turkish', 'u1932', None, 'Turkish_KULLD', 'Turkish', 'target', 'tane', '???', '???', 'N', None), (25, 'Turkish', 'u1932', None, 'Turkish_KULLD', 'Turkish', 'target', 'var', '???', '???', 'EXIST', None), (26, 'Turkish', 'u1932', None, 'Turkish_KULLD', 'Turkish', 'target', '???', 'PAST', 'PAST', 'sfx', None), (27, 'Turkish', 'u1932', None, 'Turkish_KULLD', 'Turkish', 'target', 'yok', '???', '???', 'EXIST', None), (28, 'Turkish', 'u296', None, 'Turkish_KULLD', 'Turkish', 'target', 'bayağı', '???', '???', 'ADV', None), (29, 'Turkish', 'u603', None, 'Turkish_KULLD', 'Turkish', 'target', 'al', '???', '???', 'V', None), (30, 'Turkish', 'u603', None, 'Turkish_KULLD', 'Turkish', 'target', '???', 'GER:INCE', 'GER:INCE', 'sfx', None), (31, 'Turkish', 'u603', None, 'Turkish_KULLD', 'Turkish', 'target', 'bağır', '???', '???', 'V', None), (32, 'Turkish', 'u603', None, 'Turkish_KULLD', 'Turkish', 'target', '???', 'IPFV', 'IPFV', 'sfx', None), (33, 'Turkish', 'u603', None, 'Turkish_KULLD', 'Turkish', 'target', '???', '1P', '1P', 'sfx', None)]")
        
        session.close()
    
    def test_speakers(self):
        """
        Test if all speakers for Cree test file are loaded
        """
        session = make_session('Turkish')
        self.assertEqual(session.query(db.Speaker).count(), 2)
        
        s_turk = select([db.Speaker])
        result_turk = session.execute(s_turk)
        self.assertEqual(str(result_turk.fetchall()), "[(1, 'Turkish', 'Turkish_KULLD', 'Turkish', 'CHI', 'Burcu', 'P0Y8M2D', '0;8.2', 242, 'female', 'Female', 'Target_Child', 'Target_Child', 'Target_Child', 'tur', None), (2, 'Turkish', 'Turkish_KULLD', 'Turkish', 'MOT', 'Gülcan', 'P25Y', '25;0.0', 9125, 'female', 'Female', 'Mother', 'Mother', 'Adult', 'tur', None)]")
        
        session.close()
        
    def test_uniquespeakers(self):
        """
        Test if all unique speakers for Turkish test file are loaded
        """
        session = make_session('Turkish')
        self.assertEqual(session.query(db.Uniquespeakers).count(),2)
        
        s_turk = select([db.Uniquespeakers])
        result_turk = session.execute(s_turk)
        self.assertEqual(str(result_turk.fetchall()), "[(1, 'CHI', 'Burcu', None, 'Female', 'Turkish_KULLD'), (2, 'MOT', 'Gülcan', None, 'Female', 'Turkish_KULLD')]")
        
        session.close()
        
        
class XMLTestYucatec(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = connect('Yucatec')
        cls.configs = ['Yucatec.ini']
        load_database(cls.configs, engine)
    

    def test_sessions(self):
        """
        Test if sessions for Yucatec test file are loaded
        """
        session = make_session('Yucatec')
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(XMLTestYucatec.configs))
        
        s = select([db.Session])
        result = session.execute(s)
        self.assertEqual(str(result.fetchall()), "[(1, 'Yucatec', 'Yucatec', 'Yucatec', '1996-01-03', 'Yucatec', None, None)]")
        session.close()
        
        
    def test_utterances(self):
        """
        Test if all utterances for Yucatec test file are loaded
        """
        session = make_session('Yucatec')
        self.assertEqual(session.query(db.Utterance).count(), 12)
        
        s_yuc = select([db.Utterance])
        result_yuc = session.execute(s_yuc)
        self.assertEqual(str(result_yuc.fetchall()), "[(1, 'Yucatec', 'Yucatec', 'Yucatec', 'u0', 'NEI', None, 'xáchet apool', 'xáchet apool', None, 'default', None, None, None, None, 'xáchet apool', None, None, None, None, None), (2, 'Yucatec', 'Yucatec', 'Yucatec', 'u1', 'ARM', None, 'pool', 'pool', None, 'default', None, None, None, None, 'pool', None, None, None, None, None), (3, 'Yucatec', 'Yucatec', 'Yucatec', 'u2', 'ARM', None, 'wich', 'wich', None, 'default', None, None, None, None, 'wich', None, None, None, None, None), (4, 'Yucatec', 'Yucatec', 'Yucatec', 'u3', 'NEI', None, 'wich tachʔop-ah awich yéet-el', 'wich tachʔop-ah awich yéet-el', None, 'default', None, None, None, None, 'wich tachʔop-ah awich yéet-el', None, None, None, None, None), (5, 'Yucatec', 'Yucatec', 'Yucatec', 'u4', 'ARM', None, 'wich xáacheʔ', 'wich xáacheʔ', None, 'default', None, None, None, None, 'wich xáacheʔ', None, None, None, None, None), (6, 'Yucatec', 'Yucatec', 'Yucatec', 'u5', 'LOR', None, 'yéet-el xáacheʔ', 'yéet-el xáacheʔ', None, 'default', None, None, None, None, 'yéet-el xáacheʔ', None, None, None, None, None), (7, 'Yucatec', 'Yucatec', 'Yucatec', 'u6', 'ARM', None, 'xáacheʔ', 'xáacheʔ', None, 'default', None, None, None, None, 'xáacheʔ', None, None, None, None, None), (8, 'Yucatec', 'Yucatec', 'Yucatec', 'u7', 'NEI', None, 'xáacheʔ chʔik teʔ tiʔ anookʔ-oʔ', 'xáacheʔ chʔik teʔ tiʔ anookʔ-oʔ', None, 'default', None, None, None, None, 'xáacheʔ chʔik teʔ tiʔ anookʔ-oʔ', None, None, None, None, None), (9, 'Yucatec', 'Yucatec', 'Yucatec', 'u8', 'ARM', None, 'chʔík', 'chʔík', None, 'default', None, None, None, None, 'chʔík', None, None, None, None, None), (10, 'Yucatec', 'Yucatec', 'Yucatec', 'u9', 'LOR', None, 'tiʔ abolsa', 'tiʔ abolsa', None, 'question', None, None, None, None, 'tiʔ abolsa', None, None, None, None, None), (11, 'Yucatec', 'Yucatec', 'Yucatec', 'u24', 'ARM', None, '??? yan inmaháant-ik', '??? yan inmaháant-ik', None, 'default', None, None, None, None, '??? yan inmaháant-ik', None, None, None, None, None), (12, 'Yucatec', 'Yucatec', 'Yucatec', 'u0', 'SAN', None, 'le wat-oʔ neneʔ', 'le wat-oʔ neneʔ', None, 'default', None, None, None, None, 'le wat-oʔ neneʔ', None, None, None, None, 'broken alignment full_word : segments/glosses')]")
        
        session.close()
        
        
        
    def test_words(self):
        """
        Test if all words for Cree test file are loaded
        """
        session = make_session('Yucatec')
        self.assertEqual(session.query(db.Word).count(), 27)
        
        s_yuc = select([db.Word])
        result_yuc = session.execute(s_yuc)
        self.assertEqual(str(result_yuc.fetchall()), "[(1, 'Yucatec', 'u0', 'Yucatec', 'Yucatec', 'xáchet', '???', 'xáchet', None), (2, 'Yucatec', 'u0', 'Yucatec', 'Yucatec', 'apool', '???', 'apool', None), (3, 'Yucatec', 'u1', 'Yucatec', 'Yucatec', 'pool', '???', 'pool', None), (4, 'Yucatec', 'u2', 'Yucatec', 'Yucatec', 'wich', '???', 'wich', None), (5, 'Yucatec', 'u3', 'Yucatec', 'Yucatec', 'wich', '???', 'wich', None), (6, 'Yucatec', 'u3', 'Yucatec', 'Yucatec', 'tachʔop-ah', '???', 'tachʔop-ah', None), (7, 'Yucatec', 'u3', 'Yucatec', 'Yucatec', 'awich', '???', 'awich', None), (8, 'Yucatec', 'u3', 'Yucatec', 'Yucatec', 'yéet-el', '???', 'yéet-el', None), (9, 'Yucatec', 'u4', 'Yucatec', 'Yucatec', 'wich', '???', 'wich', None), (10, 'Yucatec', 'u4', 'Yucatec', 'Yucatec', 'xáacheʔ', '???', 'xáacheʔ', None), (11, 'Yucatec', 'u5', 'Yucatec', 'Yucatec', 'yéet-el', '???', 'yéet-el', None), (12, 'Yucatec', 'u5', 'Yucatec', 'Yucatec', 'xáacheʔ', '???', 'xáacheʔ', None), (13, 'Yucatec', 'u6', 'Yucatec', 'Yucatec', 'xáacheʔ', '???', 'xáacheʔ', None), (14, 'Yucatec', 'u7', 'Yucatec', 'Yucatec', 'xáacheʔ', '???', 'xáacheʔ', None), (15, 'Yucatec', 'u7', 'Yucatec', 'Yucatec', 'chʔik', '???', 'chʔik', None), (16, 'Yucatec', 'u7', 'Yucatec', 'Yucatec', 'teʔ', '???', 'teʔ', None), (17, 'Yucatec', 'u7', 'Yucatec', 'Yucatec', 'tiʔ', '???', 'tiʔ', None), (18, 'Yucatec', 'u7', 'Yucatec', 'Yucatec', 'anookʔ-oʔ', '???', 'anookʔ-oʔ', None), (19, 'Yucatec', 'u8', 'Yucatec', 'Yucatec', 'chʔík', '???', 'chʔík', None), (20, 'Yucatec', 'u9', 'Yucatec', 'Yucatec', 'tiʔ', '???', 'tiʔ', None), (21, 'Yucatec', 'u9', 'Yucatec', 'Yucatec', 'abolsa', '???', 'abolsa', None), (22, 'Yucatec', 'u24', 'Yucatec', 'Yucatec', '???', '???', '???', 'not glossed'), (23, 'Yucatec', 'u24', 'Yucatec', 'Yucatec', 'yan', '???', 'yan', None), (24, 'Yucatec', 'u24', 'Yucatec', 'Yucatec', 'inmaháant-ik', '???', 'inmaháant-ik', None), (25, 'Yucatec', 'u0', 'Yucatec', 'Yucatec', 'le', '???', 'le', None), (26, 'Yucatec', 'u0', 'Yucatec', 'Yucatec', 'wat-oʔ', '???', 'wat-oʔ', None), (27, 'Yucatec', 'u0', 'Yucatec', 'Yucatec', 'neneʔ', '???', 'neneʔ', None)]")
        
        session.close()
        
    def test_morphemes(self):
        """
        Test if all morphemes for Yucatec test file are loaded
        """
        session = make_session('Yucatec')
        self.assertEqual(session.query(db.Morpheme).count(), 45)
        
        s_yuc = select([db.Morpheme])
        result_yuc = session.execute(s_yuc)
        self.assertEqual(str(result_yuc.fetchall()), "[(1, 'Yucatec', 'u0', None, 'Yucatec', 'Yucatec', 'target', 'xáchet', '???', '???', 'VT', None), (2, 'Yucatec', 'u0', None, 'Yucatec', 'Yucatec', 'target', '0', 'IMP', 'IMP', 'sfx', None), (3, 'Yucatec', 'u0', None, 'Yucatec', 'Yucatec', 'target', 'a', '2POS', '2SG.POSS', 'pfx', None), (4, 'Yucatec', 'u0', None, 'Yucatec', 'Yucatec', 'target', 'pool', '???', '???', 'S', None), (5, 'Yucatec', 'u1', None, 'Yucatec', 'Yucatec', 'target', 'pool', '???', '???', 'S', None), (6, 'Yucatec', 'u2', None, 'Yucatec', 'Yucatec', 'target', 'w', '1POS', '1SG.POSS', 'pfx', None), (7, 'Yucatec', 'u2', None, 'Yucatec', 'Yucatec', 'target', 'ich', '???', '???', 'S', None), (8, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'w', '2POS', '2SG.POSS', 'pfx', None), (9, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'ich', '???', '???', 'S', None), (10, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 't', 'PFV', 'PFV', 'pfx', None), (11, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'a', '2ERG', '2.ERG', 'pfx', None), (12, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'chʔop', '???', '???', 'VT', None), (13, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'ah', 'PFV', 'PFV', 'sfx', None), (14, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'a', '2POS', '2SG.POSS', 'pfx', None), (15, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'w', 'PT', '???', 'pfx', None), (16, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'ich', '???', '???', 'S', None), (17, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'y', '3POS', '3SG.POSS', 'pfx', None), (18, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', 'éet', '???', '???', 'S', None), (19, 'Yucatec', 'u3', None, 'Yucatec', 'Yucatec', 'target', '???', 'POS-el', 'POS-el', 'sfx', None), (20, 'Yucatec', 'u4', None, 'Yucatec', 'Yucatec', 'target', 'w', '1POS', '1SG.POSS', 'pfx', None), (21, 'Yucatec', 'u4', None, 'Yucatec', 'Yucatec', 'target', 'ich', '???', '???', 'S', None), (22, 'Yucatec', 'u4', None, 'Yucatec', 'Yucatec', 'target', 'xáacheʔ', '???', '???', 'S', None), (23, 'Yucatec', 'u5', None, 'Yucatec', 'Yucatec', 'target', 'y', '3POS', '3SG.POSS', 'pfx', None), (24, 'Yucatec', 'u5', None, 'Yucatec', 'Yucatec', 'target', 'éet', '???', '???', 'S', None), (25, 'Yucatec', 'u5', None, 'Yucatec', 'Yucatec', 'target', 'el', 'POS', 'POSS', 'sfx', None), (26, 'Yucatec', 'u5', None, 'Yucatec', 'Yucatec', 'target', 'xáacheʔ', '???', '???', 'S', None), (27, 'Yucatec', 'u6', None, 'Yucatec', 'Yucatec', 'target', 'xáacheʔ', '???', '???', 'S', None), (28, 'Yucatec', 'u7', None, 'Yucatec', 'Yucatec', 'target', 'xáacheʔ', '???', '???', 'S', None), (29, 'Yucatec', 'u7', None, 'Yucatec', 'Yucatec', 'target', 'chʔik', '???', '???', 'VT', None), (30, 'Yucatec', 'u7', None, 'Yucatec', 'Yucatec', 'target', 'teʔ', '???', '???', 'DEICT', None), (31, 'Yucatec', 'u7', None, 'Yucatec', 'Yucatec', 'target', 'tiʔ', '???', '???', 'PREP', None), (32, 'Yucatec', 'u7', None, 'Yucatec', 'Yucatec', 'target', 'a', '2POS', '2SG.POSS', 'pfx', None), (33, 'Yucatec', 'u7', None, 'Yucatec', 'Yucatec', 'target', '???', 'nookʔ', 'nookʔ', '???', None), (34, 'Yucatec', 'u7', None, 'Yucatec', 'Yucatec', 'target', 'oʔ', 'DIST', 'DIST', 'sfx', None), (35, 'Yucatec', 'u8', None, 'Yucatec', 'Yucatec', 'target', 'chʔik', '???', '???', 'VT', None), (36, 'Yucatec', 'u9', None, 'Yucatec', 'Yucatec', 'target', 'tiʔ', '???', '???', 'PREP', None), (37, 'Yucatec', 'u9', None, 'Yucatec', 'Yucatec', 'target', 'a', '2POS', '2SG.POSS', 'pfx', None), (38, 'Yucatec', 'u9', None, 'Yucatec', 'Yucatec', 'target', 'bolsa', '???', '???', 'S', None), (39, 'Yucatec', 'u24', None, 'Yucatec', 'Yucatec', 'target', 'yan', 'OBLIG', 'OBLIG', '???', None), (40, 'Yucatec', 'u24', None, 'Yucatec', 'Yucatec', 'target', 'in', '1ERG', '1.ERG', 'pfx', None), (41, 'Yucatec', 'u24', None, 'Yucatec', 'Yucatec', 'target', 'maháant', '???', '???', 'VT', None), (42, 'Yucatec', 'u24', None, 'Yucatec', 'Yucatec', 'target', 'ik', 'IMPF', 'IPFV', 'sfx', None), (43, 'Yucatec', 'u0', None, 'Yucatec', 'Yucatec', 'target', 'le', '???', '???', 'DET', None), (44, 'Yucatec', 'u0', None, 'Yucatec', 'Yucatec', 'target', 'awat', '???', '???', 'V', None), (45, 'Yucatec', 'u0', None, 'Yucatec', 'Yucatec', 'target', 'oʔ', 'DIST', 'DIST', 'sfx', None)]")
        
        session.close()
    
    
    def test_speakers(self):
        """
        Test if all speakers for Yucatec test file are loaded
        """
        session = make_session('Yucatec')
        self.assertEqual(session.query(db.Speaker).count(), 2)
        
        s_yuc = select([db.Speaker])
        result_yuc = session.execute(s_yuc)
        self.assertEqual(str(result_yuc.fetchall()), "[(1, 'Yucatec', 'Yucatec', 'Yucatec', 'ARM', None, None, None, None, None, 'Unspecified', 'Target_Child', 'Target_Child', 'Target_Child', 'yua', None), (2, 'Yucatec', 'Yucatec', 'Yucatec', 'SAN', None, None, None, None, None, 'Unspecified', 'Child', 'Child', 'Child', 'yua', None)]")
        
        session.close()
        
    def test_uniquespeakers(self):
        """
        Test if all unique speakers for Yucatec test file are loaded
        """
        session = make_session('Yucatec')
        self.assertEqual(session.query(db.Uniquespeakers).count(),2)
        
        s_yuc = select([db.Uniquespeakers])
        result_yuc = session.execute(s_yuc)
        self.assertEqual(str(result_yuc.fetchall()), "[(1, 'ARM', None, None, 'Unspecified', 'Yucatec'), (2, 'SAN', None, None, 'Unspecified', 'Yucatec')]")
        
        session.close()
        
        
    
    

if __name__ == "__main__":
    current_dir = os.getcwd()
    sys.path.append(current_dir)

    import database_backend as db
    import processors as processors
    import unittest
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import func
    import parsers as parsers

