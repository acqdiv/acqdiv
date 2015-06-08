# -*- coding: utf-8 -*-

## Given a directory generate an md5 hash for each file (including in subfolders of that directory).
## Useful for comparing file contents for files with possible different filenames.


''' Script to create tab-separated table of fingerprint info for each file of a given corpus.
    
    Printed format will be: corpusName \t fingerprint \t fileName \t Duplicate
    File generated will be saved under "corpora_processed/md5_fingerprints/md5_fingerprints_corpora.csv"
    
    
    Usage from main folder of repository: $ python3 extraction/md5_fingerprints/md5_fingerprints_2.py corpora/
    ====================================
    
    Author: Steven Moran <steven.moran@uzh.ch>
    Modified by: Danica Pajovic <danica.pajovic@uzh.ch>

'''

## ==========================================================================================================================================================
## IMPORTANT INFO:
## |
## +--> <corpora/> is a directory containing the language corpora as subdirectories.
## |
## +--> e.g. corpora/
##              |
##              +--> Indonesian/
##              +--> Yucatec/
##              +--> Russian/
##              +--> etc.
##
## The corpusName column in the generated csv-file then contains the path-name corpora/language_corpus/.
##
## >> For output to be written to terminal: un-escape lines 94 and 121.
## ==========================================================================================================================================================


import sys
import os
from os import path,makedirs
from path import Path as path
import collections
import codecs


## get corpora
try:
        if len(sys.argv) > 1:
                dir = sys.argv[1]
        else:
                print('You need to specify the corpora-directory as second argument when calling the script.\nPlease see script infile for more info.')

except OSError:
        print('There seems to be a problem, check md5_fingerprints.py infile for info about how to run the script.')
        
## make new folder where generated csv-file will be stored.
## NOTE: os.makedirs might for some people be os.mkdir
if not os.path.exists('corpora_processed/md5_fingerprints'):
    os.makedirs('corpora_processed/md5_fingerprints')
    
## create hash where fingerprint info for every file will be stored.
dups = collections.defaultdict(list)

## create md5 hash of each file.
def process(path):
    md5 = path.read_md5()
    result = [str(md5)]
    pathToFile = str(path.split()).replace('[','').replace(']','').replace("u'",'').replace("'",'')
        
    result.append(os.path.basename(pathToFile))
    dups[md5].append(os.path.split(pathToFile))
    

## go through every file in every folder (also subfolders) of a given directory.
def main(dir):
    for f in path(dir).walkfiles():
        ## to get all files except the hidden ones and .csv, .xlsx and .cdc files
        if not f.basename().startswith('.') and not f.basename().endswith('.csv') and not f.basename().endswith('.xlsx') and not f.basename().endswith('.cdc'):
        
        ## get only .xml, .cha and .txt files
        #if f.basename().endswith('.xml') or f.basename().endswith('.cha') or f.basename().endswith('.txt') and not f.basename().startswith('.'):
    
            process(f)
 
    

if __name__=="__main__":
    main(dir)
    
    outfile = codecs.open("corpora_processed/md5_fingerprints/md5_fingerprints_corpora.csv","w","utf-8")
    ## for first line in generated .csv file
    outfile.write("Corpus\tFingerprint of File\tFilename\tDuplicate\n")
    #print('Corpus\tFingerprint of File\tFilename\tDuplicate')
    
    # initialize defaultdict which will be later accessed to generate the output format.
    dirnames = collections.defaultdict(list)
    
    ## get path-name that consists of main directory and first subdirectory
    for k, v in list(dups.items()):        
        for (t1,t2) in v:
                pathName = t1.split("/")
                if len(pathName) > 1:
                        pathName = pathName[0]+"/"+pathName[1]
                else:
                        pathName = pathName[0]
                
                dirnames[(pathName,k)].append(t2)
    
    ## make sure the order in which the corpora are processed gets preserved:
    dirnames = collections.OrderedDict(sorted(dirnames.items()))
    
    for k,v in dirnames.items():
        ## to get only duplicate files use the below if-condition
        #if len(v) > 1:
        fileName = ' '.join(v)
        fileName = fileName.replace(" ","\t")
        fingerPrint = str(k).replace(k[0],"").replace("('', ","").replace('")','"').replace("')","'").replace("b'","'").replace('b"','"')
        pathName = k[0]
        
        #print(pathName+"\t"+fingerPrint+"\t"+fileName)
        
        ## write info to outfile
        outfile.write(pathName+"\t"+fingerPrint+"\t"+fileName+"\n")        
    outfile.close()






