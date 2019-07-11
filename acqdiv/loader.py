""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""
import time
import datetime
import argparse

from sqlalchemy import create_engine

from acqdiv.database.database_backend import Base
from acqdiv.parsers.CorpusConfigParser import CorpusConfigParser
from acqdiv.parsers.CorpusParserMapper import CorpusParserMapper
from acqdiv.database.DBProcessor import DBProcessor


class Loader:

    def load(self, test=True, new=False, phonbank=False):
        """Load data from source files into DB.

        Args:
            test (bool): Test DB is used.
            new (bool): Run over the new corpora as well.
            phonbank (bool): Run over the Phonbank corpora.
        """
        start_time = time.time()

        engine = self._get_engine(test=test)

        configs = [
            'Chintang.ini',
            'English_Manchester1.ini',
            'Indonesian.ini',
            'Russian.ini',
            'Cree.ini',
            'Inuktitut.ini',
            'Japanese_Miyata.ini',
            'Japanese_MiiPro.ini',
            'Nungon.ini',
            'Qaqet.ini',
            'Sesotho.ini',
            'Tuatschin.ini',
            'Turkish.ini',
            'Yucatec.ini'
        ]

        if new:
            configs += [
                'Dene.ini',
                'Ku_Waru.ini'
            ]

        if phonbank:

            base_path = 'Phonbank/'

            configs = [
                base_path + 'Arabic_Kuwaiti.ini',
                base_path + 'Arabic_Kern.ini',
                base_path + 'Berber.ini',
                base_path + 'Polish.ini',
                base_path + 'Quichua.ini'
            ]

        for config in configs:

            cfg = CorpusConfigParser()
            cfg.read("ini/"+config)

            print("{0} seconds --- Start processing: {1}".format(
                time.time() - start_time, config.split(".")[0]))

            # get corpus parser based on corpus name
            name = cfg['corpus']['corpus']
            corpus_parser_class = CorpusParserMapper.map(name)
            corpus_parser = corpus_parser_class(cfg)

            # get the corpus
            corpus = corpus_parser.parse()

            # add the corpus to the DB
            proc = DBProcessor(corpus, engine, test=test)
            proc.process_corpus()

        print("%s seconds --- Finished" % (time.time() - start_time))
        print()
        print("Next, call:")

        if test:
            print("acqdiv postprocess")
        else:
            print("acqdiv postprocess -f")
        print()

    @classmethod
    def _get_engine(cls, test=False):
        """Return a database engine.

        Args:
            test (bool): Is the test DB used?

        Returns:
            Engine: The DB engine.
        """
        if test:
            print("Writing test database to: database/test.sqlite3")
            print()
            engine = cls.db_connect('sqlite:///database/test.sqlite3')
            cls.create_tables(engine)
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            path = 'sqlite:///database/acqdiv_corpus_{}.sqlite3'.format(date)
            print("Writing database to: {}".format(path))
            print()
            engine = cls.db_connect(path)
            cls.create_tables(engine)

        return engine

    @staticmethod
    def db_connect(path):
        """Perform database connection.

        If desired, add database settings in settings.py, e.g. for postgres:
        return create_engine(URL(**settings.DATABASE)).

        Args:
            path (str) : Path to DB.

        Returns:
            SQLAlchemy engine instance.
        """
        return create_engine(path, echo=False)

    @staticmethod
    def create_tables(engine):
        """Drop all tables before creating them.

            Args:
                engine: An sqlalchemy database engine.
        """
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(engine)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()

    loader = Loader()
    loader.load(test=args.t)


if __name__ == "__main__":
    main()
