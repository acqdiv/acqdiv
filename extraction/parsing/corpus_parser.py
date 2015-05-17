#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Read corpus files in CHAT, Toolbox, or XML from directory corpora/, copy the structure from corpora/ to "parsing/LANGUAGE/input" and parse their structure, write everything to JSON, and put one output file per corpus in a new folder "parsing/LANGUAGE/output" in the main directory of the repository.
This script only works if the module "corpus_parser_functions.py" is in the same directory. 

Usage: python3 corpus_parser.py -[hacCiIjJrty]   -->> -h or --help for usage

Note: When using -a, the script assumes all corpora to be present under corpora/   If not all corpora are present, specify in script (line 165) below which ones to parse.

Author: Robert Schikowski <robert.schikowski@uzh.ch>
Modification: Danica Pajovic <danica.pajovic@uzh.ch>
'''

import json
import os
import sys
import argparse
from corpus_parser_functions import parse_corpus
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


        
def parser(corpus_name):
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
        
                    #corpus_object = parse_corpus(corpus_name, corpus_dic[corpus_name]['dir'], filename, corpus_dic[corpus_name]['format'])
                    corpus_object = parse_corpus(corpus_name, corpus_dic[corpus_name]['dir'], filename, corpus_dic[corpus_name]['format'])
          
                    with open('parsed/'+corpus_name + '/'+ filename[:-4]+'.json', 'w') as file:
                      json.dump(corpus_object, file, ensure_ascii=False)
                    with open('parsed/'+corpus_name + '/'+ filename[:-4]+ '_prettyprint.txt', 'w') as file:
                      # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
                      file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))
            

def parserTest(corpus_name):
    '''Function used in tests/test_parsing.py'''    
    rootdir='corpora/'
    
    # parse corpora using functions from corpus_parser_functions
    if corpus_name in corpus_dic_test:
        corpus_dic_test[corpus_name]['dir'] = rootdir + corpus_dic_test[corpus_name]['dir']
        corpus_object = parse_corpus(corpus_name, corpus_dic_test[corpus_name]['dir'], corpus_dic_test[corpus_name]['format'])        
        
        #with open('tests/parsing/'+corpus_name+'/output_test/' + corpus_name + '.json', 'w') as file:
        #    json.dump(corpus_object, file, ensure_ascii=False)
        with open('tests/parsing/'+corpus_name+'/' + corpus_name + '_prettyprint.txt', 'w') as file:
            # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
            file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))

            
        
if __name__ == '__main__':
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
        corpora_to_parse = ['Inuktitut', 'Russian', 'Sesotho', 'Indonesian', 'Cree', 'Chintang', 'Japanese_MiiPro', 'Japanese_Miyata']
        for corpus in corpora_to_parse:
            parser(corpus)
        
    
    
    
    
    
    
    