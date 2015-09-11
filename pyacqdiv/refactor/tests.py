#!/usr/bin/bash
#-*- coding: utf-8 -*-

# Test suite for the acqdiv processors and database

import database_backend as db
import metadata
import parsers
import processors
import postprocessor as pp
import time
import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


# helper functions

def test_connect():
    """ Performs database connection. We can add a database settings
    from settings.py later. Returns sqlalchemy engine instance.
    """
    # TODO: add postgres settings and change to postgres
    # return create_engine(URL(**settings.DATABASE))
    return db.create_engine('sqlite:///test_acqdiv.sqlite3', echo=False)

def test_make_session():
    engine = test_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def testLoadDatabase(configs, engine):
    db.create_tables(engine)

    for config in configs:
        # Parse the config file and call the sessions processor
        cfg = parsers.CorpusConfigParser()
        cfg.read(config)
        cfg.session_files = cfg.session_files[:8]

        # Process by parsing the files and adding extracted data to the db
        c = processors.CorpusProcessor(cfg, engine)
        c.process_corpus()

        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        pp.update_age(cfg)
        pp.unify_glosses(cfg)

# metadata tests

class TestMetadataParser(unittest.TestCase):

    def setUp(self):
        self.cfg = parsers.CorpusConfigParser()

class TestImdiParser(TestMetadataParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Russian.ini")
        self.imdi = metadata.Imdi(self.cfg, "../../corpora/Russian/metadata/A00210817.imdi")

    def testBasicImdiParsing(self):
        for k, v in self.imdi.metadata.items():
            self.assertFalse(v == None)

    def testImdiDateField(self):
        self.assertFalse(self.imdi.metadata["session"]["date"] == None)

class TestXMLParser(TestMetadataParser):

    def setUp(self):
        super().setUp()
        self.cfg.read("Cree.ini")
        self.xml = metadata.Chat(self.cfg, "../../corpora/Cree/xml/Ani/2005-09-14.xml")

    def testBasicXMLParsing(self):
        for k, v in self.xml.metadata.items():
            self.assertFalse(v == None)


# pipeline tests

class PipelineTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize database connection and drop and then create tables on each call.
        # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
        engine = test_connect()

        cls.configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Russian.ini', 'Japanese_Miyata.ini']
        # configs = ['Cree.ini', 'Indonesian.ini', 'Russian.ini']
        # configs = ['Chintang.ini']
        # configs = ['Cree.ini']
        # configs = ['Indonesian.ini']
        # configs = ['Russian.ini']
        # configs = ['CreeJSON.ini']
        # configs = ['Sesotho.ini']
        # configs = ['Japanese_Miyata.ini']

        testLoadDatabase(cls.configs, engine)

    def testLppSessionsOk(self):
        """
        Test if sessions for all corpora are loaded
        """
        session = test_make_session()
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(PipelineTest.configs))

    def testLppSpeakersOk(self):

        session = test_make_session()
        self.assertNotEqual(session.query(db.Speaker).count(), 0)

    def testLppUtterancesOk(self):

        session = test_make_session()
        self.assertNotEqual(session.query(db.Utterance).count(), 0)

    def testLppWordsOk(self):

        session = test_make_session()
        self.assertNotEqual(session.query(db.Word).count(), 0)

    def testLppMorphemesOk(self):

        session = test_make_session()
        self.assertNotEqual(session.query(db.Morpheme).count(), 0)


if __name__ == "__main__":
    unittest.main()
