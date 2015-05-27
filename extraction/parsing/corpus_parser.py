#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Read corpus files in CHAT, Toolbox, or XML from directory corpora/, copy the structure from corpora/ to "parsing/LANGUAGE/input" and parse their structure, write everything to JSON,
and put output files per corpus in a new folder "parsed/LANGUAGE/" in the main directory of the repository.

This script only works if the module "corpus_parser_functions.py" is in the same directory. 

Usage: python3 corpus_parser.py -[hacCiIjJrty]   -->> -h or --help for usage

Note: When using -a, the script assumes all corpora to be present under corpora/   If not all corpora are present, specify inline below (line 215 and 219) which ones to parse.

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
            json.dump(corpus_object, file, ensure_ascii=False)
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
                    for elem in parse_corpus(corpus_name,corpus_dic_test[corpus_name]['dir'],filepath,corpus_dic_test[corpus_name]['format']):
                        corpus_object = elem
                        
                        with open('tests/parsing/'+corpus_name+'/' + corpus_name + '_prettyprint.txt', 'w') as file:
                            # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
                            file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))

            
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("\nUse  corpus_parser.py -h    to see how to run the script.\n")
        
    else:
        
        ## use argparse to define flags 
        parser_flag = argparse.ArgumentParser(description="Use the flags below to specify which corpus to parse.")
    
        ## optional flags
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
        
        
        ## first check what corpus should be parsed (via the argparse flags), then ask user to specify the parser output:
        ## 'one' for one big json output file per corpus
        ## 'many' for a json output file per file in corpora/LANGUAGE
        if args.cree:
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Cree")
            elif parser_output == 'many':
                parser_per_file("Cree")
        if args.japaneseMP:
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if corpus_to_parse == 'one':
                parser_one_json("Japanese_MiiPro")
            elif corpora_to_parse == 'many':
                parser_per_file("Japanese_MiiPro")
        if args.japaneseMY:
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Japanese_Miyata")
            elif parser_output == 'many':
                parser_per_file("Japanese_Miyata")
        if args.sesotho:
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Sesotho")
            elif parser_output == 'many':
                parser_per_file("Sesotho")
        if args.inuktitut:
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Inuktitut")
            elif parser_output == 'many':
                parser_per_file("Inuktitut")
        if args.turkish:
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Turkish_KULLD")
            elif parser_output == 'many':
                parser_per_file("Turkish_KULLD")
        if args.chintang:
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Chintang")
            elif parser_output == 'many':
                parser_per_file("Chintang")
        if args.indonesian:
            parser_output = input("\nPlease specify the parser output:\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Indonesian")
            elif parser_output == 'many':
                parser_per_file("Indonesian")
        if args.russian:
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Russian")
            elif parser_output == 'many':
                parser_per_file("Russian")
        if args.yucatec:
            parser_output = input("\nPlease specify the parser output:\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                parser_one_json("Yucatec")
            elif parser_output == 'many':
                parser_per_file("Yucatec")
        if args.all:
            # to add: Yucatec!
            parser_output = input("\nPlease specify the parser output:\n\nType 'one' for one big json file per corpus.\nType 'many' for one json file per each file in a corpus.\nYour choice: ")
            if parser_output == 'one':
                corpora_to_parse = ['Inuktitut', 'Russian', 'Sesotho', 'Indonesian', 'Cree', 'Chintang', 'Japanese_MiiPro', 'Japanese_Miyata', 'Turkish_KULLD']
                for corpus in corpora_to_parse:
                    parser_one_json(corpus)
            if parser_output == 'many':
                corpora_to_parse = ['Inuktitut', 'Russian', 'Sesotho', 'Indonesian', 'Cree', 'Chintang', 'Japanese_MiiPro', 'Japanese_Miyata', 'Turkish_KULLD']
                for corpus in corpora_to_parse:
                    parser_per_file(corpus)
                
    

    
    
    
    
    