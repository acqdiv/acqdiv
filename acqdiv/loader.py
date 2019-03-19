""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""
import time
import argparse
import logging

from acqdiv import pipeline_logging
from acqdiv.processors.processors import CorpusProcessor
from acqdiv.parsers.parsers import CorpusConfigParser
from acqdiv.database_backend import db_connect, create_tables


def set_logger(level_i=False, supressing_formatter=False):
    """Set a logger.

    Args:
        level_i (bool): logging level is set to INFO

    """
    logger = logging.getLogger('pipeline')
    handler = logging.FileHandler('errors.log', mode='w')
    if level_i:
        handler.setLevel(logging.INFO)
    else:
        handler.setLevel(logging.WARNING)

    if supressing_formatter:
        formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                      '%(levelname)s - %(message)s')
    else:
        formatter = pipeline_logging.SuppressingFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Uncomment to define a Handler which writes INFO messages or higher to the sys.stderr.
    """
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    """


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
        print("Writing database to: database/acqdiv.sqlite3")
        print()
        engine = db_connect('sqlite:///database/acqdiv.sqlite3')
        create_tables(engine)

    return engine


def load(test=True, catch_errors=False, xml=False, new=False, phonbank=False):
    """Load data from source files into DB.

    Args:
        test (bool): Test DB is used.
        catch_errors (bool): Errors are caught.
        xml (bool): Run the XML parsers rather than the CHAT parsers.
        new (bool): Run over the new corpora as well.
        phonbank (bool): Run over the Phonbank corpoa as well.
    """
    start_time = time.time()

    engine = _get_engine(test=test)

    configs = [
        'Chintang.ini',
        'English_Manchester1.ini',
        'Indonesian.ini',
        'Russian.ini'
    ]

    if xml:
        base_path = 'xml/'

        configs += [
            base_path + 'Cree.ini',
            base_path + 'Inuktitut.ini',
            base_path + 'Japanese_Miyata.ini',
            base_path + 'Japanese_MiiPro.ini',
            base_path + 'Nungon.ini',
            base_path + 'Sesotho.ini',
            base_path + 'Turkish.ini',
            base_path + 'Yucatec.ini'
        ]

    else:
        configs += [
            'Cree.ini',
            'Inuktitut.ini',
            'Japanese_Miyata.ini',
            'Japanese_MiiPro.ini',
            'Nungon.ini',
            'Sesotho.ini',
            'Turkish.ini',
            'Yucatec.ini'
        ]

    if new:
        configs += [
            'Dene.ini',
            'Ku_Waru.ini',
            'Qaqet.ini',
            'Tuatschin.ini'
        ]

    if phonbank:
        base_path = 'Phonbank/'

        configs += [
            base_path + 'Arabic_Kuwaiti.ini',
            base_path + 'Arabic_Kern.ini',
            base_path + 'Berber.ini',
            base_path + 'Polish.ini',
            base_path + 'Quichua.ini'
        ]

    # Parse the config file and call the sessions processor.
    for config in configs:
        cfg = CorpusConfigParser()
        cfg.read("ini/"+config)

        # If test mode use test corpora path by overwriting cfg['paths']['path'].
        if test:
            cfg['paths']['path'] = "tests/corpora"

        # Process by parsing the files and adding extracted data to the database.
        print("{0} seconds --- Start processing: {1}".format(
            time.time() - start_time, config.split(".")[0]))
        c = CorpusProcessor(cfg, engine)
        c.process_corpus(catch_errors=catch_errors)

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
    p.add_argument('-s', action='store_true')
    p.add_argument('-i', action='store_true')
    args = p.parse_args()

    set_logger(level_i=args.i, supressing_formatter=args.s)
    load(test=args.t)


if __name__ == "__main__":
    main()
