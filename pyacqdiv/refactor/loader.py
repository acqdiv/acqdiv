""" Entry point for loading acqdiv corpora into the database
"""

from processors import *
from parsers import *

# TODO:

# set up config files
#  - create the config files, e.g. Chintang.ini, cree.ini...
#  - define the corpus/session-specific attributes in each config; see example in Chintang
#  - integrate metadata stuff

if __name__=="__main__":
    cfg = CorpusConfigParser()
    cfg.read('Chintang.ini')
    c = CorpusProcessor(cfg)
    c.process_corpus()


# TODO FUTURE: postprocessing tasks
#  - metadata label unification?
#  - morphological label unification (i don't think this should be
#    in the parser, but in a separate post-processing module
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.