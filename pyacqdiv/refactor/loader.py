""" Entry point for loading acqdiv corpora into the database
"""

from processors import *
from parsers import *
from database_backend import *


# TODO:

# set up config files
#  - create the config files, e.g. Chintang.ini, cree.ini...
#  - define the corpus/session-specific attributes in each config; see example in Chintang
#  - integrate metadata stuff

if __name__=="__main__":
    # probably load up the database first, eh?
    # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate

    # parse the config file and call the sessions processor
    cfg = CorpusConfigParser()
    cfg.read('Chintang.ini')
    c = CorpusProcessor(cfg)
    c.process_corpus()


# TODO FUTURE: postprocessing tasks
#  - metadata label unification?
#  - morphological label unification (i don't think this should be
#    in the parser, but in a separate post-processing module
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.