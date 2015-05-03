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
     'Cree' : {'dir' : 'Cree/input/', 'format' : 'XML'},
     'Japanese_MiiPro' : {'dir' : 'Japanese_MiiPro/input/', 'format' : 'XML'},
     'Japanese_Miyata' : {'dir' : 'Japanese_Miyata/input/', 'format' : 'XML'},
     'Sesotho' : {'dir' : 'Sesotho/input/', 'format' : 'XML'},
    'Inuktitut' : {'dir' : 'Inuktitut/input/', 'format' : 'XML'},
     'Turkish_KULLD' : {'dir' : 'Turkish_KULLD/input/', 'format' : 'XML'},
     'Chintang' : {'dir' : 'Chintang/input/', 'format' : 'Toolbox'},
     'Indonesian' : {'dir' : 'Indonesian/input/', 'format' : 'Toolbox'},
     'Russian' : {'dir' : 'Russian/input/', 'format' : 'Toolbox'},
     'Yucatec' : {'dir' : 'Yucatec/input/', 'format' : 'XML'}
}

# table with subdirectory and format for each corpus (root directory for this is "tests/")
corpus_dic_test = {
     'Cree' : {'dir' : 'parsing/Cree/input_test', 'format' : 'XML'},
     'Japanese_MiiPro' : {'dir' : 'parsing/Japanese_MiiPro/input_test/', 'format' : 'XML'},
     'Japanese_Miyata' : {'dir' : 'parsing/Japanese_Miyata/input_test/', 'format' : 'XML'},
     'Sesotho' : {'dir' : 'parsing/Sesotho/input_test/', 'format' : 'XML'},
    'Inuktitut' : {'dir' : 'parsing/Inuktitut/input_test/', 'format' : 'XML'},
     'Turkish_KULLD' : {'dir' : 'parsing/Turkish_KULLD/input_test/', 'format' : 'XML'},
     'Chintang' : {'dir' : 'parsing/Chintang/input_test/', 'format' : 'Toolbox'},
     'Indonesian' : {'dir' : 'parsing/Indonesian/input_test/', 'format' : 'Toolbox'},
     'Russian' : {'dir' : 'parsing/Russian/input_test/', 'format' : 'Toolbox'},
     'Yucatec' : {'dir' : 'parsing/Yucatec/input_test/', 'format' : 'XML'}
}    

## create folder parsing/input/ and copy there everything that lies in corpora/
def copy(src, dest):
    src_lang = str(src).replace('corpora/','').replace('/','')
    
    if src_lang in corpus_dic:
        src = 'corpora/'+src_lang
        try:
            #shutil.copytree(src, dest, ignore=ignore_patterns('*.py', '*.sh', 'specificfile.file'))
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns('.DS_Store'))
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                print('Directory not copied. Error: %s' % e)
                
        
def parser(corpus_name):
    rootdir='parsing/'
    
    if not os.path.exists('parsing/'+corpus_name + '/ouput/'):
            os.mkdir('parsing/'+corpus_name + '/output/')
    
    # parse corpora using functions from corpus_parser_functions
    if corpus_name in corpus_dic:
        corpus_dic[corpus_name]['dir'] = rootdir + corpus_dic[corpus_name]['dir']
        corpus_object = parse_corpus(corpus_name, corpus_dic[corpus_name]['dir'], corpus_dic[corpus_name]['format'])        
        
        with open('parsing/'+corpus_name + '/output/' + corpus_name + '.json', 'w') as file:
            json.dump(corpus_object, file, ensure_ascii=False)
        with open('parsing/'+corpus_name + '/output/' + corpus_name + '_prettyprint.txt', 'w') as file:
            # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
            file.write(json.dumps(corpus_object, file, sort_keys=True, indent=4, ensure_ascii=False))
            

def parserTest(corpus_name):
    '''Function used in tests/test_parsing.py'''    
    
    rootdir='tests/'
    
    if not os.path.exists('tests/parsing/'+corpus_name+'/output_test'):
        os.mkdir('tests/parsing/'+corpus_name+'/output_test')
    
    # parse corpora using functions from corpus_parser_functions
    if corpus_name in corpus_dic_test:
        corpus_dic_test[corpus_name]['dir'] = rootdir + corpus_dic_test[corpus_name]['dir']
        corpus_object = parse_corpus(corpus_name, corpus_dic_test[corpus_name]['dir'], corpus_dic_test[corpus_name]['format'])        
        
        with open('tests/parsing/'+corpus_name+'/output_test/' + corpus_name + '.json', 'w') as file:
            json.dump(corpus_object, file, ensure_ascii=False)
        with open('tests/parsing/'+corpus_name+'/output_test/' + corpus_name + '_prettyprint.txt', 'w') as file:
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
        copy('corpora/Cree/', 'parsing/Cree/input')
        parser("Cree")
    if args.japaneseMP:
        copy('corpora/Japanese_MiiPro/', 'parsing/Japanese_MiiPro/input')
        parser("Japanese_MiiPro")
    if args.japaneseMY:
        copy('corpora/Japanese_Miyata/', 'parsing/Japanese_Miyata/input')
        parser("Japanese_Miyata")
    if args.sesotho:
        copy('corpora/Sesotho/', 'parsing/Sesotho/input')
        parser("Sesotho")
    if args.inuktitut:
        copy('corpora/Inuktitut/', 'parsing/Inuktitut/input')
        parser("Inuktitut")
    if args.turkish:
        copy('corpora/Turkish_KULLD/', 'parsing/Turkish_KULLD/input')
        parser("Turkish_KULLD")
    if args.chintang:
        copy('corpora/Chintang/', 'parsing/Chintang/input')
        parser("Chintang")
    if args.indonesian:
        copy('corpora/Indonesian/', 'parsing/Indonesian/input')
        parser("Indonesian")
    if args.russian:
        copy('corpora/Russian/', 'parsing/Russian/input')
        parser("Russian")
    if args.yucatec:
        copy('corpora/Yucatec/', 'parsing/Yucatec/input')
        parser("Yucatec")
    if args.all:
        ## for now missing Yucatek and Turkish (to add!)
        corpora_to_parse = ['Inuktitut', 'Russian', 'Sesotho', 'Indonesian', 'Cree', 'Chintang', 'Japanese_MiiPro', 'Japanese_Miyata']
        for corpus in corpora_to_parse:
            copy('corpora/'+corpus+'/', 'parsing/'+corpus+'/input')
            parser(corpus)
        
    
    
    
    
    
    
    