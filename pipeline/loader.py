""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""

from processors import *
from processors.postprocessor import *
from parsers import *
from database_backend import *


def main(args):
    """ Main processing loop; for each corpus config file process all session recordings and load database.
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
        c = CorpusProcessor(cfg, engine)
        c.process_corpus()

        # Do some postprocessing
        # TODO: test if moving this outside of the loop is faster
        print("Postprocessing: {0}".format(config.split(".")[0]))

        update_age(cfg, engine)
        unify_timestamps(cfg, engine)
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

        # This seems to need to be applied after the clean_tlbx_pos_morphemes... which should be moved to the parser.
        unify_labels(cfg, engine)
        get_word_pos(cfg, engine)

        print()

    print("Calculating role entries.\n")
    unify_roles(cfg, engine)

    print("Calculating macrorole entries.\n")
    macrorole(cfg, engine)

    print("Calculating unique speaker table.\n")
    unique_speaker(cfg, engine)

    print()

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
