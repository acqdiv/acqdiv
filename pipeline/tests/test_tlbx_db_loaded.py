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
def connect():
    """ Performs database connection. We can add a database settings
    from settings.py later. Returns sqlalchemy engine instance.
    """
    return db.create_engine('sqlite:///tests/test_tlbx_acqdiv.sqlite3', echo=False)

def make_session():
    engine = connect()
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
        print(cfg.session_files)

        # Process by parsing the files and adding extracted data to the db
        c = processors.CorpusProcessor(cfg, engine)
        c.process_corpus()
        
        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        pp.update_age(cfg, engine)
        pp.unify_glosses(cfg, engine)

class ToolbxTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize database connection and drop and then create tables on each call.
        # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
        engine = connect()

        cls.configs = ['Chintang.ini', 'Russian.ini', 'Indonesian.ini']
        
        load_database(cls.configs, engine)
    

    def testXMLSessions(self):
        """
        Test if sessions for Toolbox test files are loaded
        """
        session = make_session()
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(ToolbxTest.configs))
        session.close()
        
        
    def testXMLUtterances(self):
        """
        Test if all utterances for Toolbox test files are loaded
        """
        session = make_session()
        self.assertEqual(session.query(db.Utterance).count(),  2246)
        session.close()
        
        
    def testXMLWords(self):
        """
        Test if all words for Toolbox test files are loaded
        """
        session = make_session()
        self.assertEqual(session.query(db.Word).count(), 5223)
        session.close()
        
        
    def testXMLMorphemes(self):
        """
        Test if all morphemes for Toolbox test files are loaded
        """
        session = make_session()
        self.assertEqual(session.query(db.Morpheme).count(), 5830)
        session.close()
        

    def testXMLSpeakers(self):
        """
        Test if all speakers for Toolbox test files are loaded
        """
        session = make_session()
        self.assertEqual(session.query(db.Speaker).count(),  34 )
        session.close()
        
        
    def textXMLUniquespeakers(self):
        """
        Test if all unique speakers for Toolbox test files are loaded
        """
        session = make_session()
        self.assertEqual(session.query(db.Uniquespeakers).count(),13)
    
    
    
    
    
    
    

if __name__ == "__main__":
    current_dir = os.getcwd()
    sys.path.append(current_dir)

    import database_backend as db
    import processors as processors
    import unittest
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import func
    import parsers as parsers
