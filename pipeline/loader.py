""" Entry point for loading acqdiv corpora into the database
"""

from processors import *
from postprocessor import *
from parsers import *
from database_backend import *


def main(args):
    """ Main processing loop; for each corpus config file process all session recordings and load database.
    """

    if args.t:
        print("Testing mode")
        engine = db_connect('sqlite:///../database/acqdiv.sqlite3')
    create_tables(engine)

    configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Inuktitut.ini', 'Japanese_Miyata.ini',
                'Japanese_MiiPro.ini', 'Russian.ini', 'Sesotho.ini', 'Turkish.ini', 'Yucatec.ini']

    # Parse the config file and call the sessions processor
    for config in configs:
        cfg = CorpusConfigParser()
        cfg.read(config)
        # cfg.read("ini/"+config)

        # If test mode use test corpora
        if args.t:
            cfg['paths']['path'] = "tests/corpora"

        # Process by parsing the files and adding extracted data to the db
        c = CorpusProcessor(cfg, engine)
        c.process_corpus()

        # Do some postprocessing
        # TODO: test if moving this outside of the loop is faster
        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        update_age(cfg, engine)
        unify_timestamps(cfg, engine)
        unify_glosses(cfg, engine)
        unify_gender(cfg, engine)

        if config == 'Indonesian.ini':
            unify_indonesian_labels(cfg, engine)
            clean_tlbx_pos_morphemes(cfg, engine)
            clean_utterances_table(cfg, engine)

        if config == 'Chintang.ini':
            extract_chintang_addressee(cfg, engine)
            clean_tlbx_pos_morphemes(cfg, engine)
            clean_utterances_table(cfg, engine)

        if config == 'Russian.ini':
            clean_utterances_table(cfg, engine)

    print("Creating role entries...")
    unify_roles(cfg, engine)

    print("Creating macrorole entries...")
    macrorole(cfg, engine)

    print("Creating unique speaker table...")
    unique_speaker(cfg, engine)

if __name__ == "__main__":
    import time
    import sys
    import argparse

    start_time = time.time()

    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()

    main(args)

    print("--- %s seconds ---" % (time.time() - start_time))
