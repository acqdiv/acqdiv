#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Read corpus files in CHAT, Toolbox, or XML from a directory, parse their structure, write everything to JSON, and put one output file per corpus in a new folder "corpora_parsed" in the corpus directory. This script only works if the module "corpus_parser_functions.py" is in the same directory. 

Usage: python3 corpus_parser.py -[cjJsitCIry]
Usage for help: python3 corpus_parser.py -h (or --help)

Author: Robert Schikowski <robert.schikowski@uzh.ch>
Modified by: Danica Pajovic <danica.pajovic@uzh.ch>
'''

import json
import os
import sys
import argparse
from corpus_parser_functions import parse_corpus



## get root directory from corpora from command line or assume "../Corpora" as the default
#if len(sys.argv) > 2:
#    rootdir = sys.argv[2]
#else:
#    rootdir = 'corpora/'

# TODO make paths to corpora more flexible?
## solution dp: use argpars
parser = argparse.ArgumentParser(description="Use the flags below to speficy which corpus should be parsed.")

## define the flags
parser.add_argument("-c","--cree",action="store_true",help="parse Cree corpus")
parser.add_argument("-j","--japaneseMP",action="store_true",help="parse Japanese MiiPro corpus")
parser.add_argument("-J","--japaneseMY", action="store_true",help="parse Japanese Myata corpus")
parser.add_argument("-s","--sesotho", action="store_true",help="parse Sesotho corpus")
parser.add_argument("-i","--inuktitut", action="store_true",help="parse Inuktitut corpus")
parser.add_argument("-t","--turkish", action="store_true",help="parse Turikish corpus")
parser.add_argument("-C","--chintang", action="store_true",help="parse Chintang corpus")
parser.add_argument("-I","--indonesian", action="store_true",help="parse Indonesian corpus")
parser.add_argument("-r","--russian", action="store_true",help="parse Russian corpus")
parser.add_argument("-y","--yucatec", action="store_true",help="parse Yucatec corpus")
#parser.add_argument("-d","--dir",action="store_true",help="use this when defining own copurs that should be parsed")
#
#parser.add_argument("corpus", type=str,help="use corpora/ as second argument when running the script.")

## parse arguments
args = parser.parse_args()


# table with subdirectory and format for each corpus
corpus_dic = {
     'Cree' : {'dir' : 'Cree/xml/', 'format' : 'XML'},
     'Japanese_MiiPro' : {'dir' : 'Japanese_MiiPro/test/', 'format' : 'XML'},
     'Japanese_Miyata' : {'dir' : 'Japanese_Miyata/xml/', 'format' : 'XML'},
     'Sesotho' : {'dir' : 'Sesotho/test/', 'format' : 'XML'},
     'Inuktitut' : {'dir' : 'Inuktitut/test/', 'format' : 'CHAT'},
     'Turkish_KULLD' : {'dir' : 'Turkish_KULLD/test/', 'format' : 'CHAT'},
     'Chintang' : {'dir' : 'Chintang/toolbox/', 'format' : 'Toolbox'},
    'Indonesian' : {'dir' : 'Indonesian/test/', 'format' : 'Toolbox'},
     'Russian' : {'dir' : 'Russian/test/', 'format' : 'Toolbox'},
     'Yucatec' : {'dir' : 'Yucatec/test/', 'format' : 'CHAT'}
}    

## save stdout to corpora_processed/parsed if this dir exists, otherwise create it.
if not os.path.exists('corpora_processed/parsed'):
    ## attention: os.makedirs might also be os.mkdir (didn't work for me (dp))
    os.makedirs('corpora_processed/parsed')

## get the desired corpus via the flags
if args.cree:
    corpus_name='Cree'
if args.japaneseMP:
    corpus_name='Japanese_MiiPro'
if args.japaneseMY:
    corpus_name='Japanese_Miyata'
if args.sesotho:
    corpus_name='Sesotho'
if args.inuktitut:
    corpus_name='Inuktitut'
if args.turkish:
    corpus_name='Turkish_KULLD'
if args.chintang:
    corpus_name='Chintang'
if args.indonesian:
    corpus_name='Indonesian'
if args.russian:
    corpus_name='Russian'
if args.yucatec:
    corpus_name='Yucatec'
#if args.dir:
#    args.corpus = rootdir


# parse corpora using functions from corpus_parser_functions
for name in corpus_dic:
    if corpus_name == name:
        rootdir = "corpora/"
        corpus_dic[corpus_name]['dir'] = rootdir + corpus_dic[corpus_name]['dir']
        corpus_object = parse_corpus(corpus_name,corpus_dic[corpus_name]['dir'], corpus_dic[corpus_name]['format'])
                
        with open('corpora_processed/parsed/' + corpus_name + '.json', 'w') as file:
                json.dump(corpus_object, file, ensure_ascii=False)
        with open('corpora_processed/parsed/' + corpus_name + '_prettyprint.txt', 'w') as file:
                # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
            print(json.dumps(corpus_object, sort_keys=True, indent=4, ensure_ascii=False), file=file)
            
