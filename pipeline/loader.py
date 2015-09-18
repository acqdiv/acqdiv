""" Entry point for loading acqdiv corpora into the database
"""

from processors import *
from parsers import *
from database_backend import *
import time

# TODO: setup the config files, e.g. Chintang.ini, Cree.ini...
#  - define the corpus/session-specific attributes in each config; see example in Chintang
#  - integrate metadata stuff

if __name__=="__main__":
    start_time = time.time()

    # Initialize database connection and drop and then create tables on each call.
    # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
    engine = db_connect()
    create_tables(engine)

    # configs = ['Chintang.ini', 'Cree.ini', 'Indonesian.ini', 'Inuktitut.ini', 'Russian.ini', 'Japanese_Miyata.ini']
    # configs = ['Chintang.ini']
    # configs = ['Cree.ini']
    # configs = ['Inuktitut.ini']
    # configs = ['Indonesian.ini']
    # configs = ['Japanese_Miyata.ini']
    configs = ['Japanese_MiiPro.ini']
    # configs = ['Russian.ini']
    # configs = ['Sesotho.ini']


    for config in configs:
        # Parse the config file and call the sessions processor
        cfg = CorpusConfigParser()
        cfg.read(config)

        # Process by parsing the files and adding extracted data to the db
        c = CorpusProcessor(cfg, engine)
        c.process_corpus()

        # TODO: call the post-processor

    print("--- %s seconds ---" % (time.time() - start_time))
