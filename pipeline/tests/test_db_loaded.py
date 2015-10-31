import unittest
import re

import database_backend as db
import metadata as metadata
import processors as processors
import postprocessor as pp
import time
import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from toolbox import ToolboxFile
import parsers as parsers


# helper functions
def connect():
    """ Performs database connection. We can add a database settings
    from settings.py later. Returns sqlalchemy engine instance.
    """
    # TODO: add postgres settings and change to postgres
    # return create_engine(URL(**settings.DATABASE))
    return db.create_engine('sqlite:///test_acqdiv.sqlite3', echo=False)

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
        cfg.session_files = cfg.session_files[:4]

        # Process by parsing the files and adding extracted data to the db
        c = processors.CorpusProcessor(cfg, engine)
        c.process_corpus()

        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        pp.update_age(cfg, engine)
        pp.unify_glosses(cfg, engine)

class PipelineTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize database connection and drop and then create tables on each call.
        # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
        engine = connect()

        # cls.configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Russian.ini', 'Japanese_Miyata.ini']
        cls.configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Inuktitut.ini', 'Japanese_Miyata.ini',
               'Japanese_MiiPro.ini', 'Russian.ini', 'Sesotho.ini', 'Turkish.ini']
        # cls.configs = ['Cree.ini', 'Indonesian.ini', 'Russian.ini']
        # cls.configs = ['Chintang.ini']
        # cls.configs = ['Cree.ini']
        # cls.configs = ['Indonesian.ini']
        # cls.configs = ['Russian.ini']
        # cls.configs = ['CreeJSON.ini']
        # cls.configs = ['Sesotho.ini']
        # cls.configs = ['Japanese_Miyata.ini']

        load_database(cls.configs, engine)

    def testLppSessionsOk(self):
        """
        Test if sessions for all corpora are loaded
        """
        session = make_session()
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(PipelineTest.configs))
        session.close()

    def testLppSpeakersOk(self):

        session = make_session()
        self.assertNotEqual(session.query(db.Speaker).count(), 0)
        session.close()

    def testLppUtterancesOk(self):

        session = make_session()
        self.assertNotEqual(session.query(db.Utterance).count(), 0)
        session.close()

    def testLppWordsOk(self):

        session = make_session()
        self.assertNotEqual(session.query(db.Word).count(), 0)
        session.close()

    def testLppMorphemesOk(self):

        session = make_session()
        self.assertNotEqual(session.query(db.Morpheme).count(), 0)
        session.close()

if __name__ == "__main__":
    main()