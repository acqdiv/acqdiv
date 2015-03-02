#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Read corpus files in CHAT, Toolbox, or XML from a directory, parse their structure, write everything to JSON, and put one output file per corpus in a new folder "corpora_parsed" in the corpus directory. This script only works if the module "corpus_parser_functions.py" is in the same directory. 

Usage: python3 corpus_parser.py (corpus/directory/)

Author: Robert Schikowski <robert.schikowski@uzh.ch>
'''

import json
import os
import sys
from corpus_parser_functions import parse_corpus

# TODO make paths to corpora more flexible?

# get root directory from corpora from command line or assume "../Corpora" as the default
if len(sys.argv) > 1:
    rootdir = sys.argv[1]
else:
    rootdir = 'corpora/'

# table with subdirectory and format for each corpus
corpus_dic = {
    # 'Cree' : {'dir' : 'Cree/xml/', 'format' : 'XML'},
    'Japanese_MiiPro' : {'dir' : 'Japanese_MiiPro/test/', 'format' : 'XML'},
    # 'Japanese_Miyata' : {'dir' : 'Japanese_Miyata/xml/', 'format' : 'XML'},
    # 'Sesotho' : {'dir' : 'Sesotho/test/', 'format' : 'XML'},
    # 'Inuktitut' : {'dir' : 'Inuktitut/test/', 'format' : 'CHAT'},
    # 'Turkish_KULLD' : {'dir' : 'Turkish_KULLD/test/', 'format' : 'CHAT'},
    # 'Chintang' : {'dir' : 'Chintang/toolbox/', 'format' : 'Toolbox'},
    #'Indonesian' : {'dir' : 'Indonesian/test/', 'format' : 'Toolbox'},
    # 'Russian' : {'dir' : 'Russian/test/', 'format' : 'Toolbox'},
    # 'Yucatec' : {'dir' : 'Yucatec/test/', 'format' : 'CHAT'}
}    

if not os.path.exists('corpora_processed/parsed'):
    os.mkdir('corpora_processed/parsed')


# parse corpora using functions from corpus_parser_functions
for corpus_name in corpus_dic:
    corpus_dic[corpus_name]['dir'] = rootdir + corpus_dic[corpus_name]['dir']
    corpus_object = parse_corpus(corpus_name, corpus_dic[corpus_name]['dir'], corpus_dic[corpus_name]['format'])        
    
    with open('corpora_processed/parsed/' + corpus_name + '.json', 'w') as file:
        json.dump(corpus_object, file, ensure_ascii=False)
    with open('corpora_processed/parsed/' + corpus_name + '_prettyprint.txt', 'w') as file:
        # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
        print(json.dumps(corpus_object, sort_keys=True, indent=4, ensure_ascii=False), file=file)
