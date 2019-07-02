""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""
import time
import datetime
import argparse
from acqdiv.parsers.CorpusConfigParser import CorpusConfigParser
from acqdiv.database_backend import db_connect, create_tables
from acqdiv.parsers.CorpusParserMapper import CorpusParserMapper


def _get_engine(test=False):
    """Return a database engine.

    Args:
        test (bool): test database created
    """
    if test:
        print("Writing test database to: database/test.sqlite3")
        print()
        engine = db_connect('sqlite:///database/test.sqlite3')
        create_tables(engine)
    else:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        path = 'sqlite:///database/acqdiv_corpus_{}.sqlite3'.format(date)
        print("Writing database to: {}".format(path))
        print()
        engine = db_connect(path)
        create_tables(engine)

    return engine


def load(test=True, new=False, phonbank=False):
    """Load data from source files into DB.

    Args:
        test (bool): Test DB is used.
        new (bool): Run over the new corpora as well.
        phonbank (bool): Run over the Phonbank corpora.
    """
    start_time = time.time()

    engine = _get_engine(test=test)

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

        name = cfg['corpus']['corpus']

        corpus_parser = CorpusParserMapper.map(name)

        c = corpus_parser(cfg, engine)
        c.process_corpus(test=test)

    print("%s seconds --- Finished" % (time.time() - start_time))
    print()
    print("Next, call:")

    if test:
        print("acqdiv postprocess")
    else:
        print("acqdiv postprocess -f")
    print()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()
    load(test=args.t)


if __name__ == "__main__":
    main()
