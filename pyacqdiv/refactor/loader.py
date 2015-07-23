""" Entry point for loading acqdiv corpora into the database
"""

from processors import *
from parsers import *
from database_backend import *

# TODO: setup the config files, e.g. Chintang.ini, Cree.ini...
#  - define the corpus/session-specific attributes in each config; see example in Chintang
#  - integrate metadata stuff

if __name__=="__main__":
    # Initialize database connection and drop and then create tables.
    # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
    engine = db_connect()
    create_tables(engine)

    # Parse the config file and call the sessions processor
    cfg = CorpusConfigParser()
    cfg.read('Chintang.ini')

    # Process by parsing the files and adding extracted data to the db
    c = CorpusProcessor(cfg, engine)
    c.process_corpus()


# TODO postprocessing tasks:
#  - metadata label unification?
#  - morphological label unification (i don't think this should be
#    in the parser, but in a separate post-processing module
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.