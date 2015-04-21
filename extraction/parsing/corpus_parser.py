#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Read corpus files in CHAT, Toolbox, or XML from a directory, parse their structure, write everything to JSON, and put one output file per corpus in a new folder "corpora_parsed" in the corpus directory.
This script only works if the module "corpus_parser_functions.py" is in the same directory. 

Usage: python3 corpus_parser.py -[hacCiIjJrty]   -->> -h or --help for usage

Note: When using -a, the script assumes all corpora to be present under corpora/   If not all corpora are present, specify in script (line 123) below which ones to parse.

Author: Robert Schikowski <robert.schikowski@uzh.ch>
Modification: Danica Pajovic <danica.pajovic@uzh.ch>
'''

import json
import os
import sys
import argparse
from corpus_parser_functions import parse_corpus


# table with subdirectory and format for each corpus
corpus_dic = {
     'Cree' : {'dir' : 'Cree/test/', 'format' : 'XML'},
     'Japanese_MiiPro' : {'dir' : 'Japanese_MiiPro/test/', 'format' : 'XML'},
     'Japanese_Miyata' : {'dir' : 'Japanese_Miyata/test/', 'format' : 'XML'},
     'Sesotho' : {'dir' : 'Sesotho/test/', 'format' : 'XML'},
    'Inuktitut' : {'dir' : 'Inuktitut/test/', 'format' : 'XML'},
     'Turkish_KULLD' : {'dir' : 'Turkish_KULLD/test/', 'format' : 'XML'},
     'Chintang' : {'dir' : 'Chintang/test/', 'format' : 'Toolbox'},
     'Indonesian' : {'dir' : 'Indonesian/test/', 'format' : 'Toolbox'},
     'Russian' : {'dir' : 'Russian/test/', 'format' : 'Toolbox'},
     'Yucatec' : {'dir' : 'Yucatec/test/', 'format' : 'XML'}
}    


def parser(corpus_name):
    rootdir='corpora/'
    
    if not os.path.exists('corpora_processed/parsed'):
        os.mkdir('corpora_processed/parsed')
    
    # parse corpora using functions from corpus_parser_functions
    if corpus_name in corpus_dic:
        corpus_dic[corpus_name]['dir'] = rootdir + corpus_dic[corpus_name]['dir']
        corpus_object = parse_corpus(corpus_name, corpus_dic[corpus_name]['dir'], corpus_dic[corpus_name]['format'])        
        
        with open('corpora_processed/parsed/' + corpus_name + '.json', 'w') as file:
            json.dump(corpus_object, file, ensure_ascii=False)
        with open('corpora_processed/parsed/' + corpus_name + '_prettyprint.txt', 'w') as file:
            # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
            file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))
            

def parserTest(corpus_name):
    '''Function used in tests/test_parsing.py'''
    
    rootdir='corpora/'
    
    if not os.path.exists('tests/parsing/output_test'):
        os.mkdir('tests/parsing/output_test')
    
    # parse corpora using functions from corpus_parser_functions
    if corpus_name in corpus_dic:
        corpus_dic[corpus_name]['dir'] = rootdir + corpus_dic[corpus_name]['dir']
        corpus_object = parse_corpus(corpus_name, corpus_dic[corpus_name]['dir'], corpus_dic[corpus_name]['format'])        
        
        with open('tests/parsing/output_test/' + corpus_name + '.json', 'w') as file:
            json.dump(corpus_object, file, ensure_ascii=False)
        with open('tests/parsing/output_test/' + corpus_name + '_prettyprint.txt', 'w') as file:
            # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
            file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))

            
        
if __name__ == '__main__':
    import sys    
    if len(sys.argv) == 1:
        print("\nUse  corpus_parser.py -h    to see how to run the script.\n")
    
    ## use argparse to define flags 
    parser_flag = argparse.ArgumentParser(description="Use the flags below to speficy which corpus should be parsed.")

    ## define the flags
    parser_flag.add_argument("-c","--cree",action="store_true",help="parse Cree corpus")
    parser_flag.add_argument("-j","--japaneseMP",action="store_true",help="parse Japanese MiiPro corpus")
    parser_flag.add_argument("-J","--japaneseMY", action="store_true",help="parse Japanese Myata corpus")
    parser_flag.add_argument("-s","--sesotho", action="store_true",help="parse Sesotho corpus")
    parser_flag.add_argument("-i","--inuktitut", action="store_true",help="parse Inuktitut corpus")
    parser_flag.add_argument("-t","--turkish", action="store_true",help="parse Turikish corpus")
    parser_flag.add_argument("-C","--chintang", action="store_true",help="parse Chintang corpus")
    parser_flag.add_argument("-I","--indonesian", action="store_true",help="parse Indonesian corpus")
    parser_flag.add_argument("-r","--russian", action="store_true",help="parse Russian corpus")
    parser_flag.add_argument("-y","--yucatec", action="store_true",help="parse Yucatec corpus")
    parser_flag.add_argument("-a", "--all", action="store_true", help="parse all corpora in folder corpora/")
    
    args = parser_flag.parse_args()
    
    # get the desired corpus via the flags
    if args.cree:
        parser("Cree")
    if args.japaneseMP:
        parser("Japanese_MiiPro")
    if args.japaneseMY:
        parser("Japanese_Miyata")
    if args.sesotho:
        parser("Sesotho")
    if args.inuktitut:
        parser("Inuktitut")
    if args.turkish:
        parser("Turkish_KULLD")
    if args.chintang:
        parser("Chintang")
    if args.indonesian:
        parser("Indonesian")
    if args.russian:
        parser("Russian")
    if args.yucatec:
        parser("Yucatec")
    if args.all:
        ## for now missing Yucatek and Turkish (to add!)
        corpora_to_parse = ['Inuktitut', 'Russian', 'Sesotho', 'Indonesian', 'Cree', 'Chintang', 'Japanese_MiiPro', 'Japanese_Miyata', 'Inuktitut']
        for corpus in corpora_to_parse:
            parser(corpus)
        
    
    
    
    
    
    
    