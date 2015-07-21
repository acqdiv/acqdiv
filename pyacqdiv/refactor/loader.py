""" Entry point for loading acqdiv corpora into the database
"""

import configparser
from processors import *

# TODO:

# set up config files
#  - create the config files, e.g. Chintang.ini, cree.ini...
#  - define the corpus/session-specific attributes in each config; see example in Chintang
#  - integrate metadata stuff

# write code to parse the acqdiv corpora config files

# call the processor on the config file(s)

CONFIGS = '*.ini'
optionxform = str # make config option names case sensitive

# c = Config() # returns list of config objects?
# for corpus in c:
#    cp = CorpusProcessor(corpus)


if __name__=="__main__":
    cfg = configparser.ConfigParser()
    cfg.read('Chintang.ini')
    # print(config.sections())
    c = CorpusProcessor(cfg)
    c.process_corpus()

# TODO FUTURE: postprocessing tasks
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.
#  - morphological label unification (i don't think this should be
#    in the parser, but in a separate post-processing module