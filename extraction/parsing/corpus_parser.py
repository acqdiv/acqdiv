#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Read corpus files in CHAT, Toolbox, or XML from directory corpora/, copy the structure from corpora/ to "parsing/LANGUAGE/input" and parse their structure, write everything to JSON,
and put output files per corpus in a new folder "parsed/LANGUAGE/" in the main directory of the repository.

This script only works if the module "corpus_parser_functions.py" is in the same directory. 

Usage: python3 corpus_parser.py --LANGUAGE=(one|many)   -->> -h or --help for usage

where LANGUAGE =
--cree
--japanMP
--japanMY
--sesotho
--inuk
--turkish
--chintang
--indones
--russian
--yucatec
--all

Note: When using -a, the script assumes all corpora to be present under corpora/   If not all corpora are present, specify inline below (line 246 and 250) which ones to parse.

Author: Robert Schikowski <robert.schikowski@uzh.ch>
Modification: Danica Pajovic <danica.pajovic@uzh.ch>
'''

import json
import os
import sys
import argparse
from corpus_parser_functions import parse_corpus_per_file, parse_corpus
import shutil
import errno



# table with subdirectory and format for each corpus (root directory for this is "parsing/")
corpus_dic = {
     'Cree' : {'dir' : 'Cree/', 'format' : 'XML'},
     'Japanese_MiiPro' : {'dir' : 'Japanese_MiiPro/', 'format' : 'XML'},
     'Japanese_Miyata' : {'dir' : 'Japanese_Miyata/', 'format' : 'XML'},
     'Sesotho' : {'dir' : 'Sesotho/', 'format' : 'XML'},
     'Inuktitut' : {'dir' : 'Inuktitut/', 'format' : 'XML'},
     'Turkish_KULLD' : {'dir' : 'Turkish_KULLD/', 'format' : 'XML'},
     'Chintang' : {'dir' : 'Chintang/', 'format' : 'Toolbox'},
     'Indonesian' : {'dir' : 'Indonesian/', 'format' : 'Toolbox'},
     'Russian' : {'dir' : 'Russian/', 'format' : 'Toolbox'},
     'Yucatec' : {'dir' : 'Yucatec/', 'format' : 'XML'}
}

# table with subdirectory and format for each corpus (root directory for this is "tests/")
corpus_dic_test = {
     'Cree' : {'dir' : 'testfiles/Cree/', 'format' : 'XML'},
     'Japanese_MiiPro' : {'dir' : 'testfiles/Japanese_MiiPro/', 'format' : 'XML'},
     'Japanese_Miyata' : {'dir' : 'testfiles/Japanese_Miyata/', 'format' : 'XML'},
     'Sesotho' : {'dir' : 'testfiles/Sesotho/', 'format' : 'XML'},
     'Inuktitut' : {'dir' : 'testfiles/Inuktitut/', 'format' : 'XML'},
     'Turkish_KULLD' : {'dir' : 'testfiles/Turkish_KULLD/', 'format' : 'XML'},
     'Chintang' : {'dir' : 'testfiles/Chintang/', 'format' : 'Toolbox'},
     'Indonesian' : {'dir' : 'testfiles/Indonesian/', 'format' : 'Toolbox'},
     'Russian' : {'dir' : 'testfiles/Russian/', 'format' : 'Toolbox'},
     'Yucatec' : {'dir' : 'testfiles/Yucatec/', 'format' : 'XML'}
}    

# output of parser_one_json() is one big json file per corpus
def parser_one_json(corpus_name):
    rootdir='corpora/'
    
    if not os.path.exists('parsed/'+corpus_name + '/'):
            os.makedirs('parsed/'+corpus_name + '/')
    
    # parse corpora using functions from corpus_parser_functions
    if corpus_name in corpus_dic:
        corpus_dic[corpus_name]['dir'] = rootdir + corpus_dic[corpus_name]['dir']
        corpus_object = parse_corpus(corpus_name, corpus_dic[corpus_name]['dir'], corpus_dic[corpus_name]['format'])        
        
        with open('parsed/'+corpus_name + '/' + corpus_name + '.json', 'w') as file:
            json.dump(corpus_object, file, ensure_ascii=False, indent=4)
        #with open('parsed/'+corpus_name + '/' + corpus_name + '_prettyprint.txt', 'w') as file:
        #    # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
        #    file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))
            

# output of parser_per_file() is a json file per file in corpora/LANGUAGE   
def parser_per_file(corpus_name):
    rootdir='corpora/'
    
    if not os.path.exists('parsed/'+corpus_name + '/'):
            os.makedirs('parsed/'+corpus_name + '/')
    
    # parse corpora using functions from corpus_parser_functions
    if corpus_name in corpus_dic:
        corpus_dic[corpus_name]['dir'] = rootdir + corpus_dic[corpus_name]['dir']
        for root, subs, files in os.walk(corpus_dic[corpus_name]['dir']):
            for file in files:
                filepath = os.path.join(root, file)
                filename = os.path.basename(filepath)
                if filename.endswith('.xml') or filename.endswith('.txt'):
                    for elem in parse_corpus_per_file(corpus_name, corpus_dic[corpus_name]['dir'],filepath, corpus_dic[corpus_name]['format']):
                        corpus_object = elem
                        
                        ## write outfiles with file name structure: filename.json or filename_prettyprint.txt
                        with open('parsed/'+corpus_name + '/'+ filename[:-4]+'.json', 'w') as file:
                          json.dump(corpus_object, file, ensure_ascii=False)
                        #with open('parsed/'+corpus_name + '/'+ filename[:-4]+ '_prettyprint.txt', 'w') as file:
                        #  # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
                        #  file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))
            

def parserTest(corpus_name):
    '''Function used in tests/test_parsing.py'''    
    rootdir='corpora/'
    
    # parse test corpora using functions from corpus_parser_functions
    if corpus_name in corpus_dic_test:
        corpus_dic_test[corpus_name]['dir'] = rootdir + corpus_dic_test[corpus_name]['dir']
        for root, subs, files in os.walk(corpus_dic_test[corpus_name]['dir']):
            for file in files:
                filepath = os.path.join(root,file)
                filename = os.path.basename(filepath)
                if filename.endswith('.xml') or filename.endswith('.txt'):
                    for elem in parse_corpus_per_file(corpus_name,corpus_dic_test[corpus_name]['dir'],filepath,corpus_dic_test[corpus_name]['format']):
                        corpus_object = elem
                        
                        with open('tests/parsing/'+corpus_name+'/' + corpus_name + '_prettyprint.txt', 'w') as file:
                            # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
                            file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))

            
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("\nUse  corpus_parser.py -h    to see how to run the script.\nExample usage: $ python3 extraction/parsing/corpus_parser.py --cree=one\n")
        
    else:
        
        ## use argparse to define flags 
        parser_flag = argparse.ArgumentParser(description="Use the flags below to specify which corpus to parse, e.g. --cree=one (for one big json file) or --cree=many (for many json files)")
    
        ## optional flags
        parser_flag.add_argument("--cree", nargs=1,help="parse Cree corpus")
        parser_flag.add_argument("--japanMP", nargs=1,help="parse Japanese MiiPro corpus")
        parser_flag.add_argument("--japanMY", nargs=1,help="parse Japanese Myata corpus")
        parser_flag.add_argument("--sesotho", nargs=1, help="parse Sesotho corpus")
        parser_flag.add_argument("--inuktitut", nargs=1,help="parse Inuktitut corpus")
        parser_flag.add_argument("--turkish", nargs=1, help="parse Turikish corpus")
        parser_flag.add_argument("--chintang", nargs=1, help="parse Chintang corpus")
        parser_flag.add_argument("--indonesian", nargs=1, help="parse Indonesian corpus")
        parser_flag.add_argument("--russian", nargs=1, help="parse Russian corpus")
        parser_flag.add_argument("--yucatec", nargs=1, help="parse Yucatec corpus")
        parser_flag.add_argument("--all", nargs=1, help="parse all corpora in folder corpora/")
        
        args = parser_flag.parse_args()
        
        
        ## for each language/corpus defined, check what output option has been chosen and parse accordingly:
        ## 'one' for one big json output file per corpus
        ## 'many' for a json output file per file in corpora/LANGUAGE
        
        
        if args.cree:
            if args.cree[0] == 'one':
                parser_one_json("Cree")
            elif args.cree[0] == 'many':
                parser_per_file("Cree")
            elif args.cree[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--cree=one for one big json file per corpus\n--cree=many for a json file per file in the corpus\n')
            
        if args.japanMP:
            if args.japanMP[0] == 'one':
                parser_one_json("Japanese_MiiPro")
            elif args.japanMP[0] == 'many':
                parser_per_file("Japanese_MiiPro")
            elif args.japanMP[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--japanMP=one for one big json file per corpus\n--japanMP=many for a json file per file in the corpus\n')
            
        if args.japanMY:
            if args.japanMY[0] == 'one':
                parser_one_json("Japanese_Miyata")
            elif args.japanMY[0] == 'many':
                parser_per_file("Japanese_Miyata")
            elif args.japanM>[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--japanMY=one for one big json file per corpus\n--japanMY=many for a json file per file in the corpus\n')
            
        if args.sesotho:
            if args.sesotho[0] == 'one':
                parser_one_json("Sesotho")
            elif args.sesotho[0] == 'many':
                parser_per_file("Sesotho")
            elif args.sesotho[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--sesotho=one for one big json file per corpus\n--sesotho=many for a json file per file in the corpus\n')
            
        if args.inuktitut:
            if args.inuktitut[0] == 'one':
                parser_one_json("Inuktitut")
            elif args.inuktitut == 'many':
                parser_per_file("Inuktitut")
            elif args.inuktitut[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--inuk=one for one big json file per corpus\n--inuk=many for a json file per file in the corpus\n')
        
        if args.turkish:    
            if args.turkish[0] == 'one':
                parser_one_json("Turkish_KULLD")
            elif args.turkish[0] == 'many':
                parser_per_file("Turkish_KULLD")
            elif args.turkish[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--turkish=one for one big json file per corpus\n--turkish=many for a json file per file in the corpus\n')
            
        if args.chintang:
            if args.chintang[0] == 'one':
                parser_one_json("Chintang")
            elif args.chintang == 'many':
                parser_per_file("Chintang")
            elif args.chintang[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--chintang=one for one big json file per corpus\n--chintang=many for a json file per file in the corpus\n')
            
        if args.indonesian:
            if args.indonesian[0] == 'one':
                parser_one_json("Indonesian")
            elif args.indonesian[0] == 'many':
                parser_per_file("Indonesian")
            elif args.indonesian[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--indones=one for one big json file per corpus\n--indones=many for a json file per file in the corpus\n')
            
        if args.russian:
            if args.russian[0] == 'one':
                parser_one_json("Russian")
            elif args.russian[0] == 'many':
                parser_per_file("Russian")
            elif args.russian[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--russian=one for one big json file per corpus\n--russian=many for a json file per file in the corpus\n')
            
        if args.yucatec:
            if args.yucatec[0] == 'one':
                parser_one_json("Yucatec")
            elif args.yucatec[0] == 'many':
                parser_per_file("Yucatec")
            elif args.yucatec[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--yucatec=one for one big json file per corpus\n--yucatec=many for a json file per file in the corpus\n')
            
        if args.all:
            if args.all[0] == 'one':
                # to add: Yucatec!
                corpora_to_parse = ['Inuktitut', 'Russian', 'Sesotho', 'Indonesian', 'Cree', 'Chintang', 'Japanese_MiiPro', 'Japanese_Miyata', 'Turkish_KULLD']
                for corpus in corpora_to_parse:
                    parser_one_json(corpus)
            elif args.all[0] == 'many':
                corpora_to_parse = ['Inuktitut', 'Russian', 'Sesotho', 'Indonesian', 'Cree', 'Chintang', 'Japanese_MiiPro', 'Japanese_Miyata', 'Turkish_KULLD']
                for corpus in corpora_to_parse:
                    parser_per_file(corpus)
            elif args.all[0] not in ['one', 'many']:
                print('\nPlease specify the json output:\n--all=one for one big json file per corpus\n--all=many for a json file per file in the corpus\n')
                
    

    
    
    
    
    