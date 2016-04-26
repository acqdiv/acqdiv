""" Entry point for loading ACQDIV raw input corpora data into the ACQDIV-DB
"""

from processors import *
from postprocessor import *
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
        print("%s seconds --- Start processing: {1}".format(time.time() - start_time, config.split(".")[0]))
        c = CorpusProcessor(cfg, engine)
        c.process_corpus()

        # Do some postprocessing
        # TODO: test if moving this outside of the loop is faster
        print("{0} seconds --- Start postprocessing: {1}".format(time.time() - start_time, config.split(".")[0]))

        update_age(cfg, engine)
        print("%s seconds --- update_age" % (time.time() - start_time))

        unify_timestamps(cfg, engine)
        print("%s seconds --- unify_timestamps" % (time.time() - start_time))

        unify_gender(cfg, engine)
        print("%s seconds --- unify_gender" % (time.time() - start_time))

        if config == 'Indonesian.ini':
            unify_indonesian_labels(cfg, engine)
            print("%s seconds --- Indonesian unify_indonesian_labels" % (time.time() - start_time))
            clean_tlbx_pos_morphemes(cfg, engine)
            print("%s seconds --- Indonesian clean_tlbx_pos_morphemes" % (time.time() - start_time))
            clean_utterances_table(cfg, engine)
            print("%s seconds --- Indonesian clean_utterances_table" % (time.time() - start_time))

        if config == 'Chintang.ini':
            extract_chintang_addressee(cfg, engine)
            print("%s seconds --- Chintang extract_chintang_addressee" % (time.time() - start_time))
            clean_tlbx_pos_morphemes(cfg, engine)
            print("%s seconds --- Chintang clean_tlbx_pos_morphemes" % (time.time() - start_time))
            clean_utterances_table(cfg, engine)
            print("%s seconds --- Chintang clean_utterances_table" % (time.time() - start_time))

        if config == 'Russian.ini':
            clean_utterances_table(cfg, engine)
            print("%s seconds --- Russian clean_utterances_table" % (time.time() - start_time))

        # This seems to need to be applied after the clean_tlbx_pos_morphemes... which should be moved to the parser.
        unify_labels(cfg, engine)
        print("%s seconds --- unify_labels" % (time.time() - start_time))

        get_word_pos(cfg, engine)
        print("%s seconds --- get_word_pos" % (time.time() - start_time))

        # print()

    unify_roles(cfg, engine)
    print("%s seconds --- unify_roles" % (time.time() - start_time))

    macrorole(cfg, engine)
    print("%s seconds --- macrorole" % (time.time() - start_time))

    unique_speaker(cfg, engine)
    print("%s seconds --- unique_speaker" % (time.time() - start_time))

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
