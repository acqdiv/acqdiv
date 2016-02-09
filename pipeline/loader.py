""" Entry point for loading acqdiv corpora into the database
    TODO: incorporate into pyacqdiv
"""

from processors import *
from postprocessor import *
from parsers import *
from database_backend import *
import time

if __name__ == "__main__":
    start_time = time.time()
    engine = db_connect()
    create_tables(engine)

    configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Inuktitut.ini', 'Japanese_Miyata.ini',
                'Japanese_MiiPro.ini', 'Russian.ini', 'Sesotho.ini', 'Turkish.ini', 'Yucatec.ini']

<<<<<<< HEAD
    configs = ['Chintang.ini', 'Russian.ini']
=======
    configs = ['Chintang.ini']
    # configs = ['Cree.ini']
    # configs = ['Russian.ini']
>>>>>>> 5ff17997664a24f2b652e76e4dcae2e24d048ec1

    for config in configs:
        # Parse the config file and call the sessions processor
        cfg = CorpusConfigParser()
        cfg.read(config)

        # Process by parsing the files and adding extracted data to the db
        c = CorpusProcessor(cfg, engine)
        c.process_corpus()

        # TODO: move not corpus-specific stuff out of this loop
        # Do the postprocessing
        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        update_age(cfg, engine)
        unify_timestamps(cfg, engine)
        unify_glosses(cfg, engine)
        unify_gender(cfg,engine)
        
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
    unify_roles(cfg,engine)

    print("Creating macrorole entries...")
    macrorole(cfg,engine)

    # print("Creating unique speaker table...")
    # unique_speaker(cfg,engine)

    # print("Populate foreign keys")
    # populate_fks(cfg,engine)


    # print("Populate foreign keys")
    # populate_fks(cfg,engine)


    print("--- %s seconds ---" % (time.time() - start_time))
