""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""

from processors import *
from parsers import *
from database_backend import *
import logging


def main(args):
    """ Main processing loop; for each corpus config file process all session recordings and load database.
    """
    logging.basicConfig(filemode='w')
    logger = logging.getLogger('pipeline')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('errors.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                    '%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # uncomment to define a Handler which writes INFO messages or higher to the sys.stderr
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

    # If testing mode
    if args.t:
        print("Writing test database to: acqdiv/pipeline/tests/test.sqlite3")
        print()
        engine = db_connect('sqlite:///tests/test.sqlite3')
        create_tables(engine)
    else:
        print("Writing database to: acqdiv/database/acqdiv.sqlite3")
        print()
        engine = db_connect('sqlite:///../database/acqdiv.sqlite3')
        create_tables(engine)

    configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Inuktitut.ini', 'Japanese_Miyata.ini',
                'Japanese_MiiPro.ini', 'Russian.ini', 'Sesotho.ini', 'Turkish.ini', 'Yucatec.ini']

    # Parse the config file and call the sessions processor
    for config in configs:
        cfg = CorpusConfigParser()
        cfg.read("ini/"+config)

        # If test mode use test corpora path by overwriting cfg['paths']['path'].
        if args.t:
            cfg['paths']['path'] = "tests/corpora"

        # Process by parsing the files and adding extracted data to the db
        print("{0} seconds --- Start processing: {1}".format(time.time() - start_time, config.split(".")[0]))
        c = CorpusProcessor(cfg, engine)
        c.process_corpus()


if __name__ == "__main__":
    import time
    import argparse

    start_time = time.time()

    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()

    main(args)

    print("%s seconds --- Finished" % (time.time() - start_time))
    print()
    print("Next, call: python3 postprocessor.py")
