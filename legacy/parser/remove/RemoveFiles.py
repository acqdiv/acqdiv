import sys
import os
from os import path,makedirs
from path import Path as path
import codecs
import re


''' Program that deletes files from a directory that are mentioned in an inputfile.
    
    Usage: $ python3 RemoveFiles.py filename directory
    
    
    where <filename> is the file with the names of the files that should be deleted.
    +--> Note: for Yucatec it is 'notes/Yucatec_char_files_to_delete.txt'
    
    and   <directory> is the directory where all the files are located ('cha/' in our case for Yucatec)
    
    
    Author: Danica Pajovic <danica.pajovic@uzh.ch>
    '''
    
    

## get filenames to delete from file (file is first argument from stdin)
infile = codecs.open(sys.argv[1], 'r', 'utf-8')
files_to_delete = []

## get directory where all the files are located (directory is second argument from stdin)
dir = sys.argv[2]


## get names of files that should be deleted.
for line in infile:
    line = line.strip()
    files_to_delete.append(line)

def main(dir):
    for f in path(dir).walkfiles():
        filename = re.search(r'/(.*?\.txt)', str(f))
        if filename:
            if filename.group(1) in files_to_delete:
                os.remove(f)
                
            
if __name__=="__main__":
    main(dir)
    
    